import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []


def broadcast(message, sender):
    """Send message to all clients except the sender."""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)


def handle_client(client, address):
    print(f"[CONNECTED] {address}")

    client.send("Connected to the Message Passing Server.".encode())

    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            print(f"[{address}] {message.decode()}")

            # Send message to other connected clients
            broadcast(message, client)

        except:
            break

    if client in clients:
        clients.remove(client)

    client.close()
    print(f"[DISCONNECTED] {address}")


# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind server to IP and port
server.bind((HOST, PORT))

# Listen for incoming connections
server.listen()

print("===================================")
print(" Message Passing Server")
print("===================================")
print(f"Server listening on {HOST}:{PORT}")

while True:
    # Accept client connection
    client, address = server.accept()

    # Add client to list
    clients.append(client)

    # Create separate thread for each client
    thread = threading.Thread(
        target=handle_client,
        args=(client, address)
    )

    thread.start()

    print(f"Active Clients: {len(clients)}")