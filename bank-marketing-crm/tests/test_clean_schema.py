"""
Unit tests validating cleaned parquet table schemas, data lineage, and business integrity rules.
Enforces zero post-call duration leakage, sentinel resolution, and metric reconciliation.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

DATA_CLEANED_DIR = Path("data/cleaned")
PRECALL_PARQUET_FILE = DATA_CLEANED_DIR / "fct_campaign_precall_targeting.parquet"
OPERATIONAL_PARQUET_FILE = DATA_CLEANED_DIR / "fct_campaign_full_operational.parquet"
BENCHMARK_PARQUET_FILE = DATA_CLEANED_DIR / "fct_legacy_balance_benchmark.parquet"


@pytest.fixture(scope="session")
def df_operational():
    assert OPERATIONAL_PARQUET_FILE.is_file(), f"Missing {OPERATIONAL_PARQUET_FILE}"
    return pd.read_parquet(OPERATIONAL_PARQUET_FILE)


@pytest.fixture(scope="session")
def df_precall():
    assert PRECALL_PARQUET_FILE.is_file(), f"Missing {PRECALL_PARQUET_FILE}"
    return pd.read_parquet(PRECALL_PARQUET_FILE)


@pytest.fixture(scope="session")
def df_benchmark():
    assert BENCHMARK_PARQUET_FILE.is_file(), f"Missing {BENCHMARK_PARQUET_FILE}"
    return pd.read_parquet(BENCHMARK_PARQUET_FILE)


def test_precall_zero_duration_leakage(df_precall):
    """
    ISS-01: Ensure fct_campaign_precall_targeting strictly excludes duration
    and duration_minutes to prevent post-call data leakage in pre-dial targeting models.
    """
    assert "duration" not in df_precall.columns, (
        "Post-call leakage detected: 'duration' found in precall targeting table!"
    )
    assert "duration_minutes" not in df_precall.columns, (
        "Post-call leakage detected: 'duration_minutes' found in precall targeting table!"
    )
    assert len(df_precall) == 41188, f"Expected 41,188 records, got {len(df_precall)}"


def test_operational_dataset_integrity(df_operational):
    """
    Ensure operational table contains all 41,188 records, duration fields,
    and valid target is_subscribed strictly in {0, 1}.
    """
    assert len(df_operational) == 41188, f"Expected 41,188 records, got {len(df_operational)}"
    assert "duration" in df_operational.columns, "Expected 'duration' in operational table"
    assert "duration_minutes" in df_operational.columns, "Expected 'duration_minutes' in operational table"
    assert set(df_operational["is_subscribed"].unique()).issubset({0, 1}), (
        f"Invalid values in is_subscribed: {df_operational['is_subscribed'].unique()}"
    )
    assert df_operational["is_subscribed"].isnull().sum() == 0, "Nulls found in is_subscribed"


def test_sentinel_pdays_mapping(df_operational):
    """
    ISS-02: was_previously_contacted == 0 must map 100% to pdays == 999.
    """
    never_contacted = df_operational[df_operational["was_previously_contacted"] == 0]
    assert (never_contacted["pdays"] == 999).all(), (
        "Inconsistency: was_previously_contacted == 0 does not strictly map to pdays == 999"
    )
    assert len(never_contacted) == 39673, f"Expected 39,673 never contacted, got {len(never_contacted)}"

    previously_contacted = df_operational[df_operational["was_previously_contacted"] == 1]
    assert (previously_contacted["pdays"] != 999).all(), (
        "Inconsistency: was_previously_contacted == 1 has pdays == 999"
    )
    assert len(previously_contacted) == 1515, f"Expected 1,515 previously contacted, got {len(previously_contacted)}"
    assert previously_contacted["pdays_clean"].notnull().all(), "pdays_clean should not be null for contacted leads"
    assert never_contacted["pdays_clean"].isnull().all(), "pdays_clean should be null for pdays == 999"


def test_campaign_touches_and_subscription_totals(df_operational):
    """
    Reconciles total outbound call touches (105,754) and total subscriptions (4,640).
    """
    total_campaign_touches = df_operational["campaign"].sum()
    total_subscriptions = df_operational["is_subscribed"].sum()
    subscription_rate = total_subscriptions / len(df_operational)

    assert total_campaign_touches == 105754, (
        f"Expected sum(campaign) == 105,754, got {total_campaign_touches}"
    )
    assert total_subscriptions == 4640, (
        f"Expected total subscriptions == 4,640, got {total_subscriptions}"
    )
    assert pytest.approx(subscription_rate, abs=1e-5) == (4640 / 41188), (
        f"Subscription rate mismatch: got {subscription_rate:.6f}"
    )


def test_legacy_balance_benchmark_schema(df_benchmark):
    """
    ISS-05: Validates fct_legacy_balance_benchmark row count and median balance.
    """
    assert len(df_benchmark) == 45211, f"Expected 45,211 benchmark rows, got {len(df_benchmark)}"
    assert "balance" in df_benchmark.columns, "Expected 'balance' column in benchmark table"
    assert "high_balance_flag" in df_benchmark.columns, "Expected 'high_balance_flag' in benchmark table"
    median_bal = df_benchmark["balance"].median()
    assert median_bal == 448.0, f"Expected median balance == 448.0, got {median_bal}"
    assert set(df_benchmark["is_subscribed"].unique()).issubset({0, 1})


def test_temporal_reconstruction(df_operational):
    """
    Validates chronological sequence 2008-05 through 2010-11 with zero nulls.
    """
    assert "campaign_year_month" in df_operational.columns
    assert df_operational["campaign_year_month"].min() == "2008-05"
    assert df_operational["campaign_year_month"].max() == "2010-11"
    assert df_operational["campaign_year_month"].isnull().sum() == 0
    assert set(df_operational["campaign_year"].unique()) == {2008, 2009, 2010}


def test_augmented_features_completeness(df_operational):
    """
    Validates that augmented features have zero nulls and expected categories.
    """
    expected_age_buckets = {
        "1. Young (<30)",
        "2. Core Working (31-45)",
        "3. Mature Working (46-60)",
        "4. Senior/Retired (60+)"
    }
    assert set(df_operational["age_bucket"].unique()) == expected_age_buckets
    assert df_operational["age_bucket"].isnull().sum() == 0

    expected_job_collars = {
        "White-Collar",
        "Blue-Collar & Service",
        "High-Yield Non-Working",
        "Unknown"
    }
    assert set(df_operational["job_collar_tier"].unique()) == expected_job_collars
    assert df_operational["job_collar_tier"].isnull().sum() == 0

    expected_campaign_tiers = {
        "1 Touch",
        "2 Touches",
        "3 Touches",
        "4-5 Touches",
        "6+ Touches (Fatigue Zone)"
    }
    assert set(df_operational["campaign_touch_tier"].unique()) == expected_campaign_tiers
    assert df_operational["campaign_touch_tier"].isnull().sum() == 0

    expected_euribor_regimes = {
        "Low Rate Regime (Euribor <= 3.0%)",
        "High Rate Regime (Euribor > 3.0%)"
    }
    assert set(df_operational["euribor_regime"].unique()) == expected_euribor_regimes
    assert df_operational["euribor_regime"].isnull().sum() == 0

    assert df_operational["is_exact_duplicate"].sum() == 12
    assert df_operational["has_unknown_attributes"].sum() == 10700
