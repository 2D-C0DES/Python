# VERRSION = 3.0

# Define Simulation Parameters

import simpy
import random
import matplotlib.pyplot as plt
from collections import defaultdict

# --- Simulation parameters --- #
SIM_DURATION = 50        # seconds
MESSAGE_INTERVAL = 5     # publish interval (s)
NETWORK_DELAY_MEAN = 1.0 # average delay (s)
PACKET_DROP_PROB = 0.005  # 10% network packet loss 


NUM_PUBLISHERS = 5
NUM_SUBSCRIBERS = 5
QOS_LEVEL = 2

# QoS(1,2) parameters
ACK_TIMEOUT = 3
MAX_RETRIES = 2


# Define Message and Metrics Classes

class Message:
    """MQTT message representation."""
    def __init__(self, topic, payload, qos, sender_id, message_id, timestamp):
        self.topic = topic
        self.payload = payload
        self.qos = qos
        self.sender_id = sender_id
        self.timestamp = timestamp
        self.message_id = message_id

        # --- METRICS ADDITION ---
        self.sent_time = timestamp


class Metrics:
    def __init__(self):
        # Baseline
        self.logical_messages_sent = 0

        # Delivery
        self.logical_messages_delivered = 0
        self.failed_messages = 0

        # QoS behavior
        self.retries = defaultdict(int)
        self.duplicate_deliveries = 0

        # Timing
        self.end_to_end_latency = []
        self.ack_latency = []

    # -------- Recording helpers --------
    def record_send(self, msg_id):
        self.logical_messages_sent += 1

    def record_delivery(self, sent_time, recv_time):
        self.logical_messages_delivered += 1
        self.end_to_end_latency.append(recv_time - sent_time)

    def record_failure(self):
        self.failed_messages += 1

    def record_retry(self, msg_id):
        self.retries[msg_id] += 1

    def record_duplicate(self):
        self.duplicate_deliveries += 1

    def record_ack_latency(self, sent_time, ack_time):
        self.ack_latency.append(ack_time - sent_time)

    # --- BACKWARD COMPATIBILITY ---
    def record_loss(self):
        self.failed_messages += 1

    # -------- Derived metrics --------
    @property
    def delivery_ratio(self):
        if self.logical_messages_sent == 0:
            return 0
        return self.logical_messages_delivered / self.logical_messages_sent

    @property
    def retries_per_message(self):
        if not self.retries:
            return 0
        return sum(self.retries.values()) / len(self.retries)


# Network Model (Delay + Drop)

def network_send(env, delay_mean, drop_prob):
    """Simulate network latency and packet loss."""
    yield env.timeout(random.expovariate(1.0 / delay_mean))
    if random.random() < drop_prob:
        raise Exception("PacketDropped")


# Broker Process

class Broker:
    def __init__(self, env, metrics):
        self.env = env
        self.subscriptions = defaultdict(list)
        self.metrics = metrics

        self.qos1_delivered = set()
        self.qos2_store = {}


        # Track QoS1 delivery per subscriber
        self.qos1_delivered_per_sub = defaultdict(set)  # msg_id -> set of subscriber IDs

    def subscribe(self, client, topic):
        self.subscriptions[topic].append(client)
        print(f"[{self.env.now:.2f}] {client.client_id} subscribed to {topic}")

    def receive_publish(self, message, publisher):
        if message.qos == 0:
            self.env.process(self._deliver(message))

        elif message.qos == 1:
            self.env.process(self._handle_qos1(message, publisher))

        elif message.qos == 2:
            self.env.process(self._handle_qos2_publish(message, publisher))

    # ---------- QoS 1 ----------


    # first QoS1 attempt give max duplicate deliveries

    # def _handle_qos1(self, message, publisher):
    #     delivered = yield self.env.process(self._deliver(message))
    #     if delivered:
    #         try:
    #             yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
    #             publisher.receive_puback(message.message_id)
    #         except Exception:
    #             pass

# Second QoS1 attempt give 2nd highest duplicate deliveries

    # def _handle_qos1(self, message, publisher):
    # # If already delivered earlier, do NOT deliver again
    #     if message.message_id in self.qos1_delivered:
    #         try:
    #             yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
    #             publisher.receive_puback(message.message_id)
    #         except Exception:
    #             pass
    #         return

    #     # First-time delivery
    #     delivered = yield self.env.process(self._deliver(message))

    #     if delivered:
    #         # Mark as delivered to prevent duplicates on retry
    #         self.qos1_delivered.add(message.message_id)

    #         try:
    #             yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
    #             publisher.receive_puback(message.message_id)
    #         except Exception:
    #             pass

# third QoS1 attempt give 3rd highest duplicate deliveries

    def _handle_qos1(self, message, publisher):
        delivered_to_all = True

        for sub in self.subscriptions.get(message.topic, []):
            # Skip subscribers who already got the message
            if sub.client_id in self.qos1_delivered_per_sub[message.message_id]:
                continue

            try:
                yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
                sub.receive_message(message)
                self.metrics.record_delivery(message.sent_time, self.env.now)
                self.qos1_delivered_per_sub[message.message_id].add(sub.client_id)
            except Exception:
                self.metrics.record_failure()
                delivered_to_all = False

        # Send PUBACK to publisher only if all subscribers got the message
        if delivered_to_all:
            try:
                yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
                publisher.receive_puback(message.message_id)
            except Exception:
                # PUBACK loss → publisher will retry
                pass



    # ---------- QoS 2 ----------
    def _handle_qos2_publish(self, message, publisher):
        if message.message_id in self.qos2_store:
            return

        self.qos2_store[message.message_id] = {
            "state": "PUBREC_SENT",
            "message": message
        }

        try:
            yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
            publisher.receive_pubrec(message.message_id)
        except Exception:
            pass

    def receive_pubrel(self, message_id, publisher):
        if message_id not in self.qos2_store:
            return

        message = self.qos2_store[message_id]["message"]
        self.env.process(self._finalize_qos2(message, publisher))

    def _finalize_qos2(self, message, publisher):
        yield self.env.process(self._deliver(message))
        try:
            yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
            publisher.receive_pubcomp(message.message_id)
        except Exception:
            pass

        del self.qos2_store[message.message_id]

    # ---------- Delivery ----------
    def _deliver(self, message):
        success = False
        for sub in self.subscriptions.get(message.topic, []):
            try:
                yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
                sub.receive_message(message)
                self.metrics.record_delivery(message.sent_time, self.env.now)
                success = True

            except GeneratorExit:
                raise

            except Exception:
                self.metrics.record_loss()

        return success


# Client Process (Publisher / Subscriber)

class Client:
    def __init__(self, env, broker, client_id, role, topic):
        self.env = env
        self.broker = broker
        self.client_id = client_id
        self.role = role
        self.topic = topic

        self.received_ids = set()
        self.qos1_pending = {}
        self.qos2_pending = {}

        if role == "subscriber":
            broker.subscribe(self, topic)
        else:
            env.process(self.publisher_loop())

    def publisher_loop(self):
        msg_counter = 0
        while True:
            msg_counter += 1
            msg_id = f"{self.client_id}-{msg_counter}"

            msg = Message(
                self.topic,
                f"data-{msg_id}",
                QOS_LEVEL,
                self.client_id,
                msg_id,
                self.env.now
            )

            # --- METRICS ADDITION ---
            self.broker.metrics.record_send(msg_id)

            if msg.qos == 0:
                self.broker.receive_publish(msg, self)

            elif msg.qos == 1:
                self.qos1_pending[msg_id] = msg
                self.env.process(self._qos1_send(msg))

            elif msg.qos == 2:
                self.qos2_pending[msg_id] = msg
                self._qos2_send(msg)

            yield self.env.timeout(MESSAGE_INTERVAL)

    # ---------- QoS 1 ----------
    def _qos1_send(self, msg):
        for _ in range(MAX_RETRIES + 1):
            self.broker.receive_publish(msg, self)
            self.broker.metrics.record_retry(msg.message_id)
            yield self.env.timeout(ACK_TIMEOUT)
            if msg.message_id not in self.qos1_pending:
                return

        self.broker.metrics.record_failure()
        del self.qos1_pending[msg.message_id]

    def receive_puback(self, message_id):
        msg = self.qos1_pending.pop(message_id, None)
        if msg:
            self.broker.metrics.record_ack_latency(msg.sent_time, self.env.now)

    # ---------- QoS 2 ----------
    def _qos2_send(self, msg):
        self.broker.receive_publish(msg, self)

    def receive_pubrec(self, message_id):
        self.env.process(self._send_pubrel(message_id))

    def _send_pubrel(self, message_id):
        try:
            yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
            self.broker.receive_pubrel(message_id, self)
            self.broker.metrics.record_retry(message_id)
        except Exception:
            pass

    def receive_pubcomp(self, message_id):
        msg = self.qos2_pending.pop(message_id, None)
        if msg:
            self.broker.metrics.record_ack_latency(msg.sent_time, self.env.now)
        print(f"[{self.env.now:.2f}] {self.client_id} received PUBCOMP for {message_id}")

    # ---------- Subscriber ----------
    def receive_message(self, message):
        if message.message_id in self.received_ids:
            self.broker.metrics.record_duplicate()
            return

        self.received_ids.add(message.message_id)
        print(f"[{self.env.now:.2f}] {self.client_id} received {message.payload}")


# Simulation Setup

def run_simulation():
    env = simpy.Environment()
    metrics = Metrics()
    broker = Broker(env, metrics)

    for i in range(NUM_SUBSCRIBERS):
        Client(env, broker, f"Sub-{i}", "subscriber", "topic/sensor")

    for i in range(NUM_PUBLISHERS):
        Client(env, broker, f"Pub-{i}", "publisher", "topic/sensor")

    env.run(until=SIM_DURATION)
    return metrics


# Analyse & Plot Metrics

def plot_results(metrics):
    print("\n--- Simulation Results ---")
    print(f"Logical messages sent     : {metrics.logical_messages_sent}")
    print(f"Messages delivered        : {metrics.logical_messages_delivered}")
    print(f"Delivery ratio            : {metrics.delivery_ratio:.2f}")
    print(f"Failed messages           : {metrics.failed_messages}")
    print(f"Retries per message       : {metrics.retries_per_message:.2f}")
    print(f"Duplicate deliveries      : {metrics.duplicate_deliveries}")

    if metrics.end_to_end_latency:
        avg_latency = sum(metrics.end_to_end_latency) / len(metrics.end_to_end_latency)
        print(f"Avg end-to-end latency    : {avg_latency:.2f}s")

        plt.hist(metrics.end_to_end_latency, bins=10, edgecolor="black")
        plt.title("End-to-End Latency Distribution")
        plt.xlabel("Latency (s)")
        plt.ylabel("Frequency")
        plt.show()

    if metrics.ack_latency:
        print(f"Avg ACK latency           : {sum(metrics.ack_latency)/len(metrics.ack_latency):.2f}s")


# Main Execution

if __name__ == "__main__":
    results = run_simulation()
    plot_results(results)

