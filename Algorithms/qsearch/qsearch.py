from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit_aer import AerSimulator


def encode_crime(area, crime):
    encoding = {
        "Downtown": "00", "Uptown": "01", "Suburb": "10",
        "Burglary": "00", "Assault": "01", "Robbery": "10", "Fraud": "11"
    }
    return encoding.get(area, "XX") + encoding.get(crime, "XX")


def grover_oracle(qc, target):
    n = len(target)
    for i in range(n):
        if target[i] == '0':
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # Multi-controlled NOT
    qc.h(n-1)
    for i in range(n):
        if target[i] == '0':
            qc.x(i)


def grover_diffusion(qc, n):
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))


# Define Grover's Search Circuit with multiple iterations
def grover_search(target_binary, iterations=3):
    n = len(target_binary)
    qc = QuantumCircuit(n+1, n)

    # Initialize in superposition
    qc.h(range(n))
    qc.x(n)
    qc.h(n)

    # Apply Grover iterations
    for _ in range(iterations):
        grover_oracle(qc, target_binary)
        grover_diffusion(qc, n)

    # Measure result
    qc.measure(range(n), range(n))

    return qc


# Encode target crime
target_binary = encode_crime("Downtown", "Burglary")

# Run Grover's search
qc = grover_search(target_binary, iterations=3)

# Simulate
simulator = AerSimulator()
t_qc = transpile(qc, simulator)
result = simulator.run(t_qc).result()
counts = result.get_counts()

# Get most probable match
found_binary = max(counts, key=counts.get)
print("Quantum Search Found (Binary):", found_binary)

# Convert binary back to area and crime type
area_decode_table = {"00": "Downtown", "01": "Uptown", "10": "Suburb"}
crime_decode_table = {"00": "Burglary", "01": "Assault", "10": "Robbery", "11": "Fraud"}
found_area = area_decode_table.get(found_binary[:2], "Unknown")
found_crime = crime_decode_table.get(found_binary[2:], "Unknown")

print("Quantum Search Matched:", found_area, "-", found_crime)
