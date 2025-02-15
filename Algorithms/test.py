from dotenv import load_dotenv
import os
from qiskit_aer import Aer, AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram


load_dotenv()
API_KEY = os.getenv("IBMQ_TOKEN")


circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 classical bits

# search for |10>

circuit.h([0, 1])
circuit.barrier()

# Apply Oracle: Flip phase of |10>
circuit.x(0)  # Flip qubit 0 to target |10>
circuit.h(1)  # Apply Hadamard to qubit 1
circuit.cx(0, 1)  # Controlled-X for phase flip
circuit.h(1)
circuit.x(0)
circuit.barrier()

# Apply diffusion operator
circuit.h([0, 1])
circuit.x([0, 1])
circuit.h(1)
circuit.cx(0, 1)
circuit.h(1)
circuit.x([0, 1])
circuit.h([0, 1])
circuit.barrier()

circuit.measure([0, 1], [0, 1])

# Simulate and plot results
simulator = AerSimulator()
compiled_circuit = transpile(circuit, simulator)
print("[+] compiled circuit")
print(compiled_circuit.draw())
print("[+] compiled circuit transpile")
result = simulator.run(circuit).result()
print("[+] simulator run")
counts = result.get_counts()
print("[+] result get counts: ", counts)
plot_histogram(counts)
print("[+] plot histogram")
circuit.draw('mpl')