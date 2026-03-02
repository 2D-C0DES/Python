# CRC Error Detection Program (Algorithmically Accurate Version)
# Modes:
# 1. Example Mode (Given in Question)
# 2. User Driven Mode
# 3. Exit


# ------------------ CRC CORE LOGIC ------------------

def modulo2_division(dividend, divisor):
    dividend = list(dividend)
    divisor = list(divisor)
    n = len(divisor)

    for i in range(len(dividend) - n + 1):
        if dividend[i] == '1':
            for j in range(n):
                dividend[i + j] = str(
                    int(dividend[i + j]) ^ int(divisor[j])
                )

    remainder = ''.join(dividend[-(n - 1):])
    return remainder


def generate_crc(data, divisor):
    appended_data = data + '0' * (len(divisor) - 1)
    remainder = modulo2_division(appended_data, divisor)
    return remainder


def sender_side(data, divisor):
    print("\n=========== SENDER SIDE ===========")
    remainder = generate_crc(data, divisor)
    transmitted = data + remainder

    print("Original Data        :", data)
    print("Divisor              :", divisor)
    print("CRC Remainder        :", remainder)
    print("Transmitted Bitstream:", transmitted)

    return transmitted


def receiver_side(received_data, divisor):
    print("\n=========== RECEIVER SIDE ===========")
    print("Received Bitstream   :", received_data)

    remainder = modulo2_division(received_data, divisor)

    print("Remainder After Division:", remainder)

    if set(remainder) == {'0'}:
        print("Result: ✅ No Error Detected")
    else:
        print("Result: ❌ Error Detected in Received Message")


# ------------------ MAIN MENU ------------------

while True:

    print("\n========== CRC ERROR DETECTION ==========")
    print("1. Example Mode (M=110001101, D=X^4+X^2+1)")
    print("2. User Driven Mode")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        data = "110001101"
        divisor = "10101"  # X^4 + X^2 + 1

        transmitted = sender_side(data, divisor)

        print("\n--- Transmission Options ---")
        print("1. Use Correct Bitstream")
        print("2. Enter Custom Received Bitstream")
        print("3. Introduce Manual Bit Error")

        option = input("Choose option: ")

        if option == '1':
            receiver_side(transmitted, divisor)

        elif option == '2':
            received = input("Enter received bitstream: ")
            receiver_side(received, divisor)

        elif option == '3':
            error_index = int(input("Enter bit position to flip (starting from 0): "))
            corrupted = list(transmitted)

            if corrupted[error_index] == '0':
                corrupted[error_index] = '1'
            else:
                corrupted[error_index] = '0'

            corrupted = ''.join(corrupted)
            receiver_side(corrupted, divisor)

        else:
            print("Invalid Option")

    elif choice == '2':
        data = input("Enter binary data: ")
        divisor = input("Enter divisor in binary: ")

        transmitted = sender_side(data, divisor)

        print("\n--- Transmission Options ---")
        print("1. Use Correct Bitstream")
        print("2. Enter Custom Received Bitstream")
        print("3. Introduce Manual Bit Error")

        option = input("Choose option: ")

        if option == '1':
            receiver_side(transmitted, divisor)

        elif option == '2':
            received = input("Enter received bitstream: ")
            receiver_side(received, divisor)

        elif option == '3':
            error_index = int(input("Enter bit position to flip (starting from 0): "))
            corrupted = list(transmitted)

            if corrupted[error_index] == '0':
                corrupted[error_index] = '1'
            else:
                corrupted[error_index] = '0'

            corrupted = ''.join(corrupted)
            receiver_side(corrupted, divisor)

        else:
            print("Invalid Option")

    elif choice == '3':
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice! Try Again.")