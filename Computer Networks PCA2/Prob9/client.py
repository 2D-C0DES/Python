# client.py

import socket

# ---------------- CLIENT CONFIGURATION ---------------- #

HOST = '127.0.0.1'
PORT = 5000

# ---------------- CLIENT SOCKET CREATION ---------------- #

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print("CONNECTED TO SERVER\n")

# ---------------- MENU LOOP ---------------- #

while True:

    print("\n========== MENU ==========")
    print("1. Echo Message")
    print("2. Mathematical Operation")
    print("3. DAYTIME Service")
    print("4. Exit")

    choice = input("ENTER YOUR CHOICE : ")

    # -------- ECHO MESSAGE -------- #

    if choice == "1":

        message = input("ENTER MESSAGE : ")

        send_data = f"ECHO:{message}"

        client_socket.send(send_data.encode())

        response = client_socket.recv(1024).decode()

        print("\nSERVER RESPONSE :")
        print(response)

    # -------- MATHEMATICAL OPERATION -------- #

    elif choice == "2":

        print("\nAVAILABLE OPERATIONS")
        print("1. ADD")
        print("2. SUBTRACT")
        print("3. MULTIPLY")
        print("4. DIVISION")
        print("5. MODULUS")

        op_choice = input("ENTER OPERATION CHOICE : ")

        operations = {
            "1": "ADD",
            "2": "SUBTRACT",
            "3": "MULTIPLY",
            "4": "DIVISION",
            "5": "MODULUS"
        }

        if op_choice not in operations:

            print("INVALID OPERATION CHOICE")
            continue

        num1 = float(input("ENTER FIRST NUMBER  : "))
        num2 = float(input("ENTER SECOND NUMBER : "))

        operation = operations[op_choice]

        send_data = f"MATH:{operation}:{num1}:{num2}"

        client_socket.send(send_data.encode())

        result = client_socket.recv(1024).decode()

        print(f"\nRESULT = {result}")

    # -------- DAYTIME SERVICE -------- #

    elif choice == "3":

        client_socket.send("DAYTIME".encode())

        response = client_socket.recv(1024).decode()

        print("\nSERVER RESPONSE :")
        print(response)

    # -------- EXIT -------- #

    elif choice == "4":

        client_socket.send("EXIT".encode())

        print("DISCONNECTED FROM SERVER")

        break

    # -------- INVALID CHOICE -------- #

    else:

        print("INVALID MENU CHOICE")

# ---------------- CLOSE SOCKET ---------------- #

client_socket.close()