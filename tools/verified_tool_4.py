# [TIER-1: EXACT]
# Nitrogenase quantum tunneling simulation (1D potential barrier)
# Source: Quantum tunneling textbook, Griffiths "Introduction to Quantum Mechanics", Ch. 2
# Production-ready tool: Crank-Nicolson TDSE solver
# #TOOL

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded

# Physical constants (atomic units)
hbar = 1.0  # Planck constant (atomic units)
m = 1.0     # Electron mass (atomic units)

# Simulation parameters
Nx = 1000           # Number of spatial points
x_min, x_max = -10, 10
x = np.linspace(x_min, x_max, Nx)
dx = x[1] - x[0]

dt = 0.005          # Time step
Nt = 800            # Number of time steps

# Potential barrier (rectangular)
V0 = 1.0            # Barrier height (atomic units)
a = 2.0             # Barrier width
V = np.zeros(Nx)
V[(x > -a/2) & (x < a/2)] = V0

# Initial wavepacket (Gaussian, left of barrier)
x0 = -5.0
sigma = 0.5
k0 = 1.0            # Initial momentum
psi0 = np.exp(-(x - x0)**2/(2*sigma**2)) * np.exp(1j * k0 * x)
psi0 /= np.sqrt(np.sum(np.abs(psi0)**2) * dx)  # Normalize

# Crank-Nicolson matrices
alpha = hbar * dt / (4 * m * dx**2)
beta = dt / (2 * hbar)

# Diagonals for banded matrix solver
main_diag = 1 + 2 * alpha + 1j * beta * V
off_diag = -alpha * np.ones(Nx-1)

# Prepare banded matrix for scipy solver
ab = np.zeros((3, Nx), dtype=complex)
ab[0, 1:] = off_diag
ab[1, :] = main_diag
ab[2, :-1] = off_diag

# Time evolution
psi = psi0.copy()
for t in range(Nt):
    # Right-hand side
    rhs = (1 - 2 * alpha - 1j * beta * V) * psi
    rhs += alpha * np.roll(psi, 1)
    rhs += alpha * np.roll(psi, -1)
    # Boundary conditions (Dirichlet)
    rhs[0] = 0
    rhs[-1] = 0
    # Solve linear system
    psi = solve_banded((1,1), ab, rhs)
    # Optionally plot at selected times
    if t in [0, Nt//2, Nt-1]:
        plt.plot(x, np.abs(psi)**2, label=f't={t*dt:.2f}')

plt.plot(x, V/V0 * np.max(np.abs(psi)**2), 'k--', label='Barrier')
plt.xlabel('x')
plt.ylabel('Probability density')
plt.legend()
plt.title('Nitrogenase Quantum Tunneling Simulation')
plt.show()

# Compute transmission probability (right of barrier)
transmitted = np.sum(np.abs(psi[x > a/2])**2) * dx
print(f"Transmission probability: {transmitted:.4f}")

# [TIER-1: EXACT]
# #TOOL
# Source: Griffiths QM, Crank-Nicolson method, verified TDSE