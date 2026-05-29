import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)

# Add Image
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("envision.png")

# Title Centering
st.markdown(
    "<h1 style='text-align: center;'>🎫 INDIA Software Ticket Report</h1>",
    unsafe_allow_html=True
)

# Upload File
uploaded_file = st.file_uploader(
    "Upload Incident softwares file",
    type=["xlsx", "csv"]
)

if uploaded_file:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean Column Names
    df.columns = df.columns.str.strip().str.lower()

    # Required Columns
    required_columns = [
        "number",
        "short description",
        "case state",
        "site",
        "register time",
        "close time"
    ]

    # Check Missing Columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
        st.write("Available columns:", df.columns.tolist())
        st.stop()

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

    # Statistics
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

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Closed Tickets", closed_tickets)

    # Ticket Data
    st.subheader("Ticket Data across INDIA")

    required_df = filtered_df[required_columns]

    st.dataframe(required_df)

    # Create 2 Columns
    left_col, right_col = st.columns(2)

    # LEFT SIDE - Ticket Status
    with left_col:

        st.subheader("Tickets by Case State")

        status_chart = (
            filtered_df["case state"]
            .value_counts()
            .reset_index()
        )

        status_chart.columns = ["Case State", "Count"]

        fig1 = px.pie(
            status_chart,
            names="Case State",
            values="Count",
            hole=0.5,
            title="Case State Distribution"
        )

        fig1.update_traces(textinfo="value")

        st.plotly_chart(fig1, use_container_width=True)

    #RIGHT SIDE-Ticket Status Over a Year
    
    with right_col:
        st.subheader("Ticket Status Over a Year")
        status_chart=(
            filtered_df["register time"]
            .value_counts()
            .rest_index()
        )
        status_chart.columns=["Register Time","count"]

        fig2=pie.bar(
            status_chart,
            x="Register Time",
            y="Count"
            title="Ticket Status Over a Year"
        )

        st.plotly_chart(fig2, use_container_width=True)

    

    # Filter Only Open Tickets
    open_tickets_df = filtered_df[
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

    # Keep Only Required Columns
    open_tickets_df = open_tickets_df[required_columns]

    # Show Open Tickets
    st.subheader("Total Open Tickets")

    st.dataframe(open_tickets_df)
