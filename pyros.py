import Pyro4
@Pyro4.expose
class Calculator:
    def add_numbers(self, a, b):
        return a + b
    def multiply(self, a, b):
        return a * b

# Create Pyro4 daemon
daemon = Pyro4.Daemon()

# Register Calculator object
uri = daemon.register(Calculator())

print("Calculator Server Started")
print("Server URI:", uri)
print("Waiting for client requests...")

# Start server
daemon.requestLoop()