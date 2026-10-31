"""Automated Econometric Verification Suite for Phase 3.

Validates all Phase 3 econometric hypotheses and policy simulations:
1. H1 Assertions:
   - Kruskal-Wallis H > 3400 (p < 0.0001).
   - Large (6+ SKUs) median AOV (£322.30) is 5.60x Small (1-2 SKUs) median AOV (£57.60).
   - Wholesale (31+ SKUs) median AOV is £550.58.
   - Guest checkout mean AOV (£1,101.66) is > 2.3x Registered mean AOV (£474.80, p < 0.0001).
   - 5-tier basket decomposition order counts reconcile exactly: 2313, 2041, 5622, 5253, 4544.
2. H2 Assertions:
   - All Top 10 candidate pairs have 2x2 Chi-Square p < 0.0001 and Odds Ratio > 10.0.
   - Pair 23170 + 23171 (37.20x Lift) is flagged with guardrail_1_status FLAGGED.
   - Top Anchor SKUs 22423 (5.29%) and 85123A (5.86%) are flagged (> 5.0%),
     while 85099B (2.06%) and all 5 recommended bundles (BDL-01 to BDL-05) pass Guardrail 1 (< 5.0%).
3. H3 Assertions:
   - International / EU median AOV exceeds UK domestic (£299.67, p < 0.0001).
   - Hours 10:00-15:00 capture 15,375 orders (77.76% of volume).
   - Q4 monthly revenue (£1,194.59k) exceeds Q1-Q3 baseline (£659.20k, +81.2%, p < 0.0001).
   - h3_bundle_policy_simulation.csv contains all 6 scenarios (Scenario 0 to Scenario 2C)
     with Scenario 1A net lift == 2948.04 and Scenario 2C net lift == 24527.69.
"""

from pathlib import Path
import json
import pytest
import pandas as pd

H1_JSON_PATH = Path("reports/h1_validation_results.json")
H2_JSON_PATH = Path("reports/h2_validation_results.json")
H3_JSON_PATH = Path("reports/h3_validation_results.json")

H1_CSV_PATH = Path("data/exports/h1_basket_tier_econometrics.csv")
H2_CSV_PATH = Path("data/exports/h2_association_econometrics.csv")
H3_SIM_CSV_PATH = Path("data/exports/h3_bundle_policy_simulation.csv")
H3_GRID_CSV_PATH = Path("data/exports/h3_discount_sensitivity_grid.csv")


@pytest.fixture(scope="module")
def h1_results():
    """Load H1 validation results payload."""
    assert H1_JSON_PATH.exists(), f"Missing H1 results at {H1_JSON_PATH}"
    with open(H1_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def h2_results():
    """Load H2 validation results payload."""
    assert H2_JSON_PATH.exists(), f"Missing H2 results at {H2_JSON_PATH}"
    with open(H2_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def h3_results():
    """Load H3 validation results payload."""
    assert H3_JSON_PATH.exists(), f"Missing H3 results at {H3_JSON_PATH}"
    with open(H3_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# H1 TEST SUITE
# =============================================================================
def test_h1_kruskal_wallis_omnibus(h1_results):
    """Verify H1 omnibus Kruskal-Wallis test exceeds H > 3400 threshold."""
    kw_3t = h1_results["omnibus_tests"]["kruskal_wallis_3_tier"]
    assert kw_3t["statistic"] > 3400.0, f"Expected H > 3400, got {kw_3t['statistic']}"
    assert kw_3t["p_value"] < 0.0001, f"Expected p < 0.0001, got {kw_3t['p_value']}"

    kw_5t = h1_results["omnibus_tests"]["kruskal_wallis_5_tier"]
    assert kw_5t["statistic"] > 5000.0, f"Expected H > 5000, got {kw_5t['statistic']}"
    assert kw_5t["p_value"] < 0.0001, f"Expected p < 0.0001, got {kw_5t['p_value']}"


def test_h1_basket_tier_multipliers(h1_results):
    """Verify H1 pairwise multipliers and exact median AOVs."""
    pairwise = {p["name"]: p for p in h1_results["pairwise_tests"]}

    # Small vs Large
    small_vs_large = pairwise["Small (1-2 SKUs) vs. Large (6+ SKUs)"]
    assert small_vs_large["g1_median_aov"] == 57.60
    assert small_vs_large["g2_median_aov"] == 322.30
    assert small_vs_large["median_multiplier"] == 5.60
    assert small_vs_large["mann_whitney_p"] < 0.0001
    assert small_vs_large["welch_t_p_value"] < 0.01

    # Small vs Wholesale (31+)
    small_vs_wholesale = pairwise["Small (1-2 SKUs) vs. Wholesale (31+ SKUs)"]
    assert small_vs_wholesale["g2_median_aov"] == 550.58
    assert small_vs_wholesale["median_multiplier"] == 9.56
    assert small_vs_wholesale["welch_t_p_value"] < 0.0001

    # Single vs Multi
    single_vs_multi = pairwise["Single-SKU (1 item) vs. Multi-SKU (2+ items)"]
    assert single_vs_multi["g1_median_aov"] == 45.00
    assert single_vs_multi["g2_median_aov"] == 308.60
    assert single_vs_multi["median_multiplier"] == 6.86


def test_h1_5_tier_decomposition_counts(h1_results):
    """Verify 5-tier basket decomposition order counts reconcile 100%."""
    decomp = {r["tier_name"]: r for r in h1_results["basket_tier_decomposition"]}
    assert decomp["1-2 SKUs"]["order_count"] == 2313
    assert decomp["3-5 SKUs"]["order_count"] == 2041
    assert decomp["6-15 SKUs"]["order_count"] == 5622
    assert decomp["16-30 SKUs"]["order_count"] == 5253
    assert decomp["31+ SKUs"]["order_count"] == 4544

    total_orders = sum(r["order_count"] for r in h1_results["basket_tier_decomposition"])
    assert total_orders == 19773


def test_h1_guest_checkout_wholesale_econometrics(h1_results):
    """Verify guest checkout mean AOV is > 2.3x registered account mean AOV."""
    g_vs_r = h1_results["guest_vs_registered_validation"]
    reg = g_vs_r["registered"]
    guest = g_vs_r["guest"]
    comp = g_vs_r["comparison_metrics"]

    assert reg["order_count"] == 18402
    assert guest["order_count"] == 1371
    assert reg["mean_aov"] == 474.80
    assert guest["mean_aov"] == 1101.66
    assert comp["mean_aov_multiplier"] > 2.3, f"Expected multiplier > 2.3x, got {comp['mean_aov_multiplier']}x"
    assert comp["welch_p_revenue"] < 0.0001
    assert guest["mean_basket_skus"] == 95.53
    assert reg["mean_basket_skus"] == 20.99
    assert guest["median_basket_skus"] == 38.0


# =============================================================================
# H2 TEST SUITE
# =============================================================================
def test_h2_association_rules_top_pairs(h2_results):
    """Verify top candidate pairs have Chi-Square p < 0.0001 and Odds Ratio > 10.0."""
    top_metrics = h2_results["top_10_pairs_metrics"]
    assert top_metrics["max_chi2_p_value"] < 0.0001
    assert top_metrics["min_odds_ratio"] > 10.0
    assert top_metrics["min_lift"] >= 6.0


def test_h2_guardrail_1_catch_1_anchor_exclusions(h2_results):
    """Verify Top Anchor SKUs 22423 and 85123A exceed 5.0% return rate and are blocked."""
    audit = h2_results["guardrail_1_audit"]
    exclusions = {e["stockcode"]: e for e in audit["catch_1_anchor_exclusions"]}

    # #1 Revenue SKU 22423
    assert "22423" in exclusions
    assert exclusions["22423"]["return_rate_pct"] == 5.29
    assert "FLAGGED" in exclusions["22423"]["guardrail_status"]

    # #1 Frequency SKU 85123A
    assert "85123A" in exclusions
    assert exclusions["85123A"]["return_rate_pct"] == 5.86
    assert "FLAGGED" in exclusions["85123A"]["guardrail_status"]

    # Bulk Reversals 23843 and 23166
    assert exclusions["23843"]["return_rate_pct"] == 50.00
    assert exclusions["23166"]["return_rate_pct"] == 48.67


def test_h2_guardrail_1_catch_2_flagged_pair(h2_results):
    """Verify Rank #1 Lift pair 23170 + 23171 is flagged for exceeding 5.0% return rate."""
    audit = h2_results["guardrail_1_audit"]
    flagged = audit["catch_2_flagged_pair"]

    assert flagged["stockcode_a"] == "23170"
    assert flagged["stockcode_b"] == "23171"
    assert flagged["lift"] == 37.20
    assert flagged["return_rate_a_pct"] == 8.62
    assert "FLAGGED" in flagged["guardrail_1_status"]


def test_h2_approved_bundles_pass_guardrail_1(h2_results):
    """Verify all 5 recommended bundles (BDL-01 to BDL-05) pass Guardrail 1 (< 5.0%)."""
    audit = h2_results["guardrail_1_audit"]
    bundles = audit["approved_bundles"]
    assert len(bundles) == 5

    for b in bundles:
        assert b["guardrail_1_status"] == "PASS"
        assert b["max_return_rate_pct"] < 5.0, (
            f"Bundle {b['bundle_id']} return rate {b['max_return_rate_pct']}% exceeds 5.0%"
        )
        assert b["lift"] >= 6.0


# =============================================================================
# H3 TEST SUITE
# =============================================================================
def test_h3_geographic_regimes(h3_results):
    """Verify International median AOV exceeds UK domestic (£299.67, p < 0.0001)."""
    geo = h3_results["geographic_regimes"]
    assert geo["uk_median_aov"] == 299.67
    assert geo["intl_median_aov"] > geo["uk_median_aov"]
    assert geo["intl_median_aov"] == 385.28
    assert geo["mann_whitney_p_aov"] < 0.0001
    assert geo["ks_p_value_aov"] < 0.0001


def test_h3_intraday_and_q4_seasonality(h3_results):
    """Verify 10:00-15:00 captures 15,375 orders and Q4 monthly GMV surges +81.2%."""
    temp = h3_results["temporal_and_intraday"]

    # Intraday B2B window
    assert temp["b2b_window_orders"] == 15375
    assert temp["b2b_window_order_share_pct"] == 77.76
    assert temp["mann_whitney_p_intraday"] < 0.0001

    # Q4 Seasonality
    assert round(temp["q4_monthly_avg_gmv"] / 1000.0, 2) == 1194.59
    assert round(temp["baseline_monthly_avg_gmv"] / 1000.0, 2) == 659.20
    assert temp["q4_revenue_surge_pct"] >= 81.0
    assert temp["mann_whitney_p_q4"] < 0.0001


def test_h3_bundle_policy_simulation_scenarios(h3_results):
    """Verify all 6 scenarios in h3_bundle_policy_simulation.csv match exact benchmarks."""
    assert H3_SIM_CSV_PATH.exists(), f"Missing simulation CSV at {H3_SIM_CSV_PATH}"
    df_sim = pd.read_csv(H3_SIM_CSV_PATH)

    assert len(df_sim) == 6, f"Expected 6 scenarios, got {len(df_sim)}"
    scenarios = df_sim.set_index("scenario_id").to_dict(orient="index")

    # Scenario 0
    assert "Scenario 0" in scenarios
    assert scenarios["Scenario 0"]["net_revenue_lift"] == 0.00
    assert scenarios["Scenario 0"]["guardrail_1_status"] == "PASS"

    # Scenario 1A
    assert "Scenario 1A" in scenarios
    assert scenarios["Scenario 1A"]["net_revenue_lift"] == 2948.04
    assert scenarios["Scenario 1A"]["gross_incremental_revenue"] == 3549.72
    assert scenarios["Scenario 1A"]["cannibalized_discount_cost"] == 601.68
    assert scenarios["Scenario 1A"]["guardrail_1_status"] == "PASS"

    # Scenario 1B
    assert "Scenario 1B" in scenarios
    assert "FAIL" in scenarios["Scenario 1B"]["guardrail_1_status"] or "BREACH" in scenarios["Scenario 1B"]["guardrail_1_status"]
    assert scenarios["Scenario 1B"]["max_return_rate_pct"] > 5.0

    # Scenario 2A
    assert "Scenario 2A" in scenarios
    assert scenarios["Scenario 2A"]["net_revenue_lift"] == 4367.93

    # Scenario 2B
    assert "Scenario 2B" in scenarios
    assert scenarios["Scenario 2B"]["net_revenue_lift"] == 11792.16

    # Scenario 2C
    assert "Scenario 2C" in scenarios
    assert scenarios["Scenario 2C"]["net_revenue_lift"] == 24527.69
    assert scenarios["Scenario 2C"]["gross_incremental_revenue"] == 29533.67
    assert scenarios["Scenario 2C"]["cannibalized_discount_cost"] == 5005.98
    assert scenarios["Scenario 2C"]["guardrail_1_status"] == "PASS"


def test_zero_em_dashes_in_phase3_exports():
    """Verify that zero em dashes exist in generated Phase 3 JSON, CSV, and Markdown files."""
    em_dash = "\u2014"
    en_dash = "\u2013"

    phase3_files = [
        H1_JSON_PATH,
        H2_JSON_PATH,
        H3_JSON_PATH,
        H1_CSV_PATH,
        H2_CSV_PATH,
        H3_SIM_CSV_PATH,
        H3_GRID_CSV_PATH,
        Path("reports/h1_summary.md"),
        Path("reports/h2_summary.md"),
        Path("reports/h3_summary.md"),
    ]

    for p in phase3_files:
        assert p.exists(), f"File {p} does not exist"
        content = p.read_text(encoding="utf-8")
        assert em_dash not in content, f"Em dash found in {p}!"
        assert en_dash not in content, f"En dash found in {p}!"
