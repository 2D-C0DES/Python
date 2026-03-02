import numpy as np
import matplotlib.pyplot as plt

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

def plot_selected_line_code(bits, scheme_name, encoding_function):
    """Plot the selected line coding scheme"""
    bits_array = np.array([int(b) for b in str(bits)])
    
    time, signal = encoding_function(bits_array)
    
    plt.figure(figsize=(14, 6))
    plt.plot(time, signal, linewidth=2.5, color='darkblue', marker='o', 
             markersize=3, markevery=50)
    
    plt.title(f'{scheme_name} Encoding for Binary Input: {" ".join(map(str, bits_array))}', 
              fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Voltage Level', fontsize=12, fontweight='bold')
    plt.xlabel('Bit Period', fontsize=12, fontweight='bold')
    
    plt.ylim(-1.8, 1.8)
    plt.xlim(0, len(bits_array))
    plt.grid(True, alpha=0.4, linestyle='--')
    plt.axhline(y=0, color='black', linewidth=1)
    
    # Add bit boundaries
    for i in range(len(bits_array) + 1):
        plt.axvline(x=i, color='red', linewidth=1, linestyle='--', alpha=0.6)
    
    # Add bit labels
    for i, bit in enumerate(bits_array):
        plt.text(i + 0.5, 1.6, str(bit), ha='center', fontsize=14, 
                fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.show()

def display_menu():
    """Display the line coding menu"""
    print("\n" + "="*60)
    print("LINE CODING SCHEMES - SELECT YOUR CHOICE")
    print("="*60)
    print("1. Unipolar NRZ")
    print("2. Polar NRZ-L")
    print("3. Polar NRZ-I")
    print("4. Polar RZ")
    print("5. Manchester")
    print("6. Differential Manchester")
    print("7. AMI (Bipolar)")
    print("8. Pseudoternary (Bipolar)")
    print("9. Exit")
    print("="*60)

# Main execution
if __name__ == "__main__":
    print("\n" + "*"*60)
    print("WELCOME TO LINE CODING SIMULATION")
    print("*"*60)
    
    binary_input = input("\nEnter binary sequence (e.g., 10110101): ")
    
    # Validate input
    if not all(bit in '01' for bit in binary_input):
        print("\n Error: Please enter only 0s and 1s")
        exit()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == '1':
            plot_selected_line_code(binary_input, "Unipolar NRZ", unipolar_nrz)
        
        elif choice == '2':
            plot_selected_line_code(binary_input, "Polar NRZ-L", polar_nrz_l)
        
        elif choice == '3':
            plot_selected_line_code(binary_input, "Polar NRZ-I", polar_nrz_i)
        
        elif choice == '4':
            plot_selected_line_code(binary_input, "Polar RZ", polar_rz)
        
        elif choice == '5':
            plot_selected_line_code(binary_input, "Manchester", manchester)
        
        elif choice == '6':
            plot_selected_line_code(binary_input, "Differential Manchester", differential_manchester)
        
        elif choice == '7':
            plot_selected_line_code(binary_input, "AMI (Bipolar)", ami)
        
        elif choice == '8':
            plot_selected_line_code(binary_input, "Pseudoternary (Bipolar)", pseudoternary)
        
        elif choice == '9':
            print("\n Thank you for using Line Coding Simulation!")
            print(" Goodbye!\n")
            break
        
        else:
            print("\n Invalid choice! Please select between 1-9")
        
        # Ask if user wants to continue
        continue_choice = input("\nDo you want to try another encoding? (y/n): ")
        if continue_choice.lower() != 'y':
            print("\n Thank you for using Line Coding Simulation!")
            print(" Goodbye!\n")
            break