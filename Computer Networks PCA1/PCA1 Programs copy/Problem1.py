import matplotlib.pyplot as plt

# ==========================================================
# Utility Function: Validate Binary Input
# ==========================================================
def validate_binary(data):
    for bit in data:
        if bit not in ['0', '1']:
            return False
    return True


# ==========================================================
# Manchester Encoding
# 1 -> Low(0) to High(1)
# 0 -> High(1) to Low(0)
# ==========================================================
def manchester_encoding(data):
    encoded = []

    for bit in data:
        if bit == '1':
            encoded.extend([0, 1])
        else:
            encoded.extend([1, 0])

    return encoded


# ==========================================================
# Differential Manchester Encoding
# Always mid transition
# 0 -> transition at beginning
# 1 -> no transition at beginning
# ==========================================================
def differential_manchester_encoding(data):
    encoded = []
    current_level = 1  # Starting with High

    for bit in data:

        if bit == '0':
            # Beginning transition
            current_level = 1 - current_level

        # First half
        encoded.append(current_level)

        # Mid transition
        current_level = 1 - current_level

        # Second half
        encoded.append(current_level)

    return encoded


# ==========================================================
# Plot Waveform
# ==========================================================
def plot_waveform(encoded_signal, title):
    time = []
    signal = []

    for i in range(len(encoded_signal)):
        time.extend([i, i + 1])
        signal.extend([encoded_signal[i], encoded_signal[i]])

    plt.figure()
    plt.step(time, signal, where='post')
    plt.ylim(-0.5, 1.5)
    plt.xlabel("Time")
    plt.ylabel("Signal Level")
    plt.title(title)
    plt.grid(True)
    plt.show()


# ==========================================================
# Demonstration Mode
# ==========================================================
def demonstration_mode():
    print("\n========== DEMONSTRATION MODE ==========")
    data = "1011100010"
    print("Input Data:", data)

    manchester = manchester_encoding(data)
    diff_manchester = differential_manchester_encoding(data)

    print("\nManchester Encoded Output:")
    print(manchester)

    print("\nDifferential Manchester Encoded Output:")
    print(diff_manchester)

    plot_waveform(manchester, "Manchester Encoding (Demo)")
    plot_waveform(diff_manchester, "Differential Manchester Encoding (Demo)")


# ==========================================================
# User Mode
# ==========================================================
def user_mode():
    print("\n========== USER INPUT MODE ==========")

    data = input("Enter binary data: ")

    if not validate_binary(data):
        print("Invalid binary input! Only 0 and 1 allowed.")
        return

    print("\nSelect Encoding Type:")
    print("1. Manchester Encoding")
    print("2. Differential Manchester Encoding")

    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        encoded = manchester_encoding(data)
        print("\nManchester Encoded Output:")
        print(encoded)
        plot_waveform(encoded, "Manchester Encoding (User Input)")

    elif choice == '2':
        encoded = differential_manchester_encoding(data)
        print("\nDifferential Manchester Encoded Output:")
        print(encoded)
        plot_waveform(encoded, "Differential Manchester Encoding (User Input)")

    else:
        print("Invalid choice!")


# ==========================================================
# MAIN LOOP CONTROL (Continuous Execution)
# ==========================================================
def main():

    while True:
        print("\n======================================")
        print("        LINE CODING PROGRAM")
        print("======================================")
        print("1. Demonstration Mode")
        print("2. User Input Mode")
        print("3. Exit")
        print("======================================")

        mode = input("Select Mode (1/2/3): ")

        if mode == '1':
            demonstration_mode()

        elif mode == '2':
            user_mode()

        elif mode == '3':
            print("\nExiting Program... Thank You.")
            break   # Proper controlled termination

        else:
            print("Invalid selection! Try again.")


if __name__ == "__main__":
    main()