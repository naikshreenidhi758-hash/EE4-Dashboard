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
# HEADER
# ============================================================

st.image("envision.png", use_container_width=True)
st.title("INDIA Project - Case Processing Status 📋")


# ============================================================
# LOAD AND CLEAN EXCEL DATA
# ============================================================

df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)

df.columns = df.columns.str.strip().str.lower()

# Engineer name: keep missing names missing
df["first engineer(india team)"] = (
    df["first engineer(india team)"]
    .astype("string")
    .str.strip()
)

# Status: use the unassigned label for blank status values
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

df["priority"] = (
    df["priority"]
    .fillna("Ticket Status Unassigned")
    .astype(str)
    .str.strip()
    .str.title()
)

# Convert date columns
for date_col in ["start date", "filled_date", "end time"]:
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

# Effective date uses Start Date first, then Filled Date
df["effective_date"] = (
    df["start date"].fillna(df["filled_date"])
)

# Calendar fields
df["year"] = df["effective_date"].dt.year
df["month"] = df["effective_date"].dt.month
df["month_name"] = df["effective_date"].dt.strftime("%B")
df["week_no"] = (
    df["effective_date"]
    .dt.isocalendar()
    .week
    .astype("Int64")
)
df["week_name"] = "Week " + df["week_no"].astype("string")


# ============================================================
# SIDEBAR FILTERS - SHARED BY FILTERED SECTIONS
# ============================================================

st.sidebar.markdown("## 🔎 Dashboard Filters")

years = sorted(
    df["year"].dropna().unique().tolist(),
    reverse=True
)

if not years:
    st.error("No valid dates were found in the Start Date / Filled Date columns.")
    st.stop()

selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    key="dashboard_year"
)

year_df = df[df["year"] == selected_year].copy()

available_months = (
    year_df.sort_values("month")["month_name"]
    .dropna()
    .unique()
    .tolist()
)

if not available_months:
    st.warning("No months are available for the selected year.")
    st.stop()

current_month = datetime.now().strftime("%B")
default_month_index = (
    available_months.index(current_month)
    if current_month in available_months
    else 0
)

selected_month = st.sidebar.selectbox(
    "Select Month",
    available_months,
    index=default_month_index,
    key="dashboard_month"
)

month_df = year_df[
    year_df["month_name"] == selected_month
].copy()

available_weeks = (
    month_df.sort_values("week_no")["week_name"]
    .dropna()
    .unique()
    .tolist()
)

week_options = ["All Weeks"] + available_weeks

selected_week = st.sidebar.selectbox(
    "Select Week",
    week_options,
    key="dashboard_week"
)

filtered_df = month_df.copy()

if selected_week != "All Weeks":
    filtered_df = filtered_df[
        filtered_df["week_name"] == selected_week
    ].copy()


# ============================================================
# GLOBAL KPI METRICS - COMPLETE DATASET
# These KPIs are not changed by Year / Month / Week filters.
# ============================================================

total_cases = len(df)

closed_cases = (
    df["status"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("closed")
    .sum()
)

pending_cases = total_cases - closed_cases

closure_rate = (
    (closed_cases / total_cases) * 100
    if total_cases > 0
    else 0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("📋 Total Cases", total_cases)

with kpi2:
    st.metric("⏳ Pending Cases", pending_cases)

with kpi3:
    st.metric("✅ Closed Cases", int(closed_cases))

with kpi4:
    st.metric("📈 Closure %", f"{closure_rate:.1f}%")


# ============================================================
# ALL-TICKET STATUS SUMMARY
# ============================================================

with st.expander("📊 Overall Ticket Status - All Tickets", expanded=False):
    status_summary = (
        df.groupby("status")
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


# ============================================================
# DASHBOARD NAVIGATION
# The radio menu is in the left dashboard column.
# Only the chosen section is displayed in the content column.
# ============================================================

nav_col, content_col = st.columns([1, 4], gap="large")

with nav_col:
    st.markdown("### 📌 Dashboard Navigation")

    selected_section = st.radio(
        "Choose a dashboard section",
        [
            "Status Cases by Engineer and Status",
            "Engineer Yearly Performance",
            "Pending Cases Aging Analysis"
        ],
        label_visibility="collapsed",
        key="dashboard_navigation"
    )

with content_col:

    # ========================================================
    # SECTION 1 - STATUS CASES BY ENGINEER AND STATUS
    # ========================================================

    if selected_section == "Status Cases by Engineer and Status":

        st.subheader("👨‍💻 Status Cases by Engineer and Status")

        st.caption(
            f"Showing {selected_month} {selected_year}"
            + (
                f" — {selected_week}"
                if selected_week != "All Weeks"
                else " — All Weeks"
            )
        )

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

        # Exclude blank engineer names from the engineer chart
        engineer_df = engineer_df[
            engineer_df["first engineer(india team)"].notna()
            & (engineer_df["first engineer(india team)"] != "")
            & (
                ~engineer_df["first engineer(india team)"].isin(
                    ["nan", "None", "Ticket Status Unassigned"]
                )
            )
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

        if eng_status.empty:
            st.info("No engineer status cases are available for the selected filters.")
        else:
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

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )


    # ========================================================
    # SECTION 2 - ENGINEER YEARLY PERFORMANCE
    # Current year Jan 1 through today; ignores Month / Week.
    # ========================================================

    elif selected_section == "Engineer Yearly Performance":

        st.subheader("👨‍💻 Engineer Yearly Performance")

        current_year = datetime.now().year
        today = pd.Timestamp.today().normalize()

        current_year_df = df[
            (df["year"] == current_year)
            & (df["effective_date"] <= today)
        ].copy()

        engineer_list = sorted(
            current_year_df[
                current_year_df["first engineer(india team)"].notna()
            ]["first engineer(india team)"]
            .astype(str)
            .str.strip()
            .loc[
                lambda values: ~values.isin(
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

        if not engineer_list:
            st.info("No engineer cases are available for the current year.")
        else:
            selection_col, spacer_col = st.columns([1, 1])

            with selection_col:
                selected_engineer = st.selectbox(
                    "Select Engineer",
                    engineer_list,
                    key="yearly_engineer"
                )

            engineer_year_df = current_year_df[
                current_year_df["first engineer(india team)"]
                .astype(str)
                .str.strip()
                .eq(selected_engineer)
            ].copy()

            engineer_year_df["status_clean"] = (
                engineer_year_df["status"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            year_total = len(engineer_year_df)

            year_closed = (
                engineer_year_df["status_clean"].eq("closed").sum()
            )

            year_ongoing = (
                engineer_year_df["status_clean"].eq("ongoing").sum()
            )

            year_infra = (
                engineer_year_df["status_clean"].eq("pending on infra").sum()
            )

            year_manufactures = (
                engineer_year_df[
                    "status_clean"
                ].eq("pending on manufactures").sum()
            )

            year_unassigned = (
                engineer_year_df[
                    "status_clean"
                ].eq("ticket status unassigned").sum()
            )

            year_closure_rate = (
                (year_closed / year_total) * 100
                if year_total > 0
                else 0
            )

            list_col, gauge_col = st.columns([1.2, 1])

            with list_col:
                list_col1, list_col2 = st.columns(2)

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

            with gauge_col:
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
                            "bar": {"color": "#00A86B"},
                            "steps": [
                                {"range": [0, 50], "color": "#FCE8E6"},
                                {"range": [50, 80], "color": "#FFF4CC"},
                                {"range": [80, 100], "color": "#D9F2E6"}
                            ]
                        }
                    )
                )

                fig_yearly_gauge.update_layout(
                    height=220,
                    margin=dict(l=10, r=10, t=40, b=10)
                )

                st.plotly_chart(
                    fig_yearly_gauge,
                    use_container_width=True,
                    config={"displayModeBar": False}
                )


    # ========================================================
    # SECTION 3 - PENDING CASES AGING ANALYSIS
    # Uses the selected Year / Month / Week filters.
    # ========================================================

    elif selected_section == "Pending Cases Aging Analysis":

        st.subheader("⏳ Pending Cases Aging Analysis")

        pending_df = filtered_df[
            (filtered_df["end time"].isna())
            & (
                filtered_df["status"]
                .astype(str)
                .str.strip()
                .str.lower()
                != "closed"
            )
        ].copy()

        pending_df["effective_start_date"] = (
            pending_df["start date"]
            .fillna(pending_df["filled_date"])
        )

        today = pd.Timestamp.today().normalize()

        pending_df["case_days"] = (
            today - pending_df["effective_start_date"]
        ).dt.days

        pending_df["age_bucket"] = np.select(
            [
                pending_df["case_days"].le(7),
                pending_df["case_days"].between(8, 15),
                pending_df["case_days"].gt(15)
            ],
            [
                "0-7 Days",
                "8-15 Days",
                ">15 Days"
            ],
            default="Unknown"
        )

        pending_summary = (
            pending_df
            .groupby(
                [
                    "first engineer(india team)",
                    "age_bucket"
                ],
                observed=False
            )
            .size()
            .reset_index(name="count")
        )

        pending_summary = pending_summary[
            pending_summary["count"] > 0
        ]

        if pending_summary.empty:
            st.info("No pending cases are available for the selected filters.")
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
                    ">15 Days": "red"
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
