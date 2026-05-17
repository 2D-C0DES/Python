import socket

HOST = '127.0.0.1'
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

while True:

    print("\n----- MENU -----")
    print("1. ADD")
    print("2. SUBTRACT")
    print("3. MULTIPLY")
    print("4. DIVIDE")
    print("5. MODULUS")
    print("6. EXIT")

    choice = int(input("Enter Choice : "))

    if choice == 6:
        break

    num1 = float(input("Enter First Number : "))
    num2 = float(input("Enter Second Number : "))

    if choice == 1:
        operation = "ADD"

    elif choice == 2:
        operation = "SUB"

    elif choice == 3:
        operation = "MUL"

    elif choice == 4:
        operation = "DIV"

    elif choice == 5:
        operation = "MOD"

    else:
        print("Invalid Choice")
        continue

    message = f"{operation} {num1} {num2}"

    client.send(message.encode())

    result = client.recv(1024).decode()

    print("Result :", result)

client.close()