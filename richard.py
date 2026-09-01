import socket
import threading
import time
HOST = "127.0.0.1"
PORTS = {
    0: 5000,
    1: 5001,
    2: 5002,
    3: 5003
}
N = 4
# Change this for each terminal:
MY_ID = 0
HAS_TOKEN = (MY_ID == 0)
def send_token():
    next_id = (MY_ID + 1) % N
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORTS[next_id]))
        s.send("TOKEN".encode())
        s.close()
        print(f"Token sent from P{MY_ID} to P{next_id}")

    except ConnectionRefusedError:
        print(f"P{next_id} is not running")

def receive_connections():
    global HAS_TOKEN
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    server.bind((HOST, PORTS[MY_ID]))
    server.listen()
    print(f"P{MY_ID} started on port {PORTS[MY_ID]}")
    while True:
        conn, addr = server.accept()
        message = conn.recv(1024).decode()
        conn.close()
        if message == "TOKEN":
            HAS_TOKEN = True
            print(f"\nP{MY_ID} received TOKEN")
            # Ask user whether to enter CS
            choice = input(
                f"P{MY_ID}: Enter CS? (y/n): "
            )
            if choice.lower() == "y":
                enter_critical_section()
            # Pass token to next process
            HAS_TOKEN = False
            send_token()

def enter_critical_section():
    print(f"\n>>> P{MY_ID} ENTERED CRITICAL SECTION")
    time.sleep(3)
    print(f">>> P{MY_ID} EXITED CRITICAL SECTION\n")

thread = threading.Thread(
    target=receive_connections
)
thread.daemon = True
thread.start()
if HAS_TOKEN:
    time.sleep(2)
    choice = input(
        "P0: Enter CS? (y/n): "
    )
    if choice.lower() == "y":
        enter_critical_section()
    HAS_TOKEN = False
    send_token()
# Keep program running
while True:
    time.sleep(1)