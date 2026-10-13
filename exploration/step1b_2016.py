import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

# Load the 2016 survey
df = pd.read_csv(PROJECT / "data" / "raw" / "OSMI_2016.csv")

# 1. How big is it?
print("Rows, columns:", df.shape)

# 2. 2016 has 63 columns, so just find the ones about benefits
print("\nColumns that mention 'benefit':")
for col in df.columns:
    if "benefit" in col.lower():
        print("-", col)

# 3. The benefits question (2016 uses the full question as the column name)
benefits_col = ("Does your employer provide mental health benefits "
                "as part of healthcare coverage?")
print("\nBenefits answers:")
print(df[benefits_col].value_counts(dropna=False))

# 4. The treatment question
treatment_col = ("Have you ever sought treatment for a mental health "
                 "issue from a mental health professional?")
print("\nTreatment answers:")
print(df[treatment_col].value_counts(dropna=False))