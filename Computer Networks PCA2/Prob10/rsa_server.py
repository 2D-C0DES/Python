import socket
import math
from datetime import datetime


# ---------------------------------------------------
# RSA ALGORITHM IMPLEMENTATION
# ---------------------------------------------------

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None


def generate_keys():
    # Two prime numbers
    p = 61
    q = 53

    # RSA modulus
    n = p * q

    # Euler Totient Function
    phi = (p - 1) * (q - 1)

    # Choose e such that gcd(e, phi) = 1
    e = 17

    if gcd(e, phi) != 1:
        raise Exception("e and phi are not coprime")

    # Compute private key d
    d = mod_inverse(e, phi)

    return (e, n), (d, n)


def encrypt(message, public_key):
    e, n = public_key

    encrypted = []

    for char in message:
        cipher = pow(ord(char), e, n)
        encrypted.append(cipher)

    return encrypted


def decrypt(ciphertext, private_key):
    d, n = private_key

    decrypted = ""

    for value in ciphertext:
        plain = chr(pow(value, d, n))
        decrypted += plain

    return decrypted


# ---------------------------------------------------
# DAYTIME SERVICE
# ---------------------------------------------------

def get_daytime_response():
    now = datetime.now()

    current_time = now.strftime("%d-%m-%Y %H:%M:%S")

    hour = now.hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return f"{greeting} | Current Date and Time: {current_time}"


# ---------------------------------------------------
# SOCKET SERVER
# ---------------------------------------------------

HOST = "127.0.0.1"
PORT = 5000

# Generate RSA keys
public_key, private_key = generate_keys()

print("\n========== RSA SERVER ==========")
print(f"Public Key  (e, n): {public_key}")
print(f"Private Key (d, n): {private_key}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f"\nServer listening on {HOST}:{PORT} ...")

conn, addr = server_socket.accept()

print(f"\nConnection established with {addr}")

# Send public key to client
conn.send(str(public_key).encode())

# Receive encrypted message
encrypted_message = conn.recv(4096).decode()

# Convert received string to list
encrypted_message = eval(encrypted_message)

print("\nEncrypted message received from client:")
print(encrypted_message)

# Decrypt message
decrypted_message = decrypt(encrypted_message, private_key)

print("\nDecrypted message from client:")
print(decrypted_message)

# Check request
if decrypted_message == "DAYTIME":
    response = get_daytime_response()
else:
    response = "Invalid Request"

print("\nServer Response:")
print(response)

# Encrypt response using public key
encrypted_response = encrypt(response, public_key)

print("\nEncrypted Response Sent To Client:")
print(encrypted_response)

# Send encrypted response
conn.send(str(encrypted_response).encode())

conn.close()
server_socket.close()

print("\nConnection closed.")