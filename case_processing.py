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



# Year and Month Filters

# Extract Year and Month
df["year"] = df["start date"].dt.year
df["month"] = df["start date"].dt.month
df["month_name"] = df["start date"].dt.strftime("%B")

# Select Year
years = sorted(
    df["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

# Available months for selected year
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

# Filter Data
filtered_df = df[
    (df["year"] == selected_year) &
    (df["month_name"] == selected_month)
].copy()

# Engineer vs Status 
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
    title="Cases by Engineer and Status 📊",
    color_discrete_map={
        "Closed": "blue",
        "Pending": "orange",
        "In Progress": "green",
        "Unassigned": "red"
    }
)

fig_bar.update_traces(
    textposition="inside"
)

# Clean Priority Column
df["priority"] = (
    df["priority"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# Priority Pie Chart
priority_count = (
    df["priority"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .value_counts()
    .reset_index()
)

priority_count.columns = [
    "Priority",
    "Count"
]




st.subheader(
    f"📅 Ticket Status - {selected_month} {selected_year}"
)

status_summary = (
    filtered_df.groupby("status")
    .size()
    .reset_index(name="Count")
)

fig_month = px.bar(
    status_summary,
    x="status",
    y="Count",
    color="status",
    text="Count",
    title=f"Ticket Status - {selected_month} {selected_year}"
)

fig_month.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

    fig2 = px.bar(
        monthly_status,
        x="Month",
        y="Count",
        color="Status Group",
        barmode="group",
        title=f"Open vs Closed Tickets - {selected_year}"
    )

    st.plotly_chart(fig2, use_container_width=True)

fig_pie = px.pie(
    priority_count,
    names="Priority",
    values="Count",
    title="Projects by Priority",
    color="Priority",
    color_discrete_map={
        "High": "red",
        "Medium": "orange",
        "Low": "green",
        
    }
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label"
)


# Show Side by Side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# Pending Cases Aging Analysis

# Cases where End Time is blank
pending_df = df[df["end time"].isna()].copy()

# Age calculation
today = pd.Timestamp.today().normalize()

pending_df["case_days"] = (
    today - pending_df["start date"]
).dt.days

# Buckets
pending_df["age_bucket"] = pd.cut(
    pending_df["case_days"],
    bins=[-1, 7, 15, float("inf")],
    labels=[
        "0-7 Days",
        "8-15 Days",
        ">15 Days"
    ]
)

# Engineer + Bucket summary
pending_summary = (
    pending_df.groupby(
        ["first engineer(india team)", "age_bucket"],
        observed=False
    )
    .size()
    .reset_index(name="count")
)

# Remove zero counts
pending_summary = pending_summary[
    pending_summary["count"] > 0
]

# Chart
fig_pending = px.bar(
    pending_summary,
    x="first engineer(india team)",
    y="count",
    color="age_bucket",
    text="count",
    barmode="stack",
    title="Pending cases ",
    color_discrete_map={
        "0-7 Days": "green",
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


# Optional Data Preview
with st.expander("View Raw Data"):
    st.dataframe(df)
