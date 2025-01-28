import numpy as np
from scipy.integrate import quad
from scipy import integrate 

# Define the constants
I = 1.6783  # Current in Amperes
V = 10  # Voltage in Volts

def voltage_to_temperature(voltage):
    resistance = voltage + 100 # 1 mV corresponds to 1 Ohm resistance in the configured PT-100, so the voltage can be used as the resistance
    R0 = 100  # Resistance at 0 degrees Celsius
    A = 3.9083e-3  # Callendar-Van Dusen coefficient
    B = -5.775e-7  # Callendar-Van Dusen coefficient
    T = (-A + np.sqrt(A**2 - 4*B*(1 - resistance/R0))) / (2*B)
    return T

def voltage_to_power(voltage):
    return voltage * I # P = U * I, with U = 1.6783 A

# Load data from the CSV file
data = np.loadtxt("DavPhi water.csv", delimiter=',', skiprows=3)

# Extract the columns for time, temperature, and voltage
time = data[:, 0]
temp = data[:, 1]
volt = data[:, 2]

# Convert voltage readings from thermometer to temperature
temp = voltage_to_temperature(temp)

# Convert voltage readings from heater to temperature
volt = voltage_to_power(volt)

T1 = temp[0]  # Starting temperature in Celsius

# Calculate the slope of the temperature graph
mask = (time >= 150) & (time <= 350)
slope, _ = np.polyfit(time[mask], temp[mask], 1)

# Calculate the integral from t_S to t_G of (T - T1)dt
t_S = 80
t_G = 1200

def integrand(t):
    return (temp[int(t)] - T1)

F, error = quad(integrand, t_S, t_G)

# F = integrate.trapezoid(temp, time)

# The variables needed for the specific heat calculation
I = 1.6783  # Current in Amperes
V = 10  # Voltage in Volts
dt = 200
dT = temp[350] - temp[150]
slope = slope

# Calculate the specific heat

C = (I*V*dt*dT)/((dT**2-slope*F))

print("Specific heat: {:.2f} J/g°C".format(C))
