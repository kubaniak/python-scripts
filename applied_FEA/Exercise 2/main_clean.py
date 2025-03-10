import numpy as np
import math
from utils_clean import *

# Node coordinates
node_coords = np.array([
    [0, 0],                  # Node 1
    [0, 1],                  # Node 2
    [2, 1],                # Node 3
    [2, 0],                  # Node 4
    [1, 0],                # Node 5
])

# Connectivity matrix for the truss
connectivity = [
    (1, 2),
    (1, 5),
    (2, 5),
    (2, 3),
    (3, 4),
    (3, 5),
    (4, 5),    
]

# Define different Young's modulus for each element
Es = [
    210000,  # [MPa] Element 1
    210000,  # [MPa] Element 2
    210000,  # [MPa] Element 3
    210000,  # [MPa] Element 4
    210000,  # [MPa] Element 5
    210000,  # [MPa] Element 6
    210000,  # [MPa] Element 7
]

Areas = [
    1000,  # [mm^2] Element 1
    1000,  # [mm^2] Element 2
    1000,  # [mm^2] Element 3
    1000,  # [mm^2] Element 4
    1000,  # [mm^2] Element 5
    1000,  # [mm^2] Element 6
    1000,  # [mm^2] Element 7
]

# preview_truss(node_coords, connectivity)




# Boundary conditions (None = unknown displacement/force)
# [u1, v1, u2, v2, u3, v3, u4, v4] [mm]
disp_BCs = [None, 0, None, None, None, None, 0, 0, None, None]
# [F1x, F1y, F2x, F2y, F3x, F3y, F4x, F4y] [kN]
force_BCs = [0, None, -10, 0, 0, 0, None, None, 0, 0]






# Calculate lengths and angles from node coordinates and connectivity
Lengths, Angles = calculate_lengths_angles(node_coords, connectivity)

print("Lengths:", Lengths)
print("Angles:", Angles)

# Number of nodes and elements
n_nodes = node_coords.shape[0]
n_elements = len(connectivity)

print("Number of nodes:", n_nodes)
print("Number of elements:", n_elements)

# Assemble element stiffness matrices
k_el = [PlaneTrussElementStiffness(Es[i], Areas[i], Lengths[i], Angles[i]) for i in range(n_elements)]

# Initialize and assemble the global stiffness matrix
K = np.zeros((n_nodes * 2, n_nodes * 2))
for i, (n1, n2) in enumerate(connectivity):
    K = PlaneTrussAssemble(K, k_el[i], n1, n2)

# Round the global stiffness matrix for cleaner output
K = np.round(K, 4)

# VisualizeK(K, "Global Stiffness Matrix")

# Apply the boundary conditions
K_mod, f = ApplyBCs(K, disp_BCs, force_BCs)

# VisualizeK(K_mod, "Modified Global Stiffness Matrix")

# Solve for the unknown displacements
u = np.linalg.solve(K_mod, f)

# Expand the displacements vector
U = expand_displacements(u, disp_BCs)

# Display displacements and reaction forces
print("Displacements:\n", U.reshape(-1, 2))

# Calculate the reaction forces
F = np.dot(K, U).round(4)
print("Reaction Forces:\n", F.reshape(-1, 2))

# Visualization (with scale factor for displacements)
scale_factor = 500000  # Increase to exaggerate displacements
plot_truss(node_coords, connectivity, U, scale_factor, force_BCs, name="Triangle")
