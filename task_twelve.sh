#!/bin/sh
#BSUB -q c02613
#BSUB -J cuda
#BSUB -o cuda_%J.out
#BSUB -e cuda_%J.err
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -W 02:00
#BSUB -gpu "num=1:mode=exclusive_process"



source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python task_twelve.py
