import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from requests.auth import HTTPBasicAuth

# PAGE CONFIG
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)

# IMAGE
st.image("envision.png")

# TITLE
st.title("🎫 INDIA Software Ticket Report")
INSTANCE = "https://ee.envision-energy.com"

API_URL = f"{INSTANCE}/api/now/table/u_incident_software"

USERNAME = st.secrets["SN_USERNAME"]
PASSWORD = st.secrets["SN_PASSWORD"]

response = requests.get(
    API_URL,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers={
        "Accept": "application/json"
    }
)

st.write("Status Code:", response.status_code)

if response.status_code == 200:

    st.success("Connected Successfully")

    data = response.json()["result"]

    st.write(data[:5])

else:
    st.error(response.text)


# SERVICENOW INSTANCE
INSTANCE = "https://ee.envision-energy.com"

API_URL = f"{INSTANCE}/api/now/table/u_incident_software"


# DATAFRAME
df = pd.DataFrame(data)

# CLEAN COLUMNS
df.columns = df.columns.str.strip().str.lower()


# RENAME COLUMNS
df = df.rename(columns={
    "short_description": "short description",
    "u_case_state": "case state",
    "u_site": "site",
    "u_register_time": "register time"
})

# REQUIRED COLUMNS
required_columns = [
    "number",
    "short description",
    "case state",
    "site",
    "register time"
]

# CHECK REQUIRED COLUMNS
missing_cols = [
    col for col in required_columns
    if col not in df.columns
]

if missing_cols:
    st.error(f"Missing Columns: {missing_cols}")
    st.stop()


# FILTER DATA
dashboard_df = df[required_columns]


# SHOW DATA
st.subheader("Ticket Data across INDIA")

st.dataframe(dashboard_df)

# KPI SECTION
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


# KPI DISPLAY
col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", total_tickets)
col2.metric("Open Tickets", open_tickets)
col3.metric("Closed Tickets", closed_tickets)


# PIE CHART
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
    hole=0.5,
    title="Ticket Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)
