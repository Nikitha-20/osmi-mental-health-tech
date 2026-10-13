"""Step 3 -- Simple comparisons before any modelling.

For each workplace factor: what % of people in each group have ever
sought treatment? A factor with no gap here is unlikely to matter much
in a model either.
"""

import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
df = pd.read_csv(PROJECT / "data" / "processed" / "analysis_sample.csv")
print("People in the analysis:", len(df))


def compare(data, factor):
    """Group size and % who have ever sought treatment, per group."""
    table = data.groupby(factor)["treatment"].agg(["size", "mean"])
    table.columns = ["people", "pct_sought_help"]
    table["pct_sought_help"] = (table["pct_sought_help"] * 100).round(1)
    table = table.sort_values("pct_sought_help", ascending=False)

    spread = table["pct_sought_help"].max() - table["pct_sought_help"].min()
    print(f"\n=== {factor} ===")
    print(table.to_string())
    print(f"Spread: {spread:.1f} points")


# 1. Each factor on its own
compare(df, "benefits")
compare(df, "supervisor")
compare(df[df["year"].isin([2014, 2016])], "remote_work")   # only 2 years

# 2. The headline gap: benefits Yes vs No
rate = df.groupby("benefits")["treatment"].mean() * 100
gap = rate["Yes"] - rate["No"]   # subtract BEFORE rounding
print(f"\nBenefits Yes vs No: {rate['Yes']:.1f}% vs {rate['No']:.1f}% "
      f"= {gap:.1f} point gap")

# 3. Does the gap hold in every year?
yes_no = df[df["benefits"].isin(["Yes", "No"])]
by_year = yes_no.groupby(["year", "benefits"])["treatment"].mean().unstack()
by_year = by_year * 100
by_year["gap"] = by_year["Yes"] - by_year["No"]
print("\n=== Benefits gap, year by year ===")
print(by_year[["Yes", "No", "gap"]].round(1).to_string())