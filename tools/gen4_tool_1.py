import numpy as np
import qutip as qt

# Define system parameters
num_qubits = 2  # Number of qubits in the system
gamma = 0.1     # Noise rate (dissipation coefficient)
omega = 1.0     # System frequency
t_max = 10.0    # Maximum simulation time
dt = 0.01       # Time step

# Define Pauli matrices
sigma_x = qt.sigmax()
sigma_y = qt.sigmay()
sigma_z = qt.sigmaz()
identity = qt.qeye(2)

# Define the Hamiltonian (time-dependent)
def hamiltonian(t, args):
    omega = args['omega']
    return omega * sigma_x

# Define Lindblad operators (time-dependent noise-assisted computation)
def lindblad_operators(t, args):
    gamma = args['gamma']
    return [np.sqrt(gamma) * sigma_z]

# Define initial state (pure state |0>)
initial_state = qt.basis(2, 0)

# Time-dependent coefficients
args = {'omega': omega, 'gamma': gamma}

# Solve the Lindblad master equation
times = np.arange(0, t_max, dt)
result = qt.mesolve(
    H=hamiltonian, 
    rho0=initial_state, 
    tlist=times, 
    c_ops=lindblad_operators, 
    args=args
)

# Plot the results
qt.plot_expectation_values(result, [sigma_x, sigma_y, sigma_z], title="Noise-Assisted Lindblad Dynamics")

# Save the results to a file
np.savetxt("lindblad_simulation_results.csv", np.column_stack([times, result.expect[0], result.expect[1], result.expect[2]]), delimiter=",", header="time,<sigma_x>,<sigma_y>,<sigma_z>")