import time
from collections import defaultdict
import heapq
from typing import List, Tuple, Union, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

def original_find_energy_level_and_combinations(n):
    coefficients = defaultdict(list)
    
    # Brute-force calculation of all combinations for the given n
    for n_x in range(1, n + 1):
        for n_y in range(1, n + 1):
            for n_z in range(1, n + 1):
                coefficient = n_x**2 + n_y**2 + n_z**2
                coefficients[coefficient].append((n_x, n_y, n_z))
    
    # Sorting coefficients
    sorted_coefficients = sorted(coefficients.items())
    
    # Extracting the nth energy level
    energy_level_index = n - 1  # Since n is 1-based and index is 0-based
    if energy_level_index < len(sorted_coefficients):
        coefficient, combinations = sorted_coefficients[energy_level_index]
        degeneracy = len(combinations)
        return coefficient, degeneracy, combinations
    else:
        return None, None, None

def optimized_find_energy_level_and_combinations_python_gpt(n):
    coefficients = {}
    
    # Limiting the range based on practical considerations
    max_range = int((n ** 2) ** 0.5) + 1
    
    # Optimized calculation of all combinations for the given n
    for n_x in range(1, max_range):
        for n_y in range(n_x, max_range):
            for n_z in range(n_y, max_range):
                coefficient = n_x**2 + n_y**2 + n_z**2
                if coefficient not in coefficients:
                    coefficients[coefficient] = []
                coefficients[coefficient].append((n_x, n_y, n_z))
                if n_x != n_y or n_y != n_z or n_x != n_z:
                    permutations = {(n_x, n_y, n_z), (n_x, n_z, n_y), 
                                    (n_y, n_x, n_z), (n_y, n_z, n_x), 
                                    (n_z, n_x, n_y), (n_z, n_y, n_x)}
                    for perm in permutations:
                        coefficients[coefficient].append(perm)
    
    # Sorting coefficients
    sorted_coefficients = sorted(coefficients.items())
    
    # Extracting the nth energy level
    energy_level_index = n - 1  # Since n is 1-based and index is 0-based
    if energy_level_index < len(sorted_coefficients):
        coefficient, combinations = sorted_coefficients[energy_level_index]
        unique_combinations = set(combinations)
        degeneracy = len(unique_combinations)
        return coefficient, degeneracy, list(unique_combinations)
    else:
        return None, None, None

from degeneracy import find_degeneracy

def find_energy_level_and_combinations(n: int) -> Union[Tuple[int, int, List[Tuple[int, int, int]]], Tuple[None, None, None]]:
    coefficients = defaultdict(list)
    
    # Efficient calculation of all combinations for the given n
    for n_x in range(1, n + 1):
        for n_y in range(n_x, n + 1):
            for n_z in range(n_y, n + 1):
                coefficient = n_x**2 + n_y**2 + n_z**2
                coefficients[coefficient].append((n_x, n_y, n_z))
    
    # Using a heap to maintain the smallest n coefficients
    min_heap = [(coef, combs) for coef, combs in coefficients.items()]
    heapq.heapify(min_heap)
    
    # Extracting the nth energy level
    energy_level_index = n - 1  # Since n is 1-based and index is 0-based
    sorted_coefficients = heapq.nsmallest(n, min_heap)
    
    if energy_level_index < len(sorted_coefficients):
        coefficient, combinations = sorted_coefficients[energy_level_index]
        degeneracy = find_degeneracy(combinations)
        return coefficient, degeneracy, combinations
    else:
        return None, None, None

# # Example usage
# n = 500  # Find the 200th energy level

# # Measure time for original function
# start_time = time.time()
# original_coefficient, original_degeneracy, original_combinations = original_find_energy_level_and_combinations(n)
# end_time = time.time()
# original_duration = end_time - start_time

# # Measure time for optimized function
# start_time = time.time()
# optimized_coefficient_python, optimized_degeneracy_python, optimized_combinations_python = optimized_find_energy_level_and_combinations_python_gpt(n)
# end_time = time.time()
# optimized_duration_python = end_time - start_time

# # Measure time for optimized function using code copilot
# start_time = time.time()
# optimized_coefficient_code_copilot, optimized_degeneracy_code_copilot, optimized_combinations_code_copilot = find_energy_level_and_combinations_code_copilot_gpt(n)
# end_time = time.time()
# optimized_duration_code_copilot = end_time - start_time

# # Measure time for optimized function using threading
# start_time = time.time()
# optimized_coefficient_threading, optimized_degeneracy_threading, optimized_combinations_threading = find_energy_level_and_combinations(n)
# end_time = time.time()
# optimized_duration_threading = end_time - start_time

# Print results
# # print(f"Original Function: Duration = {original_duration:.4f} seconds")
# # print(f"Optimized Function Python: Duration = {optimized_duration_python:.4f} seconds")
# print(f"Optimized Function Code Copilot: Duration = {optimized_duration_code_copilot:.4f} seconds")
# # print(f"Optimized Function Threading: Duration = {optimized_duration_threading:.4f} seconds")

# # print(f"Original Result: E_{n}: coefficient={original_coefficient}, degeneracy={original_degeneracy}")
# # print(f"Optimized Result: E_{n}: coefficient={optimized_coefficient_python}, degeneracy={optimized_degeneracy_python}")
# print(f"Optimized Result Code Copilot: E_{n}: coefficient={optimized_coefficient_code_copilot}, degeneracy={optimized_degeneracy_code_copilot}")
# # print(f"Optimized Result Threading: E_{n}: coefficient={optimized_coefficient_threading}, degeneracy={optimized_degeneracy_threading}")
