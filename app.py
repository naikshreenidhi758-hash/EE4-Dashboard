import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from requests.auth import HTTPBasicAuth

#page config
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)
#add image
st.image("envision.png")

#title
st.title("🎫 INDIA Software Ticket Report")

# ---------------------------------
# SERVICENOW API
# ---------------------------------
INSTANCE = "https://ee.envision-energy.com"

API_URL = f"{INSTANCE}/api/now/table/u_incident_software"

USERNAME = "your_username"
PASSWORD = "your_password"

headers = {
    "Accept": "application/json"
}

# ---------------------------------
# API REQUEST
# ---------------------------------
response = requests.get(
    API_URL,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers=headers
)

# ---------------------------------
# DEBUG RESPONSE
# ---------------------------------
st.write("Status Code:", response.status_code)

# Show first 500 characters
st.text(response.text[:500])

# ---------------------------------
# CHECK RESPONSE
# ---------------------------------
if response.status_code != 200:
    st.error("Failed to connect to ServiceNow")
    st.stop()

# ---------------------------------
# TRY JSON
# ---------------------------------
try:
    data = response.json()["result"]

except Exception as e:
    st.error(f"JSON Error: {e}")

    st.write("Raw Response:")
    st.code(response.text)

    st.stop()
# ---------------------------------
# LOAD DATA
# ---------------------------------
data = response.json()["result"]

df = pd.DataFrame(data)

# ---------------------------------
# CLEAN COLUMNS
# ---------------------------------
df.columns = df.columns.str.strip().str.lower()

# ---------------------------------
# REQUIRED COLUMNS
# ---------------------------------
required_columns = [
    "number",
    "short_description",
    "u_case_state",
    "u_site",
    "u_register_time"
]

# ---------------------------------
# RENAME COLUMNS
# ---------------------------------
df = df.rename(columns={
    "short_description": "short description",
    "u_case_state": "case state",
    "u_site": "site",
    "u_register_time": "register time"
})

# ---------------------------------
# KEEP REQUIRED FIELDS
# ---------------------------------
dashboard_df = df[
    [
        "number",
        "short description",
        "case state",
        "site",
        "register time"
    ]
]

# ---------------------------------
# SHOW DATA
# ---------------------------------
st.subheader("Ticket Data across INDIA")

st.dataframe(dashboard_df)

# ---------------------------------
# KPI SECTION
# ---------------------------------
total_tickets = len(dashboard_df)

open_tickets = len(
    dashboard_df[
        dashboard_df["case state"]
        .astype(str)
        .str.lower()
        .isin([
            "register",
            "in processing",
            "effect confirmation"
        ])
    ]
)

closed_tickets = len(
    dashboard_df[
        dashboard_df["case state"]
        .astype(str)
        .str.lower()
        == "closed"
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", total_tickets)
col2.metric("Open Tickets", open_tickets)
col3.metric("Closed Tickets", closed_tickets)

# ---------------------------------
# PIE CHART
# ---------------------------------
status_chart = (
    dashboard_df["case state"]
    .value_counts()
    .reset_index()
)

status_chart.columns = ["Case State", "Count"]

fig = px.pie(
    status_chart,
    names="Case State",
    values="Count",
    hole=0.5
)

st.plotly_chart(fig, use_container_width=True)
