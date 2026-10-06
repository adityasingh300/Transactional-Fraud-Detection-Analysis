"""
data_processing.py
Module for loading, profiling, cleaning, and inspecting the Credit Card Fraud dataset.
"""

import os
import sys
import logging
from typing import Tuple, Dict, Any, Optional
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

DEFAULT_DATA_PATHS = [
    r"C:\Users\Aditya\Downloads\Infyntrex internship\creditcard.csv",
    os.path.join("data", "creditcard.csv"),
    "creditcard.csv",
    os.path.join("..", "creditcard.csv")
]


def find_dataset_path(custom_path: Optional[str] = None) -> str:
    """
    Locates the dataset by checking a custom path or predefined default paths.
    """
    if custom_path and os.path.exists(custom_path):
        logger.info(f"Using provided dataset path: {custom_path}")
        return custom_path
    
    for path in DEFAULT_DATA_PATHS:
        if os.path.exists(path):
            logger.info(f"Located dataset at: {path}")
            return path
            
    raise FileNotFoundError(
        "creditcard.csv not found! Checked locations:\n" +
        "\n".join(DEFAULT_DATA_PATHS) +
        "\nPlease place creditcard.csv in data/ or provide the absolute path."
    )


def load_dataset(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads creditcard.csv into a pandas DataFrame.
    """
    path = find_dataset_path(filepath)
    logger.info(f"Loading data from: {path}")
    df = pd.read_csv(path)
    logger.info(f"Dataset loaded successfully with shape: {df.shape}")
    return df


def generate_data_quality_report(df: pd.DataFrame, output_path: str = "outputs/data_quality_report.csv") -> pd.DataFrame:
    """
    Generates a detailed column-by-column data quality report and writes to CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    report_rows = []
    total_rows = len(df)
    
    for col in df.columns:
        series = df[col]
        null_count = series.isnull().sum()
        null_pct = (null_count / total_rows) * 100
        
        # Check infinite values for numeric columns
        inf_count = np.isinf(series).sum() if pd.api.types.is_numeric_dtype(series) else 0
        
        dtype = str(series.dtype)
        unique_count = series.nunique()
        min_val = series.min() if pd.api.types.is_numeric_dtype(series) else None
        max_val = series.max() if pd.api.types.is_numeric_dtype(series) else None
        mean_val = series.mean() if pd.api.types.is_numeric_dtype(series) else None
        std_val = series.std() if pd.api.types.is_numeric_dtype(series) else None
        
        report_rows.append({
            "Column": col,
            "DataType": dtype,
            "TotalCount": total_rows,
            "NullCount": null_count,
            "NullPercentage": round(null_pct, 4),
            "InfiniteCount": inf_count,
            "UniqueCount": unique_count,
            "Min": round(float(min_val), 4) if min_val is not None else None,
            "Max": round(float(max_val), 4) if max_val is not None else None,
            "Mean": round(float(mean_val), 4) if mean_val is not None else None,
            "Std": round(float(std_val), 4) if std_val is not None else None
        })
        
    report_df = pd.DataFrame(report_rows)
    report_df.to_csv(output_path, index=False)
    logger.info(f"Data quality report saved to: {output_path}")
    return report_df


def inspect_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive verification of the dataset.
    """
    total_records = len(df)
    total_cols = df.shape[1]
    
    if "Class" not in df.columns:
        raise ValueError("Target column 'Class' missing from dataset!")
        
    class_counts = df["Class"].value_counts().to_dict()
    legit_count = class_counts.get(0, 0)
    fraud_count = class_counts.get(1, 0)
    fraud_pct = (fraud_count / total_records) * 100 if total_records > 0 else 0
    
    # Check duplicates
    duplicate_rows_count = int(df.duplicated().sum())
    duplicates_all = df[df.duplicated(keep=False)]
    dup_fraud = int(duplicates_all[duplicates_all["Class"] == 1]["Class"].count()) if not duplicates_all.empty else 0
    dup_legit = int(duplicates_all[duplicates_all["Class"] == 0]["Class"].count()) if not duplicates_all.empty else 0
    
    null_total = int(df.isnull().sum().sum())
    
    summary = {
        "total_records": total_records,
        "total_columns": total_cols,
        "columns": list(df.columns),
        "legitimate_transactions": legit_count,
        "fraudulent_transactions": fraud_count,
        "fraud_percentage": round(fraud_pct, 5),
        "missing_values_total": null_total,
        "duplicate_rows_count": duplicate_rows_count,
        "duplicate_fraud_records": dup_fraud,
        "duplicate_legit_records": dup_legit,
        "time_min": float(df["Time"].min()),
        "time_max": float(df["Time"].max()),
        "amount_min": float(df["Amount"].min()),
        "amount_max": float(df["Amount"].max()),
        "amount_mean": round(float(df["Amount"].mean()), 2),
        "amount_median": round(float(df["Amount"].median()), 2),
        "fraud_amount_mean": round(float(df[df["Class"] == 1]["Amount"].mean()), 2),
        "legit_amount_mean": round(float(df[df["Class"] == 0]["Amount"].mean()), 2),
    }
    
    logger.info("=== Dataset Inspection Summary ===")
    logger.info(f"Total Transactions: {total_records:,}")
    logger.info(f"Legitimate (Class 0): {legit_count:,} ({100 - fraud_pct:.4f}%)")
    logger.info(f"Fraudulent (Class 1): {fraud_count:,} ({fraud_pct:.4f}%)")
    logger.info(f"Total Missing Values: {null_total}")
    logger.info(f"Duplicate Rows Count: {duplicate_rows_count:,} (Includes {dup_fraud} fraudulent occurrences)")
    logger.info(f"Transaction Amount: Mean=${summary['amount_mean']}, Max=${summary['amount_max']}")
    logger.info(f"Fraud Mean Amount: ${summary['fraud_amount_mean']} vs Legit Mean Amount: ${summary['legit_amount_mean']}")
    
    return summary


def preprocess_data(df: pd.DataFrame, handle_duplicates: str = "keep") -> pd.DataFrame:
    """
    Cleans and prepares data without data leakage.
    handle_duplicates: 'keep' (default) preserves all transactional records because in
    credit card fraud, duplicate transactions often represent repeated fraud attempts (retry storms).
    'drop' removes duplicate rows if explicitly instructed.
    """
    clean_df = df.copy()
    
    if handle_duplicates == "drop":
        before = len(clean_df)
        clean_df = clean_df.drop_duplicates()
        logger.info(f"Dropped {before - len(clean_df)} duplicate rows. New shape: {clean_df.shape}")
    else:
        logger.info(f"Preserving duplicate rows ({clean_df.duplicated().sum()}) to retain true fraud frequency patterns.")
        
    return clean_df


if __name__ == "__main__":
    df = load_dataset()
    summary = inspect_data(df)
    report = generate_data_quality_report(df)
    print("Data processing inspection completed successfully.")
