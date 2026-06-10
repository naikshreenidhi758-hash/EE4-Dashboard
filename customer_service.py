import streamlit as st
from openpyxl import load_workbook
import pandas as pd
import plotly.express as px


# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service",
    layout="wide"
)

# LOAD EXCEL
df = pd.read_excel(
    "sn_customerservice_case.xlsx",
)

df.columns = df.columns.str.strip()

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower()


wb = load_workbook("sn_customerservice_case.xlsx")
ws = wb["Infra EE4 Cases"]

infra_count = 0
universe_count = 0

for row in ws.iter_rows(min_row=2):
    cell = row[3]   # Short description column (adjust index)

    color = cell.fill.fgColor.rgb

    if color == "FF00FF00":  # Green
        infra_count += 1
    elif color == "FFFF0000":  # Red
        universe_count += 1

print("Infra:", infra_count)
print("Universe:", universe_count)

fig = px.pie(
    team_summary,
    names="Team",
    values="Count",
    title="Infra vs Universe"
)

st.plotly_chart(fig, use_container_width=True)
