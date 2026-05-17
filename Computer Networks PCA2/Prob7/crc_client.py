import socket

# ---------------- CRC FUNCTIONS ---------------- #

def xor(a, b):

    result = []

    for i in range(1, len(b)):

        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


def mod2div(dividend, divisor):

    pick = len(divisor)

    temp = dividend[0:pick]

    while pick < len(dividend):

        if temp[0] == '1':
            temp = xor(divisor, temp) + dividend[pick]
        else:
            temp = xor('0' * pick, temp) + dividend[pick]

        pick += 1

    if temp[0] == '1':
        temp = xor(divisor, temp)
    else:
        temp = xor('0' * pick, temp)

    remainder = temp

    return remainder


def generate_crc(data, divisor):

    appended_data = data + '0' * (len(divisor) - 1)

    remainder = mod2div(appended_data, divisor)

    codeword = data + remainder

    return codeword


# ---------------- CLIENT ---------------- #

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

data = input("Enter Binary Data : ")
divisor = input("Enter Divisor Polynomial : ")

transmitted_data = generate_crc(data, divisor)

print("\nOriginal Data      :", data)
print("CRC Appended Data  :", transmitted_data)

choice = input("\nIntroduce Error? (y/n): ")

if choice.lower() == 'y':

    position = int(input("Enter Bit Position To Flip (starting from 0): "))

    temp = list(transmitted_data)

    if temp[position] == '0':
        temp[position] = '1'
    else:
        temp[position] = '0'

    transmitted_data = ''.join(temp)

    print("Corrupted Data     :", transmitted_data)

# Send divisor and data
client.send(divisor.encode())
client.send(transmitted_data.encode())

result = client.recv(1024).decode()

print("\nServer Response :", result)

client.close()