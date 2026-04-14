#TOOL: Proton Tunneling Time Calculation
import math

def calculate_tunneling_time(h_bar, energy, mass, frequency):
    """
    Calculate the time for a proton tunneling event using the given parameters.
    
    Parameters:
    h_bar (float): Reduced Planck constant (J·s)
    energy (float): Energy of the tunneling particle (J)
    mass (float): Mass of the proton (kg)
    frequency (float): Tunneling frequency (Hz)
    
    Returns:
    float: Tunneling time in seconds
    """
    ln_2 = math.log(2)
    tunneling_time = (h_bar * energy / (mass * frequency)) * ln_2
    return tunneling_time

# Constants
h_bar = 1.05e-34  # Reduced Planck constant (J·s)
energy = 8e-21    # Energy of the tunneling particle (J)
mass = 1.67e-27   # Mass of a proton (kg)
frequency = 1e13  # Tunneling frequency (Hz)

# Calculate tunneling time
tunneling_time = calculate_tunneling_time(h_bar, energy, mass, frequency)
print(f"Tunneling time: {tunneling_time:.2e} seconds")