import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)

st.title("🇮🇳 INDIA Project - Case Processing Status 📋")

# Read Excel
df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)


# Clean Column Names
df.columns = df.columns.str.strip().str.lower()

# Clean Engineer Column
df["first engineer(india team)"] = (
    df["first engineer(india team)"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace("", "Unassigned")
)

# Clean Status Column
df["status"] = (
    df["status"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)


# Convert Date Columns
df["start date"] = pd.to_datetime(
    df["start date"],
    errors="coerce"
)

df["end date"] = pd.to_datetime(
    df["end date"],
    errors="coerce"
)

# Engineer vs Status Analysis
eng_status = (
    df.groupby(
        ["first engineer(india team)", "status"]
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
        "Closed": "green",
        "Open": "red",
        "In Progress": "orange",
        "Pending": "blue",
        "Unknown": "gray"
    }
)

fig_bar.update_traces(textposition="inside")

# Status Pie Chart
status_count = (
    df["status"]
    .value_counts()
    .reset_index()
)

status_count.columns = ["Status", "Count"]

fig_pie = px.pie(
    status_count,
    names="Status",
    values="Count",
    title="Projects by Status"
)

# Show Charts Side by Side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.plotly_chart(fig_pie, use_container_width=True)

# Pending Case Aging Analysis

pending_df = df[
    df["status"].str.lower() == "pending"
].copy()

# Calculate age using today's date
today = pd.Timestamp.today().normalize()

pending_df["case_days"] = (
    today - pending_df["start date"]
).dt.days

# Create Aging Buckets
pending_df["age_bucket"] = pd.cut(
    pending_df["case_days"],
    bins=[-1, 7, 15, float("inf")],
    labels=[
        "0-7 Days",
        "8-15 Days",
        ">15 Days"
    ]
)

pending_summary = (
    pending_df.groupby(
        ["first engineer(india team)", "age_bucket"],
        observed=False
    )
    .size()
    .reset_index(name="count")
)


# Pending Cases Aging Chart
fig_pending = px.bar(
    pending_summary,
    x="first engineer(india team)",
    y="count",
    color="age_bucket",
    text="count",
    barmode="stack",
    title="Pending Cases by Age",
    color_discrete_map={
        "0-7 Days": "green",
        "8-15 Days": "orange",
        ">15 Days": "red"
    }
)

fig_pending.update_traces(textposition="inside")

st.plotly_chart(
    fig_pending,
    use_container_width=True
)


# KPIs
st.markdown("---")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Cases",
        len(df)
    )

with kpi2:
    st.metric(
        "Closed Cases",
        len(df[df["status"].str.lower() == "closed"])
    )

with kpi3:
    st.metric(
        "Pending Cases",
        len(df[df["status"].str.lower() == "pending"])
    )

with kpi4:
    st.metric(
        "Unassigned Cases",
        len(
            df[
                df["first engineer(india team)"]
                == "Unassigned"
            ]
        )
    )
