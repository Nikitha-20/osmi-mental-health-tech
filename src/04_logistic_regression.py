"""Step 4 -- Logistic regression: how much does each factor shift the odds?

Model A: benefits + supervisor, all 5 years.
Model B: adds remote work, 2014 + 2016 only (the years that asked it).

Each odds ratio compares a group with the baseline group:
  benefits -> "Don't know", supervisor -> "Maybe", remote work -> "No".
An odds ratio of 2.7 means 2.7 times the odds of having sought treatment.
If its 95% range (ci_low to ci_high) includes 1, the data can't tell it
apart from "no effect".
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
df = pd.read_csv(PROJECT / "data" / "processed" / "analysis_sample.csv")


def fit_model(data, factors, title):
    """Fit a logistic regression and print odds ratios with 95% ranges."""
    # Keep only people who answered every question in the model
    clean = data[factors + ["treatment"]].dropna()

    # Turn each answer into its own 0/1 column; drop_first leaves out
    # one group per factor as the baseline
    X = pd.get_dummies(clean[factors], drop_first=True).astype(float)
    X = sm.add_constant(X)   # the model's starting point (intercept)
    y = clean["treatment"].astype(int)

    model = sm.Logit(y, X).fit(disp=0)

    ranges = np.exp(model.conf_int())
    results = pd.DataFrame({
        "odds_ratio": np.exp(model.params),
        "ci_low": ranges[0],
        "ci_high": ranges[1],
    }).drop(index="const").round(2)

    print(f"\n=== {title} (n = {len(y)}) ===")
    print(results.sort_values("odds_ratio", ascending=False).to_string())
    return model


# Model A: all 5 years
model_a = fit_model(df, ["benefits", "supervisor"],
                    "Model A: benefits + supervisor, all years")

# For HR: benefits Yes compared with benefits No
yes_vs_no = np.exp(model_a.params["benefits_Yes"]
                   - model_a.params["benefits_No"])
print(f"\nBenefits Yes vs No: {yes_vs_no:.1f}x the odds")

# Model B: add remote work, only the 2 years that asked it
remote_years = df[df["year"].isin([2014, 2016])]
fit_model(remote_years, ["benefits", "supervisor", "remote_work"],
          "Model B: + remote work, 2014 and 2016")