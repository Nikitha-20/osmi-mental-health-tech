import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
st.set_page_config(page_title="Mental Health Coverage Dashboard")

st.title("What Gets Tech Workers to Seek Mental Health Help")
st.write("OSMI Mental Health in Tech Survey, 2014-2019")
st.info("**Recommendation for HR:** fund mental health coverage, and make sure employees know they have it.")

df = pd.read_csv("data/processed/analysis_sample.csv")

# ---- Sidebar filter ----
st.sidebar.header("Filters")
all_years = sorted(df["year"].unique())
chosen_years = st.sidebar.multiselect("Survey year", all_years, default=all_years)

filtered = df[df["year"].isin(chosen_years)]

if filtered.empty:
    st.warning("Pick at least one survey year in the sidebar.")
    st.stop()

# ---- Key numbers ----
rate = filtered.groupby("benefits")["treatment"].mean() * 100
gap = rate["Yes"] - rate["No"]
dont_know_share = (filtered["benefits"] == "Don't know").mean() * 100

col1, col2, col3 = st.columns(3)
col1.metric("Employees", f"{len(filtered):,}")
col2.metric("Coverage gap", f"{gap:.1f} points")
col3.metric("Don't know if covered", f"{dont_know_share:.0f}%")

# ---- Chart 1: coverage ----
st.subheader("Employees who don't know their coverage are the least likely to seek help")

groups = ["Yes", "No", "Don't know"]
labels = ["Has coverage", "No coverage", "Don't know"]
colors = ["#2E83C3", "#A6A6A6", "#2C3C43"]
values = [rate[g] for g in groups]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(labels, values, color=colors)
ax.bar_label(bars, fmt="%.1f%%", fontweight="bold")
ax.set_ylim(0, 80)
ax.set_ylabel("% who have ever sought treatment")
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)

# ---- Chart 2: gap by year ----
st.subheader("The coverage gap appears in every survey year")

by_year = (filtered[filtered["benefits"].isin(["Yes", "No"])]
           .groupby(["year", "benefits"])["treatment"].mean()
           .unstack() * 100)
by_year = by_year[["Yes", "No"]]
by_year.columns = ["Has coverage", "No coverage"]

fig2, ax2 = plt.subplots(figsize=(7, 4))
by_year.plot(kind="bar", ax=ax2, color=["#2E83C3", "#A6A6A6"], rot=0, width=0.75)
for container in ax2.containers:
    ax2.bar_label(container, fmt="%.1f", fontsize=8)
ax2.set_ylim(0, 80)
ax2.set_xlabel("")
ax2.set_ylabel("% who have ever sought treatment")
ax2.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.08))
ax2.spines[["top", "right"]].set_visible(False)
fig2.tight_layout()
st.pyplot(fig2)

# ---- Notes ----
st.divider()
st.caption(
    "How to read this: each bar is the % of employees in that group who have ever sought "
    "treatment from a mental health professional. This is survey data, so it shows a "
    "connection, not proof that coverage causes help-seeking. Self-employed respondents are "
    "excluded because the questions ask about an employer."
)
st.caption("Source: OSMI Mental Health in Tech Survey (2014, 2016-2019). Analysis by Nikitha Reddy Singu, MSDS 692.")