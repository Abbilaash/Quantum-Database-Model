import pandas as pd
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import time

# -----------------------
# Load Dataset
# -----------------------
df = pd.read_csv('dataset.csv')

# Get the unique Patient IDs
patient_ids = df['PatientID'].unique()
num_qubits = int(np.ceil(np.log2(len(patient_ids))))  # Determine qubits needed

# Binary encoding for Patient IDs
binary_map = {patient_ids[i]: format(i, f'0{num_qubits}b') for i in range(len(patient_ids))}

# -----------------------
# Define Quantum Functions
# -----------------------

def oracle(qc, fever_binaries):
    """Marks the states where 'Problem' is 'Fever'."""
    for bin_value in fever_binaries:
        for i, bit in enumerate(reversed(bin_value)):
            if bit == '0':
                qc.x(i)

        qc.h(num_qubits - 1)
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)  # Multi-controlled Z gate
        qc.h(num_qubits - 1)

        for i, bit in enumerate(reversed(bin_value)):
            if bit == '0':
                qc.x(i)

def diffusion_operator(qc):
    """Applies Grover's diffusion operator to amplify marked states."""
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))

# -----------------------
# Prepare the Quantum Circuit
# -----------------------

qc = QuantumCircuit(num_qubits, num_qubits)
qc.h(range(num_qubits))  # Apply Hadamard for superposition

# Identify Patients with Fever
fever_patients = df[df['Problem'] == 'Fever']['PatientID'].tolist()
fever_binaries = [binary_map[pid] for pid in fever_patients]

# Optimal number of iterations for Grover’s search
N = 2**num_qubits
optimal_iterations = int(np.floor((np.pi / 4) * np.sqrt(N))) + 1
print(f"Optimal Iterations: {optimal_iterations}")

start_time = time.time()

for _ in range(optimal_iterations):
    oracle(qc, fever_binaries)
    diffusion_operator(qc)

end_time = time.time()
print(f"Time taken for quantum search: {end_time - start_time:.5f} seconds")

# Measure the qubits
qc.measure(range(num_qubits), range(num_qubits))

# -----------------------
# Run Simulation
# -----------------------

simulator = AerSimulator()
compiled_qc = transpile(qc, simulator)
result = simulator.run(compiled_qc).result()
counts = result.get_counts()

# -----------------------
# Retrieve and Decode Results
# -----------------------

print("\nMeasurement Results:")
print(counts)
plot_histogram(counts).show()

# Get the most probable results (top matching patient IDs)
most_probable_binaries = sorted(counts, key=counts.get, reverse=True)[:len(fever_patients)]
found_patient_ids = [pid for bin_val in most_probable_binaries for pid, b in binary_map.items() if b == bin_val]

print("\n[+] Patients with Fever (Identified via Quantum Search):")
for pid in found_patient_ids:
    print(df[df['PatientID'] == pid])

