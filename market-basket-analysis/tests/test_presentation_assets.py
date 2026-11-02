"""
tests/test_presentation_assets.py
Automated Quality Assurance for Presentation Assets, Data Cubes, and Reports.
Validates file sizes, zero em and en dashes, zero academic/DS jargon, whole-number metric precision, and schema integrity.
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
    ROOT_DIR / "bundle-builder.html",
    ROOT_DIR / "README.md",
]

PROSE_REPORTS = [
    ROOT_DIR / "index.html",
    ROOT_DIR / "bundle-builder.html",
    ROOT_DIR / "README.md",
]

STAKEHOLDER_PAGES = [
    ROOT_DIR / "index.html",
    ROOT_DIR / "bundle-builder.html",
]

KEY_METRIC_STRINGS = [
    "19,773",
    "522,544",
    "87%",
    "£2,948",
    "£24,528",
]

BANNED_JARGON_WORDS = [
    "kruskal-wallis",
    "mann-whitney",
    "cannibalization",
    "monetization polarization",
    "empirical",
]

BANNED_AI_WORDS = [
    "underscores",
    "testament",
    "delve",
    "tapestry",
    "monetization polarization",
    "pivotal",
    "landscape",
    "unlocks",
    "showcasing",
    "highlighting",
    "exposing",
    "bifurcating",
    "synergistic",
]


def test_visual_figures_exist_and_non_empty():
    """Verify that all 4 presentation figures exist and exceed 50 KB in size."""
    for fig_path in FIG_FILES:
        assert fig_path.exists(), f"Figure missing: {fig_path}"
        file_size_kb = fig_path.stat().st_size / 1024
        assert file_size_kb > 50, f"Figure {fig_path} size ({file_size_kb:.1f} KB) is under 50 KB threshold."


def test_zero_em_dashes_in_artifacts():
    """Verify that zero em dashes and zero en dashes exist in generated JSON, HTML, and Markdown files."""
    em_dash = "\u2014"
    en_dash = "\u2013"
    for doc_path in TEXT_FILES:
        assert doc_path.exists(), f"Document missing: {doc_path}"
        content = doc_path.read_text(encoding="utf-8")
        assert em_dash not in content, f"Em dash found in {doc_path}!"
        assert en_dash not in content, f"En dash found in {doc_path}!"


def test_zero_ai_jargon_and_legacy_labels():
    """Verify that zero banned AI words or P0/P1/P2 labels appear in HTML and Markdown reports."""
    for doc_path in PROSE_REPORTS:
        assert doc_path.exists(), f"Document missing: {doc_path}"
        content = doc_path.read_text(encoding="utf-8").lower()
        assert "p0" not in content, f"Legacy priority label 'P0' found in {doc_path}!"
        for word in BANNED_AI_WORDS:
            assert word not in content, f"Banned AI jargon '{word}' found in {doc_path}!"


def test_zero_banned_jargon_in_stakeholder_pages():
    """Verify that zero banned academic/DS jargon words appear in index.html or bundle-builder.html."""
    for doc_path in STAKEHOLDER_PAGES:
        assert doc_path.exists(), f"Document missing: {doc_path}"
        content = doc_path.read_text(encoding="utf-8").lower()
        for word in BANNED_JARGON_WORDS:
            assert word not in content, f"Banned academic/DS jargon '{word}' found in {doc_path}!"


def test_key_empirical_metrics_in_reports():
    """Verify that key clean whole-number metrics are present in index.html and bundle-builder.html."""
    doc_path = ROOT_DIR / "index.html"
    assert doc_path.exists(), f"Document missing: {doc_path}"
    content = doc_path.read_text(encoding="utf-8")
    for metric_str in KEY_METRIC_STRINGS:
        assert metric_str in content, f"Metric '{metric_str}' missing from {doc_path.name}!"

    builder_path = ROOT_DIR / "bundle-builder.html"
    assert builder_path.exists(), f"Document missing: {builder_path}"
    builder_content = builder_path.read_text(encoding="utf-8")
    assert "19,773" in builder_content, f"Metric '19,773' missing from {builder_path.name}!"


def test_cockpit_bundle_cube_schema_and_values():
    """Verify that cockpit_bundle_cube.json contains valid baseline metrics, approved bundles, and blocked items."""
    cube_path = EXPORTS_DIR / "cockpit_bundle_cube.json"
    assert cube_path.exists(), f"Cockpit cube missing: {cube_path}"

    with open(cube_path, "r", encoding="utf-8") as f:
        cube = json.load(f)

    # Check top-level keys
    required_keys = [
        "metadata",
        "portfolio_baseline",
        "basket_tiers",
        "bundles",
        "blocked_items",
        "scenarios",
        "discount_sensitivity_grid",
        "portfolio_bundle_simulation_totals",
        "sku_lookup_desk"
    ]
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

    # Check exact approved bundle return rates
    bundle_dict = {b["bundle_id"]: b for b in bundles}
    assert bundle_dict["BDL-01"]["return_rate_a_pct"] == 1.70
    assert bundle_dict["BDL-01"]["return_rate_b_pct"] == 3.81
    assert bundle_dict["BDL-02"]["return_rate_a_pct"] == 2.06
    assert bundle_dict["BDL-02"]["return_rate_b_pct"] == 1.89
    assert bundle_dict["BDL-03"]["return_rate_a_pct"] == 0.58
    assert bundle_dict["BDL-03"]["return_rate_b_pct"] == 0.90
    assert bundle_dict["BDL-04"]["return_rate_a_pct"] == 2.33
    assert bundle_dict["BDL-04"]["return_rate_b_pct"] == 0.99
    assert bundle_dict["BDL-05"]["return_rate_a_pct"] == 0.58
    assert bundle_dict["BDL-05"]["return_rate_b_pct"] == 0.73

    # Check flagged items
    flagged = bundle_dict["FLAG-01"]
    assert flagged["passes_guardrail_1"] is False
    assert flagged["return_rate_a_pct"] == 8.62
    assert flagged["lift"] == 37.20

    # Check blocked items list
    blocked = {b["flag_id"]: b for b in cube["blocked_items"]}
    assert "FLAG-01" in blocked
    assert "FLAG-02" in blocked
    assert blocked["FLAG-02"]["return_rate_a_pct"] == 5.29
    assert blocked["FLAG-02"]["return_rate_b_pct"] == 5.86

    # Check 6 pre-computed scenarios
    assert len(cube["scenarios"]) == 6
    scenarios = {s["scenario_id"]: s for s in cube["scenarios"]}
    assert scenarios["Scenario 0"]["net_revenue_lift"] == 0.00
    assert scenarios["Scenario 1A"]["net_revenue_lift"] == 2948.04
    assert scenarios["Scenario 2C"]["net_revenue_lift"] == 24527.69

    # Check 12-row sensitivity grid
    assert len(cube["discount_sensitivity_grid"]) == 12


def test_zero_broken_local_links_in_reports():
    """Verify that all local href and src links in index.html, bundle-builder.html, and README.md point to valid files."""
    import re

    files_to_check = [
        ROOT_DIR / "index.html",
        ROOT_DIR / "bundle-builder.html",
        ROOT_DIR / "README.md",
    ]

    for file_path in files_to_check:
        assert file_path.exists(), f"Report file missing: {file_path}"
        content = file_path.read_text(encoding="utf-8")

        # Extract href and src in HTML
        links = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', content)
        # Extract markdown links and images
        links += re.findall(r'\[.*?\]\(([^)]+)\)', content)
        links += re.findall(r'!\[.*?\]\(([^)]+)\)', content)

        for link in links:
            if link.startswith(("http", "#", "data:", "mailto:")):
                continue
            clean_link = link.split("#")[0].split("?")[0].strip()
            if clean_link:
                target_path = Path(clean_link)
                assert target_path.exists(), f"Broken local link '{link}' found in {file_path.name}!"

