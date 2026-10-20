# SCAN Coverage & Stakeholder Alignment Audit
**Project:** LendingClub Consumer Credit Risk & Underwriting Optimization  
**Framework:** Christine Jiang SCAN EDA Framework (Stage S & Stage C)  
**Execution Timestamp:** 2026-10-19 | Runtime: 0.39 seconds  
**Dataset Grain:** 1 row = 1 funded closed loan origination (`fct_closed_loans_seasoned.parquet`)  
**Analyzed Volume:** 1,345,350 loans  

---

## 1. Stage S – Stakeholder Alignment (CRO Executive Mandate)

All exploratory dimensions are calibrated to the Chief Risk Officer's underwriting mandate:
preserving capital, measuring terminal loss leakage, and assessing return on capital.

| Executive Dimension | Value | Operational Definition / Risk Impact |
| :--- | :--- | :--- |
| **Total Capital Deployed (Funded Principal)** | **$19,388,585,275.00** | Total investor balance deployed across mature closed loans |
| **Total Cash Recoveries Collected (Gross)** | **$324,810,542.55** | Gross collections recovered post-charge-off |
| **Third-Party Recovery Fees** | **$54,121,686.29** | Collection agency servicing charges deducted from recoveries |
| **Net Cash Recoveries** | **$270,688,856.26** | Net cash retained post-default debt collection |
| **Gross Principal Charge-Offs** | **$2,999,967,360.24** | Funded principal uncollected at default ($3.00B) |
| **Cumulative Net Charge-Off Principal** | **$2,729,278,503.98** | Gross principal lost less net post-charge-off recoveries |
| **Terminal Bad Loan Volume** | **268,599** loans | Charged Off (268,568) + Default (31) |
| **Terminal Fully Paid Volume** | **1,076,751** loans | Successful full principal and interest amortizations |
| **True Terminal Bad Loan Rate** | **19.96%** | Evaluated strictly on seasoned cohort (vs. 11.88% unseasoned) |
| **Platform Aggregate Net Cash Flow** | **$825,129,158.30** | Total cash profit retained above funded capital |
| **Platform Aggregate LAROC** | **4.26%** | Portfolio-level Loss-Adjusted Return on Originated Capital |

---

## 2. Stage C – Feature Completeness & Column Profiling Overview

The mature cohort encompasses **162 columns**. Completeness distribution:
- **100% Complete Features:** 54 columns (33.3%)
- **High Completeness (≥ 95%):** 78 columns (48.1%)
- **Sparse / Subprime Features (< 50%):** 58 columns (35.8%) (e.g., secondary applicant and hardship attributes)

### Core Underwriting & Engineered Features Quality Profile

| Feature | Data Type | Non-Null Count | Null Count | Completeness (%) | Data Governance Treatment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `loan_amnt` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `funded_amnt` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `term` | `int64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `int_rate` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `installment` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `grade` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `sub_grade` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `emp_length` | `float64` | 1,266,834 | 78,516 | 94.164% | Governed Underwriting Feature |
| `home_ownership` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `annual_inc` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `verification_status` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `issue_d` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `loan_status` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `purpose` | `str` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `dti` | `float64` | 1,344,976 | 374 | 99.972% | Governed Underwriting Feature |
| `fico_range_low` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `fico_range_high` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `revol_util` | `float64` | 1,344,493 | 857 | 99.936% | Governed Underwriting Feature |
| `total_pymnt` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `total_rec_prncp` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `total_rec_int` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `recoveries` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `collection_recovery_fee` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `vintage_year` | `int64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `invalid_dti_flag` | `int64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `net_cash_flow` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `laroc` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `fico_midpoint` | `float64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |
| `dti_bracket` | `str` | 1,344,974 | 376 | 99.972% | Governed Underwriting Feature |
| `revol_util_bracket` | `str` | 1,344,493 | 857 | 99.936% | Governed Underwriting Feature |
| `is_bad_loan` | `int64` | 1,345,350 | 0 | 100.000% | Governed Underwriting Feature |

---

## 3. Stage C – Engineered Feature Verification (0% Unexpected Nulls)

All engineered analytical variables undergo rigorous data contract assertions.

| Engineered Feature | Actual Nulls | Expected Nulls | Unexpected Nulls | Unexpected Null Rate (%) | Status | Governance Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `is_bad_loan` | 0 | 0 | 0 | 0.00% | **PASS (0% Unexpected)** | Mandatory binary outcome indicator |
| `net_cash_flow` | 0 | 0 | 0 | 0.00% | **PASS (0% Unexpected)** | Mandatory ledger cash flow computation |
| `laroc` | 0 | 0 | 0 | 0.00% | **PASS (0% Unexpected)** | Mandatory return on capital metric |
| `fico_midpoint` | 0 | 0 | 0 | 0.00% | **PASS (0% Unexpected)** | Midpoint of non-null FICO high/low bounds |
| `vintage_year` | 0 | 0 | 0 | 0.00% | **PASS (0% Unexpected)** | Extracted year from non-null issue_d |
| `dti_bracket` | 376 | 376 | 0 | 0.00% | **PASS (0% Unexpected)** | Explicitly isolated invalid DTIs (invalid_dti_flag=1: 376 rows) |
| `revol_util_bracket` | 857 | 857 | 0 | 0.00% | **PASS (0% Unexpected)** | Missing raw revol_util in source (857 rows) |

---

## 4. Stage C – DTI Anomaly Flagging & Isolation Audit

| DTI Quality Metric | Record Count | Share of Book (%) | Downstream Handling Policy |
| :--- | :--- | :--- | :--- |
| **Total Seasoned Originations** | 1,345,350 | 100.00% | Verified seasoned closed loan grain |
| **Valid DTI Originations** | 1,344,974 | 99.9721% | Used for DTI brackets and risk grid cross-tabulations |
| **Missing DTI Records** | 374 | 0.0278% | Isolated via `invalid_dti_flag = 1` |
| **Negative DTI Records (< 0)** | 2 | 0.0001% | Isolated via `invalid_dti_flag = 1` |
| **Total Flagged Invalid DTI Records** | **376** | **0.0279%** | **100% Isolated; Zero Imputation Performed** |
| **Isolated in `dti_bracket` (Null Count)** | 376 | 100.00% of flagged | Successfully filtered from segmentation views |
| **Isolated in `dti_visual_capped` (Null Count)** | 376 | 100.00% of flagged | Successfully filtered from continuous distribution views |

> [!IMPORTANT]
> **DTI Governance Verdict:** PASSED: All invalid DTI records are strictly isolated without synthetic distortion.

---
*Report automatically generated by `src/analytics/scan_coverage.py` in 0.39 seconds.*
