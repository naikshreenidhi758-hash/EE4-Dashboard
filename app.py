import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from requests.auth import HTTPBasicAuth

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)

# ---------------------------------
# TOP IMAGE
# ---------------------------------
st.image("envision.png")

# ---------------------------------
# TITLE
# ---------------------------------
st.title("🎫 INDIA Software Ticket Report")

# ---------------------------------
# SERVICENOW CONFIG
# ---------------------------------
INSTANCE = "https://ee.envision-energy.com/now/nav/ui/classic/params/target/u_incident_software_list.do%3Fsysparm_query%3Du_site.u_director_of_service%253D67c3ce79db868f0085c19c27db96194e%255Eu_case_state!%253D7%255EORu_case_state%253DNULL%255Eu_site!%253D2df8921fdb3fa740e6ca9cb6db96198b%255EORu_site%253DNULL%255Eu_site.u_site_bigarea!%253DLatin%2520America%255EORu_site.u_site_bigarea%253DNULL%26sysparm_first_row%3D1%26sysparm_view%3D"

API_URL = f"{INSTANCE}/api/now/table/u_incident_software"

USERNAME = "your_username"
PASSWORD = "your_password"

# ---------------------------------
# API REQUEST
# ---------------------------------
response = requests.get(
    API_URL,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers={"Accept": "application/json"}
)

# ---------------------------------
# CHECK API RESPONSE
# ---------------------------------
if response.status_code != 200:
    st.error("Failed to fetch data from ServiceNow")
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
