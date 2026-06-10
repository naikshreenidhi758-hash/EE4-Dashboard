import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service Dashboard",
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

# CLEAN COMPANY COLUMN
df["company"] = (
    df["company"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

# DEBUG SECTION
st.subheader("Infra EE4 Cases")

company_counts = df["company"].value_counts()

st.dataframe(company_counts)

# COUNT INFRA AND UNIVERSE
infra_count = len(
    df[df["company"].str.contains("infra", na=False)]
)

universe_count = len(
    df[df["company"].str.contains("universe", na=False)]
)

# KPI CARDS
col1, col2 = st.columns(2)

with col1:
    st.metric("Infra Cases", infra_count)

with col2:
    st.metric("Universe Cases", universe_count)

# PIE CHART DATA
team_summary = pd.DataFrame({
    "Team": ["Infra", "Universe"],
    "Count": [infra_count, universe_count]
})

# PIE CHART
fig = px.pie(
    team_summary,
    names="Team",
    values="Count",
    title="Infra vs Universe Case Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
