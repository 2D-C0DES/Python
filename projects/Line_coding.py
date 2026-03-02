import numpy as np
import matplotlib.pyplot as plt

def generate_time_signal(bits, samples_per_bit):
    """Generate time axis and expanded bit array for smooth signal representation"""
    n_bits = len(bits)
    time = np.linspace(0, n_bits, n_bits * samples_per_bit)
    expanded_bits = np.repeat(bits, samples_per_bit)
    return time, expanded_bits

def unipolar_nrz(bits, samples_per_bit=100):
    """Unipolar NRZ: 0 -> 0V, 1 -> +V"""
    signal = np.repeat(bits, samples_per_bit)
    time = np.linspace(0, len(bits), len(signal))
    return time, signal

def polar_nrz_l(bits, samples_per_bit=100):
    """Polar NRZ-L: 0 -> -V, 1 -> +V"""
    signal = np.where(np.repeat(bits, samples_per_bit) == 0, -1, 1)
    time = np.linspace(0, len(bits), len(signal))
    return time, signal

def polar_nrz_i(bits, samples_per_bit=100):
    """Polar NRZ-I: Invert on 1, no change on 0"""
    signal = []
    current_level = 1
    for bit in bits:
        if bit == 1:
            current_level = -current_level
        signal.extend([current_level] * samples_per_bit)
    time = np.linspace(0, len(bits), len(signal))
    return time, np.array(signal)

def polar_rz(bits, samples_per_bit=100):
    """Polar RZ: Returns to zero in middle of bit period"""
    signal = []
    for bit in bits:
        level = 1 if bit == 1 else -1
        signal.extend([level] * (samples_per_bit // 2))
        signal.extend([0] * (samples_per_bit // 2))
    time = np.linspace(0, len(bits), len(signal))
    return time, np.array(signal)

def manchester(bits, samples_per_bit=100):
    """Manchester: 0 -> high-to-low, 1 -> low-to-high transition at middle"""
    signal = []
    for bit in bits:
        if bit == 0:
            signal.extend([1] * (samples_per_bit // 2))
            signal.extend([-1] * (samples_per_bit // 2))
        else:
            signal.extend([-1] * (samples_per_bit // 2))
            signal.extend([1] * (samples_per_bit // 2))
    time = np.linspace(0, len(bits), len(signal))
    return time, np.array(signal)

def differential_manchester(bits, samples_per_bit=100):
    """Differential Manchester: Always transition at middle, invert at start for 0"""
    signal = []
    current_level = 1
    for bit in bits:
        if bit == 0:
            current_level = -current_level
        signal.extend([current_level] * (samples_per_bit // 2))
        current_level = -current_level
        signal.extend([current_level] * (samples_per_bit // 2))
    time = np.linspace(0, len(bits), len(signal))
    return time, np.array(signal)

def ami(bits, samples_per_bit=100):
    """AMI (Alternate Mark Inversion): 0 -> 0V, 1 -> alternating +V/-V"""
    signal = []
    last_nonzero = 1
    for bit in bits:
        if bit == 0:
            signal.extend([0] * samples_per_bit)
        else:
            last_nonzero = -last_nonzero
            signal.extend([last_nonzero] * samples_per_bit)
    time = np.linspace(0, len(bits), len(signal))
    return time, np.array(signal)

def pseudoternary(bits, samples_per_bit=100):
    """Pseudoternary: 1 -> 0V, 0 -> alternating +V/-V"""
    signal = []
    last_nonzero = 1
    for bit in bits:
        if bit == 1:
            signal.extend([0] * samples_per_bit)
        else:
            last_nonzero = -last_nonzero
            signal.extend([last_nonzero] * samples_per_bit)
    time = np.linspace(0, len(bits), len(signal))
    return time, np.array(signal)

def plot_line_codes(bits):
    """Plot all line coding schemes"""
    # Convert input to numpy array
    bits = np.array([int(b) for b in str(bits)])
    
    fig, axes = plt.subplots(8, 1, figsize=(14, 12))
    fig.suptitle(f'Line Coding Schemes for Binary Input: {" ".join(map(str, bits))}', 
                 fontsize=16, fontweight='bold')
    
    schemes = [
        ('Unipolar NRZ', unipolar_nrz),
        ('Polar NRZ-L', polar_nrz_l),
        ('Polar NRZ-I', polar_nrz_i),
        ('Polar RZ', polar_rz),
        ('Manchester', manchester),
        ('Differential Manchester', differential_manchester),
        ('AMI (Bipolar)', ami),
        ('Pseudoternary (Bipolar)', pseudoternary)
    ]
    
    for idx, (name, func) in enumerate(schemes):
        time, signal = func(bits)
        axes[idx].plot(time, signal, linewidth=2, color='blue')
        axes[idx].set_ylabel(name, fontweight='bold')
        axes[idx].set_ylim(-1.5, 1.5)
        axes[idx].grid(True, alpha=0.3)
        axes[idx].axhline(y=0, color='black', linewidth=0.5)
        
        # Add bit boundaries
        for i in range(len(bits) + 1):
            axes[idx].axvline(x=i, color='red', linewidth=0.5, linestyle='--', alpha=0.5)
        
        # Add bit labels on first subplot
        if idx == 0:
            for i, bit in enumerate(bits):
                axes[idx].text(i + 0.5, 1.3, str(bit), ha='center', fontsize=12, fontweight='bold')
        
        axes[idx].set_xlim(0, len(bits))
    
    axes[-1].set_xlabel('Bit Period', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("LINE CODING SIMULATION")
    print("=" * 60)
    
    binary_input = input("\nEnter binary sequence (e.g., 10110): ")
    
    # Validate input
    if not all(bit in '01' for bit in binary_input):
        print("Error: Please enter only 0s and 1s")
    else:
        print(f"\nGenerating line coding schemes for: {binary_input}")
        plot_line_codes(binary_input)