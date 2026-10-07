# Transactional Fraud Detection Analysis
### Using Python, SQL, Machine Learning, and Streamlit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completed%20%26%20Validated-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-10%20Passed%20(100%25)-success.svg)]()
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://transactional-fraud-detection-analysis.streamlit.app/)

> 🚀 **Live Demo:** [transactional-fraud-detection-analysis.streamlit.app](https://transactional-fraud-detection-analysis.streamlit.app/)



A comprehensive, end-to-end data analytics and machine learning internship project demonstrating financial transaction fraud detection using the real-world Kaggle ULB Credit Card Fraud dataset (284,807 transactions).

---

## 📌 Project Overview
Financial fraud represents an adversarial, multi-billion-dollar challenge. In digital payments, fraudulent transactions are obscured within millions of legitimate card activities, typically comprising less than **0.2%** of volume.

This project delivers:
1. **Data Profiling & Preprocessing:** Clean, leak-free ingestion and audit of 284,807 transactions.
2. **Relational SQL Analytics:** Standalone SQLite database (`outputs/fraud_analysis.db`) executing parameterized financial queries.
3. **Exploratory Data Analysis (EDA):** Identification of monetary patterns, diurnal vulnerability spikes, and latent feature correlations.
4. **Leak-Free Machine Learning:** Scikit-Learn Pipelines training a baseline Logistic Regression (balanced) and comparison Random Forest classifier.
5. **Interactive Streamlit Dashboard:** Multi-page dashboard with executive KPIs, transaction explorer, and real-time transaction scoring demo.
6. **Automated Testing:** Pytest test suite validating data integrity, model inference, and artifact generation.
7. **Complete Documentation & Slides:** 19-section analytical report, executive summary, 10-slide presentation in Markdown and PowerPoint (`.pptx`), and an executed Jupyter Notebook.

---

## 📁 Project Structure

```text
Transactional Fraud Detection Analysis/
│
├── data/
│   └── README.md                               # Dataset documentation & path resolution
│
├── notebooks/
│   └── fraud_detection_analysis.ipynb          # Fully executed Jupyter Notebook with all outputs
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py                      # Data loading, profiling & quality audit
│   ├── sql_analysis.py                         # SQLite database ingestion & analytical queries
│   ├── eda.py                                  # Visualizations & statistical findings generator
│   ├── feature_engineering.py                  # Leak-free transformer & scaling pipeline
│   ├── train_model.py                          # Supervised model training, evaluation & serialization
│   └── predict.py                              # Standalone inference & risk-tier scoring engine
│
├── dashboard/
│   └── app.py                                  # Interactive Streamlit & Plotly dashboard
│
├── models/
│   ├── fraud_detection_model.joblib            # Primary production model pipeline (Random Forest)
│   ├── logistic_regression_model.joblib        # Baseline model pipeline
│   └── random_forest_model.joblib              # Comparison model pipeline
│
├── reports/
│   ├── figures/                                # 12 publication-grade charts (PNG)
│   ├── project_report.md                       # Comprehensive 19-section internship report
│   ├── executive_summary.md                    # C-suite executive summary
│   ├── findings.json                           # Structured empirical statistics
│   ├── presentation.md                         # 10-slide presentation deck with speaker notes
│   └── fraud_detection_presentation.pptx       # Ready-to-present PowerPoint slide deck
│
├── tests/
│   └── test_pipeline.py                        # Automated pytest test suite (8 tests)
│
├── outputs/
│   ├── data_quality_report.csv                 # Detailed column audit
│   ├── model_metrics.json                      # Formal test metrics (JSON)
│   ├── classification_report.txt               # Precision, recall, F1 summary
│   ├── confusion_matrix.csv                    # Confusion matrix breakdown
│   ├── predictions_sample.csv                  # Test sample predictions with risk probabilities
│   ├── logistic_regression_coefficients.csv    # Interpretability coefficients
│   └── fraud_analysis.db                       # Relational SQLite database
│
├── requirements.txt                            # Pinned Python package dependencies
├── README.md                                   # Project documentation
├── .gitignore                                  # Git exclusion patterns
└── run_project.py                              # Master orchestrator script
```

---

## 📊 Key Empirical Findings

From analysis of **284,807 transactions** ($25,162,590.01 total volume):

| Metric | Ground Truth Value | Analysis & Implication |
| :--- | :--- | :--- |
| **Total Transactions** | 284,807 | Complete 48-hour corpus |
| **Legitimate Transactions (Class 0)** | 284,315 (99.827%) | High volume majority traffic |
| **Fraudulent Transactions (Class 1)** | 492 (0.173%) | Extreme rarity (1 fraud per 578 legitimate) |
| **Total Fraud Financial Loss** | $60,127.97 | Documented fraud losses in corpus |
| **Average Amount: Legit vs Fraud** | $88.29 vs. **$122.21** | Fraud average is 38.4% higher than legit |
| **Peak Fraud Rate Hour** | **2:00 AM (1.713%)** | ~10x surge over baseline (nighttime vulnerability) |
| **Missing Values** | **0** | Clean tabular corpus |
| **Duplicate Records** | 1,081 (32 fraud) | Retained to preserve automated card testing patterns |

---

## 🤖 Machine Learning Model Benchmarking

Evaluated on an independent, stratified test partition of **56,962 transactions (98 true frauds)**:

| Metric | Logistic Regression (Baseline, Balanced) | Random Forest (Comparison, Balanced) | Operational Significance |
| :--- | :---: | :---: | :--- |
| **Accuracy** | 97.37% | **99.92%** | Accuracy is non-informative due to imbalance |
| **Recall (Catch Rate)** | **90.82%** (89 / 98) | 81.63% (80 / 98) | Logistic Regression catches more raw frauds |
| **Precision** | 5.63% | **75.47%** | Random Forest delivers 13.4x higher precision |
| **F1-Score** | 0.1060 | **0.7843** | Harmonic balance of precision and recall |
| **ROC-AUC** | 0.9734 | **0.9757** | Excellent overall ranking capability |
| **PR-AUC (Primary Metric)** | 0.7225 | **0.8433** | **Random Forest wins (+12.08% improvement)** |
| **False Positives (Alarms)** | 1,492 | **26** | **98.3% reduction in false alarms** |

### Operational Trade-off
- **Logistic Regression** maximizes recall (catching 90.8% of frauds), but yields **1,492 false alarms** (requiring extensive manual review queues).
- **Random Forest** cuts false alarms by **98.3% down to just 26**, saving hundreds of hours in operational investigation time while still catching **81.6%** of all fraud.

---

## 🚀 Quickstart & Reproduction Guide

### 1. Prerequisites & Environment Setup
Clone the repository and install required packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Entire Pipeline
Execute the master orchestrator to run data profiling, SQL analytics, EDA chart generation, model training, and test validation:
```bash
python run_project.py
```

### 3. Launch the Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
*The dashboard will launch locally at `http://localhost:8501` featuring executive KPIs, transaction filtering, and a live prediction sandbox.*

### 4. Run Automated Test Suite
```bash
pytest tests/test_pipeline.py -v
```

### 5. Perform Standalone Inference
```bash
python src/predict.py
```

---

## 💡 Strategic Business Recommendations

1. **Three-Tier Transaction Routing Engine:**
   - **Low Risk (< 30% Probability):** Frictionless one-click authorization (99.5% of traffic).
   - **Medium Risk (30% - 70% Probability):** Challenge with Step-Up Multi-Factor Authentication (SMS OTP / 3D-Secure) rather than outright decline.
   - **High Risk (≥ 70% Probability):** Automated block and push notification to cardholder.
2. **Nighttime Scrutiny Rule (2:00 AM - 4:00 AM):**
   - Automatically lower the risk threshold for card-not-present transactions exceeding $100 during early morning hours when fraud incident rate spikes to **1.71%**.
3. **Hybrid Model Architecture:**
   - Deploy Random Forest as the primary automated decision engine for high precision and minimal false alarms.
   - Utilize Logistic Regression coefficients to generate human-readable explainability reports for regulatory transparency.

---

## 📜 License
This project is licensed under the Apache 2.0 License.
