import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service",
    layout="wide"
)

excel_url = "https://envisionint-my.sharepoint.com"

df = pd.read_excel(excel_url)

df.columns = df.columns.str.strip()

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower()
