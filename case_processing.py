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

# SharePoint URLs
site_url = "https://envisionint.sharepoint.com/sites"

file_url = "https://envisionint.sharepoint.com/:x:/r/sites"

# Read Excel
df = pd.read_excel(file_url)

st.dataframe(df)
  
