import numpy as np
from qutip import *

# Define system parameters
num_sites = 7  # Number of sites in the FMO complex
temperature = 300  # Temperature in Kelvin
k_B = 1.380649e-23  # Boltzmann constant (J/K)
hbar = 1.0545718e-34  # Reduced Planck's constant (J·s)
gamma_dephasing = 1e-3  # Dephasing rate (arbitrary units)
gamma_dissipation = 1e-4  # Dissipation rate (arbitrary units)

# Define the system Hamiltonian (FMO complex model)
# Example Hamiltonian (arbitrary units)
H = Qobj(np.array([
    [200, -87.7, 5.5, -5.9, 6.7, -13.7, -9.9],
    [-87.7, 320, 30.8, 8.2, 0.7, 11.8, 4.3],
    [5.5, 30.8, 0, -53.5, -2.2, -9.6, 6.0],
    [-5.9, 8.2, -53.5, 110, -70.7, -17.0, -63.3],
    [6.7, 0.7, -2.2, -70.7, 270, 81.1, -1.3],
    [-13.7, 11.8, -9.6, -17.0, 81.1, 420, 39.7],
    [-9.9, 4.3, 6.0, -63.3, -1.3, 39.7, 230]
]), dims=[[num_sites], [num_sites]])

# Define the initial state (excitation at site 1)
psi0 = basis(num_sites, 0) * basis(num_sites, 0).dag()

# Define collapse operators for decoherence
c_ops = []

# Dephasing (site-specific)
for i in range(num_sites):
    c_ops.append(np.sqrt(gamma_dephasing) * basis(num_sites, i) * basis(num_sites, i).dag())

# Dissipation (site-to-site energy transfer)
for i in range(num_sites):
    for j in range(num_sites):
        if i != j:
            c_ops.append(np.sqrt(gamma_dissipation) * basis(num_sites, j) * basis(num_sites, i).dag())

# Solve the Lindblad Master Equation
tlist = np.linspace(0, 5, 500)  # Time points for simulation
result = mesolve(H, psi0, tlist, c_ops, [])

# Extract populations for each site
populations = np.array([result.expect[basis(num_sites, i) * basis(num_sites, i).dag()] for i in range(num_sites)])

# Plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
for i in range(num_sites):
    plt.plot(tlist, populations[i], label=f"Site {i+1}")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Quantum Biology Decoherence Model: Site Populations")
plt.legend()
plt.show()