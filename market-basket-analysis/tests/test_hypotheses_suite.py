"""Econometric Hypothesis Pytest Suite.

Validates that all statistical hypothesis testing thresholds pass:
1. H1: Kruskal-Wallis (p < 0.001), Mann-Whitney U (p < 0.001), Large vs Small multiplier >= 4.0x.
2. H2: Chi-Square (p < 0.0001), Lift >= 6.0x across Top 10 pairs, Guardrail 1 return rate < 5.0%, positive bundle net lift.
3. H3: International > UK AOV (p < 0.001), Q4 revenue surge >= 50% (p < 0.001).
"""

from pathlib import Path
import json
import pytest

HYPOTHESIS_JSON_PATH = Path("reports/hypothesis_test_results.json")
RULES_JSON_PATH = Path("reports/market_basket_rules.json")


@pytest.fixture(scope="module")
def hypothesis_results():
    """Load hypothesis test results payload."""
    assert HYPOTHESIS_JSON_PATH.exists(), f"Missing hypothesis results at {HYPOTHESIS_JSON_PATH}"
    with open(HYPOTHESIS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def market_basket_rules():
    """Load market basket rules payload."""
    assert RULES_JSON_PATH.exists(), f"Missing market basket rules at {RULES_JSON_PATH}"
    with open(RULES_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_h1_basket_tier_aov_multiplier(hypothesis_results):
    """Verify H1: Multi-item and Large baskets deliver statistically superior AOV."""
    h1 = hypothesis_results["H1_basket_tier_multiplier"]
    assert h1["status"] == "SUPPORTED"
    assert h1["kruskal_wallis"]["p_value"] < 0.001
    assert h1["mann_whitney_u_small_vs_large"]["p_value"] < 0.001
    assert h1["welch_t_test_small_vs_large"]["p_value"] < 0.01

    # Exact multiplier checks
    assert h1["large_vs_small_multiplier"] >= 4.0, (
        f"Expected Large/Small multiplier >= 4.0x, got {h1['large_vs_small_multiplier']}x"
    )
    assert h1["multi_vs_single_multiplier"] >= 5.0, (
        f"Expected Multi/Single multiplier >= 5.0x, got {h1['multi_vs_single_multiplier']}x"
    )


def test_h2_association_rules_and_bundle_guardrails(hypothesis_results, market_basket_rules):
    """Verify H2: Top pairs exhibit Lift > 6.0, Chi-Square p < 0.0001, and pass return & margin guardrails."""
    h2 = hypothesis_results["H2_association_synergy"]
    assert h2["status"] == "SUPPORTED"
    assert h2["top_10_pairs_max_chi2_p_value"] < 0.0001
    assert h2["top_10_pairs_min_lift"] >= 6.0
    assert h2["all_bundles_pass_guardrail_1_returns"] is True
    assert h2["total_portfolio_net_revenue_lift_10pct"] > 0

    # Verify each of the 5 recommended bundles
    rec_bundles = market_basket_rules["recommended_bundles"]
    assert len(rec_bundles) == 5, f"Expected 5 recommended bundles, got {len(rec_bundles)}"
    for b in rec_bundles:
        assert b["lift"] >= 6.0, f"Bundle {b['bundle_id']} lift ({b['lift']:.2f}) is below 6.0"
        assert b["max_return_rate_pct"] < 5.0, (
            f"Bundle {b['bundle_id']} return rate ({b['max_return_rate_pct']:.2f}%) exceeds 5% guardrail"
        )
        assert b["tier_simulations"]["10pct"]["net_revenue_lift"] > 0, (
            f"Bundle {b['bundle_id']} has non-positive net revenue lift at 10% discount"
        )


def test_h3_geographic_and_seasonal_regimes(hypothesis_results):
    """Verify H3: Cross-border wholesale outperformance and Q4 holiday surge."""
    h3 = hypothesis_results["H3_regime_shifts"]
    assert h3["status"] == "SUPPORTED"

    geo = h3["geographic"]
    assert geo["mann_whitney_u_aov_p"] < 0.001
    assert geo["mann_whitney_u_skus_p"] < 0.001
    assert geo["intl_median_aov"] > geo["uk_median_aov"]
    assert geo["intl_median_skus"] >= geo["uk_median_skus"]

    seas = h3["seasonality"]
    assert seas["mann_whitney_u_aov_p"] < 0.001
    assert seas["mann_whitney_u_skus_p"] < 0.001
    assert seas["q4_revenue_surge_pct"] >= 50.0, (
        f"Expected Q4 revenue expansion >= 50%, got {seas['q4_revenue_surge_pct']}%"
    )
