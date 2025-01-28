import numpy as np

def addition_rule(x_1: float, x_2: float) -> tuple:
    res = ()
    x_2_range = np.arange(-x_2, x_2 + 1)
    for i in x_2_range:
        res += (abs(x_1 + i),)
    return tuple(set(res))

print(addition_rule(1, 1/2))