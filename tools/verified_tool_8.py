# [TIER-1: EXACT] #TOOL
# MIT critical quantum chaos coherence simulation
# Loschmidt echo + quantum coherence
# Source: Loschmidt echo: arXiv:quant-ph/0110018, Quantum Chaos & Quantum Computers

import numpy as np
import scipy.linalg

# Hamiltonian construction: 2-qubit XX+YY+Z model
def hamiltonian(J, h):
    # H = J * (X1 X2 + Y1 Y2) + h * (Z1 + Z2)
    X = np.array([[0,1],[1,0]], dtype=complex)
    Y = np.array([[0,-1j],[1j,0]], dtype=complex)
    Z = np.array([[1,0],[0,-1]], dtype=complex)
    I = np.eye(2, dtype=complex)
    XX = np.kron(X,X)
    YY = np.kron(Y,Y)
    Z1 = np.kron(Z,I)
    Z2 = np.kron(I,Z)
    H = J*(XX+YY) + h*(Z1+Z2)
    return H

# Initial state |00>
psi0 = np.array([1,0,0,0], dtype=complex)

# Parameters: critical boundary (chaos transition)
J = 1.0    # coupling
h0 = 0.5   # integrable regime
h1 = 1.5   # chaotic regime (perturbed)

H0 = hamiltonian(J, h0)
H1 = hamiltonian(J, h1)

# Time evolution
def evolve(H, psi, t):
    U = scipy.linalg.expm(-1j * H * t)
    return U @ psi

t = 1.0  # time

# Loschmidt echo calculation
psi_t = evolve(H0, psi0, t)
psi_t_perturbed = evolve(H1, psi_t, -t)
L_echo = np.abs(np.vdot(psi0, psi_t_perturbed))**2

print("Loschmidt Echo at t=1.0:", L_echo)

# Quantum coherence (l1-norm)
def l1_coherence(rho):
    # l1-norm: sum of absolute values of off-diagonal elements
    return np.sum(np.abs(rho)) - np.sum(np.abs(np.diag(rho)))

rho = np.outer(psi_t_perturbed, np.conj(psi_t_perturbed))
coherence = l1_coherence(rho)
print("Quantum Coherence (l1-norm) at t=1.0:", coherence)

# [TIER-1: EXACT]
#TOOL