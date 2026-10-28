"""
Automated SCAN Verification Suite (Phase 2).
Validates conservation of volume, fatigue cliff guardrails, channel multiplier,
demographic lift, macroeconomic elasticity, and strict duration leakage quarantine.
"""

from pathlib import Path
import inspect
import pandas as pd
import pytest

from src.analytics import scan_coverage, scan_aggregates, scan_segments

EXPORTS_DIR = Path("data/exports")
REPORTS_DIR = Path("reports")
CLEANED_DIR = Path("data/cleaned")

PRECALL_PARQUET = CLEANED_DIR / "fct_campaign_precall_targeting.parquet"
OPERATIONAL_PARQUET = CLEANED_DIR / "fct_campaign_full_operational.parquet"
BENCHMARK_PARQUET = CLEANED_DIR / "fct_legacy_balance_benchmark.parquet"


@pytest.fixture(scope="session")
def channel_csv():
    path = EXPORTS_DIR / "segment_channel.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def demographics_csv():
    path = EXPORTS_DIR / "segment_demographics.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def poutcome_csv():
    path = EXPORTS_DIR / "segment_poutcome.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def macro_csv():
    path = EXPORTS_DIR / "segment_macro.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def financial_csv():
    path = EXPORTS_DIR / "segment_financial_profile.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def fatigue_csv():
    path = EXPORTS_DIR / "contact_fatigue_curve.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def labor_csv():
    path = EXPORTS_DIR / "operational_labor_audit.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def coverage_csv():
    path = EXPORTS_DIR / "coverage_profiling.csv"
    assert path.is_file(), f"Missing export: {path}"
    return pd.read_csv(path)


def test_conservation_of_volume(channel_csv, demographics_csv, poutcome_csv, macro_csv):
    """
    Verification Gate 1: Conservation of Volume.
    Every 1D segment table (contact, age_bucket, job_collar_tier, poutcome, euribor_regime)
    must sum to exactly 41,188 leads, 105,754 dialed calls, and 4,640 subscriptions.
    """
    dimension_tables = [
        ("contact", channel_csv),
        ("age_bucket", demographics_csv),
        ("job_collar_tier", demographics_csv),
        ("poutcome", poutcome_csv),
        ("euribor_regime", macro_csv),
    ]

    for dim_name, df in dimension_tables:
        sub_df = df[df["segment_dimension"] == dim_name]
        assert not sub_df.empty, f"Dimension '{dim_name}' not found in segment table"

        lead_sum = int(sub_df["lead_count"].sum())
        call_sum = int(sub_df["total_calls"].sum())
        sub_sum = int(sub_df["subscriptions"].sum())

        assert lead_sum == 41188, f"{dim_name}: Expected 41,188 leads, got {lead_sum}"
        assert call_sum == 105754, f"{dim_name}: Expected 105,754 calls, got {call_sum}"
        assert sub_sum == 4640, f"{dim_name}: Expected 4,640 subscriptions, got {sub_sum}"


def test_fatigue_cliff_verification(fatigue_csv):
    """
    Verification Gate 2: Fatigue Cliff Verification.
    Touches 1-3 capture 4,085 subscriptions (88.04% >= 85.0% Guardrail 2) at 12.17% conversion
    and 7.45% dialing efficiency.
    Touches 4+ drop to 7.27% conversion (< 8.0% Guardrail 1) and 1.09% dialing efficiency
    while consuming 50,949 calls (48.18%).
    """
    # Baseline: Touches 1-3
    baseline_rows = fatigue_csv[fatigue_csv["touch_count"].isin(["1", "2", "3", 1, 2, 3])]
    b_leads = int(baseline_rows["exact_prospect_count"].sum())
    b_calls = int(baseline_rows["dialed_calls"].sum())
    b_subs = int(baseline_rows["subscriptions"].sum())

    b_conv = (b_subs / b_leads) * 100.0
    b_eff = (b_subs / b_calls) * 100.0
    b_sub_share = (b_subs / 4640) * 100.0
    b_call_share = (b_calls / 105754) * 100.0

    assert b_leads == 33553, f"Expected 33,553 baseline leads, got {b_leads}"
    assert b_calls == 54805, f"Expected 54,805 baseline calls, got {b_calls}"
    assert b_subs == 4085, f"Expected 4,085 baseline subs, got {b_subs}"
    assert pytest.approx(b_conv, abs=0.01) == 12.17
    assert pytest.approx(b_eff, abs=0.01) == 7.45
    assert pytest.approx(b_sub_share, abs=0.01) == 88.04
    assert b_sub_share >= 85.0, f"Guardrail 2 breach: expected >= 85.0%, got {b_sub_share:.2f}%"
    assert pytest.approx(b_call_share, abs=0.01) == 51.82

    # Fatigue Zone: Touches 4+
    fatigue_rows = fatigue_csv[~fatigue_csv["touch_count"].isin(["1", "2", "3", 1, 2, 3])]
    f_leads = int(fatigue_rows["exact_prospect_count"].sum())
    f_calls = int(fatigue_rows["dialed_calls"].sum())
    f_subs = int(fatigue_rows["subscriptions"].sum())

    f_conv = (f_subs / f_leads) * 100.0
    f_eff = (f_subs / f_calls) * 100.0
    f_sub_share = (f_subs / 4640) * 100.0
    f_call_share = (f_calls / 105754) * 100.0

    assert f_leads == 7635, f"Expected 7,635 fatigue leads, got {f_leads}"
    assert f_calls == 50949, f"Expected 50,949 fatigue calls, got {f_calls}"
    assert f_subs == 555, f"Expected 555 fatigue subs, got {f_subs}"
    assert pytest.approx(f_conv, abs=0.01) == 7.27
    assert f_conv < 8.0, f"Guardrail 1 check failed: expected < 8.0%, got {f_conv:.2f}%"
    assert pytest.approx(f_eff, abs=0.01) == 1.09
    assert pytest.approx(f_call_share, abs=0.01) == 48.18
    assert pytest.approx(f_sub_share, abs=0.01) == 11.96

    # 6.8x efficiency collapse verification
    efficiency_drop_ratio = b_eff / f_eff
    assert efficiency_drop_ratio > 6.5, f"Expected > 6.5x efficiency collapse, got {efficiency_drop_ratio:.2f}x"


def test_channel_multiplier_verification(channel_csv):
    """
    Verification Gate 3: Channel Multiplier Verification.
    Cellular conversion rate (14.74%) is > 2.5x telephone conversion rate (5.23%).
    """
    cell_row = channel_csv[
        (channel_csv["segment_dimension"] == "contact")
        & (channel_csv["segment_value"] == "cellular")
    ].iloc[0]

    tel_row = channel_csv[
        (channel_csv["segment_dimension"] == "contact")
        & (channel_csv["segment_value"] == "telephone")
    ].iloc[0]

    cell_conv = float(cell_row["conversion_rate_pct"])
    tel_conv = float(tel_row["conversion_rate_pct"])

    assert pytest.approx(cell_conv, abs=0.01) == 14.74
    assert pytest.approx(tel_conv, abs=0.01) == 5.23
    assert cell_conv > (2.5 * tel_conv), (
        f"Cellular ({cell_conv:.2f}%) is not > 2.5x Telephone ({tel_conv:.2f}%)"
    )


def test_demographic_and_prior_outcome_lift(demographics_csv, poutcome_csv):
    """
    Verification Gate 4: Demographic & Prior-Outcome Lift.
    Senior/Retired (60+) conversion exceeds 40.0% (45.49%).
    Core Working (31-45) conversion is below 10.0% (9.37%).
    poutcome == 'success' conversion exceeds 60.0% (65.11%).
    """
    senior_row = demographics_csv[
        (demographics_csv["segment_dimension"] == "age_bucket")
        & (demographics_csv["segment_value"] == "4. Senior/Retired (60+)")
    ].iloc[0]

    core_row = demographics_csv[
        (demographics_csv["segment_dimension"] == "age_bucket")
        & (demographics_csv["segment_value"] == "2. Core Working (31-45)")
    ].iloc[0]

    succ_row = poutcome_csv[
        (poutcome_csv["segment_dimension"] == "poutcome")
        & (poutcome_csv["segment_value"] == "success")
    ].iloc[0]

    senior_conv = float(senior_row["conversion_rate_pct"])
    core_conv = float(core_row["conversion_rate_pct"])
    succ_conv = float(succ_row["conversion_rate_pct"])

    assert senior_conv > 40.0, f"Senior conversion below 40%: {senior_conv:.2f}%"
    assert pytest.approx(senior_conv, abs=0.01) == 45.49

    assert core_conv < 10.0, f"Core working conversion above 10%: {core_conv:.2f}%"
    assert pytest.approx(core_conv, abs=0.01) == 9.37

    assert succ_conv > 60.0, f"Prior success conversion below 60%: {succ_conv:.2f}%"
    assert pytest.approx(succ_conv, abs=0.01) == 65.11


def test_macroeconomic_elasticity(macro_csv):
    """
    Verification Gate 5: Macroeconomic Elasticity.
    Low Rate Regime (Euribor <= 3.0%) conversion rate (24.46%) is > 4.5x
    High Rate Regime (Euribor > 3.0%) conversion rate (4.84%).
    """
    low_rate_row = macro_csv[
        (macro_csv["segment_dimension"] == "euribor_regime")
        & (macro_csv["segment_value"] == "Low Rate Regime (Euribor <= 3.0%)")
    ].iloc[0]

    high_rate_row = macro_csv[
        (macro_csv["segment_dimension"] == "euribor_regime")
        & (macro_csv["segment_value"] == "High Rate Regime (Euribor > 3.0%)")
    ].iloc[0]

    low_conv = float(low_rate_row["conversion_rate_pct"])
    high_conv = float(high_rate_row["conversion_rate_pct"])

    assert pytest.approx(low_conv, abs=0.01) == 24.46
    assert pytest.approx(high_conv, abs=0.01) == 4.84
    assert low_conv > (4.5 * high_conv), (
        f"Low rate conv ({low_conv:.2f}%) is not > 4.5x high rate conv ({high_conv:.2f}%)"
    )


def test_leakage_quarantine_integrity():
    """
    Verification Gate 6: Leakage Quarantine Integrity.
    Confirms scan_segments.py and scan_coverage.py load strictly from
    fct_campaign_precall_targeting.parquet with zero duration leakage,
    and never touch the operational table containing post-call duration leakage.
    """
    # 1. Assert pre-call parquet has no duration or duration_minutes
    df_pre = pd.read_parquet(PRECALL_PARQUET)
    assert "duration" not in df_pre.columns, "Leakage: duration found in precall parquet"
    assert "duration_minutes" not in df_pre.columns, "Leakage: duration_minutes found in precall parquet"

    # 2. Test scan_coverage loader enforces zero duration
    cov_df = scan_coverage.load_precall_targeting()
    assert "duration" not in cov_df.columns
    assert "duration_minutes" not in cov_df.columns

    # 3. Test scan_segments loader enforces zero duration on precall
    seg_pre_df, _ = scan_segments.load_datasets()
    assert "duration" not in seg_pre_df.columns
    assert "duration_minutes" not in seg_pre_df.columns

    # 4. Source code inspection ensuring no operational table usage in targeting scripts
    cov_src = inspect.getsource(scan_coverage)
    seg_src = inspect.getsource(scan_segments)

    assert "fct_campaign_full_operational.parquet" not in cov_src, (
        "Quarantine breach: scan_coverage.py references operational parquet!"
    )
    assert "fct_campaign_full_operational.parquet" not in seg_src, (
        "Quarantine breach: scan_segments.py references operational parquet!"
    )
    assert "OPERATIONAL_PARQUET_FILE" not in cov_src
    assert "OPERATIONAL_PARQUET_FILE" not in seg_src


def test_operational_labor_reconciliation(labor_csv):
    """
    Validates operational labor audit metrics from operational table.
    """
    total_hours = labor_csv.loc[labor_csv["metric"] == "Total Hours", "value"].values[0]
    total_minutes = labor_csv.loc[labor_csv["metric"] == "Total Minutes", "value"].values[0]
    base_min_sub = labor_csv.loc[
        (labor_csv["dimension"] == "Baseline Cohort (Touches 1-3)")
        & (labor_csv["metric"] == "Agent Minutes Per Subscription"),
        "value",
    ].values[0]
    fatigue_min_sub = labor_csv.loc[
        (labor_csv["dimension"] == "Fatigue Zone (Touches 4+)")
        & (labor_csv["metric"] == "Agent Minutes Per Subscription"),
        "value",
    ].values[0]

    assert pytest.approx(total_hours, abs=0.1) == 2955.07
    assert pytest.approx(total_minutes, abs=0.1) == 177304.05
    assert pytest.approx(base_min_sub, abs=0.01) == 36.42
    assert pytest.approx(fatigue_min_sub, abs=0.01) == 51.37


def test_coverage_and_deduplication_sensitivity(coverage_csv):
    """
    Validates pre-call column completeness and deduplication sensitivity.
    """
    assert len(coverage_csv) == 34
    pdays_clean_row = coverage_csv[coverage_csv["column_name"] == "pdays_clean"].iloc[0]
    assert pdays_clean_row["null_count"] == 39673
    assert pdays_clean_row["null_pct"] == 96.32

    other_cols = coverage_csv[coverage_csv["column_name"] != "pdays_clean"]
    assert (other_cols["null_count"] == 0).all()
