#!/bin/sh
eval "$(conda shell.bash hook)"
conda activate bool
cd run1
python runner.py
cd ..
cd run2
python runner.py
cd ..
cd run3
python runner.py
cd ..
