import numpy as np
import qutip as qt

# Define system parameters
num_qubits = 2  # Number of qubits in the system
gamma = 0.1     # Noise strength (decay rate)
omega = 1.0     # System frequency
time_steps = 100  # Number of time steps
t_max = 10.0      # Maximum simulation time
dt = t_max / time_steps  # Time step size

# Define time-dependent coefficients for Lindblad operators
def gamma_t(t):
    """Time-dependent decay rate."""
    return gamma * (1 + 0.1 * np.sin(2 * np.pi * t / t_max))

def omega_t(t):
    """Time-dependent system frequency."""
    return omega * (1 + 0.05 * np.cos(2 * np.pi * t / t_max))

# Define system Hamiltonian
def hamiltonian(t):
    """Time-dependent Hamiltonian."""
    return omega_t(t) * qt.sigmaz()

# Define Lindblad operators
def lindblad_operators(t):
    """Time-dependent Lindblad operators."""
    decay_op = np.sqrt(gamma_t(t)) * qt.sigmax()  # Noise-assisted decay
    return [decay_op]

# Initial state of the system
initial_state = qt.basis(2, 0) * qt.basis(2, 0).dag()  # |0><0| state

# Time evolution using Lindblad master equation
times = np.linspace(0, t_max, time_steps)
result = qt.mesolve(
    H=hamiltonian,  # Time-dependent Hamiltonian
    rho0=initial_state,  # Initial density matrix
    tlist=times,  # Time points for simulation
    c_ops=lindblad_operators,  # Time-dependent collapse operators
    options=qt.Options(store_states=True)  # Store states for analysis
)

# Plot results
import matplotlib.pyplot as plt

# Extract populations of |0> and |1>
populations = [qt.expect(qt.basis(2, i) * qt.basis(2, i).dag(), state) for i in range(2) for state in result.states]

plt.figure(figsize=(8, 6))
plt.plot(times, populations[0], label="Population |0>")
plt.plot(times, populations[1], label="Population |1>")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Noise-Assisted Lindblad Simulation")
plt.legend()
plt.grid()
plt.show()