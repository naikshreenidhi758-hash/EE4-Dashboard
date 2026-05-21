import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)

# Title
st.title("🎫 Software Ticket Dashboard")

# Upload File
uploaded_file = st.file_uploader(
    "Upload Excel or CSV File",
    type=["xlsx", "csv"]
)

if uploaded_file:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Required columns
    required_columns = [
        "number",
        "short description",
        "case state",
        "site",
        "register time"
    ]

    # Check missing columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
        st.write("Available columns:", df.columns.tolist())
        st.stop()

    # Keep only required columns
    required_df = df[required_columns]

    # Save filtered columns to Excel
    output_file = "filtered_output.xlsx"

    required_df.to_excel(output_file, index=False)

    st.success(f"Filtered file saved as {output_file}")

    # Download button
    with open(output_file, "rb") as file:
        st.download_button(
            label="Download Filtered Excel File",
            data=file,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.success("File uploaded successfully!")

    # Show Raw Data
    st.subheader("Ticket Data")
    st.dataframe(required_df)

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Case State Filter
    status_filter = st.sidebar.multiselect(
        "Select Case State",
        options=df["case state"].dropna().unique(),
        default=df["case state"].dropna().unique()
    )

    # Site Filter
    site_filter = st.sidebar.multiselect(
        "Select Site",
        options=df["site"].dropna().unique(),
        default=df["site"].dropna().unique()
    )

    # Apply Filters
    filtered_df = df[
        (df["case state"].isin(status_filter)) &
        (df["site"].isin(site_filter))
    ]

    # ----------------------------
    # KPI Metrics
    # ----------------------------
    st.subheader("Statistics")

    total_tickets = len(filtered_df)

    open_tickets = len(
        filtered_df[
            filtered_df["case state"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin([
                "open",
                "register",
                "effect confirmation",
                "in processing"
            ])
        ]
    )

    closed_tickets = len(
        filtered_df[
            filtered_df["case state"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "closed"
        ]
    )

    # KPI Columns
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Closed Tickets", closed_tickets)

    # ----------------------------
    # Tickets by Case State
    # ----------------------------
    st.subheader("Tickets by Case State")

    status_chart = (
        filtered_df["case state"]
        .value_counts()
        .reset_index()
    )

    status_chart.columns = ["Case State", "Count"]

    fig1 = px.bar(
        status_chart,
        x="Case State",
        y="Count",
        color="Case State",
        title="Case State Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------
    # Tickets by Site
    # ----------------------------
    st.subheader("Tickets by Site")

    site_chart = (
        filtered_df["site"]
        .value_counts()
        .reset_index()
    )

    site_chart.columns = ["Site", "Count"]

    fig2 = px.pie(
        site_chart,
        names="Site",
        values="Count",
        title="Site Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # Filtered Data
    # ----------------------------
    st.subheader("Filtered Ticket Data")

    st.dataframe(filtered_df)

else:
    st.info("Please upload an Excel or CSV file.")
