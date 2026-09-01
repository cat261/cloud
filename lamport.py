class LamportClock:
    def __init__(self, process_name):
        self.process_name = process_name
        self.clock = 0

    # Local event
    def local_event(self):
        self.clock += 1
        print(f"{self.process_name}: Local Event -> Clock = {self.clock}")

    # Send message
    def send_message(self):
        self.clock += 1
        timestamp = self.clock

        print(
            f"{self.process_name}: Send Message -> "
            f"Timestamp = {timestamp}"
        )

        return timestamp

    # Receive message
    def receive_message(self, received_timestamp):
        self.clock = max(self.clock, received_timestamp) + 1

        print(
            f"{self.process_name}: Receive Message "
            f"(Timestamp = {received_timestamp}) -> "
            f"Clock = {self.clock}"
        )


# Create two processes
P1 = LamportClock("P1")
P2 = LamportClock("P2")

# Events in P1
P1.local_event()
timestamp = P1.send_message()

# Message received by P2
P2.receive_message(timestamp)

# More events
P2.local_event()

timestamp = P2.send_message()

# Message received by P1
P1.receive_message(timestamp)