# ETL Pipeline Cleaning Audit Report

## 1. Executive Summary & Reconciliation
The CLEAN Data Engineering Pipeline successfully executed for both the primary enriched dataset (`bank-additional-full.csv`) and the secondary balance benchmark dataset (`bank-full.csv`). All data anomalies, post-call duration leakage risks, and sentinel values were quarantined or transformed into structured features.

### Primary Enriched Dataset Metrics (`bank-additional-full.csv`)
* Raw Record Grain: 1 row = 1 outbound campaign evaluation episode
* Total Client Records: 41,188 rows across 21 raw columns
* Chronological Time Range Reconstructed: 2008-05 through 2010-11
* Overall Campaign Conversion Rate: 11.2654% (4,640 subscriptions)
* Total Outbound Call Touches Dialed: 105,754 calls
* Outbound Call Efficiency: 4.3875% subscriptions per dialed call
* Exact Duplicate Rows Flagged: 12 records (`is_exact_duplicate == 1`)

### Secondary Balance Benchmark Metrics (`bank-full.csv`)
* Total Client Records: 45,211 rows across 17 raw columns
* Overall Subscription Rate: 11.6985% (5,289 subscriptions)
* Benchmark Median Account Balance: 448.0 EUR
* High Balance Prospects (`balance > 448.0`): 22,603 records

---

## 2. Contact Fatigue Breakdown (The 3-Touch Boundary)

| Segment | Prospect Count | Dialed Calls | Subscriptions | Conversion Rate | Dialed Calls Share | Subscription Share |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Baseline (Touches 1-3) | 33,553 (81.46%) | 54,805 | 4,085 | 12.17% | 51.82% | 88.04% |
| Fatigue Zone (Touches 4+) | 7,635 (18.54%) | 50,949 | 555 | 7.27% | 48.18% | 11.96% |
| Total Outbound Campaign | 41,188 (100.0%) | 105,754 | 4,640 | 11.27% | 100.0% | 100.0% |

### Strategic Implications of Contact Fatigue
1. Labor Consumption: Dialing prospects more than 3 times consumed 50,949 outbound phone calls (48.18% of total call center bandwidth).
2. Diminishing Commercial Yield: Despite absorbing nearly half of total dialer touches, touches 4+ generated only 555 subscriptions (11.96% of total volume) at a meager 7.27% conversion rate.
3. Pipeline Preservation: Enforcing an automated hard-stop at 3 touches preserves 88.04% of all term deposit acquisitions while liberating 48.18% of agent calling capacity.

---

## 3. Structural Anomalies & Sentinel Audit (ISS-01 to ISS-05)

### ISS-01: Post-Call Duration Data Leakage Quarantine
* Risk: Call duration is known strictly post-call. Pre-call targeting with duration produces severe leakage.
* Resolution: Generated two dedicated Parquet views:
  * `data/cleaned/fct_campaign_precall_targeting.parquet`: 33 columns, zero duration leakage.
  * `data/cleaned/fct_campaign_full_operational.parquet`: 35 columns, retains `duration` and `duration_minutes`.

### ISS-02: Sentinel Value `pdays == 999` Resolution
* Raw Sentinel Count: 39,673 records (96.32%) had `pdays == 999` (never previously contacted).
* Previously Contacted Count: 1,515 records (3.68%).
* Engineered Features:
  * `was_previously_contacted`: Binary indicator (0 for `pdays == 999`, 1 otherwise).
  * `pdays_clean`: Continuous days since last contact (NaN for `pdays == 999`).
  * `prior_contact_recency_tier`: Categorical tiering (Recent <=7d, Warm 8-14d, Cool 15+d, Never Contacted).

### ISS-03: Explicit 'unknown' Category Governance
Missing values were retained as explicit category levels to avoid naive imputation distortions:
* Credit Default (`default == 'unknown'`): 8,597 rows
* Education Level (`education == 'unknown'`): 1,731 rows
* Housing Loan (`housing == 'unknown'`): 990 rows
* Personal Loan (`loan == 'unknown'`): 990 rows
* Job Category (`job == 'unknown'`): 330 rows
* Marital Status (`marital == 'unknown'`): 80 rows
* Composite Quality Flag: 10,700 records (25.98%) have at least one unknown attribute (`has_unknown_attributes == 1`).

### ISS-04: Exact Row Deduplication Audit
* Exact Duplicates Detected: 12 records.
* Governance: Flagged via `is_exact_duplicate`. Benchmark retains all 41,188 rows while enabling deduplicated filtering to 41,176 records.

### ISS-05: Cross-Dataset Balance Enrichment Benchmark
* Created independent table `data/cleaned/fct_legacy_balance_benchmark.parquet` with 45,211 rows.
* Preserved balance distribution without corrupting the primary macroeconomic feature space.

---

## 4. Parquet Storage Footprint & Compression

| Artifact Path | Record Count | Column Count | File Size (KB) | Compression |
| :--- | :--- | :--- | :--- | :--- |
| `fct_campaign_precall_targeting.parquet` | 41,188 | 33 | 472.3 KB | Snappy |
| `fct_campaign_full_operational.parquet` | 41,188 | 35 | 596.8 KB | Snappy |
| `fct_legacy_balance_benchmark.parquet` | 45,211 | 19 | 361.8 KB | Snappy |

---

## 5. Pipeline Verification Status
* Pre-flight raw schema tests: Passed (5 of 5)
* CLEAN pipeline execution: Complete (0 errors)
* Post-clean lineage and integrity tests: Ready for assertion
