"""
tests/test_presentation_assets.py
Automated Quality Assurance for Presentation Assets, Data Cubes, and Reports.
Validates file sizes, zero em dashes, empirical metric precision, and schema integrity.
"""
from pathlib import Path
import json
import pytest

ASSETS_DIR = Path("assets")
EXPORTS_DIR = Path("data/exports")
ROOT_DIR = Path(".")

FIG_FILES = [
    ASSETS_DIR / "fig1_basket_tier_aov.png",
    ASSETS_DIR / "fig2_product_pair_matrix.png",
    ASSETS_DIR / "fig3_country_seasonality_regime.png",
    ASSETS_DIR / "fig4_bundle_revenue_waterfall.png",
]

TEXT_FILES = [
    EXPORTS_DIR / "cockpit_bundle_cube.json",
    ROOT_DIR / "index.html",
    ROOT_DIR / "cockpit.html",
    ROOT_DIR / "README.md",
]

KEY_EMPIRICAL_STRINGS = [
    "19,773",
    "10,247,610.15",
    "8.05%",
    "14.74%",
    "2,948.04",
]


def test_visual_figures_exist_and_non_empty():
    """Verify that all 4 presentation figures exist and exceed 50 KB in size."""
    for fig_path in FIG_FILES:
        assert fig_path.exists(), f"Figure missing: {fig_path}"
        file_size_kb = fig_path.stat().st_size / 1024
        assert file_size_kb > 50, f"Figure {fig_path} size ({file_size_kb:.1f} KB) is under 50 KB threshold."


def test_zero_em_dashes_in_artifacts():
    """Verify that zero em dashes exist in generated JSON, HTML, and Markdown files."""
    em_dash = "\u2014"  # Em dash character
    for doc_path in TEXT_FILES:
        assert doc_path.exists(), f"Document missing: {doc_path}"
        content = doc_path.read_text(encoding="utf-8")
        assert em_dash not in content, f"Em dash found in {doc_path}!"


def test_key_empirical_metrics_in_reports():
    """Verify that exact empirical figures are present in both index.html and README.md."""
    for filename in ["index.html", "README.md"]:
        doc_path = ROOT_DIR / filename
        assert doc_path.exists(), f"Document missing: {doc_path}"
        content = doc_path.read_text(encoding="utf-8")
        for metric_str in KEY_EMPIRICAL_STRINGS:
            assert metric_str in content, f"Metric '{metric_str}' missing from {filename}!"


def test_cockpit_bundle_cube_schema_and_values():
    """Verify that cockpit_bundle_cube.json contains valid baseline metrics and bundles."""
    cube_path = EXPORTS_DIR / "cockpit_bundle_cube.json"
    assert cube_path.exists(), f"Cockpit cube missing: {cube_path}"

    with open(cube_path, "r", encoding="utf-8") as f:
        cube = json.load(f)

    # Check top-level keys
    required_keys = ["metadata", "portfolio_baseline", "basket_tiers", "bundles", "portfolio_bundle_simulation_totals"]
    for k in required_keys:
        assert k in cube, f"Missing key '{k}' in cockpit cube."

    # Check baseline metrics
    baseline = cube["portfolio_baseline"]
    assert baseline["raw_rows"] == 541909
    assert baseline["clean_rows"] == 522544
    assert baseline["valid_orders"] == 19773
    assert baseline["commercial_gmv"] == 10247610.15
    assert baseline["cancelled_value"] == -896812.49
    assert baseline["cancellation_leakage_pct"] == 8.05
    assert baseline["guest_share_pct"] == 14.74

    # Check bundles
    bundles = cube["bundles"]
    assert len(bundles) == 6, f"Expected 6 bundles (5 approved + 1 flagged), got {len(bundles)}"

    bundle_ids = [b["bundle_id"] for b in bundles]
    assert "BDL-01" in bundle_ids
    assert "BDL-05" in bundle_ids
    assert "FLAG-01" in bundle_ids

    flagged = next(b for b in bundles if b["bundle_id"] == "FLAG-01")
    assert flagged["passes_guardrail_1"] is False
    assert flagged["return_rate_a_pct"] == 8.62
    assert flagged["lift"] == 37.20
