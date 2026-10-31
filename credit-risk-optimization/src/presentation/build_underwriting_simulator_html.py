"""
src/presentation/build_underwriting_simulator_html.py
Consumer Credit Risk & Underwriting Optimization
Phase 4: Standalone Underwriting Decision Simulator (underwriting-simulator.html)
Refactored into a focused Live Underwriting Desk Simulator following
clean visual hierarchy principles.

Strict zero em dashes, zero en dashes.
"""

from pathlib import Path
import json


HTML_PREFIX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Underwriting Decision Simulator | John Amores</title>
  
  <!-- Typography: High-Contrast Editorial Serif + Crisp Sans + Tabular Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg-paper: #FAF8F2;
      --bg-paper-alt: #F4EFE6;
      --bg-card: #FFFFFF;
      --ink-black: #111111;
      --ink-muted: #57534E;
      --ink-subtle: #8A857D;
      --border-color: #111111;
      --border-soft: #E5E0D5;
      --border-subtle: #EFEBE4;
      --hairline: 1px solid var(--border-soft);
      --hairline-crisp: 1px solid var(--border-color);
      --color-green: #15803D;
      --color-green-light: #F0FDF4;
      --color-crimson: #BE123C;
      --color-crimson-light: #FFF1F2;
      --color-amber: #B45309;
      --color-amber-light: #FEF3C7;
      --color-charcoal: #27272A;
      --content-width: 1240px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    ::selection {
      background: #111111;
      color: #FAF8F2;
    }

    body {
      background-color: var(--bg-paper);
      color: var(--ink-black);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 15px;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }

    /* Top Sticky Navigation Header */
    .top-nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(250, 248, 242, 0.96);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border-soft);
    }

    .top-nav-inner {
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
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .nav-badge {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-green);
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .nav-links a {
      color: var(--ink-black);
      text-decoration: none;
      transition: opacity 140ms ease;
    }

    .nav-links a:hover {
      opacity: 0.65;
    }

    .nav-btn {
      padding: 6px 14px;
      background: var(--ink-black);
      color: var(--bg-paper) !important;
      border: 1px solid var(--ink-black);
      border-radius: 4px;
      white-space: nowrap;
      transition: background 140ms ease, color 140ms ease;
    }

    .nav-btn:hover {
      background: #27272A;
      opacity: 1 !important;
    }

    /* Layout Wrapper */
    .simulator-container {
      max-width: var(--content-width);
      margin: 0 auto;
      padding: 24px 24px 64px 24px;
    }

    /* Hero Section */
    .simulator-hero {
      padding: 18px 0 24px 0;
      border-bottom: 1px solid var(--border-soft);
      margin-bottom: 28px;
    }

    .hero-tag {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-muted);
      margin-bottom: 12px;
    }

    .hero-tag span {
      display: inline-block;
      padding: 3px 8px;
      border: 1px solid var(--border-soft);
      background: #FFFFFF;
      border-radius: 4px;
    }

    .hero-title {
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(2.4rem, 4.4vw, 3.8rem);
      font-weight: 400;
      line-height: 1.05;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }

    .hero-subtitle {
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(1.2rem, 1.9vw, 1.45rem);
      font-style: italic;
      color: var(--ink-muted);
      line-height: 1.4;
      margin-bottom: 20px;
    }

    /* Guardrail Status Bar */
    .guardrail-bar {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin: 16px 0 16px 0;
    }

    .guardrail-pill {
      display: flex;
      align-items: center;
      gap: 12px;
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      padding: 12px 16px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.73rem;
      color: var(--ink-black);
      line-height: 1.4;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .guardrail-pill strong {
      color: var(--ink-black);
    }

    .meta-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 18px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      color: var(--ink-subtle);
      border-top: 1px solid var(--border-subtle);
      padding-top: 12px;
      margin-top: 4px;
    }

    .meta-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Section Headings */
    .section-title {
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 1.65rem;
      font-weight: 400;
      line-height: 1.2;
    }

    .section-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: var(--ink-muted);
      text-transform: uppercase;
    }

    /* ============================================================== */
    /* 1. SAMPLE APPLICANT QUEUE BAR                                  */
    /* ============================================================== */
    .queue-section {
      margin-bottom: 32px;
    }

    .queue-header-row {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 12px;
    }

    .queue-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--ink-black);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .queue-hint {
      font-size: 0.74rem;
      color: var(--ink-muted);
    }

    .queue-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
    }

    .queue-card-btn {
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 6px;
      padding: 14px 14px;
      cursor: pointer;
      text-align: left;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 120px;
      transition: all 160ms cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .queue-card-btn:hover {
      background: #FFFFFF;
      border-color: #B5B0A4;
      transform: translateY(-2px);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.05);
    }

    .queue-card-btn.active {
      background: #FFFFFF;
      border: 2px solid var(--ink-black);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.07);
      transform: translateY(-1px);
    }

    .queue-card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .queue-card-id {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--ink-black);
    }

    .queue-card-btn.active .queue-card-id {
      color: var(--ink-black);
    }

    .queue-card-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .queue-tag-prime {
      background: var(--color-green-light);
      color: var(--color-green);
      border: 1px solid rgba(21, 128, 61, 0.25);
    }

    .queue-tag-amber {
      background: var(--color-amber-light);
      color: var(--color-amber);
      border: 1px solid rgba(180, 83, 9, 0.25);
    }

    .queue-tag-crimson {
      background: var(--color-crimson-light);
      color: var(--color-crimson);
      border: 1px solid rgba(190, 18, 60, 0.25);
    }

    .queue-card-name {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.78rem;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 8px;
      color: var(--ink-black);
    }

    .queue-card-btn.active .queue-card-name {
      color: var(--ink-black);
    }

    .queue-card-meta {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: var(--ink-muted);
      line-height: 1.45;
    }

    .queue-card-btn.active .queue-card-meta {
      color: var(--ink-muted);
    }

    .queue-card-verdict {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.63rem;
      font-weight: 700;
      margin-top: 10px;
      display: inline-block;
      line-height: 1.3;
    }

    .queue-card-btn.active .queue-card-verdict {
      text-decoration: underline;
      text-underline-offset: 2px;
    }

    /* ============================================================== */
    /* 2. MAIN TOOL: APPLICANT DESK TESTER WORKSTATION                */
    /* ============================================================== */
    .main-tool-card {
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 8px;
      padding: 32px 36px;
      margin-bottom: 36px;
      box-shadow: 0 2px 14px rgba(0, 0, 0, 0.02);
    }

    .desk-title-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 14px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--border-soft);
    }

    .engine-mode-toggle {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .mode-label {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--ink-muted);
    }

    .toggle-buttons {
      display: inline-flex;
      border: 1px solid var(--border-soft);
      background: var(--bg-paper);
      border-radius: 6px;
      overflow: hidden;
      padding: 2px;
      gap: 2px;
    }

    .mode-btn {
      padding: 6px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.70rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--ink-muted);
      cursor: pointer;
      border-radius: 4px;
      transition: all 140ms ease;
    }

    .mode-btn.active {
      background: var(--ink-black);
      color: #FFFFFF;
    }

    .mode-btn:hover:not(.active) {
      color: var(--ink-black);
      background: rgba(0, 0, 0, 0.04);
    }

    .main-tool-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 36px;
      margin-top: 18px;
      align-items: start;
    }

    /* Form Fields */
    .form-group {
      margin-bottom: 20px;
    }

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-bottom: 20px;
    }

    .input-label {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.73rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--ink-black);
    }

    .input-val-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.80rem;
      font-weight: 700;
      color: var(--ink-black);
    }

    .text-input, .select-input {
      width: 100%;
      padding: 9px 12px;
      border: 1px solid var(--border-soft);
      background: #FFFFFF;
      color: var(--ink-black);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.84rem;
      border-radius: 5px;
      transition: border-color 140ms ease;
    }

    .text-input:focus, .select-input:focus {
      outline: none;
      border-color: var(--ink-black);
      box-shadow: 0 0 0 1px var(--ink-black);
    }

    .slider-input {
      width: 100%;
      height: 6px;
      background: #E5E0D5;
      border-radius: 3px;
      outline: none;
      accent-color: var(--ink-black);
      cursor: pointer;
      margin-top: 6px;
    }

    /* FICO Band Spectrum Component */
    .fico-spectrum-container {
      margin-top: 10px;
      background: var(--bg-paper);
      border: 1px solid var(--border-soft);
      padding: 12px 14px;
      border-radius: 6px;
      position: relative;
    }

    .fico-spectrum-bar {
      display: grid;
      grid-template-columns: 0.8fr 1.6fr 1.4fr 1.2fr 1fr 0.9fr;
      gap: 3px;
      height: 26px;
      position: relative;
      margin: 16px 0 10px 0;
      border-radius: 4px;
    }

    .fico-band-segment {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--ink-muted);
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 3px;
      transition: all 120ms ease;
      cursor: pointer;
      user-select: none;
    }

    .fico-band-segment:hover {
      border-color: var(--ink-black);
      color: var(--ink-black);
    }

    .fico-band-segment.active {
      background: var(--ink-black) !important;
      border-color: var(--ink-black) !important;
      color: #FFFFFF !important;
    }

    .spectrum-cutoff-line {
      position: absolute;
      left: 36.5%;
      top: -3px;
      bottom: -3px;
      width: 2px;
      background: var(--color-crimson);
      z-index: 10;
      pointer-events: none;
    }

    .spectrum-cutoff-tag {
      position: absolute;
      top: -18px;
      left: -38px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem;
      font-weight: 700;
      color: var(--color-crimson);
      white-space: nowrap;
      background: #FFFFFF;
      padding: 1px 5px;
      border: 1px solid var(--color-crimson);
      border-radius: 3px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .band-callout-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.69rem;
      color: var(--ink-muted);
      padding-top: 8px;
      border-top: 1px solid var(--border-subtle);
    }

    .band-stat-pill {
      display: inline-block;
      padding: 1px 6px;
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 3px;
      font-weight: 700;
      color: var(--ink-black);
    }

    /* Loan Amount Presets */
    .preset-pills {
      display: flex;
      gap: 6px;
      margin-top: 8px;
    }

    .pill-btn {
      flex: 1;
      padding: 5px 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 600;
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 4px;
      cursor: pointer;
      color: var(--ink-muted);
      transition: all 120ms ease;
      text-align: center;
    }

    .pill-btn:hover {
      background: var(--ink-black);
      border-color: var(--ink-black);
      color: #FFFFFF;
    }

    .btn-choice {
      flex: 1;
      padding: 8px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      font-weight: 700;
      background: #FFFFFF;
      color: var(--ink-black);
      border: 1px solid var(--border-soft);
      border-radius: 4px;
      cursor: pointer;
      transition: all 120ms ease;
      text-align: center;
    }

    .btn-choice:hover {
      background: var(--bg-paper-alt);
    }

    .btn-choice.active {
      background: var(--ink-black);
      color: #FFFFFF;
      border-color: var(--ink-black);
    }

    /* Right Column: Underwriting Predictor Memorandum */
    .predictor-memo {
      border: 1px solid var(--border-soft);
      background: #FAF8F2;
      border-radius: 6px;
      padding: 26px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 100%;
    }

    .memo-header {
      border-bottom: 1px solid var(--border-soft);
      padding-bottom: 16px;
      margin-bottom: 16px;
    }

    .memo-eyebrow {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--ink-subtle);
      margin-bottom: 10px;
    }

    .ticket-status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 4px;
      text-transform: uppercase;
      margin-bottom: 12px;
      letter-spacing: 0.04em;
    }

    .status-declined {
      background: var(--color-crimson-light);
      color: var(--color-crimson);
      border: 1px solid rgba(190, 18, 60, 0.25);
    }

    .status-conditional {
      background: var(--color-amber-light);
      color: var(--color-amber);
      border: 1px solid rgba(180, 83, 9, 0.25);
    }

    .status-approved {
      background: var(--color-green-light);
      color: var(--color-green);
      border: 1px solid rgba(21, 128, 61, 0.25);
    }

    .profitability-verdict-title {
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 1.42rem;
      font-weight: 400;
      line-height: 1.25;
      margin-bottom: 10px;
    }

    .verdict-profitable {
      color: var(--color-green);
    }

    .verdict-conditional {
      color: var(--color-amber);
    }

    .verdict-unprofitable {
      color: var(--color-crimson);
    }

    .ticket-rationale {
      font-size: 0.82rem;
      line-height: 1.6;
      color: var(--ink-muted);
    }

    /* Financial Metrics 4-Box Grid */
    .memo-metrics-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }

    .memo-metric-box {
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 4px;
      padding: 12px 14px;
    }

    .memo-metric-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--ink-subtle);
      margin-bottom: 4px;
    }

    .memo-metric-num {
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 1.65rem;
      font-weight: 400;
      line-height: 1.1;
      color: var(--ink-black);
    }

    .memo-metric-sub {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.64rem;
      color: var(--ink-muted);
      margin-top: 3px;
    }

    /* Rules Checklist */
    .rules-list {
      border-top: 1px solid var(--border-soft);
      padding-top: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .rule-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.72rem;
      padding: 3px 0;
    }

    .rule-name {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 500;
      color: var(--ink-muted);
    }

    .rule-result {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 700;
    }

    /* ============================================================== */
    /* 3. COMPACT 4-CARD PORTFOLIO POLICY IMPACT FOOTER STRIP         */
    /* ============================================================== */
    .portfolio-impact-section {
      border-top: 1px solid var(--border-soft);
      padding-top: 28px;
      margin-top: 14px;
    }

    .impact-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 6px;
    }

    .rollout-selector {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .impact-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 16px;
      margin-bottom: 32px;
    }

    .impact-card {
      background: #FFFFFF;
      border: 1px solid var(--border-soft);
      border-radius: 6px;
      padding: 22px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 180px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
      transition: all 160ms cubic-bezier(0.16, 1, 0.3, 1);
    }

    .impact-card:hover {
      border-color: #A8A29E;
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    }

    .impact-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .impact-card-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.73rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--ink-muted);
    }

    .impact-card-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.60rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      text-transform: uppercase;
    }

    .badge-pass {
      background: var(--color-green-light);
      color: var(--color-green);
      border: 1px solid rgba(21, 128, 61, 0.25);
    }

    .badge-warn {
      background: var(--color-amber-light);
      color: var(--color-amber);
      border: 1px solid rgba(180, 83, 9, 0.25);
    }

    .impact-card-num {
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 2.3rem;
      font-weight: 400;
      line-height: 1.1;
      letter-spacing: -0.01em;
      color: var(--ink-black);
      margin-bottom: 8px;
    }

    .impact-card-desc {
      font-size: 0.77rem;
      line-height: 1.55;
      color: var(--ink-muted);
    }

    /* Footer */
    .simulator-footer {
      border-top: 1px solid var(--border-soft);
      padding-top: 24px;
      padding-bottom: 28px;
      font-size: 0.74rem;
      color: var(--ink-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    @media (max-width: 1024px) {
      .main-tool-grid {
        grid-template-columns: 1fr;
      }
      .queue-grid {
        grid-template-columns: repeat(3, 1fr);
      }
      .guardrail-bar {
        grid-template-columns: 1fr;
      }
      .impact-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    @media (max-width: 640px) {
      .queue-grid {
        grid-template-columns: 1fr;
      }
      .impact-grid {
        grid-template-columns: 1fr;
      }
      .top-nav-inner {
        flex-direction: column;
        gap: 8px;
      }
      .desk-title-bar {
        flex-direction: column;
        align-items: flex-start;
      }
    }
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

  <div class="simulator-container">

    <!-- Hero Header -->
    <header class="simulator-hero">
      <div class="hero-tag">
        <span>EXECUTIVE UNDERWRITING WORKSTATION</span>
        <span>100% STANDALONE AUDIT DECK</span>
      </div>
      <h1 class="hero-title">Underwriting Decision Simulator</h1>
      <p class="hero-subtitle">Single-Screen Live Underwriting Desk &amp; Empirical Multi-Variable Policy Engine</p>

      <!-- 3-Pill Guardrail Status Bar -->
      <div class="guardrail-bar">
        <div class="guardrail-pill">
          <span class="badge-pass">PASS</span>
          <span><strong>PROFIT HURDLE GUARDRAIL 1:</strong> +4.4% Net Return (Meets &gt;= +4.0% Target)</span>
        </div>
        <div class="guardrail-pill">
          <span class="badge-pass">PASS</span>
          <span><strong>DEFAULT CEILING GUARDRAIL 2:</strong> 19.0% Default Rate (&lt; 19.3% Cap)</span>
        </div>
        <div class="guardrail-pill">
          <span class="badge-pass">PASS</span>
          <span><strong>VOLUME FLOOR GUARDRAIL 3:</strong> 96% Lending Volume Kept ($18.6B &gt;= 80% Floor)</span>
        </div>
      </div>
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
              <input type="range" id="desk-amount-slider" min="1000" max="40000" step="500" value="15000" class="slider-input" style="display:none;" oninput="document.getElementById('desk-amount').value = this.value; document.getElementById('desk-amount-val').innerText = '$' + parseInt(this.value).toLocaleString(); updateApplicantDesk();">
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
            <span>02 PORTFOLIO-WIDE IMPACT OF ACTIVE RULES</span>
          </div>
          <div class="section-num">AUDITED HISTORICAL PORTFOLIO PERFORMANCE (1,345,350 COMPLETED LOANS / $19.4B BOOK)</div>
        </div>
        <!-- Rollout Adoption Selector -->
        <div class="rollout-selector">
          <span class="mode-label">Adoption Level:</span>
          <div class="toggle-buttons">
            <button type="button" class="mode-btn" id="btn-rollout-60" onclick="setRolloutAdoption(60)">
              60% Cautious Pilot
            </button>
            <button type="button" class="mode-btn" id="btn-rollout-80" onclick="setRolloutAdoption(80)">
              80% Year-1 Goal
            </button>
            <button type="button" class="mode-btn active" id="btn-rollout-100" onclick="setRolloutAdoption(100)">
              100% Full Rollout
            </button>
          </div>
        </div>
      </div>
      <p style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 4px;">
        Audited historical performance of the 4 underwriting rules when applied to the complete $19.4B loan book ($19.39B funded).
      </p>

      <div class="impact-grid">
        <!-- Card 1 -->
        <div class="impact-card" id="impact-card-1">
          <div class="impact-card-header">
            <span class="impact-card-title">Rule 1: Phase 1 Dual-Risk Cutoff</span>
            <span class="impact-card-tag badge-pass" id="impact-tag-1">18,548 DEFAULTS</span>
          </div>
          <div class="impact-card-num" id="impact-num-1">+$230.0M Saved</div>
          <p class="impact-card-desc" id="impact-desc-1">
            Auto-declining Grades D-G with DTI &gt; 25% &amp; Card Usage &gt; 65% prevents 18,548 defaults ($230.04M net / $254.10M gross saved).
          </p>
        </div>

        <!-- Card 2 -->
        <div class="impact-card" id="impact-card-2">
          <div class="impact-card-header">
            <span class="impact-card-title">Rule 2: Phase 2 Subgrade C4 Repricing</span>
            <span class="impact-card-tag badge-pass" id="impact-tag-2">74,422 LOANS</span>
          </div>
          <div class="impact-card-num" id="impact-num-2">+$14.2M Revenue</div>
          <p class="impact-card-desc" id="impact-desc-2">
            Adding +1.5% (+150 bps) across 74,422 Subgrade C4 loans adds +$14.20M in interest income and restores +4.00% profit hurdle.
          </p>
        </div>

        <!-- Card 3 -->
        <div class="impact-card" id="impact-card-3">
          <div class="impact-card-header">
            <span class="impact-card-title">Rule 3 &amp; 4: Volume &amp; Return Guardrails</span>
            <span class="impact-card-tag badge-pass" id="impact-tag-3">GUARDRAILS MET</span>
          </div>
          <div class="impact-card-num" id="impact-num-3">96% Volume Kept</div>
          <p class="impact-card-desc" id="impact-desc-3">
            Preserves 95.81% ($18.58B) of lending volume (+$244.2M total value) and lifts portfolio LAROC to 4.40% (+14.9 bps).
          </p>
        </div>

        <!-- Card 4 -->
        <div class="impact-card" id="impact-card-4">
          <div class="impact-card-header">
            <span class="impact-card-title">Phase 3: Small Business &amp; Late Workout</span>
            <span class="impact-card-tag badge-warn" id="impact-tag-4">REVENUE AUDIT</span>
          </div>
          <div class="impact-card-num" id="impact-num-4">$240.1M Protected</div>
          <p class="impact-card-desc" id="impact-desc-4">
            Protects $240.1M in small business loans (15,416 notes at 30% default) and targets $588.5M in late workout loans.
          </p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="simulator-footer">
      <div>JOHN AMORES | CONSUMER CREDIT RISK &amp; UNDERWRITING OPTIMIZATION</div>
      <div>Consumer Credit Risk &amp; Underwriting Optimization Case Study | Verified LendingClub Analytical Base (1.35M completed loans / $19.4B book) &bull; <a href="index.html" style="color: var(--ink-black); font-weight: 700; margin-left: 8px;">&lt;- BACK TO CASE STUDY REPORT</a></div>
    </footer>

  </div>

"""

HTML_SUFFIX = """
    const state = {
      policyMode: 'active', // 'active' (Phase 1-3 ON) or 'legacy' (Unfiltered Baseline)
      activeProfileId: '208',
      applicant: {
        fico: 680,
        subgrade: 'C4',
        amount: 15000,
        term: 36,
        dti: 22,
        util: 54,
        purpose: 'debt_consolidation'
      }
    };

    // 5 One-Click Borrower Profiles
    const APPLICANT_PROFILES = {
      '104': {
        id: '104',
        name: 'Applicant #104: Prime Consolidation',
        fico: 715,
        subgrade: 'B2',
        amount: 16000,
        term: 36,
        purpose: 'debt_consolidation',
        dti: 15,
        util: 32
      },
      '208': {
        id: '208',
        name: 'Applicant #208: Subgrade C4 Margin Leak (Default Load)',
        fico: 680,
        subgrade: 'C4',
        amount: 15000,
        term: 36,
        purpose: 'debt_consolidation',
        dti: 22,
        util: 54
      },
      '312': {
        id: '312',
        name: 'Applicant #312: Phase 1 Dual-Risk Hard-Stop',
        fico: 662,
        subgrade: 'D3',
        amount: 18000,
        term: 36,
        purpose: 'debt_consolidation',
        dti: 29,
        util: 74
      },
      '419': {
        id: '419',
        name: 'Applicant #419: 5-Year Term Cap Trigger',
        fico: 668,
        subgrade: 'D1',
        amount: 20000,
        term: 60,
        purpose: 'credit_card',
        dti: 19,
        util: 48
      },
      '505': {
        id: '505',
        name: 'Applicant #505: Small Business Verification',
        fico: 690,
        subgrade: 'C2',
        amount: 25000,
        term: 36,
        purpose: 'small_business',
        dti: 18,
        util: 42
      }
    };

    // FICO to Subgrade auto-mapping helper
    function mapFicoToSubgrade(score) {
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
    }

    // Switch Policy Mode
    function setPolicyMode(mode) {
      state.policyMode = mode;
      document.getElementById('mode-active-btn').classList.toggle('active', mode === 'active');
      document.getElementById('mode-legacy-btn').classList.toggle('active', mode === 'legacy');
      updateApplicantDesk();
    }

    // Load one of the 5 Applicant Profiles
    function loadApplicantProfile(pid) {
      state.activeProfileId = pid;
      const prof = APPLICANT_PROFILES[pid];
      if (!prof) return;

      // Update queue buttons active style
      ['104', '208', '312', '419', '505'].forEach(id => {
        const btn = document.getElementById('qcard-' + id);
        if (btn) btn.classList.toggle('active', id === pid);
      });

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
    }

    // Handle FICO input slider change
    function handleFicoChange(val, autoTrigger = true) {
      const score = parseInt(val);
      state.applicant.fico = score;
      document.getElementById('desk-fico-display').innerText = score + ' FICO';

      // Update spectrum active segment
      let activeIndex = 0;
      let bandName = '< 660 (Sub-Floor)';
      let share = '< 0.01% (2 loans)';
      let bad = '0.00%';
      let laroc = '+20.96%';

      if (score < 660) {
        activeIndex = 0;
        bandName = '< 660 (Sub-Floor)';
        share = '< 0.01% (2 loans)';
        bad = '0.00%';
        laroc = '+20.96%';
      } else if (score <= 679) {
        activeIndex = 1;
        bandName = '660-679 (Subprime / Elevated Risk)';
        share = '34.15% (459.5K loans)';
        bad = '25.29%';
        laroc = '+3.09%';
      } else if (score <= 699) {
        activeIndex = 2;
        bandName = '680-699 (Lower Prime / Threshold)';
        share = '26.86% (361.3K loans)';
        bad = '21.44%';
        laroc = '+4.47%';
      } else if (score <= 719) {
        activeIndex = 3;
        bandName = '700-719 (Core Prime / Peak Profit)';
        share = '18.30% (246.2K loans)';
        bad = '17.29%';
        laroc = '+5.39%';
      } else if (score <= 749) {
        activeIndex = 4;
        bandName = '720-749 (Upper Prime)';
        share = '12.76% (171.7K loans)';
        bad = '13.34%';
        laroc = '+5.08%';
      } else {
        activeIndex = 5;
        bandName = '750+ (Super Prime)';
        share = '7.92% (106.6K loans)';
        bad = '8.89%';
        laroc = '+3.80%';
      }

      for (let i = 0; i < 6; i++) {
        const el = document.getElementById('band-seg-' + i);
        if (el) el.classList.toggle('active', i === activeIndex);
      }

      document.getElementById('band-active-name').innerText = bandName;
      document.getElementById('band-stat-share').innerText = share;
      document.getElementById('band-stat-bad').innerText = bad;
      document.getElementById('band-stat-laroc').innerText = laroc;

      if (autoTrigger) {
        const mappedSg = mapFicoToSubgrade(score);
        const sgSelect = document.getElementById('desk-subgrade');
        if (sgSelect.value !== mappedSg) {
          sgSelect.value = mappedSg;
          document.getElementById('desk-subgrade-hint').innerText = 'Auto: ' + mappedSg;
        }
        updateApplicantDesk();
      }
    }

    function setFicoVal(score) {
      document.getElementById('desk-fico').value = score;
      handleFicoChange(score);
    }

    function setAmountVal(amt) {
      document.getElementById('desk-amount').value = amt;
      document.getElementById('desk-amount-slider').value = amt;
      document.getElementById('desk-amount-val').innerText = '$' + amt.toLocaleString();
      updateApplicantDesk();
    }

    function handleDtiSlider(val, autoTrigger = true) {
      const num = parseInt(val);
      let bracketLabel = 'Low';
      if (num > 35) bracketLabel = 'Severe';
      else if (num > 25) bracketLabel = 'High';
      else if (num > 15) bracketLabel = 'Moderate';

      document.getElementById('desk-dti-val').innerText = num + '% [' + bracketLabel + ']';
      if (autoTrigger) updateApplicantDesk();
    }

    function handleUtilSlider(val, autoTrigger = true) {
      const num = parseInt(val);
      let bracketLabel = 'Low';
      if (num > 85) bracketLabel = 'Maxed';
      else if (num > 65) bracketLabel = 'High';
      else if (num > 40) bracketLabel = 'Moderate';

      document.getElementById('desk-util-val').innerText = num + '% [' + bracketLabel + ']';
      if (autoTrigger) updateApplicantDesk();
    }

    function setApplicantTerm(months, autoTrigger = true) {
      state.applicant.term = months;
      document.getElementById('desk-term-36').classList.toggle('active', months === 36);
      document.getElementById('desk-term-60').classList.toggle('active', months === 60);
      document.getElementById('desk-term-val').innerText = months + ' Months';
      if (autoTrigger) updateApplicantDesk();
    }

    // Update Applicant Desk decision memorandum and profitability predictor
    function updateApplicantDesk() {
      const subgradeVal = document.getElementById('desk-subgrade').value;
      const amountVal = parseFloat(document.getElementById('desk-amount').value) || 15000;
      const dtiVal = parseFloat(document.getElementById('desk-dti').value) || 22;
      const utilVal = parseFloat(document.getElementById('desk-util').value) || 54;
      const termVal = state.applicant.term;
      const ficoVal = parseInt(document.getElementById('desk-fico').value) || 680;
      const purposeVal = document.getElementById('desk-purpose').value;

      const sgData = PORTFOLIO_DATA.subgrades.find(s => s.sub_grade === subgradeVal) || {
        bad_rate_pct: 24.92,
        avg_int_rate: 14.71,
        net_laroc_pct: 3.44
      };

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
      if (state.policyMode === 'active') {

        // RULE 1: Phase 1 Subprime Dual-Risk Hard Stop
        if (isPhase1Trigger) {
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
        } else if (isC4) {
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
        } else if (isTermCapTrigger) {
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
        } else if (isSmallBusiness) {
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
        } else {
          badgeEl.className = 'ticket-status-badge status-approved';
          badgeEl.innerText = '[APPROVED: PRIME STANDARD TERMS]';

          // Override for Applicant #104 profile benchmark numbers
          if (subgradeVal === 'B2') {
            expLaroc = 6.02;
            cohortBadRate = 13.39;
          }

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
        }

      // ==============================================================
      // LEGACY MODE (UNFILTERED BASELINE - POLICIES BYPASSED)
      // ==============================================================
      } else {
        if (isPhase1Trigger) {
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

        } else if (isC4) {
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

        } else if (isTermCapTrigger) {
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

        } else if (isSmallBusiness) {
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

        } else {
          badgeEl.className = 'ticket-status-badge status-approved';
          badgeEl.innerText = '[APPROVED: PRIME STANDARD TERMS]';

          if (subgradeVal === 'B2') {
            expLaroc = 6.02;
            cohortBadRate = 13.39;
          }

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
        }
      }

      // Monthly payment formula
      const r = (recApr / 100.0) / 12.0;
      const n = termVal;
      const pmt = (amountVal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);

      badRateNumEl.innerText = cohortBadRate.toFixed(2) + '%';
      aprNumEl.innerText = recApr.toFixed(2) + '%';
      paymentSubEl.innerText = 'Monthly Installment: $' + pmt.toFixed(2);
    }

    // Interactive Rollout Adoption Selector (60% Pilot | 80% Year-1 Goal | 100% Full Rollout)
    function setRolloutAdoption(pct) {
      ['60', '80', '100'].forEach(p => {
        const btn = document.getElementById('btn-rollout-' + p);
        if (btn) btn.classList.toggle('active', p === String(pct));
      });

      const tag1 = document.getElementById('impact-tag-1');
      const num1 = document.getElementById('impact-num-1');
      const desc1 = document.getElementById('impact-desc-1');

      const tag2 = document.getElementById('impact-tag-2');
      const num2 = document.getElementById('impact-num-2');
      const desc2 = document.getElementById('impact-desc-2');

      const tag3 = document.getElementById('impact-tag-3');
      const num3 = document.getElementById('impact-num-3');
      const desc3 = document.getElementById('impact-desc-3');

      const tag4 = document.getElementById('impact-tag-4');
      const num4 = document.getElementById('impact-num-4');
      const desc4 = document.getElementById('impact-desc-4');

      if (pct === 60) {
        if (tag1) tag1.innerText = '11,129 DEFAULTS';
        if (num1) num1.innerText = '+$138.0M Saved';
        if (desc1) desc1.innerText = 'During a 60% pilot, targeted rules prevent 11,129 defaults, saving +$138.0M in net losses ($152.5M gross).';

        if (tag2) tag2.innerText = '44,653 LOANS';
        if (num2) num2.innerText = '+$8.5M Revenue';
        if (desc2) desc2.innerText = 'Repricing 60% of Subgrade C4 loans adds +$8.5M in interest revenue.';

        if (tag3) tag3.innerText = 'GUARDRAILS MET';
        if (num3) num3.innerText = '97% Volume Kept';
        if (desc3) desc3.innerText = 'Preserves 97% of lending volume, delivering +$146.5M in total value.';

        if (tag4) tag4.innerText = 'REVENUE AUDIT';
        if (num4) num4.innerText = '$240.1M Protected';
        if (desc4) desc4.innerText = 'Protects $240.1M in small business loans (15,416 notes) and targets $588.5M in late loans.';
      } else if (pct === 80) {
        if (tag1) tag1.innerText = '14,838 DEFAULTS';
        if (num1) num1.innerText = '+$184.0M Saved';
        if (desc1) desc1.innerText = 'At 80% Year-1 adoption, auto-declines prevent 14,838 defaults, saving +$184.0M in net losses ($203.3M gross).';

        if (tag2) tag2.innerText = '59,538 LOANS';
        if (num2) num2.innerText = '+$11.4M Revenue';
        if (desc2) desc2.innerText = 'Repricing 80% of Subgrade C4 volume generates +$11.4M in added interest revenue.';

        if (tag3) tag3.innerText = 'GUARDRAILS MET';
        if (num3) num3.innerText = '97% Volume Kept';
        if (desc3) desc3.innerText = 'Preserves 97% of lending volume, delivering +$195.4M in total value.';

        if (tag4) tag4.innerText = 'REVENUE AUDIT';
        if (num4) num4.innerText = '$240.1M Protected';
        if (desc4) desc4.innerText = 'Protects $240.1M in small business loans (15,416 notes) and targets $588.5M in late loans.';
      } else {
        // 100% Full Rollout
        if (tag1) tag1.innerText = '18,548 DEFAULTS';
        if (num1) num1.innerText = '+$230.0M Saved';
        if (desc1) desc1.innerText = 'Auto-declining Grades D-G with DTI > 25% & Card Usage > 65% prevents 18,548 defaults ($230.04M net / $254.10M gross saved).';

        if (tag2) tag2.innerText = '74,422 LOANS';
        if (num2) num2.innerText = '+$14.2M Revenue';
        if (desc2) desc2.innerText = 'Adding +1.5% (+150 bps) across 74,422 Subgrade C4 loans adds +$14.20M in interest income and restores +4.00% profit hurdle.';

        if (tag3) tag3.innerText = 'GUARDRAILS MET';
        if (num3) num3.innerText = '96% Volume Kept';
        if (desc3) desc3.innerText = 'Preserves 95.81% ($18.58B) of lending volume (+$244.2M total value) and lifts portfolio net return to 4.40% (+15 bps).';

        if (tag4) tag4.innerText = 'REVENUE AUDIT';
        if (num4) num4.innerText = '$240.1M Protected';
        if (desc4) desc4.innerText = 'Protects $240.1M in small business loans (15,416 notes at 30% default) and targets $588.5M in late workout loans.';
      }
    }

    // Populate subgrade dropdown
    function populateSubgradeDropdown() {
      const select = document.getElementById('desk-subgrade');
      select.innerHTML = '';
      PORTFOLIO_DATA.subgrades.forEach(sg => {
        const opt = document.createElement('option');
        opt.value = sg.sub_grade;
        opt.innerText = sg.sub_grade + ' (Bad: ' + sg.bad_rate_pct.toFixed(1) + '%, APR: ' + sg.avg_int_rate.toFixed(1) + '%, LAROC: ' + sg.net_laroc_pct.toFixed(1) + '%)';
        if (sg.sub_grade === 'C4') opt.selected = true;
        select.appendChild(opt);
      });
    }

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {
      populateSubgradeDropdown();
      // Load Applicant #208 (Subgrade C4 Margin Leak) as default load
      loadApplicantProfile('208');
    });
  </script>
</body>
</html>
"""


def build_underwriting_simulator_html():
    cube_path = Path("data/exports/underwriting_simulator_cube.json")
    if not cube_path.exists():
        cube_path = Path("data/exports/cockpit_cube.json")
    if not cube_path.exists():
        raise FileNotFoundError(f"Missing cube data: {cube_path}")

    with open(cube_path, "r", encoding="utf-8") as f:
        cube_json_str = f.read().strip()

    middle_marker = (
        "  <!-- Embedded Empirical Portfolio Data Cube -->\n"
        "  <script>\n"
        "    const PORTFOLIO_DATA = "
    )
    post_marker = ";\n\n    // State"
    html_content = HTML_PREFIX + middle_marker + cube_json_str + post_marker + HTML_SUFFIX

    out_file = Path("underwriting-simulator.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[TASK] Built standalone workstation: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")
    return out_file


# Backward-compatible alias
build_cockpit_html = build_underwriting_simulator_html


if __name__ == "__main__":
    build_underwriting_simulator_html()
