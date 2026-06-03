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
    .fillna("Unassigned")
)

eng1_count = (
    df["first engineer(india team)"]
    .value_counts()
    .reset_index()
)

eng1_count.columns = ["engineer", "project_count"]

# Bar Chart
fig = px.bar(
    eng1_count,
    x="engineer",
    y="project_count",
    title="Projects Assigned to First Engineer",
    text="project_count"
)

st.plotly_chart(fig, use_container_width=True)
