import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)

# Title
st.title("🇮🇳 INDIA Project - Case Processing Status 📋")

# Read Excel
df = pd.read_excel("India project synchronous.xlsx")

st.dataframe(df)
  
