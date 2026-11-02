# Transactional Fraud Detection Analysis - Team Role Reallocation & Project Guide

## 1. Executive Context & Team Overview
- **Project:** Transactional Fraud Detection Analysis (Infyntrex Internship Capstone)
- **Dataset:** 284,807 transactions across 48 continuous hours ($25,162,590.01 total volume, 492 confirmed frauds / 0.173%).
- **Primary Presentation Deck:** `reports/transactional_fraud_detection_professional.pptx` (17 slides)
- **Primary Presentation PDF:** `reports/transactional_fraud_detection_professional.pdf`
- **Comprehensive Defense Guide PDF:** `reports/Transactional_Fraud_Detection_Team_Guide_Revised.pdf`

---

## 2. Revised 3-Member Team Ownership Breakdown

### Aditya Kumar (Project Lead, Machine Learning Architect & Business Intelligence)
- **Machine Learning & Modeling:**
  - Designed, trained, and benchmarked Scikit-Learn pipelines (`src/train_model.py`, `src/predict.py`).
  - Benchmarked Baseline Logistic Regression GLM against Production Balanced Random Forest.
  - Solved the **False Alarm Crisis**: slashed false alarms by 98.3% (from 1,492 down to 26), boosting precision to 75.47% and PR-AUC to 0.8433.
  - Handled feature scaling, log-amount transformation, and correlation drivers (V17, V14, V12 vs V11, V4).
- **Power BI & Business Intelligence:**
  - Built the master Star-Schema data model with 1 Fact (`Fact_Transactions`) and 5 Dimensions (`Dim_Time_Analysis`, `Dim_Amount_Segments`, `Dim_Risk_Tiers`, `Fact_Model_Benchmark`, `Dim_Feature_Drivers`).
  - Authored the **Enterprise DAX Measures Library** (35+ formulas for financial ROI, fraud rate, and risk tiering).
  - Developed the standalone executive web app (`PowerBI/dashboard/index.html`) with zero latency and interactive threshold sliders.
- **Economic ROI & Defense Leadership:**
  - Formulated the 3-Tier Dynamic Mitigation Architecture (<30% Clear, 30-70% MFA, >=70% Block).
  - Lead speaker defending model mathematics, financial recovery (+$47,782 net value), and business trade-offs.

### Yash Bhankale (Data Engineering & SQL Forensic Pipeline Lead)
- **Data Engineering & Ingestion Hygiene:**
  - Conducted comprehensive data profiling on the 284,807 transactions; verified zero null values across 31 features.
  - Identified and intentionally retained 1,081 duplicate transactions representing authentic cyber bot retry bursts.
- **Relational SQLite Architecture:**
  - Built and deployed the standalone relational SQLite database (`outputs/fraud_analysis.db`) via `src/sql_analysis.py`.
  - Executed parameterized SQL queries across monetary tiers and temporal velocity windows.
- **Behavioral Forensics & Discoveries:**
  - Discovered the **2:00 AM vulnerability surge**: fraud rate jumps to 1.713% (9.92x baseline risk) as legitimate traffic drops 85%.
  - Uncovered the bi-modal fraud distribution: 27 micro card tests (<$5) followed by high-ticket extractions (>$500).
- **Pipeline Robustness & Testing:**
  - Developed 10 automated test suites in `tests/test_pipeline.py` with a 100% pass rate.

### Anjali Krishna (Documentation & Data Sourcing Associate)
- **Data Collection & Ingestion Sourcing:**
  - Sourced the raw 284,807 transaction corpus from the ULB Machine Learning Group / Kaggle repository.
  - Verified file hashes (SHA-256), structural file health, column counts, and row integrity upon ingestion.
- **Data Dictionary & Schema Cataloging:**
  - Documented the schema metadata, transaction timestamp intervals, and 28 anonymized PCA feature components (V1-V28).
  - Maintained the feature definitions and target label mappings (`Class: 0 = Legit, 1 = Fraud`).
- **Project Documentation & Repository Management:**
  - Authored the repository `README.md`, organized file directory structures, and maintained deliverable checklists.
  - Kept track of team meeting minutes, development sprints, and internship submission guidelines.
- **Presentation Deck Assembly:**
  - Assisted in compiling and formatting the 17-slide master presentation deck (`reports/transactional_fraud_detection_professional.pptx`).
  - Organized speaker notes, verified visual layout consistency, and prepared submission artifacts.

---

## 3. Slide-by-Slide Speaker Allocation (17 Slides)

| Slide | Title & Topic | Assigned Presenter | Key Talking Points |
| :---: | :--- | :---: | :--- |
| **1** | Title & Presentation Introduction | **Anjali Krishna** | Welcome seniors, introduce team members, and state project title and agenda. |
| **2** | Business Context & Dilemma | **Anjali Krishna** | 0.173% rare event fraud, billions in dispute losses, threat of false declines. |
| **3** | 5 Core Technical Pillars | **Aditya Kumar** | High-level architecture: Quality Audit, SQL DB, ML, Power BI, Dynamic Policy. |
| **4** | Dataset Sourcing & Verification | **Anjali Krishna** | ULB/Kaggle dataset origin, 284,807 transactions, zero nulls, PCA privacy. |
| **5** | Data Cleaning & SQLite DB | **Yash Bhankale** | Retaining 1,081 bot duplicates, SQLite database (`fraud_analysis.db`) setup. |
| **6** | 2:00 AM Surge Forensics | **Yash Bhankale** | 1.713% fraud rate surge at 2:00 AM (9.92x baseline risk; legitimate volume drops 85%). |
| **7** | Monetary Tiers & Bi-Modal | **Yash Bhankale** | Micro card tests (<$5) vs high-ticket extractions (>$500 driving 40% of losses). |
| **8-10**| Latent PCA Space & Drivers | **Aditya Kumar** | V14 vs V17 clustering; negative anchors (V17, V14, V12) vs positive bursts (V11, V4). |
| **11** | Leak-Free Pre-Processing | **Aditya Kumar** | Scikit-Learn transformers, log-amount scaling, sine-cosine hour encoding. |
| **12** | Baseline Logistic Regression | **Aditya Kumar** | Directional odds ratios; validation of negative coefficients for V14 and V17. |
| **13-15**| ML Benchmarks & Breakthrough | **Aditya Kumar** | ROC-AUC flaw vs PR-AUC (0.8433); slashing false alarms from 1,492 to 26; saving $73.3k. |
| **16** | Power BI Dashboard & 3 Tiers | **Aditya Kumar** | Tier 1 (<30% Clear), Tier 2 (30-70% Step-up MFA at 2 AM), Tier 3 (>=70% Freeze). |
| **17** | Documentation & Conclusion | **Anjali & Aditya** | Anjali covers documentation/reproducibility; Aditya closes with production readiness. |

---

## 4. Senior Q&A Defense Matrix (Who Answers What)

1. **"Where was the dataset sourced, and how was data integrity verified?"**
   - **Speaker:** **Anjali Krishna**
   - **Answer:** Sourced from ULB Machine Learning Group via Kaggle (284,807 transactions over 48 hours). Verified via SHA-256 checksums, confirmed zero nulls across 31 features, cataloged V1-V28 PCA anonymity.
2. **"How did the team ensure reproducibility and document tracking?"**
   - **Speaker:** **Anjali Krishna**
   - **Answer:** Established modular repository conventions, maintained meeting logs and README, tracked submission checklists, and pinned dependencies in `requirements.txt`.
3. **"Why not issue a blanket block on all transactions during the 2:00 AM window?"**
   - **Speaker:** **Yash Bhankale**
   - **Answer:** 98.287% of 2:00 AM transactions are legitimate. A blanket block destroys customer trust and sales. We selectively apply Step-Up MFA and lower verification thresholds for nighttime transactions above $150.
4. **"Why did you preserve 1,081 duplicate transactions?"**
   - **Speaker:** **Yash Bhankale**
   - **Answer:** Cyber bots fire rapid retry bursts with identical card amounts. Dropping duplicates deletes genuine cyber attack signatures. Preserving them ensures models learn bot retry behavior.
5. **"Why construct a dedicated SQLite database instead of querying pandas in memory?"**
   - **Speaker:** **Yash Bhankale**
   - **Answer:** Banking compliance requires auditable, reproducible SQL queries rather than ephemeral script memory. `fraud_analysis.db` ensures query auditability and mirrors enterprise lakehouses.
6. **"Why choose Random Forest over Logistic Regression when Logistic Regression had higher Recall (90.8% vs 81.6%)?"**
   - **Speaker:** **Aditya Kumar**
   - **Answer:** Logistic Regression triggered 1,492 false alarms, costing 373 analyst hours ($18,650 in labor) and customer churn. Random Forest triggered only 26 false alarms (98.3% drop), saving $73,300 in review overhead and delivering +$47,782 net value vs -$19,991 deficit.
7. **"Why not use SMOTE or oversampling on the minority class?"**
   - **Speaker:** **Aditya Kumar**
   - **Answer:** SMOTE interpolates artificial points that cross non-linear boundaries in rare-event data (0.173%), distorting probability calibration and inflating false positives. We used cost-sensitive class weights and threshold tuning directly.
8. **"Why build an Excel Star-Schema and web app instead of just sharing a notebook?"**
   - **Speaker:** **Aditya Kumar**
   - **Answer:** Non-technical executives and risk managers need interactive, slicer-driven dashboards. The Star Schema enables instant slicing across time, amount, and risk, while the web app runs anywhere without Python.