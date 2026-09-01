import socket
import pickle


# Define DataObject class
class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values


# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 5001

# Connect to server
client_socket.connect((HOST, PORT))

print("Connected to server.")

# Create DataObject
name = input("Enter name: ")

values = list(
    map(
        int,
        input("Enter numbers separated by spaces: ").split()
    )
)

obj = DataObject(name, values)

# Serialize object
serialized_data = pickle.dumps(obj)

# Send serialized object
client_socket.send(serialized_data)

print("DataObject sent to server.")

# Receive response
response = client_socket.recv(4096).decode()

print("Response from server:")
print(response)

# Close socket
client_socket.close()