import numpy as np
import matplotlib.pyplot as plt

def voltage_to_temperature(voltage):
    resistance = voltage + 100 # 1 mV corresponds to 1 Ohm resistance in the configured PT-100, so the voltage can be used as the resistance
    R0 = 100  # Resistance at 0 degrees Celsius
    A = 3.9083e-3  # Callendar-Van Dusen coefficient
    B = -5.775e-7  # Callendar-Van Dusen coefficient
    T = (-A + np.sqrt(A**2 - 4*B*(1 - resistance/R0))) / (2*B)
    return T

def voltage_to_power(voltage):
    return voltage * 1.6783 # P = U * I, with U = 1.6783 A

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

# Create a figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 8))

# Plot the temperature data
axs[0].plot(time, temp)
axs[0].set_ylabel('Temperature (°C)')

# Plot the voltage data
axs[1].plot(time, volt)
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Power (W)')


# Fit a line to the temperature data between t = 150 and t = 350
mask = (time >= 150) & (time <= 350)
p_fit = np.polyfit(time[mask], temp[mask], 1)
slope, _ = np.polyfit(time[mask], temp[mask], 1)

# Plot the line over the temperature data
axs[0].plot(time[mask], np.polyval(p_fit, time[mask]), '--r', label=("dT/dt = {:.2f}".format(slope)))
axs[0].legend()

# Show the plot
plt.show()