# Internship Presentation: Transactional Fraud Detection Analysis

**Project Title:** Transactional Fraud Detection Analysis Using Python, SQL, Machine Learning, and Power BI  
**Author:** Data Analytics Intern  
**Date:** October 2026  
**Format:** 10 Slides with Complete Speaker Notes  

---

## Slide 1: Title & Introduction
**Title:** Transactional Fraud Detection Analysis  
**Subtitle:** Scalable Machine Learning and Advanced Analytics for Financial Risk Mitigation  
**Tech Stack:** Python, Pandas, SQLite, Scikit-learn, Streamlit, Plotly  

> **Speaker Notes:**  
> "Good morning, everyone. Today I am presenting my end-to-end internship project on Transactional Fraud Detection Analysis. In this project, I engineered a complete data pipeline, conducted relational SQL investigations, uncovered critical fraud patterns, and trained supervised classification models to safeguard digital transactions without disrupting genuine cardholders."

---

## Slide 2: The Business Problem
- **Multi-Billion Dollar Impact:** Global card fraud exceeds $30 billion annually in unauthorized charges and dispute expenses.
- **The Needle in the Haystack:** Fraud represents under 0.2% of total transaction volume.
- **The False Decline Dilemma:** Aggressive rules anger genuine customers; lax rules lead to heavy financial losses.
- **Goal:** Develop an intelligent, automated detection engine that maximizes fraud catch rate while minimizing customer friction.

> **Speaker Notes:**  
> "The fundamental challenge in fraud detection is finding a very rare needle in an enormous haystack. With less than two fraudulent transactions for every thousand legitimate ones, standard accuracy metrics fail. Our goal is to balance fraud detection with preserving customer trust."

---

## Slide 3: Project Objectives
1. **Data Profiling & Preprocessing:** Audit 284,807 transactions without data loss or leakage.
2. **Relational SQL Analysis:** Execute parameterized queries on a custom SQLite database.
3. **Exploratory Data Analysis (EDA):** Uncover monetary, diurnal, and multidimensional fraud characteristics.
4. **Leak-Free Machine Learning:** Train and benchmark baseline Logistic Regression against Random Forest using balanced class weighting.
5. **Interactive Deployment:** Deliver a production-grade Streamlit monitoring dashboard and live inference demo.

> **Speaker Notes:**  
> "Our roadmap spanned five clear milestones: thorough data profiling, relational querying in SQLite, exploratory visual analytics, leak-free machine learning, and an interactive dashboard built with Streamlit and Plotly for executive demonstration."

---

## Slide 4: Dataset Overview & Characteristics
- **Dataset Source:** Kaggle / ULB Machine Learning Group benchmark.
- **Transaction Scope:** 284,807 transactions collected over a 48-hour period.
- **Target Distribution:**
  - **Legitimate (Class 0):** 284,315 transactions (99.827%)
  - **Fraudulent (Class 1):** 492 transactions (0.173%)
  - **Imbalance Ratio:** 1 fraud per 578 legitimate transactions.
- **Features:** 28 PCA-transformed latent features (`V1` to `V28`), `Time` (seconds elapsed), `Amount` ($), and `Class`.

> **Speaker Notes:**  
> "Looking at the dataset characteristics, we analyzed 284,807 transactions. The class distribution is extremely skewed: 492 frauds against 284,315 legitimate transactions, or 1 fraud for every 578 legitimate purchases. Features V1 through V28 are PCA projections ensuring cardholder privacy."

---

## Slide 5: Data Cleaning & SQL Analytics
- **Data Quality Audit:**
  - Missing Values: **0 across all 31 features**.
  - Infinite Values: **0**.
  - Duplicate Records: 1,081 rows investigated. Identified 32 duplicate fraud transactions—retained to preserve true operational frequency patterns.
- **SQLite Analytics (`outputs/fraud_analysis.db`):**
  - Total Financial Volume: **$25,162,590.01**
  - Total Fraud Loss: **$60,127.97**
  - Average Transaction: **$88.35** overall ($122.21 for Fraud vs. $88.29 for Legit).

> **Speaker Notes:**  
> "During data cleaning, we confirmed zero missing values. We also investigated 1,081 duplicate rows and found 32 fraudulent records among them, choosing to retain them because repeated attempts are common during automated card testing. Our SQLite database queries revealed that while legitimate transactions average $88.29, fraudulent transactions average $122.21, with total fraud loss reaching $60,128."

---

## Slide 6: Key Exploratory Findings & Fraud Patterns
- **Diurnal Vulnerability Spike:**
  - Legitimate transaction volume plunges between midnight and 5:00 AM as cardholders sleep.
  - Fraud persists, driving the **fraud incident rate to 1.713% at 2:00 AM** and **1.041% at 4:00 AM** (an almost 10x surge above baseline!).
- **Amount Profiling:**
  - Fraudsters display a bimodal monetary pattern: micro-charges ($1.00) for balance testing, followed by high-dollar theft up to $2,125.87.
- **Top Discriminative Features:**
  - Strong negative correlations: `V17` (-0.327), `V14` (-0.303), `V12` (-0.261).
  - Strong positive correlations: `V11` (+0.155), `V4` (+0.133).

> **Speaker Notes:**  
> "Our visual analysis revealed a key temporal pattern: a late-night vulnerability spike. At 2:00 AM, the fraud rate climbs to 1.713%, almost ten times the baseline rate. Legitimate shoppers are asleep, but automated bots and overseas attackers remain active. Furthermore, features V17, V14, and V12 provide significant discriminatory separation."

---

## Slide 7: Visualizing the Findings
- **Diurnal Pattern Chart:** Volume drops sharply at night while fraud rate spikes.
- **Boxplots & Log Distributions:** Demonstrating heavy skewness and financial distribution differences.
- **Feature Space Separation:** Scatter plot of V14 vs. V17 shows clear cluster separation of fraud cases from the legitimate sample.
- **Correlation Heatmap:** Documents high-impact signals used in model training.

> **Speaker Notes:**  
> "Here on Slide 7, we see the visual proof. The diurnal chart clearly demonstrates the nighttime risk surge. In the 2D scatter plot of V14 versus V17, you can see how fraudulent points separate into distinct clusters away from the dense mass of legitimate transactions."

---

## Slide 8: Machine Learning Model Development & Results
- **Experimental Setup:** Stratified 80/20 train/test split (56,962 test transactions; 98 actual fraud cases). Zero data leakage.
- **Baseline vs. Comparison Results:**

| Evaluation Metric | Logistic Regression (Baseline) | Random Forest (Comparison) |
| :--- | :---: | :---: |
| **Recall (Catch Rate)** | **90.82%** (89 / 98) | 81.63% (80 / 98) |
| **Precision** | 5.63% | **75.47%** |
| **False Positives (Alarms)** | 1,492 | **26 (98.3% reduction)** |
| **ROC-AUC** | 0.9734 | **0.9757** |
| **PR-AUC (Primary Metric)** | 0.7225 | **0.8433** |

> **Speaker Notes:**  
> "Now let us examine model performance on our test set of nearly 57,000 transactions. Logistic Regression achieved an impressive 90.82% recall, catching 89 out of 98 frauds, but generated 1,492 false alarms. By deploying Random Forest, we cut false alarms by 98.3% down to just 26, while maintaining an 81.63% catch rate and boosting our PR-AUC to 0.8433."

---

## Slide 9: Interactive Dashboard & Business Strategy
- **Interactive Streamlit Dashboard:**
  - Executive KPI metrics & financial breakdown.
  - Interactive multi-criteria Transaction Explorer.
  - Live sandbox scoring with instant fraud risk gauge.
- **Strategic Implementation Roadmap:**
  - **Tier 1 (< 30% Risk):** Frictionless one-click approval (99.5% of volume).
  - **Tier 2 (30% - 70% Risk):** Step-up challenge (SMS OTP / 3DS) preventing customer churn.
  - **Tier 3 (≥ 70% Risk):** Automatic block and instant push notification.
  - **Dynamic Nighttime Rules:** Heightened sensitivity between 2:00 AM and 4:00 AM.

> **Speaker Notes:**  
> "To bridge the gap between machine learning and operational execution, we built an interactive Streamlit dashboard. It enables executives to explore transactional patterns and allows fraud analysts to test live transactions with an immediate risk score. We propose a three-tiered routing engine: frictionless approval below 30% risk, step-up authentication between 30% and 70%, and automated blocking above 70%."

---

## Slide 10: Conclusion, Technical Competencies & Future Scope
- **Internship Deliverables Achieved:**
  - Full data engineering, SQL, and exploratory pipelines.
  - Leak-free feature engineering with Scikit-learn Pipeline.
  - Production-ready models serialized with Joblib.
  - Comprehensive automated test suite (8/8 unit tests passing).
- **Future Improvements:**
  - Integrate graph database analytics for detecting shared card syndicates.
  - Deploy real-time Kafka streaming with model inference APIs.

> **Speaker Notes:**  
> "In conclusion, this project delivers a production-grade, mathematically sound, and operationally viable fraud detection system. All automated tests pass, the code is fully modular and reproducible, and the dashboard is ready for deployment. Thank you for your time, and I welcome any questions."
