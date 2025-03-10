import numpy as np
import matplotlib.pyplot as plt

def calculate_lengths_angles(node_coords, connectivity):
    """
    Calculate the lengths and angles of truss elements based on node coordinates and connectivity.
    Args:
        node_coords (np.ndarray): Coordinates of each node in the structure.
        connectivity (list of tuple): Connectivity of each element, where each tuple contains two node indices.
    Returns:
        lengths (list of float): Length of each element.
        angles (list of float): Angle of each element in radians.
    """
    lengths = []
    angles = []

    for (n1, n2) in connectivity:
        # Node coordinates (subtract 1 to account for zero-indexing)
        x1, y1 = node_coords[n1 - 1]
        x2, y2 = node_coords[n2 - 1]
        
        # Calculate length (Euclidean distance)
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        lengths.append(length)
        
        # Calculate angle (atan2 gives angle in radians directly)
        angle = np.arctan2(y2 - y1, x2 - x1)
        angles.append(angle)
    
    return lengths, angles

def PlaneTrussElementStiffness(E, A, L, angle) -> np.ndarray:
    """
    Calculate the stiffness matrix for a 2D truss element.
    """
    # Compute the transformation matrix
    T = np.array([
        [np.cos(angle), np.sin(angle), 0, 0],
        [0, 0, np.cos(angle), np.sin(angle)]
    ])
    
    # Element stiffness matrix in local coordinates
    k_local = E * A / L * np.array([[1, -1], [-1, 1]])
    
    # Compute the global stiffness matrix
    k_global = T.T @ k_local @ T
    
    return k_global

def PlaneTrussAssemble(K, k, i, j) -> np.ndarray:
    """
    Assemble the element stiffness matrix into the global stiffness matrix.
    """
    idx_i = [2 * i - 2, 2 * i - 1]
    idx_j = [2 * j - 2, 2 * j - 1]
    
    # Assembling the stiffness matrix into global matrix
    K[np.ix_(idx_i, idx_i)] += k[:2, :2]
    K[np.ix_(idx_i, idx_j)] += k[:2, 2:]
    K[np.ix_(idx_j, idx_i)] += k[2:, :2]
    K[np.ix_(idx_j, idx_j)] += k[2:, 2:]

    return K

def ApplyBCs(K: np.ndarray, disp_BCs: list, force_BCs: list) -> tuple[np.ndarray, np.ndarray]:
    """
    Apply boundary conditions by modifying the global stiffness matrix and the force vector.
    """
    # Identify rows/columns to delete (displacements known or forces unknown)
    free_dofs = [i for i, bc in enumerate(disp_BCs) if bc is None]
    
    # Reduce the system to free DoFs
    K_reduced = K[np.ix_(free_dofs, free_dofs)]
    f_reduced = np.array([force_BCs[i] for i in free_dofs], dtype=np.float64)

    return K_reduced, f_reduced

def expand_displacements(u: np.ndarray, disp_BCs: list) -> np.ndarray:
    """
    Expand the displacement vector to include known boundary conditions.
    """
    full_u = np.zeros(len(disp_BCs))
    u_iter = iter(u)
    for i, bc in enumerate(disp_BCs):
        full_u[i] = next(u_iter) if bc is None else bc
    
    return full_u

def plot_truss(node_coords, connectivity, displacements, scale_factor, force_BCs, name="Truss"):
    """
    Plot the original and deformed truss structure with exaggerated displacements.
    Also label the elements with their corresponding numbers.
    """
    n_nodes = node_coords.shape[0]
    DoFs = 2
    # Reshape displacements into (n_nodes, 2) array for x and y displacements
    disp = displacements.reshape((n_nodes, DoFs))
    
    # Create a figure and axis
    plt.figure(figsize=(8, 8))
    
    # Plot the original truss
    for idx, (i, j) in enumerate(connectivity):
        x = [node_coords[i-1, 0], node_coords[j-1, 0]]
        y = [node_coords[i-1, 1], node_coords[j-1, 1]]
        plt.plot(x, y, 'b-o', label='Undeformed' if idx == 0 else "")
        
        # Calculate the center of the element for labeling
        center_x = (x[0] + x[1]) / 2
        center_y = (y[0] + y[1]) / 2
        # Add the label for the element
        plt.text(center_x, center_y, f'Element {idx+1}', color='blue', fontsize=12)

    # Plot the deformed truss
    deformed_coords = node_coords + disp * scale_factor
    for idx, (i, j) in enumerate(connectivity):
        x_def = [deformed_coords[i-1, 0], deformed_coords[j-1, 0]]
        y_def = [deformed_coords[i-1, 1], deformed_coords[j-1, 1]]
        plt.plot(x_def, y_def, 'r--o', label='Deformed' if idx == 0 else "")
        
        # # Calculate the center of the deformed element for labeling
        # center_x_def = (x_def[0] + x_def[1]) / 2
        # center_y_def = (y_def[0] + y_def[1]) / 2
        # # Add the label for the deformed element
        # plt.text(center_x_def, center_y_def, f'Element {idx+1}', color='red', fontsize=12, alpha=0.3)
    
    # Plot force vectors from force_BCs
    for node_idx in range(n_nodes):
        Fx = force_BCs[2 * node_idx]   # x-force component
        Fy = force_BCs[2 * node_idx + 1]  # y-force component
        
        if Fx is not None or Fy is not None:
            # If there is a non-None force, plot an arrow at this node
            node_x, node_y = node_coords[node_idx]
            Fx = Fx if Fx is not None else 0
            Fy = Fy if Fy is not None else 0
            plt.quiver(node_x, node_y, Fx, Fy, angles='xy', scale_units='xy', scale=10, color='green', width=0.005, label='Forces' if node_idx == 0 else "")


    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.title('Original and Deformed Truss Structure')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.savefig(f"Exercise 2/Figures/{name}.png", dpi=300)
    plt.show()

def preview_truss(node_coords, connectivity):
    """
    Plot the undeformed truss structure.
    """
    n_nodes = node_coords.shape[0]
    
    # Create a figure and axis
    plt.figure(figsize=(8, 8))
    
    # Plot the original truss
    for idx, (i, j) in enumerate(connectivity):
        x = [node_coords[i-1, 0], node_coords[j-1, 0]]
        y = [node_coords[i-1, 1], node_coords[j-1, 1]]
        plt.plot(x, y, 'b-o', label='Undeformed' if idx == 0 else "")
        
        # Calculate the center of the element for labeling
        center_x = (x[0] + x[1]) / 2
        center_y = (y[0] + y[1]) / 2
        # Add the label for the element
        plt.text(center_x, center_y, f'Element {idx+1}', color='blue', fontsize=12)
    
    # Add node labels (1 to n)
    for i in range(n_nodes):
        plt.text(node_coords[i, 0], node_coords[i, 1], f'Node {i+1}',
                 color='darkgreen', fontsize=12, fontweight='bold',
                 ha='right', va='bottom')
    
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.title('Undeformed Truss Structure')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def VisualizeK(K, title) -> None:
    import pandas as pd
    df = pd.DataFrame(K)
    print(df)

    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(6,5))
    sns.heatmap(K, annot=True, cmap="YlGnBu", cbar=True)
    plt.title(title)
    plt.show()