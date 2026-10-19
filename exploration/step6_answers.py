import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
RAW = PROJECT / "data" / "raw"

# the question texts that change between years
Q_BENEFITS = ("Does your employer provide mental health benefits "
              "as part of healthcare coverage?")
Q_SUPER_2016 = ("Would you feel comfortable discussing a mental health "
                "disorder with your direct supervisor(s)?")
Q_SUPER_LATER = ("Would you feel comfortable discussing a mental health "
                 "issue with your direct supervisor(s)?")
Q_TREAT_2016 = ("Have you ever sought treatment for a mental health issue "
                "from a mental health professional?")
Q_TREAT_LATER = ("Have you ever sought treatment for a mental health "
                 "disorder from a mental health professional?")

# column names per year -> short names
COLUMN_MAP = {
    2014: {"benefits": "benefits", "supervisor": "supervisor",
           "remote_work": "remote_work", "treatment": "treatment",
           "self_employed": "self_employed",
           "Age": "age", "Gender": "gender"},
    2016: {Q_BENEFITS: "benefits", Q_SUPER_2016: "supervisor",
           "Do you work remotely?": "remote_work",
           Q_TREAT_2016: "treatment",
           "Are you self-employed?": "self_employed",
           "What is your age?": "age", "What is your gender?": "gender"},
    2017: {Q_BENEFITS: "benefits", Q_SUPER_LATER: "supervisor",
           Q_TREAT_LATER: "treatment",
           "<strong>Are you self-employed?</strong>": "self_employed",
           "What is your age?": "age", "What is your gender?": "gender"},
    2018: {Q_BENEFITS: "benefits", Q_SUPER_LATER: "supervisor",
           Q_TREAT_LATER: "treatment",
           "<strong>Are you self-employed?</strong>": "self_employed",
           "What is your age?": "age", "What is your gender?": "gender"},
    2019: {Q_BENEFITS: "benefits", Q_SUPER_LATER: "supervisor",
           Q_TREAT_LATER: "treatment",
           "*Are you self-employed?*": "self_employed",
           "What is your age?": "age", "What is your gender?": "gender"},
}

# answer translation tables
BENEFITS_MAP = {
    "Yes": "Yes",
    "No": "No",
    "Don't know": "Don't know",                          # 2014
    "I don't know": "Don't know",                        # 2016+
    "Not eligible for coverage / N/A": "Not eligible",   # 2016
    "Not eligible for coverage / NA": "Not eligible",    # 2017+
}

REMOTE_MAP = {
    "Yes": "Yes",            # 2014
    "No": "No",              # 2014
    "Always": "Yes",         # 2016
    "Never": "No",           # 2016
    "Sometimes": "Sometimes",
}

YES_NO_MAP = {"Yes": True, "No": False}   # 2014's treatment and self_employed


# load one year
def load_year(year):
    """Load one year, keep the 7 columns we need, and clean the answers."""
    df = pd.read_csv(RAW / f"OSMI_{year}.csv")
    df.columns = [c.replace("\xa0", " ") for c in df.columns]  # Step 4 fix

    mapping = COLUMN_MAP[year]
    df = df[list(mapping.keys())]     # keep only the columns we need
    df = df.rename(columns=mapping)   # rename them to the short names

    # Remote work wasn't asked in 2017-2019, so add it as an empty column
    if "remote_work" not in df.columns:
        df["remote_work"] = pd.NA

    # NEW: make the answers match across years
    df["benefits"] = df["benefits"].map(BENEFITS_MAP)
    df["remote_work"] = df["remote_work"].map(REMOTE_MAP)

    if year == 2014:
        df["treatment"] = df["treatment"].map(YES_NO_MAP)
        df["self_employed"] = df["self_employed"].map(YES_NO_MAP)
    else:
        df["treatment"] = df["treatment"].astype(bool)
        df["self_employed"] = df["self_employed"].astype(bool)

    df["year"] = year
    return df


# print the answers for each year
for year in [2014, 2016, 2017, 2018, 2019]:
    df = load_year(year)
    print(f"\n===== {year} =====")
    for col in ["benefits", "supervisor", "remote_work",
                "treatment", "self_employed"]:
        print(col, df[col].value_counts(dropna=False).to_dict())