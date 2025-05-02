from os.path import join
import numpy as np
from numba import cuda
import time
import gc


@cuda.jit
def jacobi_kernel(u, u_new, mask):
    i, j = cuda.grid(2)

    if 1 <= i < u.shape[0] - 1 and 1 <= j < u.shape[1] - 1:
        if mask[i - 1, j - 1]:
            u_new[i, j] = 0.25 * (u[i - 1, j] + u[i + 1, j] + u[i, j - 1] + u[i, j + 1])


def jacobi_cuda(u_host, interior_mask, max_iter):
    u_device = cuda.to_device(u_host)
    u_new_device = cuda.device_array_like(u_device)

    mask_device = cuda.to_device(interior_mask)

    threads_per_block = (16, 16)
    blocks_per_grid_x = (u_host.shape[0] + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (u_host.shape[1] + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    for _ in range(max_iter):
        jacobi_kernel[blocks_per_grid, threads_per_block](u_device, u_new_device, mask_device)

        u_device, u_new_device = u_new_device, u_device

    final_u_host = u_device.copy_to_host()

    del u_device
    del u_new_device
    del mask_device
    gc.collect()

    return final_u_host


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2), dtype=np.float64)
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


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


if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000

    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        all_building_ids = f.read().splitlines()


    N = len(all_building_ids)
    print(f"Processing all {N} buildings.")

    run_times = []

    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id,' + ','.join(stat_keys))

    for i, bid in enumerate(all_building_ids):
        print(f"Processing building {i+1}/{N}: {bid}...")

        u0, interior_mask = load_data(LOAD_DIR, bid)

        start_time = time.time()

        u_final = jacobi_cuda(u0, interior_mask, MAX_ITER)
        end_time = time.time()

        elapsed_time = end_time - start_time
        run_times.append(elapsed_time)

        stats = summary_stats(u_final, interior_mask)

        stats_string = ",".join(str(stats.get(k, 'N/A')) for k in stat_keys)
        print(f"{bid},{stats_string}")

        del u0
        del interior_mask
        del u_final
        gc.collect()

    avg_run_time = sum(run_times) / len(run_times)
    print(f"\nAverage run time per building: {avg_run_time:.3f} seconds")
