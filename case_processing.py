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
    sheet_name="CASE processing",
    
)
st.dataframe(df)

# Clean Column Names
df.columns = df.columns.str.strip().str.lower()

# Required Columns
required_columns = [
    "project code",
    "project name",
    "first enginner(india team)",
    "Second engineer(china team) ",
    "priority",
    "start date",
    "end time",
    "Status"
]

eng1_count = df["first engineer"].value_counts().reset_index()
eng1_count.columns = ["engineer", "Project code"]

fig = px.bar(
    eng1_count,
    x="engineer",
    y="Project code",
    title="Projects Assigned to First Engineer"
)

st.plotly_chart(fig, use_container_width=True)
