#!/bin/bash
#BSUB -J static-timing
#BSUB -o static_timing_output.txt
#BSUB -e static_timing_error.txt
#BSUB -W 0:30
#BSUB -n 8
#BSUB -R "rusage[mem=4096]"
#BSUB -R "span[hosts=1]"

# Run your timing bash script
bash q5_bash.sh
