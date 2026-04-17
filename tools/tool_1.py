import numpy as np
from scipy.linalg import expm

# FeMoCo quantum tunneling simulation using Lindblad master equation
# Noise-assisted computation (Lindblad implementation)

# System parameters (example: 2-level system for tunneling)
omega = 1.0         # Energy splitting (arbitrary units)
gamma = 0.05        # Lindblad decoherence rate (noise-assisted)
dt = 0.01           # Time step
steps = 1000        # Number of steps

# Pauli matrices
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
identity = np.eye(2, dtype=complex)

# Hamiltonian: tunneling term
H = 0.5 * omega * sigma_x

# Lindblad operator: decoherence in energy basis (FeMoCo tunneling)
L = np.sqrt(gamma) * sigma_z

def lindblad_rhs(rho, H, L):
    """Compute Lindblad RHS for density matrix evolution."""
    # Unitary part
    unitary = -1j * (H @ rho - rho @ H)
    # Dissipator part
    dissipator = L @ rho @ L.conj().T - 0.5 * (L.conj().T @ L @ rho + rho @ L.conj().T @ L)
    return unitary + dissipator

# Initial state: FeMoCo electron in superposition (tunneling)
rho = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)

# Time evolution
populations = []
coherences = []

for _ in range(steps):
    # RK4 integration for Lindblad equation
    k1 = lindblad_rhs(rho, H, L)
    k2 = lindblad_rhs(rho + 0.5*dt*k1, H, L)
    k3 = lindblad_rhs(rho + 0.5*dt*k2, H, L)
    k4 = lindblad_rhs(rho + dt*k3, H, L)
    rho += (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
    # Store populations and coherences
    populations.append(np.real(np.diag(rho)))
    coherences.append(np.real(rho[0,1]))

# Output: populations and coherences over time
import matplotlib.pyplot as plt

populations = np.array(populations)
coherences = np.array(coherences)

plt.figure(figsize=(8,4))
plt.plot(populations[:,0], label='State |0> population')
plt.plot(populations[:,1], label='State |1> population')
plt.plot(coherences, label='Coherence Re[rho_01]')
plt.xlabel('Time step')
plt.ylabel('Population / Coherence')
plt.title('FeMoCo Quantum Tunneling (Noise-Assisted Lindblad Simulation)')
plt.legend()
plt.tight_layout()
plt.show()