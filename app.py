import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from requests.auth import HTTPBasicAuth

# ServiceNow details
INSTANCE = "yourcompany"
USERNAME = "your_username"
PASSWORD = "your_password"

url = f"https://{INSTANCE}.service-now.com/api/now/table/incident"

params = {
    "sysparm_limit": 100,
    "sysparm_query": "active=true"
}

response = requests.get(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    params=params,
    headers={"Accept": "application/json"}
)

data = response.json()["result"]

df = pd.DataFrame(data)

st.title("EE4 ServiceNow Open Tickets Dashboard")

# KPIs
st.metric("Total Open Tickets", len(df))

# Priority distribution
priority_chart = df["priority"].value_counts().reset_index()
priority_chart.columns = ["Priority", "Count"]

fig = px.bar(
    priority_chart,
    x="Priority",
    y="Count",
    color="Priority",
    title="Tickets by Priority"
)

st.plotly_chart(fig)

# Assignment group filter
if "assignment_group" in df.columns:
    groups = df["assignment_group"].astype(str).unique()

    selected_group = st.selectbox(
        "Select Assignment Group",
        groups
    )

    filtered = df[
        df["assignment_group"].astype(str) == selected_group
    ]

    st.dataframe(filtered)
