import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
RAW = PROJECT / "data" / "raw"

# The question texts that change between years
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

# For each year: changing original column name to short name we want
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


def load_year(year):
    """Load one year, keep only the 7 columns we need, with short names."""
    df = pd.read_csv(RAW / f"OSMI_{year}.csv")
    df.columns = [c.replace("\xa0", " ") for c in df.columns]  # Step 4 fix

    mapping = COLUMN_MAP[year]
    df = df[list(mapping.keys())]     # keep only the columns we need
    df = df.rename(columns=mapping)   # rename them to the short names

    # Remote work wasn't asked in 2017-2019, so add it as an empty column
    if "remote_work" not in df.columns:
        df["remote_work"] = pd.NA

    df["year"] = year
    return df


for year in [2014, 2016, 2017, 2018, 2019]:
    df = load_year(year)
    print(year, df.shape, list(df.columns))