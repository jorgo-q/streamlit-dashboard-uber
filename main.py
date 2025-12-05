import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- Page config ----------
st.set_page_config(
    page_title="HBR - Uber Case Study Analysis Dashboard",
    layout="wide"
)

# ---------- DATA LOADING (NEW) ----------
data_url = (
    "https://docs.google.com/spreadsheets/"
    "d/1fTpJACr1Ay6DEIgFxjFZF8LgEPiwwAFY/edit?usp=sharing&"
    "ouid=103457517634340619188&rtpof=true&sd=true"
)

@st.cache_data
def load_file(url: str):
    # Turn the "edit" URL into a direct xlsx export URL
    # (split on '/edit' to avoid issues with extra query params)
    modified_url = url.split("/edit")[0] + "/export?format=xlsx"

    # Load ALL sheets from the Excel file
    all_sheets = pd.read_excel(modified_url, sheet_name=None)
    return all_sheets

# Load once (cached)
data = load_file(data_url)
switchbacks_df = data["Switchbacks"]  # main data sheet
# If you want dictionary sheet later: dict_df = data["Data Dictionary"]

# ---------- HEADER ----------
with st.container():
    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_left:
        st.image("files/Uber-logo.png", use_container_width=True)

    with col_center:
        st.markdown(
            """
            <h1 style="text-align: center; margin-bottom: 0;">
                HBR - UBER Case Study Analysis Dashboard
            </h1>
            <p style="text-align: center; font-size: 1.05rem; margin-top: 0.35rem;">
                A simple dashboard built from a multi-sheet Excel file.
            </p>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.image("files/rice-logo.jpg", use_container_width=True)

st.markdown("---")

# ---------- TABS ----------
tab_metadata, tab_dict, tab_viz = st.tabs(
    ["Metadata", "Data Dictionary", "Data Visualizations"]
)

# ===== TAB 1: METADATA =====
with tab_metadata:
    st.header("📄 Metadata")

    st.markdown(
        """
**Harvard Business School Case:** 619-003    

This courseware was prepared solely as the basis for class discussion.  
It supplements *“Innovation at Uber: The Launch of Express POOL”* and contains:

- A **Switchbacks** sheet with simulated experiment data from Boston  
- A **Data Dictionary** sheet describing each variable  
- Additional information about rider wait times, driver earnings, and match performance
        """
    )

# ===== TAB 2: DATA DICTIONARY =====
with tab_dict:
    st.header("📚 Data Dictionary")

    # Option A: keep your static markdown table
    st.markdown(
        """
| Variable              | Type    | Definition |
|----------------------|---------|-----------|
| `city_id`            | String  | Location where the experiment took place (Boston). |
| `period_start`       | Date    | Start datetime of the 160-minute time period. |
| `wait_time`          | String  | `"2 mins"` (control) or `"5 mins"` (treatment). |
| `treat`              | Boolean | `TRUE` for treatment periods with 5-minute waits. |
| `commute`            | Boolean | `TRUE` during commute hours; `FALSE` otherwise. |
| `trips_pool`         | Numeric | Number of POOL trips completed in the period. |
| `trips_express`      | Numeric | Number of Express POOL trips completed. |
| `rider_cancellations`| Numeric | Trips cancelled by riders in the period. |
| `total_driver_payout`| Numeric | Total payout to drivers in the period. |
| `total_matches`      | Numeric | Completed trips matched with at least one other rider. |
        """,
        unsafe_allow_html=False,
    )

    # Option B (later): use the actual "Data Dictionary" sheet:
    # st.dataframe(dict_df)

# ===== TAB 3: DATA VISUALIZATIONS =====
with tab_viz:
    st.header("📊 Data Visualizations")

    st.subheader("Data Preview – Switchbacks Sheet")
    st.dataframe(switchbacks_df.head())

    # ---- Simple controls + time series example ----
    st.subheader("Time Series of Uber Metrics in Boston")

    # Choose metrics to plot
    numeric_cols = [
        "trips_pool",
        "trips_express",
        "rider_cancellations",
        "total_driver_payout",
        "total_matches",
    ]
    available_metrics = [c for c in numeric_cols if c in switchbacks_df.columns]

    selected_metrics = st.multiselect(
        "Select metrics to plot:",
        options=available_metrics,
        default=available_metrics[:3] if available_metrics else [],
    )

    if "period_start" in switchbacks_df.columns and selected_metrics:
        # Melt to long format for plotly express
        plot_df = switchbacks_df[["period_start"] + selected_metrics].melt(
            id_vars="period_start",
            value_vars=selected_metrics,
            var_name="metric",
            value_name="value",
        )

        fig = px.line(
            plot_df,
            x="period_start",
            y="value",
            color="metric",
            labels={"period_start": "Time", "value": "Value", "metric": "Metric"},
            title="Time Series of Uber Metrics in Boston",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Once `period_start` and numeric metric columns are present, a time series chart will appear here.")
