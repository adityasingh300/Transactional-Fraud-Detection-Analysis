# Quick Start Guide: Loading Your Dashboard in Power BI Desktop
**Infyntrex Internship - Transactional Fraud Detection Analysis**

---

## ⚠️ Why Did the `.pbit` / `.pbip` File Show an Error?

Microsoft Power BI Desktop uses a **proprietary, compiled VertiPaq binary database engine**. When any third-party tool generates a `.pbit` or `.pbip` file externally, Power BI Desktop's security parser rejects it as *"unsupported or corrupt"* because it lacks Microsoft's internal binary signature.

**The Good News:** All your data has been **pre-engineered, structured, and curated into an optimized Star-Schema Excel Data Model**. You can load it into Power BI Desktop in **under 60 seconds**!

---

## ⚡ 3-Step Instant Load in Power BI Desktop (Under 60 Seconds)

### Step 1: Open Power BI Desktop & Load the Pre-Packaged Data Model
1. Open **Power BI Desktop** from your Windows Start Menu.
2. On the top ribbon, click **Get Data** ➔ **Excel workbook**.
3. Browse to and select:
   ```
   C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis\PowerBI\data\Fraud_Detection_PowerBI_DataModel.xlsx
   ```
4. A Navigator dialog will appear showing all 6 sheets:
   - ☑ `Fact_Transactions` (20,000 stratified transactions with enriched features, risk scores, amount bands)
   - ☑ `Dim_Time_Analysis` (24 hourly profiles with diurnal risk multipliers)
   - ☑ `Dim_Amount_Segments` (6 monetary bands with criminal modus operandi profiling)
   - ☑ `Dim_Risk_Tiers` (3-tier operational decision policy specifications)
   - ☑ `Fact_Model_Benchmark` (Complete ML metrics, confusion matrix & ROI)
   - ☑ `Dim_Feature_Drivers` (Top 10 feature drivers with PCA notes)
5. Select the checkbox next to **all 6 tables** and click **Load**.
   *(Power BI will ingest the data and automatically establish relationships in 2-3 seconds).*

---

### Step 2: Apply the Executive Corporate Theme (No AI Clutter)
1. On the top menu bar, click the **View** tab.
2. In the **Themes** dropdown, click **Browse for themes...**
3. Select the file:
   ```
   C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis\PowerBI\themes\corporate_fraud_theme.json
   ```
4. Power BI will instantly apply the **Executive Corporate Dark Slate Theme** (Dark canvas `#0F172A`, solid card containers, crisp borders, and professional fintech alert colors).

---

### Step 3: Add the DAX Measures & Build Visuals
1. In the **Modeling** tab, click **New Measure**.
2. Open the file:
   ```
   C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis\PowerBI\DAX_Measures_Library.dax
   ```
3. Copy and paste any of the 35+ pre-calculated measures (e.g., `Total Volume USD`, `Fraud Loss USD`, `Fraud Rate %`, `RF Fraud Catch Rate %`, `False Alarm Reduction %`, `Net Economic Value Delivered USD`).
4. Save your report as:
   ```
   Transactional_Fraud_Detection_Dashboard.pbix
   ```

---

## 🖥️ Alternative 1: Immediate Presentation in Browser (Zero Setup)

If you have a meeting right now or want to present immediately in full screen without waiting to build visuals:
1. Go to:
   ```
   C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis\PowerBI\dashboard\index.html
   ```
2. Double-click to open in **Google Chrome** or **Microsoft Edge**.
3. Press **F11** for full-screen presenter mode.
4. It includes:
   - 4 full interactive pages (Executive Overview, Forensics, ML Benchmark, 3-Tier Strategy)
   - Live interactive slicers (Diurnal Windows, Monetary Segments, Status)
   - Live model toggle (Random Forest vs Logistic Regression)
   - Presenter Notes drawer (click `🎙️ Presenter Notes` for word-for-word talking points)

---

## 📽️ Alternative 2: Executive PowerPoint Slide Deck

If you are presenting via slides:
1. Open:
   ```
   C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis\PowerBI\Fraud_Detection_PowerBI_Presentation.pptx
   ```
2. Contains **10 professionally formatted slides** matching the executive corporate dark theme with full ground truth numbers and charts.

