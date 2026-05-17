import socket

HOST = '127.0.0.1'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("Math Server Waiting For Connection...")

conn, addr = server.accept()

print(f"Connected with {addr}")

while True:

    data = conn.recv(1024).decode()

    if not data:
        break

    parts = data.split()

    operation = parts[0]
    num1 = float(parts[1])
    num2 = float(parts[2])

    if operation == "ADD":
        result = num1 + num2

    elif operation == "SUB":
        result = num1 - num2

    elif operation == "MUL":
        result = num1 * num2

    elif operation == "DIV":

        if num2 == 0:
            result = "Division By Zero Error"
        else:
            result = num1 / num2

    elif operation == "MOD":

        if num2 == 0:
            result = "Modulo By Zero Error"
        else:
            result = num1 % num2

    else:
        result = "Invalid Operation"

    conn.send(str(result).encode())

conn.close()
server.close()