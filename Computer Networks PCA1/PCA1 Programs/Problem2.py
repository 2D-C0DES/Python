# ------------------------------------------------------------
# Program: Bit Stuffing and De-Stuffing Demonstration
# Modes:
#   1 -> Default Flag (111110)
#   2 -> User Defined Flag (any length)
# ------------------------------------------------------------

DEFAULT_FLAG = "111110"


# CALCULATING NUMBER OF CONSECUTIVE 1s IN FLAG
def count_consecutive_ones(flag):
    max_count = 0
    current_count = 0

    for bit in flag:
        if bit == '1':
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 0

    return max_count

# ---------------- BIT STUFFING FUNCTION ---------------------

def bit_stuff(bit_stream, flag):
    data = list(bit_stream)   # Single dynamic array
    count = 0
    i = 0
    stuff_positions = []

    print("\n--- Bit Stuffing Process ---")

    while i < len(data):
        if data[i] == '1':
            count += 1
        else:
            count = 0

        # Stuff when consecutive 1s = count_consecutive_ones(flag) - 1
        if count == count_consecutive_ones(flag) - 1:
            data.insert(i + 1, '0')   # Shifting operation
            stuff_positions.append(i + 1)
            print(f"Stuffed '0' at position {i + 1}")
            count = 0
            i += 1

        i += 1

    return ''.join(data), stuff_positions


# ---------------- DE-STUFFING FUNCTION ----------------------

def bit_destuff(stuffed_stream, flag):
    data = list(stuffed_stream)   # Same single array
    count = 0
    i = 0
    removed_positions = []

    print("\n--- De-Stuffing Process ---")

    while i < len(data):
        if data[i] == '1':
            count += 1
        else:
            count = 0

        if count == count_consecutive_ones(flag) - 1:
            if i + 1 < len(data) and data[i + 1] == '0':
                data.pop(i + 1)   # Shifting operation
                removed_positions.append(i + 1)
                print(f"Removed stuffed '0' at position {i + 1}")
                count = 0

        i += 1

    return ''.join(data), removed_positions


# ------------------------- MAIN MENU ------------------------

def main():

    stuffed_data = ""
    flag = ""

    while True:

        print("\n=========== MAIN MENU ===========")
        print("1. Use Default Flag (111110)")
        print("2. Use Custom Flag (User Defined)")
        print("3. Exit")

        mode = input("Select Mode: ")

        if mode == '1':
            flag = DEFAULT_FLAG
            print(f"\nUsing Default Flag: {flag}")

        elif mode == '2':
            flag = input("Enter custom flag pattern (any bit length): ")

            # Basic validation
            if not all(bit in '01' for bit in flag):
                print("Invalid flag. Must contain only 0 and 1.")
                continue

            print(f"\nUsing Custom Flag: {flag}")

        elif mode == '3':
            print("Exiting Program...")
            break

        else:
            print("Invalid mode! Try again.")
            continue


        # ------------ SUB MENU ------------
        while True:

            print("\n----- OPERATIONS MENU -----")
            print("1. Perform Bit Stuffing")
            print("2. Perform De-Stuffing")
            print("3. Change Mode")

            choice = input("Enter your choice: ")

            if choice == '1':

                bit_stream = input("Enter binary data: ")

                if not all(bit in '01' for bit in bit_stream):
                    print("Invalid data. Enter only 0 and 1.")
                    continue

                stuffed_data, positions = bit_stuff(bit_stream, flag)

                print("\nOriginal Data     :", bit_stream)
                print("Stuffed Data      :", stuffed_data)
                print("Stuffed Positions :", positions)

            elif choice == '2':

                if stuffed_data == "":
                    print("No stuffed data available. Perform stuffing first.")
                else:
                    destuffed_data, removed = bit_destuff(stuffed_data, flag)

                    print("\nStuffed Data      :", stuffed_data)
                    print("De-Stuffed Data   :", destuffed_data)
                    print("Removed Positions :", removed)

            elif choice == '3':
                break

            else:
                print("Invalid choice!")


if __name__ == "__main__":
    main()

    