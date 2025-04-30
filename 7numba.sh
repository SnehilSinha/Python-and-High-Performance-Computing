#!/bin/sh
#BSUB -q hpc
#BSUB -J jacobi_numba
#BSUB -o jacobioutput/jacobi_numba.out
#BSUB -e jacobioutput/jacobi_numba.err
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 01:00



source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python 7numba.py 10