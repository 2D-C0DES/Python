# udp_server.py

import socket
from datetime import datetime

# ---------------- SERVER CONFIGURATION ----------------
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# ---------------- CREATE UDP SOCKET ----------------
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind server with IP and Port
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"\n[SERVER STARTED] UDP Server running on {SERVER_IP}:{SERVER_PORT}\n")


# ---------------- HELPER FUNCTION ----------------
def perform_operation(operation, num1, num2):
    """
    Performs mathematical operations based on client request.
    """

    if operation == "ADD":
        return num1 + num2

    elif operation == "SUB":
        return num1 - num2

    elif operation == "MUL":
        return num1 * num2

    elif operation == "DIV":
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2

    elif operation == "MOD":
        if num2 == 0:
            return "Error: Modulus by zero"
        return num1 % num2

    else:
        return "Invalid Operation"


# ---------------- MAIN SERVER LOOP ----------------
while True:

    # Receive message from client
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)

    # Decode received bytes into string
    message = data.decode().strip()

    print(f"[CLIENT {client_address}] -> {message}")

    # =========================================================
    # 1. ECHO SERVICE
    # =========================================================
    if message.startswith("ECHO:"):

        echo_message = message[5:]

        response = f"Echo From Server: {echo_message}"

        server_socket.sendto(response.encode(), client_address)

    # =========================================================
    # 2. DAYTIME SERVICE
    # =========================================================
    elif message == "DAYTIME":

        current_time = datetime.now()

        formatted_time = current_time.strftime("%d-%m-%Y %I:%M:%S %p")

        hour = current_time.hour

        # Greeting logic
        if 5 <= hour < 12:
            greeting = "Good Morning"

        elif 12 <= hour < 17:
            greeting = "Good Afternoon"

        elif 17 <= hour < 21:
            greeting = "Good Evening"

        else:
            greeting = "Good Night"

        response = f"{greeting}\nCurrent Date & Time: {formatted_time}"

        server_socket.sendto(response.encode(), client_address)

    # =========================================================
    # 3. MATHEMATICAL OPERATION
    # =========================================================
    elif message.startswith("MATH:"):

        try:
            # Format:
            # MATH:ADD:10:20

            parts = message.split(":")

            operation = parts[1]
            num1 = float(parts[2])
            num2 = float(parts[3])

            result = perform_operation(operation, num1, num2)

            response = f"Result = {result}"

        except Exception as error:
            response = f"Error: {error}"

        server_socket.sendto(response.encode(), client_address)

    # =========================================================
    # INVALID REQUEST
    # =========================================================
    else:

        response = "Invalid Request"

        server_socket.sendto(response.encode(), client_address)