"""
Tests for Phase 4: Executive Dashboard (The DASH Framework Implementation)
===========================================================================
Validates:
  - Dataset loading and caching
  - The 4 Core KPI calculations (Spend, Wedge, Claims, Outlier Risk Index)
  - Interactive filter behaviors (Year, Therapeutic Class, Outlier Toggle)
  - Visual figure builders (Pareto, Lorenz, Quadrant Scatter)
  - Actionable Formulary Grid structure and CSV export capability
  - Headless Streamlit AppTest execution without exceptions
"""

from __future__ import annotations

import io
import pytest
import pandas as pd
import numpy as np

import src.dashboard.app as app


@pytest.fixture(scope="module")
def datasets():
    df_overall, df_detail = app.load_datasets()
    return df_overall, df_detail


def test_load_datasets(datasets):
    df_overall, df_detail = datasets
    assert not df_overall.empty
    assert not df_detail.empty
    assert len(df_overall) == 4774
    assert len(df_detail) == 13737
    assert "Tot_Spndng_2024" in df_overall.columns
    assert "Outlier_Flag_2024" in df_overall.columns
    assert "Avg_Spnd_Per_Dsg_Unt_Wghtd_2024" in df_detail.columns


def test_kpis_default_cy2024(datasets):
    df_overall, df_detail = datasets
    kpis = app.compute_kpis(df_overall, df_detail, year=2024, exclude_outliers=False)

    # 1. Gross Spend: ~$111.3B (+45.6% 5-Yr Growth)
    assert np.isclose(kpis["tot_spend"], 111_276_419_160.83, rtol=1e-4)
    assert np.isclose(kpis["spend_5yr_pct"], 45.606, rtol=1e-2)

    # 2. Avoidable Spend Wedge: ~$10.97B across 1,170 brand medications
    assert np.isclose(kpis["total_wedge"], 10_970_540_617.66, rtol=1e-3)
    assert kpis["wedge_drug_count"] == 1170

    # 3. Prescription Claim Volume: ~745.6M (-4.6% YoY vs 2023)
    assert kpis["tot_claims"] == 745_555_715
    assert np.isclose(kpis["claims_yoy_pct"], -4.613, rtol=1e-2)

    # 4. Outlier Risk Distortion Index: ~8.16%
    assert np.isclose(kpis["outlier_risk_pct"], 8.163, rtol=1e-2)
    assert kpis["outlier_records_count"] == 1738
    assert not kpis["exclude_outliers_active"]


def test_kpis_exclude_outliers_sensitivity(datasets):
    df_overall, df_detail = datasets
    kpis_filtered = app.compute_kpis(df_overall, df_detail, year=2024, exclude_outliers=True)

    # When outliers are excluded:
    # Spend drops by ~$9.08B (from $111.3B to ~$102.2B)
    assert kpis_filtered["tot_spend"] < 111_276_419_160.83
    assert np.isclose(kpis_filtered["tot_spend"], 102_192_997_660.25, rtol=1e-3)
    assert kpis_filtered["exclude_outliers_active"] is True
    # Wedge recalculates without outlier dosage noise
    assert kpis_filtered["total_wedge"] > 0
    assert kpis_filtered["total_wedge"] < 10_970_540_617.66


def test_kpis_therapeutic_filtering(datasets):
    df_overall, df_detail = datasets
    selected = ["Antidiabetic / GLP-1"]
    kpis = app.compute_kpis(
        df_overall,
        df_detail,
        year=2024,
        exclude_outliers=False,
        selected_classes=selected,
    )
    # GLP-1 / Antidiabetics represent a multi-billion dollar subset
    assert kpis["tot_spend"] > 10_000_000_000
    assert kpis["tot_spend"] < 111_276_419_160.83
    assert kpis["wedge_drug_count"] > 0


def test_kpis_historical_years(datasets):
    df_overall, df_detail = datasets
    for yr in [2020, 2021, 2022, 2023, 2024]:
        k = app.compute_kpis(df_overall, df_detail, year=yr, exclude_outliers=False)
        assert k["tot_spend"] > 50_000_000_000
        assert k["tot_claims"] > 500_000_000
        assert k["total_wedge"] > 0


def test_pareto_chart_builder(datasets):
    df_overall, _ = datasets
    fig = app.build_pareto_distribution_chart(df_overall, year=2024, exclude_outliers=False, top_n=20)
    assert len(fig.data) == 2  # 1 Bar trace + 1 Scatter line trace
    bar_trace = fig.data[0]
    line_trace = fig.data[1]
    assert len(bar_trace.x) == 20
    assert len(line_trace.y) == 20
    # Cumulative share should be monotonically increasing
    assert all(line_trace.y[i] <= line_trace.y[i + 1] for i in range(len(line_trace.y) - 1))


def test_lorenz_chart_builder(datasets):
    df_overall, _ = datasets
    fig = app.build_lorenz_curve_chart(df_overall, year=2024, exclude_outliers=False)
    assert len(fig.data) >= 2  # Equality line + Lorenz curve + cutoff marker
    equality_trace = fig.data[0]
    lorenz_trace = fig.data[1]
    assert equality_trace.x[0] == 0 and equality_trace.x[-1] == 1
    assert lorenz_trace.x[0] == pytest.approx(1 / 4774, rel=1e-2)
    assert lorenz_trace.y[-1] == pytest.approx(1.0, rel=1e-2)


def test_quadrant_chart_builder(datasets):
    df_overall, _ = datasets
    fig = app.build_quadrant_scatter_chart(df_overall, cohort_size=50)
    assert len(fig.data) >= 1
    # Check that annotations contain quadrant labels
    annotation_texts = [a.text for a in fig.layout.annotations]
    assert any("DUAL PRESSURE" in t for t in annotation_texts)
    assert any("PRICE ESCALATION" in t for t in annotation_texts)
    assert any("VOLUME DRIVEN" in t for t in annotation_texts)


def test_actionable_formulary_grid(datasets):
    df_overall, df_detail = datasets
    tbl = app.compute_formulary_action_table(df_overall, df_detail, year=2024, exclude_outliers=False)
    assert not tbl.empty
    expected_cols = [
        "Brand Name",
        "Generic Name",
        "Therapeutic Class",
        "Competing Manufacturers",
        "Current Unit Cost",
        "Lowest Generic Unit Cost",
        "Addressable Annual Savings ($)",
    ]
    for col in expected_cols:
        assert col in tbl.columns

    # Check sort order: must be strictly descending by savings
    assert (tbl["Addressable Annual Savings ($)"].diff().dropna() <= 0).all()

    # Check top drug
    top_drug = tbl.iloc[0]
    assert top_drug["Brand Name"] == "ABILIFY MAINTENA"
    assert top_drug["Addressable Annual Savings ($)"] > 800_000_000
    assert top_drug["Competing Manufacturers"] >= 10

    # Test CSV export buffer
    csv_buf = io.StringIO()
    tbl.to_csv(csv_buf, index=False)
    csv_content = csv_buf.getvalue()
    assert "ABILIFY MAINTENA" in csv_content
    assert "Addressable Annual Savings ($)" in csv_content


def test_apptest_headless_run():
    from pathlib import Path
    from streamlit.testing.v1 import AppTest
    app_path = (Path(__file__).resolve().parent.parent / "src" / "dashboard" / "app.py")
    at = AppTest.from_file(str(app_path))
    at.run(timeout=15)
    assert len(at.exception) == 0, f"Encountered unexpected exceptions: {at.exception}"
