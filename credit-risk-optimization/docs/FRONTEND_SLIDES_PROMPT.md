/frontend-slides:frontend-slides

Generate a 7-slide executive case study presentation deck in standalone HTML based on my consumer credit risk analysis.

### DECK PARAMETERS & DESIGN DIRECTIVES
- Purpose: Portfolio Showcase / Case Study (Executive Decision Partner)
- Content Density: Reading-first (optimized for asynchronous recruiter and hiring manager review in under 60 seconds)
- Visual Style Direction: Cobalt Grid (navy and slate canvas, crisp typography, clean data grid aesthetic, zero gratuitous gradients)
- Prose Guardrail: Do not use em dashes or conversational AI filler. Every slide must feature a story-driven newsflash headline, bold metric callouts, and clear context blocks.
- Media Paths: Map all figures using local repository paths in `./assets/` (or absolute local paths).

---

### THE 3-ACT DATA-DRIVEN NARRATIVE ARC

Act I: The Beginning (Slides 1–3) — Setting the Stakes
- Mandate & Solvency Dilemma
- 3-Layer Metric Model (LAROC, Bad Loan Rate, Volume Capacity)
- 1.68x Right-Censoring Bias Resolution

Act II: The Middle (Slides 4–5) — The Diagnostic Core
- Subprime Loss Contribution Asymmetry (28.5% Capital vs. 51.5% Losses)
- Multi-Variable Risk Multiplier Grid (DTI > 25% and Utilization > 65%)
- Subprime Capital Destruction Tiers (Subgrade C4 Hurdle Breach to G5 Deficit)

Act III: The Conclusion (Slides 6–7) — Strategic Resolution & Governance
- P0 Policy Simulation & Capital Recovery Waterfall ($230M Net Write-Offs Saved)
- Volume Capacity Preservation (95.81% Retained vs. 80.0% Guardrail)
- Prioritized Executive Underwriting Roadmap (P0 to P2 Matrix)

---

### SLIDE OUTLINE & CONTENT SPECIFICATION

#### ACT I: THE BEGINNING (CONTEXT, MANDATE & LINEAGE)

- Slide 1: Title & Executive Summary
  - Title: Consumer Credit Risk & Underwriting Optimization
  - Subtitle: Balancing Capital Preservation Against Book Origination Capacity
  - Portfolio Scope: 1,345,350 seasoned, closed loan originations across multi-year vintages
  - Capital Evaluated: $19.39B in funded consumer debt ($825.13M cumulative platform net cash flow)
  - Target Audience: Chief Risk Officer (CRO), VP of Credit Underwriting Policy, Credit Risk Committee
  - Candidate Metadata: Candidate Name, Target Role (Senior Risk / Credit Analyst), links to GitHub Repository and LinkedIn

- Slide 2: The Executive Mandate & Metric Architecture
  - Newsflash Headline: Surging Subprime Charge-Offs Threaten Platform Solvency, Demanding Empirical Underwriting Hard-Stops
  - The Decision Problem: Top-line gross interest yield from subprime originations creates an illusion of profitability that masks catastrophic principal write-offs.
  - Metric Architecture (3-Card Layout):
    * North Star Metric: Loss-Adjusted Return on Originated Capital (LAROC) benchmarked against an institutional +4.00% platform cost-of-capital hurdle.
    * Guardrail 1 (Solvency): Portfolio Terminal Bad Loan Rate held strictly < 14.0%.
    * Guardrail 2 (Growth Capacity): Origination Volume Capacity Retention >= 80.0% of funded book.

- Slide 3: Data Lineage & Quality Engineering (The CLEAN Framework)
  - Newsflash Headline: Resolving Right-Censoring Bias Across 2.26M Records Unmasks a 1.68x Underestimation in Portfolio Risk
  - Censoring Isolation Fork:
    * Ingested 2,260,668 valid funded originations; 40.37% (912,569 loans) were active and unseasoned, deflating the naive default rate to 11.88%.
    * Engineered Parquet split isolating 1,345,350 mature closed loans (Fully Paid / Charged Off / Default), unmasking the true terminal default rate of 19.96% (268,599 bad loans).
    * Censoring Distortion Factor: 1.68x (~40.5% risk underestimation in naive analysis).
  - Production Issues Log Highlights: String sanitation on terms and rates, 99.5th percentile income winsorization, and foreign key stability on suppressed post-2015 member IDs.

---

#### ACT II: THE MIDDLE (DIAGNOSTIC CORE & ROOT-CAUSE MECHANISMS)

- Slide 4: Primary Insight: Subprime Loss Contribution Skew
  - Newsflash Headline: Subprime Tiers (Grades D–G) Absorb 28.5% of Capital but Drive 51.5% of Portfolio Net Charge-Offs
  - Image Path: [INSERT ABSOLUTE PATH TO ./assets/fig1_loss_contribution.png]
  - Analytical Evidence:
    * Asymmetry: Grades D through G account for $5.52B in funded principal (28.45% of book) but generate $1.40B in net charge-offs (51.45% of total losses), representing a 1.81x loss skew (Chi-Square: 1.02B, p < 0.001).
    * Subprime Margin Breakdown: Nominal rate spreads (+650 bps) fail to cover default roll rates. Platform net LAROC permanently breaches the +4.00% hurdle at Subgrade C4 (3.44%) and turns negative at Subgrade E5 (-1.34%), degrading to -9.81% in G5.
    * Takeaway: Prime borrowers (Grades A–C) actively subsidize subprime write-offs.

- Slide 5: Secondary Insight: The Multi-Variable Risk Multiplier
  - Newsflash Headline: Dual Risk Multiplier: High DTI (>25%) and Utilization (>65%) Double Terminal Default Rates to 28.4%
  - Image Path: [INSERT ABSOLUTE PATH TO ./assets/fig2_risk_grid_heatmap.png]
  - Analytical Evidence:
    * The Interaction: Borrowers pairing debt-to-income > 25% with revolving line utilization > 65% experience a 28.41% terminal default rate.
    * Statistical Association: Relative Risk is 2.01x vs. prime conservative borrowers (14.11% default rate), confirmed with Chi-Square = 5,464.86, p < 0.001, and Odds Ratio = 1.67x.
    * Capital Exposure: Captures 112,246 loans ($1.73B funded capital) with median LAROC depressed to +3.41%, pinpointing the exact boundary for underwriting intervention.

---

#### ACT III: THE CONCLUSION (INTERVENTION, CAPITAL WATERFALL & ROADMAP)

- Slide 6: Policy Intervention & Capital Recovery Waterfall
  - Newsflash Headline: Automated Underwriting Hard-Stops Eliminate $230M in Net Losses While Preserving 95.8% of Book Volume
  - Image Path: [INSERT ABSOLUTE PATH TO ./assets/fig3_capital_waterfall.png]
  - Policy Simulation Results:
    * Simulated P0 Action: Decline all applicants in Grades D through G presenting with DTI > 25% AND Revolving Line Utilization > 65%.
    * Capital Recovered: Eliminates 18,548 terminal defaults, saving $230.04M in net charge-offs ($254.10M gross losses avoided).
    * Volume Capacity Preserved: Prunes only 3.55% of loan volume (47,705 loans) and retains 95.81% of funded capital ($18.58B), surpassing the 80.0% Guardrail 2 requirement.
    * Margin Expansion: Portfolio terminal default rate drops to 19.27% (-0.70 pp), and platform net LAROC expands from 4.26% to 4.40% (+14.9 bps margin expansion).

- Slide 7: Prioritized Underwriting Roadmap (P0–P2)
  - Newsflash Headline: Strategic Underwriting Policy Recommendations for the Credit Risk Committee
  - Decision Table Layout:
    * P0 (Immediate Policy Hard-Stop): Auto-decline Grades D–G applicants with DTI > 25% and Revolving Utilization > 65% | Financial Impact: +$230.0M Net Write-Offs Saved; 18,548 defaults avoided | Owner: Head of Underwriting Policy | Validation Metric: Portfolio Terminal Default Rate (<19.3%).
    * P1 (Near-Term Margin Re-Pricing): Implement +150 bps interest rate spread adjustment on borderline Subgrade C4 originations | Financial Impact: +$14.2M Incremental Net Interest Income | Owner: VP of Pricing & Monetization | Validation Metric: Subgrade C4 Net LAROC restored to > 4.00%.
    * P2 (Ongoing Verification Operations): Mandate secondary income and debt verification on uncollateralized small business loan requests | Financial Impact: Curbs 29.71% category default rate (-0.59% net LAROC); protects $240.1M in high-exposure loans | Owner: Director of Credit Operations | Validation Metric: Small Business Bad Rate (<20.0%).