import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="HBR Uber Case Study Analysis Dashboard",
    layout="wide"
)

# ---------- HEADER ----------
with st.container():
    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_left:
        # Replace with your logo path or URL
        st.image("images/uber_logo.png", use_container_width=True)

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
        # Replace with your logo path or URL
        st.image("images/rice_logo.png", use_container_width=True)

st.markdown("---")

# ---------- TABS ----------
tab_metadata, tab_dict, tab_viz = st.tabs(
    ["Metadata", "Data Dictionary", "Data Visualizations"]
)

# ===== TAB 1: METADATA =====
with tab_metadata:
    st.header("📄 Metadata")

    # Replace this with your real metadata text
    st.markdown(
        """
**Harvard Business School Case:** 619-003  
**Courseware:** 619-702  
**Revision Date:** August 6, 2020  

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

    # Example layout – replace with your own table or markdown
    # If you already have a dataframe, just do: st.dataframe(df_dictionary)
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

# ===== TAB 3: DATA VISUALIZATIONS =====
with tab_viz:
    st.header("📊 Data Visualizations")

    st.subheader("Data Preview")
    st.write("Upload or load your data here and show a preview.")

    # Example: file uploader + table (pure Streamlit)
    uploaded_file = st.file_uploader("Upload the HBR Uber Excel file", type=["xlsx", "xls", "csv"])

    if uploaded_file is not None:
        import pandas as pd  # only for data; layout is Streamlit-only

        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(("xlsx", "xls")) else pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        st.subheader("Simple Time Series Example")
        # Replace column names with your actual ones
        time_col = "period_start"
        value_col = "trips_pool"

        if time_col in df.columns and value_col in df.columns:
            ts_df = df[[time_col, value_col]].set_index(time_col)
            st.line_chart(ts_df)
        else:
            st.info("Once your data has `period_start` and `trips_pool` columns, a time series will appear here.")
    else:
        st.info("Upload the dataset to see tables and charts.")
