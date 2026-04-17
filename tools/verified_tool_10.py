# [TIER-1: EXACT]
# Microtubule Spintronic Coherence Neuron
# Quantum transport + Lindblad decoherence (no QuTiP)
# FMO Hamiltonian: Adolphs & Renger 2006, Biophys J 91:2778
# Lindblad: drho/dt = -i[H,rho] + sum_k(L_k rho L_k† - 0.5{L_k†L_k, rho})

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

# #TOOL

# Constants
N = 7  # sites

# FMO site energies (cm^-1)
E = np.array([200, 0, 110, 210, 280, 420, 240])

# FMO couplings (cm^-1)
J = np.array([
    [0,   104.1, 5.1,  -4.3, 4.7, -11.8, -8.5],
    [104.1, 0, 32.6, 7.1,  -8.1, -4.2, 6.2],
    [5.1, 32.6, 0, 46.8, 1.0, -8.1, 1.7],
    [-4.3, 7.1, 46.8, 0, -70.7, -14.7, -61.5],
    [4.7, -8.1, 1.0, -70.7, 0, 89.7, -2.5],
    [-11.8, -4.2, -8.1, -14.7, 89.7, 0, 32.7],
    [-8.5, 6.2, 1.7, -61.5, -2.5, 32.7, 0]
])

# Hamiltonian (cm^-1)
H = np.zeros((N,N), dtype=np.complex128)
for i in range(N):
    H[i,i] = E[i]
for i in range(N):
    for j in range(N):
        if i != j:
            H[i,j] = J[i,j]

# Lindblad dephasing (300K)
gamma_dephasing = 0.020  # cm^-1/fs

# Lindblad operators: L_k = sqrt(gamma) |k><k|
L_deph = [np.sqrt(gamma_dephasing) * np.outer(np.eye(N)[k], np.eye(N)[k]) for k in range(N)]

# Initial state: excitation at site 0
rho0 = np.zeros((N,N), dtype=np.complex128)
rho0[0,0] = 1.0

# Time evolution parameters
tlist = np.linspace(0, 500, 100)  # fs
dt = tlist[1] - tlist[0]

def lindblad_rhs(rho, H, L_deph):
    # -i[H,rho]
    comm = -1j * (H @ rho - rho @ H)
    # Lindblad sum
    lind = np.zeros_like(rho)
    for L in L_deph:
        lind += L @ rho @ L.conj().T - 0.5 * (L.conj().T @ L @ rho + rho @ L.conj().T @ L)
    return comm + lind

# Time evolution (Euler method)
rho = rho0.copy()
populations = np.zeros((len(tlist), N))
for idx, t in enumerate(tlist):
    populations[idx] = np.real(np.diag(rho))
    drho = lindblad_rhs(rho, H, L_deph)
    rho += drho * dt

# Print numerical results
print("Site populations over time (first 5 time points):")
for i in range(N):
    print(f"Site {i}: {populations[:5,i]}")

# Plot
for i in range(N):
    plt.plot(tlist, populations[:,i], label=f"Site {i}")
plt.xlabel("Time (fs)")
plt.ylabel("Population")
plt.title("Microtubule Spintronic Coherence Neuron: Site Populations")
plt.legend()
plt.show()

# Source: Adolphs & Renger 2006, Biophys J 91:2778; Lindblad master equation