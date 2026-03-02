VERSION = 1.0

# Define Simulation Parameters

import simpy
import random
import matplotlib.pyplot as plt
from collections import defaultdict

# --- Simulation parameters ---
NUM_PUBLISHERS = 5
NUM_SUBSCRIBERS = 5
SIM_DURATION = 50        # seconds
MESSAGE_INTERVAL = 5     # publish interval (s)
NETWORK_DELAY_MEAN = 1.0 # average delay (s)
PACKET_DROP_PROB = 0.1  # 10% network packet loss
QOS_LEVEL = 0 

# QoS1 parameters

ACK_TIMEOUT = 3           # seconds before publisher retries
MAX_RETRIES = 2           # how many times publisher retries if no PUBACK



# Define Message and Metrics Classes

class Message:
    """MQTT message representation."""
    def __init__(self, topic, payload, qos, sender_id,message_id, timestamp):
        self.topic = topic
        self.payload = payload
        self.qos = qos
        self.sender_id = sender_id
        self.timestamp = timestamp
        self.message_id = message_id


class Metrics:
    """For collecting simulation metrics."""
    def __init__(self):
        self.delivered = 0
        self.lost = 0
        self.latencies = []

    def record_delivery(self, sent_time, recv_time):
        self.delivered += 1
        self.latencies.append(recv_time - sent_time)

    def record_loss(self):
        self.lost += 1



# Network Model (Delay + Drop)

def network_send(env, delay_mean, drop_prob):
    """Simulate network latency and packet loss."""
    yield env.timeout(random.expovariate(1.0 / delay_mean))
    if random.random() < drop_prob:
        raise Exception("PacketDropped")
    

# Broker Process

class Broker:
    """Simulated MQTT Broker handling routing and QoS logic."""
    def __init__(self, env, metrics):
        self.env = env
        self.subscriptions = defaultdict(list)
        self.metrics = metrics

    def subscribe(self, client, topic):
        self.subscriptions[topic].append(client)
        print(f"[{self.env.now:.2f}] {client.client_id} subscribed to {topic}")

    def publish(self, message, publisher=None):
        """Route message to all subscribers and send PUBACK if QoS1."""
        if message.topic not in self.subscriptions:
            print(f"[{self.env.now:.2f}] No subscribers for topic {message.topic}")
        else:
            for sub in self.subscriptions[message.topic]:
                self.env.process(self.deliver_message(sub, message))

        # QoS1 → acknowledge back to publisher
        if message.qos == 1 and publisher:
            self.env.process(self.acknowledge(publisher, message))

    def acknowledge(self, publisher, message):
        """Simulate PUBACK to publisher."""
        yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
        publisher.receive_ack(message)

    def deliver_message(self, subscriber, message):
        """Simulate message delivery."""
        try:
            yield from network_send(self.env, NETWORK_DELAY_MEAN, PACKET_DROP_PROB)
            yield self.env.timeout(0.1)
            subscriber.receive_message(message)
            self.metrics.record_delivery(message.timestamp, self.env.now)
        except Exception:
            self.metrics.record_loss()



# Client Process (Publisher / Subscriber)

class Client:
    def __init__(self, env, broker, client_id, role, topic):
        self.env = env
        self.broker = broker
        self.client_id = client_id
        self.role = role
        self.topic = topic
        self.received_messages = []
        self.pending_ack = {}  # track message IDs waiting for ACK

        if role == "subscriber":
            broker.subscribe(self, topic)
        elif role == "publisher":
            self.env.process(self.publisher_behaviour())

    def publisher_behaviour(self):
        """Periodically publish messages (supports QoS1 retry)."""
        msg_counter = 0
        while True:
            msg_counter += 1
            msg_id = f"{self.client_id}-{msg_counter}"

            msg = Message(
                topic=self.topic,
                payload=f"Data {msg_id}",
                qos=QOS_LEVEL,
                sender_id=self.client_id,
                timestamp=self.env.now,
            )

            print(f"[{self.env.now:.2f}] {self.client_id} published {msg_id}")

            if msg.qos == 0:
                self.broker.publish(msg)
            else:
                # QoS1 → track and retry
                self.pending_ack[msg_id] = msg
                self.env.process(self.qos1_send_with_retry(msg, msg_id))

            yield self.env.timeout(MESSAGE_INTERVAL)

    def qos1_send_with_retry(self, msg, msg_id):
        """Send message and retry until ACK or retry limit."""
        for attempt in range(MAX_RETRIES + 1):
            try:
                self.broker.publish(msg, publisher=self)
                print(f"[{self.env.now:.2f}] {self.client_id} sent {msg_id} (try {attempt+1})")
                # wait for ACK
                ack_event = self.env.timeout(ACK_TIMEOUT)
                yield ack_event
                if msg_id not in self.pending_ack:
                    return  # ACK received
                print(f"[{self.env.now:.2f}] {self.client_id} retrying {msg_id}")
            except Exception as e:
                print(f"Error: {e}")
        # no ACK even after retries
        print(f"[{self.env.now:.2f}] {self.client_id} failed to deliver {msg_id}")
        del self.pending_ack[msg_id]

    def receive_ack(self, msg):
        """Handle PUBACK from broker."""
        msg_id = msg.payload.split()[-1]
        if msg_id in self.pending_ack:
            print(f"[{self.env.now:.2f}] {self.client_id} received PUBACK for {msg_id}")
            del self.pending_ack[msg_id]

    def receive_message(self, message):
        """Handle message reception, detect duplicates."""
        if message.payload in [m.payload for m in self.received_messages]:
            print(f"[{self.env.now:.2f}] {self.client_id} duplicate {message.payload} ignored")
            return
        self.received_messages.append(message)
        print(f"[{self.env.now:.2f}] {self.client_id} received {message.payload}")



# Simulation Setup

def run_simulation():
    env = simpy.Environment()
    metrics = Metrics()
    broker = Broker(env, metrics)

    # Create publishers & subscribers
    for i in range(NUM_SUBSCRIBERS):
        Client(env, broker, f"Sub-{i}", "subscriber", "topic/sensor")

    for i in range(NUM_PUBLISHERS):
        Client(env, broker, f"Pub-{i}", "publisher", "topic/sensor")

    env.run(until=SIM_DURATION)

    return metrics

# Analyse & Plot Metrics

def plot_results(metrics):
    print("\n--- Simulation Results ---")
    print(f"Messages Delivered: {metrics.delivered}")
    print(f"Messages Lost: {metrics.lost}")
    if metrics.latencies:
        avg_latency = sum(metrics.latencies) / len(metrics.latencies)
        print(f"Average Latency: {avg_latency:.2f}s")

        plt.hist(metrics.latencies, bins=10, edgecolor="black")
        plt.title("Message Delivery Latency Distribution")
        plt.xlabel("Latency (s)")
        plt.ylabel("Frequency")
        plt.show()


# Main Execution

if __name__ == "__main__":
    results = run_simulation()
    plot_results(results)





