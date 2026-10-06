# Executive Summary: Transactional Fraud Detection Analysis

**Project Title:** Transactional Fraud Detection Analysis Using Python, SQL, Machine Learning, and Power BI  
**Author:** Data Analytics Intern  
**Date:** October 2026  
**Status:** Completed & Validated  

---

## 1. Executive Context & Business Problem
Financial fraud threatens customer trust, causes direct chargeback losses, and imposes severe operational costs. In high-volume credit card networks, fraudulent transactions account for less than **0.2%** of all transactional volume, requiring robust predictive systems capable of identifying needles in an immense haystack without degrading the user experience through false declines.

---

## 2. Key Empirical Findings
From an end-to-end analysis of **284,807 transactions** ($25.16M total volume):

1. **Extreme Class Imbalance:**
   - **Legitimate Transactions:** 284,315 (99.827%)
   - **Fraudulent Transactions:** 492 (0.173%)
   - **Imbalance Ratio:** 1 fraudulent transaction for every **578 legitimate transactions**.
   - **Total Financial Fraud Loss in Dataset:** **$60,127.97**

2. **Monetary Profile:**
   - Overall average transaction amount: **$88.35**
   - Fraudulent transactions have a **significantly higher mean value ($122.21)** compared to legitimate transactions (**$88.29**), but a lower median ($9.25 vs. $22.00). Fraudsters frequently conduct small balance checks before making high-value unauthorized transactions (up to $2,125.87).

3. **Critical Diurnal Fraud Spike:**
   - While normal transaction activity plummets between midnight and 5:00 AM, fraudulent transactions persist.
   - At **2:00 AM**, the fraud rate climbs to **1.713%** — an almost **10x surge** over the baseline fraud rate (0.173%).

4. **Predictive Latent Signals:**
   - Features `V17` ($r = -0.3265$), `V14` ($r = -0.3025$), and `V12` ($r = -0.2606$) exhibit the strongest negative correlation with fraud.
   - Features `V11` ($r = +0.1549$) and `V4` ($r = +0.1334$) exhibit the strongest positive correlation with fraud.

---

## 3. Machine Learning Benchmark & Operational Impact

Evaluated on an independent, stratified test set of **56,962 transactions** containing **98 actual fraud cases**:

| Model Architecture | Precision | Recall (Catch Rate) | F1-Score | ROC-AUC | PR-AUC | False Positives | True Positives (Caught) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Baseline, Balanced)** | 5.63% | **90.82%** | 0.1060 | 0.9734 | 0.7225 | 1,492 | **89 / 98** |
| **Random Forest (Comparison, Balanced)** | **75.47%** | **81.63%** | **0.7843** | **0.9757** | **0.8433** | **26** | **80 / 98** |

### Operational Trade-off Analysis:
- **Baseline Logistic Regression** prioritizes maximum fraud detection (catching 89 out of 98 frauds, 90.82%), but generates **1,492 false alarms** (~17 false alarms for every genuine fraud caught). This creates a heavy workload for fraud investigation teams.
- **Random Forest** cuts false alarms by **98.3% (from 1,492 down to 26)** while maintaining an **81.63% catch rate** (80 out of 98 frauds caught), producing a Precision-Recall AUC of **0.8433**.

---

## 4. Strategic Recommendations
1. **Multi-Tiered Decision Engine:**
   - *Risk < 30%:* Auto-approve immediately (frictionless checkout).
   - *Risk 30% - 70%:* Trigger Step-Up Multi-Factor Authentication (OTP / 3DS challenge) instead of immediate decline.
   - *Risk ≥ 70%:* Automatic freeze, alert cardholder via instant SMS/push notification.
2. **Nighttime Dynamic Rules (2:00 AM - 4:00 AM):**
   - Apply heightened sensitivity thresholds to cross-border or high-amount card-not-present (CNP) transactions during late-night windows.
3. **Continuous Deployment:**
   - Deploy Random Forest as the primary automated classification engine, with threshold tuning based on current fraud team review capacity.
