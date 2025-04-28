#!/bin/bash
#BSUB -q hpc
#BSUB -J task_one
#BSUB -o task_one_%J.out
#BSUB -e task_one_%J.err
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 01:00


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613


python task_one.py
