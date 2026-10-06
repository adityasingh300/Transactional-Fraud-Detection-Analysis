"""
predict.py
Inference module for real-time and batch credit card fraud scoring.
Loads the trained model pipeline and predicts fraud probabilities and risk tiers.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Union, List
import pandas as pd
import numpy as np
import joblib

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.feature_engineering import TransactionFeatureEngineer

logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = os.path.join(project_root, "models", "fraud_detection_model.joblib")


class FraudPredictor:
    """
    Production-grade predictor for scoring transactions.
    """

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}. Train the model first.")
        logger.info(f"Loading fraud detection model from: {self.model_path}")
        self.model = joblib.load(self.model_path)
        self.required_columns = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

    def _validate_and_format_input(self, data: Union[Dict[str, Any], pd.DataFrame, List[Dict[str, Any]]]) -> pd.DataFrame:
        """
        Validates input structure and ensures required features are present.
        """
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise TypeError("Input must be a dictionary, list of dictionaries, or pandas DataFrame.")

        # Ensure all required columns exist, impute 0 for missing latent components if needed
        for col in self.required_columns:
            if col not in df.columns:
                logger.warning(f"Missing column '{col}' in input. Defaulting to 0.0.")
                df[col] = 0.0

        # Ensure correct column ordering
        return df[self.required_columns]

    def predict(self, data: Union[Dict[str, Any], pd.DataFrame, List[Dict[str, Any]]], threshold: float = 0.5) -> pd.DataFrame:
        """
        Scores input transactions and returns predictions, probabilities, and risk tiers.
        """
        df_input = self._validate_and_format_input(data)
        
        # Predict class probabilities
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(df_input)[:, 1]
        else:
            decision = self.model.decision_function(df_input)
            probabilities = 1 / (1 + np.exp(-decision))

        # Apply configurable threshold
        predictions = (probabilities >= threshold).astype(int)
        
        results = df_input.copy()
        results["Fraud_Probability"] = np.round(probabilities, 4)
        results["Predicted_Class"] = predictions
        results["Decision"] = ["Fraudulent" if p == 1 else "Legitimate" for p in predictions]
        
        # Assign Risk Tiers
        risk_tiers = []
        for p in probabilities:
            if p >= 0.70:
                risk_tiers.append("High Risk (Auto-Block / Challenge)")
            elif p >= 0.30:
                risk_tiers.append("Medium Risk (Manual Review Queue)")
            else:
                risk_tiers.append("Low Risk (Standard Approval)")
                
        results["Risk_Tier"] = risk_tiers
        return results


def get_sample_transaction(is_fraud: bool = False) -> Dict[str, Any]:
    """
    Returns a realistic synthetic or sample transaction dictionary for testing.
    """
    sample_path = os.path.join(project_root, "outputs", "predictions_sample.csv")
    if os.path.exists(sample_path):
        sample_df = pd.read_csv(sample_path)
        target_val = 1 if is_fraud else 0
        matching = sample_df[sample_df["Actual_Class"] == target_val]
        if not matching.empty:
            row = matching.iloc[0].to_dict()
            # Clean out non-input columns
            clean_row = {k: row[k] for k in ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]}
            return clean_row

    # Fallback synthetic record
    synth = {f"V{i}": 0.0 for i in range(1, 29)}
    synth["Time"] = 86400.0
    synth["Amount"] = 149.99
    if is_fraud:
        synth["V14"] = -7.5
        synth["V17"] = -10.2
        synth["V12"] = -5.0
        synth["V10"] = -4.5
        synth["V4"] = 4.2
        synth["V11"] = 3.8
    return synth


if __name__ == "__main__":
    predictor = FraudPredictor()
    
    print("\n--- Testing Prediction on Sample Legitimate Transaction ---")
    legit_tx = get_sample_transaction(is_fraud=False)
    legit_res = predictor.predict(legit_tx)
    print(legit_res[["Amount", "Fraud_Probability", "Decision", "Risk_Tier"]].to_string())

    print("\n--- Testing Prediction on Sample Fraudulent Transaction ---")
    fraud_tx = get_sample_transaction(is_fraud=True)
    fraud_res = predictor.predict(fraud_tx)
    print(fraud_res[["Amount", "Fraud_Probability", "Decision", "Risk_Tier"]].to_string())
