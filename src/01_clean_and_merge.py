import pandas as pd
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
RAW = PROJECT / "data" / "raw"

# ---------- Part 1: the question texts that change between years ----------
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

# ---------- Part 2: column names per year -> short names ----------
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

# ---------- Part 3 (NEW): answer translation tables ----------
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

MALE = {"m", "male", "man", "cis male", "cis man", "make", "malr", "mail",
        "maile", "msle", "male-ish", "male (cis)", "guy (-ish) ^_^",
        "cis-male", "malef", "male leaning androgynous"}
FEMALE = {"f", "female", "woman", "cis female", "cis-female/femme",
          "female (cis)", "femake", "femail", "cis woman"}


def clean_gender(answer):
    """Turn one free-text gender answer into Male/Female/Non-binary/Other."""
    if pd.isna(answer):
        return pd.NA
    text = str(answer).strip().lower()
    if text in MALE:
        return "Male"
    if text in FEMALE:
        return "Female"
    return "Non-binary/Other"


# ---------- Part 4: load one year ----------
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

        # remove the 2014 joke entry (gender answer "A little about you")
    if year == 2014:
        joke = df["gender"].astype(str).str.contains(
            "a little about you", case=False)
        print("Joke rows removed:", int(joke.sum()))
        df = df[~joke]

        #fix ages -- keep the person, blank out impossible ages
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    bad_age = (df["age"] < 18) | (df["age"] > 75)
    print("Impossible ages blanked:", int(bad_age.sum()))
    df.loc[bad_age, "age"] = pd.NA

    #group gender
    df["gender"] = df["gender"].map(clean_gender)

    df["year"] = year
    return df

# ---------- Part 5 (CHANGED): stack, save, remove self-employed ----------
PROCESSED = PROJECT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)   # create the folder if needed

# 1. Load every year and stack them into one table
all_years = [load_year(year) for year in [2014, 2016, 2017, 2018, 2019]]
combined = pd.concat(all_years, ignore_index=True)

print("\nCombined table:", combined.shape)
print("Rows per year:", combined["year"].value_counts().sort_index().to_dict())

# 2. Save everyone
combined.to_csv(PROCESSED / "combined_clean.csv", index=False)
print("Saved data/processed/combined_clean.csv")

# 3. Remove self-employed people (they have no employer offering benefits)
is_self = combined["self_employed"] == True   # noqa: E712
print("\nSelf-employed removed:", int(is_self.sum()))
print("By year:", combined.loc[is_self, "year"].value_counts()
      .sort_index().to_dict())

analysis = combined[~is_self]
print("Rows left for analysis:", len(analysis))

analysis.to_csv(PROCESSED / "analysis_sample.csv", index=False)
print("Saved data/processed/analysis_sample.csv")

