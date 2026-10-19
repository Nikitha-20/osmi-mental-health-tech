import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
df17 = pd.read_csv(PROJECT / "data" / "raw" / "OSMI_2017.csv")

benefits_col = ("Does your employer provide mental health benefits "
                "as part of healthcare coverage?")

# Try to find the benefits column the normal way
print("Found the benefits column?", benefits_col in df17.columns)

# Find column names that contain the hidden character
print("\nColumns with a hidden non-breaking space:")
for col in df17.columns:
    if "\xa0" in col:
        print(repr(col))

# Swap every hidden space for a normal space
df17.columns = [col.replace("\xa0", " ") for col in df17.columns]
print("\nFound it after the fix?", benefits_col in df17.columns)

# Check the answers
print("\n2017 benefits answers:")
print(df17[benefits_col].value_counts(dropna=False))