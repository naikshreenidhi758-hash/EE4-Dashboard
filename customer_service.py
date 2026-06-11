import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service Dashboard",
    layout="wide"
)

st.title("Customer Service Dashboard")

excel_file = "sn_customerservice_case.xlsx"


# SHEET 1 : Infra EE4 Cases
st.header("Infra EE4 Cases")

df1 = pd.read_excel(
    excel_file,
    sheet_name="Infra EE4 Cases"
)

df1.columns = df1.columns.str.strip().str.lower()

df1["company"] = (
    df1["company"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

infra_count_1 = len(
    df1[df1["company"].str.contains("infra", na=False)]
)

universe_count_1 = len(
    df1[df1["company"].str.contains("universe", na=False)]
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Infra Cases", infra_count_1)

with col2:
    st.metric("Universe Cases", universe_count_1)

summary1 = pd.DataFrame({
    "Team": ["Infra", "Universe"],
    "Count": [infra_count_1, universe_count_1]
})

fig1 = px.pie(
    summary1,
    names="Team",
    values="Count",
    title="Infra EE4 Cases - Infra vs Universe"
)

st.plotly_chart(fig1, use_container_width=True)


# SHEET 2 : Enos Public IP issue
st.header("Enos Public IP Issue")

df2 = pd.read_excel(
    excel_file,
    sheet_name="Enos Public IP issue"
)

df2.columns = df2.columns.str.strip().str.lower()

df2["infra dependecies"] = (
    df2["infra dependecies"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

infra_count_2 = len(
    df2[df2["infra dependecies"] == "yes"]
)

universe_count_2 = len(
    df2[df2["infra dependecies"] == "no"]
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Infra Cases", infra_count_2)

with col2:
    st.metric("Universe Cases", universe_count_2)

summary2 = pd.DataFrame({
    "Team": ["Infra", "Universe"],
    "Count": [infra_count_2, universe_count_2]
})

fig2 = px.pie(
    summary2,
    names="Team",
    values="Count",
    title="Enos Public IP Issue - Infra vs Universe"
)

st.plotly_chart(fig2, use_container_width=True)


# SHEET 3 : Galileo
st.header("Galileo")

df3 = pd.read_excel(
    excel_file,
    sheet_name="Galileo"
)

df3.columns = df3.columns.str.strip().str.lower()

df3["infra dependecies"] = (
    df3["infra dependecies"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

infra_count_3 = len(
    df3[df3["infra dependecies"] == "yes"]
)

universe_count_3 = len(
    df3[df3["infra dependecies"] == "no"]
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Infra Cases", infra_count_3)

with col2:
    st.metric("Universe Cases", universe_count_3)

summary3 = pd.DataFrame({
    "Team": ["Infra", "Universe"],
    "Count": [infra_count_3, universe_count_3]
})

fig3 = px.pie(
    summary3,
    names="Team",
    values="Count",
    title="Galileo - Infra vs Universe"
)

st.plotly_chart(fig3, use_container_width=True)
