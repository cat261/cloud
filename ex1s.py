import socket

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host and port
HOST = "127.0.0.1"
PORT = 5000

# Bind socket to host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print("Server started...")
print(f"Waiting for connection on {HOST}:{PORT}")

# Accept client connection
client_socket, client_address = server_socket.accept()

print("Client connected:", client_address)

# Receive data from client
data = client_socket.recv(1024).decode()

print("Message received from client:", data)

# Parse numbers
numbers = list(map(int, data.split()))

# Calculate sum
total = sum(numbers)

print("Numbers:", numbers)
print("Sum:", total)

# Send result back to client
response = f"Sum of numbers = {total}"
client_socket.send(response.encode())

# Close connection
client_socket.close()
server_socket.close()

print("Server stopped.")