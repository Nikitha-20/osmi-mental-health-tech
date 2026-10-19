# What Gets Tech Workers to Actually Seek Mental Health Help

MSDS 692 Data Science Practicum · Regis University · Fall 2026

**Live dashboard:** https://osmi-mental-health-tech.streamlit.app

**Recommendation for HR:** fund mental health coverage for tech workers, and make sure employees know they have it. Of the three workplace factors HR controls, coverage is the only one tied to who actually seeks help.

| | Sought treatment |
|---|---|
| Employees **with** mental health coverage | **67.9%** (1,170 of 1,723) |
| Employees **without** coverage | **48.2%** (318 of 660) |
| Employees who **don't know** if they're covered | **42.7%** (442 of 1,036), about 29% of everyone |

The gap between "with" and "without" is **19.7 points**, and it shows up in every survey year. Manager support (spread 6.1 points) and remote work (spread 7.7 points) barely change the rate.

---

## How to run it

You need Python 3. From the project folder:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python run_all.py                  # raw data → cleaned data → results → charts
streamlit run app.py               # opens the interactive dashboard
```

`run_all.py` runs the six scripts in `src/` in order and prints every number used in the presentation. Running it on a fresh clone gives the same results each time. The model comparison uses fixed random seeds.

## What's in the repo

```
data/raw/            OSMI survey files, 2014 and 2016–2019 (as downloaded)
data/processed/      combined_clean.csv (all employees + self-employed, 4,216 rows)
                     analysis_sample.csv (employees only, 3,567 rows)
src/
  01_clean_and_merge.py        match column names across years, clean answers, combine
  02_check_self_employed.py    why some coverage answers are blank
  03_exploratory_analysis.py   % who sought help in each group, overall and by year
  04_logistic_regression.py    odds ratios with 95% ranges (Models A and B)
  05_compare_models.py         logistic regression vs Random Forest on unseen data
  06_charts.py                 the coverage chart, before and after the Week 5 redesign
exploration/         earlier step-by-step scripts from Weeks 1–3 (kept for the record)
figures/             charts saved by 06_charts.py
app.py               Streamlit dashboard for HR (filter by survey year)
run_all.py           runs everything in src/ in order
```

---

## Defensible Analysis: the five checks

### 1. How I framed the problem

**Stakeholder:** an HR leader at a tech company deciding where to spend a limited wellness budget.

**Question:** Which of the three workplace factors HR can actually change — mental health coverage, manager support, or remote work — is tied to employees seeking professional mental health help?

**Outcome:** the survey question "Have you ever sought treatment for a mental health issue from a mental health professional?" (yes/no).

I picked these three because HR can change them. Factors like age, gender or country matter, but HR can't change them, so they're out of scope.

### 2. Whether the data fits the question

**Source:** [OSMI Mental Health in Tech Survey](https://osmihelp.org/research), an anonymous yearly survey of people working in tech.

**Years used:** 2014, 2016, 2017, 2018 and 2019. These are the years where the coverage, manager and treatment questions can be matched across files. No 2015 survey file was available. The question wording changed slightly between years (for example "disorder" vs "issue"), and `01_clean_and_merge.py` maps each year's wording to one short column name.

**Cleaning, step by step:**

| Step | Rows |
|---|---|
| Raw responses, five years | 4,217 |
| Removed 1 joke response | 4,216 |
| Removed self-employed people | −649 |
| **Analysis sample (employees)** | **3,567** |

**Why I removed self-employed people:** the questions ask about *your employer*. `02_check_self_employed.py` shows that all 504 blank coverage answers came from self-employed people. The survey skipped them because they have no employer. In 2014 the survey didn't skip them, but the question still doesn't apply to them.

**"Not eligible" (148 people)** is a different group: employees who aren't on their employer's plan. None of them are self-employed. They stay in the data and the models, but they aren't on the main chart.

**Remote work** was only asked in 2014 and 2016, so it's tested separately on those two years (2,259 people).

### 3. Why this method

**First, simple comparisons** (`03_exploratory_analysis.py`): the % who sought help in each answer group. If a factor shows no gap here, a model is unlikely to find one.

**Then logistic regression** (`04_logistic_regression.py`, statsmodels). The outcome is yes/no, and logistic regression gives HR a plain number for each factor: an **odds ratio** with a 95% range. An odds ratio of 1 means no effect. I used statsmodels without regularization so the odds ratios aren't shrunk toward 1.

- **Model A** (all five years): coverage + manager support
- **Model B** (2014 and 2016): coverage + manager support + remote work

**Compared with a Random Forest** (`05_compare_models.py`) on data the models hadn't seen: 80/20 split, stratified, repeated over 20 random splits.

| Approach | Accuracy on unseen data (average of 20 splits) |
|---|---|
| Always guess "yes" (most common answer) | 56.7% |
| Logistic regression | 60.6% |
| Random Forest | 60.9% |

The two models are almost equally accurate. The gap ranges from −1.5 to +2.1 points depending on the split. One split alone (seed 42) showed 59.4% vs 61.5%, which made the gap look bigger than it is. I kept logistic regression because it's just as accurate and it can say *how much* each factor matters. Random Forest settings were left at the defaults (`random_state=42`) with the usual 0.5 cut-off. This comparison checks whether a simpler model is giving up accuracy. It isn't tuned to get the best possible prediction.

### 4. Whether the conclusions hold

**Odds ratios (Model A, all five years, n = 3,567):**

| Compared with "Don't know" coverage | Odds ratio | 95% range |
|---|---|---|
| Coverage: Yes | 2.85 | 2.43 – 3.35 |
| Coverage: No | 1.25 | 1.02 – 1.52 |
| **Coverage Yes vs No** | **≈ 2.3** | |
| Manager support groups (vs "Maybe") | 0.86 – 1.06 | all ranges include 1 |

In Model B, where remote work is added for 2014 and 2016, coverage stays strong (Yes vs Don't know: 2.66, range 2.18 – 3.25). Remote work is small: "Sometimes" is 1.27 (1.02 – 1.58), and "Yes" is 1.11 (0.90 – 1.39), which includes 1.

**The gap holds in every year, not just when years are pooled:**

| Year | With coverage | Without | Gap |
|---|---|---|---|
| 2014 | 64.3% | 45.9% | 18.4 |
| 2016 | 66.3% | 48.8% | 17.5 |
| 2017 | 69.4% | 42.9% | 26.5 |
| 2018 | 72.3% | 61.9% | 10.4 |
| 2019 | 74.4% | 60.0% | 14.4 |

The "without coverage" groups are small in 2018 (42 people) and 2019 (35), so those years move around more. The direction never changes.

**Limits — what this can't tell you:**

- **Connection, not cause.** People who already need help may be the ones who look up their coverage, or choose employers that offer it. The next step is a test: promote coverage to one group, not another, and compare after a year.
- **People chose to take the survey.** They may care more about mental health than the average tech worker.
- **Older data.** The data runs from 2014 to 2019, before COVID changed how people work. Remote work was only asked in two of those years.
- **"Ever sought treatment"** covers someone's whole life, not just their current job.
- **The models predict individuals only a little better than guessing** (about 4 points). The recommendation rests on the gap between *groups*, which is large and steady across years. It doesn't rest on predicting any one person.

### 5. Whether it reproduces

- Raw data is in the repo exactly as downloaded, and every processed file is rebuilt from it by `python run_all.py`.
- Every number in this README and in the presentation is printed by a script in `src/`. None are typed in by hand. Chart bar heights are calculated from the data.
- Random splits use fixed seeds (0–19, plus 42 for the single split), so results match on every run.
- Package list: `requirements.txt`.

---

## Dashboard

**Live app:** https://osmi-mental-health-tech.streamlit.app

No install needed. Open the link in a browser. To run it on your own computer instead, `streamlit run app.py` opens a dashboard where HR can filter by survey year and see the coverage gap, manager support and remote work rates.

## Use of AI tools

I used Claude (Anthropic) during this project for help with code, analysis and slides, and to draft this README. I documented that work every week in my LLM collaboration log. I ran every script in this repo myself, and the numbers above come from those runs.

## Data credit

Open Sourcing Mental Health (OSMI), *Mental Health in Tech Survey*, 2014 and 2016–2019. https://osmihelp.org/research
