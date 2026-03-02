
# RIGHT to LEFT orientation

# Hamming Code (Right-to-Left Traditional Method)

def calculate_redundant_bits(m):
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    return r


def insert_parity_positions(data, r):
    m = len(data)
    n = m + r
    j = 0  # data index
    result = ['0'] * n

    # Fill from RIGHT to LEFT
    for i in range(1, n + 1):
        if i == 2 ** int(i).bit_length() - 2:  # Check power of 2
            continue

    # Better explicit power-of-2 check
    j = 0
    for i in range(1, n + 1):
        if (i & (i - 1)) == 0:  # parity position
            result[-i] = '0'
        else:
            result[-i] = data[m - 1 - j]
            j += 1

    return result


def calculate_parity_bits(arr, r):
    n = len(arr)

    for i in range(r):
        parity_position = 2 ** i
        parity = 0

        for j in range(1, n + 1):
            if j & parity_position:
                parity ^= int(arr[-j])

        arr[-parity_position] = str(parity)

    return arr


def detect_error(arr, r):
    n = len(arr)
    error_position = 0

    for i in range(r):
        parity_position = 2 ** i
        parity = 0

        for j in range(1, n + 1):
            if j & parity_position:
                parity ^= int(arr[-j])

        if parity != 0:
            error_position += parity_position

    return error_position


# ---------------- MAIN ---------------- #

data = input("Enter binary data: ")

if not all(bit in '01' for bit in data):
    print("Invalid input. Enter binary data only.")
    exit()

m = len(data)

# Step 1: Calculate redundant bits
r = calculate_redundant_bits(m)
print("\nNumber of redundant bits required =", r)

# Step 2: Insert parity placeholders (Right-to-Left)
arr = insert_parity_positions(data, r)

# Step 3: Calculate parity bits
arr = calculate_parity_bits(arr, r)

transmitted = ''.join(arr)
print("\nTransmitting bit stream =", transmitted)

# Step 4: Receive message
received = input("\nEnter received bit stream (you may introduce error): ")

if len(received) != len(transmitted):
    print("Error: Length mismatch!")
    exit()

received_arr = list(received)

# Step 5: Detect error
error_position = detect_error(received_arr, r)

if error_position == 0:
    print("\nNo error detected.")
    corrected = received_arr
else:
    print("\nError detected at position (from RIGHT) =", error_position)

    # Correct error
    index = -error_position
    received_arr[index] = '1' if received_arr[index] == '0' else '0'
    corrected = received_arr

    print("Corrected bit stream =", ''.join(corrected))

# Step 6: Extract original data
original_data = ''
n = len(corrected)

for i in range(1, n + 1):
    if not (i & (i - 1)) == 0:  # not power of 2
        original_data = corrected[-i] + original_data

print("Recovered original data =", original_data)