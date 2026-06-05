import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG
st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)

st.title("🇮🇳 INDIA Project - Case Processing Status 📋")

# LOAD EXCEL
df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)


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

df["end time"] = pd.to_datetime(
    df["end time"],
    errors="coerce"
)


# YEAR / MONTH FILTERS
df["year"] = df["start date"].dt.year
df["month"] = df["start date"].dt.month
df["month_name"] = df["start date"].dt.strftime("%B")

years = sorted(
    df["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

available_months = (
    df[df["year"] == selected_year]
    .sort_values("month")
    ["month_name"]
    .unique()
)

selected_month = st.sidebar.selectbox(
    "Select Month",
    available_months
)

filtered_df = df[
    (df["year"] == selected_year) &
    (df["month_name"] == selected_month)
].copy()


# KPI METRICS (All Data)

st.subheader("📊 Overall Project Summary")

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

c1.metric("📋 Total Cases", total_cases)
c2.metric("⏳ Pending Cases", pending_cases)
c3.metric("✅ Closed Cases", closed_cases)


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
    "Pending from Universe":"yellow",
    
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
    df["end time"].isna()
].copy()

today = pd.Timestamp.today().normalize()

pending_df["case_days"] = (
    today - pending_df["start date"]
).dt.days

pending_df["age_bucket"] = pd.cut(
    pending_df["case_days"],
    bins=[-1, 7, 15, float("inf")],
    labels=[
        "0-7 Days",
        "8-15 Days",
        ">15 Days"
    ]
)

pending_df["age_bucket"] = (
    pending_df["age_bucket"]
    .cat.add_categories(["Start Date Missing"])
    .fillna("Start Date Missing")
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

