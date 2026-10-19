import pandas as pd
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent

# Load the 2014 survey
df = pd.read_csv(PROJECT / "data" / "raw" / "OSMI_2014.csv")

# Size of the data
print("Rows, columns:", df.shape)

# Types of answers in the treatment column?
print("\nTreatment answers:")
print(df["treatment"].value_counts(dropna=False))

# Types of answers in the benefits column?
print("\nBenefits answers:")
print(df["benefits"].value_counts(dropna=False))