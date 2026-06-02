import streamlit as st
import pandas as pd
import plotly.express as px

#page configuration
st.set_page_config(
 page_title="Case Processing Dashboard",
  layout="wide"
)

#title
st.title("INDIA Project-Case processing Status📋")

#read from sharepoint
df.load_sharepoint_data()
site_url=https://envisionint.sharepoint.com/sites

file_url=https://envisionint.sharepoint.com/:x:/r/sites
df = pd.read_excel(file_url)
  
