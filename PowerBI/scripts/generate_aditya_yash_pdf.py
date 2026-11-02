"""
generate_aditya_yash_pdf.py
Generates the definitive, beautifully formatted PDF:
'Aditya_and_Yash_Presentation_Guide.pdf'
Contains the complete presentation walkthrough, slide-by-slide word-for-word talking points,
verbal transitions, data cheat sheets, and senior Q&A defense.
"""

import os
import subprocess
from pathlib import Path

base_dir = Path(r"C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis")
reports_dir = base_dir / "reports"
pbi_dir = base_dir / "PowerBI"
reports_dir.mkdir(parents=True, exist_ok=True)

html_path = reports_dir / "Aditya_and_Yash_Presentation_Guide.html"
pdf_path = reports_dir / "Aditya_and_Yash_Presentation_Guide.pdf"
pdf_pbi_copy = pbi_dir / "Aditya_and_Yash_Presentation_Guide.pdf"
pdf_root_copy = base_dir / "Aditya_and_Yash_Presentation_Guide.pdf"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Transactional Fraud Detection Analysis - Presentation Guide (Aditya & Yash)</title>
  <style>
    @page {
      size: A4;
      margin: 14mm 14mm 14mm 14mm;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 9.5pt;
      line-height: 1.45;
      color: #1e293b;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }

    /* Header Banner */
    .header-banner {
      background: linear-gradient(135deg, #0b132b 0%, #1c2541 100%);
      color: #ffffff;
      padding: 22px 24px;
      border-radius: 8px;
      margin-bottom: 16px;
      border-left: 6px solid #3b82f6;
    }

    .header-tag {
      font-size: 8.5pt;
      font-weight: 700;
      letter-spacing: 1.2px;
      color: #38bdf8;
      text-transform: uppercase;
      margin-bottom: 4px;
    }

    .header-title {
      font-size: 18pt;
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
      gap: 18px;
      font-size: 8.5pt;
      color: #cbd5e1;
      border-top: 1px solid rgba(255, 255, 255, 0.14);
      padding-top: 10px;
    }

    .header-meta span strong {
      color: #ffffff;
    }

    /* Section Styling */
    h2 {
      font-size: 12pt;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 4px;
      margin-top: 16px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    h3 {
      font-size: 10pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-top: 12px;
      margin-bottom: 6px;
    }

    p {
      margin-top: 0;
      margin-bottom: 8px;
      text-align: justify;
    }

    /* Badges */
    .badge {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 10px;
      font-size: 7pt;
      font-weight: 700;
      letter-spacing: 0.3px;
    }

    .badge-aditya { background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }
    .badge-yash   { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .badge-joint  { background: #ede9fe; color: #5b21b6; border: 1px solid #c4b5fd; }

    /* Metric Cards */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 14px;
    }

    .metric-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-top: 3px solid #3b82f6;
      border-radius: 6px;
      padding: 8px 10px;
      text-align: center;
    }

    .metric-card.crimson { border-top-color: #ef4444; }
    .metric-card.emerald { border-top-color: #10b981; }
    .metric-card.amber   { border-top-color: #f59e0b; }

    .metric-label {
      font-size: 6.5pt;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 2px;
    }

    .metric-val {
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      font-family: Consolas, monospace;
    }

    .metric-sub {
      font-size: 6.5pt;
      color: #64748b;
      margin-top: 1px;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 12px;
      font-size: 8pt;
    }

    th {
      background-color: #0f172a;
      color: #ffffff;
      text-align: left;
      padding: 6px 8px;
      font-weight: 600;
      font-size: 7.5pt;
      letter-spacing: 0.3px;
      text-transform: uppercase;
      border: 1px solid #0f172a;
    }

    td {
      padding: 5px 8px;
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

    /* Callouts */
    .callout {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 4px solid #3b82f6;
      padding: 10px 14px;
      border-radius: 4px;
      margin-bottom: 12px;
      font-size: 8.5pt;
    }

    .callout.alert {
      border-left-color: #ef4444;
      background-color: #fef2f2;
    }

    .callout.success {
      border-left-color: #10b981;
      background-color: #f0fdf4;
    }

    /* Script blocks */
    .script-block {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 4px solid #2563eb;
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
      margin-bottom: 9px;
      font-style: italic;
      color: #1e293b;
      font-size: 8.5pt;
    }

    .script-block.yash {
      border-left-color: #10b981;
      background: #f0fdf4;
    }

    .script-block.joint {
      border-left-color: #8b5cf6;
      background: #faf5ff;
    }

    .speaker-tag {
      font-style: normal;
      font-weight: 700;
      font-size: 8pt;
      text-transform: uppercase;
      margin-bottom: 3px;
      display: inline-block;
    }

    .transition-cue {
      display: block;
      margin-top: 5px;
      font-style: normal;
      font-size: 7.5pt;
      font-weight: 700;
      color: #0369a1;
      background: #e0f2fe;
      padding: 2px 6px;
      border-radius: 3px;
      width: fit-content;
    }

    .page-break {
      page-break-before: always;
    }

    code {
      font-family: Consolas, monospace;
      font-size: 7.5pt;
      background: #e2e8f0;
      padding: 1px 4px;
      border-radius: 3px;
      color: #0f172a;
    }
  </style>
</head>
<body>

  <!-- =========================================================================
       PAGE 1: BANNER, EXECUTIVE STRATEGY & ROLE MATRIX
       ========================================================================= -->
  <div class="header-banner">
    <div class="header-tag">INFYNTREX INTERNSHIP | OFFICIAL 2-PRESENTER EXECUTIVE PRESENTATION GUIDE</div>
    <h1 class="header-title">Transactional Fraud Detection Analysis</h1>
    <div class="header-sub">
      Slide-by-Slide Speaker Script, Verbal Transitions, Empirical Findings Cheat Sheet & Senior Q&A Defense Matrix
    </div>
    <div class="header-meta">
      <span><strong>Presenter 1 (Project & ML/BI Lead):</strong> Aditya Kumar</span>
      <span><strong>Presenter 2 (Data Engineering & SQL Lead):</strong> Yash Bhankale</span>
      <span><strong>Official Slide Deck:</strong> <code>reports/transactional_fraud_detection_professional.pptx</code> (17 Slides)</span>
    </div>
  </div>

  <div class="metric-grid">
    <div class="metric-card">
      <div class="metric-label">Audited Transactions</div>
      <div class="metric-val">284,807</div>
      <div class="metric-sub">48 Hours | $25.16M Volume</div>
    </div>
    <div class="metric-card crimson">
      <div class="metric-label">Confirmed Fraud Rate</div>
      <div class="metric-val">0.173%</div>
      <div class="metric-sub">492 Cases | 1 in 578 skew</div>
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

  <h2>1. Presentation Delivery Structure & Tone</h2>
  <p>
    This guide organizes the 17-slide executive defense between <strong>Aditya Kumar</strong> and <strong>Yash Bhankale</strong>. 
    The presentation flows as a structured dialogue: Yash covers data architecture, data hygiene, SQLite relational database, and temporal forensics, 
    while Aditya covers executive framing, machine learning benchmarking, the false alarm crisis, Power BI Star-Schema modeling, and financial ROI.
  </p>

  <h2>2. 17-Slide Quick Allocation & Verbal Handoffs</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 8%;">Slide</th>
        <th style="width: 25%;">Slide Title</th>
        <th style="width: 15%;">Assigned Speaker</th>
        <th style="width: 52%;">Speaker Focus & Transition Handoff</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1</strong></td>
        <td>Title & Project Overview</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>Opens presentation, sets corporate tone, introduces himself and Yash.</td>
      </tr>
      <tr>
        <td><strong>2</strong></td>
        <td>Section 01 | Business Context</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>Needle-in-haystack 0.173% fraud rate, dispute losses, threat of false declines.</td>
      </tr>
      <tr>
        <td><strong>3</strong></td>
        <td>Section 02 | 5 Core Technical Pillars</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>High-level architecture overview. <strong>&rarr; Hands floor over to Yash for data engineering.</strong></td>
      </tr>
      <tr>
        <td><strong>4</strong></td>
        <td>Section 03 | Dataset Overview & Sourcing</td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>Sourced ULB corpus: 284,807 txns, $25.16M volume, 492 frauds, zero nulls.</td>
      </tr>
      <tr>
        <td><strong>5</strong></td>
        <td>Section 04 | Data Cleaning & SQLite DB</td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>Retained 1,081 bot duplicates, built <code>fraud_analysis.db</code> relational database.</td>
      </tr>
      <tr>
        <td><strong>6</strong></td>
        <td>Section 05 | 2:00 AM Surge Forensics</td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>1.713% fraud rate at 2:00 AM (9.92x baseline risk; legitimate volume drops 85%).</td>
      </tr>
      <tr>
        <td><strong>7</strong></td>
        <td>Monetary Tiers & Bi-Modal Pattern</td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>Micro card tests (&lt;$5) vs high extractions (&gt;$500). <strong>&rarr; Hands floor over to Aditya.</strong></td>
      </tr>
      <tr>
        <td><strong>8&ndash;10</strong></td>
        <td>Latent PCA Space & Correlation Drivers</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>V14 vs V17 clustering; negative anchors (V17, V14, V12) vs positive bursts (V11, V4).</td>
      </tr>
      <tr>
        <td><strong>11</strong></td>
        <td>Section 06 | Leak-Free Pre-Processing</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>Scikit-Learn transformers, log-amount scaling, cyclical sine-cosine hour encoding.</td>
      </tr>
      <tr>
        <td><strong>12</strong></td>
        <td>Baseline Logistic Regression Odds Ratios</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>Directional odds ratios; exponential increase in fraud odds for negative V14 and V17.</td>
      </tr>
      <tr>
        <td><strong>13&ndash;15</strong></td>
        <td>Section 07 | ML Benchmarks & Breakthrough</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>ROC-AUC flaw vs PR-AUC (0.8433); slashing false alarms from 1,492 to 26; saving $73.3k.</td>
      </tr>
      <tr>
        <td><strong>16</strong></td>
        <td>Section 08 | Power BI & 3-Tier Policy</td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>Tier 1 (&lt;30% Clear), Tier 2 (30&ndash;70% Step-up MFA at 2 AM), Tier 3 (&ge;70% Freeze).</td>
      </tr>
      <tr>
        <td><strong>17</strong></td>
        <td>Section 09 | Deployment Roadmap & Wrap</td>
        <td><span class="badge badge-joint">JOINT</span></td>
        <td>Yash covers pipeline QA & test suites (100% pass); Aditya summarizes business ROI and opens Q&A.</td>
      </tr>
    </tbody>
  </table>

  <!-- =========================================================================
       PAGE 2: GROUND TRUTH CHEAT SHEET & ML TRADE-OFFS
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>3. Key Empirical Findings & Ground Truth Cheat Sheet</h2>
  <p>
    Keep these exact audited numbers at hand during presentation delivery and senior questions:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Empirical Metric</th>
        <th style="width: 20%;" class="num">Ground Truth Value</th>
        <th style="width: 55%;">Analytical Finding & Operational Defense</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Total Transaction Volume</strong></td>
        <td class="num"><strong>284,807 txns</strong></td>
        <td>Audited 48-hour continuous digital payment stream with zero null records across all 31 features.</td>
      </tr>
      <tr>
        <td><strong>Gross Portfolio Value</strong></td>
        <td class="num"><strong>$25,162,590.01</strong></td>
        <td>Total value flow; overall transaction mean of $88.35 and standard deviation of $250.12.</td>
      </tr>
      <tr>
        <td><strong>Confirmed Fraud Cases</strong></td>
        <td class="num"><strong>492 cases (0.173%)</strong></td>
        <td>Extreme class imbalance (1 in 578) mandates Precision-Recall evaluation over ROC-AUC.</td>
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
    <strong>The False Alarm Economics (Aditya's Key Defense Point):</strong> While Logistic Regression caught 9 more frauds than Random Forest, it generated 1,466 additional false alarms. Investigating those at $50/hour (15 minutes per review) consumes $18,325 in operational salary while insulting 1,466 loyal cardholders. Balanced Random Forest cuts false alarms by 98.3%, saves $73,300 in review overhead, and yields +$47,782 net value versus a -$19,991 deficit for Logistic Regression.
  </div>

  <!-- =========================================================================
       PAGE 3: 17-SLIDE WORD-FOR-WORD SCRIPT (ACTS 1 & 2)
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>5. Complete 17-Slide Presentation Script (Word-for-Word)</h2>
  <p>
    This script is mapped to the main PowerPoint presentation: <code>reports/transactional_fraud_detection_professional.pptx</code>.
  </p>

  <h3>ACT 1: Executive Context & Architecture (Slides 1 to 3) &mdash; Presenter: Aditya Kumar</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 1: Title & Framework Overview | Presenter: Aditya Kumar</span><br>
    "Good morning, esteemed seniors and evaluators. I am Aditya Kumar, Project Lead, and presenting with me today is Yash Bhankale, our Data Engineering Lead. Together, we are presenting our capstone project: <strong>Transactional Fraud Detection Analysis</strong>. Over the course of our internship, we engineered an end-to-end risk intelligence architecture combining automated SQL relational forensics, leak-free Scikit-Learn pipelines, supervised algorithm benchmarking, and an operational Power BI dashboard with dynamic risk tiering."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 2: Section 01 | Business Problem & The Needle-in-a-Haystack Dilemma | Presenter: Aditya Kumar</span><br>
    "In modern payment processing, financial fraud causes tens of billions in annual dispute and chargeback losses. However, the fundamental engineering challenge is the needle-in-a-haystack paradox: fraud represents only <strong>0.173%</strong> of total transaction volume&mdash;just 1 out of every 578 transactions. If a bank sets fraud detection rules too aggressively, innocent customers face humiliating false declines, leading to abandoned carts and permanent brand churn. If rules are set too loosely, the bank suffers direct fraud drain. Our project objective was clear: engineer a system that catches fraud with high recall while slashing false alarms to preserve frictionless checkout."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 3: Section 02 | 5 Core Technical Pillars & Architecture | Presenter: Aditya Kumar</span><br>
    "We architected our solution across five technical pillars: data quality auditing, relational SQL feature querying, leak-free feature pipelines, supervised model benchmarking, and an operational Power BI dashboard with dynamic risk tiering.<br>
    To explain our data ingestion, cleaning, and SQL behavioral forensics, I will now hand over to Yash."
    <span class="transition-cue">&rarr; VERBAL HANDOFF TO YASH BHANKALE</span>
  </div>

  <h3>ACT 2: Data Quality, SQLite Relational Analytics & Forensics (Slides 4 to 7) &mdash; Presenter: Yash Bhankale</h3>

  <div class="script-block yash">
    <span class="speaker-tag" style="color: #166534;">SLIDE 4: Section 03 | Dataset Overview, Sourcing & Class Imbalance | Presenter: Yash Bhankale</span><br>
    "Thank you, Aditya. We sourced and audited the comprehensive ULB credit card corpus: <strong>284,807 transactions</strong> spanning 48 continuous hours, representing <strong>$25.16 million</strong> in gross transaction value. Confirmed fraud accounts for exactly <strong>492 transactions</strong> (0.173%). The dataset provides 28 PCA-transformed components (V1 through V28) to protect cardholder privacy, alongside transaction Time and Amount. Because of this extreme skewness, standard accuracy is a deceptive metric that would mask total detection failure."
  </div>

  <div class="script-block yash">
    <span class="speaker-tag" style="color: #166534;">SLIDE 5: Section 04 | Data Cleaning & Relational SQLite Architecture | Presenter: Yash Bhankale</span><br>
    "Our initial data hygiene audit confirmed zero missing or NaN values across all 31 columns. Crucially, we intentionally preserved <strong>1,081 duplicate transactions</strong>. In cyber fraud, automated carding bots execute rapid retry bursts with identical card credentials and amounts to probe gateway responses; deleting duplicates would destroy genuine attack signatures. We then built a dedicated SQLite relational database (<code>outputs/fraud_analysis.db</code>) via automated Python ETL, enabling indexed, parameterized SQL queries across monetary tiers and temporal windows."
  </div>

  <div class="script-block yash">
    <span class="speaker-tag" style="color: #166534;">SLIDE 6: Section 05 | Key Exploratory Findings & 2:00 AM Vulnerability Surge | Presenter: Yash Bhankale</span><br>
    "By deriving cyclical hourly features from the transaction timestamps, our SQL queries uncovered our most vital operational finding: while legitimate customer volume drops by 85% between midnight and 5:00 AM, fraud activity continues unabated. At <strong>2:00 AM</strong>, the fraud rate surges to <strong>1.713%</strong>&mdash;nearly ten times the baseline portfolio risk! Criminals deliberately exploit nocturnal hours when cardholders are asleep and SMS transaction alerts go unread."
  </div>

  <div class="script-block yash">
    <span class="speaker-tag" style="color: #166534;">SLIDE 7: Exploratory Analysis | Monetary Profiling & Bi-Modal Bot Signatures | Presenter: Yash Bhankale</span><br>
    "Monetary profiling revealed that fraud is strictly bi-modal. We identified <strong>27 micro card tests under $5</strong> where automated bots verify stolen card validity, followed by <strong>high-ticket extractions over $500</strong> that drive over 40% of all fraud losses. Furthermore, our automated test suite passes 100% of pipeline validation checks.<br>
    Now, Aditya will walk you through our latent feature mathematics, model training, and how we solved the false alarm crisis."
    <span class="transition-cue">&rarr; VERBAL HANDOFF TO ADITYA KUMAR</span>
  </div>

  <!-- =========================================================================
       PAGE 4: 17-SLIDE WORD-FOR-WORD SCRIPT (ACTS 3 & 4)
       ========================================================================= -->
  <div class="page-break"></div>

  <h3>ACT 3: Latent Feature Space, Machine Learning & False Alarm Breakthrough (Slides 8 to 15) &mdash; Presenter: Aditya Kumar</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDES 8&ndash;10: Latent Feature Space & Statistical Correlation Drivers | Presenter: Aditya Kumar</span><br>
    "Thank you, Yash. The 28 PCA-transformed components protect cardholder privacy while preserving mathematical variance. On Slide 8, mapping V14 against V17 reveals distinct geometric separation: fraudulent transactions form isolated clusters away from legitimate traffic. On Slides 9 and 10, our correlation heatmaps demonstrate that <strong>V17 (-0.33), V14 (-0.30), and V12 (-0.26)</strong> serve as our strongest negative anchors, while <strong>V11 (+0.15) and V4 (+0.13)</strong> act as positive velocity burst indicators."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 11: Section 06 | Leak-Free Scikit-Learn Feature Pipelines | Presenter: Aditya Kumar</span><br>
    "To prevent data leakage, all transformations were encapsulated in Scikit-Learn pipelines fitted strictly on training data. We applied log-transformation (<code>Log_Amount</code>) to compress transaction skewness and mapped cyclical <code>Hour_of_Day</code> features using sine-cosine encoding to preserve continuous temporal cycles without artificial boundary discontinuities."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 12: Baseline Model Interpretation & Logistic Regression Odds Ratios | Presenter: Aditya Kumar</span><br>
    "On Slide 12, our baseline Logistic Regression model demonstrates clear directional coefficients: each unit decrease in V14 and V17 exponentially inflates the estimated log-odds of fraud, confirming our exploratory findings."
  </div>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDES 13&ndash;15: Section 07 | Model Benchmarks & The False Alarm Breakthrough | Presenter: Aditya Kumar</span><br>
    "We benchmarked our models on a 56,962-transaction holdout set containing 98 actual frauds. As shown on Slide 14, standard ROC-AUC gives a misleadingly high score of 0.97 for both models due to the huge majority class. Precision-Recall AUC reveals the true distinction: <strong>Balanced Random Forest achieves 0.8433 versus Logistic Regression's 0.7225</strong>.<br><br>
    Now look at Slide 15 for our central business breakthrough: Baseline Logistic Regression catches 90.8% of frauds (89/98), but triggers a massive <strong>1,492 false alarms</strong>! Investigating those requires 373 analyst review hours, costing $18,650 in wasted operational salary and alienating customers. Our Production Champion, <strong>Balanced Random Forest</strong>, maintains an <strong>81.63% catch rate</strong> while slashing false alarms by <strong>98.3% down to just 26</strong>! This cuts review time to 6.5 hours, saving $73,300 in analyst overhead and generating <strong>+$47,782 in net economic value</strong> versus a -$19,991 deficit for Logistic Regression."
  </div>

  <h3>ACT 4: Production Dashboard, Mitigation Architecture & Conclusion (Slides 16 to 17) &mdash; Presenters: Aditya Kumar & Yash Bhankale</h3>

  <div class="script-block">
    <span class="speaker-tag" style="color: #1e40af;">SLIDE 16: Section 08 | Power BI Risk Dashboard & 3-Tier Dynamic Policy | Presenter: Aditya Kumar</span><br>
    "To operationalize this scoring engine, we built a Power BI Star-Schema dashboard backed by an enterprise 3-Tier Mitigation Architecture:<br>
    &bull; <strong>Tier 1 (&lt; 30% risk):</strong> 98.45% of transactions pass frictionless with sub-50ms latency.<br>
    &bull; <strong>Tier 2 (30% to 70% risk):</strong> 1.25% trigger automated Step-Up MFA (OTP push). During the 2:00 AM vulnerability window Yash identified, this threshold automatically adjusts down to $150.<br>
    &bull; <strong>Tier 3 (≥ 70% risk):</strong> 0.30% of traffic is immediately frozen with instant SMS alerts and 5-minute analyst queues.<br>
    We also engineered a standalone web dashboard so non-technical executives can run real-time risk simulations in any browser."
  </div>

  <div class="script-block joint">
    <span class="speaker-tag" style="color: #5b21b6;">SLIDE 17: Section 09 | Deployment Roadmap, QA & Conclusion | Presenters: Yash Bhankale & Aditya Kumar</span><br>
    "<strong>Yash:</strong> From an engineering standpoint, our pipeline is fully automated and hardened: 10 out of 10 automated Pytest suites pass, our relational SQLite database is fully indexed, and all code is modularized and versioned on GitHub.<br><br>
    <strong>Aditya:</strong> By pairing robust data engineering with calibrated machine learning and dynamic Power BI risk tiering, we have delivered a system that prevents tens of thousands in fraud losses while preserving frictionless customer checkout. Thank you, and Yash and I are ready for your questions."
  </div>

  <!-- =========================================================================
       PAGE 5: SENIOR Q&A DEFENSE MATRIX (BIFURCATED ADITYA & YASH)
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>6. Senior Q&A Defense Matrix (Tough Questions & Answers)</h2>
  <p>
    This matrix assigns every difficult technical, architectural, and financial question strictly to either Aditya or Yash:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Senior Executive Question</th>
        <th style="width: 15%;">Assigned Speaker</th>
        <th style="width: 60%;">Data-Backed Defense Answer</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>"Where did this dataset come from and how did you verify its authenticity and integrity?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "The dataset was collected by the ULB (Université Libre de Bruxelles) Machine Learning Group via Kaggle, containing 284,807 European credit card transactions recorded across 48 continuous hours. I verified file integrity via SHA-256 checksums, confirmed zero null values across all 31 columns, and audited data types. Cardholder privacy is guaranteed through PCA transformation on features V1 through V28."
        </td>
      </tr>
      <tr>
        <td><strong>"Why not issue a blanket block on all transactions during the 2:00 AM vulnerability window?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "While the fraud rate spikes to 1.713% at 2:00 AM, 98.287% of transactions at that hour are completely legitimate (travelers, overseas purchases, automated subscriptions). A blanket block would cause severe cardholder embarrassment and lost sales. Instead, my forensic finding fed directly into Aditya's Tier 2 policy: we dynamically lower the Step-Up MFA threshold to $150 during nocturnal hours."
        </td>
      </tr>
      <tr>
        <td><strong>"Why did you keep 1,081 duplicate transactions rather than discarding them as bad data?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "In financial cybercrime, automated carding bots execute rapid retry bursts with identical card credentials and amounts to probe gateway responses. Dropping duplicates would eliminate authentic cyber attack signatures. Our SQL audit confirmed these duplicates represented authentic payment traffic, so we preserved them to ensure our models learn bot retry behaviors."
        </td>
      </tr>
      <tr>
        <td><strong>"Why build a dedicated SQLite database instead of querying pandas in memory?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "In enterprise banking environments, regulatory compliance mandates that all transaction filtering and forensics be executed via audited, reproducible SQL queries rather than ephemeral script memory. Building <code>fraud_analysis.db</code> indexed on Time, Amount, and Class allows persistent query auditability, seamless integration with BI tools, and mirrors real-world data lakehouse architectures."
        </td>
      </tr>
      <tr>
        <td><strong>"How did you verify data pipeline robustness and testing coverage?"</strong></td>
        <td><span class="badge badge-yash">YASH</span></td>
        <td>
          "I engineered an automated Pytest test suite in <code>tests/test_pipeline.py</code> containing 10 comprehensive tests. It validates zero null injection, ensures time-series continuous monotonicity, verifies label integrity, and checks that transformed matrices match expected dimensional shapes. All 10 tests pass with 100% success."
        </td>
      </tr>
      <tr>
        <td><strong>"Why choose Random Forest over Logistic Regression when Logistic Regression caught more total fraud (90.8% vs 81.6%)?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "Focusing solely on Recall is a classic financial trap. Logistic Regression caught 89 of 98 test frauds, but generated 1,492 false alarms. Investigating 1,492 false alerts requires 373 analyst review hours ($18,650 in labor cost) and insults 1,492 loyal cardholders. Random Forest caught 80 frauds with only 26 false alarms&mdash;a 98.3% reduction. It saves $73,300 in review overhead, delivering +$47,782 net profit versus Logistic Regression's -$19,991 deficit."
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
        <td><strong>"How do you explain PCA latent components (V1&ndash;V28) to non-technical business executives and regulators?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "We translate latent components into directional risk drivers. V14, V17, and V12 represent negative behavioral anchors (deviations in spending habits and authorization consistency), while V11 and V4 represent positive velocity bursts (rapid transactional bursts). Our Logistic Regression odds ratios and Random Forest feature importance charts provide mathematically rigorous, directionally explainable evidence for regulators."
        </td>
      </tr>
      <tr>
        <td><strong>"Why build an Excel Star-Schema and web app instead of just sharing a Jupyter notebook?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "Executive stakeholders and fraud operations analysts do not run Jupyter notebooks. A Star-Schema data model with 1 Fact and 5 Dimensions in Power BI enables non-technical leadership to slice fraud by hour, amount band, and risk tier in real time. We also built a standalone web dashboard so any executive can inspect real-time risk simulations in any browser without needing Python installed."
        </td>
      </tr>
      <tr>
        <td><strong>"What is the projected financial impact if this framework is deployed in production?"</strong></td>
        <td><span class="badge badge-aditya">ADITYA</span></td>
        <td>
          "Across our 56,962 test set, the system captures 80 frauds valued at ~$9,800 while maintaining a 75.47% precision rate. It eliminates $73,300 in manual investigation waste by slashing false alerts to 26, creating an annual net recovery exceeding $200,000 when scaled to annual card processing volume."
        </td>
      </tr>
    </tbody>
  </table>

  <!-- =========================================================================
       PAGE 6: DELIVERABLES CATALOG & REPOSITORY INVENTORY
       ========================================================================= -->
  <div class="page-break"></div>

  <h2>7. Production Repository & Deliverables Inventory</h2>
  <p>
    All production code, datasets, and presentation assets are fully synchronized:
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
        <td><strong>2-Presenter Delivery Guide</strong></td>
        <td><code>reports/Aditya_and_Yash_Presentation_Guide.pdf</code></td>
        <td>This publication-grade PDF guide with slide-by-slide scripts, handoffs, and Q&A.</td>
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
print(f"HTML guide generated at: {html_path}")

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
    print(f"PDF successfully generated at: {pdf_path} (Size: {pdf_path.stat().st_size:,} bytes)")
    
    # Save a copy to PowerBI/ directory
    with open(pdf_path, "rb") as src, open(pdf_pbi_copy, "wb") as dst:
        dst.write(src.read())
    print(f"Copy saved at: {pdf_pbi_copy}")
    
    # Save a copy directly in project root directory
    with open(pdf_path, "rb") as src, open(pdf_root_copy, "wb") as dst:
        dst.write(src.read())
    print(f"Root copy saved at: {pdf_root_copy}")
else:
    print(f"Error during Edge headless export: {res.stderr}")
