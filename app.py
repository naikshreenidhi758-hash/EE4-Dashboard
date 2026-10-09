import re
from datetime import date

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Project Implementation",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Project Implementation")


# -----------------------------
# Helpers
# -----------------------------
def clean_name(value):
    """Normalize a column name for flexible matching."""
    return re.sub(r"[^a-z0-9]", "", str(value).strip().lower())


def find_column(columns, candidates):
    normalized = {clean_name(col): col for col in columns}
    for candidate in candidates:
        key = clean_name(candidate)
        if key in normalized:
            return normalized[key]

    # Allow a column name to contain a candidate phrase.
    for col in columns:
        col_key = clean_name(col)
        for candidate in candidates:
            candidate_key = clean_name(candidate)
            if candidate_key and candidate_key in col_key:
                return col
    return None


def display_value(value):
    if pd.isna(value) or str(value).strip() == "":
        return "—"
    if isinstance(value, pd.Timestamp):
        return value.strftime("%d-%m-%Y")
    return str(value).strip()


def normalize_status(value):
    """Return Completed, Under Implementation, or Pending."""
    if pd.isna(value) or str(value).strip() == "":
        return "Pending"

    value_text = str(value).strip().lower()
    if value_text in {"completed", "complete", "done", "closed", "yes", "✔", "✓"}:
        return "Completed"
    if value_text in {"pending", "not started", "not yet started", "na", "n/a", "-"}:
        return "Pending"
    return "Under Implementation"


def status_label(value):
    status = normalize_status(value)
    if status == "Completed":
        return "✅ Completed"
    if status == "Under Implementation":
        return "🟡 Under Implementation"
    return "⏳ Pending"


def safe_date(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NaT
    return pd.to_datetime(value, errors="coerce", dayfirst=True)

# ============================================================
# LOAD EXCEL
# ============================================================

import pandas as pd
import streamlit as st

try:
    df = pd.read_excel(
        "India project synchronous.xlsx",
        sheet_name="Project implementation"
    )

except Exception as exc:
    st.error(f"Could not read the Excel file: {exc}")
    st.stop()


# ============================================================
# VALIDATE DATA
# ============================================================

if df.empty:
    st.warning("The Excel sheet has no data rows.")
    st.stop()

# Remove whitespace from column names
df.columns = [str(col).strip() for col in df.columns]

# Remove completely empty rows
df = df.dropna(how="all").copy()

if df.empty:
    st.warning("The Excel sheet has no usable data rows.")
    st.stop()


# ============================================================
# IDENTIFY COLUMNS
# ============================================================

columns = list(df.columns)

project_col = find_column(
    columns,
    ["Project number", "Project code", "Project No", "Project ID", "Project"]
)

manager_col = find_column(
    columns,
    ["Project Manager", "Project Owner", "Manager"]
)

server_col = find_column(
    columns,
    ["Server Engineer", "Server Engg", "Server Engineer Name"]
)

network_engineer_col = find_column(
    columns,
    ["Network Engineer", "Network Engg"]
)

server_engineer_col = find_column(
    columns,
    ["Server Engineer", "Server Engg"]
)

plan_date_col = find_column(
    columns,
    ["Plan start date", "Planned start date", "Start date", "Plan Date"]
)

priority_col = find_column(
    columns,
    ["Priority Wise", "Priority", "Project Status", "Overall Status"]
)


# ============================================================
# IMPLEMENTATION STATUS COLUMNS
# ============================================================

stage_candidates = {
    "BOM": ["BOM"],
    "Jump server Installation": [
        "Jump server Installation",
        "Jump Server Install",
        "Jump Server Installation"
    ],
    "Radius Server": ["Radius Server", "RADIUS Server"],
    "Wiring": ["Wiring"],
    "Network": ["Network"],
    "Server": ["Server"],
}

stage_columns = {
    label: find_column(columns, candidates)
    for label, candidates in stage_candidates.items()
}


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

missing_core = []

if project_col is None:
    missing_core.append("Project number / Project code")

if manager_col is None:
    missing_core.append("Project Manager")

if missing_core:
    st.error(
        "Required columns not found: "
        + ", ".join(missing_core)
    )

    st.write("Available Excel columns:", columns)
    st.stop()


# ============================================================
# PREPARE PROJECT CODES
# ============================================================

df["_project_code_display"] = (
    df[project_col].apply(display_value)
)

# Remove rows without a project code
df = df[
    df["_project_code_display"] != "—"
].copy()

if df.empty:
    st.warning("No project codes were found in the Excel sheet.")
    st.stop()


# ============================================================
# SERVER ENGINEER COLUMN
# ============================================================

if server_col is None:
    st.warning(
        "The Server Engineer column was not detected. "
        "Please select the correct column below."
    )

    engineer_options = [None] + columns

    chosen = st.selectbox(
        "Select Server Engineer column",
        engineer_options,
        format_func=lambda x: (
            "— Not available —" if x is None else x
        )
    )

    server_col = chosen


# -----------------------------
# Filters in one row
# -----------------------------
st.subheader("Select project")

col_project, col_manager, col_engineer = st.columns(3)

project_codes = sorted(df["_project_code_display"].dropna().unique().tolist())
with col_project:
    selected_project = st.selectbox("Project code", ["All projects"] + project_codes)

managers = sorted(df[manager_col].dropna().astype(str).str.strip().replace("", pd.NA).dropna().unique().tolist())
with col_manager:
    selected_manager = st.selectbox("Project Manager", ["All managers"] + managers)

if server_col is not None:
    engineers = sorted(df[server_col].dropna().astype(str).str.strip().replace("", pd.NA).dropna().unique().tolist())
else:
    engineers = []
with col_engineer:
    selected_engineer = st.selectbox("Server Engineer", ["All engineers"] + engineers)

filtered = df.copy()
if selected_project != "All projects":
    filtered = filtered[filtered["_project_code_display"] == selected_project]
if selected_manager != "All managers":
    filtered = filtered[filtered[manager_col].astype(str).str.strip() == selected_manager]
if selected_engineer != "All engineers" and server_col is not None:
    filtered = filtered[filtered[server_col].astype(str).str.strip() == selected_engineer]

# -----------------------------
# Engineer project list + project detail side by side
# -----------------------------
left, right = st.columns([1, 1.65], gap="large")

with left:
    st.subheader("Total Projects for selected engineer")
    engineer_projects = df.copy()
    if selected_engineer != "All engineers" and server_col is not None:
        engineer_projects = engineer_projects[
            engineer_projects[server_col].astype(str).str.strip() == selected_engineer
        ]
    if selected_manager != "All managers":
        engineer_projects = engineer_projects[
            engineer_projects[manager_col].astype(str).str.strip() == selected_manager
        ]
    if selected_project != "All projects":
        engineer_projects = engineer_projects[
            engineer_projects["_project_code_display"] == selected_project
        ]

    list_columns = [project_col]
    if manager_col and manager_col not in list_columns:
        list_columns.append(manager_col)
    if server_col and server_col not in list_columns:
        list_columns.append(server_col)

    project_list = engineer_projects[list_columns].copy()
    project_list.columns = [
        "Project code" if col == project_col else
        "Project Manager" if col == manager_col else
        "Server Engineer" if col == server_col else str(col)
        for col in project_list.columns
    ]
    project_list = project_list.fillna("")
    st.dataframe(project_list, use_container_width=True, hide_index=True, height=300)

    available_codes = sorted(engineer_projects["_project_code_display"].dropna().unique().tolist())
    if not available_codes:
        st.warning("No projects match the selected filters.")
        st.stop()

    # This second selector controls which project's full details appear.
    default_index = available_codes.index(selected_project) if selected_project in available_codes else 0
    detail_project = st.selectbox(
        "Choose a project to view full details",
        available_codes,
        index=default_index,
        key="detail_project_code",
    )

with right:
    st.subheader("Project details")
    detail_rows = df[df["_project_code_display"] == detail_project]
    if selected_manager != "All managers":
        detail_rows = detail_rows[detail_rows[manager_col].astype(str).str.strip() == selected_manager]
    if selected_engineer != "All engineers" and server_col is not None:
        detail_rows = detail_rows[detail_rows[server_col].astype(str).str.strip() == selected_engineer]

    if detail_rows.empty:
        st.warning("No project row matches the current filters. Change the filters on the left.")
        st.stop()

    # If duplicate codes exist, show the first matching row and let the user know.
    project_row = detail_rows.iloc[0]
    if len(detail_rows) > 1:
        st.warning(f"{len(detail_rows)} rows have this project code under the current filters. Showing the first matching row.")

    # Top-level details
    a, b = st.columns(2)
    with a:
        st.markdown("**Project code**")
        st.write(display_value(project_row[project_col]))
        st.markdown("**Project Manager**")
        st.write(display_value(project_row[manager_col]))
        st.markdown("**Server Engineer**")
        st.write(display_value(project_row[server_col]) if server_col else "—")
    with b:
        st.markdown("**Network Engineer**")
        st.write(display_value(project_row[network_engineer_col]) if network_engineer_col else "—")
        st.markdown("**Server Engineer**")
        st.write(display_value(project_row[server_engineer_col]) if server_engineer_col else "—")
        st.markdown("**Plan start date**")
        start_date = safe_date(project_row[plan_date_col]) if plan_date_col else pd.NaT
        st.write(start_date.strftime("%d-%m-%Y") if not pd.isna(start_date) else "—")

    # Status for each implementation stage.
    st.markdown("### Implementation checklist")
    stage_statuses = {}
    for stage, col in stage_columns.items():
        if col is None:
            stage_statuses[stage] = "Column not found"
        else:
            stage_statuses[stage] = normalize_status(project_row[col])

    stage_items = list(stage_statuses.items())
    for start in range(0, len(stage_items), 2):
        pair = stage_items[start:start + 2]
        stage_cols = st.columns(len(pair))
        for box, (stage, status) in zip(stage_cols, pair):
            with box:
                st.markdown(f"**{stage}**")
                if status == "Completed":
                    st.success("✅ Completed")
                elif status == "Under Implementation":
                    st.warning("🟡 Under Implementation")
                elif status == "Pending":
                    st.info("⏳ Pending")
                else:
                    st.caption("Column not found in workbook")

    # Project is considered completed only when every detected implementation stage is completed.
    detected_statuses = [
        stage_statuses[stage]
        for stage in stage_statuses
        if stage_columns[stage] is not None
    ]
    all_stages_found = len(detected_statuses) > 0
    project_completed = all_stages_found and all(status == "Completed" for status in detected_statuses)

    if project_completed:
        st.success("🎉 Overall project status: Completed")
    else:
        st.warning("Overall project status: In progress / Pending")

    if not project_completed:
        if pd.isna(start_date):
            st.metric("Pending duration", "Unavailable")
            st.caption("A valid Plan start date is needed to calculate the number of days.")
        else:
            days_pending = max(0, (date.today() - start_date.date()).days)
            st.metric("Pending duration", f"{days_pending} days")
            st.caption("Calculated from the plan start date to today because not all implementation stages are completed.")

# -----------------------------
# Full source data
# -----------------------------
with st.expander("View uploaded source data"):
    st.dataframe(df.drop(columns=["_project_code_display"], errors="ignore"), use_container_width=True, hide_index=True)

st.caption("Status rule: Completed values show a check mark; blank or explicitly pending values show Pending; other non-empty values show Under Implementation.")
