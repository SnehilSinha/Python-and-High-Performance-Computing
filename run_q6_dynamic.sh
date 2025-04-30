#!/bin/bash

BUILDINGS=50
OUTPUT_FILE=q6_timing_results.txt
LOG_FILE=q6_debug.log

echo "Workers, Elapsed Time (seconds)" > $OUTPUT_FILE
echo "== Debug Output ==" > $LOG_FILE

for WORKERS in 1 2 4 8
do
    echo "Running with $WORKERS workers..." | tee -a $LOG_FILE
    python q6.py $BUILDINGS $WORKERS >> $LOG_FILE 2>&1

    # Read time directly from q6.py output
    ELAPSED=$(grep "Elapsed time:" $LOG_FILE | tail -n 1 | awk '{print $3}')
    echo "$WORKERS, $ELAPSED" >> $OUTPUT_FILE
done

echo "Done. Results saved to $OUTPUT_FILE"
