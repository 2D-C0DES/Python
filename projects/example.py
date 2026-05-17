#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   NETWORK SIMULATION SUITE v4.0                            ║
║                                                                            ║
║  A comprehensive network communication simulation framework combining:     ║
║  • Line Coding Schemes (Physical Layer)                                   ║
║  • MQTT Protocol Simulation (Application Layer)                           ║
║  • Advanced Metrics & Analytics                                           ║
║                                                                            ║
║  Author: Code Moderator & Generator                                       ║
║  Date: January 2026                                                       ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import matplotlib.pyplot as plt
import simpy
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Callable
from enum import Enum
import json
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════
#                         CONFIGURATION & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

class QoSLevel(Enum):
    """MQTT Quality of Service Levels"""
    AT_MOST_ONCE = 0    # Fire and forget
    AT_LEAST_ONCE = 1   # Acknowledged delivery
    EXACTLY_ONCE = 2    # Assured delivery


@dataclass
class SimulationConfig:
    """Centralized configuration for all simulations"""
    # MQTT Configuration
    num_publishers: int = 5
    num_subscribers: int = 5
    sim_duration: float = 50.0
    message_interval: float = 5.0
    network_delay_mean: float = 1.0
    packet_drop_prob: float = 0.005
    qos_level: QoSLevel = QoSLevel.EXACTLY_ONCE
    ack_timeout: float = 3.0
    max_retries: int = 2
    
    # Line Coding Configuration
    samples_per_bit: int = 100
    default_voltage_level: float = 1.0
    
    # Visualization Configuration
    figure_dpi: int = 100
    line_width: float = 2.5
    color_scheme: str = 'professional'  # 'professional', 'vibrant', 'monochrome'


# ═══════════════════════════════════════════════════════════════════════════
#                         LINE CODING MODULE
# ═══════════════════════════════════════════════════════════════════════════

class LineCodeType(Enum):
    """Enumeration of all supported line coding schemes"""
    UNIPOLAR_NRZ = "Unipolar NRZ"
    POLAR_NRZ_L = "Polar NRZ-L"
    POLAR_NRZ_I = "Polar NRZ-I"
    POLAR_RZ = "Polar RZ"
    MANCHESTER = "Manchester"
    DIFFERENTIAL_MANCHESTER = "Differential Manchester"
    AMI = "AMI (Bipolar)"
    PSEUDOTERNARY = "Pseudoternary (Bipolar)"


class LineCodeEncoder:
    """Advanced line coding encoder with all standard schemes"""
    
    def __init__(self, samples_per_bit: int = 100, voltage_level: float = 1.0):
        self.samples_per_bit = samples_per_bit
        self.voltage_level = voltage_level
        
    def encode(self, bits: np.ndarray, scheme: LineCodeType) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encode binary data using specified line coding scheme
        
        Args:
            bits: Binary data as numpy array
            scheme: Line coding scheme to use
            
        Returns:
            Tuple of (time_axis, signal)
        """
        encoding_methods = {
            LineCodeType.UNIPOLAR_NRZ: self._unipolar_nrz,
            LineCodeType.POLAR_NRZ_L: self._polar_nrz_l,
            LineCodeType.POLAR_NRZ_I: self._polar_nrz_i,
            LineCodeType.POLAR_RZ: self._polar_rz,
            LineCodeType.MANCHESTER: self._manchester,
            LineCodeType.DIFFERENTIAL_MANCHESTER: self._differential_manchester,
            LineCodeType.AMI: self._ami,
            LineCodeType.PSEUDOTERNARY: self._pseudoternary
        }
        
        return encoding_methods[scheme](bits)
    
    def _generate_time_axis(self, num_bits: int) -> np.ndarray:
        """Generate time axis for signal representation"""
        return np.linspace(0, num_bits, num_bits * self.samples_per_bit)
    
    def _unipolar_nrz(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Unipolar NRZ: 0 → 0V, 1 → +V"""
        signal = np.repeat(bits * self.voltage_level, self.samples_per_bit)
        time = self._generate_time_axis(len(bits))
        return time, signal
    
    def _polar_nrz_l(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Polar NRZ-L: 0 → -V, 1 → +V"""
        signal = np.where(
            np.repeat(bits, self.samples_per_bit) == 0,
            -self.voltage_level,
            self.voltage_level
        )
        time = self._generate_time_axis(len(bits))
        return time, signal
    
    def _polar_nrz_i(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Polar NRZ-I: Invert on 1, maintain on 0"""
        signal = []
        current_level = self.voltage_level
        
        for bit in bits:
            if bit == 1:
                current_level = -current_level
            signal.extend([current_level] * self.samples_per_bit)
        
        time = self._generate_time_axis(len(bits))
        return time, np.array(signal)
    
    def _polar_rz(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Polar RZ: Returns to zero at middle of bit period"""
        signal = []
        half_samples = self.samples_per_bit // 2
        
        for bit in bits:
            level = self.voltage_level if bit == 1 else -self.voltage_level
            signal.extend([level] * half_samples)
            signal.extend([0] * (self.samples_per_bit - half_samples))
        
        time = self._generate_time_axis(len(bits))
        return time, np.array(signal)
    
    def _manchester(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Manchester: 0 → high-to-low, 1 → low-to-high transition"""
        signal = []
        half_samples = self.samples_per_bit // 2
        
        for bit in bits:
            if bit == 0:
                signal.extend([self.voltage_level] * half_samples)
                signal.extend([-self.voltage_level] * (self.samples_per_bit - half_samples))
            else:
                signal.extend([-self.voltage_level] * half_samples)
                signal.extend([self.voltage_level] * (self.samples_per_bit - half_samples))
        
        time = self._generate_time_axis(len(bits))
        return time, np.array(signal)
    
    def _differential_manchester(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Differential Manchester: Transition at middle, invert at start for 0"""
        signal = []
        current_level = self.voltage_level
        half_samples = self.samples_per_bit // 2
        
        for bit in bits:
            if bit == 0:
                current_level = -current_level
            signal.extend([current_level] * half_samples)
            current_level = -current_level
            signal.extend([current_level] * (self.samples_per_bit - half_samples))
        
        time = self._generate_time_axis(len(bits))
        return time, np.array(signal)
    
    def _ami(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """AMI: 0 → 0V, 1 → alternating +V/-V"""
        signal = []
        last_nonzero = self.voltage_level
        
        for bit in bits:
            if bit == 0:
                signal.extend([0] * self.samples_per_bit)
            else:
                last_nonzero = -last_nonzero
                signal.extend([last_nonzero] * self.samples_per_bit)
        
        time = self._generate_time_axis(len(bits))
        return time, np.array(signal)
    
    def _pseudoternary(self, bits: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Pseudoternary: 1 → 0V, 0 → alternating +V/-V"""
        signal = []
        last_nonzero = self.voltage_level
        
        for bit in bits:
            if bit == 1:
                signal.extend([0] * self.samples_per_bit)
            else:
                last_nonzero = -last_nonzero
                signal.extend([last_nonzero] * self.samples_per_bit)
        
        time = self._generate_time_axis(len(bits))
        return time, np.array(signal)


class LineCodeAnalyzer:
    """Analyze line coding characteristics"""
    
    @staticmethod
    def calculate_dc_component(signal: np.ndarray) -> float:
        """Calculate DC component of signal"""
        return np.mean(signal)
    
    @staticmethod
    def calculate_bandwidth_efficiency(signal: np.ndarray, bit_rate: float) -> Dict[str, float]:
        """Estimate bandwidth requirements"""
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal))
        magnitude = np.abs(fft)
        
        # Find significant frequency components
        threshold = np.max(magnitude) * 0.1
        significant_freqs = freqs[magnitude > threshold]
        
        if len(significant_freqs) > 0:
            bandwidth = np.max(np.abs(significant_freqs)) - np.min(np.abs(significant_freqs))
        else:
            bandwidth = 0
        
        return {
            'bandwidth': bandwidth,
            'bandwidth_efficiency': bit_rate / bandwidth if bandwidth > 0 else float('inf')
        }
    
    @staticmethod
    def calculate_power_spectral_density(signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate power spectral density"""
        fft = np.fft.fft(signal)
        psd = np.abs(fft) ** 2 / len(signal)
        freqs = np.fft.fftfreq(len(signal))
        
        # Return positive frequencies only
        positive_freq_idx = freqs >= 0
        return freqs[positive_freq_idx], psd[positive_freq_idx]


# ═══════════════════════════════════════════════════════════════════════════
#                         MQTT SIMULATION MODULE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class MQTTMessage:
    """MQTT message with comprehensive metadata"""
    topic: str
    payload: str
    qos: QoSLevel
    sender_id: str
    message_id: str
    timestamp: float
    sent_time: float
    retain: bool = False
    duplicate: bool = False
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            'topic': self.topic,
            'payload': self.payload,
            'qos': self.qos.value,
            'sender_id': self.sender_id,
            'message_id': self.message_id,
            'timestamp': self.timestamp,
            'sent_time': self.sent_time,
            'retain': self.retain,
            'duplicate': self.duplicate
        }


@dataclass
class MQTTMetrics:
    """Comprehensive metrics tracking for MQTT simulation"""
    # Message counts
    logical_messages_sent: int = 0
    logical_messages_delivered: int = 0
    failed_messages: int = 0
    duplicate_deliveries: int = 0
    
    # QoS behavior
    retries: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Timing metrics
    end_to_end_latency: List[float] = field(default_factory=list)
    ack_latency: List[float] = field(default_factory=list)
    
    # Network metrics
    packets_sent: int = 0
    packets_dropped: int = 0
    
    # Per-QoS metrics
    qos0_messages: int = 0
    qos1_messages: int = 0
    qos2_messages: int = 0
    
    def record_send(self, msg_id: str, qos: QoSLevel):
        """Record message send"""
        self.logical_messages_sent += 1
        if qos == QoSLevel.AT_MOST_ONCE:
            self.qos0_messages += 1
        elif qos == QoSLevel.AT_LEAST_ONCE:
            self.qos1_messages += 1
        elif qos == QoSLevel.EXACTLY_ONCE:
            self.qos2_messages += 1
    
    def record_delivery(self, sent_time: float, recv_time: float):
        """Record successful delivery"""
        self.logical_messages_delivered += 1
        self.end_to_end_latency.append(recv_time - sent_time)
    
    def record_failure(self):
        """Record delivery failure"""
        self.failed_messages += 1
    
    def record_retry(self, msg_id: str):
        """Record retry attempt"""
        self.retries[msg_id] += 1
    
    def record_duplicate(self):
        """Record duplicate delivery"""
        self.duplicate_deliveries += 1
    
    def record_ack_latency(self, sent_time: float, ack_time: float):
        """Record acknowledgment latency"""
        self.ack_latency.append(ack_time - sent_time)
    
    def record_packet(self, dropped: bool = False):
        """Record network packet statistics"""
        self.packets_sent += 1
        if dropped:
            self.packets_dropped += 1
    
    @property
    def delivery_ratio(self) -> float:
        """Calculate delivery success ratio"""
        if self.logical_messages_sent == 0:
            return 0.0
        return self.logical_messages_delivered / self.logical_messages_sent
    
    @property
    def packet_loss_rate(self) -> float:
        """Calculate packet loss rate"""
        if self.packets_sent == 0:
            return 0.0
        return self.packets_dropped / self.packets_sent
    
    @property
    def avg_retries_per_message(self) -> float:
        """Calculate average retries per message"""
        if not self.retries:
            return 0.0
        return sum(self.retries.values()) / len(self.retries)
    
    @property
    def avg_end_to_end_latency(self) -> float:
        """Calculate average end-to-end latency"""
        if not self.end_to_end_latency:
            return 0.0
        return sum(self.end_to_end_latency) / len(self.end_to_end_latency)
    
    @property
    def avg_ack_latency(self) -> float:
        """Calculate average acknowledgment latency"""
        if not self.ack_latency:
            return 0.0
        return sum(self.ack_latency) / len(self.ack_latency)
    
    def get_summary(self) -> Dict:
        """Get comprehensive metrics summary"""
        return {
            'messages_sent': self.logical_messages_sent,
            'messages_delivered': self.logical_messages_delivered,
            'delivery_ratio': f"{self.delivery_ratio:.2%}",
            'failed_messages': self.failed_messages,
            'duplicate_deliveries': self.duplicate_deliveries,
            'avg_retries': f"{self.avg_retries_per_message:.2f}",
            'avg_latency': f"{self.avg_end_to_end_latency:.3f}s",
            'avg_ack_latency': f"{self.avg_ack_latency:.3f}s",
            'packet_loss_rate': f"{self.packet_loss_rate:.2%}",
            'qos_distribution': {
                'QoS 0': self.qos0_messages,
                'QoS 1': self.qos1_messages,
                'QoS 2': self.qos2_messages
            }
        }


class NetworkSimulator:
    """Simulates network characteristics (delay, jitter, packet loss)"""
    
    def __init__(self, env: simpy.Environment, config: SimulationConfig, metrics: MQTTMetrics):
        self.env = env
        self.config = config
        self.metrics = metrics
    
    def send(self, packet_type: str = "data"):
        """
        Simulate network transmission with delay and potential packet loss
        
        Args:
            packet_type: Type of packet being sent
            
        Yields:
            SimPy timeout event
            
        Raises:
            Exception: If packet is dropped
        """
        # Simulate network delay with exponential distribution
        delay = random.expovariate(1.0 / self.config.network_delay_mean)
        yield self.env.timeout(delay)
        
        # Simulate packet loss
        self.metrics.record_packet()
        if random.random() < self.config.packet_drop_prob:
            self.metrics.record_packet(dropped=True)
            raise Exception(f"PacketDropped: {packet_type}")


class MQTTBroker:
    """Advanced MQTT Broker with full QoS support"""
    
    def __init__(self, env: simpy.Environment, config: SimulationConfig, metrics: MQTTMetrics):
        self.env = env
        self.config = config
        self.metrics = metrics
        self.network = NetworkSimulator(env, config, metrics)
        
        # Subscription management
        self.subscriptions: Dict[str, List['MQTTClient']] = defaultdict(list)
        
        # QoS state management
        self.qos1_delivered_per_sub: Dict[str, Set[str]] = defaultdict(set)
        self.qos2_store: Dict[str, Dict] = {}
        
        # Retained messages
        self.retained_messages: Dict[str, MQTTMessage] = {}
    
    def subscribe(self, client: 'MQTTClient', topic: str):
        """Subscribe client to topic"""
        self.subscriptions[topic].append(client)
        print(f"[{self.env.now:6.2f}] {client.client_id:12} → Subscribed to '{topic}'")
        
        # Send retained message if exists
        if topic in self.retained_messages:
            self.env.process(self._deliver_to_subscriber(
                client, self.retained_messages[topic]
            ))
    
    def receive_publish(self, message: MQTTMessage, publisher: 'MQTTClient'):
        """Handle incoming PUBLISH packet"""
        # Handle retained messages
        if message.retain:
            self.retained_messages[message.topic] = message
        
        # Route based on QoS level
        if message.qos == QoSLevel.AT_MOST_ONCE:
            self.env.process(self._handle_qos0(message))
        elif message.qos == QoSLevel.AT_LEAST_ONCE:
            self.env.process(self._handle_qos1(message, publisher))
        elif message.qos == QoSLevel.EXACTLY_ONCE:
            self.env.process(self._handle_qos2_publish(message, publisher))
    
    def _handle_qos0(self, message: MQTTMessage):
        """QoS 0: Fire and forget"""
        yield self.env.process(self._deliver_to_all_subscribers(message))
    
    def _handle_qos1(self, message: MQTTMessage, publisher: 'MQTTClient'):
        """QoS 1: At least once delivery with acknowledgment"""
        delivered_to_all = True
        
        for sub in self.subscriptions.get(message.topic, []):
            # Skip if already delivered to this subscriber
            if sub.client_id in self.qos1_delivered_per_sub[message.message_id]:
                continue
            
            try:
                yield from self.network.send("QoS1-PUBLISH")
                sub.receive_message(message)
                self.metrics.record_delivery(message.sent_time, self.env.now)
                self.qos1_delivered_per_sub[message.message_id].add(sub.client_id)
            except Exception:
                self.metrics.record_failure()
                delivered_to_all = False
        
        # Send PUBACK to publisher if all subscribers received the message
        if delivered_to_all:
            try:
                yield from self.network.send("PUBACK")
                publisher.receive_puback(message.message_id)
            except Exception:
                pass  # PUBACK loss → publisher will retry
    
    def _handle_qos2_publish(self, message: MQTTMessage, publisher: 'MQTTClient'):
        """QoS 2: Exactly once delivery (4-way handshake - Part 1)"""
        if message.message_id in self.qos2_store:
            # Duplicate PUBLISH, resend PUBREC
            try:
                yield from self.network.send("PUBREC-DUP")
                publisher.receive_pubrec(message.message_id)
            except Exception:
                pass
            return
        
        # Store message
        self.qos2_store[message.message_id] = {
            "state": "PUBREC_SENT",
            "message": message
        }
        
        # Send PUBREC
        try:
            yield from self.network.send("PUBREC")
            publisher.receive_pubrec(message.message_id)
        except Exception:
            pass
    
    def receive_pubrel(self, message_id: str, publisher: 'MQTTClient'):
        """QoS 2: Handle PUBREL (4-way handshake - Part 2)"""
        if message_id not in self.qos2_store:
            return
        
        message = self.qos2_store[message_id]["message"]
        self.env.process(self._finalize_qos2(message, publisher))
    
    def _finalize_qos2(self, message: MQTTMessage, publisher: 'MQTTClient'):
        """QoS 2: Deliver message and send PUBCOMP"""
        # Deliver to subscribers
        yield self.env.process(self._deliver_to_all_subscribers(message))
        
        # Send PUBCOMP
        try:
            yield from self.network.send("PUBCOMP")
            publisher.receive_pubcomp(message.message_id)
        except Exception:
            pass
        
        # Clean up
        del self.qos2_store[message.message_id]
    
    def _deliver_to_all_subscribers(self, message: MQTTMessage):
        """Deliver message to all subscribers of the topic"""
        success = False
        for sub in self.subscriptions.get(message.topic, []):
            try:
                yield from self.network.send("MESSAGE")
                sub.receive_message(message)
                self.metrics.record_delivery(message.sent_time, self.env.now)
                success = True
            except Exception:
                self.metrics.record_failure()
        return success
    
    def _deliver_to_subscriber(self, subscriber: 'MQTTClient', message: MQTTMessage):
        """Deliver message to specific subscriber"""
        try:
            yield from self.network.send("RETAINED-MESSAGE")
            subscriber.receive_message(message)
        except Exception:
            pass


class MQTTClient:
    """MQTT Client supporting both Publisher and Subscriber roles"""
    
    def __init__(self, env: simpy.Environment, broker: MQTTBroker, 
                 client_id: str, role: str, topic: str, config: SimulationConfig):
        self.env = env
        self.broker = broker
        self.client_id = client_id
        self.role = role
        self.topic = topic
        self.config = config
        
        # Message tracking
        self.received_message_ids: Set[str] = set()
        self.qos1_pending: Dict[str, MQTTMessage] = {}
        self.qos2_pending: Dict[str, MQTTMessage] = {}
        
        # Statistics
        self.messages_received: int = 0
        self.messages_sent: int = 0
        
        # Initialize based on role
        if role == "subscriber":
            broker.subscribe(self, topic)
        elif role == "publisher":
            env.process(self.publisher_loop())
    
    def publisher_loop(self):
        """Main publisher loop - sends messages periodically"""
        msg_counter = 0
        
        while True:
            msg_counter += 1
            msg_id = f"{self.client_id}-{msg_counter}"
            
            message = MQTTMessage(
                topic=self.topic,
                payload=f"data-{msg_id}",
                qos=self.config.qos_level,
                sender_id=self.client_id,
                message_id=msg_id,
                timestamp=self.env.now,
                sent_time=self.env.now
            )
            
            self.messages_sent += 1
            self.broker.metrics.record_send(msg_id, message.qos)
            
            # Handle based on QoS level
            if message.qos == QoSLevel.AT_MOST_ONCE:
                self.broker.receive_publish(message, self)
            
            elif message.qos == QoSLevel.AT_LEAST_ONCE:
                self.qos1_pending[msg_id] = message
                self.env.process(self._qos1_send(message))
            
            elif message.qos == QoSLevel.EXACTLY_ONCE:
                self.qos2_pending[msg_id] = message
                self.env.process(self._qos2_send(message))
            
            yield self.env.timeout(self.config.message_interval)
    
    def _qos1_send(self, message: MQTTMessage):
        """QoS 1 send with retries"""
        for attempt in range(self.config.max_retries + 1):
            self.broker.receive_publish(message, self)
            
            if attempt > 0:
                self.broker.metrics.record_retry(message.message_id)
                print(f"[{self.env.now:6.2f}] {self.client_id:12} → Retry {attempt} for {message.message_id}")
            
            yield self.env.timeout(self.config.ack_timeout)
            
            # Check if acknowledged
            if message.message_id not in self.qos1_pending:
                return
        
        # Failed after all retries
        self.broker.metrics.record_failure()
        print(f"[{self.env.now:6.2f}] {self.client_id:12} → Failed to deliver {message.message_id}")
        del self.qos1_pending[message.message_id]
    
    def _qos2_send(self, message: MQTTMessage):
        """QoS 2 send - initiate 4-way handshake"""
        self.broker.receive_publish(message, self)
    
    def receive_puback(self, message_id: str):
        """Handle PUBACK (QoS 1)"""
        message = self.qos1_pending.pop(message_id, None)
        if message:
            self.broker.metrics.record_ack_latency(message.sent_time, self.env.now)
            print(f"[{self.env.now:6.2f}] {self.client_id:12} ← PUBACK for {message_id}")
    
    def receive_pubrec(self, message_id: str):
        """Handle PUBREC (QoS 2 - Step 1)"""
        print(f"[{self.env.now:6.2f}] {self.client_id:12} ← PUBREC for {message_id}")
        self.env.process(self._send_pubrel(message_id))
    
    def _send_pubrel(self, message_id: str):
        """Send PUBREL (QoS 2 - Step 2)"""
        try:
            yield from self.broker.network.send("PUBREL")
            self.broker.receive_pubrel(message_id, self)
            self.broker.metrics.record_retry(message_id)
        except Exception:
            pass
    
    def receive_pubcomp(self, message_id: str):
        """Handle PUBCOMP (QoS 2 - Step 3)"""
        message = self.qos2_pending.pop(message_id, None)
        if message:
            self.broker.metrics.record_ack_latency(message.sent_time, self.env.now)
            print(f"[{self.env.now:6.2f}] {self.client_id:12} ← PUBCOMP for {message_id}")
    
    def receive_message(self, message: MQTTMessage):
        """Handle received message (Subscriber)"""
        # Detect duplicates
        if message.message_id in self.received_message_ids:
            self.broker.metrics.record_duplicate()
            print(f"[{self.env.now:6.2f}] {self.client_id:12} ✗ Duplicate {message.payload}")
            return
        
        self.received_message_ids.add(message.message_id)
        self.messages_received += 1
        print(f"[{self.env.now:6.2f}] {self.client_id:12} ✓ Received {message.payload}")


# ═══════════════════════════════════════════════════════════════════════════
#                         VISUALIZATION MODULE
# ═══════════════════════════════════════════════════════════════════════════

class Visualizer:
    """Advanced visualization for both Line Coding and MQTT simulations"""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self._setup_style()
    
    def _setup_style(self):
        """Configure matplotlib style"""
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn' in plt.style.available else 'default')
        
        color_schemes = {
            'professional': {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'accent': '#F18F01',
                'success': '#06A77D',
                'danger': '#D00000'
            },
            'vibrant': {
                'primary': '#FF006E',
                'secondary': '#8338EC',
                'accent': '#FFBE0B',
                'success': '#06FFA5',
                'danger': '#FB5607'
            },
            'monochrome': {
                'primary': '#2D3142',
                'secondary': '#4F5D75',
                'accent': '#BFC0C0',
                'success': '#06A77D',
                'danger': '#EF8354'
            }
        }
        
        self.colors = color_schemes.get(self.config.color_scheme, color_schemes['professional'])
    
    def plot_all_line_codes(self, bits: np.ndarray, encoder: LineCodeEncoder):
        """Plot all line coding schemes in a comprehensive view"""
        schemes = list(LineCodeType)
        n_schemes = len(schemes)
        
        fig, axes = plt.subplots(n_schemes, 1, figsize=(16, 14))
        fig.suptitle(
            f'Line Coding Schemes Comparison\nBinary Input: {" ".join(map(str, bits))}',
            fontsize=18, fontweight='bold', y=0.995
        )
        
        for idx, scheme in enumerate(schemes):
            time, signal = encoder.encode(bits, scheme)
            ax = axes[idx]
            
            # Plot signal
            ax.plot(time, signal, linewidth=self.config.line_width, 
                   color=self.colors['primary'], alpha=0.8)
            ax.fill_between(time, 0, signal, alpha=0.2, color=self.colors['primary'])
            
            # Styling
            ax.set_ylabel(scheme.value, fontweight='bold', fontsize=10)
            ax.set_ylim(-1.8, 1.8)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
            
            # Add bit boundaries
            for i in range(len(bits) + 1):
                ax.axvline(x=i, color=self.colors['danger'], 
                          linewidth=0.8, linestyle='--', alpha=0.5)
            
            # Add bit labels on first subplot
            if idx == 0:
                for i, bit in enumerate(bits):
                    ax.text(i + 0.5, 1.5, str(bit), ha='center', 
                           fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor='yellow', alpha=0.7))
            
            ax.set_xlim(0, len(bits))
            
            # Remove x-tick labels except for last subplot
            if idx < n_schemes - 1:
                ax.set_xticklabels([])
        
        axes[-1].set_xlabel('Bit Period', fontsize=12, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_single_line_code(self, bits: np.ndarray, scheme: LineCodeType, 
                            encoder: LineCodeEncoder):
        """Plot a single line coding scheme with detailed analysis"""
        time, signal = encoder.encode(bits, scheme)
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Main signal plot
        ax_main = fig.add_subplot(gs[0, :])
        ax_main.plot(time, signal, linewidth=3, color=self.colors['primary'], 
                    marker='o', markersize=2, markevery=50)
        ax_main.fill_between(time, 0, signal, alpha=0.2, color=self.colors['primary'])
        
        ax_main.set_title(
            f'{scheme.value} Encoding\nBinary: {" ".join(map(str, bits))}',
            fontsize=16, fontweight='bold', pad=15
        )
        ax_main.set_ylabel('Voltage Level', fontsize=12, fontweight='bold')
        ax_main.set_xlabel('Bit Period', fontsize=12, fontweight='bold')
        ax_main.set_ylim(-1.8, 1.8)
        ax_main.grid(True, alpha=0.4, linestyle='--')
        ax_main.axhline(y=0, color='black', linewidth=1)
        
        # Add bit boundaries and labels
        for i in range(len(bits) + 1):
            ax_main.axvline(x=i, color=self.colors['danger'], 
                          linewidth=1, linestyle='--', alpha=0.6)
        
        for i, bit in enumerate(bits):
            ax_main.text(i + 0.5, 1.6, str(bit), ha='center', fontsize=14,
                       fontweight='bold', bbox=dict(boxstyle='round', 
                       facecolor='yellow', alpha=0.7))
        
        # Power Spectral Density
        ax_psd = fig.add_subplot(gs[1, 0])
        analyzer = LineCodeAnalyzer()
        freqs, psd = analyzer.calculate_power_spectral_density(signal)
        ax_psd.semilogy(freqs[:len(freqs)//2], psd[:len(psd)//2], 
                       color=self.colors['secondary'], linewidth=2)
        ax_psd.set_title('Power Spectral Density', fontweight='bold')
        ax_psd.set_xlabel('Normalized Frequency')
        ax_psd.set_ylabel('PSD (dB)')
        ax_psd.grid(True, alpha=0.3)
        
        # Signal characteristics
        ax_stats = fig.add_subplot(gs[1, 1])
        ax_stats.axis('off')
        
        dc_component = analyzer.calculate_dc_component(signal)
        signal_power = np.mean(signal ** 2)
        peak_power = np.max(np.abs(signal)) ** 2
        
        stats_text = f"""
        Signal Characteristics:
        {'─' * 30}
        DC Component:     {dc_component:.4f} V
        Average Power:    {signal_power:.4f} W
        Peak Power:       {peak_power:.4f} W
        Signal Range:     [{np.min(signal):.2f}, {np.max(signal):.2f}] V
        
        Zero Crossings:   {np.sum(np.diff(np.sign(signal)) != 0)}
        Transitions:      {np.sum(np.diff(signal) != 0) // encoder.samples_per_bit}
        """
        
        ax_stats.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                     verticalalignment='center',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Signal histogram
        ax_hist = fig.add_subplot(gs[2, :])
        ax_hist.hist(signal, bins=50, color=self.colors['accent'], 
                    alpha=0.7, edgecolor='black')
        ax_hist.set_title('Signal Amplitude Distribution', fontweight='bold')
        ax_hist.set_xlabel('Voltage Level')
        ax_hist.set_ylabel('Frequency')
        ax_hist.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_mqtt_metrics(self, metrics: MQTTMetrics, config: SimulationConfig):
        """Create comprehensive MQTT simulation visualization"""
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)
        
        # Title
        fig.suptitle(
            f'MQTT Simulation Results (QoS {config.qos_level.value})\n'
            f'Publishers: {config.num_publishers} | Subscribers: {config.num_subscribers} | '
            f'Duration: {config.sim_duration}s',
            fontsize=16, fontweight='bold'
        )
        
        # 1. Message Statistics
        ax1 = fig.add_subplot(gs[0, 0])
        categories = ['Sent', 'Delivered', 'Failed', 'Duplicates']
        values = [
            metrics.logical_messages_sent,
            metrics.logical_messages_delivered,
            metrics.failed_messages,
            metrics.duplicate_deliveries
        ]
        colors_bar = [self.colors['primary'], self.colors['success'], 
                     self.colors['danger'], self.colors['accent']]
        
        bars = ax1.bar(categories, values, color=colors_bar, alpha=0.7, edgecolor='black')
        ax1.set_title('Message Statistics', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 2. QoS Distribution
        ax2 = fig.add_subplot(gs[0, 1])
        qos_data = [metrics.qos0_messages, metrics.qos1_messages, metrics.qos2_messages]
        qos_labels = ['QoS 0', 'QoS 1', 'QoS 2']
        
        if sum(qos_data) > 0:
            wedges, texts, autotexts = ax2.pie(
                qos_data, labels=qos_labels, autopct='%1.1f%%',
                colors=[self.colors['primary'], self.colors['secondary'], self.colors['accent']],
                startangle=90
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        ax2.set_title('QoS Level Distribution', fontweight='bold', fontsize=12)
        
        # 3. Delivery Ratio
        ax3 = fig.add_subplot(gs[0, 2])
        delivery_ratio = metrics.delivery_ratio * 100
        packet_loss = metrics.packet_loss_rate * 100
        
        metrics_data = [delivery_ratio, 100 - delivery_ratio, 
                       100 - packet_loss, packet_loss]
        metric_labels = ['Delivered', 'Failed', 'Packets OK', 'Packets Lost']
        
        x_pos = [0, 1]
        ax3.barh(x_pos, [delivery_ratio, 100 - packet_loss], 
                color=[self.colors['success'], self.colors['primary']], alpha=0.7)
        ax3.set_yticks(x_pos)
        ax3.set_yticklabels(['Message\nDelivery', 'Packet\nDelivery'])
        ax3.set_xlabel('Success Rate (%)')
        ax3.set_title('Delivery Performance', fontweight='bold', fontsize=12)
        ax3.set_xlim(0, 100)
        ax3.grid(True, alpha=0.3, axis='x')
        
        # Add percentage labels
        for i, (ratio, label) in enumerate([(delivery_ratio, 'msg'), 
                                            (100 - packet_loss, 'pkt')]):
            ax3.text(ratio + 2, i, f'{ratio:.1f}%', 
                    va='center', fontweight='bold')
        
        # 4. End-to-End Latency Distribution
        ax4 = fig.add_subplot(gs[1, :2])
        if metrics.end_to_end_latency:
            ax4.hist(metrics.end_to_end_latency, bins=30, 
                    color=self.colors['secondary'], alpha=0.7, edgecolor='black')
            ax4.axvline(metrics.avg_end_to_end_latency, color=self.colors['danger'],
                       linestyle='--', linewidth=2, 
                       label=f'Mean: {metrics.avg_end_to_end_latency:.3f}s')
            ax4.set_xlabel('Latency (seconds)')
            ax4.set_ylabel('Frequency')
            ax4.set_title('End-to-End Latency Distribution', fontweight='bold', fontsize=12)
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        # 5. Retry Statistics
        ax5 = fig.add_subplot(gs[1, 2])
        if metrics.retries:
            retry_counts = list(metrics.retries.values())
            ax5.hist(retry_counts, bins=range(max(retry_counts) + 2), 
                    color=self.colors['accent'], alpha=0.7, edgecolor='black', 
                    align='left')
            ax5.set_xlabel('Number of Retries')
            ax5.set_ylabel('Message Count')
            ax5.set_title(f'Retry Distribution\n(Avg: {metrics.avg_retries_per_message:.2f})',
                         fontweight='bold', fontsize=12)
            ax5.grid(True, alpha=0.3)
        
        # 6. ACK Latency
        ax6 = fig.add_subplot(gs[2, 0])
        if metrics.ack_latency:
            ax6.boxplot([metrics.ack_latency], vert=True, patch_artist=True,
                       boxprops=dict(facecolor=self.colors['primary'], alpha=0.7))
            ax6.set_ylabel('Latency (seconds)')
            ax6.set_title(f'ACK Latency\n(Avg: {metrics.avg_ack_latency:.3f}s)',
                         fontweight='bold', fontsize=12)
            ax6.set_xticklabels(['ACK Latency'])
            ax6.grid(True, alpha=0.3, axis='y')
        
        # 7. Performance Metrics Summary
        ax7 = fig.add_subplot(gs[2, 1:])
        ax7.axis('off')
        
        summary_text = f"""
        Performance Summary:
        {'═' * 60}
        Messages Sent:              {metrics.logical_messages_sent:>6}
        Messages Delivered:         {metrics.logical_messages_delivered:>6}
        Delivery Success Rate:      {metrics.delivery_ratio:>6.2%}
        
        Failed Messages:            {metrics.failed_messages:>6}
        Duplicate Deliveries:       {metrics.duplicate_deliveries:>6}
        Average Retries/Message:    {metrics.avg_retries_per_message:>6.2f}
        
        Avg End-to-End Latency:     {metrics.avg_end_to_end_latency:>6.3f}s
        Avg ACK Latency:            {metrics.avg_ack_latency:>6.3f}s
        
        Total Packets Sent:         {metrics.packets_sent:>6}
        Packets Dropped:            {metrics.packets_dropped:>6}
        Packet Loss Rate:           {metrics.packet_loss_rate:>6.2%}
        
        QoS Configuration:          QoS {config.qos_level.value}
        Network Delay (mean):       {config.network_delay_mean:>6.2f}s
        Packet Drop Probability:    {config.packet_drop_prob:>6.3f}
        """
        
        ax7.text(0.05, 0.5, summary_text, fontsize=11, family='monospace',
                verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        plt.tight_layout()
        return fig


# ═══════════════════════════════════════════════════════════════════════════
#                         MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

class NetworkSimulationSuite:
    """Main application coordinating all simulation modules"""
    
    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or SimulationConfig()
        self.visualizer = Visualizer(self.config)
        self.encoder = LineCodeEncoder(
            samples_per_bit=self.config.samples_per_bit,
            voltage_level=self.config.default_voltage_level
        )
    
    def run_line_coding_demo(self, bits: str, mode: str = 'all'):
        """
        Run line coding demonstration
        
        Args:
            bits: Binary string (e.g., '10110101')
            mode: 'all' for all schemes, or specific scheme name
        """
        # Validate and convert bits
        if not all(b in '01' for b in bits):
            raise ValueError("Binary input must contain only 0s and 1s")
        
        bits_array = np.array([int(b) for b in bits])
        
        print(f"\n{'═' * 70}")
        print(f"LINE CODING SIMULATION")
        print(f"{'═' * 70}")
        print(f"Binary Input: {bits}")
        print(f"Number of bits: {len(bits_array)}")
        print(f"Samples per bit: {self.config.samples_per_bit}")
        
        if mode == 'all':
            print(f"\nGenerating all line coding schemes...")
            fig = self.visualizer.plot_all_line_codes(bits_array, self.encoder)
        else:
            # Find matching scheme
            scheme = None
            for s in LineCodeType:
                if s.value.lower() == mode.lower() or s.name.lower() == mode.lower():
                    scheme = s
                    break
            
            if scheme is None:
                raise ValueError(f"Unknown line coding scheme: {mode}")
            
            print(f"\nGenerating {scheme.value} encoding...")
            fig = self.visualizer.plot_single_line_code(bits_array, scheme, self.encoder)
        
        plt.show()
        return fig
    
    def run_mqtt_simulation(self) -> MQTTMetrics:
        """Run MQTT protocol simulation"""
        print(f"\n{'═' * 70}")
        print(f"MQTT PROTOCOL SIMULATION")
        print(f"{'═' * 70}")
        print(f"Configuration:")
        print(f"  Publishers:       {self.config.num_publishers}")
        print(f"  Subscribers:      {self.config.num_subscribers}")
        print(f"  QoS Level:        {self.config.qos_level.value} ({self.config.qos_level.name})")
        print(f"  Duration:         {self.config.sim_duration}s")
        print(f"  Msg Interval:     {self.config.message_interval}s")
        print(f"  Network Delay:    {self.config.network_delay_mean}s (mean)")
        print(f"  Packet Drop:      {self.config.packet_drop_prob:.3f}")
        print(f"\n{'─' * 70}")
        print(f"Simulation starting...\n")
        
        # Create simulation environment
        env = simpy.Environment()
        metrics = MQTTMetrics()
        broker = MQTTBroker(env, self.config, metrics)
        
        # Create subscribers
        subscribers = []
        for i in range(self.config.num_subscribers):
            sub = MQTTClient(
                env, broker, f"Sub-{i}", "subscriber", 
                "topic/sensor", self.config
            )
            subscribers.append(sub)
        
        # Create publishers
        publishers = []
        for i in range(self.config.num_publishers):
            pub = MQTTClient(
                env, broker, f"Pub-{i}", "publisher",
                "topic/sensor", self.config
            )
            publishers.append(pub)
        
        # Run simulation
        env.run(until=self.config.sim_duration)
        
        print(f"\n{'─' * 70}")
        print(f"Simulation completed!")
        print(f"{'═' * 70}\n")
        
        # Display results
        self._print_mqtt_results(metrics)
        
        # Visualize
        fig = self.visualizer.plot_mqtt_metrics(metrics, self.config)
        plt.show()
        
        return metrics
    
    def _print_mqtt_results(self, metrics: MQTTMetrics):
        """Print MQTT simulation results"""
        summary = metrics.get_summary()
        
        print("SIMULATION RESULTS:")
        print(f"{'─' * 70}")
        print(f"Messages Sent:           {summary['messages_sent']:>6}")
        print(f"Messages Delivered:      {summary['messages_delivered']:>6}")
        print(f"Delivery Ratio:          {summary['delivery_ratio']:>6}")
        print(f"Failed Messages:         {summary['failed_messages']:>6}")
        print(f"Duplicate Deliveries:    {summary['duplicate_deliveries']:>6}")
        print(f"Average Retries:         {summary['avg_retries']:>6}")
        print(f"Average Latency:         {summary['avg_latency']:>6}")
        print(f"Average ACK Latency:     {summary['avg_ack_latency']:>6}")
        print(f"Packet Loss Rate:        {summary['packet_loss_rate']:>6}")
        print(f"\nQoS Distribution:")
        for qos, count in summary['qos_distribution'].items():
            print(f"  {qos}: {count:>6}")
    
    def interactive_menu(self):
        """Interactive menu for running simulations"""
        while True:
            print(f"\n{'╔' + '═' * 68 + '╗'}")
            print(f"║{' ' * 68}║")
            print(f"║{'NETWORK SIMULATION SUITE v4.0':^68}║")
            print(f"║{' ' * 68}║")
            print(f"{'╠' + '═' * 68 + '╣'}")
            print(f"║  1. Run Line Coding Simulation (All Schemes)                    ║")
            print(f"║  2. Run Line Coding Simulation (Single Scheme)                  ║")
            print(f"║  3. Run MQTT Protocol Simulation                                ║")
            print(f"║  4. Configure Simulation Parameters                             ║")
            print(f"║  5. Export Results to JSON                                      ║")
            print(f"║  6. Exit                                                        ║")
            print(f"{'╚' + '═' * 68 + '╝'}")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            try:
                if choice == '1':
                    bits = input("\nEnter binary sequence (e.g., 10110101): ").strip()
                    self.run_line_coding_demo(bits, mode='all')
                
                elif choice == '2':
                    bits = input("\nEnter binary sequence (e.g., 10110101): ").strip()
                    print("\nAvailable schemes:")
                    for i, scheme in enumerate(LineCodeType, 1):
                        print(f"  {i}. {scheme.value}")
                    
                    scheme_choice = input("\nEnter scheme number: ").strip()
                    scheme_idx = int(scheme_choice) - 1
                    if 0 <= scheme_idx < len(LineCodeType):
                        scheme = list(LineCodeType)[scheme_idx]
                        self.run_line_coding_demo(bits, mode=scheme.name)
                    else:
                        print("Invalid scheme selection!")
                
                elif choice == '3':
                    self.run_mqtt_simulation()
                
                elif choice == '4':
                    self._configure_parameters()
                
                elif choice == '5':
                    print("\nFeature coming soon!")
                
                elif choice == '6':
                    print("\nThank you for using Network Simulation Suite!")
                    print("Goodbye!\n")
                    break
                
                else:
                    print("\n❌ Invalid choice! Please select 1-6.")
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.")
            
            if choice != '6':
                input("\nPress Enter to continue...")
    
    def _configure_parameters(self):
        """Interactive parameter configuration"""
        print(f"\n{'═' * 70}")
        print("CONFIGURATION")
        print(f"{'═' * 70}")
        print("\n[MQTT Parameters]")
        print(f"1. Publishers: {self.config.num_publishers}")
        print(f"2. Subscribers: {self.config.num_subscribers}")
        print(f"3. QoS Level: {self.config.qos_level.value}")
        print(f"4. Simulation Duration: {self.config.sim_duration}s")
        print(f"5. Message Interval: {self.config.message_interval}s")
        print(f"6. Network Delay Mean: {self.config.network_delay_mean}s")
        print(f"7. Packet Drop Probability: {self.config.packet_drop_prob}")
        
        print("\n[Line Coding Parameters]")
        print(f"8. Samples per Bit: {self.config.samples_per_bit}")
        
        print("\n0. Return to main menu")
        
        param_choice = input("\nSelect parameter to modify (0-8): ").strip()
        
        try:
            if param_choice == '1':
                val = int(input("Enter number of publishers: "))
                self.config.num_publishers = val
            elif param_choice == '2':
                val = int(input("Enter number of subscribers: "))
                self.config.num_subscribers = val
            elif param_choice == '3':
                val = int(input("Enter QoS level (0/1/2): "))
                self.config.qos_level = QoSLevel(val)
            elif param_choice == '4':
                val = float(input("Enter simulation duration (s): "))
                self.config.sim_duration = val
            elif param_choice == '5':
                val = float(input("Enter message interval (s): "))
                self.config.message_interval = val
            elif param_choice == '6':
                val = float(input("Enter network delay mean (s): "))
                self.config.network_delay_mean = val
            elif param_choice == '7':
                val = float(input("Enter packet drop probability (0-1): "))
                self.config.packet_drop_prob = val
            elif param_choice == '8':
                val = int(input("Enter samples per bit: "))
                self.config.samples_per_bit = val
                self.encoder = LineCodeEncoder(val, self.config.default_voltage_level)
            
            if param_choice != '0':
                print("\n✓ Parameter updated successfully!")
        
        except Exception as e:
            print(f"\n❌ Error updating parameter: {e}")


# ═══════════════════════════════════════════════════════════════════════════
#                         ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point for the application"""
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║                    NETWORK SIMULATION SUITE v4.0                       ║
    ║                                                                        ║
    ║              Comprehensive Network Protocol Simulation                ║
    ║                                                                        ║
    ║  Features:                                                             ║
    ║    • 8 Line Coding Schemes (Physical Layer)                           ║
    ║    • MQTT Protocol with QoS 0/1/2 (Application Layer)                 ║
    ║    • Advanced Metrics & Analytics                                     ║
    ║    • Professional Visualizations                                      ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create default configuration
    config = SimulationConfig()
    
    # Create and run application
    app = NetworkSimulationSuite(config)
    app.interactive_menu()


if __name__ == "__main__":
    main()