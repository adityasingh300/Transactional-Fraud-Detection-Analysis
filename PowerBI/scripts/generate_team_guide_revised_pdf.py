"""
generate_team_guide_revised_pdf.py
Generates a publication-grade, multi-page PDF document containing the REVISED
3-member team project walkthrough, where Anjali Krishna is specifically scoped to
Data Collection, Schema Documentation, and Project Reporting/Presentation Assembly,
while Aditya Kumar and Yash Bhankale handle all ML modeling, Data Engineering,
SQL relational forensics, Power BI Star-Schema modeling, and senior defense.

Uses Microsoft Edge headless print-to-pdf for pixel-perfect typography and tables.
"""

import os
import subprocess
from pathlib import Path

base_dir = Path(r"C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis")
reports_dir = base_dir / "reports"
pbi_dir = base_dir / "PowerBI"
reports_dir.mkdir(parents=True, exist_ok=True)
pbi_dir.mkdir(parents=True, exist_ok=True)

html_path = reports_dir / "Transactional_Fraud_Detection_Team_Guide_Revised.html"
pdf_path = reports_dir / "Transactional_Fraud_Detection_Team_Guide_Revised.pdf"
pdf_copy_path = pbi_dir / "Transactional_Fraud_Detection_Team_Guide_Revised.pdf"
md_path = reports_dir / "Team_Role_Reallocation_and_Project_Guide.md"
md_copy_path = pbi_dir / "Team_Role_Reallocation_and_Project_Guide.md"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Transactional Fraud Detection Analysis - Revised Team Role Distribution & Senior Presentation Guide</title>
  <style>
    @page {
      size: A4;
      margin: 16mm 14mm 16mm 14mm;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.45;
      color: #1e293b;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }

    /* Header Banner */
    .header-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 22px 24px;
      border-radius: 8px;
      margin-bottom: 20px;
      border-left: 6px solid #2563eb;
    }

    .header-tag {
      font-size: 8.5pt;
      font-weight: 700;
      letter-spacing: 1px;
      color: #38bdf8;
      text-transform: uppercase;
      margin-bottom: 4px;
    }

    .header-title {
      font-size: 17.5pt;
      font-weight: 800;
      letter-spacing: -0.3px;
      margin: 0 0 6px 0;
      color: #f8fafc;
      line-height: 1.2;
    }

    .header-sub {
      font-size: 9.5pt;
      color: #94a3b8;
      margin: 0 0 12px 0;
      line-height: 1.4;
    }

    .header-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 8.5pt;
      color: #cbd5e1;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      padding-top: 10px;
    }

    .header-meta span strong {
      color: #ffffff;
    }

    /* Section Styling */
    h2 {
      font-size: 12.5pt;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 5px;
      margin-top: 20px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    h3 {
      font-size: 10.5pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-top: 14px;
      margin-bottom: 6px;
    }

    p {
      margin-top: 0;
      margin-bottom: 8px;
      text-align: justify;
    }

    /* Callouts */
    .callout {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 4px solid #2563eb;
      padding: 10px 14px;
      border-radius: 4px;
      margin-bottom: 14px;
      font-size: 9pt;
    }

    .callout.alert {
      border-left-color: #ef4444;
      background-color: #fef2f2;
    }

    .callout.success {
      border-left-color: #10b981;
      background-color: #f0fdf4;
    }

    .callout.amber {
      border-left-color: #f59e0b;
      background-color: #fffbeb;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 14px;
      font-size: 8.5pt;
    }

    th {
      background-color: #0f172a;
      color: #ffffff;
      text-align: left;
      padding: 7px 9px;
      font-weight: 600;
      font-size: 8pt;
      letter-spacing: 0.3px;
      text-transform: uppercase;
      border: 1px solid #0f172a;
    }

    td {
      padding: 6px 9px;
      border: 1px solid #cbd5e1;
      vertical-align: top;
    }

    tr:nth-child(even) td {
      background-color: #f8fafc;
    }

    .num {
      text-align: right;
      font-family: Consolas, monospace;
    }

    /* Badges */
    .badge {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 10px;
      font-size: 7.5pt;
      font-weight: 700;
      letter-spacing: 0.3px;
    }

    .badge-aditya { background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }
    .badge-yash   { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .badge-anjali { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }

    /* Key Metric Cards */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 14px;
    }

    .metric-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-top: 3px solid #2563eb;
      border-radius: 6px;
      padding: 10px 12px;
      text-align: center;
    }

    .metric-card.crimson { border-top-color: #ef4444; }
    .metric-card.emerald { border-top-color: #10b981; }
    .metric-card.amber   { border-top-color: #f59e0b; }

    .metric-label {
      font-size: 7pt;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 3px;
    }

    .metric-val {
      font-size: 13.5pt;
      font-weight: 800;
      color: #0f172a;
      font-family: Consolas, monospace;
    }

    .metric-sub {
      font-size: 7pt;
      color: #64748b;
      margin-top: 2px;
    }

    /* Page break controls */
    .page-break {
      page-break-before: always;
    }

    .keep-together {
      page-break-inside: avoid;
    }

    .script-block {
      background: #f1f5f9;
      border-left: 3px solid #3b82f6;
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
      margin-bottom: 10px;
      font-style: italic;
      color: #1e293b;
      font-size: 8.5pt;
    }

    .speaker-tag {
      font-style: normal;
      font-weight: 700;
      font-size: 8pt;
      text-transform: uppercase;
      margin-bottom: 3px;
      display: inline-block;
    }

    ul, ol {
      margin-top: 0;
      margin-bottom: 10px;
      padding-left: 18px;
    }

    li {
      margin-bottom: 3px;
    }

    code {
      font-family: Consolas, monospace;
      font-size: 8pt;
      background: #e2e8f0;
      padding: 1px 4px;
      border-radius: 3px;
      color: #0f172a;
    }
  </style>
</head>
<body>

  <!-- =========================================================================
       PAGE 1: BANNER, EXECUTIVE CONTEXT & REVISED TEAM OWNERSHIP
       ========================================================================= -->
  <div class="header-banner">
    <div class="header-tag">INFYNTREX INTERNSHIP CAPSTONE | REVISED TEAM DISTRIBUTION & DEFENSE GUIDE</div>
    <h1 class="header-title">Transactional Fraud Detection Analysis</h1>
    <div class="header-sub">
      A High-Precision Risk Intelligence System: SQL Forensics, Scikit-Learn Benchmarking, Star-Schema Power BI Dashboard & Project Documentation
    </div>
    <div class="header-meta">
      <span><strong>Team Lead & ML/BI Architect:</strong> Aditya Kumar</span>
      <span><strong>Data Engineering & SQL Lead:</strong> Yash Bhankale</span>
      <span><strong>Documentation & Data Sourcing:</strong> Anjali Krishna</span>
      <span><strong>Evaluation Date:</strong> October / November 2026</span>
    </div>
  </div>

  <div class="metric-grid">
    <div class="metric-card">
      <div class="metric-label">Audited Transactions</div>
      <div class="metric-val">284,807</div>
      <div class="metric-sub">48 Hours Continuous Stream</div>
    </div>
    <div class="metric-card crimson">
      <div class="metric-label">Confirmed Fraud Rate</div>
      <div class="metric-val">0.173%</div>
      <div class="metric-sub">492 Frauds | 1 in 578 skew</div>
    </div>
    <div class="metric-card amber">
      <div class="metric-label">2:00 AM Surge Rate</div>
      <div class="metric-val">1.713%</div>
      <div class="metric-sub">9.92x Baseline Risk Multiple</div>
    </div>
    <div class="metric-card emerald">
      <div class="metric-label">False Alarm Slashed</div>
      <div class="metric-val">-98.3%</div>
      <div class="metric-sub">1,492 down to 26 alerts</div>
    </div>
  </div>

  <h2>1. Executive Summary & Core Business Dilemma</h2>
  <p>
    Modern payment gateways face a razor-thin trade-off: stopping criminal fraud while preserving frictionless customer checkout. 
    In our 284,807 transaction corpus ($25.16M gross volume), confirmed fraud accounts for only <strong>0.173%</strong> (492 cases). 
    A naive or overly aggressive detection model catches fraud but triggers catastrophic false alarms&mdash;insulting innocent cardholders 
    and costing $18,650 in manual analyst review. Our team engineered a production framework that maintains an <strong>81.63% fraud catch rate</strong> 
    while cutting false alarms by <strong>98.3%</strong> (from 1,492 down to just 26), delivering <strong>+$47,782</strong> in net financial recovery.
  </p>

  <h2>2. Revised 3-Member Team Ownership & Task Allocation</h2>
  <div class="callout amber">
    <strong>Team Role Realignment Notice:</strong> Technical responsibilities have been strictly divided into deep computational engineering (Aditya & Yash) and comprehensive project governance/data sourcing (Anjali). Anjali manages raw data collection, cataloging, slide deck assembly, and audit documentation, while Aditya and Yash build and defend the ML models, SQL database, Power BI architecture, and financial trade-offs.
  </div>

  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Team Member & Title</th>
        <th style="width: 26%;">Domain Ownership</th>
        <th style="width: 32%;">Core Contributions</th>
        <th style="width: 20%;">Key Deliverables</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span class="badge badge-aditya">ADITYA KUMAR</span><br>
          <strong>Project Lead & ML / BI Architect</strong>
        </td>
        <td>
          &bull; Machine Learning Modeling<br>
          &bull; False Alarm Crisis Resolution<br>
          &bull; Star-Schema Power BI Model<br>
          &bull; Enterprise DAX Library (35+)<br>
          &bull; 3-Tier Mitigation Architecture
        </td>
        <td>
          &bull; Built Scikit-Learn pipelines & trained Balanced Random Forest.<br>
          &bull; Slashed false alarms from 1,492 to 26 (PR-AUC 0.8433).<br>
          &bull; Designed 1 Fact + 5 Dim Star-Schema (<code>DataModel.xlsx</code>).<br>
          &bull; Formulated financial ROI equation & dynamic thresholds.<br>
          &bull; Lead defense speaker on model mathematics & business impact.
        </td>
        <td>
          &bull; <code>src/train_model.py</code><br>
          &bull; <code>models/*.joblib</code><br>
          &bull; <code>PowerBI/DataModel.xlsx</code><br>
          &bull; <code>DAX_Measures.dax</code><br>
          &bull; <code>dashboard/index.html</code>
        </td>
      </tr>
      <tr>
        <td>
          <span class="badge badge-yash">YASH BHANKALE</span><br>
          <strong>Data Engineering & SQL Forensic Lead</strong>
        </td>
        <td>
          &bull; Data Cleaning & Ingestion<br>
          &bull; SQLite Relational DB Build<br>
          &bull; Parameterized SQL Analytics<br>
          &bull; Behavioral Forensics (2 AM)<br>
          &bull; Pytest Pipeline Test Suite
        </td>
        <td>
          &bull; Validated all 284,807 transactions with zero null records.<br>
          &bull; Preserved 1,081 bot retry attack duplicates as true signals.<br>
          &bull; Engineered <code>outputs/fraud_analysis.db</code> SQLite database.<br>
          &bull; Uncovered 2:00 AM vulnerability surge (1.713% fraud rate).<br>
          &bull; Authored 10 automated test suites with 100% pass rate.
        </td>
        <td>
          &bull; <code>src/data_processing.py</code><br>
          &bull; <code>src/sql_analysis.py</code><br>
          &bull; <code>outputs/fraud_analysis.db</code><br>
          &bull; <code>tests/test_pipeline.py</code><br>
          &bull; <code>Agg_Hourly_Forensics.csv</code>
        </td>
      </tr>
      <tr>
        <td>
          <span class="badge badge-anjali">ANJALI KRISHNA</span><br>
          <strong>Documentation & Data Sourcing Associate</strong>
        </td>
        <td>
          &bull; Dataset Sourcing & Ingestion<br>
          &bull; Feature Dictionary Cataloging<br>
          &bull; Project Documentation & Logs<br>
          &bull; Slide Deck Presentation Assembly<br>
          &bull; Submission Compliance Checklist
        </td>
        <td>
          &bull; Sourced raw 284,807 corpus from ULB/Kaggle repository.<br>
          &bull; Verified file checksums (SHA-256) and schema structure.<br>
          &bull; Documented 28 PCA feature descriptions and timestamp units.<br>
          &bull; Authored repository README, meeting logs, and progress trackers.<br>
          &bull; Compiled and formatted 17-slide master presentation deck.
        </td>
        <td>
          &bull; <code>README.md</code><br>
          &bull; <code>data/raw/creditcard.csv</code><br>
          &bull; <code>reports/*.pptx</code> formatting<br>
          &bull; Project Meeting Logs<br>
          &bull; Submission Documentation
        </td>
      </tr>
    </tbody>
  </table>

  <!-- =========================================================================
       PAGE 2: EMPIRICAL GROUND TRUTH & ML BENCHMARKS
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>3. Key Empirical Findings & Ground Truth Cheat Sheet</h2>
  <p>
    Extracted from the exhaustive audit of the 284,807 transaction corpus ($25,162,590.01 total volume across 48 continuous hours):
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Empirical Metric</th>
        <th style="width: 20%;" class="num">Ground Truth Value</th>
        <th style="width: 55%;">Analytical Finding & Operational Implication</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Total Transaction Volume</strong></td>
        <td class="num"><strong>284,807 txns</strong></td>
        <td>Audited 48-hour continuous digital payment stream with zero null records across 31 features.</td>
      </tr>
      <tr>
        <td><strong>Gross Transaction Value</strong></td>
        <td class="num"><strong>$25,162,590.01</strong></td>
        <td>Portfolio total value with an overall transaction mean of $88.35 and standard deviation of $250.12.</td>
      </tr>
      <tr>
        <td><strong>Confirmed Fraud Cases</strong></td>
        <td class="num"><strong>492 cases (0.173%)</strong></td>
        <td>Extreme rarity (1 fraud per 578 transactions) mandates Precision-Recall evaluation over ROC-AUC.</td>
      </tr>
      <tr>
        <td><strong>Direct Fraud Losses</strong></td>
        <td class="num"><strong>$60,127.97</strong></td>
        <td>Total financial exposure across 492 fraud events (average fraud ticket of $122.21).</td>
      </tr>
      <tr>
        <td><strong>Mean Ticket Comparison</strong></td>
        <td class="num"><strong>$122.21 vs $88.29</strong></td>
        <td>Fraud carries a +38.4% premium over legitimate transactions, driving substantial single-event losses.</td>
      </tr>
      <tr>
        <td><strong>Median Ticket Comparison</strong></td>
        <td class="num"><strong>$9.25 vs $22.00</strong></td>
        <td>Bi-modal fraud distribution: 27 micro card testing probes under $5 followed by high-ticket extractions.</td>
      </tr>
      <tr>
        <td><strong>2:00 AM Vulnerability Surge</strong></td>
        <td class="num" style="color: #ef4444; font-weight:700;">1.713% Fraud Rate</td>
        <td><strong>9.92x baseline risk!</strong> Nighttime legitimate traffic drops 85%, creating optimal bot attack timing.</td>
      </tr>
      <tr>
        <td><strong>Latent Signal Anchors</strong></td>
        <td class="num"><strong>V17, V14, V12, V11</strong></td>
        <td>Negative anchors (V17 at -0.33, V14 at -0.30, V12 at -0.26) and positive bursts (V11 at +0.15, V4 at +0.13).</td>
      </tr>
    </tbody>
  </table>

  <h2>4. Algorithmic Benchmarking & Economic Trade-Off Matrix</h2>
  <p>
    Evaluated on an independent, strictly stratified test holdout of <strong>56,962 transactions</strong> (containing 98 confirmed frauds):
  </p>

  <table>
    <thead>
      <tr>
        <th>Model Architecture</th>
        <th class="num">Accuracy</th>
        <th class="num">Precision</th>
        <th class="num">Catch Rate (Recall)</th>
        <th class="num">PR-AUC</th>
        <th class="num">False Alarms</th>
        <th class="num">Analyst Hours</th>
        <th class="num">Net Economic Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Logistic Regression</strong> (Baseline GLM)</td>
        <td class="num">97.37%</td>
        <td class="num">5.63%</td>
        <td class="num" style="color: #10b981; font-weight:700;">90.82% (89/98)</td>
        <td class="num">0.7225</td>
        <td class="num" style="color: #ef4444; font-weight:700;">1,492</td>
        <td class="num">373.0 hrs</td>
        <td class="num" style="color: #ef4444; font-weight:700;">-$19,991</td>
      </tr>
      <tr>
        <td><strong>Balanced Random Forest</strong> (Production Champion)</td>
        <td class="num">99.92%</td>
        <td class="num" style="color: #10b981; font-weight:700;">75.47%</td>
        <td class="num" style="color: #10b981; font-weight:700;">81.63% (80/98)</td>
        <td class="num" style="color: #10b981; font-weight:700;">0.8433</td>
        <td class="num" style="color: #10b981; font-weight:700;">26 (-98.3%)</td>
        <td class="num" style="color: #10b981; font-weight:700;">6.5 hrs</td>
        <td class="num" style="color: #10b981; font-weight:700;">+$47,782</td>
      </tr>
    </tbody>
  </table>

  <div class="callout alert">
    <strong>The False Alarm Economics Explained:</strong> While Logistic Regression caught 9 more frauds than Random Forest, it generated 1,466 additional false alarms. Reviewing those false alarms at $50/hour (15 minutes per case) consumes $18,325 in operational salary and creates severe cardholder friction. The Random Forest saves $73,300 in analyst overhead while recovering 81.63% of stolen funds, proving why it is the mathematically superior enterprise model.
  </div>

  <!-- =========================================================================
       PAGE 3: 17-SLIDE REVISED PRESENTATION SCRIPT (ACTS 1 & 2)
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>5. Complete 17-Slide Presentation Script (Word-for-Word)</h2>
  <p>
    This script corresponds directly to the official slide deck: <code>reports/transactional_fraud_detection_professional.pptx</code>.
  </p>

  <h3>ACT 1: Project Introduction, Context & Data Sourcing (Slides 1 to 4)</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #92400e;">SLIDE 1: Title & Presentation Introduction | Presenter: Anjali Krishna</span><br>
    "Good morning, esteemed seniors and evaluators. I am Anjali Krishna, and together with my colleagues Aditya Kumar and Yash Bhankale, we are presenting our internship capstone project: Transactional Fraud Detection Analysis. We have established an end-to-end framework combining rigorous data collection, SQL relational forensics, leak-free machine learning pipelines, and an executive Power BI risk intelligence system."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #92400e;">SLIDE 2: Section 01 | Business Problem & Industry Context | Presenter: Anjali Krishna</span><br>
    "In modern digital commerce, fraud represents a severe financial threat causing tens of billions in annual dispute losses. However, fraudulent events comprise less than 0.2% of the payment stream. If a financial institution sets detection rules too aggressively, innocent cardholders experience humiliating false declines, leading to abandoned carts and brand churn. Our project's objective was to build a system that detects illicit transactions with surgical precision while preserving frictionless customer experiences."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 3: Section 02 | 5 Core Technical Pillars & Architecture | Presenter: Aditya Kumar</span><br>
    "Thank you, Anjali. To solve this problem systematically, we architected our project across five technical pillars: data quality auditing, relational SQL feature querying, leak-free Scikit-Learn pipelines, supervised algorithm benchmarking, and an operational Power BI dashboard with dynamic risk tiering. Before diving into the deep analytical queries, Anjali will detail how our dataset was collected and cataloged."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #92400e;">SLIDE 4: Section 03 | Dataset Collection, Sourcing & Verification | Presenter: Anjali Krishna</span><br>
    "Thank you, Aditya. For our benchmark, I collected and ingested the comprehensive ULB Machine Learning Group credit card transaction corpus from Kaggle. The dataset contains 284,807 transactions recorded over 48 hours, representing $25.16 million in gross flow. Confirmed fraud accounts for exactly 492 cases&mdash;just 0.173% of volume. I verified the data integrity, cataloged the 28 PCA-transformed features (V1 through V28) which protect cardholder anonymity, and confirmed zero missing or null records. Now, Yash will walk you through our data cleaning and relational SQL database."
  </div>

  <h3>ACT 2: Data Quality, SQLite Relational Analytics & Forensics (Slides 5 to 7)</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #166534;">SLIDE 5: Section 04 | Data Cleaning & Relational SQLite Architecture | Presenter: Yash Bhankale</span><br>
    "Thank you, Anjali. During our data hygiene audit, we validated zero missing values across all 31 features. Crucially, we intentionally preserved 1,081 duplicate transactions because in financial cybercrime, automated bots fire rapid retry bursts that constitute legitimate attack signatures. We then built a dedicated SQLite relational database (<code>outputs/fraud_analysis.db</code>) via automated Python ETL to execute parameterized SQL analytics across monetary bands and temporal windows."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #166534;">SLIDE 6: Section 05 | Exploratory Forensics & The 2:00 AM Vulnerability Surge | Presenter: Yash Bhankale</span><br>
    "By deriving cyclical hourly features from the transaction timestamps, we uncovered our most critical operational finding: while legitimate customer volume drops by 85% between midnight and 5:00 AM, fraud activity continues unabated. At 2:00 AM, the fraud rate spikes to 1.713%&mdash;nearly ten times the baseline portfolio risk. Attackers deliberately exploit off-peak hours when cardholders are asleep and SMS transaction alerts go unnoticed."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #166534;">SLIDE 7: Exploratory Analysis | Monetary Profiling & Bi-Modal Bot Signatures | Presenter: Yash Bhankale</span><br>
    "Our monetary SQL queries revealed a clear bi-modal fraud distribution. We observed 27 micro card testing probes under $5, where automated bots test whether stolen card numbers are active, followed by high-ticket extractions over $500 that drive over 40% of all fraud losses. Now, Aditya will present our feature engineering, latent space mathematics, and predictive modeling."
  </div>

  <!-- =========================================================================
       PAGE 4: 17-SLIDE REVISED PRESENTATION SCRIPT (ACTS 3 & 4)
       ========================================================================= -->
  <div class="page-break"></div>

  <h3>ACT 3: Latent Feature Space, Machine Learning & False Alarm Breakthrough (Slides 8 to 15)</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDES 8&ndash;10: Latent Feature Space & Statistical Correlation Drivers | Presenter: Aditya Kumar</span><br>
    "Thank you, Yash. The 28 PCA-transformed components protect user privacy while preserving mathematical variance. On Slide 8, mapping V14 against V17 reveals distinct geometric separation: fraudulent transactions form isolated clusters away from legitimate transactions. On Slides 9 and 10, our correlation matrices demonstrate that V17, V14, and V12 serve as our strongest negative anchors, while V11 and V4 act as positive velocity burst indicators."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 11: Section 06 | Leak-Free Scikit-Learn Feature Pipelines | Presenter: Aditya Kumar</span><br>
    "To prevent data leakage, all transformations were encapsulated in Scikit-Learn pipelines fitted strictly on training data. We applied log-transformation (<code>Log_Amount</code>) to compress transaction skewness and mapped cyclical <code>Hour_of_Day</code> features using sine-cosine encoding to preserve continuous temporal cycles."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 12: Baseline Model Interpretation & Logistic Regression Odds Ratios | Presenter: Aditya Kumar</span><br>
    "On Slide 12, our baseline Logistic Regression model demonstrates clear directional coefficients: each unit decrease in V14 and V17 exponentially inflates the estimated log-odds of fraud."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDES 13&ndash;15: Section 07 | Model Benchmarks & The False Alarm Breakthrough | Presenter: Aditya Kumar</span><br>
    "We benchmarked our models on a 56,962-transaction holdout set containing 98 actual frauds. As shown on Slide 14, standard ROC-AUC gives a misleadingly high score of 0.97 for both models due to the huge majority class. Precision-Recall AUC reveals the true distinction: Balanced Random Forest achieves 0.8433 versus Logistic Regression's 0.7225.<br><br>
    Slide 15 illustrates our biggest breakthrough: Baseline Logistic Regression catches 90.8% of frauds (89/98), but triggers a massive 1,492 false alarms! Investigating those requires 373 analyst review hours, costing $18,650 and alienating customers. Our Production Champion, Balanced Random Forest, maintains an 81.63% catch rate while slashing false alarms by 98.3% down to just 26! This cuts review time to 6.5 hours and generates +$47,782 in net recovery."
  </div>

  <h3>ACT 4: Production Dashboard, Mitigation Architecture & Conclusion (Slides 16 to 17)</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 16: Section 08 | Power BI Risk Dashboard & 3-Tier Dynamic Policy | Presenter: Aditya Kumar</span><br>
    "We operationalized our Random Forest model into a Power BI Star-Schema dashboard backed by a 3-Tier Mitigation Engine:<br>
    &bull; <strong>Tier 1 (&lt; 30% risk):</strong> 98.45% of transactions pass frictionless with sub-50ms latency.<br>
    &bull; <strong>Tier 2 (30% to 70% risk):</strong> 1.25% trigger automated Step-Up MFA (OTP push). During the 2:00 AM vulnerability window Yash identified, this threshold automatically adjusts to $150.<br>
    &bull; <strong>Tier 3 (≥ 70% risk):</strong> 0.30% of traffic is immediately frozen with instant SMS alerts and 5-minute analyst queues."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #92400e;">SLIDE 17: Section 09 | Project Documentation Handover & Conclusion | Presenter: Anjali Krishna & Aditya Kumar</span><br>
    "<strong>Anjali:</strong> To ensure complete auditability, I have compiled our complete project documentation, including data dictionaries, meeting minutes, reproducible setup scripts, and compliance verification checklists in our repository.<br>
    <strong>Aditya:</strong> With 100% test suite pass rates and validated financial ROI, our system is production-ready. Thank you, and we welcome your questions."
  </div>

  <!-- =========================================================================
       PAGE 5: SENIOR Q&A DEFENSE MATRIX (ALL 3 MEMBERS)
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>6. Senior Q&A Defense Matrix (Tough Questions & Answers)</h2>
  <p>
    This matrix prepares every team member with concrete, data-backed answers tailored strictly to their assigned domain:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Senior Question</th>
        <th style="width: 15%;">Assigned Speaker</th>
        <th style="width: 60%;">Data-Backed Defense Answer</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>"Where did this dataset come from and how was data integrity verified?"</strong></td>
        <td><span class="badge badge-anjali">ANJALI</span></td>
        <td>
          "The dataset was collected from the ULB (Université Libre de Bruxelles) Machine Learning Group via Kaggle, containing 284,807 European credit card transactions across 48 continuous hours. I verified file integrity using SHA-256 checksums, validated that all 31 columns had complete entries, and documented the schema dictionary. Cardholder confidentiality is mathematically guaranteed through PCA transformation on features V1 through V28."
        </td>
      </tr>
      <tr>
        <td><strong>"How did the team ensure reproducibility and document tracking?"</strong></td>
        <td><span class="badge badge-anjali">ANJALI</span></td>
        <td>
          "I established a centralized project repository with standardized directory conventions (<code>data/</code>, <code>src/</code>, <code>models/</code>, <code>PowerBI/</code>, <code>reports/</code>). Every meeting, architectural decision, and schema change was logged in our project tracker and README. Furthermore, all dependencies were pinned in <code>requirements.txt</code> to guarantee that any developer can reproduce the entire pipeline with a single command."
        </td>
      </tr>
      <tr>
        <td><strong>"Why not block all transactions at 2:00 AM if fraud is 10x higher?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "While the fraud rate reaches 1.713% at 2:00 AM, 98.287% of transactions at that hour are completely legitimate (travelers, digital subscriptions, late-night workers). A blanket block would cause severe cardholder embarrassment, dispute escalations, and revenue loss. Instead, our SQL findings fed Aditya's Tier 2 policy: we selectively apply Step-Up MFA and lower verification thresholds for nighttime transactions above $150."
        </td>
      </tr>
      <tr>
        <td><strong>"Why keep 1,081 duplicate transactions instead of dropping them?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "In financial cybercrime, automated carding bots execute rapid retry bursts with identical card credentials and amounts to probe authorization endpoints. Dropping duplicates would delete genuine cyber attack signatures and distort real-world transaction velocity. Our SQL audit confirmed these duplicates represented authentic payment traffic, so we preserved them to ensure our models learn bot retry behaviors."
        </td>
      </tr>
      <tr>
        <td><strong>"Why build an SQLite database instead of querying pandas dataframes in memory?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "In enterprise banking environments, regulatory compliance mandates that all transaction filtering and forensics be executed via audited, reproducible SQL queries rather than ephemeral script memory. Building <code>fraud_analysis.db</code> indexed on Time, Amount, and Class allows persistent query auditability, seamless integration with BI tools, and mirrors real-world data lakehouse architectures."
        </td>
      </tr>
      <tr>
        <td><strong>"Why choose Random Forest over Logistic Regression when Logistic Regression had a higher Recall (90.8% vs 81.6%)?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "Looking only at Recall is a classic financial trap. Logistic Regression caught 89 of 98 test frauds, but produced 1,492 false alarms. Investigating 1,492 false alerts requires 373 analyst hours ($18,650 in labor cost) and insults 1,492 loyal customers. Random Forest caught 80 frauds with only 26 false alarms&mdash;a 98.3% reduction. It saves $73,300 in review overhead, yielding a net economic gain of +$47,782 versus Logistic Regression's -$19,991 deficit."
        </td>
      </tr>
      <tr>
        <td><strong>"Why not use SMOTE or synthetic oversampling on the minority class?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "SMOTE synthesizes artificial data points by interpolating between nearest neighbors. In rare-event fraud (0.173%), synthetic points frequently cross non-linear decision boundaries into legitimate transaction space, severely distorting predicted probability calibrations and artificially inflating false positives. Instead, we used class-weighted balanced cost matrices and threshold tuning directly on the empirical distribution."
        </td>
      </tr>
      <tr>
        <td><strong>"Why build an Excel Star-Schema and web app instead of just sharing a notebook?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "Executive stakeholders and fraud operations analysts do not run Jupyter notebooks. A Star-Schema data model with 1 Fact and 5 Dimensions in Power BI enables non-technical leadership to slice fraud by hour, amount band, and risk tier in real time. We also built a standalone web dashboard so any executive can inspect real-time risk simulations in any browser without needing Python installed."
        </td>
      </tr>
    </tbody>
  </table>

  <!-- =========================================================================
       PAGE 6: DELIVERABLES CATALOG & REPOSITORY INVENTORY
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>7. Complete Project Directory & Artifact Deliverables Inventory</h2>
  <p>
    The complete repository has been structured into modular production assets:
  </p>

  <table>
    <thead>
      <tr>
        <th>Asset Category</th>
        <th>File Path</th>
        <th>Description & Primary Technical Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Team Project Guide (Revised)</strong></td>
        <td><code>reports/Transactional_Fraud_Detection_Team_Guide_Revised.pdf</code></td>
        <td>This comprehensive PDF guide detailing the revised role distribution, script, and Q&A.</td>
      </tr>
      <tr>
        <td><strong>Role Reallocation Summary</strong></td>
        <td><code>reports/Team_Role_Reallocation_and_Project_Guide.md</code></td>
        <td>Markdown change documentation detailing task reallocation for team sharing.</td>
      </tr>
      <tr>
        <td><strong>Main Presentation Deck</strong></td>
        <td><code>reports/transactional_fraud_detection_professional.pptx</code></td>
        <td>Master 17-slide corporate PowerPoint deck formatted for executive evaluation.</td>
      </tr>
      <tr>
        <td><strong>Presentation Deck PDF</strong></td>
        <td><code>reports/transactional_fraud_detection_professional.pdf</code></td>
        <td>High-resolution PDF export of the 17-slide master presentation deck.</td>
      </tr>
      <tr>
        <td><strong>Power BI Star-Schema Model</strong></td>
        <td><code>PowerBI/data/Fraud_Detection_PowerBI_DataModel.xlsx</code></td>
        <td>Curated 1 Fact + 5 Dim Star-Schema workbook for seamless Power BI Desktop import.</td>
      </tr>
      <tr>
        <td><strong>Enterprise DAX Library</strong></td>
        <td><code>PowerBI/DAX_Measures_Library.dax</code></td>
        <td>35+ fully tested DAX measures for financial volume, loss, and risk KPIs.</td>
      </tr>
      <tr>
        <td><strong>Interactive Web App</strong></td>
        <td><code>PowerBI/dashboard/index.html</code></td>
        <td>Zero-dependency executive dashboard with live slicers, risk sliders, and full-screen presenter mode.</td>
      </tr>
      <tr>
        <td><strong>SQLite Database</strong></td>
        <td><code>outputs/fraud_analysis.db</code></td>
        <td>Relational SQLite database storing audited transactions and forensic tables.</td>
      </tr>
      <tr>
        <td><strong>Trained Production Model</strong></td>
        <td><code>models/fraud_detection_model.joblib</code></td>
        <td>Serialized Random Forest champion pipeline and baseline classification models.</td>
      </tr>
      <tr>
        <td><strong>Automated Test Suite</strong></td>
        <td><code>tests/test_pipeline.py</code></td>
        <td>10 automated Pytest verification suites ensuring 100% pipeline integrity.</td>
      </tr>
    </tbody>
  </table>

</body>
</html>
"""

# Write HTML file
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content.strip())
print(f"Revised HTML guide generated at: {html_path}")

# Execute Microsoft Edge headless to generate PDF
print("Executing Microsoft Edge headless print-to-pdf...")
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_exe,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    str(html_path)
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and pdf_path.exists():
    print(f"Revised PDF successfully generated at: {pdf_path} (Size: {pdf_path.stat().st_size:,} bytes)")
    # Also save a copy to PowerBI/ directory
    with open(pdf_path, "rb") as src, open(pdf_copy_path, "wb") as dst:
        dst.write(src.read())
    print(f"Revised PDF copy saved at: {pdf_copy_path}")
else:
    print(f"Error during Edge headless export: {res.stderr}")

# Also generate a companion Markdown document
md_content = """# Transactional Fraud Detection Analysis - Team Role Reallocation & Project Guide

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
"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content.strip())
with open(md_copy_path, "w", encoding="utf-8") as f:
    f.write(md_content.strip())
print(f"Markdown guides saved at {md_path} and {md_copy_path}")
