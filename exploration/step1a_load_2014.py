import pandas as pd
from pathlib import Path

# Find the project folder: this file's folder (src), then one level up
PROJECT = Path(__file__).resolve().parent.parent

# Load the 2014 survey
df = pd.read_csv(PROJECT / "data" / "raw" / "OSMI_2014.csv")

# 1. How big is it?
print("Rows, columns:", df.shape)

# 2. What answers are in the treatment column?
print("\nTreatment answers:")
print(df["treatment"].value_counts(dropna=False))

# 3. What answers are in the benefits column?
print("\nBenefits answers:")
print(df["benefits"].value_counts(dropna=False))