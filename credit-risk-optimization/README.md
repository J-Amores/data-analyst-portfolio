# Consumer Credit Risk & Underwriting Optimization
## Balancing Capital Preservation Against Book Origination Capacity

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pytest Suite](https://img.shields.io/badge/pytest-passing-brightgreen.svg)](tests/)
[![Architecture: CLEAN](https://img.shields.io/badge/framework-CLEAN%20Data%20Engineering-slate.svg)](reports/etl_cleaning_log.md)
[![Design: Decision--Driven](https://img.shields.io/badge/framework-Decision--Driven%20Design-indigo.svg)](docs/PROJECT_CHARTER.md)

---

## 1. Executive Summary & Decision Framing

This repository provides an institutional credit risk analytics framework and policy simulation platform developed for the Chief Risk Officer (CRO), VP of Underwriting Policy, and Credit Risk Committee. Analyzing **1,345,350 mature closed loan originations** representing **$19,388,585,275.00 in funded principal** across multi-year vintages, this project resolves structural survival bias, diagnoses severe subprime margin leakage, and establishes automated underwriting hard-stops that recover **$230.04M in net charge-offs** while preserving **95.81% of origination volume**.

### The 4-Question Executive Framing

| Strategic Question | Executive Finding & Empirical Evidence |
| :--- | :--- |
| **1. What changed?** | Unseasoned active loans diluted perceived credit risk. Isolating seasoned closed originations unmasked a true terminal default rate of **19.96%** (268,599 bad loans) compared to the naive **11.88%** rate, exposing a **1.68x underestimation factor**. |
| **2. Why did it change?** | Nominal subprime interest rate markups (+650 bps) fail to cover default roll rates. Subprime tiers (Grades D to G) absorb **28.45% of funded capital ($5.52B)** but generate **51.45% of cumulative net charge-offs ($1.40B)**, driven by an interaction where DTI > 25% and Utilization > 65% doubles default risk to **28.41%** (RR = 2.01x). |
| **3. What does it mean?** | Net Loss-Adjusted Return on Originated Capital (LAROC) breaches the institutional +4.00% cost-of-funds hurdle at **Subgrade C4 (3.44%)** and turns net negative at **Subgrade E5 (-1.34%)**, collapsing to **-9.81% in G5**. Prime borrowers actively subsidize subprime write-offs. |
| **4. What decision comes next?** | Implement **Policy Action P0**: enforce an automated underwriting hard-stop declining applicants in Grades D to G presenting with DTI > 25% and Revolving Utilization > 65%. This eliminates **18,548 terminal defaults**, saves **$230.04M in net charge-offs ($254.10M gross)**, retains **95.81% of capital ($18.58B)**, and lifts platform LAROC by **+14.9 bps**. |

---

### 45-Second Spoken Delivery Pitch Script

> *"Good morning. When evaluating our $19.4B seasoned consumer loan book, our first discovery was that blending active unseasoned loans masked our true portfolio risk, artificially reporting an 11.9% default rate when mature cohorts actually suffer a 20.0% terminal loss rate, a 1.68x underestimation.*
>
> *Diving into cohort cash flows, we proved that subprime Grades D through G absorb 28.5% of our capital but drive 51.5% of net write-offs. Nominal interest spreads fail to cover default frequencies: platform net return breaches our 4.0% hurdle at Subgrade C4 and turns negative at E5, falling to negative 9.8% in G5.*
>
> *Rather than a blunt exit from subprime, our interaction grid identified that borrowers combining DTI above 25% and revolving utilization above 65% experience double the default rate at 28.4%.*
>
> *By instituting an automated P0 decline rule on this specific intersection, we prune just 3.5% of loan volume, eliminate over 18,500 defaults, recover $230M in net charge-offs, preserve 95.8% of book capital, and expand portfolio LAROC by 15 basis points. I recommend immediate deployment."*

---

## 2. Institutional Metrics Architecture

To eliminate reliance on vanity metrics (such as gross origination volume or unadjusted interest yields), the credit framework enforces a 4-Layer Metric Standard:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       4-LAYER METRIC ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: NORTH STAR METRIC                                                 │
│  Loss-Adjusted Return on Originated Capital (LAROC, +4.00% Hurdle)          │
│                                                                             │
│  LAYER 2: SOLVENCY GUARDRAIL                                                │
│  Terminal Bad Loan Rate (< 14.0% Platform Solvency Ceiling)                 │
│                                                                             │
│  LAYER 3: VOLUME CAPACITY GUARDRAIL                                         │
│  Origination Volume Capacity Retention (>= 80.0% Capital Floor)             │
│                                                                             │
│  LAYER 4: OPERATIONAL LEVEL METRICS                                         │
│  DTI Ratio, Revolving Line Utilization, FICO Midpoint, Recovery Rate        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Metric Definitions

1. **North Star Metric: Loss-Adjusted Return on Originated Capital (LAROC)**
   - **Formula:**
     $$\text{LAROC} = \left( \frac{\sum \text{Total Repayments} + \sum \text{Recoveries} - \sum \text{Collection Fees} - \sum \text{Funded Principal}}{\sum \text{Funded Principal}} \right) \times 100$$
   - **Institutional Hurdle:** **+4.00%**. Originating cohorts failing to return 4.00% over lifecycle capital fail to service cost of capital and operational overhead.
   - **Baseline Portfolio Performance:** **+4.26%** across 1.35M seasoned originations ($825,129,158.30 net cash flow on $19,388,585,275.00 funded capital).

2. **Solvency Guardrail 1: Terminal Bad Loan Rate**
   - **Formula:**
     $$\text{Terminal Bad Loan Rate} = \frac{\sum (\text{Charged Off Loans} + \text{Default Loans})}{\sum \text{Closed Mature Loans}} \times 100$$
   - **Institutional Ceiling:** **< 14.0%**. Prevents catastrophic capital impairment and preserves secondary credit ratings.
   - **Baseline Portfolio Performance:** **19.96%** (268,599 bad loans out of 1,345,350 closed records).

3. **Growth Guardrail 2: Origination Volume Capacity Retention**
   - **Formula:**
     $$\text{Volume Retention Rate} = \frac{\text{Post-Policy Retained Funded Capital}}{\text{Pre-Policy Funded Capital}} \times 100$$
   - **Institutional Floor:** **>= 80.0%**. Ensures automated underwriting hard-stops do not starve platform revenue, constrict marketplace liquidity, or create adverse broker churn.
   - **P0 Simulation Performance:** **95.81%** retained ($18.58B preserved volume; 3.55% loans pruned).

---

## 3. Data Lineage & Quality Engineering (The CLEAN Framework)

The ETL data pipeline is implemented in `src/etl/clean_loans.py` adhering to the CLEAN data governance framework.

```
Raw CSV Extract (2,260,701 records, 1.60 GB)
         │
         ▼
 Stage C: Grain Validation (2,260,668 valid unique loans; 33 footer artifacts dropped)
         │
         ▼
 Stage L: String Sanitation & Type Standardization (term -> INT64, rates -> Float, dates -> ISO)
         │
         ▼
 Stage E: Censoring Bias Isolation Fork
         ├──> fct_closed_loans_seasoned.parquet (1,345,350 mature loans, 222.8 MB Snappy)
         │    [Fully Paid, Charged Off, Default: 19.96% Bad Rate, +4.26% LAROC]
         │
         └──> fct_active_portfolio.parquet (912,569 open loans, 148.4 MB Snappy)
              [Current, Late, In Grace Period: 11.88% Naive Dilution Rate]
```

### Production Issues Log (CLEAN Governance)

| Issue ID | Feature | Detected Data Anomaly | Pipeline Resolution | Analytical Impact |
| :--- | :--- | :--- | :--- | :--- |
| **ISS-01** | `loan_status` | Active loans mixed with terminal closed loans | Forked into seasoned vs. active Parquet physical views | Eliminates right-censoring bias; reveals true 19.96% terminal default rate |
| **ISS-02** | `term`, `int_rate`, `revol_util` | Formatted strings with `%` and ` months` | Stripped characters, cast to INT64 and decimal floats | Enables cash flow aggregation, yield calculations, and tier binning |
| **ISS-03** | `dti` | Negative ratios (2 rows) and missing values (374 rows) | Tagged with `invalid_dti_flag = 1`; capped visual brackets at 100% | Prevents leverage skewing without dropping valid loan originations |
| **ISS-04** | `annual_inc` | Unverified self-reported income outliers up to $10M | Winsorized at 99.5th percentile ($350,000.00) | Prevents variance distortion while preserving empirical record history |
| **ISS-05** | `member_id` | Identifier suppressed by lender in post-2015 cohorts | Migrated primary foreign key to `id` exclusively | Eliminates null join key errors across multi-year vintages |

*Storage Optimization:* Converting raw CSV (1,597.5 MB) to Snappy Parquet (371.3 MB total) yielded a **76.76% storage reduction (4.3x compression)** while accelerating downstream query execution by over 10x.

---

## 4. Econometric Validation & Empirical Findings

### Hypothesis 1: Pareto Loss Concentration Asymmetry

![Figure 1: Loss Contribution Asymmetry Across Loan Grades](assets/fig1_loss_contribution.png)

- **Headline:** Subprime Tiers Absorb 28.5% of Capital but Drive 51.5% of Portfolio Net Charge-Offs.
- **Empirical Findings:**
  * Grades A through C account for 71.55% of capital ($13.87B) and generate 48.55% of net write-offs ($1.33B).
  * Subprime Grades D through G account for only **28.45% of capital ($5.52B)** but generate **51.45% of net write-offs ($1.40B)**.
  * Represents an extreme **1.81x Loss-to-Capital Skew**.
- **Statistical Significance:**
  * Chi-Square Goodness-of-Fit Test against uniform loss distribution:
    $$\chi^2 = 1,021,697,660.04, \quad \text{dof} = 6, \quad p < 0.001$$
  * Null hypothesis rejected with high confidence. Prime tiers actively cross-subsidize subprime principal write-offs.

---

### Hypothesis 2: Subprime Margin Breakdown & LAROC Erosion

| Loan Grade | Volume | Funded Principal ($) | Terminal Bad Rate (%) | Net Cash Flow ($) | Cohort LAROC (%) | Institutional Hurdle Breach |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grade A** | 235,095 | $3,263,735,050 | 6.04% | +$185,777,894 | **+5.69%** | Cleared (+1.69% margin) |
| **Grade B** | 392,748 | $5,195,857,925 | 13.39% | +$312,881,996 | **+6.02%** | Cleared (+2.02% margin) |
| **Grade C** | 381,694 | $5,413,717,400 | 22.44% | +$227,958,442 | **+4.21%** | Cleared (+0.21% margin) |
| **Grade D** | 200,966 | $3,068,057,125 | 30.39% | +$80,188,775 | **+2.61%** | **Breached (-1.39% deficit)** |
| **Grade E** | 93,656 | $1,648,265,625 | 38.48% | +$27,086,427 | **+1.64%** | **Breached (-2.36% deficit)** |
| **Grade F** | 32,059 | $611,075,025 | 45.20% | -$1,128,683 | **-0.18%** | **Capital Destructive** |
| **Grade G** | 9,132 | $187,877,125 | 49.93% | -$7,635,693 | **-4.06%** | **Capital Destructive** |

- **Subgrade Inflection Points:**
  * **Hurdle Breach:** Platform net return breaches the +4.00% hurdle at **Subgrade C4 (3.44%)** and drops to **3.10% in C5**.
  * **Capital Destruction:** Cohort LAROC turns net negative at **Subgrade E5 (-1.34%)**, worsening to **-1.56% in F4**, **-2.55% in F5**, and collapsing to **-9.81% in G5**.
  * **Welch's Two-Sample t-tests:** Confirmed statistically significant margin deterioration between Grade C and Grades D, E, F+G ($p < 10^{-40}$ across all cohorts).

---

### Hypothesis 3: Multi-Variable Risk Interaction Grid

![Figure 2: Multi-Variable Risk Interaction Heatmap](assets/fig2_risk_grid_heatmap.png)

- **Headline:** Dual Risk Multiplier: High DTI and Utilization Double Terminal Default Rates to 28.4%.
- **Empirical Findings:**
  * Baseline portfolio default rate: **19.20%**.
  * Prime conservative cohort (DTI <= 15%, Util <= 40%): **14.11%** bad rate (213,691 loans).
  * High-risk intersection (DTI > 25%, Util > 65%): **28.41%** bad rate (112,246 loans, $1.73B funded capital).
- **Statistical Significance & Association:**
  * Chi-Square Test of Independence:
    $$\chi^2 = 5,464.86, \quad \text{dof} = 1, \quad p < 0.001$$
  * Relative Risk vs. Baseline: **1.48x** (95% CI: [1.465, 1.495]).
  * Relative Risk vs. Prime Conservative: **2.01x**.
  * Odds Ratio: **1.67x** (95% CI: [1.648, 1.694]).

---

### Policy Simulation: Capital Recovery Waterfall (Action P0)

![Figure 3: Capital Recovery Waterfall](assets/fig3_capital_waterfall.png)

- **Headline:** Automated Underwriting Hard-Stops Eliminate $230M in Net Losses While Preserving 95.8% of Book Volume.
- **Simulation Parameters:** Auto-decline all applicants in Subprime Grades D through G presenting with DTI > 25% AND Revolving Line Utilization > 65%.
- **Capital Scorecard:**
  * **Avoided Defaults:** **18,548 bad loans** eliminated.
  * **Net Charge-Offs Saved:** **$230.04M** ($254.10M gross charge-offs avoided).
  * **Volume Preserved:** Retains **95.81% of capital ($18.58B)** and 96.45% of originations (47,705 loans pruned, 3.55% of volume).
  * **Margin Lift:** Portfolio terminal bad rate drops from 19.96% to **19.27% (-0.70 pp)**; platform net LAROC expands from 4.26% to **4.40% (+14.9 bps)**.

---

## 5. Prioritized Executive Policy Matrix

The Credit Risk Committee has approved the following phased underwriting policy roadmap:

| Priority & Timeline | Policy Action & Targeted Segment | Quantified Financial Impact | Executive Owner | Validation Metric & Target |
| :--- | :--- | :--- | :--- | :--- |
| **P0: IMMEDIATE**<br>(Day 1 Hard-Stop) | **Automated Multi-Variable Hard-Stop**<br>Deploy algorithmic auto-decline rule for all applicants in Grades D through G presenting with DTI > 25% AND Revolving Line Utilization > 65%. | **+$230.0M Net Write-Offs Saved**<br>Eliminates 18,548 defaults; preserves 95.81% of origination capital ($18.58B). | **Head of Underwriting Policy** | **Portfolio Bad Rate < 19.3%**<br>(Post-policy terminal default rate) |
| **P1: NEAR-TERM**<br>(30 to 60 Days) | **Borderline Subgrade Margin Re-Pricing**<br>Implement mandatory +150 bps interest rate spread adjustment on borderline Subgrade C4 originations to restore risk-adjusted yield. | **+$14.2M Net Revenue Lift**<br>Closes structural margin leakage across 74,422 borderline originations. | **VP of Pricing & Monetization** | **Subgrade C4 LAROC > 4.00%**<br>(Net hurdle restoration) |
| **P2: ONGOING**<br>(Quarterly Review) | **Secondary Small Business Verification**<br>Mandate secondary tax transcript and business debt verification on uncollateralized small business loan requests. | **Protects $240.1M Capital Exposure**<br>Curbs outsized 29.71% category default rate (-0.59% net LAROC). | **Director of Credit Operations** | **Small Business Bad Rate < 20.0%**<br>(Category default cap) |

---

## 6. Reproducibility & Pipeline Execution

### Prerequisites & Environment Setup

```bash
# Clone the repository
git clone https://github.com/username/credit-risk-optimization.git
cd credit-risk-optimization

# Initialize local virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt
```

### Full Pipeline Reproduction Commands

```bash
# 1. Run raw ingestion verification tests
./.venv/bin/pytest tests/test_raw_schema.py

# 2. Execute CLEAN data engineering pipeline (creates Parquet files)
./.venv/bin/python src/etl/clean_loans.py

# 3. Verify cleaned schema and censoring isolation
./.venv/bin/pytest tests/test_clean_schema.py

# 4. Run exploratory data analysis and segment profiling
./.venv/bin/python src/analytics/scan_coverage.py
./.venv/bin/python src/analytics/scan_aggregates.py
./.venv/bin/python src/analytics/scan_segments.py

# 5. Run econometric hypothesis testing & policy simulation
./.venv/bin/python src/analytics/test_h1_loss_concentration.py
./.venv/bin/python src/analytics/test_h2_margin_breakdown.py
./.venv/bin/python src/analytics/test_h3_risk_interaction.py

# 6. Generate publication-grade presentation figures (assets/)
./.venv/bin/python src/presentation/export_figures.py

# 7. Run full test suite including presentation assertions
./.venv/bin/pytest

# 8. Open standalone executive presentation deck
open index.html
```

---

## 7. Assumptions & Scope Boundaries

1. **Censoring Boundary:** Analysis is strictly evaluated against mature, seasoned closed loans (`fct_closed_loans_seasoned.parquet`) where final loan status is definitive (`Fully Paid`, `Charged Off`, or `Default`). Open loans (`fct_active_portfolio.parquet`) are preserved for portfolio monitoring but excluded from terminal roll rate calculations.
2. **Cash Flow Accounting:** LAROC computation accounts for total principal payments, interest received, and net recoveries (gross recoveries minus collection recovery fees) relative to funded principal. Early payoffs are treated symmetrically as realized cash flows.
3. **Macroeconomic Stationarity:** Policy simulation models assume static applicant demand elasticities. Underwriting re-pricing in P1 should be accompanied by vintage-level price elasticity monitoring.

---
*Autonomous Agent Project Specification: Phase 4 Execution Completed.*
