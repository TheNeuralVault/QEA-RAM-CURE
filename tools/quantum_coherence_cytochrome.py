#TOOL
import numpy as np

def quantum_tunneling_probability(m, V, E, t):
    """
    Calculate the quantum tunneling probability using the WKB approximation.
    
    Parameters:
    m (float): Mass of the particle (kg)
    V (float): Potential energy barrier (J)
    E (float): Energy of the tunneling particle (J)
    t (float): Time (s)
    
    Returns:
    float: Tunneling probability P(t)
    """
    hbar = 1.05e-34  # Reduced Planck constant (J·s)
    P_t = np.exp(-2 * np.pi * m * V / E * t)
    return P_t

def tunneling_time(m, E, nu):
    """
    Calculate the time for a single tunneling event.
    
    Parameters:
    m (float): Mass of the particle (kg)
    E (float): Energy of the tunneling particle (J)
    nu (float): Tunneling frequency (Hz)
    
    Returns:
    float: Tunneling time (s)
    """
    hbar = 1.05e-34  # Reduced Planck constant (J·s)
    t = (hbar * E / (m * nu)) * np.log(2)
    return t

# Constants
m_proton = 1.67e-27  # Mass of a proton (kg)
V_barrier = 1e-20    # Example potential energy barrier (J)
E_particle = 8e-21   # Energy of the tunneling particle (J)
nu_frequency = 1e13  # Tunneling frequency (Hz)

# Calculate tunneling time
t_tunneling = tunneling_time(m_proton, E_particle, nu_frequency)
print(f"Tunneling Time: {t_tunneling:.2e} seconds")

# Calculate tunneling probability at a given time
time = 1e-12  # Example time (s)
P_tunneling = quantum_tunneling_probability(m_proton, V_barrier, E_particle, time)
print(f"Tunneling Probability at t={time}s: {P_tunneling:.2e}")