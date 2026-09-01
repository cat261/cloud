import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 7000

# Waiting processes
waiting_queue = []

# Indicates whether CS is occupied
cs_busy = False

# Lock for shared data
lock = threading.Lock()


def send_message(process_id, message):
    """
    Send a message to a process.
    """

    ports = {
        1: 7001,
        2: 7002,
        3: 7003
    }

    try:
        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        s.connect(
            (HOST, ports[process_id])
        )

        s.send(message.encode())

        s.close()

    except ConnectionRefusedError:

        print(
            f"P{process_id} is not available"
        )


def handle_request(process_id):
    """
    Handle a REQUEST from a process.
    """

    global cs_busy

    with lock:

        if not cs_busy:

            # CS is free
            cs_busy = True

            print(
                f"\nP{process_id} requested CS"
            )

            print(
                f"Coordinator: Granting CS to P{process_id}"
            )

            send_message(
                process_id,
                "GRANT"
            )

        else:

            # CS is busy
            waiting_queue.append(
                process_id
            )

            print(
                f"P{process_id} added to waiting queue"
            )


def handle_release(process_id):
    """
    Handle RELEASE from a process.
    """

    global cs_busy

    with lock:

        print(
            f"\nP{process_id} released CS"
        )

        cs_busy = False

        # Give CS to next waiting process
        if waiting_queue:

            next_process = waiting_queue.pop(0)

            cs_busy = True

            print(
                f"Coordinator: Granting CS to "
                f"P{next_process}"
            )

            send_message(
                next_process,
                "GRANT"
            )


def start_coordinator():

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
        (HOST, PORT)
    )

    server.listen()
    print(
        f"Coordinator running on port {PORT}"
    )

    while True:

        conn, address = server.accept()

        message = conn.recv(1024).decode()

        conn.close()

        parts = message.split("|")

        message_type = parts[0]

        process_id = int(parts[1])

        if message_type == "REQUEST":

            handle_request(process_id)

        elif message_type == "RELEASE":

            handle_release(process_id)


start_coordinator()