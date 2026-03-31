import numpy as np
import math
from utils_clean import *

# Node coordinates [x, y] [mm]
node_coords = np.array([
    [0, 0],                  # Node 0
    [300, 300],                  # Node 1
    [0, 300],                # Node 2
])

# Connectivity matrix for the truss
connectivity = [
    (0,1), # Element 1
    (1,2), # Element 2
    (2,0), # Element 3
]

# Define different Young's modulus for each element
Es = [
    210000,  # [MPa] Element 1
    210000,  # [MPa] Element 2
    210000,  # [MPa] Element 3
]

Areas = [
    200,  # [mm^2] Element 1
    200,  # [mm^2] Element 2
    200,  # [mm^2] Element 3
]

preview_truss(node_coords, connectivity)




# Boundary conditions (None = unknown displacement/force)# [u0, v0, u1, v1, u2, v2] [mm] - for 3 nodes with 2 DOFs each
disp_BCs = [0, 0, None, None, 0, 0]
# [F0x, F0y, F1x, F1y, F2x, F2y] [kN] (0 = internal force)
force_BCs = [None, None, 0.3, 0, None, None]






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
