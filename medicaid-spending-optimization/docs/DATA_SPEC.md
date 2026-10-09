Data Specification & Quality Engineering: CMS Medicaid Drug Utilization Files
1. Data Grain & Architecture Overview
The analysis utilizes two core CMS data sources, supported by federal methodology and dictionary documentation:
Table A: mcd_spending_bgm (DSD_MCD_RY26_P06_V20_D24_BGM.xlsx)
Grain: Brnd_Name $\times$ Gnrc_Name $\times$ Mftr_Name across 5 longitudinal benefit years (CY2020–CY2024).
Hierarchy: Contains both individual manufacturer records AND summary rows where Mftr_Name == 'Overall' (representing the claim-weighted rollup across all manufacturers for that specific brand/generic combination).
Table B: mcd_spending_dbexport (DSD_MCD_RY26_P04_V10_YTD24_DBExport - 20260603.xlsx)
Grain: Brand Name Desc $\times$ Generic Name $\times$ Manufacturer Desc $\times$ Year (Normalized Long Format).
Enrichment: Contains consumer-friendly clinical indications and therapeutic descriptions (Uses).
Entity Relationship: Joined on composite business key (Brnd_Name == Brand Name Desc, Gnrc_Name == Generic Name, Mftr_Name == Manufacturer Desc, Year).
┌────────────────────────────────────────────────────────┐
│             Table A: mcd_spending_bgm                  │
│             (Wide Longitudinal Matrix)                 │
├────────────────────────────────────────────────────────┤
│ PK: [Brnd_Name, Gnrc_Name, Mftr_Name]                  │
│ Tot_Spndng_2020 ... Tot_Spndng_2024                    │
│ Tot_Clms_2020   ... Tot_Clms_2024                      │
│ Avg_Spnd_Per_Dsg_Unt_Wghtd_2020 ... 2024               │
│ Outlier_Flag_2020 ... Outlier_Flag_2024                │
│ CAGR_Avg_Spnd_Per_Dsg_Unt_20_24                        │
└───────────────────────────┬────────────────────────────┘
                            │
                            │ 1:Many (by Year)
                            ▼
┌────────────────────────────────────────────────────────┐
│          Table B: mcd_spending_dbexport                │
│             (Long Clinical Fact Table)                 │
├────────────────────────────────────────────────────────┤
│ PK: [Brand Name Desc, Generic Name, Mftr Desc, Year]   │
│ Total Payments, Total Claim Count, Total Service Units │
│ Cost Per Unit, Cost Per Unit All Mfg                   │
│ Uses (Clinical Indication Text / Therapeutic Class)    │
└────────────────────────────────────────────────────────┘
2. Column Definitions & Physical Schema
Core Entity Identifiers & Dimensions
Brnd_Name (VARCHAR(150), Non-Null): Commercial trade name of the drug filled, or chemical name if unbranded generic.
Gnrc_Name (VARCHAR(200), Non-Null): Active chemical ingredient name.
Tot_Mftr (INTEGER, Min: 1): Number of distinct labelers/manufacturers competing in the Medicaid marketplace for this drug entity.
Mftr_Name (VARCHAR(150), Non-Null): Labeler name, or 'Overall' indicating the cross-manufacturer weighted composite.
Uses (TEXT, Nullable): Clinical narrative detailing FDA-approved indications, mechanism of action, and patient administration instructions.
Metric Measures (Annual Repetition for $YYYY \in [2020, 2021, 2022, 2023, 2024]$)
Tot_Spndng_YYYY (DECIMAL(15,2), $\ge 0.00$): Aggregate gross pharmacy reimbursement paid by State Medicaid agencies and federal share, inclusive of pharmacy dispensing fees, BEFORE manufacturer rebates.
Tot_Dsg_Unts_YYYY (DECIMAL(15,3), $\ge 0.000$): Sum of physical dispensable dosage units (e.g., number of tablets, capsules, milliliters of liquid, grams of ointment).
Tot_Clms_YYYY (INTEGER, $\ge 0$): Total prescription fills (original scripts plus authorized refills). Must be $\ge 11$ in CY2024; values $< 11$ in historical years are suppressed by CMS.
Avg_Spnd_Per_Dsg_Unt_Wghtd_YYYY (DECIMAL(12,4), $\ge 0.0000$): Claim-weighted average reimbursement per single dosage unit. Weighted across unique National Drug Codes (NDCs), strengths, dosage forms, and routes of administration.
Avg_Spnd_Per_Clm_YYYY (DECIMAL(12,2), $\ge 0.00$): Average reimbursement per prescription claim (Tot_Spndng_YYYY / Tot_Clms_YYYY).
Outlier_Flag_YYYY (INTEGER, Allowed: ${0, 1}$): Binary CMS audit flag. Set to 1 if SDUD records violate interquartile bounds ($[Q_1 - 1.5 \times \text{IQR}, Q_3 + 1.5 \times \text{IQR}]$) or have $< 30$ records, shifting weighted unit cost by $> 10%$ and $> $1.00$.
Chg_Avg_Spnd_Per_Dsg_Unt_23_24 (DECIMAL(8,4)): 1-year percentage change in weighted spending per dosage unit from 2023 to 2024.
CAGR_Avg_Spnd_Per_Dsg_Unt_20_24 (DECIMAL(8,4)): 5-year Compound Annual Growth Rate in weighted spending per dosage unit: $$\text{CAGR} = \left(\frac{\text{Avg_Spnd_Per_Dsg_Unt_Wghtd_2024}}{\text{Avg_Spnd_Per_Dsg_Unt_Wghtd_2020}}\right)^{1/4} - 1$$
3. Data Cleaning Pipeline: The CLEAN Framework Implementation
┌─────────────────────────────────────────────────────────────────────────────┐
│                            THE CLEAN FRAMEWORK                              │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ C - Conceptualize   │ Establish grain, measures, dimensions, critical cols  │
│ L - Locate Solvable │ Whitespace, casing, types, double-count isolation     │
│ E - Evaluate Hard   │ Suppression (<11 claims), outlier sensitivity, rebates│
│ A - Augment Data    │ Brand/generic flags, spend decomposition, indications │
│ N - Note & Document │ Audit logs, magnitude benchmarks, executive caveats   │
└─────────────────────┴───────────────────────────────────────────────────────┘
C – Conceptualize the Data
Grain Integrity: Verify that every unique drug entity is tracked at two distinct analysis layers: the composite market layer (Mftr_Name == 'Overall') and the competitor labeler layer (Mftr_Name != 'Overall').
Critical vs. Non-Critical Columns:
Critical Columns ($> 95%$ completeness required): Brnd_Name, Gnrc_Name, Mftr_Name, Tot_Spndng_2024, Tot_Clms_2024, Avg_Spnd_Per_Dsg_Unt_Wghtd_2024.
Non-Critical / Contextual: Historical years for newly launched post-2020 drugs, free-text narrative instructions in Uses.
L – Locate Solvable Issues
The Double-Counting Elimination Rule:
Problem: Both individual manufacturer rows and summary 'Overall' rows exist in the same column (Mftr_Name). Summing Tot_Spndng_2024 naively across the file doubles the true program spend!
Resolution: Fork the dataset in the data pipeline into two dedicated views:
fct_medicaid_drug_summary: Filtered strictly where Mftr_Name == 'Overall'.
fct_medicaid_manufacturer_detail: Filtered strictly where Mftr_Name != 'Overall'.
Text Sanitation & Entity Normalization:
Strip leading/trailing whitespaces across Brnd_Name, Gnrc_Name, and Mftr_Name (TRIM(UPPER(col))).
Standardize joint compound delimiters (e.g., replacing slash / with comma ,  in fixed-dose combination generic names).
Type Coercion & Financial Casting:
Convert currency strings, thousands separators, and non-numeric representations to standard FLOAT64 / DECIMAL(15,2).
Ensure binary outlier flags are explicitly stored as INT64 with allowed set ${0, 1}$.
E – Evaluate Unsolvable Issues
CMS Privacy Redactions ($< 11$ Claims):
Phenomenon: In compliance with federal HIPAA privacy regulations, CMS suppresses claim volume and spending in years prior to 2024 where total claims were $< 11$.
Handling Policy: Do NOT impute with zeros or cohort means! Imputing zero artificially spikes CAGR, while mean imputation fabricates claims data. Store as NULL / NaN with an explicit audit metadata tag data_suppressed_hipaa = True. Exclude suppressed multi-year spans from 5-year CAGR calculations, substituting 1-year or 2-year annualized growth where valid.
Gross Spend vs. Statutory Medicaid Rebates:
Phenomenon: CMS totals represent payments to dispensing pharmacies and do not subtract manufacturer statutory Medicaid rebates (which average 30% to 55%+ across brand drugs).
Handling Policy: Document as an institutional scope boundary in the executive metadata. Label all dollar metrics as Gross Program Spend (Pre-Rebate) to prevent misrepresentation during legislative hearings.
Statistical Outlier Flags (Outlier_Flag == 1):
Phenomenon: ~1% to 3% of records have erratic dosage unit costs caused by unit mismatch reporting (e.g., billing 1 package of inhaler as 200 actuations or vice versa).
Handling Policy: Retain all records in the baseline database to preserve spend reconciliation, but add an executive toggle in all downstream views: Exclude Outliers (CMS Flagged).
A – Augment the Data
is_brand_flag (BOOLEAN): Calculated via string matching and taxonomy rules: $$\text{is_brand_flag} = \begin{cases} \text{FALSE} & \text{if } \text{LOWER}(\text{Brnd_Name}) == \text{LOWER}(\text{Gnrc_Name}) \ \text{TRUE} & \text{otherwise} \end{cases}$$
spend_growth_abs_20_24 (DECIMAL(15,2)): Net absolute dollar change from 2020 to 2024: $$\text{Tot_Spndng_2024} - \text{Tot_Spndng_2020}$$
price_vs_volume_driver (VARCHAR(30)): Categorical classification based on log-decomposition:
'Price-Driven' if $\Delta \ln(\text{Unit Cost}) > \Delta \ln(\text{Claims})$
'Volume-Driven' if $\Delta \ln(\text{Claims}) \ge \Delta \ln(\text{Unit Cost})$
therapeutic_class_macro (VARCHAR(100)): Extracted from Uses text via rule-based regex parsing (e.g., GLP-1 / Antidiabetic, Cardiovascular / Antihypertensive, Central Nervous System / Psychotropic, Respiratory / Asthma, Oncology / Immunomodulator).
N – Note and Document (The Production Issues Log)
Issue ID
Column / Feature
Detected Anomaly
Severity / Magnitude
Final Resolution Strategy
Impact on Downstream Analysis
ISS-01
Mftr_Name
Summary rows (Overall) interleaved with raw labeler rows.
100% of drug entities (doubles total spend if unfiltered).
Splitting into two distinct views: fct_drug_summary vs. fct_mftr_detail.
Prevents fatal budget double-counting error.
ISS-02
Tot_Clms_2020 ... 2023
Suppressed claims for small cells ($< 11$ fills).
~4.2% of longitudinal records.
Preserved as NULL; filtered from 5-year CAGR; calculated 1-year change where valid.
Eliminates artificial CAGR spikes.
ISS-03
Outlier_Flag_YYYY
CMS flags anomalous dosage pricing (IQR $\pm 1.5$).
~2.1% of drug lines.
Preserved in raw view; built dynamic executive filter Exclude Outliers.
Allows sensitivity analysis without data loss.
ISS-04
Uses
Free-text unstructured clinical summary.
~100% text coverage in DBExport.
Extracted top 8 macro therapeutic classes via regex keyword classification.
Enables executive clinical domain slicing.