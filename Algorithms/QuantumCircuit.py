from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from dotenv import load_dotenv
import pandas as pd 
import os

load_dotenv()
API_KEY = os.getenv("IBMQ_TOKEN")


def dr_no_to_binary(dr_no, bit_size=28):
    return format(int(dr_no), f'0{bit_size}b')

df = pd.read_csv("C:/Users/abbil/Downloads/Crime_Data_from_2020_to_Present.csv", delimiter=',')
df['Binary_DR_NO'] = df['DR_NO'].apply(dr_no_to_binary)

# Function to perform Grover's search with a given DR_NO in decimal
def grovers_search_for_drno(decimal_dr_no, target_bit_size=28):

    target_binary = dr_no_to_binary(decimal_dr_no, bit_size=target_bit_size)
    print(f"Target binary DR_NO to search: {target_binary}")


    oracle_input = [int(bit) for bit in target_binary]
    n_qubits = len(target_binary)
    

    circuit = QuantumCircuit(n_qubits)

    # Oracle function to flag the solution
    def oracle(oracle_input):
        oracle_circuit = QuantumCircuit(len(oracle_input), len(oracle_input))  # Classical bits for measurement

        # Apply X gates on the qubits where the oracle_input is 1
        for qubit in range(len(oracle_input)):
            if oracle_input[qubit] == 1:
                oracle_circuit.x(qubit)

        # Apply H, multi-controlled Toffoli, and H again (oracle behavior)
        oracle_circuit.h(len(oracle_input) - 1)  # Apply Hadamard gate on the last qubit
        oracle_circuit.mcx(list(range(len(oracle_input) - 1)), len(oracle_input) - 1)  # Apply multi-controlled Toffoli
        oracle_circuit.h(len(oracle_input) - 1)  # Apply Hadamard gate on the last qubit

        # Undo the X gates applied earlier
        for qubit in range(len(oracle_input)):
            if oracle_input[qubit] == 1:
                oracle_circuit.x(qubit)

        return oracle_circuit


    oracle_circuit = oracle(oracle_input)  # oracle circuit

    # Add measurement after oracle
    oracle_circuit.measure(range(len(target_binary)), range(len(target_binary)))  # Measure all qubits into classical bits


    simulator = AerSimulator()

    # Compile the circuit
    compiled_circuit = transpile(oracle_circuit, simulator)

    # Run the simulation
    result = simulator.run(compiled_circuit).result()

    # Get the counts (measurements)
    counts = result.get_counts()

    # Output the results
    print("[+] Counts:", counts)
    print("[+] Circuit diagram")
    print(compiled_circuit.draw())

    # Extract the most likely DR_NO from the result
    result_drno = list(counts.keys())[0]
    print(f"Most likely DR_NO found: {result_drno}")

    # Find the matching row in the dataset (check for binary match)
    matching_row = df[df['Binary_DR_NO'] == result_drno]
    print("Matching row from the dataset:")
    print(matching_row)


# Example: Search for a given decimal DR_NO
decimal_dr_no = 250504051  # Replace this with the decimal DR_NO you'd like to search for
grovers_search_for_drno(decimal_dr_no)