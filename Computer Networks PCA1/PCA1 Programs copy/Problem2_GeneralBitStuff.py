# ------------------------------------------------------------
# General Bit Stuffing & De-Stuffing
# Works for ANY flag pattern (not only 111110 type)
# ------------------------------------------------------------

DEFAULT_FLAG = "111110"


# ---------------- GENERAL BIT STUFFING ----------------------

def bit_stuff(bit_stream, flag):
    data = list(bit_stream)   # Single dynamic array
    n = len(flag)
    i = 0
    stuff_positions = []

    print("\n--- Bit Stuffing Process ---")

    while i <= len(data) - n + 1:

        # Check if first n-1 bits match flag prefix
        if ''.join(data[i:i+n-1]) == flag[:-1]:
            
            # If next bit would complete the flag
            if i + n - 1 < len(data) and data[i+n-1] == flag[-1]:
                
                # Insert opposite bit of last flag bit
                stuffed_bit = '1' if flag[-1] == '0' else '0'
                data.insert(i + n - 1, stuffed_bit)

                stuff_positions.append(i + n - 1)
                print(f"Stuffed '{stuffed_bit}' at position {i + n - 1}")

                i += n   # Skip past stuffed section
                continue

        i += 1

    return ''.join(data), stuff_positions


# ---------------- GENERAL DE-STUFFING -----------------------

def bit_destuff(stuffed_stream, flag):
    data = list(stuffed_stream)
    n = len(flag)
    i = 0
    removed_positions = []

    print("\n--- De-Stuffing Process ---")

    while i <= len(data) - n:

        if ''.join(data[i:i+n-1]) == flag[:-1]:

            # Check for stuffed bit
            expected_stuffed_bit = '1' if flag[-1] == '0' else '0'

            if data[i+n-1] == expected_stuffed_bit:
                data.pop(i + n - 1)
                removed_positions.append(i + n - 1)
                print(f"Removed stuffed bit at position {i + n - 1}")

                i += n - 1
                continue

        i += 1

    return ''.join(data), removed_positions


# ---------------------------- MENU --------------------------

def main():

    stuffed_data = ""
    flag = ""

    while True:

        print("\n=========== MAIN MENU ===========")
        print("1. Use Default Flag (111110)")
        print("2. Use Custom Flag")
        print("3. Exit")

        mode = input("Select Mode: ")

        if mode == '1':
            flag = DEFAULT_FLAG
            print(f"\nUsing Default Flag: {flag}")

        elif mode == '2':
            flag = input("Enter custom flag pattern: ")

            if not all(bit in '01' for bit in flag):
                print("Invalid flag! Only 0 and 1 allowed.")
                continue

            print(f"\nUsing Custom Flag: {flag}")

        elif mode == '3':
            print("Exiting program...")
            break

        else:
            print("Invalid choice!")
            continue


        # -------- OPERATIONS MENU --------

        while True:

            print("\n----- OPERATIONS MENU -----")
            print("1. Perform Bit Stuffing")
            print("2. Perform De-Stuffing")
            print("3. Change Mode")

            choice = input("Enter your choice: ")

            if choice == '1':

                bit_stream = input("Enter binary data: ")

                if not all(bit in '01' for bit in bit_stream):
                    print("Invalid data! Only 0 and 1 allowed.")
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