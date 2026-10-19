# ETL Data Quality & Cleaning Audit Log
**Pipeline:** LendingClub Consumer Credit Risk & Underwriting Optimization  
**Framework:** Christine Jiang CLEAN Data Quality Framework  
**Execution Timestamp:** 2026-10-19 18:58:18 UTC  

---

## 1. Executive Summary & Record Reconciliation

| Cohort Metric | Record Count | Share of Funded Originations (%) | Operational Purpose |
| :--- | :--- | :--- | :--- |
| **Total Ingested CSV Rows** | 2,260,701 | -- | Raw Kaggle ingestion extract |
| **Dropped Kaggle Footer Artifacts** | 33 | -- | Empty summary strings dropped at stage C |
| **Total Valid Funded Originations** | 2,260,668 | 100.00% | Verified 100% unique `id` loan grain |
| **Mature Closed Loans (`fct_closed_loans_seasoned`)** | 1,345,350 | 59.51% | **Single source of truth** for terminal defaults, LAROC, and risk grids |
| **Active Portfolio Loans (`fct_active_portfolio`)** | 912,569 | 40.37% | Open loan exposures (Current, Late, Grace Period) |
| **Excluded Policy-Noncompliant Loans** | 2,749 | 0.12% | Historical non-compliant credit policy records |

---

## 2. Censoring Bias Isolation: Terminal vs. Naive Risk Profile

Calculating loss rates across active/open loans introduces severe **right-censoring (survival) bias**, artificially masking default roll rates.

| Risk Dimension | Value | Methodological Rationale |
| :--- | :--- | :--- |
| **Mature Cohort Total Write-Offs (Charged Off + Default)** | 268,599 loans | Definitive terminal debt settlements |
| **True Terminal Default Rate (Seasoned Closed Cohort)** | **19.96%** | Evaluated strictly on `fct_closed_loans_seasoned` |
| **Naive Aggregate Default Rate (With Active Unseasoned Loans)** | **11.88%** | Diluted by 912,569 active originations |
| **Censoring Distortion Factor** | **1.68x** | Underwriting without seasoning underestimates credit risk by ~40% |

---

## 3. Storage & Memory Optimization

Transitioning from raw formatted CSV to partitioned Apache Parquet files yields substantial compute and memory savings:

| Storage Layer | Format | File Size (MB) | Size Reduction (%) |
| :--- | :--- | :--- | :--- |
| **Raw Source Ingestion** | CSV | 1597.53 MB | Baseline (1.0x) |
| **Seasoned Closed Table** | Parquet (Snappy) | 222.84 MB | 86.05% reduction |
| **Active Portfolio Table** | Parquet (Snappy) | 148.42 MB | 90.71% reduction |
| **Consolidated Analytical Parquet** | Parquet (Snappy) | 371.26 MB | **76.76% overall disk savings (4.3x)** |

---

## 4. Completeness & Quality Profile (Seasoned Closed Loans)

| Column | Total Records | Missing Records | Completeness (%) | Missingness (%) |
| :--- | :--- | :--- | :--- | :--- |
| dti | 1,345,350 | 374 | 99.972% | 0.028% |
| revol_util | 1,345,350 | 857 | 99.936% | 0.064% |
| annual_inc | 1,345,350 | 0 | 100.000% | 0.000% |
| emp_length | 1,345,350 | 78,516 | 94.164% | 5.836% |
| int_rate | 1,345,350 | 0 | 100.000% | 0.000% |
| term | 1,345,350 | 0 | 100.000% | 0.000% |
| grade | 1,345,350 | 0 | 100.000% | 0.000% |
| fico_range_low | 1,345,350 | 0 | 100.000% | 0.000% |

* **DTI Handling Policy:** Negative values (2 rows) and missing values (374 rows) isolated via `invalid_dti_flag = 1`. No synthetic cohort averaging was imputed.
* **Income Winsorization:** Extreme self-reported incomes winsorized at 99.5th percentile ($350,000.00), protecting variance calculations while preserving raw values in `annual_inc`.
* **Zero Income Audit:** Flagged 361 originations reporting $0 annual income with `zero_income_flag = 1`.

---

## 5. Production Issues Log (CLEAN Governance)

| Issue ID | Feature | Detected Anomaly | Resolution in Pipeline | Downstream Analytical Impact |
| :--- | :--- | :--- | :--- | :--- |
| **ISS-01** | `loan_status` | Active loans mixed with terminal loans | Segregated into seasoned vs. active Parquet views | Eliminates right-censoring bias; reveals true ~20.0% bad rate |
| **ISS-02** | `term`, `int_rate`, `revol_util` | Formatted strings with `%` and ` months` | Stripped units, converted to INT64 and decimal floats | Enables mathematical modeling, yield calculations, and tier binning |
| **ISS-03** | `dti` | Missing and negative ratio values | Created `invalid_dti_flag = 1`; capped visualization at 100% | Prevents leverage skewing without discarding loan originations |
| **ISS-04** | `emp_length` | Ordinal strings `< 1 year`, `10+ years` | Standardized to integer years [0..10], preserving NaNs | Supports ordinal tenure modeling without fabricating employment data |
| **ISS-05** | `id` | Kaggle CSV summary footer artifacts | Dropped empty records; enforced 100% primary key uniqueness | Prevents duplicate join keys and entity corruption |

---
*Pipeline completed in 49.37 seconds.*
