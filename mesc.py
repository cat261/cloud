import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    """Receive messages from the server."""
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            print("\n" + message.decode())
            print("Enter messages: ", end="")

        except:
            break


# Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect((HOST, PORT))

print("Connected to the Message Passing Server.")

# Thread for receiving messages
thread = threading.Thread(
    target=receive_messages,
    args=(client,)
)

thread.daemon = True
thread.start()


# Send messages
while True:

    message = input("Enter message: ")

    if message.lower() == "exit":
        break

    client.send(message.encode())


client.close()
print("Disconnected from server.")