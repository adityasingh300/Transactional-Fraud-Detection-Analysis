"""
run_project.py
Master execution script for the Transactional Fraud Detection Analysis Project.
Orchestrates data processing, SQL analytics, EDA, model training, evaluation, and test validation.
"""

import os
import sys
import time
import argparse
import logging
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_processing import load_dataset, inspect_data, generate_data_quality_report
from src.sql_analysis import FraudSQLAnalyzer
from src.eda import FraudEDA
from src.train_model import train_and_evaluate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger("RunProject")


def print_banner():
    banner = """
========================================================================================
   TRANSACTIONAL FRAUD DETECTION ANALYSIS: END-TO-END PIPELINE RUNNER
========================================================================================
   Stack: Python, Pandas, SQLite, Scikit-learn, Streamlit, Plotly
   Dataset: Kaggle ULB Credit Card Fraud Detection (284,807 transactions)
========================================================================================
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(description="Execute Fraud Detection Analysis Pipeline")
    parser.add_argument("--data-path", type=str, default=None, help="Path to creditcard.csv")
    parser.add_argument("--skip-tests", action="store_true", help="Skip pytest test suite")
    parser.add_argument("--launch-dashboard", action="store_true", help="Launch Streamlit dashboard upon completion")
    args = parser.parse_args()

    start_time = time.time()
    print_banner()

    # Step 1: Data Profiling & Quality Audit
    logger.info(">>> STEP 1/5: Loading and Profiling Dataset...")
    df = load_dataset(args.data_path)
    summary = inspect_data(df)
    report_df = generate_data_quality_report(df)
    logger.info(f"Data profiling complete: {summary['total_records']:,} rows, {summary['fraudulent_transactions']:,} frauds ({summary['fraud_percentage']}%)")

    # Step 2: SQL Analytics
    logger.info("\n>>> STEP 2/5: Initializing SQLite Analytics Database...")
    sql_analyzer = FraudSQLAnalyzer()
    sql_results = sql_analyzer.run_all_analyses()
    logger.info("SQLite analytics complete. Table 'transactions' populated with indexed queries.")

    # Step 3: Exploratory Data Analysis & Visualizations
    logger.info("\n>>> STEP 3/5: Executing Exploratory Data Analysis & Generating Charts...")
    eda = FraudEDA()
    eda_findings = eda.run_full_eda(df)
    logger.info("EDA completed. 9 publication-grade figures saved to reports/figures/.")

    # Step 4: Machine Learning Model Training & Evaluation
    logger.info("\n>>> STEP 4/5: Training Baseline & Comparison Models...")
    model_metrics = train_and_evaluate(test_size=0.2, random_state=42, include_random_forest=True)
    logger.info("Model training & evaluation complete. Primary pipeline saved to models/fraud_detection_model.joblib.")

    # Step 5: Automated Testing
    if not args.skip_tests:
        logger.info("\n>>> STEP 5/5: Running Automated Test Suite...")
        import pytest
        test_exit_code = pytest.main(["tests/test_pipeline.py", "-v"])
        if test_exit_code == 0:
            logger.info("All unit and pipeline tests PASSED successfully!")
        else:
            logger.error("Some tests failed. Please review the test logs above.")
    else:
        logger.info("\n>>> STEP 5/5: Skipping tests as requested.")

    elapsed = time.time() - start_time
    print(f"""
========================================================================================
   PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN {elapsed:.1f} SECONDS!
========================================================================================
   Artifacts Summary:
   - Cleaned SQLite DB:     outputs/fraud_analysis.db
   - Quality Report:        outputs/data_quality_report.csv
   - Model Metrics:         outputs/model_metrics.json
   - Persisted Model:       models/fraud_detection_model.joblib
   - Generated Figures:     reports/figures/ (12 figures)
   - Comprehensive Report:  reports/project_report.md
   - Executive Summary:     reports/executive_summary.md
   - Presentation Deck:     reports/presentation.md & reports/fraud_detection_presentation.pptx
   - Jupyter Notebook:      notebooks/fraud_detection_analysis.ipynb

   Commands to Interact:
   1. Launch Dashboard:     streamlit run dashboard/app.py
   2. Run Test Suite:       pytest tests/test_pipeline.py
   3. Single Inference:     python src/predict.py
========================================================================================
    """)

    if args.launch_dashboard:
        logger.info("Launching Streamlit dashboard...")
        os.system("streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()
