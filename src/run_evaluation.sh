#!/bin/bash
echo "Starting first script..."
python evaluator.py --input_data ./data/LeCoDe_testset.jsonl --evaluation_data ./outputs/output_file_askq_32b/
echo "First script completed"

