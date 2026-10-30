"""
Architecture & Verification Tests for Redesigned Single-Page Editorial Research Whitepaper (index.html).
Validates:
- Warm Archival Paper palette (#FAF8F2, #F4F1EA, #D6D3CD, #111111)
- Google Fonts typography: Newsreader Serif, Plus Jakarta Sans, JetBrains Mono
- Sticky Top Navigation Bar with exact anchor links and CTA button
- 4-Column Bordered KPI Strip with exact verified CMS project metrics
- Hospital Pharmacy Framing: $85M hospital budget model, $3.2M annual savings
- Plain-English Analyst Voice: zero forbidden academic jargon terms
- 5 Chapters + Executive Overview (CLEAN framework, Budget Breakdown, Price vs Volume, Savings Plan, 90-Day Rollout)
- Figure containers referencing assets/fig1, assets/fig2, and assets/fig3
- Interactive image lightbox modal with ESC key handling
- Accessibility (prefers-reduced-motion)
- Strict executive restraint: ZERO em dashes and ZERO en dashes across deliverables
- Interactive Pharmacy Cost Simulator (cost-simulator.html) and Guardrail 2 (0.0% outlier risk)
"""

from pathlib import Path
import pytest

INDEX_HTML_PATH = Path("index.html")
COST_SIMULATOR_HTML_PATH = Path("cost-simulator.html")
README_MD_PATH = Path("README.md")
FIGURES_SCRIPT_PATH = Path("src/presentation/export_figures.py")

FIG1_PATH = Path("assets/fig1_spend_concentration.png")
FIG2_PATH = Path("assets/fig2_price_volume_matrix.png")
FIG3_PATH = Path("assets/fig3_formulary_waterfall.png")


@pytest.fixture(scope="module")
def html_content() -> str:
    assert INDEX_HTML_PATH.exists(), "index.html must exist at repository root."
    return INDEX_HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def cost_simulator_content() -> str:
    assert COST_SIMULATOR_HTML_PATH.exists(), "cost-simulator.html must exist at repository root."
    return COST_SIMULATOR_HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def readme_content() -> str:
    assert README_MD_PATH.exists(), "README.md must exist at repository root."
    return README_MD_PATH.read_text(encoding="utf-8")


def test_editorial_design_system_and_typography(html_content: str):
    """Verify warm archival paper palette and Google Fonts typography."""
    assert "#FAF8F2" in html_content, "Must use warm archival paper background #FAF8F2."
    assert "#F4F1EA" in html_content, "Must use warm stone card fill #F4F1EA."
    assert "#D6D3CD" in html_content, "Must use crisp hairline border #D6D3CD."
    assert "#111111" in html_content, "Must use high-contrast ink #111111."

    # Fonts
    assert "Newsreader" in html_content, "Must import Newsreader editorial serif font."
    assert "Plus Jakarta Sans" in html_content or "Inter" in html_content, "Must import narrative sans font."
    assert "JetBrains Mono" in html_content, "Must import JetBrains Mono tabular font."


def test_sticky_top_navigation_bar(html_content: str):
    """Verify sticky top bar with exact anchor links and CTA button."""
    assert "sticky-nav" in html_content or "top-nav" in html_content, "Must contain top-nav/sticky-nav element."
    assert "JOHN AMORES" in html_content
    assert "HOSPITAL PHARMACY ANALYTICS CASE STUDY" in html_content or "HEALTHCARE ANALYTICS CASE STUDY" in html_content
    assert "OVERVIEW" in html_content or "EXECUTIVE BRIEFING" in html_content
    assert "01 DATA & CAVEATS" in html_content or "01 DATA &amp; CAVEATS" in html_content or "01. DATA CLEANUP" in html_content
    assert "02 BUDGET BREAKDOWN" in html_content or "02. BUDGET BREAKDOWN" in html_content
    assert "03 PRICE VS VOLUME" in html_content or "03. PRICE VS VOLUME" in html_content
    assert "04 SAVINGS PLAN" in html_content or "04. SAVINGS PLAN" in html_content
    assert "05 90-DAY ROLLOUT" in html_content or "05. 90-DAY ROLLOUT" in html_content
    assert "LAUNCH SIMULATOR" in html_content or "LAUNCH COCKPIT" in html_content
    assert "cost-simulator.html" in html_content


def test_hero_header_and_4column_kpi_strip(html_content: str):
    """Verify hero title, subtitle, and 4-column bordered KPI strip with verified metrics."""
    assert "Cutting Hospital Pharmacy Drug Costs by $3.2M Without Limiting Patient Care" in html_content or \
           "Cutting Hospital Pharmacy Drug Costs Without Limiting Patient Care" in html_content

    # 4 KPI cards with whole numbers
    assert "$85M" in html_content and "$111B" in html_content
    assert "+46%" in html_content
    assert "72%" in html_content
    assert "+$3.2M" in html_content

    # Verified claims and formulations
    assert "4,774" in html_content


def test_chapter_structure_and_anchors(html_content: str):
    """Verify all 5 chapters and overview/briefing are structured with proper IDs."""
    sections = [
        'id="chapter-01"',
        'id="chapter-02"',
        'id="chapter-03"',
        'id="chapter-04"',
        'id="chapter-05"',
    ]
    for sec in sections:
        assert sec in html_content, f"Missing section anchor {sec} in index.html"
    assert 'id="overview"' in html_content or 'id="briefing"' in html_content


def test_plain_english_analyst_voice(html_content: str, readme_content: str):
    """Verify plain-English voice and absence of forbidden academic jargon across index.html and README.md."""
    forbidden_terms = [
        "econometric decomposition",
        "pareto asymmetry",
        "methodological segregation",
        "censoring",
        "gini",
        "kolmogorov-smirnov",
        "chi-square",
        "wilcoxon",
        "p < 1.0e-99",
        "addressable wedge",
        "bioequivalent",
        "chemical entities",
        "molecules",
        "adalimumab",
    ]
    for term in forbidden_terms:
        assert term not in html_content.lower(), f"Forbidden academic term found in index.html: {term}"

    readme_forbidden = [
        "gini",
        "kolmogorov-smirnov",
        "wilcoxon",
        "logarithmic growth decomposition",
        "bundled prospective payment models",
        "bioequivalent",
        "multi-source generic molecules",
        "0.076386%",
    ]
    for term in readme_forbidden:
        assert term not in readme_content.lower(), f"Forbidden academic term found in README.md: {term}"


def test_readme_editorial_and_phases(readme_content: str):
    """Verify README.md matches plain-English voice, whole numbers, and Phase 1-3 structure."""
    # Phase 1 / Phase 2 / Phase 3 structure (no P0 / P1 / P2 phase tags)
    assert "Phase 1: Days 1 to 30" in readme_content
    assert "Phase 2: Days 30 to 60" in readme_content
    assert "Phase 3: Days 60 to 90" in readme_content
    assert "P0 " not in readme_content and "P1 " not in readme_content and "P2 " not in readme_content
    assert "P0:" not in readme_content and "P1:" not in readme_content and "P2:" not in readme_content

    # Whole-Number Rounding metrics
    whole_numbers = [
        "$85M",
        "$111B",
        "46%",
        "72%",
        "$61M",
        "90%",
        "$77M",
        "33%",
        "$408",
        "$22",
        "19x",
        "98%",
        "$3.2M",
        "$3,200K",
        "$1.1M",
        "$2.1M",
    ]
    for metric in whole_numbers:
        assert metric in readme_content, f"Missing metric '{metric}' in README.md"

    # Plus-prefixed savings
    assert "+$3.2M" in readme_content or r"+\$3.2M" in readme_content
    assert "+$1.1M" in readme_content or r"+\$1.1M" in readme_content
    assert "+$2.1M" in readme_content or r"+\$2.1M" in readme_content

    # 6 target drug clean savings
    for drug_saving in ["$472K", "$367K", "$176K", "$136K", "$97K", "$80K"]:
        assert drug_saving in readme_content, f"Missing 6-drug saving '{drug_saving}' in README.md"

    # Zero em or en dashes
    assert "—" not in readme_content, "Em dash found in README.md"
    assert "–" not in readme_content, "En dash found in README.md"


def test_figure_assets_and_containers(html_content: str):
    """Verify all three publication figures exist on disk and are linked in index.html."""
    assert FIG1_PATH.exists(), "assets/fig1_spend_concentration.png must exist."
    assert FIG2_PATH.exists(), "assets/fig2_price_volume_matrix.png must exist."
    assert FIG3_PATH.exists(), "assets/fig3_formulary_waterfall.png must exist."

    assert "assets/fig1_spend_concentration.png" in html_content
    assert "assets/fig2_price_volume_matrix.png" in html_content
    assert "assets/fig3_formulary_waterfall.png" in html_content

    # Plain-English figure captions / takeaways (zero jargon)
    assert "Brand-name drugs make up just 33% of prescriptions filled" in html_content
    assert "88 of the top 100 fastest-growing drugs were driven by treating more patients" in html_content
    assert "Switching 6 overpriced brand drugs saves $1.1M" in html_content


def test_verified_analytical_findings_and_tables(html_content: str):
    """Verify verified figures and tables in Chapter 01 to Chapter 05."""
    # Chapter 01
    assert "18,511" in html_content
    assert "4,774" in html_content
    assert "$111B ($85M hosp)" in html_content or "$111B" in html_content

    # Chapter 02
    assert "90%" in html_content
    assert "33%" in html_content
    assert "67%" in html_content
    assert "10%" in html_content
    assert "$408" in html_content
    assert "$22" in html_content
    assert "19x" in html_content

    # Chapter 03
    assert "Ozempic" in html_content
    assert "10x" in html_content
    assert "Trulicity" in html_content
    assert "107%" in html_content
    assert "46" in html_content

    # Chapter 04
    assert "$4M" in html_content or "$3.9M" in html_content
    assert "$1.1M" in html_content or "$1,100K" in html_content
    assert "$2.1M" in html_content or "$2,100K" in html_content
    assert "$3.2M" in html_content or "$3,200K" in html_content
    assert "$1.9M" in html_content or "$1,920K" in html_content
    assert "$2.6M" in html_content or "$2,560K" in html_content
    assert "98%" in html_content

    # Chapter 05
    for drug in ["Vyvanse", "Concerta", "Spiriva Respimat", "Advair Diskus", "Banzel", "Jornay PM"]:
        assert drug in html_content, f"Must include target drug {drug} in Chapter 05 roadmap."


def test_zero_em_and_en_dashes(html_content: str, cost_simulator_content: str, readme_content: str):
    """Enforce executive restraint rule: zero em dashes and zero en dashes across deliverables."""
    files_to_check = [
        ("index.html", html_content),
        ("cost-simulator.html", cost_simulator_content),
        ("README.md", readme_content),
    ]
    for name, content in files_to_check:
        assert "—" not in content, f"Em dash found in {name}!"
        assert "–" not in content, f"En dash found in {name}!"


def test_interactive_image_lightbox(html_content: str):
    """Verify full-screen image lightbox modal with ESC key and backdrop close."""
    assert "lightbox" in html_content.lower(), "Must contain lightbox modal."
    assert "Escape" in html_content or "key === 'Escape'" in html_content, "Must support ESC key to close lightbox."
    assert "openLightbox" in html_content, "Must have openLightbox function."


def test_accessibility_reduced_motion(html_content: str):
    """Verify accessibility for prefers-reduced-motion."""
    assert "prefers-reduced-motion: reduce" in html_content or "prefers-reduced-motion:reduce" in html_content, \
        "Must include prefers-reduced-motion media query."


def test_cost_simulator_guardrail2(cost_simulator_content: str):
    """Verify cost-simulator.html displays 0.0% post-filter outlier risk."""
    content = cost_simulator_content
    assert "PACKAGING OUTLIER RISK (POST-FILTER)" in content
    assert "0.0%" in content
    assert "0.0% < 5.0%" in content or "0.0% &lt; 5.0%" in content


def test_cost_simulator_interactive_controls(cost_simulator_content: str):
    """Verify upgraded 3-lever interactive controls in cost-simulator.html."""
    content = cost_simulator_content
    # Lever 1: Implementation Phase Toggle
    assert "Current Baseline (No Changes)" in content
    assert "Phase 1 Only: Auto-Generic E-Prescribing (Days 1-30)" in content
    assert "Phase 1 + Phase 2: Add Outpatient Biosimilars (Days 30-60)" in content
    assert "Full Implementation: Phases 1, 2 &amp; 3 (Days 1-90 - Default Active)" in content or \
           "Full Implementation: Phases 1, 2 & 3 (Days 1-90 - Default Active)" in content

    # Lever 2: Doctor Adoption Rate Selector
    assert "60% Cautious Pilot" in content
    assert "80% Year-1 Hospital Goal" in content
    assert "100% Full Pharmacy Rollout" in content

    # Lever 3: Category Filter and Search
    assert "All Pharmacy Categories" in content
    assert "CNS / ADHD &amp; Mental Health" in content or "CNS / ADHD & Mental Health" in content
    assert "Specialty Biologics &amp; Infusions" in content or "Specialty Biologics & Infusions" in content
    assert "Respiratory &amp; Pulmonary Inhalers" in content or "Respiratory & Pulmonary Inhalers" in content
    assert "Acute Care &amp; Routine Generics" in content or "Acute Care & Routine Generics" in content
    assert "searchInput" in content


def test_cost_simulator_top_kpi_cards(cost_simulator_content: str):
    """Verify 4 upgraded KPI cards showing before vs. after budget numbers in cost-simulator.html."""
    content = cost_simulator_content
    assert "CURRENT TARGET BRAND SPEND" in content
    assert "$3.89M" in content
    assert "Baseline before pharmacy switches" in content

    assert "NEW OPTIMIZED BUDGET" in content
    assert "kpiOptimizedBudget" in content

    assert "ANNUAL HOSPITAL SAVINGS CAPTURED" in content
    assert "+$3.2M" in content or "+$3.20M" in content
    assert "kpiSavingsCaptured" in content

    assert "PATIENT PRESCRIPTION ACCESS KEPT" in content
    assert "100% Covered / &gt;=95% Untouched" in content or "100% Covered / >=95% Untouched" in content


def test_cost_simulator_implementation_charts(cost_simulator_content: str):
    """Verify 3 implementation-focused charts inside cost-simulator.html."""
    content = cost_simulator_content
    # Chart 1: Paired Before vs After Bar Chart
    assert "svgChart1" in content
    assert "Switching Overpriced Brands Cuts Top Drug Category Costs" in content
    assert "Current Spend ($M)" in content
    assert "New Implemented Spend ($M)" in content

    # Chart 2: Step-by-Step Budget Recovery Waterfall
    assert "svgChart2" in content
    assert "How Phases 1 to 3 Recover" in content
    assert "Starting Spend ($3.89M)" in content
    assert "Phase Savings Step-Down" in content
    assert "Final Implemented Budget" in content

    # Chart 3: Monthly Cumulative Savings & Budget Burn-Down Curve
    assert "svgChart3" in content
    assert "12-Month Pharmacy Budget Trajectory: Old Spending Pace vs. New Implemented Plan" in content
    assert "Unchanged Pace" in content or "Unchanged spending pace" in content.lower()
    assert "Implemented Plan" in content or "Implemented spend pace" in content.lower()


def test_cost_simulator_purchasing_switch_table(cost_simulator_content: str):
    """Verify hospital pharmacy implementation table and conditional formatting color bars in cost-simulator.html."""
    content = cost_simulator_content
    # Table Headers
    assert "Drug / Category Name" in content
    assert "Rollout Phase" in content
    assert "Price Hike Driver" in content
    assert "Current Cost / Rx" in content
    assert "New Cost / Rx" in content
    assert "Annual Hospital Savings" in content
    assert "Hospital Action Status" in content

    # Core Target Formulations
    assert "Vyvanse" in content
    assert "Concerta" in content
    assert "Spiriva Respimat" in content
    assert "Advair Diskus" in content
    assert "Banzel" in content
    assert "Jornay PM" in content
    assert "Humira Pen" in content
    assert "Enbrel SureClick" in content
    assert "Ketorolac Tromethamine" in content
    assert "Epinephrine" in content

    # Action status badges
    assert "E-Prescribing Rule Ready" in content
    assert "Biosimilar on Formulary" in content
    assert "Contract Cap Active" in content

    # Conditional color bar element
    assert "savings-bar-fill" in content
    assert "savings-bar-track" in content

