import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
RAW = PROJECT / "data" / "raw"

df14 = pd.read_csv(RAW / "OSMI_2014.csv")
df16 = pd.read_csv(RAW / "OSMI_2016.csv")
df17 = pd.read_csv(RAW / "OSMI_2017.csv")
df17.columns = [col.replace("\xa0", " ") for col in df17.columns]  # Step 4 fix

# One dictionary that translates every year's wording into shared labels
BENEFITS_MAP = {
    "Yes": "Yes",
    "No": "No",
    "Don't know": "Don't know",                     # 2014 wording
    "I don't know": "Don't know",                   # 2016 wording
    "Not eligible for coverage / N/A": "Not eligible", # 2016 spelling
    "Not eligible for coverage / NA": "Not eligible", # 2017+ spelling
}

benefits_col_16 = ("Does your employer provide mental health benefits "
                   "as part of healthcare coverage?")


clean14 = df14["benefits"].map(BENEFITS_MAP)
clean16 = df16[benefits_col_16].map(BENEFITS_MAP)
clean17 = df17[benefits_col_16].map(BENEFITS_MAP)   # same question text as 2016

print("2014 after cleaning:")
print(clean14.value_counts(dropna=False))
print("\n2016 after cleaning:")
print(clean16.value_counts(dropna=False))
print("\n2017 after cleaning:")
print(clean17.value_counts(dropna=False))