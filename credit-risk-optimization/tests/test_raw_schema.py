"""
tests/test_raw_schema.py
Pre-flight raw schema validation asserting data/raw/accepted_2007_to_2018Q4.csv
exists and contains all critical underwriting and performance attributes.
"""
from pathlib import Path
import pytest
import pandas as pd

RAW_DATA_PATH = Path("data/raw/accepted_2007_to_2018Q4.csv")

IDENTIFIERS_AND_TERMS = [
    "id", "loan_amnt", "funded_amnt", "term", "int_rate", "installment",
    "grade", "sub_grade", "issue_d", "loan_status", "purpose", "addr_state"
]

BORROWER_PROFILE = [
    "emp_length", "home_ownership", "annual_inc", "verification_status", "dti"
]

CREDIT_RISK_AND_BUREAU = [
    "fico_range_low", "fico_range_high", "open_acc", "total_acc",
    "revol_bal", "revol_util", "pub_rec"
]

PERFORMANCE_AND_COLLECTIONS = [
    "total_pymnt", "total_rec_prncp", "total_rec_int", "recoveries",
    "collection_recovery_fee"
]

ALL_CRITICAL_COLUMNS = (
    IDENTIFIERS_AND_TERMS +
    BORROWER_PROFILE +
    CREDIT_RISK_AND_BUREAU +
    PERFORMANCE_AND_COLLECTIONS
)


def test_raw_data_file_exists():
    """Assert that the raw CSV file exists and has non-zero size."""
    assert RAW_DATA_PATH.exists(), f"Raw file missing at {RAW_DATA_PATH.resolve()}"
    assert RAW_DATA_PATH.stat().st_size > 100_000_000, "Raw file exists but size is unexpectedly small."


@pytest.fixture(scope="module")
def raw_columns():
    """Read only the header line to inspect columns without loading the full 1.6GB file."""
    df_head = pd.read_csv(RAW_DATA_PATH, nrows=0)
    return set(df_head.columns)


def test_identifiers_and_terms_present(raw_columns):
    """Verify all identifier and loan term columns exist."""
    missing = [c for c in IDENTIFIERS_AND_TERMS if c not in raw_columns]
    assert not missing, f"Missing Identifiers & Terms columns: {missing}"


def test_borrower_profile_present(raw_columns):
    """Verify all borrower profile columns exist."""
    missing = [c for c in BORROWER_PROFILE if c not in raw_columns]
    assert not missing, f"Missing Borrower Profile columns: {missing}"


def test_credit_risk_and_bureau_present(raw_columns):
    """Verify all credit risk and bureau history columns exist."""
    missing = [c for c in CREDIT_RISK_AND_BUREAU if c not in raw_columns]
    assert not missing, f"Missing Credit Risk & Bureau History columns: {missing}"


def test_performance_and_collections_present(raw_columns):
    """Verify all financial performance and cash collections columns exist."""
    missing = [c for c in PERFORMANCE_AND_COLLECTIONS if c not in raw_columns]
    assert not missing, f"Missing Performance & Collections columns: {missing}"


def test_all_critical_columns_present(raw_columns):
    """Verify the entire union of critical columns is present."""
    missing = [c for c in ALL_CRITICAL_COLUMNS if c not in raw_columns]
    assert not missing, f"Missing critical columns: {missing}"


def test_sample_records_data_types():
    """Read a small sample (100 rows) to ensure parseability and baseline integrity."""
    df_sample = pd.read_csv(
        RAW_DATA_PATH,
        usecols=ALL_CRITICAL_COLUMNS,
        nrows=100,
        low_memory=False
    )
    assert len(df_sample) == 100
    assert "Fully Paid" in df_sample["loan_status"].values or "Current" in df_sample["loan_status"].values
    assert df_sample["funded_amnt"].dropna().gt(0).all()
