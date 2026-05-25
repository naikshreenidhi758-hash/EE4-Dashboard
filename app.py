import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)

# ---------------------------------
# IMAGE
# ---------------------------------
st.image("envision.png")

# ---------------------------------
# TITLE
# ---------------------------------
st.title("🎫 INDIA Software Ticket Report")

# ---------------------------------
# SERVICENOW INSTANCE
# ---------------------------------
INSTANCE = "https://ee.envision-energy.com"

# ---------------------------------
# OAUTH CONFIG
# ---------------------------------
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

TOKEN_URL = f"{INSTANCE}/oauth_token.do"

# ---------------------------------
# GET OAUTH TOKEN
# ---------------------------------
token_payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

try:
    token_response = requests.post(
        TOKEN_URL,
        data=token_payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    st.write("OAuth Status Code:", token_response.status_code)

    if token_response.status_code != 200:
        st.error("Failed to get OAuth token")
        st.code(token_response.text)
        st.stop()

    token_data = token_response.json()

    access_token = token_data["access_token"]

except Exception as e:
    st.error(f"OAuth Error: {e}")
    st.stop()

# ---------------------------------
# SERVICENOW API URL
# ---------------------------------
API_URL = f"{INSTANCE}/api/now/table/u_incident_software"

# ---------------------------------
# API REQUEST
# ---------------------------------
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

try:
    response = requests.get(
        API_URL,
        headers=headers
    )

except Exception as e:
    st.error(f"API Connection Error: {e}")
    st.stop()

# ---------------------------------
# DEBUG RESPONSE
# ---------------------------------
st.write("API Status Code:", response.status_code)

# ---------------------------------
# CHECK RESPONSE
# ---------------------------------
if response.status_code != 200:
    st.error("Failed to connect to ServiceNow API")

    st.write("Response:")
    st.code(response.text)

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
# LOAD DATAFRAME
# ---------------------------------
df = pd.DataFrame(data)

# ---------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------
df.columns = df.columns.str.strip().str.lower()

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
# REQUIRED COLUMNS
# ---------------------------------
required_columns = [
    "number",
    "short description",
    "case state",
    "site",
    "register time"
]

# ---------------------------------
# CHECK MISSING COLUMNS
# ---------------------------------
missing_cols = [
    col for col in required_columns
    if col not in df.columns
]

if missing_cols:
    st.error(f"Missing Columns: {missing_cols}")
    st.stop()

# ---------------------------------
# FILTER DATA
# ---------------------------------
dashboard_df = df[required_columns]

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
