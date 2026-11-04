import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)


# ============================================================
# HEADER / IMAGE
# ============================================================

st.image("envision.png")

st.title("INDIA Project - Case Processing Status 📋")


# ============================================================
# LOAD EXCEL
# ============================================================

df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip().str.lower()


# ============================================================
# CLEAN ENGINEER COLUMN
# IMPORTANT:
# Do NOT replace missing engineer with Ticket Status Unassigned
# ============================================================

df["first engineer(india team)"] = (
    df["first engineer(india team)"]
    .astype("string")
    .str.strip()
)


# ============================================================
# CLEAN STATUS
# Ticket Status Unassigned belongs to STATUS
# ============================================================

df["status"] = (
    df["status"]
    .fillna("Ticket Status Unassigned")
    .astype(str)
    .str.strip()
    .replace(
        ["", "nan", "None"],
        "Ticket Status Unassigned"
    )
)


# ============================================================
# CLEAN PRIORITY
# ============================================================

df["priority"] = (
    df["priority"]
    .fillna("Ticket Status Unassigned")
    .astype(str)
    .str.strip()
    .str.title()
)


# ============================================================
# DATE CONVERSION
# ============================================================

df["start date"] = pd.to_datetime(
    df["start date"],
    errors="coerce"
)

df["filled_date"] = pd.to_datetime(
    df["filled_date"],
    errors="coerce"
)

df["end time"] = pd.to_datetime(
    df["end time"],
    errors="coerce"
)


# ============================================================
# EFFECTIVE DATE
# Use Start Date first, otherwise Filled Date
# ============================================================

df["effective_date"] = (
    df["start date"]
    .fillna(df["filled_date"])
)


# ============================================================
# YEAR / MONTH / WEEK
# ============================================================

df["year"] = df["effective_date"].dt.year

df["month"] = df["effective_date"].dt.month

df["month_name"] = (
    df["effective_date"]
    .dt.strftime("%B")
)

df["week_no"] = (
    df["effective_date"]
    .dt.isocalendar()
    .week
    .astype("Int64")
)

df["week_name"] = (
    "Week " +
    df["week_no"].astype(str)
)


# ============================================================
# DASHBOARD SIDEBAR NAVIGATION
# ============================================================

selected_section = st.sidebar.radio(
    "📌 Dashboard Navigation",
    [
        "Status Cases by Engineer and Status",
        "Engineer Yearly Performance",
        "Pending Cases Aging Analysis"
    ],
    key="dashboard_navigation"
)

# ============================================================
# KPI METRICS - ALL TICKETS
# These KPIs ALWAYS show the complete dataset
# Year / Month / Week filters do NOT affect them
# ============================================================

total_cases = len(df)


closed_cases = len(
    df[
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("closed")
    ]
)


pending_cases = (
    total_cases - closed_cases
)


closure_rate = (
    (closed_cases / total_cases) * 100
    if total_cases > 0
    else 0
)


closure_rate = (
    (closed_cases / total_cases) * 100
    if total_cases > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:
    st.metric(
        "📋 Total Cases",
        total_cases
    )


with c2:
    st.metric(
        "⏳ Pending Cases",
        pending_cases
    )


with c3:
    st.metric(
        "✅ Closed Cases",
        closed_cases
    )


with c4:
    st.metric(
        "📈 Closure %",
        f"{closure_rate:.1f}%"
    )


# ============================================================
# PENDING CASE LIST
# ============================================================

with st.expander(
    f"View All {pending_cases} Pending Cases"
):

    pending_case_list = df[
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .ne("closed")
    ]

    st.dataframe(
        pending_case_list,
        use_container_width=True
    )


# ============================================================
# OVERALL TICKET STATUS - ALL TICKETS
# ============================================================

st.subheader("📊 Overall Ticket Status")


status_summary = (
    df
    .groupby("status")
    .size()
    .reset_index(name="Count")
)


fig_status = px.pie(
    status_summary,
    names="status",
    values="Count",
    color="status",
    hole=0.45,
    title="Overall Ticket Status - All Tickets"
)


fig_status.update_traces(
    textinfo="label+value+percent",
    textposition="outside"
)


fig_status.update_layout(
    showlegend=True,
    legend_title="Status"
)


st.plotly_chart(
    fig_status,
    use_container_width=True
)

if selected_section == "Status Cases by Engineer and Status":
    # ============================================================
    # ENGINEER VS STATUS
    # Filters are displayed on the right of this chart.
    # ============================================================
    st.markdown(
        "<div id='status-cases-by-engineer'></div>",
        unsafe_allow_html=True
    )

    st.subheader("👨‍💻 Status Cases by Engineer and Status")

    st.subheader("👨‍💻 Cases by Engineer and Status")

    chart_col, filter_col = st.columns([3, 1])

    with filter_col:
        st.markdown("### 🔎 Filters")

        years = sorted(
            df["year"].dropna().unique().tolist(),
            reverse=True
        )

        selected_year = st.selectbox(
            "Select Year",
            years,
            key="engineer_status_year"
        )

        available_months = (
            df[df["year"] == selected_year]
            .sort_values("month")["month_name"]
            .dropna()
            .unique()
            .tolist()
        )

        current_month = datetime.now().strftime("%B")
        default_month_index = (
            available_months.index(current_month)
            if current_month in available_months
            else 0
        )

        selected_month = st.selectbox(
            "Select Month",
            available_months,
            index=default_month_index,
            key="engineer_status_month"
        )

        available_weeks = (
            df[
                (df["year"] == selected_year) &
                (df["month_name"] == selected_month)
            ]
            .sort_values("week_no")["week_name"]
            .dropna()
            .unique()
            .tolist()
        )

        week_options = ["All Weeks"] + available_weeks

        selected_week = st.selectbox(
            "Select Week",
            week_options,
            key="engineer_status_week"
        )

    # Year / Month / Week filtering is used by the Engineer vs Status chart
    filtered_df = df[
        (df["year"] == selected_year) &
        (df["month_name"] == selected_month)
    ].copy()

    if selected_week != "All Weeks":
        filtered_df = filtered_df[
            filtered_df["week_name"] == selected_week
        ].copy()

    engineer_df = filtered_df.copy()

    engineer_df["first engineer(india team)"] = (
        engineer_df["first engineer(india team)"]
        .astype("string")
        .str.strip()
    )

    engineer_df["status"] = (
        engineer_df["status"]
        .fillna("Ticket Status Unassigned")
        .astype(str)
        .str.strip()
        .replace(
            ["", "nan", "None"],
            "Ticket Status Unassigned"
        )
    )

    engineer_df = engineer_df[
        engineer_df["first engineer(india team)"].notna() &
        (engineer_df["first engineer(india team)"] != "") &
        (~engineer_df["first engineer(india team)"].isin(
            ["nan", "None", "Ticket Status Unassigned"]
        ))
    ].copy()

    eng_status = (
        engineer_df
        .groupby(
            ["first engineer(india team)", "status"],
            dropna=False
        )
        .size()
        .reset_index(name="count")
    )

    fig_bar = px.bar(
        eng_status,
        x="first engineer(india team)",
        y="count",
        color="status",
        text="count",
        barmode="stack",
        title="Cases by Engineer and Status",
        color_discrete_map={
            "Closed": "blue",
            "Ongoing": "green",
            "Pending on Infra": "orange",
            "Pending on Manufactures": "yellow",
            "Pending on Universe": "orange",
            "Not Started": "pink",
            "Ticket Status Unassigned": "black"
        }
    )

    fig_bar.update_traces(textposition="inside")

    fig_bar.update_layout(
        xaxis_title="Engineer",
        yaxis_title="Number of Cases",
        legend_title="Status"
    )

    with chart_col:
        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )


elif selected_section == "Engineer Yearly Performance":
    # ============================================================
    # ENGINEER YEARLY PERFORMANCE
    # CURRENT YEAR: JANUARY 1 -> TODAY
    #
    # IMPORTANT:
    # This section intentionally ignores selected Month and Week.
    # It shows the engineer's complete current-year performance.
    # ============================================================

    st.subheader(
        "👨‍💻 Engineer Yearly Performance"
    )


    # ------------------------------------------------------------
    # Current calendar year
    # ------------------------------------------------------------

    current_year = datetime.now().year

    today = pd.Timestamp.today().normalize()


    # ------------------------------------------------------------
    # All cases from January 1 until today
    # ------------------------------------------------------------

    current_year_df = df[
        (df["year"] == current_year) &
        (df["effective_date"] <= today)
    ].copy()


    # ------------------------------------------------------------
    # Engineer list
    # ------------------------------------------------------------

    engineer_list = sorted(
        current_year_df[
            current_year_df[
                "first engineer(india team)"
            ].notna()
        ]["first engineer(india team)"]
        .astype(str)
        .str.strip()
        .loc[
            lambda x:
            ~x.isin(
                [
                    "",
                    "nan",
                    "None",
                    "Ticket Status Unassigned"
                ]
            )
        ]
        .unique()
    )


    # ------------------------------------------------------------
    # Engineer selection
    # ------------------------------------------------------------

    if engineer_list:

        # Show engineer selection in half of the dashboard
        selection_col, empty_col = st.columns(2)

        with selection_col:
            selected_engineer = st.selectbox(
                "Select Engineer",
                engineer_list,
                key="yearly_engineer"
            )


        # --------------------------------------------------------
        # Selected engineer data
        # --------------------------------------------------------

        engineer_year_df = current_year_df[
            current_year_df[
                "first engineer(india team)"
            ]
            .astype(str)
            .str.strip()
            .eq(selected_engineer)
        ].copy()


        # --------------------------------------------------------
        # NORMALIZE STATUS FOR CALCULATIONS
        # --------------------------------------------------------

        engineer_year_df["status_clean"] = (
            engineer_year_df["status"]
            .astype(str)
            .str.strip()
            .str.lower()
        )


    # --------------------------------------------------------
    # ============================================================
    # YEARLY ENGINEER PERFORMANCE
    # ============================================================

    # --------------------------------------------------------
    # STATUS COUNTS
    # --------------------------------------------------------

    year_total = len(engineer_year_df)

    year_closed = len(
        engineer_year_df[
            engineer_year_df["status_clean"] == "closed"
        ]
    )

    year_ongoing = len(
        engineer_year_df[
            engineer_year_df["status_clean"] == "ongoing"
        ]
    )

    year_infra = len(
        engineer_year_df[
            engineer_year_df["status_clean"] == "pending on infra"
        ]
    )

    year_manufactures = len(
        engineer_year_df[
            engineer_year_df["status_clean"] == "pending on manufactures"
        ]
    )

    year_unassigned = len(
        engineer_year_df[
            engineer_year_df["status_clean"] == "ticket status unassigned"
        ]
    )


    # --------------------------------------------------------
    # CLOSURE PERCENTAGE
    # Calculate this BEFORE creating the gauge
    # --------------------------------------------------------

    year_closure_rate = (
        (year_closed / year_total) * 100
        if year_total > 0
        else 0
    )


    # --------------------------------------------------------
    # LEFT SIDE - PERFORMANCE LIST | RIGHT SIDE - GAUGE
    # --------------------------------------------------------

    list_col, chart_col = st.columns([1.2, 1])


    # --------------------------------------------------------
    # LEFT SIDE - PERFORMANCE LIST IN TWO COLUMNS
    # --------------------------------------------------------

    with list_col:

        list_col1, list_col2 = st.columns(2)

        # First list column
        with list_col1:

            st.markdown(
                f"**Total Cases:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_total}</span>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"**Closed:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_closed}</span>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"**Ongoing:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_ongoing}</span>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"**Closure:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_closure_rate:.1f}%</span>",
                unsafe_allow_html=True
            )

        # Second list column
        with list_col2:

            st.markdown(
                f"**Pending:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_infra}</span>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"**Pending from Mfg:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_manufactures}</span>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"**Unassigned:** "
                f"<span style='font-size:24px;font-weight:700;'>{year_unassigned}</span>",
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # RIGHT SIDE - CLOSURE RATE GAUGE
    # --------------------------------------------------------

    with chart_col:

        fig_yearly_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=year_closure_rate,

                number={
                    "suffix": "%",
                    "font": {"size": 28}
                },

                title={
                    "text": "Yearly Closure Rate",
                    "font": {"size": 14}
                },

                gauge={
                    "axis": {
                        "range": [0, 100],
                        "ticksuffix": "%"
                    },

                    "bar": {
                        "color": "#00A86B"
                    },

                    "steps": [
                        {
                            "range": [0, 50],
                            "color": "#FCE8E6"
                        },
                        {
                            "range": [50, 80],
                            "color": "#FFF4CC"
                        },
                        {
                            "range": [80, 100],
                            "color": "#D9F2E6"
                        },
                    ],
                },
            )
        )

        fig_yearly_gauge.update_layout(
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            )
        )

        st.plotly_chart(
            fig_yearly_gauge,
            use_container_width=True,
            config={"displayModeBar": False}
        )


elif selected_section == "Pending Cases Aging Analysis":

    st.subheader("⏳ Pending Cases Aging Analysis")

    # ------------------------------------------------------------
    # YEAR / MONTH / WEEK FILTERS
    # Define filtered_df inside this section
    # ------------------------------------------------------------

    filter_col, empty_col = st.columns([1, 3])

    with filter_col:

        years = sorted(
            df["year"].dropna().unique().tolist(),
            reverse=True
        )

        if not years:
            st.warning("No date records are available.")
            st.stop()

        selected_year = st.selectbox(
            "Select Year",
            years,
            key="aging_year"
        )

        available_months = (
            df[df["year"] == selected_year]
            .sort_values("month")["month_name"]
            .dropna()
            .unique()
            .tolist()
        )

        if not available_months:
            st.warning("No month records are available for this year.")
            st.stop()

        current_month = datetime.now().strftime("%B")

        default_month_index = (
            available_months.index(current_month)
            if current_month in available_months
            else 0
        )

        selected_month = st.selectbox(
            "Select Month",
            available_months,
            index=default_month_index,
            key="aging_month"
        )

        available_weeks = (
            df[
                (df["year"] == selected_year) &
                (df["month_name"] == selected_month)
            ]
            .sort_values("week_no")["week_name"]
            .dropna()
            .unique()
            .tolist()
        )

        week_options = ["All Weeks"] + available_weeks

        selected_week = st.selectbox(
            "Select Week",
            week_options,
            key="aging_week"
        )

    # ------------------------------------------------------------
    # APPLY FILTERS
    # ------------------------------------------------------------

    filtered_df = df[
        (df["year"] == selected_year) &
        (df["month_name"] == selected_month)
    ].copy()

    if selected_week != "All Weeks":
        filtered_df = filtered_df[
            filtered_df["week_name"] == selected_week
        ].copy()

    # ------------------------------------------------------------
    # FILTER PENDING CASES
    # ------------------------------------------------------------

    pending_df = filtered_df[
        (filtered_df["end time"].isna()) &
        (
            filtered_df["status"]
            .astype(str)
            .str.strip()
            .str.lower()
            .ne("closed")
        )
    ].copy()

    if pending_df.empty:
        st.info("No pending cases found for the selected filters.")
        st.stop()

    # ------------------------------------------------------------
    # CALCULATE CASE AGE
    # ------------------------------------------------------------

    pending_df["effective_start_date"] = (
        pending_df["start date"]
        .fillna(pending_df["filled_date"])
    )

    today = pd.Timestamp.today().normalize()

    pending_df["case_days"] = (
        today - pending_df["effective_start_date"]
    ).dt.days

    # ------------------------------------------------------------
    # AGE BUCKETS
    # ------------------------------------------------------------

    pending_df["age_bucket"] = np.select(
        [
            pending_df["case_days"].between(0, 7),
            pending_df["case_days"].between(8, 15),
            pending_df["case_days"] > 15
        ],
        [
            "0-7 Days",
            "8-15 Days",
            ">15 Days"
        ],
        default="Unknown"
    )

    # ------------------------------------------------------------
    # GROUP BY ENGINEER + AGE BUCKET
    # ------------------------------------------------------------

    pending_summary = (
        pending_df
        .groupby(
            [
                "first engineer(india team)",
                "age_bucket"
            ],
            dropna=False
        )
        .size()
        .reset_index(name="count")
    )

    pending_summary = pending_summary[
        pending_summary["count"] > 0
    ]
    # ------------------------------------------------------------
    # PENDING AGING CHART - NAVIGATION SECTION
    # ------------------------------------------------------------

    if pending_summary.empty:
        st.info("No pending cases available for the selected filters.")

    else:
        fig_pending = px.bar(
            pending_summary,
            x="first engineer(india team)",
            y="count",
            color="age_bucket",
            text="count",
            barmode="stack",
            title="Pending Cases Aging Analysis",
            color_discrete_map={
                "0-7 Days": "blue",
                "8-15 Days": "orange",
                ">15 Days": "red",
                "Unknown": "gray"
            }
        )

        fig_pending.update_traces(
            textposition="inside"
        )

        fig_pending.update_layout(
            xaxis_title="Engineer",
            yaxis_title="Number of Pending Cases",
            legend_title="Case Age"
        )

        st.plotly_chart(
            fig_pending,
            use_container_width=True
        )
