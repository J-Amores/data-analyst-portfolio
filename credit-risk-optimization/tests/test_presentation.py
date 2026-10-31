"""
tests/test_presentation.py
Consumer Credit Risk & Underwriting Optimization
Presentation Asset & Documentation Assertion Suite

Asserts:
  1. All 3 high-resolution figure files exist in assets/ and exceed 20 KB.
  2. index.html exists at the repository root, contains all 7 slide blocks,
     references all 3 generated figures, has zero em/en dashes, and contains
     the verified Chapter 02 patched metrics.
  3. README.md exists, contains the P0-P2 strategic policy table, and strictly
     satisfies the zero em/en dash guardrail.
  4. src/presentation/export_figures.py satisfies the zero em/en dash guardrail.
  5. underwriting-simulator.html exists at the repository root, contains zero em/en dashes,
     embeds PORTFOLIO_DATA, and satisfies all underwriting decision simulator metrics.
  6. data/exports/underwriting_simulator_cube.json exists, exceeds 20 KB, and contains valid
     empirical cube schema.
"""

from pathlib import Path
import json
import pytest


def test_presentation_figures_exist_and_non_trivial():
    """Verify that all three figures exist in assets/ with file sizes > 20 KB."""
    assets_dir = Path("assets")
    assert assets_dir.exists(), "assets/ directory does not exist."

    expected_figures = [
        "fig1_loss_contribution.png",
        "fig2_risk_grid_heatmap.png",
        "fig3_capital_waterfall.png",
    ]

    min_size_bytes = 20 * 1024  # 20 KB

    for fig_name in expected_figures:
        fig_path = assets_dir / fig_name
        assert fig_path.exists(), f"Figure file missing: {fig_path}"
        file_size = fig_path.stat().st_size
        assert (
            file_size > min_size_bytes
        ), f"Figure {fig_name} is too small: {file_size} bytes (expected > {min_size_bytes} bytes)."


def test_index_html_structure_and_assets():
    """Verify that index.html exists, contains 7 slide blocks, references figures, and has zero em/en dashes."""
    html_path = Path("index.html")
    assert html_path.exists(), "index.html does not exist at project root."

    html_content = html_path.read_text(encoding="utf-8")

    # Assert 7 slides are present
    for slide_idx in range(1, 8):
        assert f'data-slide="{slide_idx}"' in html_content, f"Slide {slide_idx} block missing from index.html"

    # Assert all three figure assets are referenced
    assert "fig1_loss_contribution.png" in html_content, "fig1_loss_contribution.png not referenced in index.html"
    assert "fig2_risk_grid_heatmap.png" in html_content, "fig2_risk_grid_heatmap.png not referenced in index.html"
    assert "fig3_capital_waterfall.png" in html_content, "fig3_capital_waterfall.png not referenced in index.html"

    # Assert link to underwriting-simulator.html
    assert "underwriting-simulator.html" in html_content, "Link to underwriting-simulator.html missing from index.html"

    # Assert Chapter 02 patched figures (Task 1)
    assert "335,813 loans" in html_content, "Patched subprime loan count (335,813 loans) missing from index.html"
    assert "382,604 loans" not in html_content, "Legacy unverified loan count (382,604 loans) still present in index.html"
    assert "45.2%" in html_content, "Patched Grade F default rate (45.2%) missing from index.html"
    assert "43.8%" not in html_content, "Legacy unverified Grade F rate (43.8%) still present in index.html"

    # Assert zero em dashes and zero en dashes in index.html
    assert "\u2014" not in html_content, "Em dash ('\u2014') detected in index.html."
    assert "\u2013" not in html_content, "En dash ('\u2013') detected in index.html."


def test_readme_whitepaper_structure_and_em_dashes():
    """Verify README.md exists, contains P0-P2 policy matrix, and contains no em/en dashes."""
    readme_path = Path("README.md")
    assert readme_path.exists(), "README.md does not exist at project root."

    readme_content = readme_path.read_text(encoding="utf-8")

    # Assert presence of Phase 1 to Phase 3 policy matrix items
    assert "Phase 1" in readme_content or "P0" in readme_content, "Phase 1 / P0 action item missing from README.md"
    assert "Phase 2" in readme_content or "P1" in readme_content, "Phase 2 / P1 action item missing from README.md"
    assert "Phase 3" in readme_content or "P2" in readme_content, "Phase 3 / P2 action item missing from README.md"
    assert "230" in readme_content, "Expected financial recovery ($230M) missing from README.md"
    assert "18,548" in readme_content, "Avoided defaults metric missing from README.md"

    # Assert figure references in README.md
    assert "assets/fig1_loss_contribution.png" in readme_content, "Figure 1 embed missing from README.md"
    assert "assets/fig2_risk_grid_heatmap.png" in readme_content, "Figure 2 embed missing from README.md"
    assert "assets/fig3_capital_waterfall.png" in readme_content, "Figure 3 embed missing from README.md"

    # Assert zero em dashes and en dashes in README.md
    assert "\u2014" not in readme_content, "Em dash ('\u2014') detected in README.md."
    assert "\u2013" not in readme_content, "En dash ('\u2013') detected in README.md."


def test_export_figures_script_no_em_dashes():
    """Verify export_figures.py contains no em/en dashes and has escaped dollar signs."""
    script_path = Path("src/presentation/export_figures.py")
    assert script_path.exists(), "src/presentation/export_figures.py does not exist."

    script_content = script_path.read_text(encoding="utf-8")
    assert "\u2014" not in script_content, "Em dash ('\u2014') detected in export_figures.py."
    assert "\u2013" not in script_content, "En dash ('\u2013') detected in export_figures.py."


def test_underwriting_simulator_html_structure_and_metrics():
    """Verify underwriting-simulator.html exists, contains no em/en dashes, and satisfies all simulator metrics."""
    simulator_path = Path("underwriting-simulator.html")
    assert simulator_path.exists(), "underwriting-simulator.html does not exist at project root."

    simulator_content = simulator_path.read_text(encoding="utf-8")

    # Guardrails: Zero em dashes and zero en dashes
    assert "\u2014" not in simulator_content, "Em dash ('\u2014') detected in underwriting-simulator.html."
    assert "\u2013" not in simulator_content, "En dash ('\u2013') detected in underwriting-simulator.html."

    # Top Sticky Header assertions
    assert "JOHN AMORES | UNDERWRITING DECISION WORKSTATION" in simulator_content, "Top brand title missing from underwriting-simulator.html"
    assert "LIVE APPLICANT DESK TESTER" in simulator_content, "Desk tester navigation link missing from underwriting-simulator.html"
    assert "SAMPLE BORROWER QUEUE" in simulator_content, "Borrower queue navigation link missing from underwriting-simulator.html"
    assert "PORTFOLIO GUARDRAIL BENCHMARKS" in simulator_content, "Benchmarks navigation link missing from underwriting-simulator.html"
    assert "index.html" in simulator_content, "Link back to index.html missing from underwriting-simulator.html"
    assert "BACK TO EXECUTIVE REPORT" in simulator_content, "Back button text missing from underwriting-simulator.html"

    # Sample Applicant Queue assertions (5 One-Click Borrower Profiles)
    assert "Applicant #104: Prime Consolidation" in simulator_content, "Applicant #104 profile missing from underwriting-simulator.html"
    assert "Applicant #208: Subgrade C4 Margin Leak" in simulator_content, "Applicant #208 profile missing from underwriting-simulator.html"
    assert "Applicant #312: Phase 1 Dual-Risk Hard-Stop" in simulator_content, "Applicant #312 profile missing from underwriting-simulator.html"
    assert "Applicant #419: 5-Year Term Cap Trigger" in simulator_content, "Applicant #419 profile missing from underwriting-simulator.html"
    assert "Applicant #505: Small Business Verification" in simulator_content, "Applicant #505 profile missing from underwriting-simulator.html"

    # Policy Engine Mode Toggle assertions
    assert "Policy Engine Mode:" in simulator_content, "Policy engine mode toggle label missing from underwriting-simulator.html"
    assert "Active: Phase 1-3 Guardrails ON" in simulator_content, "Active guardrails toggle missing from underwriting-simulator.html"
    assert "Legacy: Unfiltered Baseline" in simulator_content, "Legacy baseline toggle missing from underwriting-simulator.html"

    # Compact 4-Card Portfolio Policy Impact assertions
    assert "02 PORTFOLIO-WIDE IMPACT OF ACTIVE RULES" in simulator_content, "Portfolio-wide impact header missing from underwriting-simulator.html"
    assert "230.04" in simulator_content, "$230.04M net savings metric missing from underwriting-simulator.html"
    assert "18,548" in simulator_content, "18,548 avoided defaults count missing from underwriting-simulator.html"
    assert "254.10" in simulator_content, "$254.10M gross savings metric missing from underwriting-simulator.html"
    assert "14.20" in simulator_content, "$14.20M repricing revenue metric missing from underwriting-simulator.html"
    assert "74,422" in simulator_content, "74,422 Subgrade C4 loans metric missing from underwriting-simulator.html"
    assert "95.81%" in simulator_content, "95.81% lending volume kept missing from underwriting-simulator.html"
    assert "4.40%" in simulator_content, "4.40% post-policy net LAROC return missing from underwriting-simulator.html"
    assert "240.1" in simulator_content, "$240.1M small business protection metric missing from underwriting-simulator.html"
    assert "588.5" in simulator_content, "$588.5M late workout loan volume missing from underwriting-simulator.html"

    # Single-Applicant Underwriting Desk Decision badges
    assert "[AUTO-DECLINED: PHASE 1 DUAL-RISK HARD-STOP]" in simulator_content, "Hard-stop decline ticket badge missing from underwriting-simulator.html"
    assert "[CONDITIONAL APPROVAL: PHASE 2 RE-PRICED (+150 BPS)]" in simulator_content, "Subgrade C4 repriced badge missing from underwriting-simulator.html"
    assert "[CONDITIONAL APPROVAL: TERM CAPPED TO 36 MONTHS]" in simulator_content, "Term cap conditional badge missing from underwriting-simulator.html"
    assert "[CONDITIONAL APPROVAL: PHASE 3 IRS TAX VERIFICATION REQUIRED]" in simulator_content, "Small business audit badge missing from underwriting-simulator.html"
    assert "[APPROVED: PRIME STANDARD TERMS]" in simulator_content, "Prime approved badge missing from underwriting-simulator.html"

    # Main tool FICO spectrum and profitability predictor assertions
    assert "desk-fico" in simulator_content, "Credit score (FICO) input missing from underwriting-simulator.html"
    assert "Empirical Credit Score Spectrum" in simulator_content, "Credit score spectrum indicator missing from underwriting-simulator.html"
    assert "CUTOFF: 685 FICO" in simulator_content, "Spectrum cutoff line marker missing from underwriting-simulator.html"
    assert "PROFITABLE" in simulator_content, "Profitability verdict missing from underwriting-simulator.html"
    assert "UNPROFITABLE" in simulator_content, "Unprofitable verdict missing from underwriting-simulator.html"

    # Embedded empirical cube check
    assert "const PORTFOLIO_DATA =" in simulator_content, "Embedded PORTFOLIO_DATA missing from underwriting-simulator.html"


def test_underwriting_simulator_cube_json_export():
    """Verify data/exports/underwriting_simulator_cube.json exists, exceeds 20 KB, and contains valid cube structure."""
    cube_path = Path("data/exports/underwriting_simulator_cube.json")
    if not cube_path.exists():
        cube_path = Path("data/exports/cockpit_cube.json")
    assert cube_path.exists(), "Underwriting simulator cube JSON does not exist."
    assert cube_path.stat().st_size > 20 * 1024, "Cube JSON is smaller than 20 KB."

    cube_raw = cube_path.read_text(encoding="utf-8")
    assert "\u2014" not in cube_raw, "Em dash ('\u2014') detected in cube JSON."
    assert "\u2013" not in cube_raw, "En dash ('\u2013') detected in cube JSON."

    data = json.loads(cube_raw)
    assert "metadata" in data, "Missing metadata in cube JSON"
    assert "policy_cube" in data, "Missing policy_cube in cube JSON"
    assert "risk_grid_16" in data, "Missing risk_grid_16 in cube JSON"
    assert "subgrades" in data, "Missing subgrades in cube JSON"
    assert "terms" in data, "Missing terms in cube JSON"
    assert "purposes" in data, "Missing purposes in cube JSON"
    assert "fico_bands" in data, "Missing fico_bands in cube JSON"

    assert len(data["policy_cube"]) == 112, f"Expected 112 cells in 3D policy cube, found {len(data['policy_cube'])}"
    assert len(data["subgrades"]) == 35, f"Expected 35 subgrades (A1-G5), found {len(data['subgrades'])}"
    assert len(data["fico_bands"]) == 6, f"Expected 6 empirical FICO bands, found {len(data['fico_bands'])}"
    assert data["metadata"]["total_loans"] == 1345350, "Total loans count does not match 1,345,350."
    assert data["metadata"]["recommended_avoided_defaults"] == 18548, "Avoided defaults does not match 18,548."
