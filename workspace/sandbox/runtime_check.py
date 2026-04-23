import numpy as np
from qutip import Qobj, tensor, identity, destroy, create, mesolve

# Define the system Hamiltonian and interaction terms
H = Qobj([[1, 0], [0, -1]])  # Example Hamiltonian for a spin-1/2 system
L1 = Qobj([[0, 1], [1, 0]])  # Interaction term with environment 1
L2 = Qobj([[0, 1], [1, 0]])  # Interaction term with environment 2

# Define the initial state of the system
psi0 = tensor(identity(2), create(2))  # Initial state |0⟩ ⊗ |↑⟩

# Define the Lindblad operators
L = [L1, L2]

# Set up the time grid
tlist = np.linspace(0, 10, 100)

# Solve the master equation using mesolve
result = mesolve(H, psi0, tlist, [], L)

# Plot the results
import matplotlib.pyplot as plt

plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('Expectation value of system')
plt.title('Lindblad Master Equation Simulation')
plt.show()