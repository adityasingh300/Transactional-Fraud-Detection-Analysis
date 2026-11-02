# Transactional Fraud Detection Analysis — 2-Presenter Delivery & Senior Defense Guide
**Presenters:** Aditya Kumar (Project Lead & ML/BI Architect) & Yash Bhankale (Data Engineering & SQL Forensic Lead)  
**Main Slide Deck:** `reports/transactional_fraud_detection_professional.pptx` (17 Slides)  
**Main Slide Deck PDF:** `reports/transactional_fraud_detection_professional.pdf`  
**2-Presenter Master PDF Guide:** `reports/Transactional_Fraud_Detection_Presenter_Guide_2Presenters.pdf`

---

## 1. Quick Slide Allocation Summary

| Slide | Topic | Presenter | Hand-Off / Transition Cue |
| :---: | :--- | :---: | :--- |
| **1** | Title & Presentation Overview | **Aditya Kumar** | Opens presentation, sets the executive tone, introduces himself and Yash. |
| **2** | Business Context & Dilemma | **Aditya Kumar** | 0.173% needle-in-a-haystack, dispute losses, false decline threat. |
| **3** | 5 Core Technical Pillars | **Aditya Kumar** | High-level 5 pillars &rarr; **Passes floor to Yash** for data engineering. |
| **4** | Dataset Overview & Collection Scope | **Yash Bhankale** | Sourcing ULB corpus: 284,807 txns, $25.16M gross volume, 492 frauds, zero nulls. |
| **5** | Data Cleaning & SQLite DB | **Yash Bhankale** | Retaining 1,081 bot duplicates, SQLite DB (`fraud_analysis.db`) build. |
| **6** | 2:00 AM Surge Forensics | **Yash Bhankale** | 1.713% fraud rate at 2:00 AM (9.92x baseline risk; legitimate volume drops 85%). |
| **7** | Monetary Tiers & Bi-Modal Pattern | **Yash Bhankale** | Micro card tests (<$5) vs high-ticket extractions (>$500) &rarr; **Passes floor to Aditya**. |
| **8–10** | Latent PCA Space & Drivers | **Aditya Kumar** | V14 vs V17 clustering; negative anchors (V17, V14, V12) vs positive bursts (V11, V4). |
| **11** | Leak-Free Pre-Processing | **Aditya Kumar** | Scikit-Learn transformers, log-amount scaling, sine-cosine hour encoding. |
| **12** | Baseline Logistic Regression | **Aditya Kumar** | Directional odds ratios; validation of negative coefficients for V14 and V17. |
| **13–15**| ML Benchmarks & Breakthrough | **Aditya Kumar** | ROC-AUC flaw vs PR-AUC (0.8433); slashing false alarms from 1,492 to 26; saving $73.3k. |
| **16** | Power BI Dashboard & 3 Tiers | **Aditya Kumar** | Tier 1 (<30% Clear), Tier 2 (30–70% Step-up MFA at 2 AM), Tier 3 (>=70% Freeze). |
| **17** | Deployment Roadmap & Conclusion | **Yash & Aditya** | Yash covers pipeline QA and tests; Aditya concludes with business ROI and opens Q&A. |

---

## 2. Complete Word-for-Word Script with Transitions

### ACT 1: Executive Context & Architecture (Slides 1 to 3) — Aditya Kumar
- **SLIDE 1 (Title):**  
  *"Good morning, esteemed seniors and evaluators. I am Aditya Kumar, Project Lead, and presenting with me today is Yash Bhankale, our Data Engineering Lead. Together, we are presenting our capstone project: Transactional Fraud Detection Analysis. Over the course of our internship, we engineered an end-to-end risk intelligence architecture combining automated SQL relational forensics, leak-free Scikit-Learn pipelines, supervised algorithm benchmarking, and an operational Power BI dashboard with dynamic risk tiering."*
- **SLIDE 2 (Business Problem):**  
  *"In modern payment processing, financial fraud causes tens of billions in annual dispute and chargeback losses. However, the fundamental engineering challenge is the needle-in-a-haystack paradox: fraud represents only 0.173% of total transaction volume—just 1 out of every 578 transactions. If a bank sets fraud detection rules too aggressively, innocent customers face humiliating false declines, leading to abandoned carts and permanent brand churn. If rules are set too loosely, the bank suffers direct fraud drain. Our project objective was clear: engineer a system that catches fraud with high recall while slashing false alarms to preserve frictionless checkout."*
- **SLIDE 3 (5 Pillars & Architecture):**  
  *"We architected our solution across five technical pillars: data quality auditing, relational SQL feature querying, leak-free feature pipelines, supervised model benchmarking, and an operational Power BI dashboard with dynamic risk tiering. To explain our data ingestion, cleaning, and SQL behavioral forensics, I will now hand over to Yash."*  
  *(Verbal Hand-Off: "Yash, please walk us through the data architecture.")*

---

### ACT 2: Data Quality, SQLite Relational Analytics & Forensics (Slides 4 to 7) — Yash Bhankale
- **SLIDE 4 (Dataset Overview):**  
  *"Thank you, Aditya. We sourced and audited the comprehensive ULB credit card corpus: 284,807 transactions spanning 48 continuous hours, representing $25.16 million in gross transaction value. Confirmed fraud accounts for exactly 492 transactions (0.173%). The dataset provides 28 PCA-transformed components (V1 through V28) to protect cardholder privacy, alongside transaction Time and Amount. Because of this extreme skewness, standard accuracy is a deceptive metric that would mask total detection failure."*
- **SLIDE 5 (Data Cleaning & SQLite Architecture):**  
  *"Our initial data hygiene audit confirmed zero missing or NaN values across all 31 columns. Crucially, we intentionally preserved 1,081 duplicate transactions. In cyber fraud, automated carding bots execute rapid retry bursts with identical card credentials and amounts to probe gateway responses; deleting duplicates would destroy genuine attack signatures. We then built a dedicated SQLite relational database (`outputs/fraud_analysis.db`) via automated Python ETL, enabling indexed, parameterized SQL queries across monetary tiers and temporal windows."*
- **SLIDE 6 (Key Exploratory Findings & 2:00 AM Surge):**  
  *"By deriving cyclical hourly features from the transaction timestamps, our SQL queries uncovered our most vital operational finding: while legitimate customer volume drops by 85% between midnight and 5:00 AM, fraud activity continues unabated. At 2:00 AM, the fraud rate surges to 1.713%—nearly ten times the baseline portfolio risk! Criminals deliberately exploit nocturnal hours when cardholders are asleep and SMS transaction alerts go unread."*
- **SLIDE 7 (Monetary Tiers & Bi-Modal Pattern):**  
  *"Monetary profiling revealed that fraud is strictly bi-modal. We identified 27 micro card tests under $5 where automated bots verify stolen card validity, followed by high-ticket extractions over $500 that drive over 40% of all fraud losses. Furthermore, our automated test suite passes 100% of pipeline validation checks. Now, Aditya will walk you through our latent feature mathematics, model training, and how we solved the false alarm crisis."*  
  *(Verbal Hand-Off: "Aditya, take us through the ML modeling.")*

---

### ACT 3: Machine Learning & False Alarm Breakthrough (Slides 8 to 15) — Aditya Kumar
- **SLIDES 8–10 (Latent PCA Space & Correlation Drivers):**  
  *"Thank you, Yash. The 28 PCA-transformed components protect cardholder privacy while preserving mathematical variance. On Slide 8, mapping V14 against V17 reveals distinct geometric separation: fraudulent transactions form isolated clusters away from legitimate traffic. On Slides 9 and 10, our correlation heatmaps demonstrate that V17 (-0.33), V14 (-0.30), and V12 (-0.26) serve as our strongest negative anchors, while V11 (+0.15) and V4 (+0.13) act as positive velocity burst indicators."*
- **SLIDE 11 (Leak-Free Pipelines):**  
  *"To prevent data leakage, all transformations were encapsulated in Scikit-Learn pipelines fitted strictly on training data. We applied log-transformation (`Log_Amount`) to compress transaction skewness and mapped cyclical `Hour_of_Day` features using sine-cosine encoding to preserve continuous temporal cycles."*
- **SLIDE 12 (Baseline Logistic Regression):**  
  *"On Slide 12, our baseline Logistic Regression model demonstrates clear directional coefficients: each unit decrease in V14 and V17 exponentially inflates the estimated log-odds of fraud, confirming our exploratory findings."*
- **SLIDES 13–15 (Model Benchmarks & The False Alarm Breakthrough):**  
  *"We benchmarked our models on a 56,962-transaction holdout set containing 98 actual frauds. As shown on Slide 14, standard ROC-AUC gives a misleadingly high score of 0.97 for both models due to the huge majority class. Precision-Recall AUC reveals the true distinction: Balanced Random Forest achieves 0.8433 versus Logistic Regression's 0.7225.*  
  *Now look at Slide 15 for our central business breakthrough: Baseline Logistic Regression catches 90.8% of frauds (89/98), but triggers a massive 1,492 false alarms! Investigating those requires 373 analyst review hours, costing $18,650 in wasted operational salary and alienating customers. Our Production Champion, Balanced Random Forest, maintains an 81.63% catch rate while slashing false alarms by 98.3% down to just 26! This cuts review time to 6.5 hours, saving $73,300 in analyst overhead and generating +$47,782 in net economic value versus a -$19,991 deficit for Logistic Regression."*

---

### ACT 4: Dashboard, Dynamic Mitigation & Conclusion (Slides 16 to 17) — Aditya & Yash
- **SLIDE 16 (Power BI Risk Dashboard & 3-Tier Dynamic Policy) — Aditya Kumar:**  
  *"To operationalize this scoring engine, we built a Power BI Star-Schema dashboard backed by an enterprise 3-Tier Mitigation Architecture:*  
  *• Tier 1 (< 30% risk): 98.45% of transactions pass frictionless with sub-50ms latency.*  
  *• Tier 2 (30% to 70% risk): 1.25% trigger automated Step-Up MFA (OTP push). During the 2:00 AM vulnerability window Yash identified, this threshold automatically adjusts down to $150.*  
  *• Tier 3 (≥ 70% risk): 0.30% of traffic is immediately frozen with instant SMS alerts and 5-minute analyst queues.*  
  *We also engineered a standalone web dashboard so non-technical executives can run real-time risk simulations in any browser."*
- **SLIDE 17 (Deployment Roadmap, QA & Conclusion) — Yash Bhankale & Aditya Kumar:**  
  *• Yash: "From an engineering standpoint, our pipeline is fully automated and hardened: 10 out of 10 automated Pytest suites pass, our relational SQLite database is fully indexed, and all code is modularized and versioned on GitHub."*  
  *• Aditya: "By pairing robust data engineering with calibrated machine learning and dynamic Power BI risk tiering, we have delivered a system that prevents tens of thousands in fraud losses while preserving frictionless customer checkout. Thank you, and Yash and I are ready for your questions."*

---

## 3. Senior Q&A Defense Matrix (Bifurcated Aditya & Yash)

### Yash Bhankale Answers:
1. **"Where did the dataset come from and how was integrity verified?"**  
   &rarr; ULB Machine Learning Group via Kaggle (284,807 transactions, $25.16M volume, 492 frauds). SHA-256 validated, zero null records, V1–V28 PCA anonymity.
2. **"Why not issue a blanket block on all transactions during the 2:00 AM window?"**  
   &rarr; 98.287% of 2:00 AM transactions are legitimate. A blanket block destroys customer trust and sales. We selectively apply Step-Up MFA and lower thresholds to $150.
3. **"Why did you preserve 1,081 duplicate transactions?"**  
   &rarr; Automated bots fire rapid retry bursts with identical credentials. Dropping duplicates deletes authentic cyber attack signatures.
4. **"Why construct a dedicated SQLite database instead of querying pandas in memory?"**  
   &rarr; Banking compliance requires auditable, reproducible SQL queries rather than ephemeral memory. `fraud_analysis.db` ensures query auditability and lakehouse compatibility.
5. **"How did you verify data pipeline robustness and testing coverage?"**  
   &rarr; Built 10 automated test suites in `tests/test_pipeline.py` checking zero null injection, temporal monotonicity, and shape validity (100% pass rate).

### Aditya Kumar Answers:
1. **"Why choose Random Forest over Logistic Regression when Logistic Regression had higher Recall (90.8% vs 81.6%)?"**  
   &rarr; Logistic Regression triggered 1,492 false alarms, costing 373 analyst hours ($18,650) and customer churn. Random Forest triggered only 26 false alarms (98.3% drop), saving $73,300 in review overhead and delivering +$47,782 net value vs -$19,991 deficit.
2. **"Why not use SMOTE or oversampling on the minority class?"**  
   &rarr; SMOTE interpolates artificial points that cross non-linear boundaries in rare-event data (0.173%), distorting probability calibration and inflating false positives. We used cost-sensitive class weights and threshold tuning directly.
3. **"How do you explain PCA latent components (V1–V28) to non-technical business executives?"**  
   &rarr; Translated into directional risk drivers: V14, V17, V12 are negative behavioral anchors (anomalies in spending consistency), while V11 and V4 are positive velocity bursts.
4. **"Why build an Excel Star-Schema and web app instead of just sharing a notebook?"**  
   &rarr; Executives and fraud analysts do not run Jupyter notebooks. The Star Schema enables real-time slicing by hour, amount, and tier; the web app runs anywhere without Python.
5. **"What is the projected financial impact if deployed in production?"**  
   &rarr; Slashes review waste by $73,300 on our test set while recovering 81.6% of fraud losses, creating annual net benefits exceeding $200,000 at enterprise scale.