# Dataset Directory Documentation

## Dataset Location
The primary dataset used in this project is the **Kaggle Credit Card Fraud Detection Dataset**:
- **Source:** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Local Source Path:** `C:\Users\Aditya\Downloads\Infyntrex internship\creditcard.csv`
- **Fallback Project Path:** `data/creditcard.csv` (or root `creditcard.csv`)

## Schema Information
- **Total Records:** 284,807 transactions
- **Total Features:** 31
- **Features:**
  - `Time`: Elapsed seconds from the first recorded transaction (spans 48 hours).
  - `V1` to `V28`: Latent numerical components obtained via Principal Component Analysis (PCA) to maintain confidentiality.
  - `Amount`: Monetary value of the transaction.
  - `Class`: Binary response label:
    - `0`: Legitimate transaction (284,315 records, 99.827%)
    - `1`: Fraudulent transaction (492 records, 0.173%)

## Data Integrity Rules
- The original CSV is strictly treated as read-only. No raw rows or headers are modified in-place.
- Duplicate rows (1,081 rows) are retained to capture authentic fraud retry frequency patterns.
- 0 missing or NaN values exist in this dataset.
