"""
Automated Econometric Verification Suite (Phase 3).
Formally tests Hypothesis 1 (Contact Fatigue), Hypothesis 2 (Channel Superiority),
Hypothesis 3 (Macro Elasticity & Demographics), and Outbound Policy Simulation.
"""

from pathlib import Path
import json
import pytest
import pandas as pd
import numpy as np

REPORTS_DIR = Path("reports")
EXPORTS_DIR = Path("data/exports")
CLEANED_DIR = Path("data/cleaned")

PRECALL_PARQUET = CLEANED_DIR / "fct_campaign_precall_targeting.parquet"
OPERATIONAL_PARQUET = CLEANED_DIR / "fct_campaign_full_operational.parquet"
BENCHMARK_PARQUET = CLEANED_DIR / "fct_legacy_balance_benchmark.parquet"

H1_JSON = REPORTS_DIR / "h1_validation_results.json"
H2_JSON = REPORTS_DIR / "h2_validation_results.json"
H3_JSON = REPORTS_DIR / "h3_validation_results.json"

H1_CSV = EXPORTS_DIR / "h1_fatigue_econometrics.csv"
H2_CSV = EXPORTS_DIR / "h2_channel_poutcome_matrix.csv"
H3_ODDS_CSV = EXPORTS_DIR / "h3_multivariate_odds_ratios.csv"
H3_SIM_CSV = EXPORTS_DIR / "h3_policy_simulation.csv"


@pytest.fixture(scope="session")
def h1_results():
    assert H1_JSON.is_file(), f"Missing report: {H1_JSON}"
    with open(H1_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def h2_results():
    assert H2_JSON.is_file(), f"Missing report: {H2_JSON}"
    with open(H2_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def h3_results():
    assert H3_JSON.is_file(), f"Missing report: {H3_JSON}"
    with open(H3_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def h3_sim_df():
    assert H3_SIM_CSV.is_file(), f"Missing export: {H3_SIM_CSV}"
    return pd.read_csv(H3_SIM_CSV)


@pytest.fixture(scope="session")
def h3_odds_df():
    assert H3_ODDS_CSV.is_file(), f"Missing export: {H3_ODDS_CSV}"
    return pd.read_csv(H3_ODDS_CSV)


# ==============================================================================
# 1. HYPOTHESIS 1 ASSERTIONS: CONTACT FATIGUE BOUNDARY
# ==============================================================================

def test_h1_fatigue_p_value(h1_results):
    """
    H1 Verification: p_value < 0.001 for Touches 1-3 vs Touches 4+.
    Validates both Pearson Chi-Square test of independence and Proportion Z-test.
    """
    ct = h1_results["contingency_test"]
    assert ct["chi2_p_value_yates"] < 0.001, (
        f"Expected Chi-Square p-value < 0.001, got {ct['chi2_p_value_yates']}"
    )
    assert ct["z_p_value"] < 0.001, (
        f"Expected Z-test p-value < 0.001, got {ct['z_p_value']}"
    )
    assert ct["z_statistic"] > 10.0, (
        f"Expected robust Z-statistic > 10.0, got {ct['z_statistic']}"
    )


def test_h1_subscription_retention_guardrail_2(h1_results):
    """
    H1 Verification: Touches 1-3 subscription retention is 88.0388% (>= 85.0% Guardrail 2).
    """
    retention_pct = h1_results["guardrails"]["guardrail_2_retention_pct"]
    assert pytest.approx(88.0388, rel=1e-3) == retention_pct, (
        f"Expected retention ~88.0388%, got {retention_pct}"
    )
    assert retention_pct >= 85.0, (
        f"Guardrail 2 breach: Retention {retention_pct}% < 85.0%"
    )
    assert h1_results["guardrails"]["guardrail_2_status"] == "PASS"


def test_h1_fatigue_zone_conversion_guardrail_1(h1_results):
    """
    H1 Verification: Touches 4+ conversion rate is 7.2692% (< 8.0% Guardrail 1).
    """
    fatigue_conv_pct = h1_results["contingency_test"]["touches_4_plus_conv_rate_pct"]
    assert pytest.approx(7.2692, rel=1e-3) == fatigue_conv_pct, (
        f"Expected Touches 4+ conversion rate ~7.2692%, got {fatigue_conv_pct}"
    )
    assert fatigue_conv_pct < 8.0, (
        f"Expected Touches 4+ to fail Guardrail 1 (< 8.0%), got {fatigue_conv_pct}%"
    )
    assert h1_results["guardrails"]["guardrail_1_status_touches_4_plus"] == "FAIL"


def test_h1_logistic_decay_coefficient(h1_results):
    """
    H1 Verification: Logistic regression coefficient on campaign touch is strictly negative (OR < 1.0, p < 0.001).
    """
    decay = h1_results["logistic_decay"]
    beta_1 = decay["beta_1"]
    or_per_call = decay["odds_ratio_per_call"]
    p_val = decay["beta_1_p_value"]

    assert beta_1 < 0.0, f"Expected negative logistic slope, got {beta_1}"
    assert or_per_call < 1.0, f"Expected Odds Ratio per call < 1.0, got {or_per_call}"
    assert p_val < 0.001, f"Expected Wald p-value < 0.001, got {p_val}"


def test_h1_touch_inflection_point(h1_results):
    """
    H1 Verification: Touch 4 is 9.39% (cohort) and Touch 5 drops to 7.50% (< 8.0% Guardrail 1).
    """
    decay = h1_results["logistic_decay"]
    t4_conv = decay["touch_4_cohort_conversion_pct"]
    t5_conv = decay["touch_5_cohort_conversion_pct"]

    assert pytest.approx(9.39, rel=1e-2) == t4_conv, f"Expected Touch 4 conv ~9.39%, got {t4_conv}"
    assert t4_conv >= 8.0, f"Touch 4 should pass Guardrail 1, got {t4_conv}"

    assert pytest.approx(7.50, rel=1e-2) == t5_conv, f"Expected Touch 5 conv ~7.50%, got {t5_conv}"
    assert t5_conv < 8.0, f"Touch 5 must breach Guardrail 1 (< 8.0%), got {t5_conv}"
    assert decay["permanent_breach_touch"] == 5


# ==============================================================================
# 2. HYPOTHESIS 2 ASSERTIONS: CHANNEL SUPERIORITY & PRIOR-OUTCOME
# ==============================================================================

def test_h2_cellular_relative_risk(h2_results):
    """
    H2 Verification: Cellular vs Telephone Relative Risk is 2.817x (> 2.5x, p < 0.001).
    """
    chan = h2_results["channel_superiority"]
    rr = chan["relative_risk"]
    p_val = chan["chi2_p_value_yates"]

    assert pytest.approx(2.8172, rel=1e-3) == rr, f"Expected Relative Risk ~2.8172x, got {rr}"
    assert rr > 2.5, f"Expected Relative Risk > 2.5x, got {rr}"
    assert p_val < 0.001, f"Expected p-value < 0.001, got {p_val}"


def test_h2_cmh_stratified_odds_ratio(h2_results):
    """
    H2 Verification: Cochran-Mantel-Haenszel stratified odds ratio remains > 2.0x (p < 0.001).
    """
    cmh = h2_results["cmh_stratified_test"]
    cmh_or = cmh["cmh_odds_ratio"]
    p_val = cmh["cmh_age_p_value"]

    assert pytest.approx(2.9048, rel=1e-3) == cmh_or, f"Expected CMH OR ~2.9048x, got {cmh_or}"
    assert cmh_or > 2.0, f"Expected CMH OR > 2.0x, got {cmh_or}"
    assert p_val < 0.001, f"Expected CMH p-value < 0.001, got {p_val}"


def test_h2_poutcome_success_conversion(h2_results):
    """
    H2 Verification: poutcome == 'success' conversion rate is 65.1129% (> 60.0%, p < 0.001).
    """
    pout = h2_results["prior_outcome_recency"]
    succ_conv = pout["poutcome_breakdown"]["success"]["conversion_rate_pct"]
    omnibus_p = pout["omnibus_chi2_p_value"]

    assert pytest.approx(65.1129, rel=1e-3) == succ_conv, (
        f"Expected prior success conversion ~65.1129%, got {succ_conv}"
    )
    assert succ_conv > 60.0, f"Expected prior success conversion > 60.0%, got {succ_conv}%"
    assert omnibus_p < 0.001, f"Expected omnibus p-value < 0.001, got {omnibus_p}"


# ==============================================================================
# 3. HYPOTHESIS 3 ASSERTIONS: MACRO ELASTICITY & DEMOGRAPHICS
# ==============================================================================

def test_h3_macro_relative_risk(h3_results):
    """
    H3 Verification: Low Rate Regime vs High Rate Regime Relative Risk is 5.057x (> 3.0x, p < 0.001).
    """
    macro = h3_results["macro_elasticity"]
    rr_conv = macro["relative_risk_conversion"]
    p_val = macro["chi2_p_value_yates"]

    assert pytest.approx(5.0573, rel=1e-3) == rr_conv, (
        f"Expected Macro Relative Risk ~5.0573x, got {rr_conv}"
    )
    assert rr_conv > 3.0, f"Expected Macro Relative Risk > 3.0x, got {rr_conv}"
    assert p_val < 0.001, f"Expected Chi-Square p-value < 0.001, got {p_val}"


def test_h3_senior_to_core_conversion_ratio(h3_results):
    """
    H3 Verification: Senior/Retired (60+) conversion (45.49%) is > 4.5x Core Working (31-45) (9.37%).
    """
    demo = h3_results["demographic_misallocation"]
    ratio = demo["senior_to_core_conversion_ratio"]
    senior_conv = demo["age_cohorts"]["4. Senior/Retired (60+)"]["conversion_rate_pct"]
    core_conv = demo["age_cohorts"]["2. Core Working (31-45)"]["conversion_rate_pct"]

    assert pytest.approx(45.4945, rel=1e-3) == senior_conv, (
        f"Expected Senior conversion ~45.49%, got {senior_conv}"
    )
    assert pytest.approx(9.3656, rel=1e-3) == core_conv, (
        f"Expected Core Working conversion ~9.37%, got {core_conv}"
    )
    assert ratio > 4.5, f"Expected Senior to Core Working ratio > 4.5x, got {ratio}"


def test_h3_multivariate_propensity_zero_leakage_and_auc(h3_results, h3_odds_df):
    """
    H3 Verification: Multivariate logistic regression inputs strictly exclude
    duration and duration_minutes and achieve ROC-AUC > 0.75.
    """
    model = h3_results["multivariate_propensity_model"]
    auc = model["roc_auc"]

    # 1. Zero duration leakage assertion
    model_features = model["model_features"]
    csv_features = h3_odds_df["feature"].tolist()
    for feat in model_features + csv_features:
        assert "duration" not in feat.lower(), f"Leakage detected: {feat} in model features!"

    # 2. Predictive discrimination assertion
    assert auc > 0.75, f"Expected ROC-AUC > 0.75, got {auc}"
    assert pytest.approx(0.7704, rel=1e-2) == auc, f"Expected ROC-AUC ~0.7704, got {auc}"


# ==============================================================================
# 4. OUTBOUND POLICY SIMULATION ASSERTIONS
# ==============================================================================

def test_policy_simulation_reconciliation_and_guardrails(h3_sim_df):
    """
    Policy Simulation Verification:
    h3_policy_simulation.csv exists, reconciles to 41,188 leads and 105,754 baseline calls,
    and passes both Guardrail 1 (>= 8.0% cohort conversion) and Guardrail 2 (>= 85.0% retention).
    """
    assert not h3_sim_df.empty, "Policy simulation dataframe is empty"

    # Baseline row check
    baseline_row = h3_sim_df[h3_sim_df["scenario_id"] == "Scenario 0"].iloc[0]
    assert int(baseline_row["target_pipeline_leads"]) == 41188, (
        f"Expected 41,188 baseline leads, got {baseline_row['target_pipeline_leads']}"
    )
    assert int(baseline_row["total_calls_dialed"]) == 105754, (
        f"Expected 105,754 baseline calls, got {baseline_row['total_calls_dialed']}"
    )
    assert int(baseline_row["subscriptions_won"]) == 4640, (
        f"Expected 4,640 baseline subscriptions, got {baseline_row['subscriptions_won']}"
    )

    # Policy P0 Cohort Pruning check
    p0_pruning = h3_sim_df[h3_sim_df["scenario_id"] == "Scenario 1A"].iloc[0]
    assert int(p0_pruning["subscriptions_won"]) == 4085
    assert pytest.approx(88.04, rel=1e-2) == float(p0_pruning["subscription_retention_pct"])
    assert float(p0_pruning["subscription_retention_pct"]) >= 85.0  # Guardrail 2
    assert float(p0_pruning["lead_conversion_rate_pct"]) >= 8.0     # Guardrail 1
    assert p0_pruning["guardrail_1_status"] == "PASS"
    assert p0_pruning["guardrail_2_status"] == "PASS"

    # Policy P0 Truncated Cap check
    p0_trunc = h3_sim_df[h3_sim_df["scenario_id"] == "Scenario 1B"].iloc[0]
    assert int(p0_trunc["total_calls_dialed"]) == 77710  # 54,805 + 7,635 * 3
    assert int(p0_trunc["calls_saved_vs_baseline"]) == 28044
    assert int(p0_trunc["subscriptions_won"]) == 4085
    assert p0_trunc["guardrail_1_status"] == "PASS"
    assert p0_trunc["guardrail_2_status"] == "PASS"

    # Reallocation Scenarios check
    for sc_id in ["Scenario 2A", "Scenario 2B", "Scenario 2C"]:
        realloc_row = h3_sim_df[h3_sim_df["scenario_id"] == sc_id].iloc[0]
        assert float(realloc_row["subscription_retention_pct"]) >= 100.0, (
            f"Expected positive commercial upside in {sc_id}"
        )
        assert realloc_row["guardrail_1_status"] == "PASS"
        assert realloc_row["guardrail_2_status"] == "PASS"
