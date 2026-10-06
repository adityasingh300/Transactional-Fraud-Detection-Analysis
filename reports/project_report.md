# Analytical Report: Transactional Fraud Detection Analysis

**Project Title:** Transactional Fraud Detection Analysis Using Python, SQL, Machine Learning, and Power BI  
**Author:** Data Analytics Intern  
**Date:** October 2026  
**Tools & Stack:** Python 3, Pandas, NumPy, SQLite, Scikit-learn, Streamlit, Plotly, Joblib  
**Dataset Source:** Kaggle / ULB Machine Learning Group (Credit Card Fraud Detection)  

---

## Table of Contents
1. Executive Summary
2. Business Problem Definition
3. Project Objectives
4. Dataset Description and Source
5. Data Quality Assessment
6. Data Cleaning & Preprocessing Methodology
7. SQL-Based Data Exploration
8. Exploratory Data Analysis (EDA) Methodology
9. Major Analytical Findings (Empirically Grounded)
10. Feature Engineering
11. Machine Learning Model Development
12. Model Evaluation Metrics
13. Confusion Matrix & Trade-off Interpretation
14. Business Implications
15. Strategic Business Recommendations
16. Limitations & Technical Boundaries
17. Conclusion & Next Steps
18. Reproducibility & Deployment Instructions

---

## 1. Executive Summary
Financial fraud poses an ongoing challenge to retail banking, payment gateways, and consumers. In modern payment processors, fraudulent transactions are obscured within hundreds of thousands of legitimate transactions. This report documents the end-to-end design, analysis, modeling, and interactive deployment of a Credit Card Fraud Detection system.

Using a real-world benchmark dataset of **284,807 transactions**, we identified:
- An extreme class imbalance: **492 fraudulent transactions (0.173%)** vs. **284,315 legitimate transactions (99.827%)**.
- A total documented financial fraud loss of **$60,127.97**, with an average fraudulent transaction amount of **$122.21** (peaking at $2,125.87).
- A sharp diurnal fraud spike at **2:00 AM (1.713% fraud incident rate)**, representing a ten-fold increase above baseline.
- An imbalanced machine learning pipeline delivering **90.82% recall** with baseline Logistic Regression and **81.63% recall with 75.47% precision and 0.8433 PR-AUC** with Random Forest.

---

## 2. Business Problem Definition
E-commerce and card-not-present (CNP) transaction volumes continue to expand exponentially. However, unauthorized card usage results in direct financial write-offs, chargeback processing fees (often $15-$50 per dispute), regulatory penalties, and reputational attrition. 

The analytical challenge is dual-faceted:
1. **The Rarity Challenge:** With fewer than 2 frauds per 1,000 transactions, a naive model that predicts "legitimate" for every transaction achieves 99.83% accuracy while missing 100% of fraud.
2. **The Friction vs. Security Dilemma:** Overly aggressive fraud blocking causes false positives (declining legitimate cardholders), which causes embarrassment and lost revenue. An effective solution must balance high recall (fraud catch rate) with viable precision.

---

## 3. Project Objectives
The key objectives of this project are:
- **Data Profiling & Hygiene:** Ingest, inspect, and profile the full transactional corpus without information loss or leakage.
- **SQL Analytics:** Utilize SQLite to demonstrate relational querying, amount tier stratification, and temporal aggregation.
- **Visual Analytics:** Uncover fraud patterns across monetary, temporal, and latent feature dimensions using Matplotlib, Seaborn, and Plotly.
- **Feature Pipeline:** Engineer leak-free temporal (`Hour_of_Day`) and monetary (`Log_Amount`) features integrated into a Scikit-Learn ColumnTransformer pipeline.
- **Supervised Modeling:** Train and evaluate a baseline Logistic Regression classifier with balanced class weights and a comparison Random Forest model.
- **Interactive UI:** Deploy an interactive Streamlit dashboard (`dashboard/app.py`) allowing stakeholders to explore data and score live transactions.
- **Business Roadmap:** Provide concrete operational thresholds and policy recommendations for anti-fraud teams.

---

## 4. Dataset Description and Source
- **Origin:** Collected and shared by the Machine Learning Group at Université Libre de Bruxelles (ULB) via Kaggle.
- **Temporal Span:** Transactions made by European credit cardholders over a two-day duration (48 hours / 172,792 seconds).
- **Dimensions:** 284,807 records, 31 columns.
- **Features:**
  - `Time`: Elapsed seconds from the initial transaction in the dataset.
  - `V1` through `V28`: Principal Component Analysis (PCA) latent feature projections to safeguard cardholder confidentiality.
  - `Amount`: Transaction monetary value in currency units.
  - `Class`: Binary ground-truth label (0 = Legitimate, 1 = Fraudulent).

---

## 5. Data Quality Assessment
Prior to modeling, a column-by-column audit was conducted (`outputs/data_quality_report.csv`):
- **Missing Values:** Exactly **0 missing, null, or NaN values** across all 31 features.
- **Infinite Values:** Exactly **0 positive or negative infinite values**.
- **Data Types:** 30 features are `float64`; target variable `Class` is `int64`.
- **Duplicate Records:** **1,081 duplicate rows** were identified. 
  - Breakdown: 1,822 legitimate rows and 32 fraudulent rows (17 distinct instances).
  - Assessment: In financial streaming systems, identical rows often correspond to transaction retry storms or rapid successive swipes rather than data corruption. Automatically dropping duplicates removes 17 real fraud examples (3.5% of total fraud). Thus, duplicate rows were retained to preserve the true operational risk distribution.

---

## 6. Data Cleaning & Preprocessing Methodology
- **Leakage Prevention:** All scalers and transformers are strictly fit on the training partition (`X_train`) only, and subsequently transformed on test/inference data.
- **Target Separation:** The target column `Class` was isolated prior to feature scaling.
- **Stratified Partitioning:** A Stratified 80/20 train/test split was employed (`stratify=y`, `random_state=42`), allocating:
  - **Training Set:** 227,845 records (394 fraud, 227,451 legit)
  - **Testing Set:** 56,962 records (98 fraud, 56,864 legit)

---

## 7. SQL-Based Data Exploration
A standalone SQLite database (`outputs/fraud_analysis.db`) was constructed and populated to run relational queries (`src/sql_analysis.py`).

### Key SQL Query Results:
1. **Overall Transaction Volume:**
   ```sql
   SELECT COUNT(*), SUM(CASE WHEN Class=1 THEN 1 ELSE 0 END), ROUND(AVG(Class)*100, 4) FROM transactions;
   ```
   *Result:* 284,807 transactions, 492 fraud, **0.1727%** fraud rate.

2. **Amount Tier Stratification:**
   ```sql
   SELECT amount_tier, COUNT(*), SUM(CASE WHEN Class=1 THEN 1 ELSE 0 END) AS fraud_count,
          ROUND(SUM(CASE WHEN Class=1 THEN 1 ELSE 0 END)*100.0/COUNT(*), 4) AS fraud_rate_pct
   FROM transactions GROUP BY amount_tier;
   ```
   *Findings:*
   - **Micro (< $10):** 81,176 transactions, 107 fraud (0.1318% fraud rate)
   - **Small ($10 - $50):** 85,910 transactions, 137 fraud (0.1595% fraud rate)
   - **Medium ($50 - $100):** 44,792 transactions, 77 fraud (0.1719% fraud rate)
   - **Large ($100 - $500):** 62,398 transactions, 149 fraud (**0.2388%** fraud rate)
   - **High ($500 - $1,000):** 7,052 transactions, 16 fraud (0.2269% fraud rate)
   - **Very High ($1,000+):** 3,479 transactions, 6 fraud (0.1725% fraud rate)

---

## 8. Exploratory Data Analysis (EDA) Methodology
A complete exploratory visualization pipeline was executed (`src/eda.py`), saving high-resolution assets to `reports/figures/`:
1. `01_class_distribution.png`: Linear and logarithmic representation of class imbalance.
2. `02_amount_distribution.png`: Right-skewed monetary values and log-transformed KDE comparisons.
3. `03_amount_by_class_boxplot.png`: Whiskers and interquartile ranges comparing classes.
4. `04_time_distribution.png`: Bimodal cyclical distribution of transactions across 48 hours.
5. `05_fraud_time_hourly_pattern.png`: Diurnal comparison highlighting the nighttime fraud surge.
6. `06_correlation_heatmap.png`: Correlation matrix of top discriminating features with Class.
7. `07_top_features_distribution.png`: Density distributions of V17, V14, V12, V10, V4, V11.
8. `08_amount_bands_fraud_rate.png`: Bar chart of incident rates across amount tiers.
9. `09_scatter_v14_v17.png`: 2D feature projection showing separation of fraud instances.

---

## 9. Major Analytical Findings (Empirically Grounded)

### Finding 1: Extreme Rarity of Fraud
- 492 fraud cases across 284,807 transactions.
- Ratio: **1 fraud per 578 legitimate transactions**.
- Standard classification models using default 50% thresholds without imbalance handling fail completely on this distribution.

### Finding 2: Higher Fraud Mean vs. Lower Median
- **Legitimate:** Mean = $88.29, Median = $22.00, Max = $25,691.16
- **Fraudulent:** Mean = **$122.21**, Median = **$9.25**, Max = $2,125.87
- **Interpretation:** Fraudsters commonly initiate low-value "card verification" probes ($1.00 or micro-charges), followed by large bursts up to several hundred or thousand dollars.

### Finding 3: Diurnal Nighttime Surge
- The overall transaction rate drops significantly during nighttime (12:00 AM - 5:00 AM).
- Fraudulent transactions persist throughout the night, causing the fraud incident rate to climb to **1.713% at 2:00 AM** and **1.041% at 4:00 AM** (compared to the 0.173% baseline).

### Finding 4: Key Discriminative Features
- **Strongest Negative Associations with Fraud:**
  - `V17`: $r = -0.3265$
  - `V14`: $r = -0.3025$
  - `V12`: $r = -0.2606$
  - `V10`: $r = -0.2169$
  - `V16`: $r = -0.1965$
- **Strongest Positive Associations with Fraud:**
  - `V11`: $r = +0.1549$
  - `V4`: $r = +0.1334$
  - `V2`: $r = +0.0913$

---

## 10. Feature Engineering
Implemented in `src/feature_engineering.py`:
1. **`Hour_of_Day`:** Calculated as `(Time // 3600) % 24`. Incorporates the cyclical daily rhythm discovered during EDA.
2. **`Log_Amount`:** Calculated as `log1p(max(Amount, 0))`. Normalizes the severe right-skewness of monetary values.
3. **Scaling Strategy:**
   - `RobustScaler`: Applied to `Time`, `Amount`, `Hour_of_Day`, `Log_Amount` to prevent extreme outliers from biasing gradient updates.
   - `StandardScaler`: Applied to `V1` through `V28` (which are already normalized PCA features).
4. **Customer Velocity Note:** The dataset does not contain cardholder or merchant identifiers; per-customer velocity or historical frequency features were deliberately omitted to maintain empirical rigor.

---

## 11. Machine Learning Model Development
Two distinct architectures were developed and trained (`src/train_model.py`):
1. **Baseline Model: Logistic Regression**
   - Optimization: L-BFGS solver with balanced class weighting (`class_weight='balanced'`), $C = 1.0$, `max_iter=1000`.
   - Purpose: Establish an interpretable, transparent linear baseline that penalizes false negatives proportionally to class rarity.
2. **Comparison Model: Random Forest Classifier**
   - Architecture: 100 decision trees, `max_depth=12`, `class_weight='balanced'`, `n_jobs=-1`.
   - Purpose: Capture non-linear feature interactions (such as the joint distribution of V14 and V17) without overfitting.

---

## 12. Model Evaluation Metrics

Evaluated on the independent test set (56,962 transactions; 98 actual fraud cases):

| Metric | Logistic Regression (Baseline) | Random Forest (Comparison) | Winner / Practical Implication |
| :--- | :---: | :---: | :--- |
| **Accuracy** | 97.37% | **99.92%** | Random Forest (+2.55% fewer total misclassifications) |
| **Recall (Fraud Catch Rate)** | **90.82%** | 81.63% | **Logistic Regression** (caught 89/98 vs. 80/98) |
| **Precision** | 5.63% | **75.47%** | **Random Forest** (75.5% precision vs. 5.6%) |
| **F1-Score** | 0.1060 | **0.7843** | **Random Forest** (significantly better balance) |
| **ROC-AUC** | 0.9734 | **0.9757** | Slight edge to Random Forest |
| **PR-AUC (Average Precision)** | 0.7225 | **0.8433** | **Random Forest** (+12.08% improvement) |

---

## 13. Confusion Matrix & Trade-off Interpretation

### Test Set Breakdown:
- **Logistic Regression:**
  - True Negatives: **55,372**
  - False Positives (False Alarms): **1,492**
  - False Negatives (Missed Fraud): **9**
  - True Positives (Caught Fraud): **89**
  - *Operational Ratio:* **16.8 false alarms** per genuine fraud detected.

- **Random Forest:**
  - True Negatives: **56,838**
  - False Positives (False Alarms): **26**
  - False Negatives (Missed Fraud): **18**
  - True Positives (Caught Fraud): **80**
  - *Operational Ratio:* **0.32 false alarms** per genuine fraud detected.

### The Business Trade-off:
- Logistic Regression prevents **90.8% of fraudulent losses**, but forces operations teams to investigate **1,492 false alarms**.
- Random Forest misses 9 additional fraudulent transactions compared to Logistic Regression (80 vs. 89), but **eliminates 1,466 false alarms (a 98.3% reduction)**. This dramatically cuts manual review labor costs and reduces cardholder friction.

---

## 14. Business Implications
1. **Cost of False Negatives (Missed Fraud):** Direct chargeback loss (average fraud cost: $122.21 + $25 dispute fee = ~$147 per occurrence).
2. **Cost of False Positives (False Declines):** Unnecessary customer friction, abandoned carts, and potential churn.
3. **Threshold Calibration:** Rather than using a static 50% cutoff, financial institutions should vary thresholds dynamically based on transaction amount and time of day.

---

## 15. Strategic Business Recommendations

1. **Implement a Three-Tier Real-Time Decision Matrix:**
   - **Tier 1 (Probability < 30%): Automated Approval.** Frictionless authorization for ~99.5% of transaction volume.
   - **Tier 2 (Probability 30% - 70%): Step-Up Verification.** Route to 3D-Secure, SMS One-Time Passcode (OTP), or biometric verification rather than immediate decline.
   - **Tier 3 (Probability ≥ 70%): Automated Block & Customer Notification.** Instant authorization denial with a push notification to confirm legitimate cardholder possession.

2. **Nighttime Scrutiny Rule (2:00 AM - 4:00 AM):**
   - Automatically lower the risk threshold for card-not-present transactions exceeding $100 during early morning hours.

3. **Hybrid Model Deployment:**
   - Deploy the **Random Forest model** as the primary real-time inference engine due to its superior precision (75.5%) and PR-AUC (0.8433).
   - Use Logistic Regression coefficients as an explainability benchmark for regulatory compliance (e.g., Fair Credit Reporting Act disclosures).

---

## 16. Limitations & Technical Boundaries
- **PCA Anonymization:** Because V1 through V28 are anonymized latent features, physical explanations (e.g., merchant category code, IP geolocation) cannot be directly mapped without original metadata.
- **Absence of Customer IDs:** Longitudinal velocity features (e.g., transactions in last 1 hour per user) cannot be constructed from this dataset.
- **Concept Drift:** Transactional patterns evolve rapidly as fraudsters adapt techniques; periodic retraining (e.g., bi-weekly) and drift monitoring are required in production.

---

## 17. Conclusion & Next Steps
This project successfully delivers an end-to-end fraud analytics solution, spanning exploratory analysis, SQL queries, reproducible Scikit-Learn pipelines, supervised model benchmarking, and an interactive Streamlit UI. Future improvements include integrating graph-based relational analytics and incorporating real-time streaming architectures with Apache Kafka.

---

## 18. Reproducibility & Deployment Instructions

### Prerequisites
- Python 3.10+ installed
- Repository cloned

### Setup & Execution Commands
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the complete analysis pipeline
python run_project.py

# 3. Execute automated test suite
pytest tests/test_pipeline.py -v

# 4. Launch interactive Streamlit dashboard
streamlit run dashboard/app.py
```
