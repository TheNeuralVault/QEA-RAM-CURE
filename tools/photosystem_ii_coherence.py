#TOOL
import numpy as np
import matplotlib.pyplot as plt

# Constants
hbar = 1.0545718e-34  # Reduced Planck's constant (J·s)
omega = 1e12          # Oscillation frequency (Hz)
time_steps = 1000     # Number of time steps
dt = 1e-15            # Time step size (s)

# Initial quantum state (superposition)
psi_0 = np.array([1/np.sqrt(2), 1j/np.sqrt(2)])  # |ψ(0)> = (|0> + i|1>)/√2

# Hamiltonian for a two-level system
H = np.array([[0, hbar * omega],
              [hbar * omega, 0]])

# Time evolution operator
def time_evolution_operator(H, dt):
    return np.linalg.expm(-1j * H * dt / hbar)

# Simulate quantum coherence
psi_t = psi_0
coherence = []
time = []

for t in range(time_steps):
    U = time_evolution_operator(H, dt)
    psi_t = np.dot(U, psi_t)
    coherence.append(np.abs(np.vdot(psi_t, psi_0))**2)  # Coherence measure
    time.append(t * dt)

# Plot results
plt.plot(time, coherence)
plt.title("Quantum Coherence in Photosynthesis")
plt.xlabel("Time (s)")
plt.ylabel("Coherence")
plt.grid()
plt.show()