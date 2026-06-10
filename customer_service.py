import streamlit as st
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

