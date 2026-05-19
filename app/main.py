import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Fix local lookups across system boundary tracks
current_dir = Path(__file__).resolve().parent
root_path = str(current_dir.parent)
src_path = str(current_dir.parent / "src")
if root_path not in sys.path: sys.path.insert(0, root_path)
if src_path not in sys.path: sys.path.insert(0, src_path)

from medinsight.core.reporting import generate_pdf_report
from medinsight.core.analytics import generate_healthcare_insights, validate_dataset_schema
from medinsight.core.cleaning import DataCleaner
from medinsight.core.visualizations import suggest_charts_by_type, plot_histogram, plot_correlation
from medinsight.utils.helpers import get_dataset_profile, analyze_column_types
from app.styles import inject_custom_css

def main():
    st.set_page_config(page_title="MedInsight Engine", layout="wide", initial_sidebar_state="expanded")
    inject_custom_css()

    st.sidebar.title("🏥 MedInsight Core")
    st.sidebar.markdown("---")

    dataset_type = st.sidebar.selectbox(
        "Dataset Domain Profile Focus:",
        ["Select target profile...", "Patient Records", "Diabetes Dataset", "Heart Disease Dataset", 
         "Hospital Management Dataset", "Disease Statistics Dataset", "Medical Survey Dataset", "Generic Healthcare Dataset"]
    )

    if dataset_type == "Select target profile...":
        # Completely clear state if the user resets the selection dropdown
        st.session_state.pop("schema_error", None)
        st.session_state.pop("last_uploaded", None)
        st.session_state.pop("active_df", None)
        st.info("### 🚀 Portal Active\nPlease define your clinical context framework in the sidebar parameters panel to initialize tracking.")
        return

    uploaded_file = st.sidebar.file_uploader(f"Upload local target payload ({dataset_type})", type=["csv", "xlsx"])

    if not uploaded_file:
        # If a user removes a file, clean out all dependent session caches instantly
        st.session_state.pop("schema_error", None)
        st.session_state.pop("last_uploaded", None)
        st.session_state.pop("active_df", None)
        st.warning("📥 Operational buffer idle. Please load a corresponding dataset file structure to run analytical metrics.")
        return

    # CRITICAL FIX: Explicit State Reset on New Upload Detection
    if "last_uploaded" in st.session_state and st.session_state.last_uploaded != uploaded_file.name:
        st.session_state.pop("schema_error", None)
        st.session_state.pop("active_df", None)

    # Thread-Safe File Context Upload Sync + Core Guardrail Schema Check
    if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            # Run Schema Guardrail Validation
            is_valid, expected_keywords = validate_dataset_schema(df.columns.tolist(), dataset_type)
            
            if not is_valid:
                st.session_state.schema_error = {
                    "dataset_type": dataset_type,
                    "expected": expected_keywords,
                    "found": df.columns.tolist()
                }
                st.session_state.last_uploaded = uploaded_file.name # Mark processed to prevent infinite ingestion loops
            else:
                # Clear structural errors completely upon successful validation profile match
                st.session_state.pop("schema_error", None)
                st.session_state.raw_df = df
                st.session_state.active_df = df.copy()
                st.session_state.last_uploaded = uploaded_file.name
                
        except Exception as e:
            st.error(f"Operational File Ingestion Error: {e}")
            return

    # Handle soft-halt if dataset type validation fails
    if "schema_error" in st.session_state:
        err = st.session_state["schema_error"]
        st.error(f"🚨 **Dataset Mismatch Error Detected!**")
        st.warning(f"""
        You specified that you are uploading a **{err['dataset_type']}**, but the file headers do not look like they match this specific profile.
        
        * **Expected columns to contain clinical themes like:** `{', '.join(err['expected'])}`
        * **What we actually found in your file:** `{', '.join(err['found'][:6])}...`
        
        Please select a different profile focus in the sidebar or upload a matching data matrix to proceed.
        """)
        return

    # Clear Navigation Context Routing Configuration
    menu = st.sidebar.radio("Analysis Lifecycle Station:", ["1. Executive Summary Control", "2. Cleansing Workspace", "3. Distribution Explorations"])

    # Engine Core Computations
    profile = get_dataset_profile(st.session_state.active_df)
    types = analyze_column_types(st.session_state.active_df)
    current_insights = generate_healthcare_insights(st.session_state.active_df, dataset_type)

    # --- TAB 1: SUMMARY STATION ---
    if menu == "1. Executive Summary Control":
        st.header("📊 Executive Analytics Control Console")
        
        # High-Fidelity KPI Block Tracking Grid
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        m_col1.metric("Dataset Sample Depth", f"{profile['rows']:,} Rows")
        m_col2.metric("Dimensional Columns", profile['cols'])
        m_col3.metric("Missing Values", profile['missing_cells'])
        m_col4.metric("Cloned Duplicates", profile['duplicate_rows'])
        m_col5.metric("Memory Scale Weight", f"{profile['memory_mb']} MB")

        st.markdown("---")
        st.subheader("🧬 Contextual Rule-Engine Summary Reports")
        
        if current_insights["metrics"]:
            sub_grid = st.columns(min(len(current_insights["metrics"]), 4))
            for i, (metric_key, metric_val) in enumerate(current_insights["metrics"].items()):
                sub_grid[i % len(sub_grid)].metric(metric_key, metric_val)
                
        for alert_log in current_insights["alerts"]:
            st.info(f"💡 {alert_log}")

        st.markdown("### Matrix Structural Snapshot View")
        st.dataframe(st.session_state.active_df.head(10), use_container_width=True)

        st.markdown("---")
        st.subheader("📋 Production Report Engine Output")
        if st.button("⚙️ Compile and Bind PDF Executive Summary Report"):
            report_name = "MedInsight_Corporate_Brief.pdf"
            generate_pdf_report(profile, current_insights, report_name)
            with open(report_name, "rb") as f:
                st.download_button(label="📥 Download Production-Ready PDF Report", data=f, file_name=report_name, mime="application/pdf")
            st.success("PDF Brief rendered cleanly without character compilation issues.")

    # --- TAB 2: CLEANSING ENGINE ---
    elif menu == "2. Cleansing Workspace":
        st.header("🧼 Active Dataset Structuring Workspace")
        cleaner = DataCleaner(st.session_state.active_df)
        status = cleaner.get_cleaning_status()

        # Immediate Visual Status Cards
        st.subheader("⚠️ Structural Fault Indicators")
        err_col1, err_col2 = st.columns(2)
        
        if status["total_nulls"] > 0:
            err_col1.error(f"❌ Missing Cell Allocation Hazard: {status['total_nulls']} null pointers detected inside column boundaries.")
        else:
            err_col1.success("✅ Clean Grid Array: Zero missing cells identified inside current matrix.")

        if status["duplicate_count"] > 0:
            err_col2.error(f"❌ Identity Conflict Hazard: {status['duplicate_count']} completely redundant matching records detected.")
        else:
            err_col2.success("✅ Clean Structural Identity: Zero duplicate rows flagged inside workspace.")

        st.markdown("---")
        layout_l, layout_r = st.columns([1, 2])
        with layout_l:
            st.markdown("### Structural Transform Controls")
            if st.button("🗑️ Purge Duplicate Rows"):
                st.session_state.active_df = cleaner.remove_duplicates()
                st.success("Target duplicate records purged.")
                st.rerun()

            st.markdown("---")
            st.markdown("### Missing Value Imputation Engine")
            target_col = st.selectbox("Select Target Feature Coordinate", st.session_state.active_df.columns)
            strategy = st.selectbox("Mathematical Imputation Vector Strategy", ["Mean", "Median", "Mode"])
            
            if st.button("Execute Vector Imputation"):
                st.session_state.active_df = cleaner.fill_missing(target_col, strategy)
                st.success(f"Successfully imputed structural nodes via [{strategy}] calculations.")
                st.rerun()
        
        with layout_r:
            st.markdown("### Continuous Metric Attributes Map")
            st.dataframe(st.session_state.active_df.describe(), use_container_width=True)

    # --- TAB 3: VISUALIZATIONS ---
    elif menu == "3. Distribution Explorations":
        st.header("📈 Explanatory Graphic Visualizer Engine")
        chart_hints = suggest_charts_by_type(types)
        st.markdown("#### 💡 Structural Distribution Advice:\n" + ", ".join([f"`{hint}`" for hint in chart_hints]))
        
        col_view1, col_view2 = st.columns(2)
        
        with col_view1:
            st.markdown("### High-Fidelity Variable Density Distribution View")
            if types.get("numeric"):
                chosen_numeric = st.selectbox("Target Continuous Distribution Node", types["numeric"])
                st.plotly_chart(plot_histogram(st.session_state.active_df, chosen_numeric), use_container_width=True)
                
                st.info(f"""
                **💡 Interpreting the Distribution View:**
                * **The Vertical Bars (Histogram):** Show how frequent values are for **{chosen_numeric}**. The tallest blocks tell you where the heavy majority of patient records naturally aggregate.
                * **The Upper Axis Line (Box Plot):** Displays data boundary limits. The center line splits your metrics right at the **Median (true middle)**, while any lone dots sitting on the edges highlight unusual clinical **Outliers**.
                """)
            else:
                st.warning("No continuous numeric features found inside current active layout matrix.")

        with col_view2:
            st.markdown("### Cross-Feature Covariance Heatmap Matrix")
            if len(types.get("numeric", [])) >= 2:
                st.plotly_chart(plot_correlation(st.session_state.active_df, types["numeric"]), use_container_width=True)
                
                st.info("""
                **💡 Interpreting the Correlation Matrix:**
                * **The Scale Values (-1.00 to 1.00):** Show you whether variables share structural relationships.
                * **Scores near 1.00 (Bright Green):** Direct proportional link. As one feature climbs, the other follows it upward (e.g., Blood Pressure scaling directly with Age).
                * **Scores near -1.00 (Deep Slate Navy):** Inverse proportional link. When one attribute climbs, the other falls.
                * **Scores near 0.00 (Neutral Blue):** Independent noise. There is zero significant trend between those metrics.
                """)
            else:
                st.warning("Covariance evaluation requires at least 2 independent numeric vector columns.")

if __name__ == "__main__":
    main()