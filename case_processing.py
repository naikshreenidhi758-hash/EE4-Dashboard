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
#Rename column
eng1_count.columns=["engineer", "project_count"]


eng1_count["color"] = eng1_count["engineer"].apply(
    lambda x: "Unassigned" if x == "Unassigned" else "Assigned"
)

fig = px.bar(
    eng1_count,
    x="engineer",
    y="project_count",
    color="color",
    color_discrete_map={
        "Assigned": "blue",
        "Unassigned": "red"
    },
    text="project_count"
)

st.plotly_chart(fig, use_container_width=True)

status_count=df["Status"].value_counts().reset_index()
status_count.columns=["Status","Count"]

fig=px.pie(
    status_count,
    names="Status",
    values="Count",
    title="Projects by Status"
)
st.plotly_chart(fig, use_container_width=True)
