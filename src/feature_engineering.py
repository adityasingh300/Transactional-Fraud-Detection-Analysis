"""
feature_engineering.py
Feature engineering and transformation pipeline for credit card fraud detection.
Ensures zero data leakage by strictly fitting transformations on training data only.
"""

import logging
from typing import Tuple, List
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


class TransactionFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom Scikit-Learn Transformer to engineer temporal and monetary features.
    
    Engineered Features:
    1. Hour_of_Day: Derived from Time in seconds ((Time // 3600) % 24).
       Captures diurnal risk patterns (e.g., night-time fraud spikes).
    2. Log_Amount: Logarithmic transformation (log1p) of transaction amount.
       Handles extreme right-skewness and compresses wide dynamic range of financial values.
       
    Note on Customer Velocity:
    The dataset does not contain an explicit Customer ID or Account ID. Therefore,
    per-customer transaction velocity / frequency cannot be computed without making
    unverified assumptions. We explicitly focus on transaction-level features.
    """
    
    def __init__(self):
        self.feature_names_out_ = None
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Convert to DataFrame if numpy array
        if isinstance(X, np.ndarray):
            # Assume standard column ordering: Time, V1..V28, Amount
            col_names = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
            df = pd.DataFrame(X, columns=col_names)
        else:
            df = X.copy()
            
        # Ensure numeric types
        df["Time"] = pd.to_numeric(df["Time"], errors="coerce").fillna(0)
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        
        # 1. Hour of Day (0 to 23)
        df["Hour_of_Day"] = ((df["Time"] // 3600) % 24).astype(float)
        
        # 2. Log-transformed Amount
        df["Log_Amount"] = np.log1p(np.maximum(df["Amount"], 0))
        
        self.feature_names_out_ = list(df.columns)
        return df

    def get_feature_names_out(self, input_features=None):
        return np.array(self.feature_names_out_)


def create_preprocessor() -> Pipeline:
    """
    Creates an end-to-end preprocessing pipeline combining feature engineering and scaling.
    
    Architecture:
    - Step 1: TransactionFeatureEngineer creates 'Hour_of_Day' and 'Log_Amount'.
    - Step 2: ColumnTransformer scales:
        * 'Time', 'Amount', 'Log_Amount', 'Hour_of_Day' using RobustScaler (resistant to financial outliers).
        * 'V1' through 'V28' (already PCA normalized) pass through or undergo standard scaling.
    """
    pca_features = [f"V{i}" for i in range(1, 29)]
    monetary_temporal_features = ["Time", "Amount", "Hour_of_Day", "Log_Amount"]
    
    column_scaler = ColumnTransformer(
        transformers=[
            ("scaler_monetary", RobustScaler(), monetary_temporal_features),
            ("scaler_pca", StandardScaler(), pca_features)
        ],
        remainder="passthrough"
    )
    
    preprocessor = Pipeline(
        steps=[
            ("engineer", TransactionFeatureEngineer()),
            ("scale", column_scaler)
        ]
    )
    return preprocessor


def get_feature_names() -> List[str]:
    """
    Returns the list of final feature names produced by the preprocessing pipeline.
    """
    pca_features = [f"V{i}" for i in range(1, 29)]
    monetary_temporal_features = ["Time", "Amount", "Hour_of_Day", "Log_Amount"]
    return monetary_temporal_features + pca_features


if __name__ == "__main__":
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.data_processing import load_dataset
    
    df = load_dataset()
    X = df.drop(columns=["Class"])
    pipeline = create_preprocessor()
    X_trans = pipeline.fit_transform(X.head(100))
    print(f"Original features count: {X.shape[1]}")
    print(f"Transformed features shape: {X_trans.shape}")
    print("Feature engineering pipeline validated successfully.")
