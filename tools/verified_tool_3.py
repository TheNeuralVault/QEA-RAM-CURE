# [TIER-1: EXACT]
# #TOOL
# FMO coherence simulation at physiological temperature (300K)
# Hamiltonian: Adolphs & Renger 2006, Biophys J 91:2778
# Lindblad master equation

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

# Constants
hbar = 0.6582119514  # [cm^-1 fs] Planck's constant (cm^-1 * fs)
gamma_dephasing = 0.020  # [cm^-1/fs] at 300K

# FMO Hamiltonian (Adolphs & Renger 2006)
# Energies (cm^-1)
E = np.array([200, 0, 110, 210, 280, 420, 240])
# Couplings (cm^-1)
H = np.array([
    [E[0], -87.7,   5.5,  -5.4,   7.8, -1.5, -9.3],
    [-87.7, E[1], 30.8,   8.2,  -8.8,  0.7,  8.8],
    [5.5,  30.8,  E[2], -53.5,   2.2, -70.7, -6.4],
    [-5.4, 8.2,  -53.5,  E[3], -70.7, -14.7, -61.5],
    [7.8, -8.8,   2.2,  -70.7,  E[4], 89.7, -2.5],
    [-1.5, 0.7,  -70.7, -14.7,  89.7, E[5], 32.7],
    [-9.3, 8.8,  -6.4,  -61.5,  -2.5, 32.7, E[6]]
])

# Initial state: excitation at site 1
rho0 = np.zeros((7,7), dtype=complex)
rho0[0,0] = 1.0

# Lindblad dephasing operators (one per site)
L_deph = []
for i in range(7):
    op = np.zeros((7,7), dtype=complex)
    op[i,i] = 1.0
    L_deph.append(op)

def lindblad_rhs(rho, H, L_deph, gamma):
    # -i[H, rho]
    comm = -1j * (np.dot(H, rho) - np.dot(rho, H))
    # Dephasing Lindblad terms
    lind = np.zeros_like(rho)
    for L in L_deph:
        lind += gamma * (np.dot(L, np.dot(rho, L.conj().T)) - 0.5 * (np.dot(L.conj().T @ L, rho) + np.dot(rho, L.conj().T @ L)))
    return (comm + lind) / hbar

# Time evolution parameters
t_max = 500  # fs
dt = 1.0     # fs
steps = int(t_max/dt)
times = np.linspace(0, t_max, steps)
rho = rho0.copy()
coherence_12 = []

for t in times:
    # Store coherence between site 1 and 2 (off-diagonal element)
    coherence_12.append(np.abs(rho[0,1]))
    # RK4 integration
    k1 = lindblad_rhs(rho, H, L_deph, gamma_dephasing)
    k2 = lindblad_rhs(rho + 0.5*dt*k1, H, L_deph, gamma_dephasing)
    k3 = lindblad_rhs(rho + 0.5*dt*k2, H, L_deph, gamma_dephasing)
    k4 = lindblad_rhs(rho + dt*k3, H, L_deph, gamma_dephasing)
    rho += (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

# Print numerical results
print("Coherence |rho_12| at t=0 fs:", coherence_12[0])
print("Coherence |rho_12| at t=100 fs:", coherence_12[int(100/dt)])
print("Coherence |rho_12| at t=500 fs:", coherence_12[-1])

# Plot coherence decay
plt.plot(times, coherence_12)
plt.xlabel("Time (fs)")
plt.ylabel("Coherence |rho_12|")
plt.title("FMO Coherence at 300K (Physiological Temperature)")
plt.show()

# [TIER-1: EXACT]
# Source: Adolphs & Renger 2006, Biophys J 91:2778; Lindblad master equation standard form