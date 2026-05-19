import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Software Ticket Dashboard", layout="wide")

st.title("🎫 Software Tickets")

# Upload Excel File
uploaded_file = st.file_uploader(
    "Upload Ticket Excel File",
    type=["xlsx", "csv"]
)

if uploaded_file:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("Ticket Data")
    st.dataframe(df)

    # Sidebar Filters
    st.sidebar.header("Filters")

    status_filter = st.sidebar.multiselect(
        "Select Case State",
        options=df["Case State"].unique(),
        default=df["Case State"].unique()
    )

    priority_filter = st.sidebar.multiselect(
        "Select Site",
        options=df["Site"].unique(),
        default=df["Site"].unique()
    )

    filtered_df = df[
        (df["Case State"].isin(Case State_filter)) &
        (df["Site"].isin(priority_filter))
    ]

    # KPIs
    total_tickets = len(filtered_df)
    open_tickets = len(filtered_df[filtered_df["Case State"] == "Open"])
    closed_tickets = len(filtered_df[filtered_df["Case State"] == "Closed"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Closed Tickets", closed_tickets)

    # Status Chart
    st.subheader("Tickets by Status")

    Case State_chart = filtered_df["Case State"].value_counts().reset_index()
    Case State_chart.columns = ["Case State", "Count"]

    fig1 = px.bar(
       Case State_chart,
        x="Case State",
        y="Count",
        color="Case State",
        title="Ticket Status Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Priority Chart
    st.subheader("Tickets by Site")

    priority_chart = filtered_df["Site"].value_counts().reset_index()
    priority_chart.columns = ["Site", "Count"]

    fig2 = px.pie(
        priority_chart,
        names="Site",
        values="Count",
        title="Site Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Filtered Data
    st.subheader("Filtered Tickets")
    st.dataframe(filtered_df)

else:
    st.info("Please upload an Excel or CSV file.")
