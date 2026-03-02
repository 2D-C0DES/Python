
print("========== CHECKSUM ERROR DETECTION (n-bit) ==========")

# If number of data bits is not multiple of slice size then we will add padding to the lsb of the last slice to make all the same sized
# ---------------- FUNCTION FOR 1's COMPLEMENT ADDITION ----------------
def ones_complement_addition(a, b, n):
    result = ""
    carry = 0

    # Add from LSB to MSB
    for i in range(n-1, -1, -1):
        total = carry + int(a[i]) + int(b[i])
        bit = total % 2
        carry = total // 2
        result = str(bit) + result

    # Wrap-around carry
    if carry == 1:
        carry_binary = "0"*(n-1) + "1"
        result = ones_complement_addition(result, carry_binary, n)

    return result


# ---------------- SENDER SIDE ----------------

message = input("Enter binary message: ")

if not all(bit in '01' for bit in message):
    print("Error: Input must be binary.")
    exit()

n = int(input("Enter slice size (number of bits per block): "))

if len(message) % n != 0:
    print("Error: Message length must be multiple of slice size.")
    exit()

# Divide into n-bit slices
slices = []
for i in range(0, len(message), n):
    slices.append(message[i:i+n])

print("\nTransmitting Message Slices:")
for i in range(len(slices)):
    print("Slice", i+1, ":", slices[i])

# Add all slices
total_sum = slices[0]

for i in range(1, len(slices)):
    total_sum = ones_complement_addition(total_sum, slices[i], n)

print("\nBinary Sum (Before Complement):", total_sum)

# Find checksum (1's complement)
checksum = ""
for bit in total_sum:
    if bit == '0':
        checksum += '1'
    else:
        checksum += '0'

print("Generated Checksum:", checksum)

transmitted_message = message + checksum

print("\nFinal Transmitted Bit Stream:")
print(transmitted_message)


# ---------------- RECEIVER SIDE ----------------

print("\n========== RECEIVER SIDE ==========")

received = input("Enter received bit stream: ")

if len(received) % n != 0:
    print("Error: Received data not valid.")
    exit()

# Divide received into n-bit slices
received_slices = []
for i in range(0, len(received), n):
    received_slices.append(received[i:i+n])

print("\nReceived Slices:")
for i in range(len(received_slices)):
    print("Slice", i+1, ":", received_slices[i])

# Add all received slices
receiver_sum = received_slices[0]

for i in range(1, len(received_slices)):
    receiver_sum = ones_complement_addition(receiver_sum, received_slices[i], n)

print("\nReceiver Final Sum:", receiver_sum)

# Check if all bits are 1
if receiver_sum == "1"*n:
    print("Result: NO ERROR detected.")
else:
    print("Result: ERROR detected in transmission.")