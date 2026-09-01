import socket
import threading
import time

HOST = "127.0.0.1"

COORDINATOR_PORT = 7000

MY_ID = 1

MY_PORT = {
    1: 7001,
    2: 7002,
    3: 7003
}[MY_ID]


def send_to_coordinator(message):

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        s.connect(
            (HOST, COORDINATOR_PORT)
        )

        s.send(message.encode())

        s.close()

    except ConnectionRefusedError:

        print(
            "Coordinator is not running"
        )


def receive_messages():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, MY_PORT)
    )

    server.listen()

    while True:

        conn, address = server.accept()

        message = conn.recv(1024).decode()

        conn.close()

        if message == "GRANT":

            print(
                f"\n>>> P{MY_ID} ENTERED "
                f"CRITICAL SECTION"
            )

            # Simulate work
            time.sleep(5)

            print(
                f">>> P{MY_ID} EXITED "
                f"CRITICAL SECTION"
            )

            # Inform coordinator
            send_to_coordinator(
                f"RELEASE|{MY_ID}"
            )


def start_process():

    print("================================")
    print("      DISTRIBUTED PROCESS")
    print("================================")

    print(
        f"P{MY_ID} running on port {MY_PORT}"
    )

    # Start receiving thread
    thread = threading.Thread(
        target=receive_messages
    )

    thread.daemon = True
    thread.start()

    while True:

        print("\n1. Request Critical Section")
        print("2. Exit")

        choice = input(
            f"P{MY_ID}: Enter choice: "
        )

        if choice == "1":

            print(
                f"\nP{MY_ID} requesting "
                f"Critical Section..."
            )

            send_to_coordinator(
                f"REQUEST|{MY_ID}"
            )

        elif choice == "2":

            print(
                f"P{MY_ID} terminated."
            )

            break

        else:

            print("Invalid choice")


start_process()