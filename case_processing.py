import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)

# Title
st.title("🇮🇳 INDIA Project - Case Processing Status 📋")

# Read Excel
df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

df["first engineer(india team)"] = (
    df["first engineer(india team)"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["first engineer(india team)"] = df["first engineer(india team)"].replace(
    "", "Unassigned"
)


df["status"] = (
    df["status"]
    .fillna("Unknown")
)

# Count cases by Engineer and Status
eng_status = (
    df.groupby(
        ["first engineer(india team)", "status"]
    )
    .size()
    .reset_index(name="count")
)

# Stacked Bar
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
        "Open": "purple",
        "In Progress": "green",
        "Pending": "yellow",
        "Unassigned": "red"
    }
)

# Status Count
status_count = (
    df["status"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

status_count.columns = ["Status", "Count"]

# Pie Chart
fig_pie= px.pie(
    status_count,
    names="Status",
    values="Count",
    title="Projects by Status"
)


# Display side-by-side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.plotly_chart(fig_pie, use_container_width=True)
