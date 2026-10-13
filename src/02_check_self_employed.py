"""Step 2 -- Why are some benefits answers blank?

Checks that the blank benefits answers all come from self-employed
people (who the survey never asked), and that "Not eligible" is a
different group.
"""

import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
df = pd.read_csv(PROJECT / "data" / "processed" / "combined_clean.csv")

blank = df["benefits"].isna()
self_emp = df["self_employed"] == True   # noqa: E712

# 1. Blank benefits answers, and how many are self-employed, per year
print("Year | blank benefits | of them self-employed")
for year in [2014, 2016, 2017, 2018, 2019]:
    in_year = df["year"] == year
    n_blank = int((blank & in_year).sum())
    n_both = int((blank & self_emp & in_year).sum())
    print(f"{year} | {n_blank} | {n_both}")

print(f"\nAll years: {int((blank & self_emp).sum())} of {int(blank.sum())} "
      f"blanks are self-employed")

# 2. Is "Not eligible" the same group?
not_elig = df["benefits"] == "Not eligible"
print(f"\n'Not eligible': {int(not_elig.sum())} people, "
      f"{int((not_elig & self_emp).sum())} of them self-employed")

# 3. Self-employed people who DID answer the benefits question
answered = self_emp & ~blank
print(f"\nSelf-employed who answered benefits: {int(answered.sum())}")
print("By year:", df.loc[answered, "year"].value_counts().to_dict())