#!/bin/bash

# Bash script to run simulate_static.py with different numbers of workers
# Saves results to a simple text file

BUILDINGS=50  
PYTHON_SCRIPT=q5.py
OUTPUT_FILE=static_timing_results.txt

# Clear the previous output file
echo "Workers, Elapsed Time (seconds)" > $OUTPUT_FILE

# List of workers to test
for WORKERS in 1 2 4 8
do
    echo "Running with $WORKERS workers..."

    # Run the script and capture the elapsed time
    ELAPSED_TIME=$(python $PYTHON_SCRIPT $BUILDINGS $WORKERS | grep "Elapsed time:" | awk '{print $3}')

    echo "$WORKERS, $ELAPSED_TIME" >> $OUTPUT_FILE
done

echo "Done. Results saved to $OUTPUT_FILE"
