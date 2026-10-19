"""
LendingClub Raw Data Profiler (SCAN Framework - Phase 1 & 2)
Audits the raw CSV, verifies DATA_SPEC requirements, and isolates censoring splits.
"""
from pathlib import Path
import pandas as pd
import numpy as np

# Adjust raw data file path if different
DATA_PATH = Path("data/raw/accepted_2007_to_2018Q4.csv")

if not DATA_PATH.exists():
    # Check current directory fallback
    alt_path = Path("accepted_2007_to_2018Q4.csv")
    if alt_path.exists():
        DATA_PATH = alt_path
    else:
        raise FileNotFoundError(f"Could not locate raw dataset at {DATA_PATH.resolve()}")

print(f"=== 1. LOADING & GRAIN AUDIT: {DATA_PATH.name} ===")

# Core columns defined in docs/DATA_SPEC.md
CRITICAL_COLS = [
    "id", "loan_amnt", "funded_amnt", "term", "int_rate", "installment",
    "grade", "sub_grade", "emp_length", "home_ownership", "annual_inc",
    "verification_status", "issue_d", "loan_status", "purpose", "addr_state",
    "dti", "fico_range_low", "fico_range_high", "open_acc", "pub_rec",
    "revol_bal", "revol_util", "total_acc", "total_pymnt", "total_rec_prncp",
    "total_rec_int", "recoveries", "collection_recovery_fee"
]

# Read only critical columns with low_memory=False to prevent Dtype warnings
print("Reading target schema columns...")
df = pd.read_csv(DATA_PATH, usecols=lambda c: c in CRITICAL_COLS, low_memory=False)

# Drop any entirely empty footer rows common in Kaggle dumps
df = df.dropna(subset=["loan_amnt", "issue_d", "loan_status"])

total_rows = len(df)
total_funded = df["funded_amnt"].sum()
unique_ids = df["id"].nunique()

print(f"Total Funded Originations (Grain Check): {total_rows:,} records")
print(f"Unique Loan IDs: {unique_ids:,} (100% Unique: {total_rows == unique_ids})")
print(f"Total Funded Capital: ${total_funded:,.2f}")

print("\n=== 2. CENSONRING & LOAN STATUS BREAKDOWN (CLEAN Protocol ISS-01) ===")
status_counts = df["loan_status"].value_counts(dropna=False)
status_pcts = df["loan_status"].value_counts(normalize=True, dropna=False) * 100
status_summary = pd.DataFrame({"Count": status_counts, "Share (%)": status_pcts.round(2)})
print(status_summary.to_string())

# Define terminal mature vs active cohort
closed_statuses = ["Fully Paid", "Charged Off", "Default"]
mature_mask = df["loan_status"].isin(closed_statuses)
n_mature = mature_mask.sum()
n_active = total_rows - n_mature

print(f"\nMature Closed Loans (fct_closed_loans_seasoned): {n_mature:,} ({n_mature/total_rows:.1%})")
print(f"Active / Unseasoned Loans (fct_active_portfolio): {n_active:,} ({n_active/total_rows:.1%})")

print("\n=== 3. MATURE COHORT RISK BASELINE ===")
df_mature = df[mature_mask].copy()
bad_mask = df_mature["loan_status"].isin(["Charged Off", "Default"])
n_bad = bad_mask.sum()
bad_rate = (n_bad / n_mature) * 100

print(f"Terminal Bad Loans (Charged Off / Default): {n_bad:,}")
print(f"True Terminal Default Rate (Closed Cohort): {bad_rate:.2f}%")
raw_naive_rate = (n_bad / total_rows) * 100
print(f"Naive Unfiltered Default Rate (With Censoring Bias): {raw_naive_rate:.2f}%")

print("\n=== 4. DATA COMPLETENESS AUDIT (CRITICAL COLUMNS) ===")
null_summary = df_mature[["int_rate", "term", "grade", "dti", "revol_util", "annual_inc", "fico_range_low"]].isnull().sum()
null_pct = (null_summary / n_mature) * 100
print(pd.DataFrame({"Missing Count": null_summary, "Missing (%)": null_pct.round(3)}).to_string())

print("\n=== 5. VINTAGE SPAN CHECK ===")
# Parse issue date to verify vintage range
df_mature["issue_year"] = pd.to_datetime(df_mature["issue_d"], format="%b-%Y", errors="coerce").dt.year
vintage_breakdown = df_mature.groupby("issue_year")["funded_amnt"].agg(["count", "sum"]).rename(columns={"count": "Originations", "sum": "Funded_Capital"})
vintage_breakdown["Funded_Capital"] = vintage_breakdown["Funded_Capital"].apply(lambda x: f"${x:,.0f}")
print(vintage_breakdown.to_string())
print("\n[Done] Run completed successfully.")