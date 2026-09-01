class VectorClock:
    def __init__(self, process_id, total_processes):
        self.process_id = process_id
        self.total_processes = total_processes

        # Initialize vector with zeros
        self.vector = [0] * total_processes

    # Local event
    def local_event(self):
        self.vector[self.process_id] += 1

        print(
            f"P{self.process_id + 1}: "
            f"Local Event -> {self.vector}"
        )

    # Send message
    def send_message(self):
        self.vector[self.process_id] += 1

        message_vector = self.vector.copy()

        print(
            f"P{self.process_id + 1}: "
            f"Send Message -> {message_vector}"
        )

        return message_vector

    # Receive message
    def receive_message(self, received_vector):
        # Merge received vector with current vector
        for i in range(self.total_processes):
            self.vector[i] = max(
                self.vector[i],
                received_vector[i]
            )

        # Increment own component
        self.vector[self.process_id] += 1

        print(
            f"P{self.process_id + 1}: "
            f"Receive Message {received_vector} "
            f"-> {self.vector}"
        )


# Create 3 processes
P1 = VectorClock(0, 3)
P2 = VectorClock(1, 3)
P3 = VectorClock(2, 3)


# P1 performs a local event
P1.local_event()

# P1 sends message to P2
message1 = P1.send_message()

# P2 receives message
P2.receive_message(message1)

# P2 performs a local event
P2.local_event()

# P2 sends message to P3
message2 = P2.send_message()

# P3 receives message
P3.receive_message(message2)

# P3 performs a local event
P3.local_event()