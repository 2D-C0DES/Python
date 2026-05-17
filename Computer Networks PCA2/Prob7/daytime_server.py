import socket
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("DAYTIME Server Waiting For Connection...")

conn, addr = server.accept()

print(f"Connected with {addr}")

request = conn.recv(1024).decode()

print("Client Request :", request)

if request == "DAYTIME":

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
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

    response = (
        f"{greeting}\n"
        f"Date : {current_date}\n"
        f"Time : {current_time}"
    )

else:
    response = "INVALID REQUEST"

conn.send(response.encode())

conn.close()
server.close()