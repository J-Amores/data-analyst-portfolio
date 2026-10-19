/frontend-slides:frontend-slides

Generate a 7-slide executive case study presentation deck in standalone HTML based on my consumer credit risk analysis.

Deck Parameters:
- Purpose: Portfolio Showcase / Case Study
- Content Density: Reading-first (asynchronous hiring manager / executive review)
- Visual Style Direction: Cobalt Grid or Swiss Modern (professional financial risk aesthetic, navy/slate foundation with crisp accent indicators)

Slide Outline & Content:
- Slide 1: Title & Executive Summary
  - Title: Consumer Credit Risk & Underwriting Optimization
  - Subtitle: Balancing Capital Preservation Against Book Origination Capacity
  - Context: 1.35M seasoned LendingClub loan originations ($18.5B funded capital)
  - Links: GitHub Repository, Portfolio Home, LinkedIn

- Slide 2: Executive Mandate & Decision Context
  - Header: Curbing Portfolio Credit Loss Leakage Without Constraining Prime Lending
  - Decision: CRO setting automated underwriting cutoffs to prevent subprime adverse selection
  - Key Metrics: North Star LAROC (Loss-Adjusted Return on Capital, +4.0% hurdle), Risk Guardrail (Bad Loan Rate <14.0%), Capacity Guardrail (Volume Retention >=80.0%)

- Slide 3: Data Lineage & Quality Engineering (CLEAN Framework)
  - Header: Resolving Right-Censoring Bias Across 2.26M Raw Records
  - Highlight: Segregated ~890k active/censored loans from 1.35M mature closed loans to unmask true terminal risk
  - Engineering Checks: String sanitation on term/interest rates, winsorization of extreme income outliers, and suppression handling

- Slide 4: Primary Insight — The Loss Concentration Asymmetry
  - Headline: Subprime Grades D–G Account for 68% of Total Cumulative Write-Offs
  - Image Path: [INSERT ABSOLUTE PATH TO ./assets/fig1_loss_concentration.png]
  - Takeaway: Subprime pricing premiums fail to cover default roll rates, generating a net $14.8M margin drain

- Slide 5: Secondary Insight — Multi-Variable Risk Interaction
  - Headline: Dual-Trigger Hard-Stop: DTI > 25% and Revolving Utilization > 65% Spikes Defaults 2.3x
  - Image Path: [INSERT ABSOLUTE PATH TO ./assets/fig2_risk_grid_heatmap.png]
  - Takeaway: Non-linear default clustering across debt-consolidation cohorts identifies the optimal policy intervention boundary

- Slide 6: Policy Intervention & Financial Impact Waterfall
  - Headline: Proposed Underwriting Hard-Stops Eliminate $14.8M in Losses While Preserving 91.8% of Originations
  - Image Path: [INSERT ABSOLUTE PATH TO ./assets/fig3_capital_waterfall.png]
  - Takeaway: Targeted pruning of 8.2% of toxic applicants satisfies the 80% volume retention guardrail and recovers portfolio margin

- Slide 7: Prioritized Underwriting Roadmap (P0–P2)
  - Headline: Strategic Policy Recommendations for the Credit Risk Committee
  - Table Structure:
    * P0 (Policy Hard-Stop): Decline Grade D-G with DTI > 25% & Util > 65% | Impact: -$14.8M write-offs | Owner: Head of Underwriting
    * P1 (Risk Re-Pricing): +150 bps spread adjustment on borderline Grade C | Impact: +$3.4M net interest yield | Owner: VP Pricing
    * P2 (Verification Operations): Mandatory secondary verification on small business loans | Impact: Lowers sector default rate to <19% | Owner: Credit Ops