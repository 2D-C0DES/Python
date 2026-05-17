import socket


# ---------------------------------------------------
# RSA DECRYPTION & ENCRYPTION
# ---------------------------------------------------

def decrypt(ciphertext, private_key):
    d, n = private_key

    decrypted = ""

    for value in ciphertext:
        plain = chr(pow(value, d, n))
        decrypted += plain

    return decrypted


def encrypt(message, public_key):
    e, n = public_key

    encrypted = []

    for char in message:
        cipher = pow(ord(char), e, n)
        encrypted.append(cipher)

    return encrypted


# ---------------------------------------------------
# CLIENT RSA KEYS
# ---------------------------------------------------

# Same keys used for demonstration
# (In real RSA systems keys are managed differently)

public_key = None

private_key = (2753, 3233)

# ---------------------------------------------------
# SOCKET CLIENT
# ---------------------------------------------------

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print("\n========== RSA CLIENT ==========")

# Receive public key from server
public_key_data = client_socket.recv(1024).decode()

public_key = eval(public_key_data)

print(f"\nReceived Public Key From Server: {public_key}")

# Message to send
message = "DAYTIME"

print(f"\nOriginal Message:")
print(message)

# Encrypt message
encrypted_message = encrypt(message, public_key)

print("\nEncrypted Message Sent To Server:")
print(encrypted_message)

# Send encrypted message
client_socket.send(str(encrypted_message).encode())

# Receive encrypted response
encrypted_response = client_socket.recv(4096).decode()

encrypted_response = eval(encrypted_response)

print("\nEncrypted Response Received From Server:")
print(encrypted_response)

# Decrypt response
decrypted_response = decrypt(encrypted_response, private_key)

print("\nDecrypted Response From Server:")
print(decrypted_response)

client_socket.close()