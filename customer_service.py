import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service",
    layout="wide"
)

st.title("Customer Service")

# LOAD EXCEL
df = pd.read_excel(
)   

df.columns = df.columns.str.strip()

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower()
