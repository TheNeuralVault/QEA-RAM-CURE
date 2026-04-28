from qiskit import QuantumCircuit, Aer, execute

# Create a quantum circuit with one qubit and one classical bit
qc = QuantumCircuit(1, 1)

# Apply a Hadamard gate to put the qubit into superposition
qc.h(0)

# Measure the qubit
qc.measure(0, 0)

# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')

# Execute the circuit on the qasm simulator
job = execute(qc, simulator, shots=1024)

# Grab results from the job
result = job.result()

# Get counts of each outcome
counts = result.get_counts(qc)
print(counts)