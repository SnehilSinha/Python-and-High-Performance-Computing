import numpy as np
import matplotlib.pyplot as plt

# --- Load the results ---
workers = []
elapsed_times = []

with open('static_timing_results.txt', 'r') as f:
    lines = f.readlines()[1:]  # skip header
    for line in lines:
        parts = line.strip().split(',')
        workers.append(int(parts[0]))
        elapsed_times.append(float(parts[1]))

workers = np.array(workers)
elapsed_times = np.array(elapsed_times)

# --- Calculate speedup ---
T1 = elapsed_times[0]  # Time with 1 worker
speedup = T1 / elapsed_times

# --- Plot ---
plt.figure(figsize=(8,6))
plt.plot(workers, speedup, 'o-', label='Measured Speedup')
plt.plot(workers, workers, 'k--', label='Ideal Linear Speedup')
plt.xlabel('Number of Workers')
plt.ylabel('Speedup')
plt.title('Speedup vs Number of Workers (Static Scheduling)')
plt.grid(True)
plt.legend()
plt.tight_layout()

# --- Save the figure ---
plt.savefig('speedup_static.png')
plt.show()