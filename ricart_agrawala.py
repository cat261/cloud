import socket
import threading
import time
HOST = "127.0.0.1"
PORTS = {
    0: 6000,
    1: 6001,
    2: 6002,
    3: 6003
}
N = 4
# Change this value in each terminal
MY_ID = 0
clock = 0
state = "RELEASED"
my_request = None
replies_received = set()
deferred_requests = set()
lock = threading.Lock()

def send_message(process_id, message):
    try:
        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        s.connect(
            (HOST, PORTS[process_id])
        )
        s.send(message.encode())
        s.close()
    except ConnectionRefusedError:
        print(
            f"Could not connect to P{process_id}"
        )

def request_critical_section():
    global clock
    global state
    global my_request
    global replies_received
    with lock:
        clock += 1
        my_request = (clock, MY_ID)
        state = "REQUESTING"
        replies_received.clear()
        timestamp = clock
    print(
        f"\nP{MY_ID} requesting CS "
        f"with timestamp {timestamp}"
    )
    # Send REQUEST to every other process
    for process_id in range(N):
        if process_id != MY_ID:
            message = (
                f"REQUEST|{timestamp}|{MY_ID}"
            )
            send_message(
                process_id,
                message
            )
    # Wait for replies from all processes
    while True:
        with lock:
            if len(replies_received) == N - 1:
                break
        time.sleep(0.1)
    enter_critical_section()

def enter_critical_section():
    global state
    with lock:
        state = "ENTERED"

    print(
        f"\n>>> P{MY_ID} ENTERED "
        f"CRITICAL SECTION"
    )

    time.sleep(3)

    print(
        f">>> P{MY_ID} EXITED "
        f"CRITICAL SECTION"
    )
    release_critical_section()

def release_critical_section():
    global state
    global my_request
    with lock:

        state = "RELEASED"

        my_request = None

        pending = list(
            deferred_requests
        )

        deferred_requests.clear()

    # Send delayed replies
    for process_id in pending:

        send_message(
            process_id,
            f"REPLY|{MY_ID}"
        )

        print(
            f"P{MY_ID} sent deferred REPLY "
            f"to P{process_id}"
        )

def handle_request(timestamp, process_id):
    global clock
    with lock:
        clock = max(
            clock,
            timestamp
        ) + 1

        received_request = (
            timestamp,
            process_id
        )

        # If we are inside CS,
        # defer the request
        if state == "ENTERED":

            deferred_requests.add(
                process_id
            )

            print(
                f"P{MY_ID}: Deferred request "
                f"from P{process_id}"
            )

            return

        # If we are requesting CS,
        # compare priorities
        if state == "REQUESTING":

            if my_request < received_request:

                # Our request has priority
                deferred_requests.add(
                    process_id
                )

                print(
                    f"P{MY_ID}: Deferred request "
                    f"from P{process_id}"
                )

                return

    # Otherwise send REPLY
    send_message(
        process_id,
        f"REPLY|{MY_ID}"
    )

    print(
        f"P{MY_ID} sent REPLY "
        f"to P{process_id}"
    )

def receive_connections():
    global clock
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
        (HOST, PORTS[MY_ID])
    )
    server.listen()
    print(
        f"P{MY_ID} listening on "
        f"port {PORTS[MY_ID]}"
    )

    while True:
        conn, addr = server.accept()
        message = conn.recv(1024).decode()
        conn.close()
        parts = message.split("|")
        if parts[0] == "REQUEST":
            timestamp = int(parts[1])
            process_id = int(parts[2])
            handle_request(
                timestamp,
                process_id
            )
        elif parts[0] == "REPLY":
            process_id = int(parts[1])
            with lock:
                replies_received.add(
                    process_id
                )
            print(
                f"P{MY_ID} received REPLY "
                f"from P{process_id}"
            )

thread = threading.Thread(
    target=receive_connections
)
thread.daemon = True
thread.start()
time.sleep(2)
while True:
    print("\nOptions:")
    print("1. Request Critical Section")
    print("2. Exit")
    choice = input(
        f"P{MY_ID}: Enter choice: "
    )
    if choice == "1":
        request_critical_section()
    elif choice == "2":
        print(
            f"P{MY_ID} terminated."
        )

        break
    else:
        print("Invalid choice")