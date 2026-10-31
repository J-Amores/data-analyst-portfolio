"""
tests/test_hypotheses.py
Phase 3 / Statistical Hypothesis Testing & Policy Simulation Test Suite
Framework: Christine Jiang Decision-Driven Design Framework

Asserts:
  1. Deliverables and artifact existence for H1, H2, and H3.
  2. H1: Subprime Loss Concentration & Chi-Square Goodness-of-Fit (p < 0.001).
  3. H2: Margin Breakdown, Welch's t-tests (C vs D, E, FG; p < 0.001),
         hurdle breach at C4, negative return threshold at E5.
  4. H3: Multi-variable risk interaction Relative Risk (RR > 1.40, p < 0.001),
         Odds Ratio (OR > 1.50), and Chi-Square with Yates' correction.
  5. Policy Simulation Action P0: Guardrail 2 satisfaction (Capital Retention >= 80.0%),
         volume retention, avoided defaults, charge-offs eliminated, and margin expansion.
"""

from pathlib import Path
import json
import pytest
import pandas as pd


REPORTS_DIR = Path("reports")
EXPORTS_DIR = Path("data/exports")

H1_JSON = REPORTS_DIR / "h1_validation_results.json"
H1_MD = REPORTS_DIR / "h1_summary.md"
H1_CSV = EXPORTS_DIR / "h1_loss_contribution_by_grade.csv"

H2_JSON = REPORTS_DIR / "h2_validation_results.json"
H2_MD = REPORTS_DIR / "h2_summary.md"
H2_CSV = EXPORTS_DIR / "h2_subgrade_laroc_margin.csv"

H3_JSON = REPORTS_DIR / "h3_validation_results.json"
H3_MD = REPORTS_DIR / "h3_summary.md"
H3_CSV = EXPORTS_DIR / "h3_policy_simulation_p0.csv"


# -------------------------------------------------------------------------
# Test Deliverable Artifacts Existence & Non-Emptiness
# -------------------------------------------------------------------------
def test_hypothesis_reports_and_exports_exist():
    """Verify that all Phase 3 JSON metrics, Markdown reports, and CSV exports exist."""
    files = [
        H1_JSON, H1_MD, H1_CSV,
        H2_JSON, H2_MD, H2_CSV,
        H3_JSON, H3_MD, H3_CSV,
    ]
    for f in files:
        assert f.exists(), f"Required Phase 3 deliverable missing: {f}"
        assert f.stat().st_size > 100, f"File appears empty or truncated: {f}"


# -------------------------------------------------------------------------
# Test Task 3.1: Hypothesis 1 - Subprime Loss Contribution Analysis
# -------------------------------------------------------------------------
def test_h1_loss_concentration_significance():
    """
    Test H1: Subprime tiers (Grades D-G) contribute an outsized share of total net charge-offs
    relative to funded capital share, confirmed by Chi-Square Goodness-of-Fit test (p < 0.001).
    """
    with open(H1_JSON, "r") as f:
        h1 = json.load(f)

    # Chi-Square test validation
    test = h1["statistical_test"]
    assert test["p_value"] < 0.001, f"Expected H1 Chi-Square p < 0.001, got {test['p_value']}"
    assert test["chi2_statistic"] > 1000.0, f"Expected large chi2 statistic, got {test['chi2_statistic']}"
    assert test["degrees_of_freedom"] == 6, f"Expected 6 degrees of freedom (7 grades - 1), got {test['degrees_of_freedom']}"
    assert test["is_statistically_significant"] is True

    # Loss Contribution Concentration
    subprime = h1["tier_summary"]["subprime"]
    prime = h1["tier_summary"]["prime"]

    # Subprime generates >50% of losses on <30% of capital
    assert subprime["net_charge_off_share_pct"] > 50.0, f"Subprime loss share should exceed 50%, got {subprime['net_charge_off_share_pct']}%"
    assert subprime["capital_share_pct"] < 30.0, f"Subprime capital share should be under 30%, got {subprime['capital_share_pct']}%"

    # Loss-to-Capital Ratio
    assert subprime["loss_to_capital_ratio"] > 1.50, f"Expected Subprime Loss-to-Capital Ratio > 1.50x, got {subprime['loss_to_capital_ratio']:.2f}x"
    assert prime["loss_to_capital_ratio"] < 1.00, f"Expected Prime Loss-to-Capital Ratio < 1.00x, got {prime['loss_to_capital_ratio']:.2f}x"

    # Monotonic escalation in grade loss-to-capital ratios
    grades = h1["grade_metrics"]
    grade_dict = {g["grade"]: g["loss_to_capital_ratio"] for g in grades}
    assert grade_dict["A"] < grade_dict["B"] < grade_dict["C"] < grade_dict["D"] < grade_dict["E"] < grade_dict["F"] < grade_dict["G"], (
        f"Loss-to-capital ratios should increase monotonically across grades: {grade_dict}"
    )


# -------------------------------------------------------------------------
# Test Task 3.2: Hypothesis 2 - Subprime Margin Breakdown & LAROC
# -------------------------------------------------------------------------
def test_h2_margin_breakdown_and_welch_tests():
    """
    Test H2: Subprime grades fail to absorb elevated charge-offs; Welch's t-tests
    confirm yield degradation (p < 0.001), with hurdle breach at C4 and negative pivot at E5.
    """
    with open(H2_JSON, "r") as f:
        h2 = json.load(f)

    # Welch's t-test: Grade C vs Grade D
    t_cd = h2["welch_tests"]["test_a_grade_c_vs_grade_d"]
    assert t_cd["p_value"] < 0.001, f"Expected Welch's t-test C vs D p < 0.001, got {t_cd['p_value']}"
    assert t_cd["t_statistic"] > 0, f"Expected Grade C LAROC to exceed Grade D LAROC, got t = {t_cd['t_statistic']}"
    assert t_cd["is_statistically_significant"] is True

    # Welch's t-test: Grade C vs Grade E
    t_ce = h2["welch_tests"]["test_b_grade_c_vs_grade_e"]
    assert t_ce["p_value"] < 0.001, f"Expected Welch's t-test C vs E p < 0.001, got {t_ce['p_value']}"
    assert t_ce["t_statistic"] > 0

    # Welch's t-test: Grade C vs Grades F & G
    t_cfg = h2["welch_tests"]["test_c_grade_c_vs_grades_fg"]
    assert t_cfg["p_value"] < 0.001, f"Expected Welch's t-test C vs FG p < 0.001, got {t_cfg['p_value']}"
    assert t_cfg["t_statistic"] > 0

    # Threshold Inflection Points
    meta = h2["metadata"]
    assert meta["first_hurdle_breach_subgrade"] == "C4", f"Expected hurdle breach at C4, got {meta['first_hurdle_breach_subgrade']}"
    assert meta["first_negative_return_subgrade"] == "E5", f"Expected negative return threshold at E5, got {meta['first_negative_return_subgrade']}"

    # Verify C4 cohort LAROC is below +4.0%
    subgrade_dict = {m["sub_grade"]: m["cohort_aggregate_laroc_pct"] for m in h2["subgrade_metrics"]}
    assert subgrade_dict["C3"] >= 4.0, f"C3 should meet hurdle, got {subgrade_dict['C3']}%"
    assert subgrade_dict["C4"] < 4.0, f"C4 should breach hurdle, got {subgrade_dict['C4']}%"

    # Verify E5 cohort LAROC is negative
    assert subgrade_dict["E4"] > 0.0, f"E4 should be positive, got {subgrade_dict['E4']}%"
    assert subgrade_dict["E5"] < 0.0, f"E5 should be negative, got {subgrade_dict['E5']}%"


# -------------------------------------------------------------------------
# Test Task 3.3: Hypothesis 3 - Risk Interaction & Contingency Table
# -------------------------------------------------------------------------
def test_h3_risk_interaction_relative_risk():
    """
    Test H3: DTI > 25% and Revol_Util > 65% multiplies default risk non-linearly (RR > 1.40, p < 0.001).
    """
    with open(H3_JSON, "r") as f:
        h3 = json.load(f)

    assoc = h3["statistical_association"]

    # Chi-Square Test of Independence with Yates' correction
    assert assoc["chi2_p_value"] < 0.001, f"Expected Chi2 p < 0.001, got {assoc['chi2_p_value']}"
    assert assoc["chi2_statistic"] > 1000.0, f"Expected large chi2 stat, got {assoc['chi2_statistic']}"

    # Relative Risk vs. Baseline strictly greater than 1.40
    rr = assoc["relative_risk_vs_baseline"]
    assert rr > 1.40, f"Expected RR > 1.40, got {rr:.4f}"
    assert assoc["relative_risk_95_ci"][0] > 1.40, f"Lower CI for RR should exceed 1.40, got {assoc['relative_risk_95_ci'][0]:.4f}"

    # Relative Risk vs Prime Conservative (> 2.0x)
    rr_prime = assoc["relative_risk_vs_prime_conservative"]
    assert rr_prime > 2.00, f"Expected RR vs Prime > 2.00x, got {rr_prime:.4f}"

    # Odds Ratio strictly greater than 1.50
    odds_ratio = assoc["odds_ratio"]
    assert odds_ratio > 1.50, f"Expected OR > 1.50, got {odds_ratio:.4f}"
    assert assoc["odds_ratio_95_ci"][0] > 1.50, f"Lower CI for OR should exceed 1.50, got {assoc['odds_ratio_95_ci'][0]:.4f}"


# -------------------------------------------------------------------------
# Test Task 3.3 Policy Simulation: Guardrails & Portfolio Economics
# -------------------------------------------------------------------------
def test_policy_simulation_guardrails_and_economics():
    """
    Test Underwriting Action P0 Simulation: Satisfies Guardrail 2 (Capital Retention >= 80.0%),
    eliminates >$200M in gross charge-offs, avoids >15,000 defaults, and expands net LAROC.
    """
    with open(H3_JSON, "r") as f:
        h3 = json.load(f)

    sim = h3["policy_simulation"]

    # Guardrail 2: Retained Funded Capital >= 80.0%
    assert sim["retained_capital_retention_rate_pct"] >= 80.0, (
        f"Guardrail 2 violation: Capital retention must be >= 80.0%, got {sim['retained_capital_retention_rate_pct']:.2f}%"
    )
    assert sim["guardrail_2_satisfied"] is True

    # Volume Count Retention >= 80.0%
    assert sim["retained_volume_count_pct"] >= 80.0, (
        f"Volume retention count must be >= 80.0%, got {sim['retained_volume_count_pct']:.2f}%"
    )

    # Defaults Avoided > 15,000
    assert sim["avoided_defaults_count"] > 15000, f"Expected >15,000 avoided defaults, got {sim['avoided_defaults_count']:,}"

    # Charge-Off Dollars Eliminated > $200,000,000
    assert sim["gross_charge_off_dollars_eliminated"] > 200_000_000.0, (
        f"Expected gross charge-offs eliminated > $200M, got ${sim['gross_charge_off_dollars_eliminated']:,.2f}"
    )
    assert sim["net_charge_off_dollars_eliminated"] > 200_000_000.0, (
        f"Expected net charge-offs eliminated > $200M, got ${sim['net_charge_off_dollars_eliminated']:,.2f}"
    )

    # Portfolio Margin & Risk Improvement
    assert sim["post_policy_platform_net_laroc_pct"] > sim["pre_policy_platform_net_laroc_pct"], (
        f"Expected LAROC expansion, got pre={sim['pre_policy_platform_net_laroc_pct']:.2f}%, post={sim['post_policy_platform_net_laroc_pct']:.2f}%"
    )
    assert sim["post_policy_terminal_bad_rate_pct"] < sim["pre_policy_terminal_bad_rate_pct"], (
        f"Expected default rate reduction, got pre={sim['pre_policy_terminal_bad_rate_pct']:.2f}%, post={sim['post_policy_terminal_bad_rate_pct']:.2f}%"
    )
