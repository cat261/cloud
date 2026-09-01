import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server details
HOST = "127.0.0.1"
PORT = 5000

# Connect to server
client_socket.connect((HOST, PORT))

print("Connected to server.")

# Get numbers from user
numbers = input("Enter numbers separated by spaces: ")

# Send numbers to server
client_socket.send(numbers.encode())

# Receive response
response = client_socket.recv(1024).decode()

print("Response from server:", response)

# Close connection
client_socket.close()