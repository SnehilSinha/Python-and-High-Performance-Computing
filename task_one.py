import numpy as np
import matplotlib.pyplot as plt
import os
from os.path import join


LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
OUTPUT_DIR = './task_one_output'

BUILDING_IDS_TO_VISUALIZE = ['10000', '10334', '10786', '11117']
GRID_SIZE = 512


def load_data_for_visualization(load_dir, bid):
    domain_path = join(load_dir, f"{bid}_domain.npy")
    interior_path = join(load_dir, f"{bid}_interior.npy")

    u = None
    interior_mask = None

    if os.path.exists(domain_path):
        u_full = np.zeros((GRID_SIZE + 2, GRID_SIZE + 2))
        u_full[1:-1, 1:-1] = np.load(domain_path)
        u = u_full

    if os.path.exists(interior_path):
        interior_mask = np.load(interior_path)

    return u, interior_mask


def visualize_and_save_data(bid, temp_grid, interior_mask, output_dir):
    if temp_grid is None or interior_mask is None:
        print(f"Skipping visualization for Building ID {bid} due to missing data.")
        return

    # Initial Temperature Grid
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    im1 = ax1.imshow(temp_grid[1:-1, 1:-1], cmap='viridis', origin='lower')
    ax1.set_title(f'Building {bid} - Initial Temperature Grid')
    ax1.set_xlabel('X-coordinate')
    ax1.set_ylabel('Y-coordinate')
    fig1.colorbar(im1, ax=ax1, label='Temperature (°C)')
    plt.tight_layout()

    filename1 = join(output_dir, f"{bid}_domain.png")
    plt.savefig(filename1)
    print(f"Saved: {filename1}")
    plt.close(fig1)

    # Interior Mask
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    im2 = ax2.imshow(interior_mask, cmap='gray', origin='lower')
    ax2.set_title(f'Building {bid} - Interior Mask')
    ax2.set_xlabel('X-coordinate')
    ax2.set_ylabel('Y-coordinate')
    plt.tight_layout()

    filename2 = join(output_dir, f"{bid}_interior_mask.png")
    plt.savefig(filename2)
    print(f"Saved: {filename2}")
    plt.close(fig2)


if __name__ == "__main__":
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for building_id in BUILDING_IDS_TO_VISUALIZE:
        print(f"\nProcessing Building ID: {building_id}")
        u_data, interior_mask_data = load_data_for_visualization(LOAD_DIR, building_id)
        visualize_and_save_data(building_id, u_data, interior_mask_data, OUTPUT_DIR)
