import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Software Tickets", layout="wide")

st.title("🎫 Software Ticket Dashboard")

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
        "Select Status",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )

    priority_filter = st.sidebar.multiselect(
        "Select Priority",
        options=df["Priority"].unique(),
        default=df["Priority"].unique()
    )

    filtered_df = df[
        (df["Status"].isin(status_filter)) &
        (df["Priority"].isin(priority_filter))
    ]

    # KPIs
    total_tickets = len(filtered_df)
    open_tickets = len(filtered_df[filtered_df["Status"] == "Open"])
    closed_tickets = len(filtered_df[filtered_df["Status"] == "Closed"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Closed Tickets", closed_tickets)

    # Status Chart
    st.subheader("Tickets by Status")

    status_chart = filtered_df["Status"].value_counts().reset_index()
    status_chart.columns = ["Status", "Count"]

    fig1 = px.bar(
        status_chart,
        x="Status",
        y="Count",
        color="Status",
        title="Ticket Status Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Priority Chart
    st.subheader("Tickets by Priority")

    priority_chart = filtered_df["Priority"].value_counts().reset_index()
    priority_chart.columns = ["Priority", "Count"]

    fig2 = px.pie(
        priority_chart,
        names="Priority",
        values="Count",
        title="Priority Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Filtered Data
    st.subheader("Filtered Tickets")
    st.dataframe(filtered_df)

else:
    st.info("Please upload an Excel or CSV file.")
