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

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Check Required Columns
    required_columns = ["Number","Short description","Case State","Site","Register time"]

    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            st.stop()
    # Keep only required columns
    required_df = df[required_columns]

    # Save filtered columns to Excel
    output_file = "filtered_output.xlsx"

    required_df.to_excel(output_file, index=False)

    st.success(f"Filtered file saved as {output_file}")
    st.success(f"File saved as {output_file}")

    # Save to new Excel file
    filtered_df.to_excel(output_file, index=False)
 
    print("Filtered file saved as:", output_file)       

    st.success("File uploaded successfully!")

    # Show Raw Data
    st.subheader("Ticket Data")
    st.dataframe(df)

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Case State Filter
    status_filter = st.sidebar.multiselect(
        "Select Case State",
        options=df["Case State"].dropna().unique(),
        default=df["Case State"].dropna().unique()
    )

    # Site Filter
    site_filter = st.sidebar.multiselect(
        "Select Site",
        options=df["Site"].dropna().unique(),
        default=df["Site"].dropna().unique()
    )

    # Apply Filters
    filtered_df = df[
        (df["Case State"].isin(status_filter)) &
        (df["Site"].isin(site_filter))
    ]

        # KPI Metrics
    st.subheader("Statistics")
    total_tickets = len(filtered_df)

    open_tickets = len(
        filtered_df[
            filtered_df["Case State"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["open", "register"," Effect confirmation", "in processing"])
        ]
    )

    closed_tickets = len(
        filtered_df[
            filtered_df["Case State"]
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
        filtered_df["Case State"]
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
        filtered_df["Site"]
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
