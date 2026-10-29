"""
Presentation and Executive Deliverables Test Suite (Phase 4).
Asserts that static charts, HTML presentations, and whitepaper meet all design,
editorial, and quantitative reconciliation criteria.
"""

from pathlib import Path
import re
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
INDEX_HTML = ROOT_DIR / "index.html"
COCKPIT_HTML = ROOT_DIR / "cockpit.html"
README_MD = ROOT_DIR / "README.md"

REQUIRED_CHARTS = [
    "fig1_contact_fatigue_cliff.png",
    "fig2_channel_poutcome_matrix.png",
    "fig3_macro_demographic_heatmap.png",
    "fig4_policy_reallocation_waterfall.png",
]

INDEX_VERIFIED_NUMBERS = [
    "41,188",
    "105,754",
    "88%",
    "48%",
    "65%",
    "3,242",
]

COCKPIT_README_VERIFIED_NUMBERS = [
    "41,188",
    "105,754",
    "88.04%",
    "14.74%",
    "65.11%",
    "0.7704",
]

BANNED_AI_WORDS = [
    "underscores",
    "testament",
    "pivotal",
    "delve",
    "landscape",
    "tapestry",
    "unlocks",
    "showcasing",
    "highlighting",
    "exposing",
]


def test_charts_exist_and_meet_file_size():
    """Verify that all 4 static chart export PNGs exist and exceed 50 KB."""
    assert ASSETS_DIR.is_dir(), f"Assets directory not found at {ASSETS_DIR}"
    for filename in REQUIRED_CHARTS:
        chart_path = ASSETS_DIR / filename
        assert chart_path.is_file(), f"Missing required chart: {chart_path}"
        size_kb = chart_path.stat().st_size / 1024.0
        assert size_kb > 50.0, f"Chart {filename} is too small: {size_kb:.1f} KB (expected > 50 KB)"


def test_documents_exist():
    """Verify that index.html, cockpit.html, and README.md exist."""
    assert INDEX_HTML.is_file(), f"Missing {INDEX_HTML}"
    assert COCKPIT_HTML.is_file(), f"Missing {COCKPIT_HTML}"
    assert README_MD.is_file(), f"Missing {README_MD}"


def test_index_verified_numbers_present():
    """Verify that whole-number benchmarks are represented in index.html."""
    content = INDEX_HTML.read_text(encoding="utf-8")
    for number in INDEX_VERIFIED_NUMBERS:
        assert number in content, f"Verified figure '{number}' missing in index.html"


@pytest.mark.parametrize("file_path", [COCKPIT_HTML, README_MD])
def test_cockpit_readme_numbers_present(file_path):
    """Verify that core econometric findings are represented in cockpit.html and README.md."""
    content = file_path.read_text(encoding="utf-8")
    for number in COCKPIT_README_VERIFIED_NUMBERS:
        assert number in content, f"Verified figure '{number}' missing in {file_path.name}"


@pytest.mark.parametrize("file_path", [INDEX_HTML, COCKPIT_HTML, README_MD])
def test_humanizer_zero_dashes(file_path):
    """Verify that zero em dashes and zero en dashes appear in prose or code."""
    content = file_path.read_text(encoding="utf-8")
    assert "\u2014" not in content, f"Em dash (U+2014) detected in {file_path.name}"
    assert "\u2013" not in content, f"En dash (U+2013) detected in {file_path.name}"


@pytest.mark.parametrize("file_path", [INDEX_HTML, COCKPIT_HTML, README_MD])
def test_humanizer_zero_banned_labels(file_path):
    """Verify that legacy priority codes and theatrical act labels are absent."""
    content = file_path.read_text(encoding="utf-8")
    # Priority codes: P followed by 0, 1, or 2 as standalone token
    banned_codes = ["P" + str(i) for i in [0, 1, 2]]
    for code in banned_codes:
        match = re.search(r"\b" + re.escape(code) + r"\b", content)
        assert match is None, f"Banned code '{code}' detected in {file_path.name}"

    # Theatrical labels: Act I, Act II, Act III
    acts = ["Act " + num for num in ["I", "II", "III"]]
    for act in acts:
        assert act not in content, f"Theatrical label '{act}' detected in {file_path.name}"


@pytest.mark.parametrize("file_path", [INDEX_HTML, COCKPIT_HTML, README_MD])
def test_humanizer_zero_ai_buzzwords(file_path):
    """Verify that zero AI vocabulary words or participles appear in deliverables."""
    content = file_path.read_text(encoding="utf-8").lower()
    for word in BANNED_AI_WORDS:
        assert word not in content, f"Banned AI vocabulary word '{word}' detected in {file_path.name}"
