import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#add image
st.image("envision.png")

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
    .astype("string")
    .str.strip()
)

df["status"] = (
    df["status"]
    .fillna("Ticket Status Unassigned")
    .astype(str)
    .str.strip()
    .replace(
        ["", "nan", "None"],
        "Ticket Status Unassigned"
    )
)

df["priority"] = (
    df["priority"]
    .fillna("Ticket Status Unassigned")
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

# YEARLY STATUS BREAKDOWN

year_status_summary = (
    engineer_year_df
    .groupby("status")
    .size()
    .reset_index(name="count")
)

fig_year_status = px.bar(
    year_status_summary,
    x="status",
    y="count",
    color="status",
    text="count",
    title=f"{selected_engineer} - {current_year} Status Breakdown"
)

fig_year_status.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_year_status,
    use_container_width=True
)

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

engineer_df = filtered_df.copy()

# Keep engineer name as engineer
engineer_df["first engineer(india team)"] = (
    engineer_df["first engineer(india team)"]
    .astype("string")
    .str.strip()
)

# Keep Ticket Status Unassigned ONLY in STATUS
engineer_df["status"] = (
    engineer_df["status"]
    .fillna("Ticket Status Unassigned")
    .astype(str)
    .str.strip()
    .replace(
        ["", "nan", "None"],
        "Ticket Status Unassigned"
    )
)

# Remove rows that genuinely have no engineer
# This prevents a separate "Unassigned" engineer bar
engineer_df = engineer_df[
    engineer_df["first engineer(india team)"].notna() &
    (engineer_df["first engineer(india team)"] != "") &
    (~engineer_df["first engineer(india team)"].isin(
        ["nan", "None", "Ticket Status Unassigned"]
    ))
]

# Group by ENGINEER + STATUS
eng_status = (
    engineer_df
    .groupby(
        ["first engineer(india team)", "status"],
        dropna=False
    )
    .size()
    .reset_index(name="count")
)

# STACKED BAR
fig_bar = px.bar(
    eng_status,
    x="first engineer(india team)",
    y="count",
    color="status",
    text="count",
    barmode="stack",
    title="Cases by Engineer and Status",
    color_discrete_map={
        "Closed": "blue",
        "Ongoing": "green",
        "Pending on Infra": "orange",
        "Pending on Manufactures": "yellow",
        "Pending on Universe": "orange",
        "Not Started": "pink",
        "Ticket Status Unassigned": "black"
    }
)

fig_bar.update_traces(
    textposition="inside"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )
    
# ============================================================
# ENGINEER YEARLY PERFORMANCE - CURRENT YEAR
# ============================================================

st.subheader("👨‍💻 Engineer Yearly Performance")

# Current calendar year
current_year = datetime.now().year

# All cases from January 1 until today
current_year_df = df[
    (df["year"] == current_year) &
    (df["effective_date"] <= pd.Timestamp.today())
].copy()

# Engineer list
engineer_list = sorted(
    current_year_df[
        current_year_df["first engineer(india team)"].notna()
    ]["first engineer(india team)"]
    .astype(str)
    .str.strip()
    .loc[lambda x: ~x.isin(["", "nan", "None", "Ticket Status Unassigned"])]
    .unique()
)

# Engineer selection
selected_engineer = st.selectbox(
    "Select Engineer",
    engineer_list,
    key="yearly_engineer"
)

# Selected engineer data
engineer_year_df = current_year_df[
    current_year_df["first engineer(india team)"]
    .astype(str)
    .str.strip()
    == selected_engineer
].copy()

# Status counts
year_total = len(engineer_year_df)

year_closed = len(
    engineer_year_df[
        engineer_year_df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "closed"
    ]
)

year_ongoing = len(
    engineer_year_df[
        engineer_year_df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "ongoing"
    ]
)

year_infra = len(
    engineer_year_df[
        engineer_year_df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "pending on infra"
    ]
)

year_manufactures = len(
    engineer_year_df[
        engineer_year_df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "pending on manufactures"
    ]
)

year_unassigned = len(
    engineer_year_df[
        engineer_year_df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "ticket status unassigned"
    ]
)

# Closure percentage
year_closure_rate = (
    (year_closed / year_total) * 100
    if year_total > 0
    else 0
)

# KPI cards
k1, k2, k3, k4, k5, k6, k7 = st.columns(7)

with k1:
    st.metric(
        "📋 Total Cases",
        year_total
    )

with k2:
    st.metric(
        "✅ Closed",
        year_closed
    )

with k3:
    st.metric(
        "🔄 Ongoing",
        year_ongoing
    )

with k4:
    st.metric(
        "🏭 Pending Infra",
        year_infra
    )

with k5:
    st.metric(
        "🏭 Pending Mfg",
        year_manufactures
    )

with k6:
    st.metric(
        "⚠️ Unassigned",
        year_unassigned
    )

with k7:
    st.metric(
        "📈 Closure %",
        f"{year_closure_rate:.1f}%"
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
