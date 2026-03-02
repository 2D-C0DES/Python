def ones_complement_addition(a, b):
    """
    Perform 1's complement addition of two binary strings.
    """
    max_len = max(len(a), len(b))
    
    # Make both binary strings equal length
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    result = ''
    carry = 0

    # Add bit by bit from LSB to MSB
    for i in range(max_len - 1, -1, -1):
        total = carry
        total += 1 if a[i] == '1' else 0
        total += 1 if b[i] == '1' else 0

        bit = total % 2
        carry = total // 2

        result = str(bit) + result

    # If carry remains, wrap around
    if carry:
        result = ones_complement_addition(result, '1'.zfill(max_len))

    return result


def ones_complement(binary):
    """
    Find 1's complement of binary string
    """
    complement = ''
    for bit in binary:
        if bit == '0':
            complement += '1'
        else:
            complement += '0'
    return complement


def checksum_program():
    print("\n===== CHECKSUM ERROR DETECTION (4-bit slices) =====")

    message = input("Enter binary message (multiple of 4 bits): ")

    # Validation
    if not all(bit in '01' for bit in message):
        print("Error: Input must be binary.")
        return

    if len(message) % 4 != 0:
        print("Error: Number of bits must be multiple of 4.")
        return

    # Divide into 4-bit slices
    slices = [message[i:i+4] for i in range(0, len(message), 4)]

    print("\nTransmitting Message Slices:")
    for i, s in enumerate(slices):
        print(f"Slice {i+1}: {s}")

    # Perform checksum calculation
    total_sum = slices[0]

    for i in range(1, len(slices)):
        total_sum = ones_complement_addition(total_sum, slices[i])

    print("\nBinary Sum (Before Complement):", total_sum)

    checksum = ones_complement(total_sum)

    print("Checksum (1's Complement of Sum):", checksum)

    transmitted_message = message + checksum

    print("\nFinal Transmitted Bit Stream:")
    print(transmitted_message)


# Run program
checksum_program()