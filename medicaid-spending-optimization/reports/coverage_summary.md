# Medicaid Outpatient Drug Utilization (CY2020–CY2024): Data Profiling & Coverage Summary Report

## 1. Executive Context & Scope
- **Data Domain**: CMS Medicaid Outpatient Drug Spending & Utilization Dashboard (DSD_MCD_RY26).
- **Longitudinal Span**: CY2020 through CY2024 (5 benefit years).
- **Composite Rollup (`OVERALL`)**: 4,774 unique drug entities (National Market Layer).
- **Manufacturer Detail Layer**: 13,737 distinct labeler lines (Competitor Detail Layer).
- **Methodological Partitioning**: Strict fork separating composite rolls from labeler records to eliminate budget double-counting.

---

## 2. HIPAA Privacy Redaction Audit (< 11 Claims)
Under federal statutory privacy guidelines, CMS suppresses utilization and spending figures for drug lines where total prescription fills are strictly fewer than 11 in historical benefit years (2020–2023).

| Benefit Year | Overall Total Drugs | Overall Suppressed (< 11 Fills) | Overall Suppressed (%) | Detail Total Rows | Detail Suppressed Rows | Detail Suppressed (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 2020 | 4,774 | 1,008 | 21.11% | 13,737 | 4,400 | 32.03% |
| 2021 | 4,774 | 775 | 16.23% | 13,737 | 3,468 | 25.25% |
| 2022 | 4,774 | 559 | 11.71% | 13,737 | 2,506 | 18.24% |
| 2023 | 4,774 | 315 | 6.60% | 13,737 | 1,326 | 9.65% |
| 2024 | 4,774 | 0 | 0.00% | 13,737 | 0 | 0.00% |

- **Unique Drugs with Historical Suppressions (`has_hipaa_suppression == True`)**: 1,065 of 4,774 entities (22.31%) in the national summary view.
- **Detail Records with Suppressions**: 4,593 of 13,737 rows (33.44%).
- **CY2024 Completeness Assertion**: Exactly **0.00%** suppressions in CY2024. CMS inclusion criteria mandate $\ge 11$ claims in the reporting benchmark year, guaranteeing 100% active utilization coverage for current-year formulary analytics.

### Statistical Handling Policy: Strict Prohibition of Zero-Imputation
> [!IMPORTANT]
> **Why Zero-Imputation is Forbidden**: Imputing suppressed cells ($< 11$ claims) with $0.00$ falsely fabricates zero utilization where 1 to 10 claims were actively reimbursed. Calculating growth from an artificial zero divisor produces infinite or mathematically corrupted Compound Annual Growth Rates (CAGR).
> 
> **Pipeline Resolution**: Suppressed values are strictly preserved as `NaN`/`None` with an audit tag (`has_hipaa_suppression = True`). Multi-year CAGR calculations exclude suppressed cells, substituting verified 1-year or 2-year annualized rate metrics.

---

## 3. Schema Completeness & Attribute Profiling
The cleaned analytical table `mcd_drug_overall_2020_2024.parquet` contains 43 production attributes.

| Attribute Name | Physical DataType | Non-Null Count | Null Count | Null Rate (%) | Description & Handling |
|:---|:---:|:---:|:---:|:---:|:---|
| `Brnd_Name` | `str` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `Gnrc_Name` | `str` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `Tot_Mftr` | `int64` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `Mftr_Name` | `str` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `Tot_Spndng_2020` | `float64` | 3,766 | 1,008 | 21.11% | CY2020 metric (suppressed/new drug launch if null) |
| `Tot_Dsg_Unts_2020` | `float64` | 3,766 | 1,008 | 21.11% | CY2020 metric (suppressed/new drug launch if null) |
| `Tot_Clms_2020` | `Int64` | 3,766 | 1,008 | 21.11% | CY2020 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Dsg_Unt_Wghtd_2020` | `float64` | 3,766 | 1,008 | 21.11% | CY2020 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Clm_2020` | `float64` | 3,766 | 1,008 | 21.11% | CY2020 metric (suppressed/new drug launch if null) |
| `Outlier_Flag_2020` | `Int64` | 3,766 | 1,008 | 21.11% | CY2020 metric (suppressed/new drug launch if null) |
| `Tot_Spndng_2021` | `float64` | 3,999 | 775 | 16.23% | CY2021 metric (suppressed/new drug launch if null) |
| `Tot_Dsg_Unts_2021` | `float64` | 3,999 | 775 | 16.23% | CY2021 metric (suppressed/new drug launch if null) |
| `Tot_Clms_2021` | `Int64` | 3,999 | 775 | 16.23% | CY2021 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Dsg_Unt_Wghtd_2021` | `float64` | 3,999 | 775 | 16.23% | CY2021 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Clm_2021` | `float64` | 3,999 | 775 | 16.23% | CY2021 metric (suppressed/new drug launch if null) |
| `Outlier_Flag_2021` | `Int64` | 3,999 | 775 | 16.23% | CY2021 metric (suppressed/new drug launch if null) |
| `Tot_Spndng_2022` | `float64` | 4,215 | 559 | 11.71% | CY2022 metric (suppressed/new drug launch if null) |
| `Tot_Dsg_Unts_2022` | `float64` | 4,215 | 559 | 11.71% | CY2022 metric (suppressed/new drug launch if null) |
| `Tot_Clms_2022` | `Int64` | 4,215 | 559 | 11.71% | CY2022 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Dsg_Unt_Wghtd_2022` | `float64` | 4,215 | 559 | 11.71% | CY2022 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Clm_2022` | `float64` | 4,215 | 559 | 11.71% | CY2022 metric (suppressed/new drug launch if null) |
| `Outlier_Flag_2022` | `Int64` | 4,215 | 559 | 11.71% | CY2022 metric (suppressed/new drug launch if null) |
| `Tot_Spndng_2023` | `float64` | 4,459 | 315 | 6.60% | CY2023 metric (suppressed/new drug launch if null) |
| `Tot_Dsg_Unts_2023` | `float64` | 4,459 | 315 | 6.60% | CY2023 metric (suppressed/new drug launch if null) |
| `Tot_Clms_2023` | `Int64` | 4,459 | 315 | 6.60% | CY2023 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Dsg_Unt_Wghtd_2023` | `float64` | 4,459 | 315 | 6.60% | CY2023 metric (suppressed/new drug launch if null) |
| `Avg_Spnd_Per_Clm_2023` | `float64` | 4,459 | 315 | 6.60% | CY2023 metric (suppressed/new drug launch if null) |
| `Outlier_Flag_2023` | `Int64` | 4,459 | 315 | 6.60% | CY2023 metric (suppressed/new drug launch if null) |
| `Tot_Spndng_2024` | `float64` | 4,774 | 0 | 0.00% | CY2024 benchmark metric (100% complete) |
| `Tot_Dsg_Unts_2024` | `float64` | 4,774 | 0 | 0.00% | CY2024 benchmark metric (100% complete) |
| `Tot_Clms_2024` | `Int64` | 4,774 | 0 | 0.00% | CY2024 benchmark metric (100% complete) |
| `Avg_Spnd_Per_Dsg_Unt_Wghtd_2024` | `float64` | 4,774 | 0 | 0.00% | CY2024 benchmark metric (100% complete) |
| `Avg_Spnd_Per_Clm_2024` | `float64` | 4,774 | 0 | 0.00% | CY2024 benchmark metric (100% complete) |
| `Outlier_Flag_2024` | `Int64` | 4,774 | 0 | 0.00% | CY2024 benchmark metric (100% complete) |
| `Chg_Avg_Spnd_Per_Dsg_Unt_23_24` | `float64` | 4,451 | 323 | 6.77% | Derived growth rate (null when baseline suppressed) |
| `CAGR_Avg_Spnd_Per_Dsg_Unt_20_24` | `float64` | 4,760 | 14 | 0.29% | Derived growth rate (null when baseline suppressed) |
| `has_hipaa_suppression` | `bool` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `Uses` | `str` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `therapeutic_class_macro` | `str` | 4,774 | 0 | 0.00% | Core dimension (100% complete) |
| `is_brand_flag` | `bool` | 4,774 | 0 | 0.00% | Engineered analytical flag (100% complete) |
| `spend_growth_abs_20_24` | `float64` | 3,766 | 1,008 | 21.11% | Derived 5-year growth metric (null when 2020 baseline suppressed) |
| `spend_growth_pct_20_24` | `float64` | 3,765 | 1,009 | 21.14% | Derived 5-year growth metric (null when 2020 baseline suppressed) |
| `price_vs_volume_driver` | `str` | 4,774 | 0 | 0.00% | Engineered analytical flag (100% complete) |

---

## 4. Clinical Text & Indication Parsing Coverage
- **Clinical Narrative Source**: CMS DBExport `Uses` fact table joined via composite business key `(Brnd_Name, Gnrc_Name)`.
- **Text Coverage**: 100% of rows enriched with clinical indication text.
- **Macro Classification**: Extracted 11 distinct clinical therapeutic indication classes via regex classification across clinical narratives, trade names, and generic chemical compounds.

## 5. Executive Sign-Off & Data Quality Verdict
- **Reconciliation Status**: PASS. CY2024 national gross spend reconciled across Overall ($111.28B) and Manufacturer Detail ($111.28B) within $0.00 variance.
- **Privacy Compliance**: PASS. All historical cells $< 11$ claims preserved without zero imputation.
- **Formulary Readiness**: Ready for Phase 3 Statistical Hypothesis Validation.