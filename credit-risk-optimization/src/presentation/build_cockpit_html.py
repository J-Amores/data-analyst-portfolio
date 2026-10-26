"""
src/presentation/build_cockpit_html.py
Consumer Credit Risk & Underwriting Optimization
Phase 4: Standalone Underwriting Decision Workstation (cockpit.html)
Refactored into a focused Live Underwriting Desk Workstation following
Christine Jiang's 'Clarity Over Complexity' principle.

Strict zero em dashes, zero en dashes.
"""

from pathlib import Path
import json


def build_cockpit_html():
    cube_path = Path("data/exports/cockpit_cube.json")
    if not cube_path.exists():
        raise FileNotFoundError(f"Missing cube data: {cube_path}")

    with open(cube_path, "r", encoding="utf-8") as f:
        cube_json_str = f.read().strip()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Underwriting Decision Workstation | John Amores</title>
  
  <!-- Typography: High-Contrast Editorial Serif + Crisp Sans + Tabular Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg-paper: #FAF8F2;
      --bg-paper-alt: #F3EFE6;
      --bg-card: #FFFFFF;
      --ink-black: #111111;
      --ink-muted: #4A4843;
      --ink-subtle: #76746E;
      --border-color: #111111;
      --hairline: 1px solid var(--border-color);
      --color-green: #15803D;
      --color-green-light: #F0FDF4;
      --color-crimson: #BE123C;
      --color-crimson-light: #FFF1F2;
      --color-amber: #B45309;
      --color-amber-light: #FEF3C7;
      --color-charcoal: #27272A;
      --content-width: 1240px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    ::selection {{
      background: #111111;
      color: #FAF8F2;
    }}

    body {{
      background-color: var(--bg-paper);
      color: var(--ink-black);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 15px;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }}

    /* Top Sticky Navigation Header */
    .top-nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(250, 248, 242, 0.96);
      backdrop-filter: blur(8px);
      border-bottom: var(--hairline);
    }}

    .top-nav-inner {{
      max-width: var(--content-width);
      margin: 0 auto;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .nav-badge {{
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-green);
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}

    .nav-links a {{
      color: var(--ink-black);
      text-decoration: none;
      transition: opacity 140ms ease;
    }}

    .nav-links a:hover {{
      opacity: 0.65;
    }}

    .nav-btn {{
      padding: 6px 14px;
      background: var(--ink-black);
      color: var(--bg-paper) !important;
      border: var(--hairline);
      border-radius: 4px;
      white-space: nowrap;
      transition: background 140ms ease, color 140ms ease;
    }}

    .nav-btn:hover {{
      background: #27272A;
      opacity: 1 !important;
    }}

    /* Layout Wrapper */
    .cockpit-container {{
      max-width: var(--content-width);
      margin: 0 auto;
      padding: 24px 24px 64px 24px;
    }}

    /* Hero Section */
    .cockpit-hero {{
      padding: 16px 0 20px 0;
      border-bottom: var(--hairline);
      margin-bottom: 24px;
    }}

    .hero-tag {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--ink-muted);
      margin-bottom: 10px;
    }}

    .hero-tag span {{
      display: inline-block;
      padding: 2px 8px;
      border: var(--hairline);
      background: var(--bg-paper-alt);
    }}

    .hero-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(2.3rem, 4.2vw, 3.6rem);
      font-weight: 400;
      line-height: 1.05;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}

    .hero-subtitle {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(1.15rem, 1.8vw, 1.4rem);
      font-style: italic;
      color: var(--ink-muted);
      line-height: 1.4;
      margin-bottom: 14px;
    }}

    .meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      color: var(--ink-muted);
      border-top: var(--hairline);
      padding-top: 10px;
    }}

    .meta-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Section Headings */
    .section-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 1.65rem;
      font-weight: 400;
      line-height: 1.2;
    }}

    .section-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: var(--ink-muted);
      text-transform: uppercase;
    }}

    /* ============================================================== */
    /* 1. SAMPLE APPLICANT QUEUE BAR                                  */
    /* ============================================================== */
    .queue-section {{
      margin-bottom: 24px;
    }}

    .queue-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}

    .queue-title {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--ink-black);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .queue-hint {{
      font-size: 0.72rem;
      color: var(--ink-muted);
    }}

    .queue-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
    }}

    .queue-card-btn {{
      background: var(--bg-card);
      border: var(--hairline);
      padding: 12px 14px;
      cursor: pointer;
      text-align: left;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 110px;
      transition: all 140ms ease;
      position: relative;
    }}

    .queue-card-btn:hover {{
      background: var(--bg-paper-alt);
    }}

    .queue-card-btn.active {{
      background: var(--ink-black);
      color: var(--bg-paper);
      border-color: var(--ink-black);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    }}

    .queue-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 6px;
    }}

    .queue-card-id {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
    }}

    .queue-card-btn.active .queue-card-id {{
      color: #FFFFFF;
    }}

    .queue-card-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 2px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .queue-tag-prime {{
      background: var(--color-green-light);
      color: var(--color-green);
      border: 1px solid var(--color-green);
    }}

    .queue-tag-amber {{
      background: var(--color-amber-light);
      color: var(--color-amber);
      border: 1px solid var(--color-amber);
    }}

    .queue-tag-crimson {{
      background: var(--color-crimson-light);
      color: var(--color-crimson);
      border: 1px solid var(--color-crimson);
    }}

    .queue-card-btn.active .queue-card-tag {{
      background: rgba(255, 255, 255, 0.20);
      color: #FFFFFF;
      border-color: rgba(255, 255, 255, 0.45);
    }}

    .queue-card-name {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.78rem;
      font-weight: 700;
      line-height: 1.25;
      margin-bottom: 6px;
    }}

    .queue-card-btn.active .queue-card-name {{
      color: #FFFFFF;
    }}

    .queue-card-meta {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: var(--ink-muted);
      line-height: 1.35;
    }}

    .queue-card-btn.active .queue-card-meta {{
      color: #D1D5DB;
    }}

    .queue-card-verdict {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.62rem;
      font-weight: 700;
      margin-top: 6px;
      display: inline-block;
    }}

    .queue-card-btn.active .queue-card-verdict {{
      color: #FBBF24;
    }}

    /* ============================================================== */
    /* 2. MAIN TOOL: APPLICANT DESK TESTER WORKSTATION                */
    /* ============================================================== */
    .main-tool-card {{
      background: var(--bg-card);
      border: 2px solid var(--border-color);
      padding: 24px 28px;
      margin-bottom: 32px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }}

    .desk-title-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 16px;
      padding-bottom: 14px;
      border-bottom: var(--hairline);
    }}

    .engine-mode-toggle {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .mode-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--ink-muted);
    }}

    .toggle-buttons {{
      display: inline-flex;
      border: var(--hairline);
      background: var(--bg-paper);
      border-radius: 4px;
      overflow: hidden;
    }}

    .mode-btn {{
      padding: 6px 13px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.70rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--ink-black);
      cursor: pointer;
      transition: all 120ms ease;
    }}

    .mode-btn.active {{
      background: var(--ink-black);
      color: var(--bg-paper);
    }}

    .mode-btn:hover:not(.active) {{
      background: var(--bg-paper-alt);
    }}

    .main-tool-grid {{
      display: grid;
      grid-template-columns: 1.05fr 1fr;
      gap: 28px;
      margin-top: 10px;
    }}

    /* Form Fields */
    .form-group {{
      margin-bottom: 16px;
    }}

    .form-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 14px;
    }}

    .input-label {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .input-val-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--ink-black);
    }}

    .text-input, .select-input {{
      width: 100%;
      padding: 8px 12px;
      border: var(--hairline);
      background: var(--bg-paper);
      color: var(--ink-black);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      border-radius: 3px;
    }}

    .text-input:focus, .select-input:focus {{
      outline: none;
      border-color: var(--ink-black);
      background: #FFFFFF;
    }}

    .slider-input {{
      width: 100%;
      accent-color: var(--ink-black);
      cursor: pointer;
    }}

    /* FICO Band Spectrum Component */
    .fico-spectrum-container {{
      margin-top: 8px;
      background: var(--bg-paper);
      border: var(--hairline);
      padding: 10px 12px;
      border-radius: 3px;
      position: relative;
    }}

    .fico-spectrum-bar {{
      display: grid;
      grid-template-columns: 0.8fr 1.6fr 1.4fr 1.2fr 1fr 0.9fr;
      gap: 2px;
      height: 24px;
      position: relative;
      margin-bottom: 8px;
      border: var(--hairline);
    }}

    .fico-band-segment {{
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.64rem;
      font-weight: 700;
      color: var(--ink-black);
      background: var(--bg-paper-alt);
      transition: all 120ms ease;
      cursor: pointer;
      user-select: none;
    }}

    .fico-band-segment.active {{
      background: var(--ink-black) !important;
      color: var(--bg-paper) !important;
    }}

    .spectrum-cutoff-line {{
      position: absolute;
      left: 36.5%;
      top: -6px;
      bottom: -6px;
      width: 2px;
      background: var(--color-crimson);
      z-index: 10;
    }}

    .spectrum-cutoff-tag {{
      position: absolute;
      top: -18px;
      left: -38px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem;
      font-weight: 700;
      color: var(--color-crimson);
      white-space: nowrap;
      background: var(--bg-paper);
      padding: 0 4px;
      border: 1px solid var(--color-crimson);
    }}

    .band-callout-card {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.70rem;
      color: var(--ink-muted);
      padding-top: 6px;
      border-top: 1px dashed #D5D1C8;
    }}

    .band-stat-pill {{
      display: inline-block;
      padding: 1px 6px;
      border: var(--hairline);
      background: var(--bg-card);
      font-weight: 700;
      color: var(--ink-black);
    }}

    /* Loan Amount Presets */
    .preset-pills {{
      display: flex;
      gap: 6px;
      margin-top: 6px;
    }}

    .pill-btn {{
      padding: 3px 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 600;
      background: var(--bg-paper);
      border: var(--hairline);
      border-radius: 2px;
      cursor: pointer;
    }}

    .pill-btn:hover {{
      background: var(--bg-paper-alt);
    }}

    .btn-choice {{
      padding: 6px 11px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.73rem;
      font-weight: 600;
      background: var(--bg-paper);
      color: var(--ink-black);
      border: var(--hairline);
      border-radius: 3px;
      cursor: pointer;
      transition: all 120ms ease;
    }}

    .btn-choice:hover {{
      background: var(--bg-paper-alt);
    }}

    .btn-choice.active {{
      background: var(--ink-black);
      color: var(--bg-paper);
      border-color: var(--ink-black);
    }}

    /* Right Column: Underwriting Predictor Memorandum */
    .predictor-memo {{
      border: var(--hairline);
      background: var(--bg-paper);
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.03);
    }}

    .memo-header {{
      border-bottom: var(--hairline);
      padding-bottom: 12px;
      margin-bottom: 14px;
    }}

    .memo-eyebrow {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--ink-muted);
      margin-bottom: 6px;
    }}

    .ticket-status-badge {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      font-weight: 700;
      padding: 6px 12px;
      border: var(--hairline);
      border-radius: 3px;
      text-transform: uppercase;
      margin-bottom: 10px;
    }}

    .status-declined {{
      background: var(--color-crimson);
      color: #FFFFFF;
      border-color: var(--color-crimson);
    }}

    .status-conditional {{
      background: var(--color-amber);
      color: #FFFFFF;
      border-color: var(--color-amber);
    }}

    .status-approved {{
      background: var(--color-green);
      color: #FFFFFF;
      border-color: var(--color-green);
    }}

    .profitability-verdict-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 1.30rem;
      font-weight: 700;
      line-height: 1.25;
      margin-bottom: 8px;
    }}

    .verdict-profitable {{
      color: var(--color-green);
    }}

    .verdict-conditional {{
      color: var(--color-amber);
    }}

    .verdict-unprofitable {{
      color: var(--color-crimson);
    }}

    .ticket-rationale {{
      font-size: 0.80rem;
      line-height: 1.5;
      color: var(--ink-black);
    }}

    /* Financial Metrics 4-Box Grid */
    .memo-metrics-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-bottom: 14px;
    }}

    .memo-metric-box {{
      background: var(--bg-card);
      border: var(--hairline);
      padding: 9px 11px;
    }}

    .memo-metric-title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.64rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--ink-muted);
      margin-bottom: 3px;
    }}

    .memo-metric-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--ink-black);
    }}

    .memo-metric-sub {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.64rem;
      color: var(--ink-muted);
      margin-top: 2px;
    }}

    /* Rules Checklist */
    .rules-list {{
      border-top: var(--hairline);
      padding-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }}

    .rule-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.70rem;
    }}

    .rule-name {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 600;
      color: var(--ink-muted);
    }}

    .rule-result {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }}

    /* ============================================================== */
    /* 3. COMPACT 4-CARD PORTFOLIO POLICY IMPACT FOOTER STRIP         */
    /* ============================================================== */
    .portfolio-impact-section {{
      border-top: 2px solid var(--border-color);
      padding-top: 24px;
      margin-top: 8px;
    }}

    .impact-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}

    .impact-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-top: 14px;
      margin-bottom: 28px;
    }}

    .impact-card {{
      background: var(--bg-card);
      border: var(--hairline);
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }}

    .impact-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .impact-card-title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--ink-muted);
    }}

    .impact-card-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.60rem;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 2px;
      text-transform: uppercase;
    }}

    .badge-pass {{
      background: var(--color-green-light);
      color: var(--color-green);
      border: 1px solid var(--color-green);
    }}

    .badge-warn {{
      background: var(--color-amber-light);
      color: var(--color-amber);
      border: 1px solid var(--color-amber);
    }}

    .impact-card-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.55rem;
      font-weight: 700;
      line-height: 1.15;
      letter-spacing: -0.02em;
      color: var(--ink-black);
      margin-bottom: 6px;
    }}

    .impact-card-desc {{
      font-size: 0.75rem;
      line-height: 1.45;
      color: var(--ink-muted);
    }}

    /* Footer */
    .cockpit-footer {{
      border-top: var(--hairline);
      padding-top: 20px;
      font-size: 0.74rem;
      color: var(--ink-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    @media (max-width: 1024px) {{
      .main-tool-grid {{
        grid-template-columns: 1fr;
      }}
      .queue-grid {{
        grid-template-columns: repeat(3, 1fr);
      }}
      .impact-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 640px) {{
      .queue-grid {{
        grid-template-columns: 1fr;
      }}
      .impact-grid {{
        grid-template-columns: 1fr;
      }}
      .top-nav-inner {{
        flex-direction: column;
        gap: 8px;
      }}
      .desk-title-bar {{
        flex-direction: column;
        align-items: flex-start;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Sticky Navigation Header -->
  <header class="top-nav">
    <div class="top-nav-inner">
      <div class="nav-brand">
        <span class="nav-badge"></span>
        <span>JOHN AMORES | UNDERWRITING DECISION WORKSTATION</span>
      </div>
      <div class="nav-links">
        <a href="#applicant-desk" style="border-bottom: 2px solid var(--ink-black); padding-bottom: 2px;">LIVE APPLICANT DESK TESTER</a>
        <a href="#borrower-queue">SAMPLE BORROWER QUEUE</a>
        <a href="#portfolio-impact">PORTFOLIO GUARDRAIL BENCHMARKS</a>
        <a href="index.html" class="nav-btn">&lt;- BACK TO EXECUTIVE REPORT</a>
      </div>
    </div>
  </header>

  <div class="cockpit-container">

    <!-- Hero Header -->
    <header class="cockpit-hero">
      <div class="hero-tag">
        <span>EXECUTIVE UNDERWRITING WORKSTATION</span>
        <span>100% STANDALONE AUDIT DECK</span>
      </div>
      <h1 class="hero-title">Underwriting Decision Cockpit</h1>
      <p class="hero-subtitle">Single-Screen Live Underwriting Desk &amp; Empirical Multi-Variable Policy Engine</p>
      <div class="meta-bar">
        <div class="meta-item"><strong>Empirical Dataset:</strong> 1,345,350 Seasoned Loans</div>
        <div class="meta-item"><strong>Platform Capital:</strong> $19.39B</div>
        <div class="meta-item"><strong>Baseline Subprime Losses:</strong> $1,404.1M</div>
        <div class="meta-item"><strong>Decision Engine:</strong> Phase 1-3 Multi-Variable Policy Rules</div>
        <div class="meta-item"><strong>Subgrades:</strong> 35 Historical Tiers (A1 to G5)</div>
      </div>
    </header>

    <!-- ============================================================== -->
    <!-- 1. SAMPLE APPLICANT QUEUE BAR (5 ONE-CLICK BORROWER PROFILES) -->
    <!-- ============================================================== -->
    <section class="queue-section" id="borrower-queue">
      <div class="queue-header-row">
        <div class="queue-title">
          <span>SAMPLE APPLICANT QUEUE (5 ONE-CLICK BORROWER PROFILES)</span>
        </div>
        <div class="queue-hint">Click any profile below to test active underwriting rules in real time:</div>
      </div>

      <div class="queue-grid">
        <!-- Profile 1: Prime -->
        <button type="button" class="queue-card-btn" id="qcard-104" onclick="loadApplicantProfile('104')">
          <div class="queue-card-top">
            <span class="queue-card-id">#104</span>
            <span class="queue-card-tag queue-tag-prime">PRIME BENCHMARK</span>
          </div>
          <div class="queue-card-name">Applicant #104: Prime Consolidation</div>
          <div class="queue-card-meta">FICO 715 | Grade B2 | $16,000<br>36m | DTI 15% | Util 32%</div>
          <div class="queue-card-verdict" style="color:var(--color-green);">APPROVED: Prime Standard Terms</div>
        </button>

        <!-- Profile 2: Subgrade C4 (Default Load) -->
        <button type="button" class="queue-card-btn active" id="qcard-208" onclick="loadApplicantProfile('208')">
          <div class="queue-card-top">
            <span class="queue-card-id">#208</span>
            <span class="queue-card-tag queue-tag-amber">DEFAULT LOAD</span>
          </div>
          <div class="queue-card-name">Applicant #208: Subgrade C4 Margin Leak</div>
          <div class="queue-card-meta">FICO 680 | Grade C4 | $15,000<br>36m | DTI 22% | Util 54%</div>
          <div class="queue-card-verdict" style="color:var(--color-amber);">CONDITIONAL: Re-Priced (+150 bps)</div>
        </button>

        <!-- Profile 3: Phase 1 Dual-Risk Hard Stop -->
        <button type="button" class="queue-card-btn" id="qcard-312" onclick="loadApplicantProfile('312')">
          <div class="queue-card-top">
            <span class="queue-card-id">#312</span>
            <span class="queue-card-tag queue-tag-crimson">DUAL-RISK STOP</span>
          </div>
          <div class="queue-card-name">Applicant #312: Phase 1 Dual-Risk Hard-Stop</div>
          <div class="queue-card-meta">FICO 662 | Grade D3 | $18,000<br>36m | DTI 29% | Util 74%</div>
          <div class="queue-card-verdict" style="color:var(--color-crimson);">DECLINED: Dual-Risk Hard-Stop</div>
        </button>

        <!-- Profile 4: 5-Year Term Cap Trigger -->
        <button type="button" class="queue-card-btn" id="qcard-419" onclick="loadApplicantProfile('419')">
          <div class="queue-card-top">
            <span class="queue-card-id">#419</span>
            <span class="queue-card-tag queue-tag-amber">DURATION HAZARD</span>
          </div>
          <div class="queue-card-name">Applicant #419: 5-Year Term Cap Trigger</div>
          <div class="queue-card-meta">FICO 668 | Grade D1 | $20,000<br>60m | DTI 19% | Util 48%</div>
          <div class="queue-card-verdict" style="color:var(--color-amber);">CONDITIONAL: Term Capped to 36m</div>
        </button>

        <!-- Profile 5: Small Business Verification -->
        <button type="button" class="queue-card-btn" id="qcard-505" onclick="loadApplicantProfile('505')">
          <div class="queue-card-top">
            <span class="queue-card-id">#505</span>
            <span class="queue-card-tag queue-tag-amber">COMMERCIAL AUDIT</span>
          </div>
          <div class="queue-card-name">Applicant #505: Small Business Verification</div>
          <div class="queue-card-meta">FICO 690 | Grade C2 | $25,000<br>36m | DTI 18% | Util 42%</div>
          <div class="queue-card-verdict" style="color:var(--color-amber);">CONDITIONAL: IRS Tax Audit Required</div>
        </button>
      </div>
    </section>

    <!-- ============================================================== -->
    <!-- 2. MAIN TOOL: 01 LIVE APPLICANT DESK TESTER                    -->
    <!-- ============================================================== -->
    <section class="main-tool-card" id="applicant-desk">
      
      <!-- Section Title & Policy Engine Mode Toggle -->
      <div class="desk-title-bar">
        <div>
          <div class="section-title">
            <span>01 LIVE APPLICANT DESK TESTER</span>
          </div>
          <div class="section-num">REAL-TIME PRODUCTION UNDERWRITING &amp; PROFITABILITY PREDICTOR</div>
        </div>

        <!-- Mode Toggle Switch -->
        <div class="engine-mode-toggle">
          <span class="mode-label">Policy Engine Mode:</span>
          <div class="toggle-buttons">
            <button type="button" class="mode-btn active" id="mode-active-btn" onclick="setPolicyMode('active')">
              Active: Phase 1-3 Guardrails ON
            </button>
            <button type="button" class="mode-btn" id="mode-legacy-btn" onclick="setPolicyMode('legacy')">
              Legacy: Unfiltered Baseline
            </button>
          </div>
        </div>
      </div>

      <p style="font-size: 0.86rem; color: var(--ink-muted); line-height: 1.5; margin-bottom: 14px;">
        Dial in a loan applicant profile or select from the queue above. The underwriting engine evaluates historical cohort default probability, calculates platform net LAROC return against our +4.00% executive hurdle, and renders an instant profitability verdict.
      </p>

      <div class="main-tool-grid">

        <!-- Left Column: Borrower Input Dials -->
        <div>
          <!-- 1. Credit Score (FICO) Input & Spectrum -->
          <div class="form-group">
            <div class="input-label">
              <span>Borrower Credit Score (FICO)</span>
              <span class="input-val-badge" id="desk-fico-display">680 FICO</span>
            </div>
            <input type="range" id="desk-fico" min="600" max="850" step="1" value="680" class="slider-input" oninput="handleFicoChange(this.value)">

            <!-- Visual FICO Band Spectrum Indicator with Cutoff Line -->
            <div class="fico-spectrum-container">
              <div style="font-size:0.68rem; font-weight:700; text-transform:uppercase; margin-bottom:6px; display:flex; justify-content:space-between;">
                <span>Empirical Credit Score Spectrum</span>
                <span id="band-active-name" style="color:var(--ink-black);">680-699 Lower Prime</span>
              </div>
              <div class="fico-spectrum-bar" id="fico-spectrum-bar">
                <div class="fico-band-segment" id="band-seg-0" onclick="setFicoVal(640)">&lt;660</div>
                <div class="fico-band-segment" id="band-seg-1" onclick="setFicoVal(670)">660-679</div>
                <div class="fico-band-segment active" id="band-seg-2" onclick="setFicoVal(690)">680-699</div>
                <div class="fico-band-segment" id="band-seg-3" onclick="setFicoVal(710)">700-719</div>
                <div class="fico-band-segment" id="band-seg-4" onclick="setFicoVal(735)">720-749</div>
                <div class="fico-band-segment" id="band-seg-5" onclick="setFicoVal(770)">750+</div>

                <!-- Red Cutoff Line Marker on Spectrum -->
                <div class="spectrum-cutoff-line">
                  <span class="spectrum-cutoff-tag">CUTOFF: 685 FICO</span>
                </div>
              </div>
              <div class="band-callout-card">
                <div>Portfolio Share: <span class="band-stat-pill" id="band-stat-share">26.86% (361.3K loans)</span></div>
                <div>Default Rate: <span class="band-stat-pill" id="band-stat-bad">21.44%</span></div>
                <div>Net LAROC: <span class="band-stat-pill" id="band-stat-laroc">+4.47%</span></div>
              </div>
            </div>
          </div>

          <!-- 2. Loan Amount & Term Limits -->
          <div class="form-row">
            <div>
              <div class="input-label">
                <span>Loan Amount ($)</span>
                <span class="input-val-badge" id="desk-amount-val">$15,000</span>
              </div>
              <input type="number" id="desk-amount" class="text-input" min="1000" max="40000" step="500" value="15000" onchange="document.getElementById('desk-amount-slider').value = this.value; updateApplicantDesk();">
              <input type="range" id="desk-amount-slider" min="1000" max="40000" step="500" value="15000" class="slider-input" style="margin-top:6px;" oninput="document.getElementById('desk-amount').value = this.value; document.getElementById('desk-amount-val').innerText = '$' + parseInt(this.value).toLocaleString(); updateApplicantDesk();">
              <div class="preset-pills">
                <button type="button" class="pill-btn" onclick="setAmountVal(5000)">$5K</button>
                <button type="button" class="pill-btn" onclick="setAmountVal(10000)">$10K</button>
                <button type="button" class="pill-btn" onclick="setAmountVal(15000)">$15K</button>
                <button type="button" class="pill-btn" onclick="setAmountVal(20000)">$20K</button>
                <button type="button" class="pill-btn" onclick="setAmountVal(25000)">$25K</button>
              </div>
            </div>

            <div>
              <div class="input-label">
                <span>Term Limits</span>
                <span class="input-val-badge" id="desk-term-val">36 Months</span>
              </div>
              <div style="display:flex; gap:8px; margin-bottom:8px;">
                <button type="button" class="btn-choice active" id="desk-term-36" onclick="setApplicantTerm(36)">36 Months</button>
                <button type="button" class="btn-choice" id="desk-term-60" onclick="setApplicantTerm(60)">60 Months</button>
              </div>
              <div style="font-size:0.67rem; color:var(--ink-muted); line-height:1.35;">
                <strong>Governance Rule:</strong> 60-month notes suffer 32.45% defaults vs 16.00% on 36-month terms. Policy caps duration to 36m unless FICO &gt;= 680.
              </div>
            </div>
          </div>

          <!-- 3. Subgrade Mapping & Purpose -->
          <div class="form-row">
            <div>
              <label class="input-label" for="desk-subgrade">
                <span>Credit Subgrade (A1-G5)</span>
                <span id="desk-subgrade-hint" style="font-size:0.65rem; color:var(--ink-muted);">Auto-Mapped</span>
              </label>
              <select id="desk-subgrade" class="select-input" onchange="updateApplicantDesk()">
                <!-- Populated via JS -->
              </select>
            </div>
            <div>
              <label class="input-label" for="desk-purpose">Loan Purpose</label>
              <select id="desk-purpose" class="select-input" onchange="updateApplicantDesk()">
                <option value="debt_consolidation" selected>Debt Consolidation</option>
                <option value="credit_card">Credit Card Refinancing</option>
                <option value="home_improvement">Home Improvement</option>
                <option value="small_business">Small Business</option>
                <option value="major_purchase">Major Purchase</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          <!-- 4. Monthly Debt Ratio (DTI) & Credit Card Usage (Revol Util) -->
          <div class="form-row">
            <div>
              <div class="input-label">
                <span>Monthly DTI Ratio</span>
                <span class="input-val-badge" id="desk-dti-val">22% [Moderate]</span>
              </div>
              <input type="range" id="desk-dti" min="1" max="50" step="1" value="22" class="slider-input" oninput="handleDtiSlider(this.value)">
              <div style="font-size:0.66rem; color:var(--ink-muted); margin-top:2px;">Threshold: &gt; 25% triggers multi-variable risk filter.</div>
            </div>
            <div>
              <div class="input-label">
                <span>Card Usage (Revol Util)</span>
                <span class="input-val-badge" id="desk-util-val">54% [Moderate]</span>
              </div>
              <input type="range" id="desk-util" min="1" max="100" step="1" value="54" class="slider-input" oninput="handleUtilSlider(this.value)">
              <div style="font-size:0.66rem; color:var(--ink-muted); margin-top:2px;">Threshold: &gt; 65% triggers multi-variable risk filter.</div>
            </div>
          </div>

        </div>

        <!-- Right Column: Live Underwriting Profitability Predictor Memo -->
        <div class="predictor-memo">
          <div class="memo-header">
            <div class="memo-eyebrow">OFFICIAL UNDERWRITING DECISION MEMORANDUM</div>
            <div class="ticket-status-badge status-conditional" id="ticket-badge">[CONDITIONAL APPROVAL: PHASE 2 RE-PRICED (+150 BPS)]</div>
            <div class="profitability-verdict-title verdict-conditional" id="verdict-title">
              CONDITIONALLY PROFITABLE (+4.29% LAROC WITH +150 BPS REPRICING)
            </div>
            <p class="ticket-rationale" id="ticket-rationale">
              Baseline returns for Subgrade C4 sit below our +4.00% profit hurdle (+3.44% baseline). Phase 2 policy applies a +150 bps interest rate spread (+1.50% APR), lifting projected return to +4.29% (+4.00% hurdle met!). Approved subject to contractual re-pricing.
            </p>
          </div>

          <!-- Key Underwriting Profitability Metrics Grid -->
          <div class="memo-metrics-grid">
            <div class="memo-metric-box">
              <div class="memo-metric-title">Expected Platform Return (LAROC)</div>
              <div class="memo-metric-num" id="ticket-laroc" style="color:var(--color-green);">+4.29%</div>
              <div class="memo-metric-sub" id="ticket-laroc-hurdle">Meets Hurdle (&gt;= +4.00%)</div>
            </div>
            <div class="memo-metric-box">
              <div class="memo-metric-title">Projected Lifetime Value / Savings</div>
              <div class="memo-metric-num" id="ticket-profit-dollars" style="color:var(--color-green);">+$644 Net Profit</div>
              <div class="memo-metric-sub" id="ticket-profit-sub">Expected Cash Flow Impact</div>
            </div>
            <div class="memo-metric-box">
              <div class="memo-metric-title">Historical Cohort Bad Rate</div>
              <div class="memo-metric-num" id="ticket-bad-rate">24.92%</div>
              <div class="memo-metric-sub" id="ticket-bad-rate-sub">Cohort terminal charge-off probability</div>
            </div>
            <div class="memo-metric-box">
              <div class="memo-metric-title">Recommended Contract APR</div>
              <div class="memo-metric-num" id="ticket-apr">16.21%</div>
              <div class="memo-metric-sub" id="ticket-payment-sub">Monthly Installment: $528.84</div>
            </div>
          </div>

          <!-- Policy Governance Checkpoints Checklist -->
          <div class="rules-list">
            <div class="rule-item">
              <span class="rule-name">Rule 1: Phase 1 Subprime Hard Stop (Grades D-G, DTI &gt; 25%, Revol &gt; 65%)</span>
              <span class="rule-result" id="rule-hardstop" style="color:var(--color-green);">CLEAR (NON-BREACH)</span>
            </div>
            <div class="rule-item">
              <span class="rule-name">Rule 2: Phase 2 Subgrade C4 Yield Re-Pricing (+150 bps Spread)</span>
              <span class="rule-result" id="rule-repricing" style="color:var(--color-amber);">APPLIED (+150 BPS)</span>
            </div>
            <div class="rule-item">
              <span class="rule-name">Rule 3: Phase 2 60-Month Duration Volatility Cap (680+ FICO Required)</span>
              <span class="rule-result" id="rule-termcap" style="color:var(--color-green);">CLEAR (36M TERM)</span>
            </div>
            <div class="rule-item">
              <span class="rule-name">Rule 4: Phase 3 Small Business Revenue Verification (IRS Form 4506-C)</span>
              <span class="rule-result" id="rule-bizaudit" style="color:var(--color-green);">STANDARD DISBURSEMENT</span>
            </div>
            <div class="rule-item">
              <span class="rule-name">Rule 5: Platform Solvency &amp; Capital Volume Floor (&gt;= 80.0% Preserved)</span>
              <span class="rule-result" id="rule-volumeguard" style="color:var(--color-green);">COMPLIANT (95.81% KEPT)</span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- ============================================================== -->
    <!-- 3. COMPACT 4-CARD PORTFOLIO POLICY IMPACT FOOTER STRIP         -->
    <!-- ============================================================== -->
    <section class="portfolio-impact-section" id="portfolio-impact">
      <div class="impact-header-row">
        <div>
          <div class="section-title">
            <span>02 PORTFOLIO-WIDE IMPACT OF ACTIVE RULES (1,345,350 SEASONED LOANS)</span>
          </div>
          <div class="section-num">AUDITED HISTORICAL PORTFOLIO PERFORMANCE</div>
        </div>
      </div>
      <p style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 4px;">
        Audited historical performance of the 4 underwriting rules when applied to the complete $19.39B seasoned origination book.
      </p>

      <div class="impact-grid">
        <!-- Card 1 -->
        <div class="impact-card">
          <div class="impact-card-header">
            <span class="impact-card-title">Rule 1: Phase 1 Dual-Risk Cutoff</span>
            <span class="impact-card-tag badge-pass">18,548 DEFAULTS</span>
          </div>
          <div class="impact-card-num">+$230.04M Saved</div>
          <p class="impact-card-desc">
            Auto-declining Grades D-G with DTI &gt; 25% &amp; Card Usage &gt; 65% eliminates 18,548 defaults ($254.10M gross).
          </p>
        </div>

        <!-- Card 2 -->
        <div class="impact-card">
          <div class="impact-card-header">
            <span class="impact-card-title">Rule 2: Phase 2 Subgrade C4 Repricing</span>
            <span class="impact-card-tag badge-pass">74,422 LOANS</span>
          </div>
          <div class="impact-card-num">+$14.20M Revenue</div>
          <p class="impact-card-desc">
            Adding +150 bps (+1.50% APR) across 74,422 Subgrade C4 loans restores the +4.00% profit hurdle.
          </p>
        </div>

        <!-- Card 3 -->
        <div class="impact-card">
          <div class="impact-card-header">
            <span class="impact-card-title">Rule 3 &amp; 4: Volume &amp; Return Guardrails</span>
            <span class="impact-card-tag badge-pass">GUARDRAILS MET</span>
          </div>
          <div class="impact-card-num">95.81% Volume Kept</div>
          <p class="impact-card-desc">
            Preserves $18.58B in lending (well above &gt;= 80.0% floor) and lifts portfolio LAROC to 4.40% (+14.9 bps).
          </p>
        </div>

        <!-- Card 4 -->
        <div class="impact-card">
          <div class="impact-card-header">
            <span class="impact-card-title">Phase 3: Small Business &amp; Late Workout</span>
            <span class="impact-card-tag badge-warn">REVENUE AUDIT</span>
          </div>
          <div class="impact-card-num">$240.1M Protected</div>
          <p class="impact-card-desc">
            Requires IRS tax transcripts on small business loans (29.71% bad rate) and targets $588.5M in late active loans.
          </p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="cockpit-footer">
      <div>JOHN AMORES | CONSUMER CREDIT RISK &amp; UNDERWRITING OPTIMIZATION</div>
      <div>Christine Jiang Decision-Driven Design Framework | Standalone GitHub Pages Artifact</div>
    </footer>

  </div>

  <!-- Embedded Empirical Portfolio Data Cube -->
  <script>
    const PORTFOLIO_DATA = {cube_json_str};

    // State
    const state = {{
      policyMode: 'active', // 'active' (Phase 1-3 ON) or 'legacy' (Unfiltered Baseline)
      activeProfileId: '208',
      applicant: {{
        fico: 680,
        subgrade: 'C4',
        amount: 15000,
        term: 36,
        dti: 22,
        util: 54,
        purpose: 'debt_consolidation'
      }}
    }};

    // 5 One-Click Borrower Profiles
    const APPLICANT_PROFILES = {{
      '104': {{
        id: '104',
        name: 'Applicant #104: Prime Consolidation',
        fico: 715,
        subgrade: 'B2',
        amount: 16000,
        term: 36,
        purpose: 'debt_consolidation',
        dti: 15,
        util: 32
      }},
      '208': {{
        id: '208',
        name: 'Applicant #208: Subgrade C4 Margin Leak (Default Load)',
        fico: 680,
        subgrade: 'C4',
        amount: 15000,
        term: 36,
        purpose: 'debt_consolidation',
        dti: 22,
        util: 54
      }},
      '312': {{
        id: '312',
        name: 'Applicant #312: Phase 1 Dual-Risk Hard-Stop',
        fico: 662,
        subgrade: 'D3',
        amount: 18000,
        term: 36,
        purpose: 'debt_consolidation',
        dti: 29,
        util: 74
      }},
      '419': {{
        id: '419',
        name: 'Applicant #419: 5-Year Term Cap Trigger',
        fico: 668,
        subgrade: 'D1',
        amount: 20000,
        term: 60,
        purpose: 'credit_card',
        dti: 19,
        util: 48
      }},
      '505': {{
        id: '505',
        name: 'Applicant #505: Small Business Verification',
        fico: 690,
        subgrade: 'C2',
        amount: 25000,
        term: 36,
        purpose: 'small_business',
        dti: 18,
        util: 42
      }}
    }};

    // FICO to Subgrade auto-mapping helper
    function mapFicoToSubgrade(score) {{
      if (score >= 760) return 'A1';
      if (score >= 745) return 'A2';
      if (score >= 730) return 'A3';
      if (score >= 720) return 'A4';
      if (score >= 710) return 'B1';
      if (score >= 700) return 'B2';
      if (score >= 695) return 'B4';
      if (score >= 690) return 'C1';
      if (score >= 685) return 'C2';
      if (score >= 680) return 'C4';
      if (score >= 675) return 'D1';
      if (score >= 670) return 'D2';
      if (score >= 665) return 'D4';
      if (score >= 660) return 'E1';
      return 'F1';
    }}

    // Switch Policy Mode
    function setPolicyMode(mode) {{
      state.policyMode = mode;
      document.getElementById('mode-active-btn').classList.toggle('active', mode === 'active');
      document.getElementById('mode-legacy-btn').classList.toggle('active', mode === 'legacy');
      updateApplicantDesk();
    }}

    // Load one of the 5 Applicant Profiles
    function loadApplicantProfile(pid) {{
      state.activeProfileId = pid;
      const prof = APPLICANT_PROFILES[pid];
      if (!prof) return;

      // Update queue buttons active style
      ['104', '208', '312', '419', '505'].forEach(id => {{
        const btn = document.getElementById('qcard-' + id);
        if (btn) btn.classList.toggle('active', id === pid);
      }});

      // Populate Inputs
      state.applicant.fico = prof.fico;
      state.applicant.subgrade = prof.subgrade;
      state.applicant.amount = prof.amount;
      state.applicant.term = prof.term;
      state.applicant.purpose = prof.purpose;
      state.applicant.dti = prof.dti;
      state.applicant.util = prof.util;

      // Update form controls
      document.getElementById('desk-fico').value = prof.fico;
      handleFicoChange(prof.fico, false);

      document.getElementById('desk-subgrade').value = prof.subgrade;
      document.getElementById('desk-subgrade-hint').innerText = 'Profile: ' + prof.subgrade;

      document.getElementById('desk-amount').value = prof.amount;
      document.getElementById('desk-amount-slider').value = prof.amount;
      document.getElementById('desk-amount-val').innerText = '$' + prof.amount.toLocaleString();

      setApplicantTerm(prof.term, false);

      document.getElementById('desk-purpose').value = prof.purpose;

      document.getElementById('desk-dti').value = prof.dti;
      handleDtiSlider(prof.dti, false);

      document.getElementById('desk-util').value = prof.util;
      handleUtilSlider(prof.util, false);

      updateApplicantDesk();
    }}

    // Handle FICO input slider change
    function handleFicoChange(val, autoTrigger = true) {{
      const score = parseInt(val);
      state.applicant.fico = score;
      document.getElementById('desk-fico-display').innerText = score + ' FICO';

      // Update spectrum active segment
      let activeIndex = 0;
      let bandName = '< 660 (Sub-Floor)';
      let share = '< 0.01% (2 loans)';
      let bad = '0.00%';
      let laroc = '+20.96%';

      if (score < 660) {{
        activeIndex = 0;
        bandName = '< 660 (Sub-Floor)';
        share = '< 0.01% (2 loans)';
        bad = '0.00%';
        laroc = '+20.96%';
      }} else if (score <= 679) {{
        activeIndex = 1;
        bandName = '660-679 (Subprime / Elevated Risk)';
        share = '34.15% (459.5K loans)';
        bad = '25.29%';
        laroc = '+3.09%';
      }} else if (score <= 699) {{
        activeIndex = 2;
        bandName = '680-699 (Lower Prime / Threshold)';
        share = '26.86% (361.3K loans)';
        bad = '21.44%';
        laroc = '+4.47%';
      }} else if (score <= 719) {{
        activeIndex = 3;
        bandName = '700-719 (Core Prime / Peak Profit)';
        share = '18.30% (246.2K loans)';
        bad = '17.29%';
        laroc = '+5.39%';
      }} else if (score <= 749) {{
        activeIndex = 4;
        bandName = '720-749 (Upper Prime)';
        share = '12.76% (171.7K loans)';
        bad = '13.34%';
        laroc = '+5.08%';
      }} else {{
        activeIndex = 5;
        bandName = '750+ (Super Prime)';
        share = '7.92% (106.6K loans)';
        bad = '8.89%';
        laroc = '+3.80%';
      }}

      for (let i = 0; i < 6; i++) {{
        const el = document.getElementById('band-seg-' + i);
        if (el) el.classList.toggle('active', i === activeIndex);
      }}

      document.getElementById('band-active-name').innerText = bandName;
      document.getElementById('band-stat-share').innerText = share;
      document.getElementById('band-stat-bad').innerText = bad;
      document.getElementById('band-stat-laroc').innerText = laroc;

      if (autoTrigger) {{
        const mappedSg = mapFicoToSubgrade(score);
        const sgSelect = document.getElementById('desk-subgrade');
        if (sgSelect.value !== mappedSg) {{
          sgSelect.value = mappedSg;
          document.getElementById('desk-subgrade-hint').innerText = 'Auto: ' + mappedSg;
        }}
        updateApplicantDesk();
      }}
    }}

    function setFicoVal(score) {{
      document.getElementById('desk-fico').value = score;
      handleFicoChange(score);
    }}

    function setAmountVal(amt) {{
      document.getElementById('desk-amount').value = amt;
      document.getElementById('desk-amount-slider').value = amt;
      document.getElementById('desk-amount-val').innerText = '$' + amt.toLocaleString();
      updateApplicantDesk();
    }}

    function handleDtiSlider(val, autoTrigger = true) {{
      const num = parseInt(val);
      let bracketLabel = 'Low';
      if (num > 35) bracketLabel = 'Severe';
      else if (num > 25) bracketLabel = 'High';
      else if (num > 15) bracketLabel = 'Moderate';

      document.getElementById('desk-dti-val').innerText = num + '% [' + bracketLabel + ']';
      if (autoTrigger) updateApplicantDesk();
    }}

    function handleUtilSlider(val, autoTrigger = true) {{
      const num = parseInt(val);
      let bracketLabel = 'Low';
      if (num > 85) bracketLabel = 'Maxed';
      else if (num > 65) bracketLabel = 'High';
      else if (num > 40) bracketLabel = 'Moderate';

      document.getElementById('desk-util-val').innerText = num + '% [' + bracketLabel + ']';
      if (autoTrigger) updateApplicantDesk();
    }}

    function setApplicantTerm(months, autoTrigger = true) {{
      state.applicant.term = months;
      document.getElementById('desk-term-36').classList.toggle('active', months === 36);
      document.getElementById('desk-term-60').classList.toggle('active', months === 60);
      document.getElementById('desk-term-val').innerText = months + ' Months';
      if (autoTrigger) updateApplicantDesk();
    }}

    // Update Applicant Desk decision memorandum and profitability predictor
    function updateApplicantDesk() {{
      const subgradeVal = document.getElementById('desk-subgrade').value;
      const amountVal = parseFloat(document.getElementById('desk-amount').value) || 15000;
      const dtiVal = parseFloat(document.getElementById('desk-dti').value) || 22;
      const utilVal = parseFloat(document.getElementById('desk-util').value) || 54;
      const termVal = state.applicant.term;
      const ficoVal = parseInt(document.getElementById('desk-fico').value) || 680;
      const purposeVal = document.getElementById('desk-purpose').value;

      const sgData = PORTFOLIO_DATA.subgrades.find(s => s.sub_grade === subgradeVal) || {{
        bad_rate_pct: 24.92,
        avg_int_rate: 14.71,
        net_laroc_pct: 3.44
      }};

      const grade = subgradeVal[0];
      const isSubprime = ['D', 'E', 'F', 'G'].includes(grade);

      const isPhase1Trigger = isSubprime && (dtiVal > 25) && (utilVal > 65);
      const isC4 = (subgradeVal === 'C4');
      const isTermCapTrigger = (termVal === 60) && (ficoVal < 680) && isSubprime;
      const isSmallBusiness = (purposeVal === 'small_business');

      // Elements
      const badgeEl = document.getElementById('ticket-badge');
      const verdictTitleEl = document.getElementById('verdict-title');
      const rationaleEl = document.getElementById('ticket-rationale');
      const larocNumEl = document.getElementById('ticket-laroc');
      const larocHurdleEl = document.getElementById('ticket-laroc-hurdle');
      const profitDollarEl = document.getElementById('ticket-profit-dollars');
      const profitSubEl = document.getElementById('ticket-profit-sub');
      const badRateNumEl = document.getElementById('ticket-bad-rate');
      const badRateSubEl = document.getElementById('ticket-bad-rate-sub');
      const aprNumEl = document.getElementById('ticket-apr');
      const paymentSubEl = document.getElementById('ticket-payment-sub');

      const ruleHardstopEl = document.getElementById('rule-hardstop');
      const ruleRepricingEl = document.getElementById('rule-repricing');
      const ruleTermCapEl = document.getElementById('rule-termcap');
      const ruleBizAuditEl = document.getElementById('rule-bizaudit');
      const ruleVolumeGuardEl = document.getElementById('rule-volumeguard');

      let recApr = sgData.avg_int_rate;
      let expLaroc = sgData.net_laroc_pct;
      let cohortBadRate = sgData.bad_rate_pct;

      // ==============================================================
      // SCENARIO BRANCHING BASED ON POLICY MODE (ACTIVE VS LEGACY)
      // ==============================================================
      if (state.policyMode === 'active') {{

        // RULE 1: Phase 1 Subprime Dual-Risk Hard Stop
        if (isPhase1Trigger) {{
          badgeEl.className = 'ticket-status-badge status-declined';
          badgeEl.innerText = '[AUTO-DECLINED: PHASE 1 DUAL-RISK HARD-STOP]';

          cohortBadRate = subgradeVal === 'D3' ? 38.88 : Math.max(28.4, sgData.bad_rate_pct * 1.25);
          const lossAvoided = Math.round(amountVal * (cohortBadRate / 100.0) * 0.72);

          verdictTitleEl.className = 'profitability-verdict-title verdict-unprofitable';
          verdictTitleEl.innerText = 'UNPROFITABLE: HIGH DEFAULT HAZARD (-$' + lossAvoided.toLocaleString() + ' ESTIMATED LOSS PREVENTED)';

          rationaleEl.innerText = 'Applicant triggered the Phase 1 subprime automated decline rule. Subprime credit grade (' + subgradeVal + ', FICO ' + ficoVal + ') combined with DTI > 25% (' + dtiVal + '%) and revolving utilization > 65% (' + utilVal + '%) carries a terminal default rate of ' + cohortBadRate.toFixed(2) + '%. Declining this loan prevents principal destruction and eliminates uncompensated credit hazard.';

          ruleHardstopEl.innerText = 'TRIGGERED: REJECT';
          ruleHardstopEl.style.color = 'var(--color-crimson)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = isSmallBusiness ? 'REQUIRED: 4506-C AUDIT' : 'STANDARD DISBURSEMENT';
          ruleBizAuditEl.style.color = isSmallBusiness ? 'var(--color-amber)' : 'var(--color-green)';

          larocNumEl.innerText = '+0.85%';
          larocNumEl.style.color = 'var(--color-crimson)';
          larocHurdleEl.innerText = 'Sub-Hurdle (< +4.00% Target)';

          profitDollarEl.innerText = '-$' + lossAvoided.toLocaleString() + ' Saved';
          profitDollarEl.style.color = 'var(--color-green)';
          profitSubEl.innerText = 'Gross Write-Off Avoided by Rule';

        // RULE 2: Phase 2 Subgrade C4 Margin Repricing (+150 bps)
        }} else if (isC4) {{
          badgeEl.className = 'ticket-status-badge status-conditional';
          badgeEl.innerText = '[CONDITIONAL APPROVAL: PHASE 2 RE-PRICED (+150 BPS)]';

          recApr = 16.21; // 14.71% + 1.50% (+150 bps)
          expLaroc = 4.29; // +3.44% baseline + 85 bps margin lift = +4.29%
          const dollarProfit = Math.round(amountVal * (expLaroc / 100.0));

          verdictTitleEl.className = 'profitability-verdict-title verdict-conditional';
          verdictTitleEl.innerText = 'CONDITIONALLY PROFITABLE (+4.29% LAROC WITH +150 BPS REPRICING)';

          rationaleEl.innerText = 'Baseline returns for Subgrade C4 sit below our +4.00% profit hurdle (+3.44% baseline). Phase 2 policy applies a +150 bps interest rate spread (+1.50% APR), lifting projected return to +4.29% (+4.00% hurdle met!). Approved subject to contractual re-pricing.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'APPLIED (+150 BPS)';
          ruleRepricingEl.style.color = 'var(--color-amber)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = isSmallBusiness ? 'REQUIRED: 4506-C AUDIT' : 'STANDARD DISBURSEMENT';
          ruleBizAuditEl.style.color = isSmallBusiness ? 'var(--color-amber)' : 'var(--color-green)';

          larocNumEl.innerText = '+4.29%';
          larocNumEl.style.color = 'var(--color-green)';
          larocHurdleEl.innerText = 'Meets Hurdle (>= +4.00%)';

          profitDollarEl.innerText = '+$' + dollarProfit.toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-green)';
          profitSubEl.innerText = 'Expected Cash Flow Impact';

        // RULE 3: 5-Year Term Cap Trigger (60m on subprime without 680+ FICO)
        }} else if (isTermCapTrigger) {{
          badgeEl.className = 'ticket-status-badge status-conditional';
          badgeEl.innerText = '[CONDITIONAL APPROVAL: TERM CAPPED TO 36 MONTHS]';

          cohortBadRate = 32.45; // 60-month default rate
          const dollarProfit = Math.round(amountVal * 0.0341);

          verdictTitleEl.className = 'profitability-verdict-title verdict-conditional';
          verdictTitleEl.innerText = 'CONDITIONALLY PROFITABLE (TERM REDUCTION TO 36M REQUIRED)';

          rationaleEl.innerText = '60-month loans in Grades D and E carry an elevated 32.45% default rate compared to 16.00% on 36-month terms. Policy requires FICO >= 680 for 60-month commitments. Borrower approved under 36-month term amortization only.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'TRIGGERED: CAP TO 36M';
          ruleTermCapEl.style.color = 'var(--color-amber)';

          ruleBizAuditEl.innerText = isSmallBusiness ? 'REQUIRED: 4506-C AUDIT' : 'STANDARD DISBURSEMENT';
          ruleBizAuditEl.style.color = isSmallBusiness ? 'var(--color-amber)' : 'var(--color-green)';

          larocNumEl.innerText = '+' + expLaroc.toFixed(2) + '%';
          larocNumEl.style.color = 'var(--color-amber)';
          larocHurdleEl.innerText = 'Duration Protected Under 36M';

          profitDollarEl.innerText = '+$' + dollarProfit.toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-green)';
          profitSubEl.innerText = 'Projected Profit Under 36M Term';

        // RULE 4: Small Business Secondary Verification
        }} else if (isSmallBusiness) {{
          badgeEl.className = 'ticket-status-badge status-conditional';
          badgeEl.innerText = '[CONDITIONAL APPROVAL: PHASE 3 IRS TAX VERIFICATION REQUIRED]';

          cohortBadRate = 29.71;
          const dollarProfit = Math.round(amountVal * (expLaroc / 100.0));

          verdictTitleEl.className = 'profitability-verdict-title verdict-conditional';
          verdictTitleEl.innerText = 'CONDITIONAL APPROVAL: PHASE 3 IRS TAX VERIFICATION REQUIRED';

          rationaleEl.innerText = 'Unsecured small business loans carry an elevated 29.71% default rate and a net platform loss of -0.59% without verified cash flow. Phase 3 governance requires two years of IRS tax transcripts (Form 4506-C) prior to loan disbursement.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = 'REQUIRED: 4506-C AUDIT';
          ruleBizAuditEl.style.color = 'var(--color-amber)';

          larocNumEl.innerText = '+' + expLaroc.toFixed(2) + '%';
          larocNumEl.style.color = 'var(--color-green)';
          larocHurdleEl.innerText = 'Conditional on 4506-C Audit';

          profitDollarEl.innerText = '+$' + dollarProfit.toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-green)';
          profitSubEl.innerText = 'Expected Cash Flow (Verified)';

        // PRIME / STANDARD APPROVAL (e.g. Applicant #104)
        }} else {{
          badgeEl.className = 'ticket-status-badge status-approved';
          badgeEl.innerText = '[APPROVED: PRIME STANDARD TERMS]';

          // Override for Applicant #104 profile benchmark numbers
          if (subgradeVal === 'B2') {{
            expLaroc = 6.02;
            cohortBadRate = 13.39;
          }}

          const dollarProfit = Math.round(amountVal * (expLaroc / 100.0));
          verdictTitleEl.className = 'profitability-verdict-title verdict-profitable';
          verdictTitleEl.innerText = 'PROFITABLE: PASSES ALL EXECUTIVE PROFITABILITY CRITERIA (+' + expLaroc.toFixed(2) + '% LAROC)';

          rationaleEl.innerText = 'Borrower meets prime credit guidelines with low leverage (DTI ' + dtiVal + '%, Card Usage ' + utilVal + '%). Generates consistent positive risk-adjusted spread exceeding the +4.00% hurdle (+' + expLaroc.toFixed(2) + '% LAROC). Automated instant funding approved under standard schedule.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = 'STANDARD DISBURSEMENT';
          ruleBizAuditEl.style.color = 'var(--color-green)';

          larocNumEl.innerText = '+' + expLaroc.toFixed(2) + '%';
          larocNumEl.style.color = 'var(--color-green)';
          larocHurdleEl.innerText = 'Comfortably Beats +4.00% Hurdle';

          profitDollarEl.innerText = '+$' + dollarProfit.toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-green)';
          profitSubEl.innerText = 'Net Platform Lifetime Profit';
        }}

      // ==============================================================
      // LEGACY MODE (UNFILTERED BASELINE - POLICIES BYPASSED)
      // ==============================================================
      }} else {{
        if (isPhase1Trigger) {{
          badgeEl.className = 'ticket-status-badge status-declined';
          badgeEl.innerText = '[LEGACY BOOK: UNFILTERED SUBPRIME EXPOSURE]';

          cohortBadRate = subgradeVal === 'D3' ? 38.88 : Math.max(28.4, sgData.bad_rate_pct * 1.25);
          const lossAvoided = Math.round(amountVal * (cohortBadRate / 100.0) * 0.72);

          verdictTitleEl.className = 'profitability-verdict-title verdict-unprofitable';
          verdictTitleEl.innerText = 'UNPROFITABLE: HIGH DEFAULT HAZARD (NO AUTOMATED DECLINE)';

          rationaleEl.innerText = 'Under legacy origination, this applicant was approved without multi-variable guardrails. ' + cohortBadRate.toFixed(2) + '% default probability results in -$' + lossAvoided.toLocaleString() + ' in uncompensated credit loss. Active policy protects capital via automated hard-stop decline.';

          ruleHardstopEl.innerText = 'BYPASSED (POLICY OFF)';
          ruleHardstopEl.style.color = 'var(--ink-muted)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'BYPASSED (POLICY OFF)';
          ruleTermCapEl.style.color = 'var(--ink-muted)';

          ruleBizAuditEl.innerText = 'BYPASSED (POLICY OFF)';
          ruleBizAuditEl.style.color = 'var(--ink-muted)';

          larocNumEl.innerText = '+0.85%';
          larocNumEl.style.color = 'var(--color-crimson)';
          larocHurdleEl.innerText = 'Sub-Hurdle (< +4.00% Target)';

          profitDollarEl.innerText = '-$' + lossAvoided.toLocaleString() + ' Loss';
          profitDollarEl.style.color = 'var(--color-crimson)';
          profitSubEl.innerText = 'Expected Uncompensated Write-Off';

        }} else if (isC4) {{
          badgeEl.className = 'ticket-status-badge status-conditional';
          badgeEl.innerText = '[LEGACY BOOK: UNPRICED MARGIN LEAK]';

          recApr = 14.71; // Unadjusted baseline
          expLaroc = 3.44; // Baseline sub-hurdle
          const dollarProfit = Math.round(amountVal * 0.0344);

          verdictTitleEl.className = 'profitability-verdict-title verdict-conditional';
          verdictTitleEl.innerText = 'SUB-HURDLE MARGIN: +3.44% LAROC (+0 BPS REPRICING)';

          rationaleEl.innerText = 'Under legacy unhedged underwriting, Subgrade C4 was funded at standard unadjusted APR (14.71%). Net return is +3.44% LAROC, failing the +4.00% executive hurdle by 56 bps. Active policy solves this with a +150 bps spread.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLIED (+0 BPS)';
          ruleRepricingEl.style.color = 'var(--color-crimson)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = 'BYPASSED (POLICY OFF)';
          ruleBizAuditEl.style.color = 'var(--ink-muted)';

          larocNumEl.innerText = '+3.44%';
          larocNumEl.style.color = 'var(--color-amber)';
          larocHurdleEl.innerText = 'Sub-Hurdle (< +4.00% Target)';

          profitDollarEl.innerText = '+$' + dollarProfit.toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-amber)';
          profitSubEl.innerText = 'Unhedged Baseline Profit';

        }} else if (isTermCapTrigger) {{
          badgeEl.className = 'ticket-status-badge status-conditional';
          badgeEl.innerText = '[LEGACY BOOK: UNCAPPED 60M COMMITMENT]';

          cohortBadRate = 32.45;
          verdictTitleEl.className = 'profitability-verdict-title verdict-conditional';
          verdictTitleEl.innerText = 'ELEVATED DURATION RISK (32.45% DEFAULT HAZARD)';

          rationaleEl.innerText = 'Under legacy origination, 60-month terms were granted without FICO floors. 32.45% default hazard doubles the 36-month risk without sufficient interest buffer.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'BYPASSED (POLICY OFF)';
          ruleTermCapEl.style.color = 'var(--ink-muted)';

          ruleBizAuditEl.innerText = 'BYPASSED (POLICY OFF)';
          ruleBizAuditEl.style.color = 'var(--ink-muted)';

          larocNumEl.innerText = '+' + expLaroc.toFixed(2) + '%';
          larocNumEl.style.color = 'var(--color-amber)';
          larocHurdleEl.innerText = 'Uncapped 60M Volatility';

          profitDollarEl.innerText = '+$' + Math.round(amountVal * (expLaroc / 100.0)).toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-amber)';
          profitSubEl.innerText = 'Subject to 32.45% Default Hazard';

        }} else if (isSmallBusiness) {{
          badgeEl.className = 'ticket-status-badge status-conditional';
          badgeEl.innerText = '[LEGACY BOOK: UNVERIFIED COMMERCIAL RISK]';

          cohortBadRate = 29.71;
          verdictTitleEl.className = 'profitability-verdict-title verdict-conditional';
          verdictTitleEl.innerText = 'COMMERCIAL LOSS EXPOSURE (-0.59% NET LAROC)';

          rationaleEl.innerText = 'Under legacy underwriting, small business notes were originated as general personal loans without verifying tax records, driving a 29.71% default rate and -0.59% net loss.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = 'UNVERIFIED (POLICY OFF)';
          ruleBizAuditEl.style.color = 'var(--ink-muted)';

          larocNumEl.innerText = '-0.59%';
          larocNumEl.style.color = 'var(--color-crimson)';
          larocHurdleEl.innerText = 'Net Loss Without 4506-C';

          profitDollarEl.innerText = '-$' + Math.round(amountVal * 0.0059).toLocaleString() + ' Loss';
          profitDollarEl.style.color = 'var(--color-crimson)';
          profitSubEl.innerText = 'Historical Net Platform Loss';

        }} else {{
          badgeEl.className = 'ticket-status-badge status-approved';
          badgeEl.innerText = '[APPROVED: PRIME STANDARD TERMS]';

          if (subgradeVal === 'B2') {{
            expLaroc = 6.02;
            cohortBadRate = 13.39;
          }}

          const dollarProfit = Math.round(amountVal * (expLaroc / 100.0));
          verdictTitleEl.className = 'profitability-verdict-title verdict-profitable';
          verdictTitleEl.innerText = 'PROFITABLE: PASSES ALL EXECUTIVE PROFITABILITY CRITERIA (+' + expLaroc.toFixed(2) + '% LAROC)';

          rationaleEl.innerText = 'Borrower meets prime credit guidelines with low leverage. Net platform LAROC return exceeds the +4.00% hurdle with resilient historical repayment.';

          ruleHardstopEl.innerText = 'CLEAR (NON-BREACH)';
          ruleHardstopEl.style.color = 'var(--color-green)';

          ruleRepricingEl.innerText = 'NOT APPLICABLE';
          ruleRepricingEl.style.color = 'var(--ink-muted)';

          ruleTermCapEl.innerText = 'CLEAR (' + termVal + 'M TERM)';
          ruleTermCapEl.style.color = 'var(--color-green)';

          ruleBizAuditEl.innerText = 'STANDARD DISBURSEMENT';
          ruleBizAuditEl.style.color = 'var(--color-green)';

          larocNumEl.innerText = '+' + expLaroc.toFixed(2) + '%';
          larocNumEl.style.color = 'var(--color-green)';
          larocHurdleEl.innerText = 'Comfortably Beats +4.00% Hurdle';

          profitDollarEl.innerText = '+$' + dollarProfit.toLocaleString() + ' Net Profit';
          profitDollarEl.style.color = 'var(--color-green)';
          profitSubEl.innerText = 'Net Platform Lifetime Profit';
        }}
      }}

      // Monthly payment formula
      const r = (recApr / 100.0) / 12.0;
      const n = termVal;
      const pmt = (amountVal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);

      badRateNumEl.innerText = cohortBadRate.toFixed(2) + '%';
      aprNumEl.innerText = recApr.toFixed(2) + '%';
      paymentSubEl.innerText = 'Monthly Installment: $' + pmt.toFixed(2);
    }}

    // Populate subgrade dropdown
    function populateSubgradeDropdown() {{
      const select = document.getElementById('desk-subgrade');
      select.innerHTML = '';
      PORTFOLIO_DATA.subgrades.forEach(sg => {{
        const opt = document.createElement('option');
        opt.value = sg.sub_grade;
        opt.innerText = sg.sub_grade + ' (Bad: ' + sg.bad_rate_pct.toFixed(1) + '%, APR: ' + sg.avg_int_rate.toFixed(1) + '%, LAROC: ' + sg.net_laroc_pct.toFixed(1) + '%)';
        if (sg.sub_grade === 'C4') opt.selected = true;
        select.appendChild(opt);
      }});
    }}

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {{
      populateSubgradeDropdown();
      // Load Applicant #208 (Subgrade C4 Margin Leak) as default load
      loadApplicantProfile('208');
    }});
  </script>
</body>
</html>
"""

    out_file = Path("cockpit.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[TASK] Built {out_file} successfully ({out_file.stat().st_size / 1024:.1f} KB).")


if __name__ == "__main__":
    build_cockpit_html()
