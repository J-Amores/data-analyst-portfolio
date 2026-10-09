"""
Unit tests for Phase 3: Statistical Hypothesis Validation & Econometric Decomposition
Tests cover:
- Task 3.1: H1 Pareto Spend Concentration & Lorenz Curve (Gini, exact cutoffs, KS test)
- Task 3.2: H2 Logarithmic Price-Volume Growth Decomposition & Paired Tests
- Task 3.3: H3 Multi-Source Price Spread & State MAC Reimbursement Simulation
- Output artifacts verification (PNG and HTML visuals)
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.analytics.test_h1_pareto import (
    compute_gini_coefficient,
    compute_cumulative_spend_distribution,
    calculate_pareto_thresholds,
    test_h1_cost_concentration as run_h1_cost_concentration_test,
    OVERALL_PARQUET_PATH,
    OUTPUT_PNG_PATH as H1_PNG,
    OUTPUT_HTML_PATH as H1_HTML,
)
from src.analytics.test_h2_decomposition import (
    prepare_longitudinal_data,
    compute_log_decomposition,
    classify_spend_surge_drivers,
    run_paired_growth_test,
    test_h2_price_volume_hypothesis as run_h2_price_volume_test,
    OUTPUT_PNG_PATH as H2_PNG,
    OUTPUT_HTML_PATH as H2_HTML,
)
from src.analytics.test_h3_price_spread import (
    isolate_multisource_drugs,
    calculate_manufacturer_price_dispersion,
    simulate_state_mac_savings,
    test_h3_price_spread_hypothesis as run_h3_price_spread_test,
    DETAIL_PARQUET_PATH,
    OUTPUT_PNG_PATH as H3_PNG,
    OUTPUT_HTML_PATH as H3_HTML,
)


@pytest.fixture(scope="module")
def df_overall():
    """Loads cleaned drug overall parquet dataset."""
    assert OVERALL_PARQUET_PATH.exists(), f"Missing {OVERALL_PARQUET_PATH}"
    return pd.read_parquet(OVERALL_PARQUET_PATH)


@pytest.fixture(scope="module")
def df_detail():
    """Loads cleaned manufacturer detail parquet dataset."""
    assert DETAIL_PARQUET_PATH.exists(), f"Missing {DETAIL_PARQUET_PATH}"
    return pd.read_parquet(DETAIL_PARQUET_PATH)


# =============================================================================
# Task 3.1 (H1: Pareto Spend Concentration) Unit Tests
# =============================================================================
class TestHypothesis1Pareto:
    """Verifies H1 calculations, Lorenz properties, and statistical test outputs."""

    def test_gini_coefficient_synthetic(self):
        """Tests Gini coefficient properties on theoretical distributions."""
        # Perfectly equal distribution
        equal_vals = np.ones(100) * 50.0
        assert compute_gini_coefficient(equal_vals) == pytest.approx(0.0, abs=1e-4)

        # Extremely concentrated distribution (1 person has almost everything)
        concentrated = np.zeros(1000)
        concentrated[-1] = 1_000_000.0
        gini_conc = compute_gini_coefficient(concentrated)
        assert gini_conc > 0.99

        # Empty / zero case
        assert compute_gini_coefficient(np.array([])) == 0.0
        assert compute_gini_coefficient(np.zeros(10)) == 0.0

    def test_gini_coefficient_empirical(self, df_overall):
        """Verifies Gini on CY2024 gross spend indicates extreme concentration (0.9028)."""
        gini = compute_gini_coefficient(df_overall["Tot_Spndng_2024"])
        assert 0.88 <= gini <= 0.93
        assert np.isclose(gini, 0.9028, atol=1e-3)

    def test_pareto_exact_threshold_counts(self, df_overall):
        """Verifies exact drug counts for 50%, 65%, and 80% cumulative spend thresholds."""
        df_cum = compute_cumulative_spend_distribution(df_overall)
        assert len(df_cum) == 4774
        assert df_cum["cum_spend_share"].iloc[-1] == pytest.approx(1.0, abs=1e-5)

        thresholds = calculate_pareto_thresholds(df_cum, [0.50, 0.65, 0.80])
        t = thresholds["thresholds"]

        # Exact drug counts verified empirically:
        # 50% spend reached at drug 75 (1.57%)
        assert t["50pct"]["drug_count"] == 75
        assert np.isclose(t["50pct"]["drug_share_pct"], 1.57, atol=0.05)
        assert t["50pct"]["achieved_spend_share"] >= 0.50

        # 65% spend reached at drug 165 (3.46%)
        assert t["65pct"]["drug_count"] == 165
        assert np.isclose(t["65pct"]["drug_share_pct"], 3.46, atol=0.05)
        assert t["65pct"]["achieved_spend_share"] >= 0.65

        # 80% spend reached at drug 361 (7.56%)
        assert t["80pct"]["drug_count"] == 361
        assert np.isclose(t["80pct"]["drug_share_pct"], 7.56, atol=0.05)
        assert t["80pct"]["achieved_spend_share"] >= 0.80

        # Top 5% share exceeds the 60% decision threshold
        assert thresholds["top_5pct"]["share_of_spend"] > 0.70
        assert np.isclose(thresholds["top_5pct"]["share_of_spend"], 0.7218, atol=0.01)

    def test_lorenz_monotonicity_and_bounds(self, df_overall):
        """Verifies that the cumulative spend distribution is strictly monotonically non-decreasing."""
        df_cum = compute_cumulative_spend_distribution(df_overall)
        cum_shares = df_cum["cum_spend_share"].values
        diffs = np.diff(cum_shares)
        assert (diffs >= 0).all(), "Cumulative spend share must be non-decreasing"
        assert cum_shares[0] > 0
        assert cum_shares[-1] == pytest.approx(1.0, abs=1e-6)

    def test_h1_statistical_verdict(self, df_overall):
        """Verifies that H0 is strongly rejected and KS test p-value < 0.001."""
        h1_res = run_h1_cost_concentration_test(df_overall)
        assert h1_res["h0_rejected"] is True
        assert "REJECT H0" in h1_res["verdict"]
        assert h1_res["ks_pvalue"] < 0.001
        assert h1_res["top_5pct_share"] > 0.60


# =============================================================================
# Task 3.2 (H2: Logarithmic Price-Volume Decomposition) Unit Tests
# =============================================================================
class TestHypothesis2Decomposition:
    """Verifies econometric log decomposition, surge classification, and paired statistical tests."""

    def test_longitudinal_filtering(self, df_overall):
        """Verifies isolation of drugs with complete positive longitudinal 5-year data."""
        df_valid = prepare_longitudinal_data(df_overall)
        assert len(df_valid) == 3762
        assert (df_valid["Tot_Spndng_2020"] > 0).all()
        assert (df_valid["Tot_Spndng_2024"] > 0).all()
        assert (df_valid["Avg_Spnd_Per_Dsg_Unt_Wghtd_2020"] > 0).all()
        assert (df_valid["Avg_Spnd_Per_Dsg_Unt_Wghtd_2024"] > 0).all()
        assert (df_valid["Tot_Clms_2020"] > 0).all()
        assert (df_valid["Tot_Clms_2024"] > 0).all()

    def test_log_decomposition_identity(self, df_overall):
        """Verifies econometric log identity: d_ln(Spend) ≈ d_ln(Price) + d_ln(Volume)."""
        df_valid = prepare_longitudinal_data(df_overall)
        df_decomp = compute_log_decomposition(df_valid)

        # For the median drug, the log unit cost + log dosage units equals log spend within precision
        diff = np.abs(df_decomp["d_ln_spend"] - (df_decomp["d_ln_price"] + df_decomp["d_ln_volume"]))
        # Median discrepancy should be close to 0
        assert diff.median() < 0.01

    def test_spend_surge_classification_categories(self, df_overall):
        """Verifies that all spend surges are partitioned into valid driver categories."""
        df_valid = prepare_longitudinal_data(df_overall)
        df_decomp = compute_log_decomposition(df_valid)
        df_classified = classify_spend_surge_drivers(df_decomp, volume_basis="claims")

        surges = df_classified[df_classified["spend_diff"] > 0]
        assert len(surges) == 1894

        valid_drivers = {"Volume-Driven", "Dual Pressure", "Price-Driven"}
        assert set(surges["surge_driver_claims"].unique()).issubset(valid_drivers)

        # Counts verified:
        counts = surges["surge_driver_claims"].value_counts()
        assert counts["Volume-Driven"] > 900
        assert counts["Dual Pressure"] > 350
        assert counts["Price-Driven"] > 400

    def test_paired_statistical_testing_top100(self, df_overall):
        """
        Verifies paired test between unit cost growth vs. claim volume growth across top 100 growth drugs.
        Confirms claim volume growth significantly outpaces price growth (p < 1e-10).
        """
        df_valid = prepare_longitudinal_data(df_overall)
        df_decomp = compute_log_decomposition(df_valid)
        df_classified = classify_spend_surge_drivers(df_decomp, volume_basis="claims")

        test_res = run_paired_growth_test(df_classified, top_n=100)
        assert test_res["top_n"] == 100
        assert np.isclose(test_res["total_net_spend_expansion"] / 1e9, 31.52, atol=0.1)

        # Wilcoxon and paired t-test results
        assert test_res["wilcoxon_pval_claims"] < 1e-10
        assert test_res["paired_t_pval_claims"] < 1e-10
        assert test_res["paired_t_stat_claims"] < 0  # Price growth is significantly less than claims growth

        # 88 drugs outpaced by claim volume
        assert test_res["claims_outpaced_price_count"] == 88
        assert test_res["price_outpaced_claims_count"] == 12

    def test_h2_statistical_verdict(self, df_overall):
        """Verifies that H0 is NOT rejected because growth is volume-driven."""
        h2_res = run_h2_price_volume_test(df_overall)
        assert "FAIL TO REJECT H0" in h2_res["verdict"]
        assert h2_res["price_dominates"] is False


# =============================================================================
# Task 3.3 (H3: Multi-Source Spread & State MAC Modeling) Unit Tests
# =============================================================================
class TestHypothesis3PriceSpread:
    """Verifies multi-source isolation, price dispersion metrics, and State MAC policy modeling."""

    def test_multisource_isolation(self, df_overall, df_detail):
        """Verifies multi-source drug filtering where Tot_Mftr >= 2."""
        ms_ov, ms_dt = isolate_multisource_drugs(df_overall, df_detail)
        assert len(ms_ov) == 1537
        assert len(ms_dt) == 10435  # active records with positive spend/units in 2024
        assert (ms_dt["Avg_Spnd_Per_Dsg_Unt_Wghtd_2024"] > 0).all()
        assert (ms_dt["Tot_Dsg_Unts_2024"] > 0).all()

    def test_dispersion_metrics_nonnegative(self, df_overall, df_detail):
        """Verifies that price dispersion metrics are non-negative and mathematically valid."""
        _, ms_dt = isolate_multisource_drugs(df_overall, df_detail)
        df_disp = calculate_manufacturer_price_dispersion(ms_dt)

        assert len(df_disp) == 1525
        assert (df_disp["iqr_price_spread"] >= 0).all()
        assert (df_disp["iqr_spread_pct"] >= 0).all()
        assert (df_disp["cv_pct"] >= 0).all()
        assert (df_disp["max_min_ratio"] >= 1.0).all()

    def test_mac_savings_simulation_properties(self, df_overall, df_detail):
        """Verifies State MAC P25 savings simulation logic and non-negativity."""
        _, ms_dt = isolate_multisource_drugs(df_overall, df_detail)
        df_mac, summary = simulate_state_mac_savings(ms_dt, percentile=0.25)

        assert len(df_mac) == 1525
        assert (df_mac["simulated_mac_savings"] >= 0).all()
        assert (df_mac["simulated_mac_savings"] <= df_mac["total_spend_2024"] + 1e-4).all()

        # Multi-source generic savings:
        assert summary["n_multisource_generic_drugs"] == 759
        assert summary["generic_baseline_spend"] > 1e10  # ~$10.74B
        assert summary["generic_mac_savings"] > 3e9      # ~$3.17B
        assert summary["generic_mac_savings_pct"] > 25.0 # ~29.5%

        # Dispersion thresholds
        assert summary["generic_median_iqr_spread_pct"] > 35.0 # 50.23% > 35%
        assert summary["generic_median_cv_pct"] > 10.0         # 78.28% > 10%

    def test_h3_statistical_verdict(self, df_overall, df_detail):
        """Verifies that H0 is strongly rejected and simulated savings > $100M."""
        h3_res = run_h3_price_spread_test(df_overall, df_detail)
        assert h3_res["h0_rejected"] is True
        assert "REJECT H0" in h3_res["verdict"]
        assert h3_res["wilcoxon_iqr_pval"] < 1e-15
        assert h3_res["mac_summary"]["generic_mac_savings"] > 1e8  # > $100M


# =============================================================================
# Visual Artifacts Existence & Integrity Tests
# =============================================================================
class TestVisualArtifacts:
    """Verifies that required publication PNG and HTML figures exist and are non-empty."""

    def test_h1_figures_exist(self):
        """Verifies H1 Lorenz curve figures exist."""
        assert H1_PNG.exists(), f"Missing {H1_PNG}"
        assert H1_HTML.exists(), f"Missing {H1_HTML}"
        assert H1_PNG.stat().st_size > 50_000

    def test_h2_figures_exist(self):
        """Verifies H2 price-volume decomposition figures exist."""
        assert H2_PNG.exists(), f"Missing {H2_PNG}"
        assert H2_HTML.exists(), f"Missing {H2_HTML}"
        assert H2_PNG.stat().st_size > 50_000

    def test_h3_figures_exist(self):
        """Verifies H3 MAC savings spread figures exist."""
        assert H3_PNG.exists(), f"Missing {H3_PNG}"
        assert H3_HTML.exists(), f"Missing {H3_HTML}"
        assert H3_PNG.stat().st_size > 50_000
