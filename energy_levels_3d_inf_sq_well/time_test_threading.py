from main_opt import find_energy_level_and_combinations
import time
from matplotlib import pyplot as plt
import threading

times = []
max_n = 200
multiple_tests = 5
for n in range(1, max_n + 1):
    duration = 0
    def calculate_duration(n):
        start_time = time.time()
        coefficient, degeneracy, combinations = find_energy_level_and_combinations(n)
        end_time = time.time()
        return end_time - start_time

    for n in range(1, max_n + 1):
        duration = 0
        threads = []
        for _ in range(multiple_tests):
            t = threading.Thread(target=lambda: times.append(calculate_duration(n)))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        print(f"[INFO]: n = {n} Done, Time = {sum(times[-multiple_tests:]):.4f} seconds")