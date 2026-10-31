"""
tests/test_scan_analytics.py
Phase 2 / SCAN Analytics Automated Test Suite
Framework: Christine Jiang SCAN Framework Verification

Tests:
  - Task 2.1: S & C - Stakeholder Alignment & Coverage Profiling
  - Task 2.2: A - Aggregates & Anomalies Auditing
  - Task 2.3: N - Notable Segments Profiling
"""

from pathlib import Path
import pytest
import pandas as pd
import numpy as np


REPORTS_DIR = Path("reports")
EXPORTS_DIR = Path("data/exports")
DATA_DIR = Path("data/cleaned")

COVERAGE_REPORT = REPORTS_DIR / "coverage_summary.md"
AGGREGATES_REPORT = REPORTS_DIR / "scan_aggregates_summary.md"
SEGMENTS_REPORT = REPORTS_DIR / "notable_segments_summary.md"

COVERAGE_CSV = EXPORTS_DIR / "coverage_profiling.csv"
PORTFOLIO_AGG_CSV = EXPORTS_DIR / "portfolio_aggregates.csv"
ACTIVE_EXP_CSV = EXPORTS_DIR / "active_portfolio_exposure.csv"
GRADE_CSV = EXPORTS_DIR / "segment_grade.csv"
SUBGRADE_CSV = EXPORTS_DIR / "segment_subgrade.csv"
TERM_CSV = EXPORTS_DIR / "segment_term.csv"
PURPOSE_CSV = EXPORTS_DIR / "segment_purpose.csv"
RISK_GRID_CSV = EXPORTS_DIR / "segment_risk_grid.csv"


# -------------------------------------------------------------------------
# Test Artifacts and Files Existence
# -------------------------------------------------------------------------
def test_scan_reports_and_exports_exist():
    """Verify all Markdown reports and CSV export deliverables exist with content."""
    reports = [COVERAGE_REPORT, AGGREGATES_REPORT, SEGMENTS_REPORT]
    for r in reports:
        assert r.exists(), f"Missing report: {r}"
        assert r.stat().st_size > 500, f"Report {r} appears truncated or empty."

    exports = [
        COVERAGE_CSV,
        PORTFOLIO_AGG_CSV,
        ACTIVE_EXP_CSV,
        GRADE_CSV,
        SUBGRADE_CSV,
        TERM_CSV,
        PURPOSE_CSV,
        RISK_GRID_CSV,
    ]
    for e in exports:
        assert e.exists(), f"Missing export: {e}"
        assert e.stat().st_size > 100, f"Export {e} appears empty."


# -------------------------------------------------------------------------
# Test Task 2.1: Coverage & Stakeholder Alignment
# -------------------------------------------------------------------------
def test_coverage_profiling_completeness():
    """Verify coverage profiling covers all 162 features and has 0 unexpected nulls."""
    cov_df = pd.read_csv(COVERAGE_CSV)
    assert len(cov_df) == 162, f"Expected 162 columns profiled, got {len(cov_df)}"

    # Engineered columns check
    eng_features = [
        "is_bad_loan",
        "net_cash_flow",
        "laroc",
        "fico_midpoint",
        "vintage_year",
        "dti_bracket",
        "revol_util_bracket",
    ]
    for feat in eng_features:
        row = cov_df[cov_df["column_name"] == feat]
        assert not row.empty, f"Feature {feat} missing from coverage profile"
        if feat in ["is_bad_loan", "net_cash_flow", "laroc", "fico_midpoint", "vintage_year"]:
            assert row["null_records"].values[0] == 0, f"Engineered column {feat} has unexpected nulls!"

    # DTI Bracket nulls must match invalid_dti_flag exactly (376 rows)
    dti_row = cov_df[cov_df["column_name"] == "dti_bracket"]
    assert dti_row["null_records"].values[0] == 376, f"Expected 376 nulls in dti_bracket, got {dti_row['null_records'].values[0]}"


# -------------------------------------------------------------------------
# Test Task 2.2: Aggregates & Dispersion Statistics
# -------------------------------------------------------------------------
def test_dispersion_statistics_monotonicity():
    """Verify that quantile order holds across dispersion statistics: P25 <= Median <= P75 <= P90 <= P99."""
    disp_df = pd.read_csv(PORTFOLIO_AGG_CSV)
    assert len(disp_df) == 7, f"Expected 7 features profiled in aggregates, got {len(disp_df)}"

    for _, row in disp_df.iterrows():
        p25 = row["p25"]
        med = row["median"]
        p75 = row["p75"]
        p90 = row["p90"]
        p99 = row["p99"]
        iqr = row["iqr"]

        assert p25 <= med <= p75 <= p90 <= p99, f"Quantile monotonicity violated for {row['feature']}"
        np.testing.assert_allclose(iqr, p75 - p25, rtol=1e-5, atol=1e-4)


def test_active_portfolio_exposure_reconciliation():
    """Verify active portfolio exposures reconcile with the active cohort."""
    act_df = pd.read_csv(ACTIVE_EXP_CSV)
    total_active_vol = act_df["volume"].sum()
    assert total_active_vol == 912569, f"Unexpected active loan count: {total_active_vol}"

    expected_statuses = {"Current", "In Grace Period", "Late (16-30 days)", "Late (31-120 days)"}
    assert set(act_df["loan_status"]).issubset(expected_statuses)

    total_active_funded = act_df["total_funded"].sum()
    assert 14_000_000_000 < total_active_funded < 15_000_000_000, f"Unexpected active balance: {total_active_funded}"


# -------------------------------------------------------------------------
# Test Task 2.3: Notable Segments
# -------------------------------------------------------------------------
def test_grade_and_subgrade_segmentation():
    """Verify Grade and Subgrade segmentation integrity and threshold inflections."""
    grade_df = pd.read_csv(GRADE_CSV)
    assert len(grade_df) == 7, "Expected 7 loan grades (A through G)"
    assert grade_df["volume"].sum() == 1345350, "Total grade volume must equal 1,345,350 seasoned loans"

    # Terminal bad rate monotonicity: increases across grades
    bad_rates = grade_df["terminal_bad_rate_pct"].tolist()
    assert bad_rates[0] < bad_rates[1] < bad_rates[2] < bad_rates[3] < bad_rates[4] < bad_rates[5] < bad_rates[6], (
        "Expected monotonically increasing bad rates from Grade A to G"
    )

    subgrade_df = pd.read_csv(SUBGRADE_CSV)
    assert len(subgrade_df) == 35, "Expected 35 subgrades (A1 through G5)"
    assert subgrade_df["volume"].sum() == 1345350, "Total subgrade volume must equal 1,345,350"

    # Subgrade crossing 20% bad rate must be C2
    sub_20 = subgrade_df[subgrade_df["terminal_bad_rate_pct"] >= 20.0].iloc[0]
    assert sub_20["sub_grade"] == "C2", f"Expected C2 to cross 20% bad rate, got {sub_20['sub_grade']}"

    # Subgrade median LAROC < 4.0% must be G4
    sub_laroc_4 = subgrade_df[subgrade_df["median_laroc"] < 4.0].iloc[0]
    assert sub_laroc_4["sub_grade"] == "G4", f"Expected G4 for median LAROC < 4%, got {sub_laroc_4['sub_grade']}"


def test_term_segmentation():
    """Verify 36-month vs 60-month term segmentation metrics."""
    term_df = pd.read_csv(TERM_CSV)
    assert len(term_df) == 2, "Expected 2 term categories (36 and 60)"
    assert term_df["volume"].sum() == 1345350, "Total term volume must equal 1,345,350"

    t36 = term_df[term_df["term"] == 36].iloc[0]
    t60 = term_df[term_df["term"] == 60].iloc[0]

    # 60-month default rate is more than double 36-month default rate
    assert t60["terminal_bad_rate_pct"] > 30.0, f"Expected 60-month bad rate > 30%, got {t60['terminal_bad_rate_pct']:.2f}%"
    assert t36["terminal_bad_rate_pct"] < 20.0, f"Expected 36-month bad rate < 20%, got {t36['terminal_bad_rate_pct']:.2f}%"
    assert t60["terminal_bad_rate_pct"] / t36["terminal_bad_rate_pct"] > 2.0


def test_purpose_segmentation():
    """Verify purpose segmentation and small_business toxicity."""
    purp_df = pd.read_csv(PURPOSE_CSV)
    assert purp_df["volume"].sum() == 1345350, "Total purpose volume must equal 1,345,350"

    sb = purp_df[purp_df["purpose"] == "small_business"].iloc[0]
    assert sb["terminal_bad_rate_pct"] > 28.0, f"Small business bad rate too low: {sb['terminal_bad_rate_pct']:.2f}%"
    assert sb["cohort_laroc_pct"] < 0.0, f"Small business cohort LAROC must be negative: {sb['cohort_laroc_pct']:.2f}%"


def test_risk_grid_segmentation():
    """Verify 2D Risk Grid has 16 cells and high-risk intersection metrics."""
    grid_df = pd.read_csv(RISK_GRID_CSV)
    assert len(grid_df) == 16, f"Expected 16 risk grid cells, got {len(grid_df)}"

    total_grid_vol = grid_df["volume"].sum()
    assert total_grid_vol == 1344118, f"Expected 1,344,118 complete grid loans, got {total_grid_vol}"

    # High-Risk Intersection cells: High DTI & Severe DTI combined with High Revol & Maxed Revol
    hr_cells = grid_df[
        grid_df["dti_bracket"].isin(["3. High (25-35%)", "4. Severe (>35%)"])
        & grid_df["revol_util_bracket"].isin(["3. High (65-85%)", "4. Maxed (>85%)"])
    ]
    assert len(hr_cells) == 4, f"Expected 4 high risk cells, got {len(hr_cells)}"
    hr_vol = hr_cells["volume"].sum()
    hr_bad = hr_cells["bad_count"].sum()
    hr_bad_rate = (hr_bad / hr_vol) * 100.0

    assert hr_vol == 112246, f"Expected 112,246 high risk loans, got {hr_vol}"
    assert 28.0 <= hr_bad_rate <= 29.0, f"Expected ~28.4% bad rate, got {hr_bad_rate:.2f}%"
