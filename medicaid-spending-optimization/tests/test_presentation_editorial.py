"""
Architecture & Verification Tests for Redesigned Single-Page Editorial Research Whitepaper (index.html).
Validates:
- Warm Archival Paper palette (#FAF8F2, #F4F1EA, #D6D3CD, #111111)
- Google Fonts typography: Newsreader Serif, Plus Jakarta Sans, JetBrains Mono
- Sticky Top Navigation Bar with exact anchor links and CTA button
- 4-Column Bordered KPI Strip with exact verified CMS project metrics
- Hospital Pharmacy Framing: $85.0M hospital budget model, $3.20M annual savings
- Plain-English Analyst Voice: zero forbidden academic jargon terms
- 5 Chapters + Executive Overview (CLEAN framework, Budget Breakdown, Price vs Volume, Savings Plan, 90-Day Rollout)
- Figure containers referencing assets/fig1, assets/fig2, and assets/fig3
- Interactive image lightbox modal with ESC key handling
- Accessibility (prefers-reduced-motion)
- Strict executive restraint: ZERO em dashes and ZERO en dashes across deliverables
- P&T Decision Cockpit (cockpit.html / dashboard.html) synchronization and Guardrail 2 (0.0% outlier risk)
"""

from pathlib import Path
import pytest

INDEX_HTML_PATH = Path("index.html")
COCKPIT_HTML_PATH = Path("cockpit.html")
DASHBOARD_HTML_PATH = Path("dashboard.html")
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
def cockpit_content() -> str:
    assert COCKPIT_HTML_PATH.exists(), "cockpit.html must exist at repository root."
    return COCKPIT_HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def dashboard_content() -> str:
    assert DASHBOARD_HTML_PATH.exists(), "dashboard.html must exist at repository root."
    return DASHBOARD_HTML_PATH.read_text(encoding="utf-8")


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
    assert "sticky-nav" in html_content, "Must contain sticky-nav element."
    assert "JOHN AMORES" in html_content
    assert "HOSPITAL PHARMACY ANALYTICS CASE STUDY" in html_content or "HEALTHCARE ANALYTICS CASE STUDY" in html_content
    assert "OVERVIEW" in html_content or "EXECUTIVE BRIEFING" in html_content
    assert "01. DATA CLEANUP" in html_content or "01. DATA BLIND SPOT" in html_content
    assert "02. BUDGET BREAKDOWN" in html_content or "02. SPEND SKEW" in html_content
    assert "03. PRICE VS VOLUME" in html_content
    assert "04. SAVINGS PLAN" in html_content or "04. SAVINGS WATERFALL" in html_content
    assert "05. 90-DAY ROLLOUT" in html_content or "05. 90-DAY PLAN" in html_content
    assert "LAUNCH SIMULATOR" in html_content or "LAUNCH COCKPIT" in html_content
    assert "cockpit.html" in html_content


def test_hero_header_and_4column_kpi_strip(html_content: str):
    """Verify hero title, subtitle, and 4-column bordered KPI strip with verified metrics."""
    assert "Cutting Hospital Pharmacy Drug Costs Without Limiting Patient Care" in html_content or \
           "Optimizing Medicaid Drug Formulary" in html_content

    # 4 KPI cards
    assert "$111.3B / $85.0M" in html_content or ("$111.3B" in html_content and "$85.0M" in html_content)
    assert "+45.6%" in html_content
    assert "72.2%" in html_content
    assert "+$3.20M" in html_content

    # Verified claims and formulations
    assert "745,555,715" in html_content or "745.6M" in html_content
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


def test_plain_english_analyst_voice(html_content: str):
    """Verify plain-English voice and absence of forbidden academic jargon."""
    forbidden_terms = [
        "econometric decomposition",
        "pareto asymmetry",
        "methodological segregation",
        "censoring",
    ]
    for term in forbidden_terms:
        assert term not in html_content.lower(), f"Forbidden academic term found in index.html: {term}"


def test_figure_assets_and_containers(html_content: str):
    """Verify all three publication figures exist on disk and are linked in index.html."""
    assert FIG1_PATH.exists(), "assets/fig1_spend_concentration.png must exist."
    assert FIG2_PATH.exists(), "assets/fig2_price_volume_matrix.png must exist."
    assert FIG3_PATH.exists(), "assets/fig3_formulary_waterfall.png must exist."

    assert "assets/fig1_spend_concentration.png" in html_content
    assert "assets/fig2_price_volume_matrix.png" in html_content
    assert "assets/fig3_formulary_waterfall.png" in html_content

    # Statistical validation strip strings
    assert "Chi-Square" in html_content
    assert "Wilcoxon W = 252.0" in html_content
    assert "Result" in html_content or "28.3%" in html_content


def test_verified_analytical_findings_and_tables(html_content: str):
    """Verify verified figures and tables in Chapter 01 to Chapter 05."""
    # Chapter 01
    assert "Raw CMS Extract" in html_content
    assert "Validated Active Formulary" in html_content
    assert "18,511" in html_content

    # Chapter 02
    assert "90.19%" in html_content or "90.2%" in html_content
    assert "9.81%" in html_content or "9.8%" in html_content
    assert "407.87" in html_content or "$408" in html_content
    assert "21.86" in html_content or "$22" in html_content

    # Chapter 03
    assert "Ozempic" in html_content
    assert "928.7%" in html_content
    assert "Trulicity" in html_content
    assert "+106.6%" in html_content

    # Chapter 04
    assert "$3.89M" in html_content
    assert "$1.10M" in html_content
    assert "$2.79M" in html_content
    assert "$1.92M" in html_content
    assert "$2.56M" in html_content

    # Chapter 05
    for drug in ["Vyvanse", "Concerta", "Spiriva Respimat", "Advair Diskus", "Banzel", "Jornay PM"]:
        assert drug in html_content, f"Must include target drug {drug} in Chapter 05 roadmap."


def test_zero_em_and_en_dashes(html_content: str, cockpit_content: str, dashboard_content: str, readme_content: str):
    """Enforce executive restraint rule: zero em dashes and zero en dashes across deliverables."""
    files_to_check = [
        ("index.html", html_content),
        ("cockpit.html", cockpit_content),
        ("dashboard.html", dashboard_content),
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


def test_cockpit_and_dashboard_guardrail2(cockpit_content: str, dashboard_content: str):
    """Verify cockpit.html and dashboard.html display 0.0% post-filter outlier risk."""
    for name, content in [("cockpit.html", cockpit_content), ("dashboard.html", dashboard_content)]:
        assert "PACKAGING OUTLIER RISK (POST-FILTER)" in content
        assert "0.0%" in content
        assert "0.0% < 5.0%" in content or "0.0% &lt; 5.0%" in content


def test_cockpit_interactive_controls(cockpit_content: str, dashboard_content: str):
    """Verify upgraded 3-lever interactive controls across cockpit and dashboard."""
    for name, content in [("cockpit.html", cockpit_content), ("dashboard.html", dashboard_content)]:
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


def test_cockpit_top_kpi_cards(cockpit_content: str, dashboard_content: str):
    """Verify 4 upgraded KPI cards showing before vs. after budget numbers."""
    for name, content in [("cockpit.html", cockpit_content), ("dashboard.html", dashboard_content)]:
        assert "CURRENT TARGET BRAND SPEND" in content
        assert "$3.89M" in content
        assert "Baseline before pharmacy switches" in content

        assert "NEW OPTIMIZED BUDGET" in content
        assert "kpiOptimizedBudget" in content

        assert "ANNUAL HOSPITAL SAVINGS CAPTURED" in content
        assert "+$3.20M" in content
        assert "kpiSavingsCaptured" in content

        assert "PATIENT PRESCRIPTION ACCESS KEPT" in content
        assert "100% Covered / &gt;=95% Untouched" in content or "100% Covered / >=95% Untouched" in content


def test_cockpit_implementation_charts(cockpit_content: str, dashboard_content: str):
    """Verify 3 implementation-focused charts inside cockpit and dashboard."""
    for name, content in [("cockpit.html", cockpit_content), ("dashboard.html", dashboard_content)]:
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


def test_cockpit_purchasing_switch_table(cockpit_content: str, dashboard_content: str):
    """Verify hospital pharmacy implementation table and conditional formatting color bars."""
    for name, content in [("cockpit.html", cockpit_content), ("dashboard.html", dashboard_content)]:
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

