# Import necessary libraries
from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Define system parameters
omega = 2 * np.pi * 1.0  # Qubit frequency
gamma = 0.1              # Decoherence rate
tlist = np.linspace(0, 10, 200)  # Time evolution

# Define Pauli matrices
sx = sigmax()
sy = sigmay()
sz = sigmaz()

# Define the Hamiltonian for the qubit
H = 0.5 * omega * sz

# Initial state of the qubit (superposition state)
psi0 = (basis(2, 0) + basis(2, 1)).unit()

# Collapse operators for decoherence
c_ops = [np.sqrt(gamma) * sz]

# Solve the master equation
result = mesolve(H, psi0, tlist, c_ops, [sx, sy, sz])

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(tlist, result.expect[0], label=r'$\langle \sigma_x \rangle$')
plt.plot(tlist, result.expect[1], label=r'$\langle \sigma_y \rangle$')
plt.plot(tlist, result.expect[2], label=r'$\langle \sigma_z \rangle$')
plt.xlabel('Time')
plt.ylabel('Expectation values')
plt.legend()
plt.title('Quantum Coherence and Decoherence in a Qubit')
plt.grid()
plt.show()