import socket
import pickle


# Define DataObject class
class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values


# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 5001

# Bind server
server_socket.bind((HOST, PORT))

# Listen for client
server_socket.listen(1)

print("Server started...")
print(f"Waiting for connection on {HOST}:{PORT}")

# Accept connection
client_socket, client_address = server_socket.accept()

print("Client connected:", client_address)

# Receive serialized object
data = client_socket.recv(4096)

# Deserialize object
obj = pickle.loads(data)

print("Object received successfully.")

# Display object details
print("Name:", obj.name)
print("Values:", obj.values)

# Calculate sum
total = sum(obj.values)

print("Sum of values:", total)

# Prepare response
response = f"Name: {obj.name}, Sum of values: {total}"

# Send response
client_socket.send(response.encode())

# Close connections
client_socket.close()
server_socket.close()

print("Server stopped.")