from itertools import combinations_with_replacement
from concurrent.futures import ThreadPoolExecutor
import math

def find_combinations_parallel(coefficient):
    max_value = int(math.sqrt(coefficient))
    squares = [i**2 for i in range(1, max_value + 1)]  # Start from 1
    combinations = []

    def check_combination(combo):
        if sum(combo) == coefficient:
            nx, ny, nz = sorted([int(math.sqrt(val)) for val in combo])
            return (nx, ny, nz)
        return None

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_combination, comb) for comb in combinations_with_replacement(squares, 3)]
        for future in futures:
            result = future.result()
            if result:
                combinations.append(result)
    
    return combinations

# Example usage
coefficient = 144
result = find_combinations_parallel(coefficient)
print(result)
