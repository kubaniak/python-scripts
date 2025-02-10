import numpy as np

def PlaneTrussElementStiffness(E, A, L, angle) -> np.ndarray:
    # Compute the transformation matrix
    T = np.array([
        [np.cos(angle), np.sin(angle), 0,             0            ],
        [0,             0,             np.cos(angle), np.sin(angle)],
    ])
    
    # Element stiffness matrix in local coordinates
    k = E * A / L * np.array([
        [1, -1],
        [-1, 1],
    ])
    
    # Compute the element stiffness matrix
    k_el = T.T @ k @ T
    
    return k_el

def PlaneTrussAssemble(K, k, i, j) -> np.ndarray:
    # Assemble the element stiffness matrix
    K[2 * i - 2:2 * i, 2 * i - 2:2 * i] += k[:2, :2]
    K[2 * i - 2:2 * i, 2 * j - 2:2 * j] += k[:2, 2:]
    K[2 * j - 2:2 * j, 2 * i - 2:2 * i] += k[2:, :2]
    K[2 * j - 2:2 * j, 2 * j - 2:2 * j] += k[2:, 2:]

    return K

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

    pass

def ApplyBCs(K: np.ndarray, disp_BCs: list, force_BCs: list) -> np.ndarray:
    # Apply the boundary conditions
    rows_to_delete = []
    for i in range(len(force_BCs)):
        if force_BCs[i] is None:
            rows_to_delete.append(i)
    K = np.delete(K, rows_to_delete, axis=0)
    f = np.delete(force_BCs, rows_to_delete)
    f = np.array(f, dtype=np.float64)

    cols_to_delete = []
    for i in range(len(disp_BCs)):
        if disp_BCs[i] is not None:
            cols_to_delete.append(i)
    K = np.delete(K, cols_to_delete, axis=1)

    return K, f

def expand_displacements(u, disp_BCs):
    # Expand the displacements
    u_expanded = np.zeros(len(disp_BCs))
    idx = 0
    for i in range(len(disp_BCs)):
        if disp_BCs[i] is None:
            u_expanded[i] = u[idx]
            idx += 1
        else:
            u_expanded[i] = disp_BCs[i]

    return u_expanded