import numpy as np
import matplotlib.pyplot as plt

# Parameters
R = 1.0  # Radius of the disk
omega = 2.0  # Angular velocity (arbitrary units)

# Vertical positions from top (-R) to bottom (+R)
y_positions = np.linspace(-R, R, 100)

# Calculate vertical acceleration profile
a_vertical = -y_positions * omega**2

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(a_vertical, y_positions, label=r"$a_{\text{vertical}}(y) = -y \omega^2$", color="blue")
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')

# Labels and titles
plt.xlabel("Vertical Acceleration $a_{\text{vertical}}$ (units)")
plt.ylabel("Position along Vertical Axis $y$ (units)")
plt.title("Vertical Acceleration Profile along Vertical Diameter of Disk")
plt.legend()
plt.grid(True)
plt.show()
