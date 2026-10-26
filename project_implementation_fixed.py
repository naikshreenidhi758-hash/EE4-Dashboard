import re
from datetime import date
from pathlib import Path

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

# Load the workbook from the same folder as this Python script, not the
# PowerShell current working directory.
EXCEL_PATH = Path(__file__).resolve().parent / "India project synchronous.xlsx"

try:
    if not EXCEL_PATH.exists():
        st.error(
            "Excel workbook not found. Put 'India project synchronous.xlsx' "
            "in the same folder as this Python script."
        )
        st.caption(f"Expected file location: {EXCEL_PATH}")
        st.stop()

    df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="Project implementation"
    )
except Exception as exc:
    st.error(f"Could not read the Excel file: {exc}")
    st.caption(f"Workbook path checked: {EXCEL_PATH}")
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

network_col = find_column(
    columns,
    ["Network Engineer", "Network Engg", "Network Engineer Name"]
)

server_col = find_column(
    columns,
    ["Server Engineer", "Server Engg", "Server Engineer Name"]
)

project_name_col = find_column(
    columns,
    ["Project name", "Project Title"]
)

manager_col = find_column(
    columns,
    ["Project Manager"]
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

# Network/Server Engineer columns are optional; the dashboard can still
# render project details if the workbook uses different header names.
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


# ============================================================
# FILTERS: 1. ALL PROJECTS  2. NETWORK ENGINEER  3. SERVER ENGINEER
# ============================================================
st.subheader("Select project filters")

col_project, col_network, col_server = st.columns(3)
project_codes = sorted(df["_project_code_display"].dropna().unique().tolist())

with col_project:
    selected_project = st.selectbox(
        "1. All projects",
        ["All projects"] + project_codes,
        key="filter_project_code",
    )

network_options = sorted(
    df[network_col].dropna().astype(str).str.strip().replace("", pd.NA).dropna().unique().tolist()
) if network_col is not None else []
with col_network:
    selected_network = st.selectbox(
        "2. Network engineer",
        ["All network engineers"] + network_options,
        key="filter_network_engineer",
    )

if server_col is not None:
    server_options = sorted(
        df[server_col].dropna().astype(str).str.strip().replace("", pd.NA).dropna().unique().tolist()
    )
else:
    server_options = []
with col_server:
    selected_server = st.selectbox(
        "3. Server engineer",
        ["All server engineers"] + server_options,
        key="filter_server_engineer",
    )

# Apply all three filters consistently to the project tables.
filtered = df.copy()
if selected_project != "All projects":
    filtered = filtered[filtered["_project_code_display"] == selected_project]
if selected_network != "All network engineers" and network_col is not None:
    filtered = filtered[filtered[network_col].astype(str).str.strip() == selected_network]
if selected_server != "All server engineers" and server_col is not None:
    filtered = filtered[filtered[server_col].astype(str).str.strip() == selected_server]

# Identify projects that are not fully complete.
detected_stage_columns = [col for col in stage_columns.values() if col is not None]
if detected_stage_columns:
    pending_mask = filtered.apply(
        lambda row: any(
            normalize_status(row[col]) != "Completed"
            for col in detected_stage_columns
        ),
        axis=1,
    )
    pending_df = filtered[pending_mask].copy()
else:
    pending_df = filtered.iloc[0:0].copy()

# ============================================================
# LAYOUT: 4. TOTAL PROJECTS | 5. PROJECT DETAILS
#          6. PENDING PROJECTS | 7. IMPLEMENTATION CHECKLIST
# ============================================================
row_top_left, row_top_right = st.columns([1, 1.25], gap="large")
row_bottom_left, row_bottom_right = st.columns([1, 1.25], gap="large")

# -----------------------------
# 4. Total projects for selected engineer + project dropdown
# -----------------------------
with row_top_left:
    st.subheader("4. Total Projects for selected engineer")
    engineer_projects = filtered.copy()

    list_columns = [project_col]
    if network_col and network_col not in list_columns:
        list_columns.append(network_col)
    if server_col and server_col not in list_columns:
        list_columns.append(server_col)

    project_list = engineer_projects[list_columns].copy()
    project_list.columns = [
        "Project Number" if col == project_col else
        "Network Engineer" if col == network_col else
        "Server Engineer" if col == server_col else str(col)
        for col in project_list.columns
    ]
    st.dataframe(
        project_list.fillna(""),
        use_container_width=True,
        hide_index=True,
        height=260,
    )

    # This dropdown is directly below the Total Projects table.
    available_codes = sorted(filtered["_project_code_display"].dropna().unique().tolist())
    all_codes = sorted(df["_project_code_display"].dropna().unique().tolist())
    if not available_codes:
        st.warning("No projects match the selected filters. Change the filters above.")
        detail_project = None
    else:
        prior_pending = st.session_state.get("selected_pending_project")
        current_choice = st.session_state.get("detail_project_code")
        if prior_pending in available_codes:
            default_project = prior_pending
        elif current_choice in available_codes:
            default_project = current_choice
        elif selected_project in available_codes:
            default_project = selected_project
        else:
            default_project = available_codes[0]

        # Set the default before creating the selectbox. This avoids stale
        # values when a different pending row is selected.
        if st.session_state.get("detail_project_code") != default_project:
            st.session_state["detail_project_code"] = default_project

        # Consume the pending-row selection once so the user can still change
        # the dropdown manually afterwards.
        if prior_pending in available_codes:
            st.session_state.pop("selected_pending_project", None)

        detail_project = st.selectbox(
            "Choose project number for details",
            available_codes,
            key="detail_project_code",
        )

# Resolve selected project row once, for both details and checklist.
project_row = None
start_date = pd.NaT
if detail_project is not None:
    detail_rows = df[df["_project_code_display"] == detail_project]
    if not detail_rows.empty:
        project_row = detail_rows.iloc[0]
        start_date = safe_date(project_row[plan_date_col]) if plan_date_col else pd.NaT

# -----------------------------
# 5. Project details
# -----------------------------
with row_top_right:
    st.subheader("5. Project Details")
    if project_row is None:
        st.info("Select a project using the dropdown under Total Projects.")
    else:
        details_a, details_b = st.columns(2)
        with details_a:
            st.markdown("**Project Code**")
            st.write(display_value(project_row[project_col]))
            st.markdown("**Project Name**")
            st.write(display_value(project_row[project_name_col]) if project_name_col else "—")
            st.markdown("**Network Engineer**")
            st.write(display_value(project_row[network_col]) if network_col else "—")
        with details_b:
            st.markdown("**Project Manager**")
            st.write(display_value(project_row[manager_col]) if manager_col else "—")
            st.markdown("**Server Engineer**")
            st.write(display_value(project_row[server_col]) if server_col else "—")
            st.markdown("**Plan Start Date**")
            st.write(start_date.strftime("%d-%m-%Y") if not pd.isna(start_date) else "—")


# -----------------------------
# 6. Pending projects
# -----------------------------
with row_bottom_left:
    st.subheader("6. Pending Projects")
    pending_columns = {"Project Number": "_project_code_display"}
    if project_name_col is not None:
        pending_columns["Project Name"] = project_name_col
    pending_table = pending_df[list(pending_columns.values())].copy()
    pending_table.columns = list(pending_columns.keys())
    pending_table = pending_table.drop_duplicates(subset=["Project Number"]).reset_index(drop=True)

    if pending_table.empty:
        st.success("No pending projects found for the selected filters.")
    else:
        st.caption("Select a row to show its details and checklist.")
        pending_selection = st.dataframe(
            pending_table,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="pending_projects_table",
        )
        selected_rows = pending_selection.selection.rows
        if selected_rows:
            clicked_project = pending_table.iloc[selected_rows[0]]["Project Number"]
            # Clicking a pending row sets the dropdown value for the next rerun.
            if (
                clicked_project in available_codes
                and st.session_state.get("detail_project_code") != clicked_project
            ):
                # Apply this on the next rerun before the dropdown is created.
                st.session_state["selected_pending_project"] = clicked_project
                st.rerun()

# -----------------------------
# 7. Implementation checklist (beside Pending Projects)
# -----------------------------
with row_bottom_right:
    st.subheader("7. Implementation Checklist")
    if project_row is None:
        st.info("Select a project using the dropdown under Total Projects.")
    else:
        # Six checklist items displayed in two columns across three rows.
        stage_items = list(stage_columns.items())
        for index in range(0, len(stage_items), 2):
            stage_pair = stage_items[index:index + 2]
            checklist_cols = st.columns(2, gap="medium")
            for checklist_col, (stage, source_col) in zip(checklist_cols, stage_pair):
                with checklist_col:
                    st.markdown(f"**{stage}**")
                    if source_col is None:
                        st.caption("Column not found in workbook")
                    else:
                        status = normalize_status(project_row[source_col])
                        if status == "Completed":
                            st.success("✅ Completed")
                        elif status == "Under Implementation":
                            st.warning("🟡 Under Implementation")
                        else:
                            st.info("⏳ Pending")

        # Overall status and pending duration belong below the checklist.
        detected_statuses = [
            normalize_status(project_row[col])
            for col in stage_columns.values()
            if col is not None
        ]
        all_stages_completed = (
            bool(detected_statuses)
            and all(status == "Completed" for status in detected_statuses)
        )

        st.divider()
        st.markdown("### Overall Project Status")
        if all_stages_completed:
            st.success("🎉 Completed")
        else:
            st.warning("🟡 In progress / Pending")
            if pd.isna(start_date):
                st.metric("Pending duration", "Unavailable")
                st.caption("A valid Plan Start Date is needed to calculate duration.")
            else:
                days_pending = max(0, (date.today() - start_date.date()).days)
                st.metric("Pending duration", f"{days_pending} days")

# -----------------------------
# Full source data
# -----------------------------
with st.expander("View uploaded source data"):
    st.dataframe(df.drop(columns=["_project_code_display"], errors="ignore"), use_container_width=True, hide_index=True)

st.caption("Status rule: Completed values show a check mark; blank or explicitly pending values show Pending; other non-empty values show Under Implementation.")