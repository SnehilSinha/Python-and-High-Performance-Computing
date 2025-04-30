from os.path import join
import sys
import numpy as np
import time
import multiprocessing as mp


# --- Functions (same as before) ---
def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)
    for i in range(max_iter):
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior
        if delta < atol:
            break
    return u

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }

# --- Worker function ---
def worker(building_ids_chunk):
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    results = []
    
    for bid in building_ids_chunk:
        u0, interior_mask = load_data(LOAD_DIR, bid)
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        stats = summary_stats(u, interior_mask)
        results.append((bid, stats))
    
    return results

# --- Main ---
if __name__ == '__main__':
    start_time = time.perf_counter()

    # Load building IDs
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 3:
        N = 10
        num_workers = 2
    else:
        N = int(sys.argv[1])
        num_workers = int(sys.argv[2])

    building_ids = building_ids[:N]

    # Split work statically
    chunk_size = (N + num_workers - 1) // num_workers  # ceil division
    chunks = [building_ids[i:i + chunk_size] for i in range(0, N, chunk_size)]

    with mp.Pool(processes=num_workers) as pool:
        all_results = pool.map(worker, chunks)

    # Flatten the list
    all_results = [item for sublist in all_results for item in sublist]

    # Print CSV output
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))
    for bid, stats in all_results:
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))

    end_time = time.perf_counter()
    print(f"\nElapsed time: {end_time - start_time:.2f} seconds")
