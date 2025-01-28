import numpy as np
from scipy.integrate import quad

def voltage_to_temperature(voltage):
    resistance = voltage + 100 # 1 mV corresponds to 1 Ohm resistance in the configured PT-100, so the voltage can be used as the resistance
    R0 = 100  # Resistance at 0 degrees Celsius
    A = 3.9083e-3  # Callendar-Van Dusen coefficient
    B = -5.775e-7  # Callendar-Van Dusen coefficient
    T = (-A + np.sqrt(A**2 - 4*B*(1 - resistance/R0))) / (2*B)
    return T

# Load data from the CSV file
data = np.loadtxt("DavPhi water.csv", delimiter=',', skiprows=3)

# Extract the columns for time, temperature, and voltage
time = data[:, 0]
temp = data[:, 1]
volt = data[:, 2] 

# Convert voltage readings from thermometer to temperature
temp = voltage_to_temperature(temp)

# Starting temperature
T1 = temp[0]

# Time intervals for integration
t_S = 80
t_G = 900

def integrand(t):
    return (temp[int(t)] - T1)

result, error = quad(integrand, t_S, t_G)

# Print the result
print("Integral result:", result)
