"""
test_pipeline.py
Automated test suite validating data processing, SQL analytics, ML modeling, inference, and artifacts.
"""

import os
import sys
import json
import pytest
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_processing import find_dataset_path, load_dataset, inspect_data, preprocess_data
from src.sql_analysis import FraudSQLAnalyzer
from src.feature_engineering import create_preprocessor, get_feature_names
from src.predict import FraudPredictor, get_sample_transaction


@pytest.fixture(scope="session")
def raw_df():
    """Session fixture loading dataset once for efficiency."""
    return load_dataset()


def test_dataset_loading_and_shape(raw_df):
    """Validates dataset dimensions and required columns."""
    assert raw_df is not None
    assert raw_df.shape == (284807, 31), f"Unexpected shape: {raw_df.shape}"
    assert "Class" in raw_df.columns
    assert "Amount" in raw_df.columns
    assert "Time" in raw_df.columns


def test_target_variable_distribution(raw_df):
    """Validates binary labels and exact fraud/legit counts."""
    classes = set(raw_df["Class"].unique())
    assert classes == {0, 1}, f"Target classes must be 0 and 1, got {classes}"
    
    counts = raw_df["Class"].value_counts()
    assert counts[0] == 284315, f"Expected 284,315 legitimate transactions, got {counts[0]}"
    assert counts[1] == 492, f"Expected 492 fraudulent transactions, got {counts[1]}"


def test_missing_values(raw_df):
    """Verifies that no missing or NaN values exist in the raw dataset."""
    total_nulls = raw_df.isnull().sum().sum()
    assert total_nulls == 0, f"Found unexpected null values: {total_nulls}"


def test_sql_summary_consistency(raw_df):
    """Reconciles SQLite analytical queries against Pandas ground truth."""
    analyzer = FraudSQLAnalyzer(db_path="outputs/fraud_analysis.db")
    analyzer.setup_database(raw_df)
    
    summary = analyzer.get_overall_summary()
    assert len(summary) == 1
    
    sql_total = summary["total_transactions"].iloc[0]
    sql_legit = summary["legitimate_transactions"].iloc[0]
    sql_fraud = summary["fraudulent_transactions"].iloc[0]
    sql_amount = summary["total_amount"].iloc[0]
    
    assert sql_total == len(raw_df), f"SQL total {sql_total} != Pandas total {len(raw_df)}"
    assert sql_legit == (raw_df["Class"] == 0).sum()
    assert sql_fraud == (raw_df["Class"] == 1).sum()
    assert abs(sql_amount - round(raw_df["Amount"].sum(), 2)) < 1.0


def test_feature_engineering_pipeline(raw_df):
    """Tests feature transformer logic and checks for zero target leakage."""
    sample_X = raw_df.drop(columns=["Class"]).head(50)
    preprocessor = create_preprocessor()
    
    # Fit and transform
    X_transformed = preprocessor.fit_transform(sample_X)
    
    assert X_transformed.shape[0] == 50
    # 4 monetary/temporal features + 28 PCA features = 32
    assert X_transformed.shape[1] == 32
    assert not np.isnan(X_transformed).any()


def test_saved_model_inference():
    """Validates that persisted model loads and produces calibrated probabilities."""
    model_path = os.path.join(project_root, "models", "fraud_detection_model.joblib")
    assert os.path.exists(model_path), f"Saved model not found at {model_path}"
    
    predictor = FraudPredictor(model_path=model_path)
    
    # Test legit transaction
    legit_input = get_sample_transaction(is_fraud=False)
    res_legit = predictor.predict(legit_input)
    assert len(res_legit) == 1
    assert "Fraud_Probability" in res_legit.columns
    prob_legit = res_legit["Fraud_Probability"].iloc[0]
    assert 0.0 <= prob_legit <= 1.0
    assert prob_legit < 0.5, f"Legitimate transaction expected low risk, got {prob_legit}"
    
    # Test fraud transaction
    fraud_input = get_sample_transaction(is_fraud=True)
    res_fraud = predictor.predict(fraud_input)
    prob_fraud = res_fraud["Fraud_Probability"].iloc[0]
    assert 0.0 <= prob_fraud <= 1.0
    assert prob_fraud >= 0.5, f"Fraudulent transaction expected high risk, got {prob_fraud}"


def test_model_metrics_file():
    """Validates that outputs/model_metrics.json exists and contains required metrics."""
    metrics_path = os.path.join(project_root, "outputs", "model_metrics.json")
    assert os.path.exists(metrics_path)
    
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
        
    assert "logistic_regression" in metrics
    lr = metrics["logistic_regression"]
    assert "recall" in lr
    assert "precision" in lr
    assert "f1_score" in lr
    assert "roc_auc" in lr
    assert "pr_auc" in lr
    assert lr["recall"] > 0.80  # Balanced LR catches >80% fraud


def test_generated_figures_exist():
    """Verifies that all required EDA and model figures were generated."""
    figures_dir = os.path.join(project_root, "reports", "figures")
    expected_figures = [
        "01_class_distribution.png",
        "02_amount_distribution.png",
        "03_amount_by_class_boxplot.png",
        "04_time_distribution.png",
        "05_fraud_time_hourly_pattern.png",
        "06_correlation_heatmap.png",
        "07_top_features_distribution.png",
        "08_amount_bands_fraud_rate.png",
        "09_scatter_v14_v17.png",
        "10_confusion_matrix.png",
        "11_pr_roc_curves.png",
        "12_feature_importance.png"
    ]
    for fig in expected_figures:
        fig_path = os.path.join(figures_dir, fig)
        assert os.path.exists(fig_path), f"Missing figure: {fig_path}"


def test_batch_prediction_and_risk_tiers(raw_df):
    """Tests batch prediction on multiple rows and validates Risk_Tier assignment."""
    predictor = FraudPredictor()
    sample_batch = raw_df.head(10).drop(columns=["Class"])
    results = predictor.predict(sample_batch)
    
    assert len(results) == 10
    assert "Risk_Tier" in results.columns
    assert "Fraud_Probability" in results.columns
    assert "Decision" in results.columns
    for tier in results["Risk_Tier"]:
        assert any(t in tier for t in ["Low Risk", "Medium Risk", "High Risk"])


def test_data_quality_report_content():
    """Validates that outputs/data_quality_report.csv contains audit rows for all 31 features."""
    report_path = os.path.join(project_root, "outputs", "data_quality_report.csv")
    assert os.path.exists(report_path)
    report_df = pd.read_csv(report_path)
    assert len(report_df) == 31
    assert "Column" in report_df.columns
    assert "NullCount" in report_df.columns
    assert report_df["NullCount"].sum() == 0
