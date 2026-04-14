import pennylane as qml
from pennylane import numpy as np

# Define system parameters
num_qubits = 2  # Simplified model with 2 qubits representing the cytochrome system
omega = 1.0     # Energy gap between states (arbitrary units)
gamma = 0.1     # Dephasing rate (environmental noise)
time_steps = 100
time_max = 10.0

# Time evolution parameters
dt = time_max / time_steps
times = np.linspace(0, time_max, time_steps)

# Initial state: Superposition state to study coherence
initial_state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])  # Bell state

# Define the Hamiltonian of the system
H = omega * qml.PauliZ(0) + omega * qml.PauliZ(1)

# Define the Lindblad operators for dephasing noise
L_dephasing_0 = np.sqrt(gamma) * qml.PauliZ(0)
L_dephasing_1 = np.sqrt(gamma) * qml.PauliZ(1)

# Define the quantum device
dev = qml.device("default.mixed", wires=num_qubits)

@qml.qnode(dev)
def lindblad_evolution(t):
    # Initialize the system in the given state
    qml.QubitStateVector(initial_state, wires=range(num_qubits))
    
    # Apply time evolution under the Hamiltonian
    qml.ApproxTimeEvolution(H, t, 1)
    
    # Apply Lindblad noise (dephasing)
    qml.KrausChannel([L_dephasing_0, L_dephasing_1], wires=0)
    qml.KrausChannel([L_dephasing_0, L_dephasing_1], wires=1)
    
    # Return the density matrix
    return qml.state()

# Simulate the time evolution
density_matrices = []
for t in times:
    rho_t = lindblad_evolution(t)
    density_matrices.append(rho_t)

# Analyze coherence
def l1_norm_coherence(rho):
    """Calculate the l1-norm coherence of a density matrix."""
    coherence = 0
    for i in range(len(rho)):
        for j in range(len(rho)):
            if i != j:
                coherence += np.abs(rho[i, j])
    return coherence

# Compute coherence over time
coherence_values = [l1_norm_coherence(rho) for rho in density_matrices]

# Plot the results
import matplotlib.pyplot as plt

plt.plot(times, coherence_values, label="L1-norm Coherence")
plt.xlabel("Time")
plt.ylabel("Coherence")
plt.title("Quantum Coherence in Cytochrome")
plt.legend()
plt.show()