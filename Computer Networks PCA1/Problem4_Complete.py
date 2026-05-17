def ones_complement_addition(a, b):
    # Perform 1's complement addition of two 4-bit binary strings
    
    result = ""
    carry = 0

    for i in range(3, -1, -1):  # from LSB to MSB
        total = carry + int(a[i]) + int(b[i])
        bit = total % 2
        carry = total // 2
        result = str(bit) + result

    # Wrap-around carry
    if carry == 1:
        result = ones_complement_addition(result, "0001")

    return result


print("========== CHECKSUM ERROR DETECTION (4-bit) ==========")

# ------------------- SENDER SIDE -------------------

message = input("Enter binary message (multiple of 4 bits): ")

if not all(bit in '01' for bit in message):
    print("Error: Input must be binary.")
    exit()

if len(message) % 4 != 0:
    print("Error: Number of bits must be multiple of 4.")
    exit()

# Divide into 4-bit slices
slices = []
for i in range(0, len(message), 4):
    slices.append(message[i:i+4])

print("\nTransmitting Message Slices:")
for i in range(len(slices)):
    print("Slice", i+1, ":", slices[i])

# Add all slices using 1's complement addition
total_sum = slices[0]

for i in range(1, len(slices)):
    total_sum = ones_complement_addition(total_sum, slices[i])

print("\nBinary Sum (Before Complement):", total_sum)

# Find checksum (1's complement of sum)
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

# ------------------- RECEIVER SIDE -------------------

print("\n========== RECEIVER SIDE ==========")

received = input("Enter received bit stream: ")

if len(received) % 4 != 0:
    print("Error: Received data not valid (must be multiple of 4).")
    exit()

# Divide received data into 4-bit slices
received_slices = []
for i in range(0, len(received), 4):
    received_slices.append(received[i:i+4])

print("\nReceived Slices:")
for i in range(len(received_slices)):
    print("Slice", i+1, ":", received_slices[i])

# Add all received slices
receiver_sum = received_slices[0]

for i in range(1, len(received_slices)):
    receiver_sum = ones_complement_addition(receiver_sum, received_slices[i])

print("\nReceiver Final Sum:", receiver_sum)

# Check if all bits are 1
if receiver_sum == "1111":
    print("Result: NO ERROR detected.")
else:
    print("Result: ERROR detected in transmission.")