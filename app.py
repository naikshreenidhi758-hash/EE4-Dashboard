import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from requests.auth import HTTPBasicAuth


# PAGE CONFIG
st.set_page_config(
    page_title="INDIA Software Ticket Report",
    layout="wide"
)


# HEADER
st.image("envision.png")

st.title("🎫 INDIA Software Ticket Report")


# SERVICENOW CONFIG
INSTANCE = "https://ee.envision-energy.com"

API_URL = f"{INSTANCE}/api/now/table/u_incident_software"


# SECURE CREDENTIALS
USERNAME = st.secrets["SN_USERNAME"]
PASSWORD = st.secrets["SN_PASSWORD"]


# API REQUEST
try:

    response = requests.get(
        API_URL,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={
            "Accept": "application/json"
        },
        timeout=30
    )

except requests.exceptions.RequestException as e:
    st.error(f"Connection Error: {e}")
    st.stop()


# STATUS CHECK
if response.status_code != 200:

    st.error(
        f"ServiceNow Connection Failed | Status Code: {response.status_code}"
    )

    st.code(response.text)

    st.stop()


# JSON PARSE
try:

    data = response.json()["result"]

except Exception as e:

    st.error(f"JSON Parsing Error: {e}")

    st.code(response.text)

    st.stop()


# EMPTY DATA CHECK
if not data:

    st.warning("No ticket data found")

    st.stop()

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

# ---------------------------------
# COLUMN VALIDATION
# ---------------------------------
missing_cols = [
    col for col in required_columns
    if col not in df.columns
]

if missing_cols:

    st.error(f"Missing Columns: {missing_cols}")

    st.write("Available Columns:")

    st.write(df.columns.tolist())

    st.stop()


# FILTER DATA
dashboard_df = df[required_columns]


# SIDEBAR
st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect(
    "Select Case State",
    options=dashboard_df["case state"].dropna().unique(),
    default=dashboard_df["case state"].dropna().unique()
)

site_filter = st.sidebar.multiselect(
    "Select Site",
    options=dashboard_df["site"].dropna().unique(),
    default=dashboard_df["site"].dropna().unique()
)

# ---------------------------------
# APPLY FILTERS
# ---------------------------------
dashboard_df = dashboard_df[
    (dashboard_df["case state"].isin(status_filter)) &
    (dashboard_df["site"].isin(site_filter))
]

# ---------------------------------
# KPI SECTION
# ---------------------------------
total_tickets = len(dashboard_df)

open_tickets = len(
    dashboard_df[
        dashboard_df["case state"]
        .astype(str)
        .str.strip()
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
        .str.strip()
        .str.lower()
        == "closed"
    ]
)

# ---------------------------------
# KPI DISPLAY
# ---------------------------------
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
    hole=0.5,
    title="Ticket Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)


# CURRENT MONTH OPEN TICKETS
dashboard_df["register time"] = pd.to_datetime(
    dashboard_df["register time"],
    errors="coerce"
)

current_month = pd.Timestamp.now().month
current_year = pd.Timestamp.now().year

open_states = [
    "register",
    "in processing",
    "effect confirmation"
]

current_month_df = dashboard_df[
    (dashboard_df["register time"].dt.month == current_month) &
    (dashboard_df["register time"].dt.year == current_year) &
    (
        dashboard_df["case state"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(open_states)
    )
]


# CURRENT MONTH TABLE
st.subheader("Current Month Open Ticket Summary")

st.dataframe(current_month_df)
