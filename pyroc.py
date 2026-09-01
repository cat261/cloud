import Pyro4
uri = input("Enter the Server URI: ")

# Connect to remote object
calculator = Pyro4.Proxy(uri)

# Get input
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

# Invoke remote methods
addition = calculator.add_numbers(a, b)
multiplication = calculator.multiply(a, b)

# Display results
print("\nResults:")
print("Addition:", addition)
print("Multiplication:", multiplication)