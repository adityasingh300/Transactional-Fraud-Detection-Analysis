"""
train_model.py
Trains and evaluates machine learning models for Credit Card Fraud Detection.
Includes baseline Logistic Regression (balanced) and comparison Random Forest.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve
)

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_processing import load_dataset, preprocess_data
from src.feature_engineering import create_preprocessor, get_feature_names

logger = logging.getLogger(__name__)


def evaluate_model_performance(model_name: str, y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> Dict[str, Any]:
    """
    Computes rigorous classification metrics tailored to highly imbalanced fraud detection.
    """
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_true, y_proba)
    pr_auc = average_precision_score(y_true, y_proba)
    acc = accuracy_score(y_true, y_pred)
    
    metrics = {
        "model_name": model_name,
        "accuracy": round(float(acc), 5),
        "precision": round(float(precision), 5),
        "recall": round(float(recall), 5),
        "f1_score": round(float(f1), 5),
        "roc_auc": round(float(roc_auc), 5),
        "pr_auc": round(float(pr_auc), 5),
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        },
        "business_impact": {
            "total_test_fraud": int(fn + tp),
            "caught_fraud_count": int(tp),
            "missed_fraud_count": int(fn),
            "false_alarms": int(fp),
            "fraud_catch_rate_pct": round(float(recall * 100), 2),
            "false_positive_ratio": f"{int(round(fp / tp)) if tp > 0 else 0} false alarms per true fraud detected"
        }
    }
    return metrics


def train_and_evaluate(
    test_size: float = 0.2,
    random_state: int = 42,
    include_random_forest: bool = True
) -> Dict[str, Any]:
    """
    Executes end-to-end model training, evaluation, interpretation, and artifact persistence.
    """
    logger.info("Loading dataset for model training...")
    raw_df = load_dataset()
    df = preprocess_data(raw_df, handle_duplicates="keep")
    
    X = df.drop(columns=["Class"])
    y = df["Class"].values
    
    logger.info(f"Performing Stratified Train/Test Split (test_size={test_size}, random_state={random_state})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    logger.info(f"Train samples: {len(X_train):,} (Fraud: {y_train.sum():,})")
    logger.info(f"Test samples: {len(X_test):,} (Fraud: {y_test.sum():,})")

    models_dir = "models"
    outputs_dir = "outputs"
    figures_dir = "reports/figures"
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    results = {}
    fitted_pipelines = {}

    # 1. Baseline Model: Logistic Regression (Balanced Class Weights)
    logger.info("--- Training Baseline: Logistic Regression (class_weight='balanced') ---")
    lr_pipeline = Pipeline([
        ("preprocessor", create_preprocessor()),
        ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=random_state))
    ])
    lr_pipeline.fit(X_train, y_train)
    fitted_pipelines["Logistic Regression"] = lr_pipeline
    
    y_pred_lr = lr_pipeline.predict(X_test)
    y_proba_lr = lr_pipeline.predict_proba(X_test)[:, 1]
    lr_metrics = evaluate_model_performance("Logistic Regression", y_test, y_pred_lr, y_proba_lr)
    results["logistic_regression"] = lr_metrics
    logger.info(f"Logistic Regression F1: {lr_metrics['f1_score']:.4f}, Recall: {lr_metrics['recall']:.4f}, PR-AUC: {lr_metrics['pr_auc']:.4f}")

    # 2. Comparison Model: Random Forest
    rf_pipeline = None
    if include_random_forest:
        logger.info("--- Training Comparison Model: Random Forest (Balanced) ---")
        rf_pipeline = Pipeline([
            ("preprocessor", create_preprocessor()),
            ("classifier", RandomForestClassifier(
                n_estimators=100,
                max_depth=12,
                class_weight="balanced",
                random_state=random_state,
                n_jobs=-1
            ))
        ])
        rf_pipeline.fit(X_train, y_train)
        fitted_pipelines["Random Forest"] = rf_pipeline
        
        y_pred_rf = rf_pipeline.predict(X_test)
        y_proba_rf = rf_pipeline.predict_proba(X_test)[:, 1]
        rf_metrics = evaluate_model_performance("Random Forest", y_test, y_pred_rf, y_proba_rf)
        results["random_forest"] = rf_metrics
        logger.info(f"Random Forest F1: {rf_metrics['f1_score']:.4f}, Recall: {rf_metrics['recall']:.4f}, PR-AUC: {rf_metrics['pr_auc']:.4f}")

    # Determine Best Model based on PR-AUC / F1-Score
    best_model_name = "Random Forest" if include_random_forest and rf_metrics["pr_auc"] >= lr_metrics["pr_auc"] else "Logistic Regression"
    best_pipeline = fitted_pipelines[best_model_name]
    logger.info(f"Selected best production model: {best_model_name}")

    # Save Primary Model Pipeline
    model_save_path = os.path.join(models_dir, "fraud_detection_model.joblib")
    joblib.dump(best_pipeline, model_save_path)
    logger.info(f"Saved primary model pipeline to: {model_save_path}")

    # Also save individual models if needed
    joblib.dump(lr_pipeline, os.path.join(models_dir, "logistic_regression_model.joblib"))
    if rf_pipeline is not None:
        joblib.dump(rf_pipeline, os.path.join(models_dir, "random_forest_model.joblib"))

    # Save Metrics JSON
    metrics_path = os.path.join(outputs_dir, "model_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    logger.info(f"Saved metrics to: {metrics_path}")

    # Save Classification Report
    report_text = f"=== Baseline: Logistic Regression ===\n"
    report_text += classification_report(y_test, y_pred_lr, digits=4)
    if include_random_forest:
        report_text += f"\n\n=== Comparison: Random Forest ===\n"
        report_text += classification_report(y_test, y_pred_rf, digits=4)
    
    report_file = os.path.join(outputs_dir, "classification_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    logger.info(f"Saved classification report to: {report_file}")

    # Save Confusion Matrix CSV
    cm_lr = confusion_matrix(y_test, y_pred_lr)
    cm_df = pd.DataFrame(cm_lr, index=["Actual_Legit", "Actual_Fraud"], columns=["Pred_Legit", "Pred_Fraud"])
    cm_file = os.path.join(outputs_dir, "confusion_matrix.csv")
    cm_df.to_csv(cm_file)
    logger.info(f"Saved confusion matrix CSV to: {cm_file}")

    # Save Sample Predictions
    test_sample = X_test.copy()
    test_sample["Actual_Class"] = y_test
    test_sample["LR_Predicted"] = y_pred_lr
    test_sample["LR_Fraud_Probability"] = np.round(y_proba_lr, 4)
    if include_random_forest:
        test_sample["RF_Predicted"] = y_pred_rf
        test_sample["RF_Fraud_Probability"] = np.round(y_proba_rf, 4)
    
    sample_csv = os.path.join(outputs_dir, "predictions_sample.csv")
    # Take a representative sample: 50 fraud and 150 legit
    fraud_samples = test_sample[test_sample["Actual_Class"] == 1]
    legit_samples = test_sample[test_sample["Actual_Class"] == 0].sample(n=min(200, len(test_sample[test_sample["Actual_Class"] == 0])), random_state=random_state)
    combined_sample = pd.concat([fraud_samples, legit_samples]).sample(frac=1.0, random_state=random_state)
    combined_sample.to_csv(sample_csv, index=False)
    logger.info(f"Saved prediction samples to: {sample_csv}")

    # --- Generate Model Interpretation & Visualizations ---
    # 1. Confusion Matrix Heatmaps
    fig, axes = plt.subplots(1, 2 if include_random_forest else 1, figsize=(14 if include_random_forest else 7, 5))
    if not include_random_forest:
        axes = [axes]
    
    sns.heatmap(cm_lr, annot=True, fmt="d", cmap="Blues", ax=axes[0],
                xticklabels=["Pred Legit", "Pred Fraud"], yticklabels=["Actual Legit", "Actual Fraud"])
    axes[0].set_title(f"Logistic Regression\nRecall: {lr_metrics['recall']:.2%}, Prec: {lr_metrics['precision']:.2%}")
    axes[0].set_ylabel("True Label")
    axes[0].set_xlabel("Predicted Label")

    if include_random_forest:
        cm_rf = confusion_matrix(y_test, y_pred_rf)
        sns.heatmap(cm_rf, annot=True, fmt="d", cmap="Greens", ax=axes[1],
                    xticklabels=["Pred Legit", "Pred Fraud"], yticklabels=["Actual Legit", "Actual Fraud"])
        axes[1].set_title(f"Random Forest\nRecall: {rf_metrics['recall']:.2%}, Prec: {rf_metrics['precision']:.2%}")
        axes[1].set_ylabel("True Label")
        axes[1].set_xlabel("Predicted Label")

    plt.tight_layout()
    cm_fig_path = os.path.join(figures_dir, "10_confusion_matrix.png")
    plt.savefig(cm_fig_path, dpi=200, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved: {cm_fig_path}")

    # 2. ROC and Precision-Recall Curves
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # ROC Curves
    fpr_lr, tpr_lr, _ = roc_curve(y_test, y_proba_lr)
    axes[0].plot(fpr_lr, tpr_lr, label=f"Logistic Regression (AUC = {lr_metrics['roc_auc']:.4f})", color="#2b5c8f", lw=2)
    if include_random_forest:
        fpr_rf, tpr_rf, _ = roc_curve(y_test, y_proba_rf)
        axes[0].plot(fpr_rf, tpr_rf, label=f"Random Forest (AUC = {rf_metrics['roc_auc']:.4f})", color="#27ae60", lw=2)
    axes[0].plot([0, 1], [0, 1], "k--", alpha=0.6, label="Random Guess")
    axes[0].set_title("ROC Curves (Receiver Operating Characteristic)")
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate (Recall)")
    axes[0].legend(loc="lower right")

    # Precision-Recall Curves (Key for Imbalanced Data)
    prec_lr, rec_lr, _ = precision_recall_curve(y_test, y_proba_lr)
    axes[1].plot(rec_lr, prec_lr, label=f"Logistic Regression (PR-AUC = {lr_metrics['pr_auc']:.4f})", color="#2b5c8f", lw=2)
    if include_random_forest:
        prec_rf, rec_rf, _ = precision_recall_curve(y_test, y_proba_rf)
        axes[1].plot(rec_rf, prec_rf, label=f"Random Forest (PR-AUC = {rf_metrics['pr_auc']:.4f})", color="#27ae60", lw=2)
    axes[1].set_title("Precision-Recall Curves (Critical Metric)")
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].legend(loc="upper right")

    plt.tight_layout()
    curves_fig_path = os.path.join(figures_dir, "11_pr_roc_curves.png")
    plt.savefig(curves_fig_path, dpi=200, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved: {curves_fig_path}")

    # 3. Model Interpretation: Feature Importance & Coefficients
    feature_names = get_feature_names()
    
    # Logistic Regression Coefficients
    lr_coefs = lr_pipeline.named_steps["classifier"].coef_[0]
    coef_df = pd.DataFrame({"Feature": feature_names, "Coefficient": lr_coefs})
    coef_df["Abs_Coef"] = coef_df["Coefficient"].abs()
    coef_df = coef_df.sort_values(by="Abs_Coef", ascending=False)
    coef_df.to_csv(os.path.join(outputs_dir, "logistic_regression_coefficients.csv"), index=False)

    plt.figure(figsize=(12, 6))
    top_coefs = coef_df.head(15).sort_values(by="Coefficient")
    colors = ["#d9534f" if c > 0 else "#2b5c8f" for c in top_coefs["Coefficient"]]
    plt.barh(top_coefs["Feature"], top_coefs["Coefficient"], color=colors, edgecolor="black", alpha=0.85)
    plt.axvline(0, color="black", linestyle="--", alpha=0.7)
    plt.title("Top 15 Logistic Regression Coefficients (Feature Associations with Fraud)")
    plt.xlabel("Coefficient Value (Positive = Increases Fraud Odds, Negative = Decreases Odds)")
    plt.ylabel("Feature")
    plt.tight_layout()
    feat_fig_path = os.path.join(figures_dir, "12_feature_importance.png")
    plt.savefig(feat_fig_path, dpi=200, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved: {feat_fig_path}")

    logger.info("Training and evaluation completed successfully!")
    return results


if __name__ == "__main__":
    results = train_and_evaluate(include_random_forest=True)
    print("--- Model Training Results Summary ---")
    print(json.dumps(results, indent=2))
