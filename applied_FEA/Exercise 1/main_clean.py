import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def truss_analysis(E_list: List[float], lengths: List[float], Area: float) -> Tuple[np.ndarray, np.ndarray]:
    n_elements = len(E_list)

    # Calculate the stiffness matrices and assemble the global stiffness matrix
    K_global = np.zeros((n_elements + 1, n_elements + 1))
    for i in range(n_elements):
        E = E_list[i]
        L = lengths[i]
        K = (E * Area / L) * np.array([[1, -1], [-1, 1]])
        K_global[i:i + 2, i:i + 2] += K

    # Apply boundary conditions
    u, free_nodes = apply_boundary_conditions(K_global)

    # Solve for the displacements
    K_reduced = K_global[np.ix_(free_nodes, free_nodes)]
    f_reduced = np.dot(K_global[free_nodes], u)

    for i, node in enumerate(free_nodes):
        f_reduced[i] = -f_reduced[i]

    u_reduced = np.linalg.solve(K_reduced, f_reduced)

    print(u_reduced)

    # Update the global displacements
    for i, node in enumerate(free_nodes):
        u[node] = u_reduced[i]

    # Calculate the reaction forces
    f = np.dot(K_global, u)

    return u, f

def apply_boundary_conditions(K_global: np.ndarray) -> Tuple[np.ndarray, List[int]]:
    BCs = {
        0: 0,
        5: 0.5,
    }  # (node : displacement)
    n_elements = K_global.shape[0] - 1
    u = np.zeros(n_elements + 1)

    for node, displacement in BCs.items():
        u[node] = displacement

    free_nodes = [i for i in range(n_elements + 1) if i not in BCs.keys()]
    
    return u, free_nodes

def plot_displacements(u: np.ndarray, lengths: List[float], title: str) -> None:
    # Create an array for x positions based on lengths
    x_positions = np.zeros(len(lengths) + 1)
    for i in range(1, len(lengths) + 1):
        x_positions[i] = x_positions[i - 1] + lengths[i - 1]

    plt.plot(x_positions, u, marker='o')  # Add markers to show nodes
    plt.xlabel("Position along the truss (mm)")
    plt.ylabel("Displacement")
    plt.title(title)
    plt.grid()

def plot_reaction_forces(f: np.ndarray, lengths: List[float], title: str) -> None:
    # Create an array for x positions based on lengths
    x_positions = np.zeros(len(lengths) + 1)
    for i in range(1, len(lengths) + 1):
        x_positions[i] = x_positions[i - 1] + lengths[i - 1]

    plt.plot(x_positions, f, marker='o')  # Add markers to show nodes
    plt.xlabel("Position along the truss (mm)")
    plt.ylabel("Reaction Force")
    plt.title(title)
    plt.grid()

np.set_printoptions(precision=3, suppress=True)

# Define parameters
Area = 25
lengths = [180, 30, 90, 120, 230]

# Case 1: Initial E_list
E_list_1 = [250, 120, 320, 150, 220]
u1, f1 = truss_analysis(E_list_1, lengths, Area)
print(f"Displacements (Case 1): {u1}")
print(f"Reaction forces (Case 1): {f1}")
plot_displacements(u1, lengths, "Displacement of nodes (Case 1)")


# # Case 2: Uniform E_list
# E_list_2 = [120] * 5
# u2, f2 = truss_analysis(E_list_2, lengths, Area)
# print(f"Displacements (Case 2): {u2}")
# print(f"Reaction forces (Case 2): {f2}")
# plot_displacements(u2, lengths, "Displacement of nodes (Case 2)")

plt.legend(["Case 1", "Case 2"])
plt.show()

plot_reaction_forces(f1, lengths, "Reaction forces along the truss (Case 1)")
# plot_reaction_forces(f2, lengths, "Reaction forces along the truss (Case 2)")

plt.legend(["Case 1", "Case 2"])
plt.show()