"""
tests/test_presentation.py
Consumer Credit Risk & Underwriting Optimization
Phase 4 / Task 4.4: Presentation Asset & Documentation Assertion Suite
Framework: Christine Jiang Decision-Driven Design Framework

Asserts:
  1. All 3 high-resolution figure files exist in assets/ and exceed 20 KB.
  2. index.html exists at the repository root, contains all 7 slide blocks,
     and references all 3 generated figures.
  3. README.md exists, contains the P0-P2 strategic policy table, and strictly
     satisfies the zero em dash guardrail.
  4. index.html and export_figures.py also satisfy the zero em dash guardrail.
"""

from pathlib import Path
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
    """Verify that index.html exists, contains 7 slide blocks, and references figures."""
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

    # Assert zero em dashes in index.html
    assert "\u2014" not in html_content, "Em dash ('\u2014') detected in index.html."


def test_readme_whitepaper_structure_and_em_dashes():
    """Verify README.md exists, contains P0-P2 policy matrix, and contains no em dashes."""
    readme_path = Path("README.md")
    assert readme_path.exists(), "README.md does not exist at project root."

    readme_content = readme_path.read_text(encoding="utf-8")

    # Assert presence of P0 to P2 policy matrix items
    assert "P0: IMMEDIATE" in readme_content, "P0 action item missing from README.md"
    assert "P1: NEAR-TERM" in readme_content, "P1 action item missing from README.md"
    assert "P2: ONGOING" in readme_content, "P2 action item missing from README.md"
    assert "230.0" in readme_content, "Expected financial recovery ($230M) missing from README.md"
    assert "18,548" in readme_content, "Avoided defaults metric missing from README.md"

    # Assert figure references in README.md
    assert "assets/fig1_loss_contribution.png" in readme_content, "Figure 1 embed missing from README.md"
    assert "assets/fig2_risk_grid_heatmap.png" in readme_content, "Figure 2 embed missing from README.md"
    assert "assets/fig3_capital_waterfall.png" in readme_content, "Figure 3 embed missing from README.md"

    # Assert zero em dashes in README.md
    assert "\u2014" not in readme_content, "Em dash ('\u2014') detected in README.md."


def test_export_figures_script_no_em_dashes():
    """Verify export_figures.py contains no em dashes."""
    script_path = Path("src/presentation/export_figures.py")
    assert script_path.exists(), "src/presentation/export_figures.py does not exist."

    script_content = script_path.read_text(encoding="utf-8")
    assert "\u2014" not in script_content, "Em dash ('\u2014') detected in export_figures.py."
