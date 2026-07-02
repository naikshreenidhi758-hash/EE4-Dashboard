import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# PAGE CONFIG
st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)

st.title("INDIA Project - Case Processing Status 📋")

# LOAD EXCEL
df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)

df.columns = df.columns.str.strip()

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower()


# CLEAN DATA
df["first engineer(india team)"] = (
    df["first engineer(india team)"]
    .fillna("Unassigned")
    .astype(str)
    .str.strip()
)

df["status"] = (
    df["status"]
    .fillna("Unassigned")
    .astype(str)
    .str.strip()
)

df["priority"] = (
    df["priority"]
    .fillna("Unassigned")
    .astype(str)
    .str.strip()
    .str.title()
)

# DATE CONVERSION
df["start date"] = pd.to_datetime(
    df["start date"],
    errors="coerce"
)

df["filled_date"] = pd.to_datetime(
    df["filled_date"],
    errors="coerce"
)

df["end time"] = pd.to_datetime(
    df["end time"],
    errors="coerce"
)

# Use start date if available, otherwise filled date
df["effective_date"] = df["start date"].fillna(df["filled_date"])
# YEAR
df["year"] = df["effective_date"].dt.year

# MONTH
df["month"] = df["effective_date"].dt.month

# MONTH NAME
df["month_name"] = df["effective_date"].dt.strftime("%B")

# WEEK NUMBER
df["week_no"] = (
    df["effective_date"]
    .dt.isocalendar()
    .week
    .astype("Int64")
)

# WEEK NAME
df["week_name"] = "Week " + df["week_no"].astype(str)


# YEAR / MONTH / WEEK FILTER

df["year"] = df["effective_date"].dt.year

df["month"] = df["effective_date"].dt.month

df["month_name"] = df["effective_date"].dt.strftime("%B")

df["week_no"] = (
    df["effective_date"]
    .dt.isocalendar()
    .week
    .astype("Int64")
)

df["week_name"] = "Week " + df["week_no"].astype(str)
# YEAR

years = sorted(
    df["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)


# MONTH

available_months = (
    df[df["year"] == selected_year]
    .sort_values("month")["month_name"]
    .unique()
)

from datetime import datetime

current_month = datetime.now().strftime("%B")

if current_month in available_months:
    default_month_index = list(available_months).index(current_month)
else:
    default_month_index = 0

selected_month = st.sidebar.selectbox(
    "Select Month",
    available_months,
    index=default_month_index
)


# WEEK
available_weeks = (
    df[
        (df["year"] == selected_year) &
        (df["month_name"] == selected_month)
    ]
    .sort_values("week_no")["week_name"]
    .unique()
)

week_options = ["All Weeks"] + list(available_weeks)

selected_week = st.sidebar.selectbox(
    "Select Week",
    week_options
)


# FILTER DATA

filtered_df = df[
    (df["year"] == selected_year) &
    (df["month_name"] == selected_month)
].copy()

if selected_week != "All Weeks":
    filtered_df = filtered_df[
        filtered_df["week_name"] == selected_week
    ]

# KPI METRICS
total_cases = len(df)

closed_cases = len(
    df[
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("closed")
    ]
)

pending_cases = total_cases - closed_cases

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("📋 Total Cases", total_cases)

with c2:
    st.metric("⏳ Pending Cases", pending_cases)

with st.expander(f"View All {pending_cases} Pending Cases"):
    pending_case_list = df[
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .ne("closed")
    ]

    st.dataframe(
        pending_case_list,
        use_container_width=True
    )

with c3:
    st.metric("✅ Closed Cases", closed_cases)
    
# STATUS CHART
status_summary = (
    df.groupby("status")
    .size()
    .reset_index(name="Count")
)

fig_status = px.bar(
    status_summary,
    x="status",
    y="Count",
    color="status",
    text="Count",
    title="Overall Ticket Status"
)

fig_status.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)

# ENGINEER VS STATUS
# Clean engineer column
filtered_df["first engineer(india team)"] = (
    filtered_df["first engineer(india team)"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Replace empty strings and 'nan' strings
filtered_df["first engineer(india team)"] = filtered_df[
    "first engineer(india team)"
].replace(["", "nan", "None"], "Unassigned")


filtered_df["first engineer(india team)"] = (
    filtered_df["first engineer(india team)"]
    .fillna("")
    .astype(str)
    .str.strip()
)

filtered_df.loc[
    filtered_df["first engineer(india team)"] == "",
    "first engineer(india team)"
] = "Unassigned"

eng_status = (
    filtered_df.groupby(
        ["first engineer(india team)", "status"],
        dropna=False
    )
    .size()
    .reset_index(name="count")
)

fig_bar = px.bar(
    eng_status,
    x="first engineer(india team)",
    y="count",
    color="status",
    text="count",
    barmode="stack",
    title="Cases by Engineer and Status",
    color_discrete_map={
    "Closed":"blue",
    "Ongoing":"green",
    "Pending on Manufactures":"orange",
    "Pending on Universe":"yellow",
    "Not Started":"pink", 
     "Blank":"black",   
    
}
)

fig_bar.update_traces(
    textposition="inside"
)

# SIDE BY SIDE CHARTS
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# PENDING AGING ANALYSIS (Overall Data)
pending_df = df[
    (df["end time"].isna()) &
    (
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower() != "closed"
    )
].copy()

pending_df["effective_start_date"] = (
    pending_df["start date"]
    .fillna(pending_df["filled_date"])
)

today = pd.Timestamp.today().normalize()

pending_df["case_days"] = (
    today - pending_df["effective_start_date"]
).dt.days


pending_df["age_bucket"] = np.select(
    [
        pending_df["case_days"] <= 7,
        pending_df["case_days"].between(8, 15),
        pending_df["case_days"] > 15
    ],
    [
        "0-7 Days",
        "8-15 Days",
        ">15 Days"
    ],
    default="Unknown"
)

pending_summary = (
    pending_df.groupby(
        ["first engineer(india team)", "age_bucket"],
        observed=False
    )
    .size()
    .reset_index(name="count")
)

pending_summary = pending_summary[
    pending_summary["count"] > 0
]

fig_pending = px.bar(
    pending_summary,
    x="first engineer(india team)",
    y="count",
    color="age_bucket",
    text="count",
    barmode="stack",
    title="Overall Pending Cases Aging Analysis",
    color_discrete_map={
        "0-7 Days": "blue",
        "8-15 Days": "orange",
        ">15 Days": "red"
    }
)

fig_pending.update_traces(
    textposition="inside"
)

st.plotly_chart(
    fig_pending,
    use_container_width=True
)
