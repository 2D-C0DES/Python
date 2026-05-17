# server.py

import socket
from datetime import datetime

# ---------------- SERVER CONFIGURATION ---------------- #

HOST = '127.0.0.1'
PORT = 5000

# ---------------- FUNCTION DEFINITIONS ---------------- #

def perform_operation(choice, num1, num2):
    """
    Performs mathematical operations based on user choice.
    """

    if choice == "ADD":
        return num1 + num2

    elif choice == "SUBTRACT":
        return num1 - num2

    elif choice == "MULTIPLY":
        return num1 * num2

    elif choice == "DIVISION":
        if num2 == 0:
            return "Error: Division by zero is not allowed."
        return num1 / num2

    elif choice == "MODULUS":
        if num2 == 0:
            return "Error: Modulus by zero is not allowed."
        return num1 % num2

    else:
        return "Invalid Operation"


def get_daytime():
    """
    Returns current date, time and greeting.
    """

    now = datetime.now()

    current_time = now.strftime("%I:%M:%S %p")
    current_date = now.strftime("%d-%m-%Y")

    hour = now.hour

    if 5 <= hour < 12:
        greeting = "Good Morning"

    elif 12 <= hour < 17:
        greeting = "Good Afternoon"

    elif 17 <= hour < 21:
        greeting = "Good Evening"

    else:
        greeting = "Good Night"

    return f"{greeting}\nDate: {current_date}\nTime: {current_time}"


# ---------------- SERVER SOCKET CREATION ---------------- #

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print("SERVER IS WAITING FOR CONNECTION...\n")

# ---------------- ACCEPT CLIENT CONNECTION ---------------- #

client_socket, client_address = server_socket.accept()

print(f"CONNECTED WITH CLIENT : {client_address}\n")

# ---------------- SERVER EXECUTION LOOP ---------------- #

while True:

    data = client_socket.recv(1024).decode()

    if not data:
        break

    # -------- EXIT CONDITION -------- #

    if data.upper() == "EXIT":

        print("CLIENT DISCONNECTED.")
        break

    # -------- DAYTIME SERVICE -------- #

    elif data.upper() == "DAYTIME":

        print("DAYTIME REQUEST RECEIVED FROM CLIENT")

        response = get_daytime()

        client_socket.send(response.encode())

    # -------- ECHO MESSAGE -------- #

    elif data.startswith("ECHO:"):

        message = data[5:]

        print(f"CLIENT MESSAGE : {message}")

        response = f"Echo From Server : {message}"

        client_socket.send(response.encode())

    # -------- MATHEMATICAL OPERATION -------- #

    elif data.startswith("MATH:"):

        # Format:
        # MATH:ADD:10:20

        parts = data.split(":")

        operation = parts[1]
        num1 = float(parts[2])
        num2 = float(parts[3])

        result = perform_operation(operation, num1, num2)

        print(f"OPERATION : {operation}")
        print(f"NUMBERS   : {num1}, {num2}")
        print(f"RESULT    : {result}\n")

        client_socket.send(str(result).encode())

    # -------- INVALID REQUEST -------- #

    else:

        client_socket.send("INVALID REQUEST".encode())

# ---------------- CLOSE CONNECTION ---------------- #

client_socket.close()
server_socket.close()

print("\nSERVER CLOSED.")