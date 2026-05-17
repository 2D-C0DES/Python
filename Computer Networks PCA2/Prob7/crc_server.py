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


def verify_crc(received_data, divisor):

    remainder = mod2div(received_data, divisor)

    if '1' in remainder:
        return False
    else:
        return True


# ---------------- SERVER ---------------- #

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("CRC Server Waiting For Connection...")

conn, addr = server.accept()

print(f"Connected with {addr}")

# Receive divisor polynomial
divisor = conn.recv(1024).decode()

# Receive transmitted data
received_data = conn.recv(1024).decode()

print("\nReceived Bit Stream :", received_data)
print("Divisor Polynomial  :", divisor)

# Verify CRC
status = verify_crc(received_data, divisor)

if status:
    result = "NO ERROR DETECTED"
else:
    result = "ERROR DETECTED"

print("Verification Result :", result)

conn.send(result.encode())

conn.close()
server.close()