import numpy as np
import matplotlib.pyplot as plt

def truss_analysis(E_list, lengths, Area) -> tuple:
    n_elements = len(E_list)

    # Calculate the stiffness matrices
    K_list = []
    for i in range(n_elements):
        E = E_list[i]
        A = Area
        L = lengths[i]
        K = (E * A / L) * np.array([[1, -1], [-1, 1]])
        K_list.append(K)

    # Assemble the global stiffness matrix
    K_global = np.zeros((n_elements + 1, n_elements + 1))
    for i in range(n_elements):
        K_global[i:i + 2, i:i + 2] += K_list[i]

    # Apply boundary conditions
    # (node : displacement)
    BCs = {
        0 : 0,
        5 : 1,
    }

    u = np.zeros(n_elements + 1)
    f = np.zeros(n_elements + 1)

    for node, displacement in BCs.items():
        u[node] = displacement

    free_nodes = [i for i in range(n_elements + 1) if i not in BCs.keys()]

    K_reduced = K_global[np.ix_(free_nodes, free_nodes)] # K_reduced = K_global[free_nodes][:, free_nodes] is equivalent

    f_reduced = f[free_nodes]

    for i, node in enumerate(free_nodes):
        f_reduced[i] = f[node] - np.dot(K_global[node], u)

    # Solve for the displacements
    u_reduced = np.linalg.solve(K_reduced, f_reduced)

    # Update the global displacements
    for i, node in enumerate(free_nodes):
        u[node] = u_reduced[i]

    # Calculate the reaction forces
    f = np.dot(K_global, u)

    return u, f

np.set_printoptions(precision=3, suppress=True)

Area = 25
E_list = [250, 120, 320, 150, 220]
lengths = [180, 30, 90, 120, 230]

u, f = truss_analysis(E_list, lengths, Area)

print(f"Displacements: {u}")
print(f"Reaction forces: {f}")

# Plot the displacements
plt.plot(u)
plt.xlabel("Node")
plt.ylabel("Displacement")
plt.title("Displacement of nodes")

E_list = [120]*5

u, f = truss_analysis(E_list, lengths, Area)

print(f"Displacements: {u}")
print(f"Reaction forces: {f}")

# Plot the displacements
plt.plot(u)

lengths = [100]*5

u, f = truss_analysis(E_list, lengths, Area)

print(f"Displacements: {u}")
print(f"Reaction forces: {f}")

# Plot the displacements
plt.plot(u)

plt.show()
