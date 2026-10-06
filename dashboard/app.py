"""
app.py
Interactive Streamlit Dashboard for Transactional Fraud Detection Analysis.
Features:
- Executive Overview KPI Metrics
- Interactive Transaction Explorer (CSV or cached fallback)
- Deep-Dive Fraud EDA Charts (Plotly)
- Machine Learning Model Evaluation & Metrics
- Live Transaction Scoring & Prediction Demo
- Strategic Business Recommendations
"""

import os
import sys
import json
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="Transactional Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3d59;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.2rem;
        border-left: 5px solid #2b5c8f;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-fraud {
        border-left: 5px solid #d9534f !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Data / model loaders (all with graceful fallback)
# ─────────────────────────────────────────────

@st.cache_data
def load_findings():
    findings_path = project_root / "reports" / "findings.json"
    if findings_path.exists():
        with open(findings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


@st.cache_data
def load_model_metrics():
    metrics_path = project_root / "outputs" / "model_metrics.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


@st.cache_data
def load_sample_dataset():
    """
    Tries to load the raw CSV first (local run).
    Falls back to predictions_sample.csv (always in GitHub) for deployed mode.
    Returns a DataFrame with at minimum: Time, Amount, Class, Hour, Class_Label columns.
    """
    # Attempt 1 — raw CSV (local only)
    csv_candidates = [
        project_root / "creditcard.csv",
        Path("C:/Users/Aditya/Downloads/Infyntrex internship/creditcard.csv"),
    ]
    # Try find_dataset_path from src module
    try:
        from src.data_processing import find_dataset_path
        raw_path = find_dataset_path()
        df = pd.read_csv(raw_path)
        fraud = df[df["Class"] == 1]
        legit = df[df["Class"] == 0].sample(n=min(50000, len(df[df["Class"] == 0])), random_state=42)
        sample = pd.concat([fraud, legit]).sample(frac=1.0, random_state=42).reset_index(drop=True)
        sample["Hour"] = ((sample["Time"] // 3600) % 24).astype(int)
        sample["Class_Label"] = sample["Class"].map({0: "Legitimate", 1: "Fraudulent"})
        return sample, False  # (data, is_demo_mode)
    except Exception:
        pass

    # Attempt 2 — predictions_sample.csv (in GitHub)
    sample_path = project_root / "outputs" / "predictions_sample.csv"
    if sample_path.exists():
        df = pd.read_csv(sample_path)
        if "Actual_Class" in df.columns:
            df = df.rename(columns={"Actual_Class": "Class"})
        if "Class" in df.columns:
            df["Hour"] = ((df["Time"] // 3600) % 24).astype(int)
            df["Class_Label"] = df["Class"].map({0: "Legitimate", 1: "Fraudulent"})
            return df, True  # demo mode

    return pd.DataFrame(), True


@st.cache_resource
def load_predictor():
    """Load model — tries RF first, then LR fallback."""
    model_candidates = [
        project_root / "models" / "fraud_detection_model.joblib",
        project_root / "models" / "logistic_regression_model.joblib",
    ]
    for path in model_candidates:
        if path.exists():
            try:
                import joblib
                from src.predict import FraudPredictor
                return FraudPredictor(model_path=str(path))
            except Exception:
                pass
    return None


def get_sample_tx(is_fraud: bool, df: pd.DataFrame):
    """Pull a sample transaction row from cached data."""
    if df is not None and not df.empty and "Class" in df.columns:
        target = 1 if is_fraud else 0
        subset = df[df["Class"] == target]
        if not subset.empty:
            row = subset.iloc[0]
            cols = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
            available = {c: float(row[c]) for c in cols if c in row.index}
            return available
    synth = {f"V{i}": 0.0 for i in range(1, 29)}
    synth["Time"] = 86400.0
    synth["Amount"] = 149.99
    if is_fraud:
        synth.update({"V14": -7.5, "V17": -10.2, "V12": -5.0, "V10": -4.5, "V4": 4.2, "V11": 3.8})
    return synth


# ─────────────────────────────────────────────
# Load all resources
# ─────────────────────────────────────────────
findings = load_findings()
model_metrics = load_model_metrics()
df_sample, is_demo_mode = load_sample_dataset()
predictor = load_predictor()

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/000000/bank-cards.png", width=70)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to section:",
    [
        "📊 Executive Overview",
        "🔍 Transaction Explorer",
        "📈 Fraud Pattern Analysis",
        "🤖 ML Model Performance",
        "⚡ Real-Time Prediction Demo",
        "💡 Business Recommendations"
    ]
)

st.sidebar.markdown("---")
if is_demo_mode:
    st.sidebar.warning("""
**☁️ Deployed Mode**
Running without the 150MB raw dataset.
Explorer & charts use pre-cached sample data.
Clone the repo locally for full dataset access.
""")
else:
    st.sidebar.success("✅ Full dataset loaded (284,807 transactions)")

st.sidebar.info("""
**Project:** Transactional Fraud Detection  
**Tech Stack:** Python, Pandas, SQLite, Scikit-learn, Streamlit, Plotly  
**Dataset:** Kaggle ULB Credit Card Fraud
""")

# ==============================================================================
# 1. EXECUTIVE OVERVIEW
# ==============================================================================
if page == "📊 Executive Overview":
    st.markdown('<div class="main-header">Transactional Fraud Detection Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive Monitoring Dashboard & Real-Time Analytics</div>', unsafe_allow_html=True)

    if findings:
        overview = findings["dataset_overview"]
        amounts = findings["amount_statistics"]
        temporal = findings["temporal_insights"]

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Transactions", f"{overview['total_transactions']:,}")
        with col2:
            st.metric("Legitimate Volume", f"{overview['legitimate_count']:,}")
        with col3:
            st.metric("Fraudulent Incidents", f"{overview['fraudulent_count']:,}")
        with col4:
            st.metric("Fraud Rate", f"{overview['fraud_rate_pct']:.4f}%")
        with col5:
            st.metric("Total Fraud Loss", f"${amounts['fraud_total_financial_loss']:,.2f}")

        st.markdown("---")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Class Imbalance Breakdown")
            fig_pie = go.Figure(data=[go.Pie(
                labels=["Legitimate (99.83%)", "Fraudulent (0.17%)"],
                values=[overview["legitimate_count"], overview["fraudulent_count"]],
                hole=0.6,
                marker=dict(colors=["#2b5c8f", "#d9534f"]),
                textinfo="label+value"
            )])
            fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=320)
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("Financial Comparison: Avg & Max Amount")
            comp_df = pd.DataFrame({
                "Category": ["Legitimate", "Fraudulent"],
                "Average Amount ($)": [amounts["legit_mean"], amounts["fraud_mean"]],
                "Median Amount ($)": [amounts["legit_median"], amounts["fraud_median"]],
                "Max Amount ($)": [amounts["overall_max"], amounts["fraud_max"]]
            })
            fig_bar = px.bar(
                comp_df,
                x="Category",
                y="Average Amount ($)",
                color="Category",
                color_discrete_map={"Legitimate": "#2b5c8f", "Fraudulent": "#d9534f"},
                text="Average Amount ($)"
            )
            fig_bar.update_traces(texttemplate="$%{text:.2f}", textposition="outside")
            fig_bar.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=320)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.info(f"""
        **Key Executive Insight:**
        - Fraud occurs at an extreme ratio of **{overview['imbalance_ratio']}**.
        - Fraudulent transactions have a **higher average amount (${amounts['fraud_mean']:.2f})** vs legitimate (${amounts['legit_mean']:.2f}).
        - Temporal analysis confirms: **Peak fraud rate reaches {temporal['peak_fraud_rate_pct']:.3f}% at Hour {temporal['peak_fraud_rate_hour']}:00 (late night)**, ~10x the baseline!
        """)

        st.markdown("---")
        st.subheader("Pre-Generated Analysis Figures")
        figures_dir = project_root / "reports" / "figures"
        fig_files = sorted(figures_dir.glob("*.png")) if figures_dir.exists() else []
        if fig_files:
            cols = st.columns(3)
            for i, fig_path in enumerate(fig_files[:6]):
                with cols[i % 3]:
                    st.image(str(fig_path), caption=fig_path.stem.replace("_", " ").title(), use_container_width=True)
    else:
        st.warning("findings.json not found. Run `python src/eda.py` to generate analytics.")


# ==============================================================================
# 2. TRANSACTION EXPLORER
# ==============================================================================
elif page == "🔍 Transaction Explorer":
    st.markdown('<div class="main-header">Interactive Transaction Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Filter, inspect, and analyze transactional activity</div>', unsafe_allow_html=True)

    if is_demo_mode:
        st.info("☁️ **Deployed Mode** — showing pre-cached sample transactions (250 rows: all frauds + 200 legit). Clone locally for all 284K transactions.")

    if not df_sample.empty:
        st.sidebar.subheader("Filter Transactions")
        selected_class = st.sidebar.selectbox("Transaction Class", ["All", "Legitimate Only", "Fraudulent Only"])

        min_amt = float(df_sample["Amount"].min())
        max_amt = float(df_sample["Amount"].max())
        amt_range = st.sidebar.slider("Amount Range ($)", min_value=0.0, max_value=min(2500.0, max_amt), value=(0.0, min(1000.0, max_amt)))

        hour_range = st.sidebar.slider("Hour of Day (0 to 23)", min_value=0, max_value=23, value=(0, 23))

        filtered_df = df_sample[
            (df_sample["Amount"] >= amt_range[0]) &
            (df_sample["Amount"] <= amt_range[1]) &
            (df_sample["Hour"] >= hour_range[0]) &
            (df_sample["Hour"] <= hour_range[1])
        ]
        if selected_class == "Legitimate Only":
            filtered_df = filtered_df[filtered_df["Class"] == 0]
        elif selected_class == "Fraudulent Only":
            filtered_df = filtered_df[filtered_df["Class"] == 1]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Matching Transactions", f"{len(filtered_df):,}")
        fraud_in_filter = int((filtered_df["Class"] == 1).sum())
        c2.metric("Fraud Incidents", f"{fraud_in_filter:,}")
        rate_in_filter = (fraud_in_filter / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        c3.metric("Segment Fraud Rate", f"{rate_in_filter:.3f}%")
        c4.metric("Total Dollar Volume", f"${filtered_df['Amount'].sum():,.2f}")

        display_cols = [c for c in ["Time", "Hour", "Amount", "Class_Label", "V14", "V17", "V12", "V10", "V4", "V11"] if c in filtered_df.columns]
        st.dataframe(filtered_df[display_cols].head(100), use_container_width=True)

        csv_download = filtered_df[display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Transactions (CSV)",
            data=csv_download,
            file_name="filtered_transactions.csv",
            mime="text/csv"
        )
    else:
        st.warning("No transaction data available.")


# ==============================================================================
# 3. FRAUD PATTERN ANALYSIS
# ==============================================================================
elif page == "📈 Fraud Pattern Analysis":
    st.markdown('<div class="main-header">Exploratory Fraud Pattern Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Deep-dive visualizations into temporal, monetary, and dimensional patterns</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["⏰ Temporal Risk Patterns", "💰 Monetary Distributions", "🧬 Discriminative Features", "🖼️ All EDA Figures"])

    with tab1:
        st.subheader("Diurnal Analysis: Transaction Volume vs. Fraud Rate by Hour")
        if not df_sample.empty and "Hour" in df_sample.columns:
            hourly_stats = df_sample.groupby("Hour").agg(
                total=("Class", "count"),
                fraud=("Class", "sum")
            ).reset_index()
            hourly_stats["fraud_rate_pct"] = (hourly_stats["fraud"] / hourly_stats["total"]) * 100

            fig_hourly = go.Figure()
            fig_hourly.add_trace(go.Bar(x=hourly_stats["Hour"], y=hourly_stats["total"], name="Total Volume", marker_color="#a4c2f4", yaxis="y"))
            fig_hourly.add_trace(go.Scatter(x=hourly_stats["Hour"], y=hourly_stats["fraud_rate_pct"], name="Fraud Rate (%)", marker_color="#d9534f", mode="lines+markers", yaxis="y2", line=dict(width=3)))
            fig_hourly.update_layout(
                xaxis=dict(title="Hour of Day (0-23)", tickmode="linear", tick0=0, dtick=1),
                yaxis=dict(title="Transaction Volume", side="left"),
                yaxis2=dict(title="Fraud Rate (%)", side="right", overlaying="y"),
                legend=dict(x=0.01, y=0.99),
                height=450, margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
            st.markdown("**Observation:** Fraud rates spike to ~1.71% at 2:00 AM when legitimate volume drops sharply.")
        else:
            # fallback to static figure
            fig_path = project_root / "reports" / "figures" / "05_fraud_time_hourly_pattern.png"
            if fig_path.exists():
                st.image(str(fig_path), use_container_width=True)

    with tab2:
        st.subheader("Amount Distribution Comparison (Log Scale)")
        if not df_sample.empty and "Class_Label" in df_sample.columns:
            fig_amt = px.histogram(
                df_sample, x="Amount", color="Class_Label", nbins=50, log_y=True, barmode="overlay",
                color_discrete_map={"Legitimate": "#2b5c8f", "Fraudulent": "#d9534f"},
                labels={"Amount": "Transaction Amount ($)"}
            )
            fig_amt.update_layout(height=420)
            st.plotly_chart(fig_amt, use_container_width=True)
        else:
            fig_path = project_root / "reports" / "figures" / "02_amount_distribution.png"
            if fig_path.exists():
                st.image(str(fig_path), use_container_width=True)

    with tab3:
        st.subheader("Feature Space Separation: V14 vs V17")
        if not df_sample.empty and "V14" in df_sample.columns and "Class_Label" in df_sample.columns:
            scatter_df = df_sample.sample(n=min(5000, len(df_sample)), random_state=42)
            fig_scatter = px.scatter(
                scatter_df, x="V14", y="V17", color="Class_Label",
                color_discrete_map={"Legitimate": "rgba(43, 92, 143, 0.4)", "Fraudulent": "#d9534f"},
                opacity=0.7, title="PCA Projections Separation: V14 vs V17"
            )
            fig_scatter.update_layout(height=450)
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            fig_path = project_root / "reports" / "figures" / "09_scatter_v14_v17.png"
            if fig_path.exists():
                st.image(str(fig_path), use_container_width=True)

    with tab4:
        st.subheader("All 12 Pre-Generated EDA & Model Figures")
        figures_dir = project_root / "reports" / "figures"
        fig_files = sorted(figures_dir.glob("*.png")) if figures_dir.exists() else []
        if fig_files:
            cols = st.columns(2)
            for i, fig_path in enumerate(fig_files):
                with cols[i % 2]:
                    st.image(str(fig_path), caption=fig_path.stem.replace("_", " ").title(), use_container_width=True)
        else:
            st.warning("Figures not found. Run `python src/eda.py` and `python src/train_model.py`.")


# ==============================================================================
# 4. ML MODEL PERFORMANCE
# ==============================================================================
elif page == "🤖 ML Model Performance":
    st.markdown('<div class="main-header">Machine Learning Model Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluation of Baseline Logistic Regression vs. Comparison Random Forest</div>', unsafe_allow_html=True)

    if model_metrics:
        lr_m = model_metrics.get("logistic_regression", {})
        rf_m = model_metrics.get("random_forest", {})

        st.subheader("Summary Evaluation Metrics (Test Set: 56,962 transactions, 98 fraud)")
        comp_data = {
            "Metric": ["Accuracy", "Recall (Fraud Catch Rate)", "Precision (Alarm Accuracy)", "F1-Score", "ROC-AUC", "PR-AUC (Primary Metric)", "False Positives (Alarms)", "True Positives (Caught)"],
            "Logistic Regression (Baseline)": [
                f"{lr_m.get('accuracy', 0):.4f}", f"{lr_m.get('recall', 0):.2%}",
                f"{lr_m.get('precision', 0):.2%}", f"{lr_m.get('f1_score', 0):.4f}",
                f"{lr_m.get('roc_auc', 0):.4f}", f"{lr_m.get('pr_auc', 0):.4f}",
                f"{lr_m.get('confusion_matrix', {}).get('false_positives', 0):,}",
                f"{lr_m.get('confusion_matrix', {}).get('true_positives', 0):,}"
            ],
            "Random Forest (Comparison)": [
                f"{rf_m.get('accuracy', 0):.4f}", f"{rf_m.get('recall', 0):.2%}",
                f"{rf_m.get('precision', 0):.2%}", f"{rf_m.get('f1_score', 0):.4f}",
                f"{rf_m.get('roc_auc', 0):.4f}", f"{rf_m.get('pr_auc', 0):.4f}",
                f"{rf_m.get('confusion_matrix', {}).get('false_positives', 0):,}",
                f"{rf_m.get('confusion_matrix', {}).get('true_positives', 0):,}"
            ]
        }
        st.table(pd.DataFrame(comp_data))

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Confusion Matrix: Logistic Regression")
            cm_lr = lr_m.get("confusion_matrix", {})
            z_lr = [[cm_lr.get("true_negatives", 0), cm_lr.get("false_positives", 0)],
                    [cm_lr.get("false_negatives", 0), cm_lr.get("true_positives", 0)]]
            fig_cm1 = px.imshow(z_lr, labels=dict(x="Predicted", y="Actual", color="Count"),
                                x=["Legitimate", "Fraudulent"], y=["Legitimate", "Fraudulent"],
                                text_auto=True, color_continuous_scale="Blues")
            fig_cm1.update_layout(height=350)
            st.plotly_chart(fig_cm1, use_container_width=True)

        with c2:
            st.subheader("Confusion Matrix: Random Forest")
            cm_rf = rf_m.get("confusion_matrix", {})
            z_rf = [[cm_rf.get("true_negatives", 0), cm_rf.get("false_positives", 0)],
                    [cm_rf.get("false_negatives", 0), cm_rf.get("true_positives", 0)]]
            fig_cm2 = px.imshow(z_rf, labels=dict(x="Predicted", y="Actual", color="Count"),
                                x=["Legitimate", "Fraudulent"], y=["Legitimate", "Fraudulent"],
                                text_auto=True, color_continuous_scale="Greens")
            fig_cm2.update_layout(height=350)
            st.plotly_chart(fig_cm2, use_container_width=True)

        # Static model figures
        st.markdown("---")
        st.subheader("Model Evaluation Figures")
        model_figs = ["10_confusion_matrix.png", "11_pr_roc_curves.png", "12_feature_importance.png"]
        fig_cols = st.columns(3)
        for i, fname in enumerate(model_figs):
            fpath = project_root / "reports" / "figures" / fname
            if fpath.exists():
                with fig_cols[i]:
                    st.image(str(fpath), caption=fname.replace("_", " ").replace(".png", "").title(), use_container_width=True)

        st.markdown("""
        **Operational Trade-off Analysis:**
        - **Logistic Regression** optimizes for maximum recall (**90.82%**), catching 89/98 fraud cases, but generates **1,492 false alarms**.
        - **Random Forest** optimizes for high precision (**75.47%**) and high PR-AUC (**0.8433**), generating only **26 false alarms** while still capturing **81.63%** of fraud.
        """)
    else:
        st.warning("model_metrics.json not found. Run `python src/train_model.py` to generate metrics.")


# ==============================================================================
# 5. REAL-TIME PREDICTION DEMO
# ==============================================================================
elif page == "⚡ Real-Time Prediction Demo":
    st.markdown('<div class="main-header">Real-Time Transaction Scoring Demo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live inference sandbox for scoring transactions with fraud probability and risk tiers</div>', unsafe_allow_html=True)

    if predictor is None:
        st.error("⚠️ Model file not found. The logistic_regression_model.joblib must be present in `models/`.")
        st.info("If running locally: `python src/train_model.py` to regenerate it.")
    else:
        st.write("Load a preset profile or manually modify parameters to test the classification model.")

        col_preset1, col_preset2 = st.columns(2)
        with col_preset1:
            load_normal = st.button("🟢 Pre-fill Typical Legitimate Transaction")
        with col_preset2:
            load_fraud = st.button("🔴 Pre-fill Highly Suspicious Fraudulent Transaction")

        if "demo_tx" not in st.session_state:
            st.session_state["demo_tx"] = get_sample_tx(is_fraud=False, df=df_sample)
        if load_normal:
            st.session_state["demo_tx"] = get_sample_tx(is_fraud=False, df=df_sample)
        if load_fraud:
            st.session_state["demo_tx"] = get_sample_tx(is_fraud=True, df=df_sample)

        tx = st.session_state["demo_tx"]

        with st.form("prediction_form"):
            st.subheader("Transaction Metadata")
            c1, c2, c3 = st.columns(3)
            time_val = c1.number_input("Time (Seconds from Day 0)", value=float(tx.get("Time", 50000.0)), step=100.0)
            amount_val = c2.number_input("Amount ($)", value=float(tx.get("Amount", 45.00)), step=5.0)
            threshold_val = c3.slider("Decision Threshold", min_value=0.1, max_value=0.9, value=0.5, step=0.05)

            st.subheader("Primary Latent PCA Signals (V1–V28)")
            st.caption("Key discriminative features: V14, V17, V12, V10, V4, V11")
            k1, k2, k3 = st.columns(3)
            v14_val = k1.number_input("V14 (Strong negative correlation)", value=float(tx.get("V14", 0.0)), format="%.4f")
            v17_val = k2.number_input("V17 (Strong negative correlation)", value=float(tx.get("V17", 0.0)), format="%.4f")
            v12_val = k3.number_input("V12 (Strong negative correlation)", value=float(tx.get("V12", 0.0)), format="%.4f")

            k4, k5, k6 = st.columns(3)
            v10_val = k4.number_input("V10 (Negative correlation)", value=float(tx.get("V10", 0.0)), format="%.4f")
            v4_val = k5.number_input("V4 (Positive correlation)", value=float(tx.get("V4", 0.0)), format="%.4f")
            v11_val = k6.number_input("V11 (Positive correlation)", value=float(tx.get("V11", 0.0)), format="%.4f")

            submit_btn = st.form_submit_button("⚡ Score Transaction Now")

        if submit_btn:
            input_dict = {f"V{i}": float(tx.get(f"V{i}", 0.0)) for i in range(1, 29)}
            input_dict.update({"Time": time_val, "Amount": amount_val,
                               "V14": v14_val, "V17": v17_val, "V12": v12_val,
                               "V10": v10_val, "V4": v4_val, "V11": v11_val})

            result_df = predictor.predict(input_dict, threshold=threshold_val)
            prob = float(result_df["Fraud_Probability"].iloc[0])
            decision = result_df["Decision"].iloc[0]
            tier = result_df["Risk_Tier"].iloc[0]

            st.markdown("---")
            st.subheader("Inference Result")
            res_c1, res_c2, res_c3 = st.columns(3)
            res_c1.metric("Predicted Decision", decision)
            res_c2.metric("Fraud Probability", f"{prob:.2%}")
            res_c3.metric("Assigned Risk Tier", tier)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={"text": "Fraud Risk Score (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#d9534f" if prob >= threshold_val else "#2b5c8f"},
                    "steps": [
                        {"range": [0, 30], "color": "#d9ead3"},
                        {"range": [30, 70], "color": "#fff2cc"},
                        {"range": [70, 100], "color": "#f4cccc"}
                    ],
                    "threshold": {"line": {"color": "black", "width": 4}, "thickness": 0.75, "value": threshold_val * 100}
                }
            ))
            fig_gauge.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.caption("⚠️ **Notice:** This ML probability estimate should be combined with transaction history before irreversible actions.")


# ==============================================================================
# 6. BUSINESS RECOMMENDATIONS
# ==============================================================================
elif page == "💡 Business Recommendations":
    st.markdown('<div class="main-header">Business Recommendations & Strategic Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Actionable guidance derived from empirical findings and model evaluation</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### 1. Multi-Tiered Transaction Routing Engine
        - **Low Risk (< 30% Probability):** Frictionless one-click approval (99.5% of traffic).
        - **Medium Risk (30–70%):** Step-up authentication via 3D Secure / OTP / SMS challenge.
        - **High Risk (≥ 70%):** Automatic block with push notification to customer.
        """)

        st.markdown("""
        ### 2. Time-Based Risk Dynamic Weighting
        - **Late Night Vulnerability:** Fraud rate climbs **10× higher (up to 1.71%) between 2–4 AM**.
        - Implement strict rule multipliers during nighttime for transactions exceeding $100.
        """)

    with c2:
        st.markdown("""
        ### 3. Operational Cost-Benefit Optimization
        - Baseline LR: catching 89 frauds incurred **1,492 false alarms** (17:1 ratio).
        - **Random Forest reduced false alarms by 98.3% (to just 26)** with 81.6% catch rate.
        - Prevents brand damage and cuts tier-1 investigation costs significantly.
        """)

        st.markdown("""
        ### 4. Continuous Monitoring & Feature Store
        - Latent features V14, V17, and V12 represent 60%+ of predictive signal.
        - Future work: Device fingerprinting, IP geolocation distance, user velocity scoring once PII/metadata is accessible.
        """)
