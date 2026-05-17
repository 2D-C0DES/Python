# udp_client.py

import socket

# ---------------- SERVER CONFIGURATION ----------------
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# ---------------- CREATE UDP SOCKET ----------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("\n========== UDP CLIENT ==========")

while True:

    print("\nSelect Operation")
    print("1. Echo Message")
    print("2. Mathematical Operation")
    print("3. DAYTIME Service")
    print("4. Exit")

    choice = input("\nEnter Choice: ")

    # =========================================================
    # 1. ECHO MESSAGE
    # =========================================================
    if choice == "1":

        message = input("Enter message to echo: ")

        request = f"ECHO:{message}"

        client_socket.sendto(request.encode(), (SERVER_IP, SERVER_PORT))

        response, _ = client_socket.recvfrom(BUFFER_SIZE)

        print("\n[SERVER RESPONSE]")
        print(response.decode())

    # =========================================================
    # 2. MATHEMATICAL OPERATION
    # =========================================================
    elif choice == "2":

        print("\nAvailable Operations")
        print("ADD")
        print("SUB")
        print("MUL")
        print("DIV")
        print("MOD")

        operation = input("Enter operation: ").upper()

        num1 = input("Enter first number: ")
        num2 = input("Enter second number: ")

        request = f"MATH:{operation}:{num1}:{num2}"

        client_socket.sendto(request.encode(), (SERVER_IP, SERVER_PORT))

        response, _ = client_socket.recvfrom(BUFFER_SIZE)

        print("\n[SERVER RESPONSE]")
        print(response.decode())

    # =========================================================
    # 3. DAYTIME SERVICE
    # =========================================================
    elif choice == "3":

        request = "DAYTIME"

        client_socket.sendto(request.encode(), (SERVER_IP, SERVER_PORT))

        response, _ = client_socket.recvfrom(BUFFER_SIZE)

        print("\n[SERVER RESPONSE]")
        print(response.decode())

    # =========================================================
    # 4. EXIT
    # =========================================================
    elif choice == "4":

        print("\nClient Closed")
        break

    else:
        print("\nInvalid Choice")

# Close socket
client_socket.close()