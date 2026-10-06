"""
sql_analysis.py
Performs transactional fraud analysis using SQLite to demonstrate practical SQL skills.
"""

import os
import sqlite3
import logging
from typing import Dict, Any, Optional
import pandas as pd
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_processing import load_dataset, find_dataset_path

logger = logging.getLogger(__name__)


class FraudSQLAnalyzer:
    """
    Manages SQLite database ingestion and analytical queries for credit card fraud data.
    """
    
    def __init__(self, db_path: str = "outputs/fraud_analysis.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)
        
    def setup_database(self, df: Optional[pd.DataFrame] = None, force_reload: bool = False):
        """
        Loads dataset into SQLite table 'transactions' with an index on Class and Time.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
            table_exists = cursor.fetchone() is not None
            
            if table_exists and not force_reload:
                cursor.execute("SELECT COUNT(*) FROM transactions;")
                count = cursor.fetchone()[0]
                logger.info(f"Database already populated with {count:,} transactions.")
                return
                
            if df is None:
                logger.info("Loading dataset to populate SQLite database...")
                df = load_dataset()
                
            logger.info("Writing dataframe to SQLite table 'transactions'...")
            df.to_sql("transactions", conn, if_exists="replace", index=False)
            
            # Create indexes for analytical performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_class ON transactions(Class);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_time ON transactions(Time);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_amount ON transactions(Amount);")
            conn.commit()
            logger.info("SQLite database setup complete with indexes.")

    def run_query(self, query: str, params: tuple = ()) -> pd.DataFrame:
        """
        Executes a SQL query and returns results as a pandas DataFrame.
        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)

    def get_overall_summary(self) -> pd.DataFrame:
        """
        Query 1: Overall transaction and fraud volume metrics.
        """
        query = """
        SELECT
            COUNT(*) AS total_transactions,
            SUM(CASE WHEN Class = 0 THEN 1 ELSE 0 END) AS legitimate_transactions,
            SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) AS fraudulent_transactions,
            ROUND(AVG(Class) * 100, 4) AS fraud_rate_percentage,
            ROUND(SUM(Amount), 2) AS total_amount,
            ROUND(AVG(Amount), 2) AS overall_avg_amount
        FROM transactions;
        """
        return self.run_query(query)

    def get_class_comparison(self) -> pd.DataFrame:
        """
        Query 2: Detailed statistical comparison between Legitimate and Fraudulent transactions.
        """
        query = """
        SELECT
            CASE WHEN Class = 1 THEN 'Fraudulent' ELSE 'Legitimate' END AS transaction_type,
            COUNT(*) AS transaction_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 4) AS volume_percentage,
            ROUND(SUM(Amount), 2) AS total_amount,
            ROUND(AVG(Amount), 2) AS avg_amount,
            ROUND(MIN(Amount), 2) AS min_amount,
            ROUND(MAX(Amount), 2) AS max_amount
        FROM transactions
        GROUP BY Class
        ORDER BY Class DESC;
        """
        return self.run_query(query)

    def get_amount_bands_analysis(self) -> pd.DataFrame:
        """
        Query 3: Fraud distribution across transaction amount tiers.
        """
        query = """
        SELECT
            CASE
                WHEN Amount < 10 THEN '1. Micro (< $10)'
                WHEN Amount BETWEEN 10 AND 50 THEN '2. Small ($10 - $50)'
                WHEN Amount BETWEEN 50 AND 100 THEN '3. Medium ($50 - $100)'
                WHEN Amount BETWEEN 100 AND 500 THEN '4. Large ($100 - $500)'
                WHEN Amount BETWEEN 500 AND 1000 THEN '5. High ($500 - $1,000)'
                ELSE '6. Very High ($1,000+)'
            END AS amount_tier,
            COUNT(*) AS total_tx_count,
            SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) AS fraud_tx_count,
            ROUND(SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS fraud_rate_pct,
            ROUND(SUM(Amount), 2) AS total_volume_in_tier
        FROM transactions
        GROUP BY amount_tier
        ORDER BY amount_tier;
        """
        return self.run_query(query)

    def get_hourly_analysis(self) -> pd.DataFrame:
        """
        Query 4: Hourly transaction patterns (Time is seconds elapsed over 48 hours).
        Maps Time to hour of day (0-23) across both days.
        """
        query = """
        SELECT
            CAST((Time / 3600) % 24 AS INT) AS hour_of_day,
            COUNT(*) AS total_tx,
            SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) AS fraud_tx,
            ROUND(SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS fraud_rate_pct,
            ROUND(AVG(Amount), 2) AS avg_amount
        FROM transactions
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
        """
        return self.run_query(query)

    def get_top_fraud_transactions(self, limit: int = 10) -> pd.DataFrame:
        """
        Query 5: Parameterized query to fetch top largest fraudulent transactions.
        """
        query = """
        SELECT
            Time,
            Amount,
            V1, V2, V3, V4, V14, V17
        FROM transactions
        WHERE Class = ?
        ORDER BY Amount DESC
        LIMIT ?;
        """
        return self.run_query(query, params=(1, limit))

    def run_all_analyses(self) -> Dict[str, pd.DataFrame]:
        """
        Executes all SQL queries and returns a dictionary of DataFrames.
        """
        self.setup_database()
        results = {
            "overall_summary": self.get_overall_summary(),
            "class_comparison": self.get_class_comparison(),
            "amount_bands": self.get_amount_bands_analysis(),
            "hourly_analysis": self.get_hourly_analysis(),
            "top_fraud_tx": self.get_top_fraud_transactions(limit=10)
        }
        return results


if __name__ == "__main__":
    analyzer = FraudSQLAnalyzer()
    results = analyzer.run_all_analyses()
    print("\n--- Overall Summary ---")
    print(results["overall_summary"])
    print("\n--- Class Comparison ---")
    print(results["class_comparison"])
    print("\n--- Amount Bands Analysis ---")
    print(results["amount_bands"])
    print("\n--- Hourly Analysis (First 5 hours) ---")
    print(results["hourly_analysis"].head())
