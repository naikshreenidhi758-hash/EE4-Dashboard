import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG
st.set_page_config(
    page_title="Customer Service",
    layout="wide"
)

excel_url = "https://envisionint-my.sharepoint.com/:x:/r/personal/nitheesh_ng_envision-energy_com/Documents/sn_customerservice_case.xlsx?d=w64b168e1f1bf4a74acefdd6145bf8aa4&csf=1&web=1&e=805A4H"

df = pd.read_excel(excel_url)

df.columns = df.columns.str.strip()

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower()
