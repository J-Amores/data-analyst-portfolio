# ==============================================================================
# docs/AGENT_TASKS.md
# ==============================================================================

# Autonomous Agent Task Plan: Google Antigravity Agent Execution Specification
# Target Domain: Consumer Credit Risk & Underwriting Optimization (LendingClub Book)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SEQUENTIAL AGENT WORKFLOW ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 1: Environment Setup, Virtualenv, Directory Scaffolding & Py Tests   │
│                                      │                                      │
│                                      ▼                                      │
│  PHASE 2: The SCAN Exploratory Data Analysis Pipeline (S -> C -> A -> N)   │
│                                      │                                      │
│                                      ▼                                      │
│  PHASE 3: Statistical Hypothesis Validation & Econometric Risk Modeling     │
│                                      │                                      │
│                                      ▼                                      │
│  PHASE 4: Executive Presentation Build & Asset Pipeline (Frontend-Slides)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Environment Setup & Data Pipeline Foundation
[Framework: Decision-Driven Design] [Framework: CLEAN][cite: 3, 7, 12]

* [x] **Task 1.1: Environment Initialization & Directory Scaffolding**
  * Initialize a dedicated Python 3.11 virtual environment: `python3.11 -m venv .venv && source .venv/bin/activate`.
  * Build the production directory hierarchy:
    ```bash
    mkdir -p data/{raw,cleaned,exports} docs/ src/{etl,analytics,presentation} tests/ assets/ reports/
    ```
  * Pin and install core scientific, testing, and charting dependencies in `requirements.txt`:
    `pandas>=2.2.0`, `numpy>=1.26.0`, `pyarrow>=15.0.0`, `scipy>=1.12.0`, `statsmodels>=0.14.1`, `matplotlib>=3.8.0`, `seaborn>=0.13.0`, `pytest>=8.0.0`[cite: 3].

* [x] **Task 1.2: Ingestion & Raw Schema Verification Harness**
  * Place the downloaded LendingClub dataset (`accepted_2007_to_2018Q4.csv`) into `data/raw/`[cite: 3].
  * Implement `tests/test_raw_schema.py` asserting that all required underwriting and performance columns defined in `docs/DATA_SPEC.md` (`loan_amnt`, `funded_amnt`, `term`, `int_rate`, `grade`, `sub_grade`, `loan_status`, `dti`, `revol_util`, `fico_range_low`, `fico_range_high`, `total_pymnt`, `recoveries`) exist prior to pipeline execution[cite: 3, 7].

* [x] **Task 1.3: CLEAN Pipeline Implementation (`src/etl/clean_loans.py`)**
  * **C – Conceptualize:** Enforce table grain (1 row = 1 funded loan origination)[cite: 7]. Assert uniqueness on primary key `id`[cite: 7].
  * **L – Locate Solvable Issues:**
    * Strip whitespace and strings from `term` (`' 36 months'` $\rightarrow$ `36`, `' 60 months'` $\rightarrow$ `60` as INT64)[cite: 7, 11].
    * Strip `%` from `int_rate` and `revol_util`, dividing by 100 to cast as numeric decimals (`0.1349`)[cite: 7, 11].
    * Standardize `emp_length` into integer years: map `'< 1 year'` to 0, `'10+ years'` to 10, nulls to `np.nan`[cite: 7, 11].
    * Parse `issue_d` and `earliest_cr_line` from `MMM-YYYY` strings into ISO dates (`YYYY-MM-01`)[cite: 7, 11].
  * **E – Evaluate Unsolvable Issues (Censoring Isolation):**
    * Segregate mature closed loans from active/unseasoned loans to prevent survival bias[cite: 3, 7, 11]:
      * Save `loan_status IN ('Fully Paid', 'Charged Off', 'Default')` to `data/cleaned/fct_closed_loans_seasoned.parquet`[cite: 3, 7].
      * Save `loan_status IN ('Current', 'In Grace Period', 'Late (16-30 days)', 'Late (31-120 days)')` to `data/cleaned/fct_active_portfolio.parquet`[cite: 3, 7].
    * Filter out invalid negative DTIs; cap visual DTI representations at 100.0% without dropping valid loans[cite: 7, 11].
    * Winsorize extreme self-reported `annual_inc` values at the 99.5th percentile for distribution modeling[cite: 7, 11].
  * **A – Augment Analytical Features:**
    * `is_bad_loan`: Binary indicator (1 if `'Charged Off'` or `'Default'`, 0 if `'Fully Paid'`)[cite: 7, 11].
    * `net_cash_flow`: `total_pymnt + recoveries - collection_recovery_fee - funded_amnt`[cite: 7, 11].
    * `laroc`: `(net_cash_flow / funded_amnt) * 100.0`[cite: 7, 11].
    * `fico_midpoint`: `(fico_range_low + fico_range_high) / 2.0`[cite: 7, 11].
    * `vintage_year`: `issue_d.dt.year`[cite: 7, 11].
    * Categorical bins: `dti_bracket` (`<=15%`, `15-25%`, `25-35%`, `>35%`) and `revol_util_bracket` (`<=40%`, `40-65%`, `65-85%`, `>85%`)[cite: 7, 11].
  * **N – Note & Document:** Generate `reports/etl_cleaning_log.md` logging record counts, memory reduction via Parquet compression, and dropped null rates[cite: 7, 11].

* [x] **Task 1.4: Unit Testing Cleaned Lineage (`tests/test_clean_schema.py`)**
  * Assert `fct_closed_loans_seasoned` contains zero `'Current'` loans[cite: 3, 7].
  * Verify `is_bad_loan` is non-null and strictly binary $\{0, 1\}$[cite: 3, 7].
  * Assert `laroc` calculations reconcile with raw payment ledger sums[cite: 3, 7].

---

## Phase 2: Executing the SCAN EDA Framework
[Framework: SCAN][cite: 3, 22, 26]

* [x] **Task 2.1: S & C – Stakeholder Alignment & Coverage Profiling (`src/analytics/scan_coverage.py`)**
  * Parameterize exploratory summaries to directly address the Chief Risk Officer's core mandate:
    * Total capital deployed ($19.39B), gross/net recoveries ($324.81M / $270.69M), net charge-offs ($2.73B), true terminal bad rate (19.96%).
    * Profile completeness and data types across all 162 features in `fct_closed_loans_seasoned.parquet`.
    * Validate 0% unexpected null rates across engineered columns (`is_bad_loan`, `net_cash_flow`, `laroc`, `fico_midpoint`, `dti_bracket`, `revol_util_bracket`, `vintage_year`).
    * Verify `invalid_dti_flag` tagging and isolation (376 records).
    * Export audit report to `reports/coverage_summary.md` and `data/exports/coverage_profiling.csv`.

* [x] **Task 2.2: A – Aggregates & Anomaly Auditing (`src/analytics/scan_aggregates.py`)**
  * Reconcile top-line portfolio cash flows: Total Funded ($19.39B), Repaid ($16.39B), Interest ($3.23B), Net Recoveries ($270.69M), Net Cash Flow ($825.13M), Platform LAROC (4.26%).
  * Generate parametric and non-parametric summary stats (Mean, Median, Std Dev, P25, P75, P90, P99, IQR) for `funded_amnt`, `int_rate`, `annual_inc`, `dti`, `revol_util`, `fico_midpoint`, and `laroc`.
  * Audit active portfolio exposure: 912,569 open loans across `Current` ($14.00B), `Late (31-120 days)` ($363.79M), `In Grace Period` ($149.09M), and `Late (16-30 days)` ($75.63M).
  * Save outputs to `reports/scan_aggregates_summary.md`, `data/exports/portfolio_aggregates.csv`, and `data/exports/active_portfolio_exposure.csv`.

* [x] **Task 2.3: N – Notable Segments Identification (`src/analytics/scan_segments.py`)**
  * Cross-tabulate terminal bad rate and median/mean LAROC across primary operational dimensions:
    1. **Loan Grade & Subgrade:** Grade A through G and subgrades A1 through G5; pinpoint subgrade C2 crossing 20.0% default rate and G4 dropping below +4.0% median LAROC (C4 for mean/cohort LAROC).
    2. **Loan Term:** 36-month vs. 60-month contracts (16.00% vs. 32.45% bad rate; 5.12% vs. 2.57% cohort LAROC).
    3. **Loan Purpose:** Highlight `small_business` as outsized risk (29.71% bad rate, -0.59% net cohort LAROC).
    4. **Multi-Variable Risk Grid:** 4x4 DTI x Revolving Utilization grid; high-risk intersection (`DTI > 25%` & `Revol_Util > 65%`) accounts for 112,246 loans (8.35% volume) with 28.41% default rate.
  * Save consolidated findings to `reports/notable_segments_summary.md` and CSVs in `data/exports/`.

---

## Phase 3: Statistical Hypothesis Validation & Econometric Risk Modeling
[Framework: Decision-Driven Design][cite: 3, 12]

* [x] **Task 3.1: Hypothesis 1 Validation — Pareto Loss Concentration (`src/analytics/test_h1_loss_concentration.py`)**
  * Test $H_1$: Subprime tiers (Grades D through G) absorb only 28.45% of portfolio capital ($5.52B) but generate 51.45% of cumulative net charge-off losses ($1.40B), representing a 1.81x Loss-to-Capital Ratio (p < 0.001)[cite: 3].
  * Compute cumulative distribution of funded principal vs. cumulative distribution of net charge-off dollars across Loan Grades (A $\rightarrow$ G) and Subgrades (A1 $\rightarrow$ G5)[cite: 3].
  * Calculate the Gini coefficient of loss concentration[cite: 3].
  * Run a Lorenz curve decomposition and execute a Chi-Square goodness-of-fit test against a uniform loss distribution (Chi-Square: 1,021,697,660.04, $p < 0.001$)[cite: 3].
  * Output summary tables and statistical test metrics to `reports/h1_validation_results.json` and `reports/h1_summary.md`[cite: 3].

* [x] **Task 3.2: Hypothesis 2 Validation — Subprime Margin Breakdown & LAROC (`src/analytics/test_h2_margin_breakdown.py`)**
  * Test $H_2$: High nominal interest rates in Grades D through G fail to compensate for charge-off frequency, resulting in net LAROC below institutional cost of capital (+4.0%)[cite: 3].
  * Compute cohort cash flow reconciliations by subgrade:
    $$\text{LAROC}_{\text{subgrade}} = \frac{\sum (\text{total\_pymnt} + \text{recoveries} - \text{collection\_recovery\_fee} - \text{funded\_amnt})}{\sum \text{funded\_amnt}} \times 100$$[cite: 3]
  * Pinpoint cost-of-capital hurdle (+4.0%) breach starting at Subgrade C4 (3.44%), and capital destruction (negative net LAROC) starting at Subgrade E5 (-1.34%) down to G5 (-9.81%)[cite: 3].
  * Perform two-sample Welch's t-tests comparing LAROC of prime originations (Grade C) versus subprime originations (Grades D, E, F+G) to confirm statistically significant net margin degradation ($p < 0.001$ across all tests)[cite: 3].
  * Output statistical test outputs to `reports/h2_validation_results.json` and `reports/h2_summary.md`[cite: 3].

* [x] **Task 3.3: Hypothesis 3 Validation — Multi-Variable Risk Interaction Grid (`src/analytics/test_h3_risk_interaction.py`)**
  * Test $H_3$: The combination of high DTI ($> 25\%$) and high credit utilization ($> 65\%$) causes terminal default rates to multiply non-linearly (28.41% default rate, 1.48x Relative Risk vs. baseline, 2.01x vs. prime conservative; Chi-Square = 5,464.86, $p < 0.001$)[cite: 3].
  * Build a 2D risk grid cross-tabulating `dti_bracket` by `revol_util_bracket` across closed loans (112,246 loans, $1.73B funded capital)[cite: 3].
  * Calculate Relative Risk (RR) ratios and Odds Ratios (1.67x) for the high-risk intersection relative to baseline borrowers[cite: 3].
  * **Policy Simulation Module (Action P0):** Model prospective portfolio impact of an automated hard-stop declining Grades D–G applicants with DTI > 25% and Revolving Utilization > 65%[cite: 3, 12]:
    * Eliminates 18,548 terminal defaults and saves $230.04M in net charge-offs ($254.10M gross losses avoided)[cite: 3, 12].
    * Retains 95.81% of funded capital ($18.58B) and 96.45% of loan volume (surpassing Guardrail 2: $\ge 80.0\%$)[cite: 3, 12].
    * Portfolio terminal default rate drops from 19.96% to 19.27% (-0.70 pp), and platform net LAROC expands from 4.26% to 4.40% (+14.9 bps)[cite: 3, 12].
  * Output policy figures to `reports/h3_validation_results.json` and `reports/h3_summary.md`[cite: 3].

---

## Phase 4: Executive Presentation Build & Asset Pipeline
[SOP: Frontend Slides HTML Presentation Workflow][cite: 4, 6]

* [x] **Task 4.1: Production Chart Export Pipeline (`src/presentation/export_figures.py`)**
  * Implement an automated matplotlib/seaborn script generating publication-grade static figures for executive consumption[cite: 4]:
    * Figure 1 (`assets/fig1_loss_contribution.png`): Paired bar chart contrasting Originated Capital Share (%) vs. Net Charge-Off Share (%) across loan grades[cite: 3, 4].
    * Figure 2 (`assets/fig2_risk_grid_heatmap.png`): 2D Risk Heatmap showing Terminal Bad Loan Rate across DTI Brackets (rows) vs. Revolving Utilization Brackets (columns) with text overlays of default rates[cite: 3, 4].
    * Figure 3 (`assets/fig3_capital_waterfall.png`): Financial Impact Waterfall chart displaying Baseline Losses -> Capital Recovered via Hard-Stops -> Post-Intervention Net Loss Exposure -> Preserved Origination Volume[cite: 3, 4].
  * Enforce visual design rules: Monochromatic slate palette (`#1E293B`, `#64748B`), single accent colors (`#DC2626` for default risk, `#059669` for capital saved), zero background gridlines, clean percentage/dollar labels, and bold story-driven newsflash headlines on every image[cite: 3, 4, 15, 23].

* [x] **Task 4.2: Frontend-Slides Specification & Prompt Assembly**
  * Assemble the slide-generation prompt in `docs/FRONTEND_SLIDES_PROMPT.md` following the standard operating procedure[cite: 4, 6]:
    * Purpose: Case Study / Portfolio Showcase[cite: 4, 6].
    * Density: Reading-first (optimized for asynchronous recruiter review without a speaker)[cite: 4, 6].
    * Style Direction: Cobalt Grid or Swiss Modern (clean financial risk aesthetic, slate/navy canvas with crisp metric callout badges)[cite: 4, 6].
    * Asset Integration: Map local absolute paths for Figures 1, 2, and 3[cite: 4, 6].

* [x] **Task 4.3: HTML Slide Deck Assembly (`index.html`)**
  * Execute the `frontend-slides` workflow in Antigravity / Claude Code to build `index.html`[cite: 4, 6]:
    * Slide 1: Executive Title, Context (1.35M seasoned loans, $19.39B funded principal), candidate metadata, and GitHub link[cite: 4, 6].
    * Slide 2: Executive Decision Mandate, CRO problem context, North Star LAROC, and 2 Guardrail Metrics[cite: 4, 6, 12].
    * Slide 3: Data Lineage & The CLEAN Framework Audit (censoring isolation diagram, data cleaning log)[cite: 4, 6, 7].
    * Slide 4: Primary Insight: Subprime Loss Contribution Skew (embed `assets/fig1_loss_contribution.png`)[cite: 4, 6].
    * Slide 5: Secondary Insight: Multi-Variable Risk Grid (embed `assets/fig2_risk_grid_heatmap.png`)[cite: 4, 6].
    * Slide 6: Policy Intervention & Capital Recovery Waterfall (embed `assets/fig3_capital_waterfall.png`)[cite: 4, 6].
    * Slide 7: Prioritized Underwriting Roadmap (P0 to P2 Decision Table with owners, expected dollar impact, and validation metrics)[cite: 4, 6, 12].
  * Validate responsive formatting, click-to-enlarge chart lightbox modals, keyboard navigation, and fast local loading (<500ms)[cite: 4, 6].

* [x] **Task 4.4: Technical Whitepaper Documentation (`README.md`)**
  * Author the executive-facing repository `README.md` using the 2-layer architecture[cite: 5, 12, 15]:
    * Section 1: Executive Summary & Spoken Delivery Pitch Script (30-second conversational summary)[cite: 12, 15].
    * Section 2: Decision Context & 4-Layer Metric Model (LAROC, Bad Loan Rate, Volume Capacity)[cite: 12, 15, 25].
    * Section 3: Data Architecture & CLEAN Data Quality Audit (Production Issues Log ISS-01 to ISS-05)[cite: 7, 11, 15].
    * Section 4: Statistical Evidence & Hypotheses Findings (embedding key charts with newsflash headlines)[cite: 12, 15].
    * Section 5: Prioritized Underwriting Policy Matrix (P0 to P2 Recommendations Table)[cite: 12, 15].
    * Section 6: Assumptions, Censoring Scope Boundaries, and Reproducibility Instructions[cite: 15].

* [x] **Task 4.5: Deployment & Verification Run**
  * Run pytest test suite: `./.venv/bin/pytest tests/`[cite: 3].
  * Deploy `index.html` and `assets/` to GitHub Pages for instant recruiter viewing[cite: 4, 6].
  * Run a final out-loud delivery test against the 45-second pitch script[cite: 3, 14].