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

# SECOND SHEET
df_sheet2 = pd.read_excel(
    "sn_customerservice_case.xlsx",
    sheet_name="Enos Public IP issue"
)

# CLEAN COLUMN NAMES
df_sheet2.columns = df_sheet2.columns.str.strip().str.lower()

# CLEAN VALUES
df_sheet2["infra dependecies"] = (
    df_sheet2["infra dependecies"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

# COUNTS
infra_count = len(
    df_sheet2[
        df_sheet2["infra dependecies"] == "yes"
    ]
)

universe_count = len(
    df_sheet2[
        df_sheet2["infra dependecies"] == "no"
    ]
)

# SUMMARY DATAFRAME
sheet2_summary = pd.DataFrame({
    "Team": ["Infra", "Universe"],
    "Count": [infra_count, universe_count]
})

# PIE CHART
fig2 = px.pie(
    sheet2_summary,
    names="Team",
    values="Count",
    title="Enos Public IP Issue - Infra vs Universe"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
# THIRD SHEET
df_sheet3 = pd.read_excel(
    "sn_customerservice_case.xlsx",
    sheet_name="Galileo"
)

# CLEAN COLUMN NAMES
df_sheet3.columns = df_sheet3.columns.str.strip().str.lower()

# CLEAN VALUES
df_sheet3["infra dependecies"] = (
    df_sheet3["infra dependecies"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)
# COUNTS
infra_count = len(
    df_sheet3[
        df_sheet3["infra dependecies"] == "yes"
    ]
)

universe_count = len(
    df_sheet3[
        df_sheet3["infra dependecies"] == "no"
    ]
)

# SUMMARY DATAFRAME
sheet3_summary = pd.DataFrame({
    "Team": ["Infra", "Universe"],
    "Count": [infra_count, universe_count]
})

# PIE CHART
fig3 = px.pie(
    sheet3_summary,
    names="Team",
    values="Count",
    title="Galileo"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)
