import streamlit as st

import pandas as pd

import plotly.express as px
 
#add image

st.image("envision.png")
 
# Page Configuration

st.set_page_config(

    page_title="Software Ticket Dashboard",

    layout="wide"

)
 
# Title

st.title("🎫 INDIA  Software Ticket Report ")
 
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
 
    # Keep only required columns

    required_df = df[required_columns]
 
    st.success("File uploaded successfully!")
 
    # Show Raw Data

    st.subheader("Ticket Data across INDIA")

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
 
    # Create 2 columns

    left_col, right_col = st.columns(2)
 
    # ----------------------------

    # LEFT SIDE - Statistics

    # ----------------------------

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
 
    # ----------------------------

    # RIGHT SIDE - Ticket Status

    # ----------------------------

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
 
    # ----------------------------

    # Filtered Data

    # ----------------------------
 
    # Convert register time column to datetime

    df["register time"] = pd.to_datetime(

        df["register time"],

        errors="coerce"

    )
 
    # Get current month and year

    current_month = pd.Timestamp.now().month

    current_year = pd.Timestamp.now().year
 
    # Apply current month filter

    filtered_df = filtered_df[

        (filtered_df["register time"].dt.month == current_month) &

        (filtered_df["register time"].dt.year == current_year)

    ]
 
    # Keep only required columns

    filtered_df = filtered_df[required_columns]
 
    # Show Filtered Data

    st.subheader("Current Month Ticket Summary")
 
    st.dataframe(filtered_df)
 
