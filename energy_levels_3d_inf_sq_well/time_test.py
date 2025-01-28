from main_opt import find_energy_level_and_combinations
import time
from matplotlib import pyplot as plt

times = []
max_n = 200
multiple_tests = 2
for n in range(1, max_n + 1):
    duration = 0
    for _ in range(multiple_tests):
        start_time = time.time()
        coefficient, degeneracy, combinations = find_energy_level_and_combinations(n)
        end_time = time.time()
        duration += end_time - start_time
    times.append(duration)
    print(f"[INFO]: n = {n} Done, Time = {duration:.4f} seconds")

# Plotting the results
plt.plot(range(1, max_n + 1), times)
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Execution Time vs n")
plt.show()