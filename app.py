import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Software Ticket Dashboard",
    layout="wide"
)

# ---------------------------------
# TOP IMAGE
# ---------------------------------
st.image("envision.png", use_container_width=True)

# ---------------------------------
# HEADER SECTION
# ---------------------------------
col1, col2 = st.columns([1, 6])

with col1:
    st.image("images/logo.png", width=90)

with col2:
    st.markdown(
        """
        <h1 style='margin-bottom:0px; color:#003366;'>
            🎫 INDIA  Software Ticket Report
        </h1>
        """,
        unsafe_allow_html=True
    )

# Subtitle
st.markdown(
    """
    <h4 style='color:gray; margin-top:0px;'>
        Upload Incident Software File
    </h4>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# FILE UPLOAD
# ---------------------------------
uploaded_file = st.file_uploader(
    "",
    type=["xlsx", "csv"]
)

# ---------------------------------
# READ FILE
# ---------------------------------
if uploaded_file:

    # Read Excel or CSV
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
        "register time",
        "close time"
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

    # Keep required columns
    required_df = df[required_columns]

    st.success(f"Uploaded File: {uploaded_file.name}")

    # ---------------------------------
    # SHOW DATA
    # ---------------------------------
    st.subheader("Ticket Data across INDIA")
    st.dataframe(required_df)

    # ---------------------------------
    # SIDEBAR FILTERS
    # ---------------------------------
    st.sidebar.header("Filters")

    status_filter = st.sidebar.multiselect(
        "Select Case State",
        options=df["case state"].dropna().unique(),
        default=df["case state"].dropna().unique()
    )

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

    # ---------------------------------
    # KPI SECTION
    # ---------------------------------
    left_col, right_col = st.columns(2)

    with left_col:

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

    # ---------------------------------
    # PIE CHART
    # ---------------------------------
    with right_col:

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

    # ---------------------------------
    # CURRENT MONTH FILTER
    # ---------------------------------
    filtered_df["register time"] = pd.to_datetime(
        filtered_df["register time"],
        errors="coerce"
    )

    current_month = pd.Timestamp.now().month
    current_year = pd.Timestamp.now().year

    current_month_df = filtered_df[
        (filtered_df["register time"].dt.month == current_month) &
        (filtered_df["register time"].dt.year == current_year)
    ]

    current_month_df = current_month_df[required_columns]

    # ---------------------------------
    # CURRENT MONTH SUMMARY
    # ---------------------------------
    st.subheader("Current Month Ticket Summary")

    st.dataframe(current_month_df)
