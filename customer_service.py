import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service",
    layout="wide"
)

st.title("Infra vs Universe Cases")

# LOAD EXCEL
df = pd.read_excel(
    "sn_customerservice_case.xlsx",
    sheet_name="Infra EE4 Cases"
)

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower()

df["company"] = (
    df["company"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.lower()
)

infra_count = len(df[df["company"] == "infra"])
universe_count = len(df[df["company"] == "universe"])

# COUNT CASES
company_summary = (
    df["company"]
    .value_counts()
    .reset_index()
)

company_summary.columns = ["Company", "Count"]

# KPI Metrics
col1, col2 = st.columns(2)

infra_count = len(df[df["company"] == "Infra"])
universe_count = len(df[df["company"] == "Universe"])

with col1:
    st.metric("Infra Cases", infra_count)

with col2:
    st.metric("Universe Cases", universe_count)

# PIE CHART
fig = px.pie(
    company_summary,
    names="Company",
    values="Count",
    title="Infra vs Universe Distribution"
)

st.plotly_chart(fig, use_container_width=True)
