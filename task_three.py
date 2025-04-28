import os
from os.path import join
import sys

import numpy as np
import matplotlib.pyplot as plt


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
            break
    return u


def visualize_and_save_data(bid, u, output_dir):
    if u is None:
        print(f"Skipping visualization for Building ID {bid} due to missing data.")
        return

    fig1, ax1 = plt.subplots(figsize=(6, 5))
    im1 = ax1.imshow(u[1:-1, 1:-1], cmap='viridis', origin='lower')
    ax1.set_title(f'Building {bid} - Simulated Temperature Grid')
    ax1.set_xlabel('X-coordinate')
    ax1.set_ylabel('Y-coordinate')
    fig1.colorbar(im1, ax=ax1, label='Temperature (°C)')
    plt.tight_layout()

    filename1 = join(output_dir, f"{bid}_simulated.png")
    plt.savefig(filename1)
    print(f"Saved: {filename1}")
    plt.close(fig1)


if __name__ == '__main__':
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    OUTPUT_DIR = './task_three_output'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u


    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        visualize_and_save_data(bid, u, OUTPUT_DIR)
