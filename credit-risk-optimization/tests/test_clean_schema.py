"""
tests/test_clean_schema.py
Clean Lineage Assertion Suite (Phase 1 / Task 1.3)

Pytest suite validating data contracts for:
  - data/cleaned/fct_closed_loans_seasoned.parquet
  - data/cleaned/fct_active_portfolio.parquet

Key assertions:
  1. Mature cohort contains zero 'Current' or open loans.
  2. is_bad_loan is non-null and strictly binary {0, 1}.
  3. laroc is finite and reconciles with cash flow ledger totals.
  4. funded_amnt is strictly positive (> 0).
  5. Active portfolio contains only open loans with zero mature loans.
"""

from pathlib import Path
import pytest
import pandas as pd
import numpy as np

CLEANED_DIR = Path("data/cleaned")
CLOSED_PARQUET = CLEANED_DIR / "fct_closed_loans_seasoned.parquet"
ACTIVE_PARQUET = CLEANED_DIR / "fct_active_portfolio.parquet"

OPEN_STATUSES = {"Current", "Late (16-30 days)", "Late (31-120 days)", "In Grace Period"}
CLOSED_STATUSES = {"Fully Paid", "Charged Off", "Default"}


def test_cleaned_parquet_files_exist():
    """Verify both cleaned Parquet files exist and have non-trivial size."""
    assert CLOSED_PARQUET.exists(), f"Missing mature closed loans file: {CLOSED_PARQUET}"
    assert ACTIVE_PARQUET.exists(), f"Missing active portfolio file: {ACTIVE_PARQUET}"
    assert CLOSED_PARQUET.stat().st_size > 10_000_000, "fct_closed_loans_seasoned.parquet is too small"
    assert ACTIVE_PARQUET.stat().st_size > 10_000_000, "fct_active_portfolio.parquet is too small"


@pytest.fixture(scope="module")
def df_seasoned():
    """Load core verification columns from fct_closed_loans_seasoned.parquet."""
    cols = [
        "id", "loan_status", "is_bad_loan", "funded_amnt", "total_pymnt",
        "recoveries", "collection_recovery_fee", "net_cash_flow", "laroc",
        "term", "int_rate", "revol_util", "fico_range_low", "fico_range_high",
        "fico_midpoint", "vintage_year", "dti", "invalid_dti_flag",
        "dti_bracket", "revol_util_bracket", "annual_inc", "annual_inc_winsorized"
    ]
    return pd.read_parquet(CLOSED_PARQUET, columns=cols)


@pytest.fixture(scope="module")
def df_active():
    """Load core verification columns from fct_active_portfolio.parquet."""
    return pd.read_parquet(ACTIVE_PARQUET, columns=["id", "loan_status", "funded_amnt"])


def test_seasoned_contains_zero_current_or_open_loans(df_seasoned):
    """
    Assert that data/cleaned/fct_closed_loans_seasoned.parquet contains
    zero 'Current' or open loans (strictly mature resolved outcomes).
    """
    actual_statuses = set(df_seasoned["loan_status"].unique())
    # Must be strictly subset of closed statuses
    assert actual_statuses.issubset(CLOSED_STATUSES), (
        f"Unexpected loan statuses found in seasoned cohort: {actual_statuses - CLOSED_STATUSES}"
    )
    # Zero open statuses allowed
    overlap = actual_statuses.intersection(OPEN_STATUSES)
    assert len(overlap) == 0, f"Open loans found in mature seasoned table: {overlap}"


def test_is_bad_loan_is_non_null_and_strictly_binary(df_seasoned):
    """
    Assert that is_bad_loan is non-null and strictly binary {0, 1},
    perfectly matching the terminal loan status definitions.
    """
    # 1. Non-null
    assert df_seasoned["is_bad_loan"].isna().sum() == 0, "is_bad_loan contains NULL values!"

    # 2. Strictly binary {0, 1}
    unique_vals = set(df_seasoned["is_bad_loan"].unique())
    assert unique_vals.issubset({0, 1}), f"Non-binary values in is_bad_loan: {unique_vals}"

    # 3. Status mapping fidelity
    bad_status_mask = df_seasoned["loan_status"].isin(["Charged Off", "Default"])
    assert (df_seasoned.loc[bad_status_mask, "is_bad_loan"] == 1).all(), (
        "Charged Off / Default loans not marked as 1 in is_bad_loan"
    )
    good_status_mask = df_seasoned["loan_status"] == "Fully Paid"
    assert (df_seasoned.loc[good_status_mask, "is_bad_loan"] == 0).all(), (
        "Fully Paid loans not marked as 0 in is_bad_loan"
    )


def test_laroc_is_finite_and_matches_ledger_totals(df_seasoned):
    """
    Assert that laroc is finite and matches raw cash flow ledger totals:
    net_cash_flow = total_pymnt + recoveries - collection_recovery_fee - funded_amnt
    laroc = (net_cash_flow / funded_amnt) * 100.0
    """
    # 1. Finite check
    assert np.isfinite(df_seasoned["laroc"]).all(), "LAROC contains non-finite values (NaN / Inf)!"
    assert np.isfinite(df_seasoned["net_cash_flow"]).all(), "net_cash_flow contains non-finite values!"

    # 2. Recomputed cash flow reconciliation
    expected_ncf = (
        df_seasoned["total_pymnt"]
        + df_seasoned["recoveries"]
        - df_seasoned["collection_recovery_fee"]
        - df_seasoned["funded_amnt"]
    )
    np.testing.assert_allclose(
        df_seasoned["net_cash_flow"].values,
        expected_ncf.values,
        rtol=1e-5,
        atol=1e-4,
        err_msg="net_cash_flow does not match raw payment ledger sum!"
    )

    # 3. Recomputed LAROC reconciliation
    expected_laroc = (df_seasoned["net_cash_flow"] / df_seasoned["funded_amnt"]) * 100.0
    np.testing.assert_allclose(
        df_seasoned["laroc"].values,
        expected_laroc.values,
        rtol=1e-5,
        atol=1e-4,
        err_msg="LAROC does not match (net_cash_flow / funded_amnt) * 100.0!"
    )

    # 4. Aggregate ledger reconciliation
    total_funded = df_seasoned["funded_amnt"].sum()
    total_net_cash = df_seasoned["net_cash_flow"].sum()
    expected_agg_laroc = (total_net_cash / total_funded) * 100.0
    assert -50.0 < expected_agg_laroc < 50.0, f"Unreasonable aggregate portfolio LAROC: {expected_agg_laroc:.2f}%"


def test_funded_amnt_strictly_positive(df_seasoned):
    """Assert funded_amnt is strictly positive (> 0) and has no missing values."""
    assert df_seasoned["funded_amnt"].isna().sum() == 0, "funded_amnt contains NULLs!"
    assert (df_seasoned["funded_amnt"] > 0).all(), "funded_amnt contains zero or negative amounts!"
    assert df_seasoned["funded_amnt"].min() >= 500.0, f"Unexpected min funded amount: {df_seasoned['funded_amnt'].min()}"


def test_active_portfolio_contract(df_active):
    """Assert active portfolio contains exclusively open loan originations."""
    actual_active_statuses = set(df_active["loan_status"].unique())
    assert actual_active_statuses.issubset(OPEN_STATUSES), (
        f"Unexpected loan statuses in active portfolio: {actual_active_statuses - OPEN_STATUSES}"
    )
    assert len(actual_active_statuses.intersection(CLOSED_STATUSES)) == 0, (
        "Closed loans leaked into active portfolio table!"
    )
    assert (df_active["funded_amnt"] > 0).all(), "Active portfolio contains zero/negative funded amount!"


def test_underwriting_feature_engineering_sanity(df_seasoned):
    """Assert integrity of augmented risk features and categorical brackets."""
    # term
    assert set(df_seasoned["term"].unique()).issubset({36, 60}), "Unexpected loan term values"

    # int_rate in [0.05, 0.35]
    valid_rates = df_seasoned["int_rate"].dropna()
    assert (valid_rates > 0.0).all() and (valid_rates < 1.0).all(), "int_rate values out of decimal [0, 1] range"

    # fico_midpoint
    expected_fico = (df_seasoned["fico_range_low"] + df_seasoned["fico_range_high"]) / 2.0
    np.testing.assert_allclose(df_seasoned["fico_midpoint"].values, expected_fico.values)

    # vintage_year
    assert df_seasoned["vintage_year"].between(2007, 2019).all(), "vintage_year out of valid LendingClub range"

    # invalid_dti_flag
    assert set(df_seasoned["invalid_dti_flag"].unique()).issubset({0, 1})

    # dti_bracket valid categories
    valid_dti_cats = {
        "1. Low (<=15%)", "2. Moderate (15-25%)", "3. High (25-35%)", "4. Severe (>35%)"
    }
    actual_dti_cats = set(df_seasoned["dti_bracket"].dropna().unique())
    assert actual_dti_cats.issubset(valid_dti_cats), f"Unexpected DTI brackets: {actual_dti_cats}"

    # revol_util_bracket valid categories
    valid_util_cats = {
        "1. Conservative (<=40%)", "2. Moderate (40-65%)", "3. High (65-85%)", "4. Maxed (>85%)"
    }
    actual_util_cats = set(df_seasoned["revol_util_bracket"].dropna().unique())
    assert actual_util_cats.issubset(valid_util_cats), f"Unexpected util brackets: {actual_util_cats}"

    # annual_inc_winsorized
    assert (df_seasoned["annual_inc_winsorized"] <= 350000.0 + 1e-3).all()
