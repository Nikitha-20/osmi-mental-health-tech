"""Run the whole project in order, from raw data to results and charts.

Run from the project folder:  python run_all.py
"""

import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "src"

STEPS = [
    "01_clean_and_merge.py",
    "02_check_self_employed.py",
    "03_exploratory_analysis.py",
    "04_logistic_regression.py",
    "05_compare_models.py",
    "06_charts.py",
]

for step in STEPS:
    print("\n" + "#" * 60)
    print("# " + step)
    print("#" * 60)
    result = subprocess.run([sys.executable, str(SRC / step)])
    if result.returncode != 0:
        sys.exit(f"\nStopped: {step} failed.")

print("\nAll steps finished.")
print("Results are printed above; charts are in figures/.")