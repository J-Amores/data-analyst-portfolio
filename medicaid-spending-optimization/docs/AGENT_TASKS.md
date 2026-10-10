Autonomous Agent Task Plan: Google Antigravity Agent Execution Specification
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SEQUENTIAL AGENT WORKFLOW ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 1: Environment Setup, Virtualenv, Directory Scaffolding & Py Tests   │
│                                      │                                      │
│                                      ▼                                      │
│  PHASE 2: The SCAN Exploratory Data Analysis Pipeline (S -> C -> A -> N)   │
│                                      │                                      │
│                                      ▼                                      │
│  PHASE 3: Statistical Hypothesis Validation & Econometric Decomposition     │
│                                      │                                      │
│                                      ▼                                      │
│  PHASE 4: Interactive Executive Dashboard Build (The DASH Framework)       │
└─────────────────────────────────────────────────────────────────────────────┘
Phase 1: Environment Setup & Data Pipeline Foundation
- [x] Task 1.1: Environment Initialization & Directory Scaffolding
  - [x] Initialize Python virtual environment: python -m venv .venv && source .venv/bin/activate.
  - [x] Create production directory hierarchy: `data/{raw,cleaned,exports}`, `docs/`, `src/{etl,analytics,dashboard}`, `tests/`, `reports/figures`.
  - [x] Pin and install core scientific and reporting dependencies in `requirements.txt`: `pandas>=2.2.0`, `openpyxl>=3.1.2`, `scipy>=1.12.0`, `statsmodels>=0.14.1`, `plotly>=5.19.0`, `pytest>=8.0.0`, `pyarrow>=15.0.0`.
- [x] Task 1.2: Ingestion & Verification Harness
  - [x] Load `DSD_MCD_RY26_P06_V20_D24_BGM.xlsx` and `DSD_MCD_RY26_P04_V10_YTD24_DBExport - 20260603.xlsx`.
  - [x] Write validation script `tests/test_raw_schema.py` confirming expected column headers match the CMS Data Dictionary (all 34 core variables + trend metrics).
- [x] Task 1.3: CLEAN Pipeline Execution
  - [x] Implement `src/etl/clean_pipeline.py`.
  - [x] Enforce uppercase and trimmed strings for drug and manufacturer names.
  - [x] Isolate `Mftr_Name == 'Overall'` into `data/cleaned/mcd_drug_overall_2020_2024.parquet` (4,774 rows).
  - [x] Isolate `Mftr_Name != 'Overall'` into `data/cleaned/mcd_mftr_detail_2020_2024.parquet` (13,737 rows).
  - [x] Parse clinical text in `Uses` into `therapeutic_class_macro`.
Phase 2: Executing the SCAN EDA Framework
┌─────────────────────────────────────────────────────────────────────────────┐
│                            THE SCAN EDA FRAMEWORK                           │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ S - Stakeholder     │ Clarify PBM / Medicaid decision parameters            │
│ C - Columns         │ Verify completeness, suppressions, distributions      │
│ A - Aggregates      │ Top-line spend, claim volumes, IQR outlier audit      │
│ N - Notable Segments│ Slice by Brand vs Generic, Top Spenders, Therapeutic  │
└─────────────────────┴───────────────────────────────────────────────────────┘
- [x] Task 2.1: S – Stakeholder Goals Operationalization
  - [x] Implement `src/analytics/eda_scan.py` calculating national top-line Medicaid spend, 5-year budget shifts, and brand vs. generic cost concentration.
  - [x] Quantify the North Star Avoidable Brand-to-Generic Spend Wedge ($10.97B across 1,170 brand medications).
  - [x] Extract top 20 budget-draining drugs and top 20 expenditure growth drivers.
- [x] Task 2.2: C – Columns & Coverage Verification
  - [x] Generate comprehensive data profiling report `reports/coverage_summary.md` calculating null rates across all 43 attributes in national summary and detail views.
  - [x] Audit HIPAA suppression magnitude across historical years (2020–2023): isolate < 11 claims without zero-imputation; verify 0.00% suppressions in CY2024.
- [x] Task 2.3: A – Aggregates & Anomalies Auditing
  - [x] Calculate national aggregate gross spend across all benefit years ($76.4B in 2020 to $111.3B in 2024, +45.6% growth, 9.85% CAGR).
  - [x] Compute parametric and non-parametric summary statistics (Mean, Median, P75, P90, P99, Max, IQR) for `Avg_Spnd_Per_Dsg_Unt_Wghtd_2024` and `Avg_Spnd_Per_Clm_2024`.
  - [x] Quantify the fiscal impact of `Outlier_Flag_2024 == 1`: 1,738 flagged records (36.4%) driving $9.08B (8.16% of outlay) and 43.7M claims (5.86%).
- [x] Task 2.4: N – Notable Segments Identification
  - [x] Segment national spend by Brand vs. Generic (Brand: 90.2% spend / 33.0% claims; Generic: 9.8% spend / 67.0% claims; 18.7x cost-per-claim spread).
  - [x] Segment spend across top 10 clinical therapeutic indication classes parsed from `Uses` ($91.8B / 82.5% of outlay).
  - [x] Analyze competitor density and price dispersion across single-source vs. multi-source generic markets (7.32x median labeler price ratio).
  - [x] Export executive figures with newsflash headlines to `reports/figures/` in publication PNG and interactive Plotly HTML formats.
Phase 3: Statistical Hypothesis Validation & Econometric Decomposition
- [x] Task 3.1: Hypothesis 1 Validation (Pareto Budget Concentration)
  - [x] Script: `src/analytics/test_h1_pareto.py`.
  - [x] Compute cumulative distribution of spend across 4,774 unique drug entities ($111.3B gross outlay).
  - [x] Generate publication Lorenz curve visual in `reports/figures/h1_lorenz_curve.png` and interactive `h1_lorenz_curve.html`.
  - [x] Calculate the Gini coefficient (0.9028, KS $D = 0.7609, p < 10^{-99}$, Reject H0) and determine exact top drugs driving 50% (75 drugs / 1.57%), 65% (165 drugs / 3.46%), and 80% (361 drugs / 7.56%) of total program outlay.
- [x] Task 3.2: Hypothesis 2 Validation (Logarithmic Price-Volume Decomposition)
  - [x] Script: `src/analytics/test_h2_decomposition.py`.
  - [x] For all drugs with longitudinal data from 2020 to 2024 (3,762 drugs): $$\Delta \ln(\text{Spend}) = \ln\left(\frac{\text{Tot_Spndng_2024}}{\text{Tot_Spndng_2020}}\right), \quad \Delta \ln(P) = \ln\left(\frac{\text{Avg_Unit_Cost_2024}}{\text{Avg_Unit_Cost_2020}}\right), \quad \Delta \ln(Q) = \ln\left(\frac{\text{Tot_Dsg_Unts_2024}}{\text{Tot_Dsg_Unts_2020}}\right)$$
  - [x] Classify each drug's expenditure surge into: Price-Driven, Volume-Driven, or Dual Pressure (Catalog: 1,003 Volume / 482 Price / 409 Dual; Top 100: 68 Volume / 27 Dual / 5 Price).
  - [x] Run paired t-test ($t = -7.97, p = 2.79 \times 10^{-12}$) and Wilcoxon signed-rank test ($W = 252.0, p = 5.48 \times 10^{-15}$) across top 100 growth drugs (+$31.52B expansion); Claim volume growth (+124.2% mean) significantly outpaces unit cost growth (+19.2% mean) in 88 of 100 drugs (Fail to Reject H0, volume dominance proven).
  - [x] Export `reports/figures/h2_price_volume_decomposition.png` and interactive `h2_price_volume_decomposition.html`.
- [x] Task 3.3: Hypothesis 3 Validation (Multi-Source Brand-Generic Spread & MAC Modeling)
  - [x] Script: `src/analytics/test_h3_price_spread.py`.
  - [x] Isolate drugs where $\text{Tot\_Mftr} \ge 2$ (1,525 active multi-source drugs, 759 multi-source generics across 10,435 labeler detail lines).
  - [x] Calculate the coefficient of variation ($CV = 78.28\%$) and Interquartile Price Spread (50.23% median, 7.35x max/min ratio) across competing manufacturers (Wilcoxon $W = 211,957, p = 1.78 \times 10^{-29}$, Reject H0).
  - [x] Simulate potential Medicaid savings under State Maximum Allowable Cost (MAC) policy set at 25th percentile manufacturer price ($3.17B addressable generic savings / $5.21B total multi-source savings).
  - [x] Export `reports/figures/h3_mac_savings_spread.png` and interactive `h3_mac_savings_spread.html`.
  - [x] Compile comprehensive statistical synthesis report `reports/hypothesis_testing_summary.md`.
Phase 4: Interactive Dashboard Build (The DASH Framework Implementation)
┌─────────────────────────────────────────────────────────────────────────────┐
│                            THE DASH FRAMEWORK                               │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ D - Decision        │ Monthly PDL Tiering & State MAC Price Ceiling Updates │
│ A - Audience        │ State Medicaid Pharmacy Director & Formulary Board    │
│ S - Signal          │ 4 Executive KPIs (Spend, Wedge, Claims, Outlier Idx)  │
│ H - Hierarchy       │ Top: KPI Cards -> Mid: Quadrants -> Bottom: Action Grd│
└─────────────────────┴───────────────────────────────────────────────────────┘
- [x] Task 4.1: Decision & Audience Architecture (D & A)
  - [x] Primary Decision: Which brand medications should be shifted to non-preferred status, and which multi-source generics should have state MAC price ceilings updated for the upcoming benefit quarter?
  - [x] Audience: Non-technical executive leadership (State Medicaid Director, CMO, Legislative Budget Analysts). Built in `src/dashboard/app.py` delivering immediate high-level clarity, zero technical jargon, and interactive drill-down capabilities.
- [x] Task 4.2: Signal Isolation (S – The 4 Core Metrics)
  - [x] Card 1: 2024 Gross Medicaid Spend ($111.3B Total, formatted in $B with +45.6% 5-year growth badge).
  - [x] Card 2: Avoidable Brand-to-Generic Spend Wedge ($10,970.5M Addressable Savings across 1,170 brand medications, highlighted in Emerald #059669).
  - [x] Card 3: Total Prescription Claim Volume (745.6M claims with -4.6% year-over-year % change badge).
  - [x] Card 4: Outlier Distortion Risk Index (8.16% of outlay tied to CMS IQR Outlier Flag == 1; dynamic 0.00% when outlier filter is active).
- [x] Task 4.3: Visual Hierarchy & Interface Layout (H)
  - [x] Header Tier: Executive Title, Benefit Year Selector (2020–2024, default: 2024), Outlier Sensitivity Toggle (Exclude CMS Outlier Records), and Therapeutic Class multi-select filter.
  - [x] Top Tier (Signal Callouts): 4 Clean KPI summary cards formatted with bold values, units, and directional delta badges.
  - [x] Middle Tier (Macro Strategy & Drivers - 2 Columns):
    - [x] Left Column: Cumulative Spend Concentration (Pareto distribution of top 20 budget-draining drugs with cumulative outlay curve and full-market Lorenz curve tab).
    - [x] Right Column: Price vs. Volume Growth Quadrant Plot (X: 5-Year Claim Volume Growth %, Y: Unit Cost CAGR %, Bubble Size: Gross Spend).
  - [x] Bottom Tier (Actionable Formulary Grid): Interactive sortable data grid listing Brand Name, Generic Name, Therapeutic Class, Competing Manufacturers, Current Unit Cost, Lowest Generic Unit Cost, and Addressable Annual Savings ($), with search, minimum savings cutoff, and CSV download export.
- [x] Task 4.4: Executive Polish & Cognitive Ergonomics
  - [x] Strict palette: Professional slate/navy (#1E293B, #64748B) with single accent (#059669 emerald for savings).
  - [x] Zero chartjunk: eliminated background gridlines, clean currency ($B, $M) and percentage axis formatting, and story-driven newsflash headlines on every visual container.