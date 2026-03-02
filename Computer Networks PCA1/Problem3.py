# CRC Error Detection Program
# Two Modes:
# 1. Example Mode (Given in Question)
# 2. User Driven Mode
# 3. Exit

def xor(a, b):
    result = ""
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result


def crc_division(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    return tmp


def generate_crc(data, divisor):
    l_key = len(divisor)
    appended_data = data + '0' * (l_key - 1)
    remainder = crc_division(appended_data, divisor)
    return remainder


def sender(data, divisor):
    remainder = generate_crc(data, divisor)
    transmitted_data = data + remainder
    print("\n--- SENDER SIDE ---")
    print("Original Data       :", data)
    print("CRC Remainder       :", remainder)
    print("Transmitted Bitstream:", transmitted_data)
    return transmitted_data


def receiver(received_data, divisor):
    print("\n--- RECEIVER SIDE ---")
    remainder = crc_division(received_data, divisor)
    print("Received Data       :", received_data)
    print("Remainder After Division:", remainder)

    if '1' in remainder:
        print("Result: Error Detected in Received Message")
    else:
        print("Result: No Error Detected")


# ================= MAIN MENU =================

while True:
    print("\n========== CRC ERROR DETECTION ==========")
    print("1. Example Mode (Given Question)")
    print("2. User Driven Mode")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        data = "110001101"
        divisor = "10101"  # X^4 + X^2 + 1

        transmitted = sender(data, divisor)

        print("\nSimulating Transmission...")
        received = input("Enter received bitstream (or press Enter for no error): ")

        if received == "":
            received = transmitted

        receiver(received, divisor)

    elif choice == '2':
        data = input("Enter binary data: ")
        divisor = input("Enter divisor in binary: ")

        transmitted = sender(data, divisor)

        print("\nSimulating Transmission...")
        received = input("Enter received bitstream (modify bits to simulate error): ")

        receiver(received, divisor)

    elif choice == '3':
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice! Try Again.")