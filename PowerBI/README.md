# Power BI Risk Intelligence & Fraud Detection Dashboard Suite
### Infyntrex Internship Capstone Project

This directory contains the **Power BI Dashboard Suite**, **Curated Star-Schema Data Models**, **35+ Enterprise DAX Measures Library**, **Corporate Executive Dark Theme (Zero AI Clutter)**, **PowerPoint Presentation Deck**, and **Executive Presentation Script** for presenting to company stakeholders.

---

## 🚀 Quick Launch Options

### Option 1: Power BI Desktop Project (`.pbip`)
- **File:** `Transactional_Fraud_Detection_Dashboard.pbip`
- **How to open:** In Power BI Desktop, select `File` -> `Open` -> `Browse reports` -> select `Transactional_Fraud_Detection_Dashboard.pbip`.
- **Contains:** 4 full report pages, complete Tabular Model TMSL schema (`model.bim`), relationships, and pre-calculated DAX measures.

### Option 2: Power BI Template (`.pbit`)
- **File:** `Transactional_Fraud_Detection_Dashboard.pbit`
- **How to open:** Double-click the file in Windows Explorer. Power BI Desktop will launch and connect to the local curated data files in `data/`.

### Option 3: Standalone Interactive Power BI Dashboard Application
- **File:** `dashboard/index.html`
- **How to open:** Double-click to open in any web browser (Chrome, Edge).
- **Features:** High-fidelity Power BI UI, live slicers (Diurnal Time Windows, Monetary Segments, Fraud Status), interactive confusion matrix toggle (Random Forest vs Logistic Regression), full-screen presenter mode (`F11`), and presenter notes drawer (`🎙️ Presenter Notes`).

### Option 4: Executive PowerPoint Slide Deck
- **File:** `Fraud_Detection_PowerBI_Presentation.pptx`
- **How to open:** Open in Microsoft PowerPoint. Contains 10 professionally formatted slides styled with the custom executive dark theme (no AI background clutter).

---

## 📊 Core Empirical Metrics to Quote

| Metric | Ground Truth Value | Presentation Talking Point |
| :--- | :--- | :--- |
| **Total Transaction Corpus** | 284,807 transactions | Complete 48-hour audited transactional snapshot |
| **Gross Portfolio Volume** | $25,162,590.01 ($25.16M) | High-velocity card payment network flow |
| **Confirmed Fraud Volume** | 492 cases (0.173%) | Extreme rarity: **1 fraud per 578 legitimate** |
| **Confirmed Fraud Loss** | $60,127.97 | Direct monetary loss in audited window |
| **Average Ticket Size** | Fraud: $122.21 vs. Legit: $88.29 | Fraud is +38.4% higher than legitimate |
| **Median Ticket Size** | Fraud: $9.25 vs. Legit: $22.00 | Fraud has lower median due to micro card probes (<$5) |
| **Critical Diurnal Peak** | **2:00 AM (1.713% Fraud Rate)** | **9.9x surge** over the 0.173% baseline risk |
| **Production Model (Random Forest)** | **Precision: 75.47% \| Catch: 81.63%** | PR-AUC: 0.8433 |
| **Baseline Model (Logistic Reg.)** | **Precision: 5.63% \| Catch: 90.82%** | High catch rate, but burns **1,492 false alarms** |
| **False Alarm Reduction** | **-98.3% (1,492 down to 26)** | Eliminates investigator fatigue (0.3 alarms/fraud) |
| **Investigator Labor Saved** | **366.5 hours per test period** | Cuts review time from 373 hours down to 6.5 hours |
| **Net Economic Value** | **+$47,782 (Test) / $122.3k (Scaled)** | Direct prevented fraud losses + eliminated labor costs |

---

## 📁 Directory Structure & Deliverable Manifest

```text
PowerBI/
├── Transactional_Fraud_Detection_Dashboard.pbip       # Native Power BI Desktop Project
├── Transactional_Fraud_Detection_Dashboard.pbit       # Native Power BI Template File
│
├── Transactional_Fraud_Detection_Dashboard.Report/    # Report definition folder
│   ├── definition.pbir                                # PBIR pointer to semantic model
│   └── report.json                                    # 4-page executive visual layout
│
├── Transactional_Fraud_Detection_Dashboard.SemanticModel/ # Semantic Model definition folder
│   ├── definition.pbism                               # PBISM metadata
│   └── model.bim                                      # TMSL Model (Tables, Rel, Measures)
│
├── data/                                              # Curated dimensional star-schema datasets
│   ├── Fraud_Detection_PowerBI_DataModel.xlsx         # Master Excel workbook with 6 formatted sheets
│   ├── Fact_Transactions_Analytical.csv               # 20,000 stratified analytical transactions (41 cols)
│   ├── Fact_Transactions_Full.csv                     # 284,807 full transactions (41 cols)
│   ├── Dim_Time_Analysis.csv                          # 24-hour diurnal risk indices & protocols
│   ├── Dim_Amount_Segments.csv                        # 6 monetary bands & MO profiling
│   ├── Dim_Risk_Tiers.csv                             # 3-tier operational policy specifications
│   ├── Fact_Model_Benchmark.csv                       # Complete ML metrics, confusion matrix & ROI
│   ├── Agg_Hourly_Forensics.csv                       # Hourly aggregations for rapid charting
│   └── Dim_Feature_Drivers.csv                        # Top 10 predictive features with PCA notes
│
├── themes/
│   └── corporate_fraud_theme.json                     # Executive dark theme (zero AI background clutter)
│
├── DAX_Measures_Library.dax                           # 35+ enterprise DAX measures with full comments
├── PowerQuery_ETL_Scripts.m                           # M scripts for Power Query Advanced Editor
├── Fraud_Detection_PowerBI_Presentation.pptx          # 10-slide ready-to-present executive deck
├── PowerBI_Presentation_Guide.md                      # Word-for-word presentation script & Q&A guide
│
└── dashboard/
    └── index.html                                     # Interactive full-screen standalone dashboard app
```

