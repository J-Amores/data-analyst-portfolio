"""
Unit & Integration Test Suite for Phase 2: SCAN EDA Pipeline
Tests src/analytics/eda_scan.py
"""

from pathlib import Path
import pytest
import pandas as pd
import numpy as np

from src.analytics.eda_scan import (
    PROJECT_ROOT,
    OVERALL_PARQUET_PATH,
    DETAIL_PARQUET_PATH,
    COVERAGE_REPORT_PATH,
    FIGURES_DIR,
    load_cleaned_data,
    calculate_topline_spend_trends,
    calculate_5yr_budget_shifts,
    calculate_distribution_metrics,
    calculate_outlier_impact,
    calculate_brand_generic_breakdown,
    calculate_therapeutic_class_breakdown,
    calculate_competitor_density,
    calculate_multisource_price_dispersion,
    calculate_avoidable_spend_wedge,
    audit_columns_and_coverage,
)


@pytest.fixture(scope="module")
def loaded_data():
    """Loads cleaned datasets once for the test module."""
    df_overall, df_detail = load_cleaned_data()
    return df_overall, df_detail


def test_data_loading_and_grain_integrity(loaded_data):
    """Verifies row counts, column counts, and Mftr_Name partitioning."""
    df_overall, df_detail = loaded_data

    assert len(df_overall) == 4774, f"Expected 4,774 overall rows, got {len(df_overall)}"
    assert len(df_detail) == 13737, f"Expected 13,737 detail rows, got {len(df_detail)}"

    # Grain partitioning assertions
    assert (df_overall["Mftr_Name"] == "OVERALL").all()
    assert not (df_detail["Mftr_Name"] == "OVERALL").any()

    # Column coverage
    assert len(df_overall.columns) == 43
    assert len(df_detail.columns) == 43


def test_topline_spend_reconciliation(loaded_data):
    """Verifies gross spend across benefit years 2020-2024 and 5-year budget shift metrics."""
    df_overall, df_detail = loaded_data

    df_topline = calculate_topline_spend_trends(df_overall)
    assert len(df_topline) == 5

    # Check 2024 spend values
    sp24_ov = float(df_overall["Tot_Spndng_2024"].sum())
    sp24_dt = float(df_detail["Tot_Spndng_2024"].sum())
    assert abs(sp24_ov - sp24_dt) < 1.0, "Overall and Detail 2024 spend mismatch"
    assert 1.10e11 < sp24_ov < 1.15e11, f"Expected ~111.3B, got {sp24_ov}"

    shifts = calculate_5yr_budget_shifts(df_topline)
    assert shifts["spend_growth_abs"] > 3.0e10  # > $30B growth
    assert 40.0 < shifts["spend_growth_pct"] < 50.0  # ~45.6%
    assert 9.0 < shifts["spend_cagr_pct"] < 11.0  # ~9.85% CAGR


def test_distribution_metrics(loaded_data):
    """Verifies distribution metrics for weighted unit cost and cost per claim."""
    df_overall, _ = loaded_data

    dist_df = calculate_distribution_metrics(df_overall)
    assert len(dist_df) == 2

    unit_row = dist_df[dist_df["metric"] == "Avg_Spnd_Per_Dsg_Unt_Wghtd_2024"].iloc[0]
    clm_row = dist_df[dist_df["metric"] == "Avg_Spnd_Per_Clm_2024"].iloc[0]

    # Extreme positive skewness verification: Mean >> Median
    assert unit_row["mean"] > unit_row["median"]
    assert unit_row["skewness"] > 0
    assert 5.0 < unit_row["median"] < 10.0  # Median is ~$6.40
    assert unit_row["iqr"] > 0

    assert clm_row["mean"] > clm_row["median"]
    assert 150.0 < clm_row["median"] < 250.0  # Median is ~$198.06
    assert clm_row["iqr"] > 500.0


def test_outlier_impact(loaded_data):
    """Verifies Outlier_Flag_2024 audit metrics."""
    df_overall, _ = loaded_data

    outlier_res = calculate_outlier_impact(df_overall)

    assert outlier_res["total_records"] == 4774
    assert outlier_res["flagged_count"] == 1738
    assert 30.0 < outlier_res["flagged_count_pct"] < 40.0  # ~36.41%

    # Flagged spend should be ~8.16%
    assert 7.0 < outlier_res["flagged_spend_pct"] < 10.0
    assert abs(outlier_res["flagged_spend"] + outlier_res["clean_spend"] - outlier_res["total_spend"]) < 1.0


def test_brand_vs_generic_concentration(loaded_data):
    """Verifies Brand vs Generic asymmetry: Brand absorbs 90%+ spend on 33% claims."""
    df_overall, _ = loaded_data

    bg_df = calculate_brand_generic_breakdown(df_overall)
    brand_row = bg_df[bg_df["segment"] == "Brand"].iloc[0]
    gen_row = bg_df[bg_df["segment"] == "Generic"].iloc[0]

    assert 88.0 < brand_row["spend_share_2024"] < 92.0  # ~90.19%
    assert 30.0 < brand_row["claim_share_2024"] < 36.0  # ~33.00%
    assert 64.0 < gen_row["claim_share_2024"] < 70.0  # ~67.00%
    assert 8.0 < gen_row["spend_share_2024"] < 12.0  # ~9.81%

    # Ratio of cost per claim
    ratio = brand_row["avg_cost_per_clm_2024"] / gen_row["avg_cost_per_clm_2024"]
    assert 15.0 < ratio < 22.0  # ~18.7x


def test_top_therapeutic_classes(loaded_data):
    """Verifies therapeutic indication class ranking and concentration."""
    df_overall, _ = loaded_data

    therap_df = calculate_therapeutic_class_breakdown(df_overall)
    assert len(therap_df) >= 10

    # Top specific classes should include CNS, Antidiabetic / GLP-1, Immunology
    top3_names = therap_df.head(4)["therapeutic_class_macro"].tolist()
    assert any("Antidiabetic" in n for n in top3_names)
    assert any("Immunology" in n for n in top3_names)
    assert any("Central Nervous System" in n for n in top3_names)


def test_avoidable_spend_wedge_calculation(loaded_data):
    """Verifies North Star Avoidable Brand-to-Generic Spend Wedge calculation."""
    df_overall, df_detail = loaded_data

    wedge_df, summary = calculate_avoidable_spend_wedge(df_overall, df_detail)
    assert len(wedge_df) > 500  # Over 1,000 brand drugs with generic equivalents
    assert summary["total_avoidable_spend_wedge"] > 1.0e10  # Over $10 Billion addressable
    assert summary["affected_brand_drugs_count"] == len(wedge_df)


def test_multisource_price_dispersion(loaded_data):
    """Verifies price dispersion across multi-source generic drugs."""
    df_overall, df_detail = loaded_data

    disp_df, summary = calculate_multisource_price_dispersion(df_overall, df_detail)
    assert summary["multi_source_generic_drugs_count"] == 760
    assert summary["median_price_ratio_max_min"] > 5.0  # At least 5x price multiple
    assert summary["median_cv_pct"] > 50.0  # Significant coefficient of variation


def test_coverage_audit_and_report_generation(loaded_data):
    """Verifies audit results and existence of reports/coverage_summary.md."""
    df_overall, df_detail = loaded_data

    audit = audit_columns_and_coverage(df_overall, df_detail)
    assert audit["overall_records_with_hipaa_flag"] == 1065
    assert (audit["suppression_audit"].loc[audit["suppression_audit"]["year"] == 2024, "overall_suppressed_cells"] == 0).all()

    assert COVERAGE_REPORT_PATH.exists()
    assert COVERAGE_REPORT_PATH.stat().st_size > 1000


def test_figure_artifacts_exist():
    """Verifies that all required figure artifacts exist in PNG and HTML formats."""
    expected_figures = [
        "brand_vs_generic_market_share.png",
        "brand_vs_generic_market_share.html",
        "top10_therapeutic_classes_spend.png",
        "top10_therapeutic_classes_spend.html",
        "generic_price_dispersion_single_vs_multi.png",
        "generic_price_dispersion_single_vs_multi.html",
        "medicaid_spend_trend_2020_2024.png",
        "medicaid_spend_trend_2020_2024.html",
    ]

    for fname in expected_figures:
        fpath = FIGURES_DIR / fname
        assert fpath.exists(), f"Missing figure file: {fname}"
        assert fpath.stat().st_size > 0, f"Figure file is empty: {fname}"
