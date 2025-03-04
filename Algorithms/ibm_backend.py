import pandas as pd
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session
import numpy as np


# Load IBM Quantum API Key (Directly in the Code)
QiskitRuntimeService.save_account(channel='ibm_quantum',token='',overwrite=True)
service = QiskitRuntimeService()

# Load dataset
df = pd.read_csv("dataset.csv")  # Ensure the file is in the correct directory

# Encode the "Problem" column in binary
unique_problems = list(df['Problem'].unique())
problem_map = {problem: format(i, '05b') for i, problem in enumerate(unique_problems)}

# Get binary representation for "Fever"
target_problem = "Fever"
target_binary = problem_map[target_problem]

# Number of qubits needed
num_qubits = len(target_binary)

# Create Quantum Circuit
qc = QuantumCircuit(num_qubits, num_qubits)
qc.h(range(num_qubits))  # Hadamard gate

# Oracle function
def oracle(qc, target_binary):
    for i, bit in enumerate(reversed(target_binary)):
        if bit == '0':
            qc.x(i)
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    for i, bit in enumerate(reversed(target_binary)):
        if bit == '0':
            qc.x(i)

# Diffusion operator
def diffusion_operator(qc):
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))

# Run Grover's Algorithm (√N iterations)
iterations = int(np.pi / 4 * np.sqrt(2**num_qubits))
for _ in range(iterations):
    oracle(qc, target_binary)
    diffusion_operator(qc)

# Measure the qubits
qc.measure(range(num_qubits), range(num_qubits))

backend = service.least_busy(operational=True, simulator=False)
with Session(backend=backend) as session:
    sampler = SamplerV2(mode=session)
    job = sampler.run([qc])
    pub_result = job.result()[0]
    print(f"Sampler job ID: {job.job_id()}")
    print(f"Counts: {pub_result.data.cr.get_counts()}")
