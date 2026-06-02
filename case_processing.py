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
        "Project Code",
        "Project name",
        "First enginner(India Team)",
        "Second engineer(China Team) ",
        "Priority",
        "start date",
        "end time",
        "Status"
    ]
