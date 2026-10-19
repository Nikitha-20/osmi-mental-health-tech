import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

# Load the 2016 survey
df = pd.read_csv(PROJECT / "data" / "raw" / "OSMI_2016.csv")

# Size of the data
print("Rows, columns:", df.shape)

# 2016 has 63 columns, so finding the ones about benefits
print("\nColumns that mention 'benefit':")
for col in df.columns:
    if "benefit" in col.lower():
        print("-", col)

# The benefits question (2016 uses the full question as the column name)
benefits_col = ("Does your employer provide mental health benefits "
                "as part of healthcare coverage?")
print("\nBenefits answers:")
print(df[benefits_col].value_counts(dropna=False))

# The treatment question
treatment_col = ("Have you ever sought treatment for a mental health "
                 "issue from a mental health professional?")
print("\nTreatment answers:")
print(df[treatment_col].value_counts(dropna=False))