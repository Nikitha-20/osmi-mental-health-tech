"""Step 6 -- The benefits chart, before and after the Week 5 redesign.

Before: six bars covering three questions, a vague label, 0-100 scale.
After: one comparison (benefits Yes vs No), the unit spelled out,
a 0-80 axis that still starts at zero, and a headline stating the claim.

All bar heights are calculated from the data, not typed in.

"""

import matplotlib
matplotlib.use("Agg")   # save charts to files; no pop-up window
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from pathlib import Path  # noqa: E402

PROJECT = Path(__file__).resolve().parent.parent
FIGURES = PROJECT / "figures"
FIGURES.mkdir(exist_ok=True)

df = pd.read_csv(PROJECT / "data" / "processed" / "analysis_sample.csv")
remote = df[df["year"].isin([2014, 2016])]   # remote work: 2 years only


def pct(data, factor, group):
    """% of people in one group who have ever sought treatment."""
    rate = data.loc[data[factor] == group, "treatment"].mean() * 100
    return round(float(rate), 1)


# ---------- BEFORE: six bars, three questions ----------
labels = ["Benefits\nYes", "Benefits\nNo", "Supervisor\nYes",
          "Supervisor\nNo", "Remote\nYes", "Remote\nNo"]
values = [pct(df, "benefits", "Yes"), pct(df, "benefits", "No"),
          pct(df, "supervisor", "Yes"), pct(df, "supervisor", "No"),
          pct(remote, "remote_work", "Yes"),
          pct(remote, "remote_work", "No")]

fig, ax = plt.subplots(figsize=(7, 4.2))
ax.bar(labels, values, color=["#4C72B0"] * 2 + ["#9A9A9A"] * 4)
ax.set_ylim(0, 100)
ax.set_ylabel("% who sought treatment")
ax.set_title("Treatment-Seeking by Workplace Factors")
fig.tight_layout()
fig.savefig(FIGURES / "benefits_chart_before.png", dpi=150)
plt.close(fig)
print("Before chart:", dict(zip([lab.replace("\n", " ") for lab in labels],
                                values)))

# ---------- AFTER: one focused comparison ----------
yes = pct(df, "benefits", "Yes")
no = pct(df, "benefits", "No")

fig, ax = plt.subplots(figsize=(7, 4.2))
bars = ax.bar(["Yes", "No"], [yes, no], color=["#4C72B0", "#B0B0B0"],
              width=0.5)
ax.set_ylim(0, 80)   # still starts at zero; nothing goes above 68%
ax.set_ylabel("% who have ever sought treatment")
ax.set_xlabel("Employer provides mental health benefits")
ax.set_title("Employees with mental health benefits are far more\n"
             "likely to have sought treatment",
             fontsize=11, fontweight="bold")
for bar, value in zip(bars, [yes, no]):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1.2, f"{value}%",
            ha="center", fontsize=11, fontweight="bold")
fig.tight_layout()
fig.savefig(FIGURES / "benefits_chart_after.png", dpi=150)
plt.close(fig)
print("After chart:", {"Benefits Yes": yes, "Benefits No": no})
print("Saved both charts in the figures folder")