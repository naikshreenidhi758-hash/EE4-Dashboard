import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(
    page_title="Case Processing Dashboard",
    layout="wide"
)

st.title("🇮🇳 INDIA Project - Case Processing Status 📋")

# Read Excel
df = pd.read_excel(
    "India project synchronous.xlsx",
    sheet_name="CASE processing"
)


# Clean Column Names
df.columns = df.columns.str.strip().str.lower()

# Clean Engineer Column
df["first engineer(india team)"] = (
    df["first engineer(india team)"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace("", "Unassigned")
)


# Clean Status Column
df["status"] = (
    df["status"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)


# Convert Dates
df["start date"] = pd.to_datetime(
    df["start date"],
    errors="coerce"
)

df["end time"] = pd.to_datetime(
    df["end time"],
    errors="coerce"
)

# Engineer vs Status 
eng_status = (
    df.groupby(
        ["first engineer(india team)", "status"]
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
    title="Cases by Engineer and Status 📊",
    color_discrete_map={
        "Closed": "blue",
        "Pending": "orange",
        "In Progress": "green",
        "Unassigned": "red"
    }
)

fig_bar.update_traces(
    textposition="inside"
)

# Clean Priority Column
df["priority"] = (
    df["priority"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# Priority Pie Chart
priority_count = (
    df["priority"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .value_counts()
    .reset_index()
)

priority_count.columns = [
    "Priority",
    "Count"
]




# Convert register time to datetime
filtered_df["status"] = pd.to_datetime(
    filtered_df["status"],
    errors="coerce"
)

# Available years
years = sorted(
   filtered_df["status"]
   .dt.year
   .dropna()
   .unique(),
    reverse=True
)

current_month = pd.Timestamp.now().year

if len(months) > 0:

    selected_month = st.selectbox(
        "Select month",
            years,
            index=months.index(current_month)
             if current_month in month else 0
    )

    # Filter selected month
    month_df = filtered_df[
        filtered_df["status"].dt.month == selected_month
    ].copy()

    # Month Name
    month_df["Month"] = month_df["status"].dt.strftime("%b")

    # Open / Closed Group
        month_df["Status Group"] = (
            month_df["case state"]
            .astype(str)
            .str.strip()
            .str.lower()
            .apply(
                    
            )
        )

    # Monthly Summary
    monthly_status = (
        year_df.groupby(
            ["Month", "Status Group"]
        )
        .size()
        .reset_index(name="Count")
    )

    # Month Order
    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

            monthly_status["Month"] = pd.Categorical(
                monthly_status["Month"],
                categories=month_order,
                ordered=True
            )

            monthly_status = monthly_status.sort_values("Month")

            fig2 = px.bar(
                monthly_status,
                x="Month",
                y="Count",
                color="Status Group",
                barmode="group",
                title=f"Open vs Closed Tickets - {selected_year}"
            )

            st.plotly_chart(fig2, use_container_width=True)

fig_pie = px.pie(
    priority_count,
    names="Priority",
    values="Count",
    title="Projects by Priority",
    color="Priority",
    color_discrete_map={
        "High": "red",
        "Medium": "orange",
        "Low": "green",
        
    }
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label"
)


# Show Side by Side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# Pending Cases Aging Analysis

# Cases where End Time is blank
pending_df = df[df["end time"].isna()].copy()

# Age calculation
today = pd.Timestamp.today().normalize()

pending_df["case_days"] = (
    today - pending_df["start date"]
).dt.days

# Buckets
pending_df["age_bucket"] = pd.cut(
    pending_df["case_days"],
    bins=[-1, 7, 15, float("inf")],
    labels=[
        "0-7 Days",
        "8-15 Days",
        ">15 Days"
    ]
)

# Engineer + Bucket summary
pending_summary = (
    pending_df.groupby(
        ["first engineer(india team)", "age_bucket"],
        observed=False
    )
    .size()
    .reset_index(name="count")
)

# Remove zero counts
pending_summary = pending_summary[
    pending_summary["count"] > 0
]

# Chart
fig_pending = px.bar(
    pending_summary,
    x="first engineer(india team)",
    y="count",
    color="age_bucket",
    text="count",
    barmode="stack",
    title="Pending cases ",
    color_discrete_map={
        "0-7 Days": "green",
        "8-15 Days": "orange",
        ">15 Days": "red"
    }
)

fig_pending.update_traces(
    textposition="inside"
)

st.plotly_chart(
    fig_pending,
    use_container_width=True
)


# Optional Data Preview
with st.expander("View Raw Data"):
    st.dataframe(df)
