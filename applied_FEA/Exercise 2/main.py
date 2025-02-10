import numpy as np
import pandas as pd
import math
from utils import *

# Initialize Values¨
E = 210000 # [MPa]
A = 1000 # [mm^2]

Lengths = [
    4,
    4,
    4,
    4,
    4 * math.sqrt(2),
] # [m]

Angles = [
    45,
    315,
    45,
    315,
    270,
] # [°]

n_elements = 5
n_nodes = 4
DoFs = 2

k_el = []

for i in range(n_elements):
    k_el.append(PlaneTrussElementStiffness(E, A, Lengths[i], math.radians(Angles[i])))

# Initialize the global stiffness matrix
K = np.zeros((n_nodes * DoFs, n_nodes * DoFs))

# Assemble the global stiffness matrix
K = PlaneTrussAssemble(K, k_el[0], 1, 2)
K = PlaneTrussAssemble(K, k_el[1], 1, 3)
K = PlaneTrussAssemble(K, k_el[2], 3, 4)
K = PlaneTrussAssemble(K, k_el[3], 2, 4)
K = PlaneTrussAssemble(K, k_el[4], 3, 2)

# Clean up the results
K = np.round(K, 4)

# # Visualize the global stiffness matrix
# print("Global Stiffness Matrix:")
# VisualizeK(K, "Global Stiffness Matrix")

# Boundary conditions (None = unknown displacement/force)
# [u1, v1, u2, v2, u3, v3, u4, v4]
# [F1x, F1y, F2x, F2y, F3x, F3y, F4x, F4y]

disp_BCs = [
    0, 
    0, 
    None, 
    None, 
    None, 
    None, 
    None, 
    0,
] # [mm]

force_BCs = [
    None, 
    None, 
    0., 
    0., 
    0., 
    0., 
    10., 
    None,
] # [kN]

# Apply the boundary conditions
k, f = ApplyBCs(K, disp_BCs, force_BCs)

# print("Truncated Global Stiffness Matrix:")
# VisualizeK(K, "Truncated Global Stiffness Matrix")
print("Force Vector:", f)

# Solve for the displacements
u = np.linalg.solve(k, f)

# Update the global displacements
U = expand_displacements(u, disp_BCs)

print("Displacements:\n", U.reshape(-1, 2))

# Calculate the reaction forces
F:np.ndarray = np.dot(K, U)

print("Reaction Forces:\n", F.reshape(-1, 2))