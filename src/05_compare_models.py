"""Step 5 -- Logistic regression vs Random Forest, on unseen data.

Each model learns from 80% of people and is tested on the hidden 20%.
Because one split can be lucky, the test is also repeated over 20
different random splits and averaged. The baseline is "always guess the
most common answer" -- a model is only useful if it beats that.
"""

import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

PROJECT = Path(__file__).resolve().parent.parent
df = pd.read_csv(PROJECT / "data" / "processed" / "analysis_sample.csv")

# Same factors as Model A: benefits + supervisor
clean = df[["benefits", "supervisor", "treatment"]].dropna()
X = pd.get_dummies(clean[["benefits", "supervisor"]],
                   drop_first=True).astype(int)
y = clean["treatment"].astype(int)
print("People used:", len(y))


def test_once(seed):
    """Split 80/20 with this seed; return both models' test accuracy."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y)

    lr = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)

    baseline = max(y_test.mean(), 1 - y_test.mean())
    return lr.score(X_test, y_test), rf.score(X_test, y_test), baseline


# 1. One fixed split (seed 42) -- the same numbers every time
lr_acc, rf_acc, base = test_once(42)
print("\n1) One split (seed 42):")
print(f"   Logistic regression: {lr_acc:.1%}")
print(f"   Random Forest:       {rf_acc:.1%}")

# 2. Average over 20 different random splits
results = pd.DataFrame([test_once(seed) for seed in range(20)],
                       columns=["logistic", "forest", "baseline"])
gaps = (results["forest"] - results["logistic"]) * 100

print("\n2) Average over 20 splits:")
print(f"   Logistic regression: {results['logistic'].mean():.1%}")
print(f"   Random Forest:       {results['forest'].mean():.1%}")
print(f"   Gap: {gaps.mean():+.1f} points on average "
      f"(from {gaps.min():+.1f} to {gaps.max():+.1f})")

# 3. The baseline
print(f"\n3) Always guessing the most common answer: "
      f"{results['baseline'].mean():.1%}")