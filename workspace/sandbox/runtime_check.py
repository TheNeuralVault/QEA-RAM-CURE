import numpy as np

# Define the number of states
num_states = 4  # Example: triplet and singlet states

# Define the energy levels of the states
energy_levels = np.array([0.0, 1.5, 3.0, 4.5])  # Example energies in eV

# Define the interaction matrix (Hamiltonian)
interaction_matrix = np.zeros((num_states, num_states))

# Add interactions between triplet and singlet states
interaction_matrix[0, 1] = -1.0  # Example interaction strength
interaction_matrix[1, 0] = -1.0  # Symmetric interaction

# Print the Hamiltonian matrix
print("Radical Pair Hamiltonian:")
print(interaction_matrix)

# Function to calculate the energy of a given state
def calculate_energy(state_index):
    return energy_levels[state_index]

# Example: Calculate the energy of the singlet state (state index 1)
singlet_energy = calculate_energy(1)
print(f"Energy of the singlet state: {singlet_energy} eV")