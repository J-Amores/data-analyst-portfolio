# Data Specification: Bank Direct Marketing Pipeline

## 1. Overview & Architecture
This document specifies the physical data schemas, data lineage, data grain, and data quality transformations applied to the Banco de Portugal outbound marketing campaign datasets. The project adheres to Christine Jiang's Decision-Driven Design methodology and the Two-Layer Project Architecture.

Primary analytical datasets:
1. Primary Enriched Dataset: `data/raw/bank-additional-full.csv` (41,188 rows, 21 columns, May 2008 to November 2010).
2. Secondary Balance Benchmark: `data/raw/bank-full.csv` (45,211 rows, 17 columns, May 2008 to November 2010).

Target Cleaned Parquet Exports (`data/cleaned/`):
1. `fct_campaign_precall_targeting.parquet`: Pre-call targeting view strictly excluding call duration.
2. `fct_campaign_full_operational.parquet`: Operational view retaining call duration for post-hoc labor economics.
3. `fct_legacy_balance_benchmark.parquet`: Financial balance benchmark view from `bank-full.csv`.

---

## 2. Raw Schema Comparison

| Dimension | Primary Enriched (`bank-additional-full.csv`) | Secondary Benchmark (`bank-full.csv`) |
| :--- | :--- | :--- |
| File Path | `data/raw/bank-additional-full.csv` | `data/raw/bank-full.csv` |
| Row Count | 41,188 | 45,211 |
| Column Count | 21 | 17 |
| Delimiter | Semicolon (`;`) | Semicolon (`;`) |
| Unique Columns | `emp.var.rate`, `cons.price.idx`, `cons.conf.idx`, `euribor3m`, `nr.employed`, `day_of_week` | `balance`, `day` |
| Common Columns | `age`, `job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `duration`, `campaign`, `pdays`, `previous`, `poutcome`, `y` | Same 15 attributes |
| Target Distribution | `no`: 36,548 (88.73%), `yes`: 4,640 (11.27%) | `no`: 39,922 (88.30%), `yes`: 5,289 (11.70%) |
| Sentinel Code for Prior Contact | `pdays == 999` (39,673 rows, 96.32%) | `pdays == -1` (36,954 rows, 81.74%) |

---

## 3. Physical Schema Specification (`bank-additional-full.csv`)

| Column Name | Raw Type | Standardized Name | Clean Type | Description & Domain |
| :--- | :--- | :--- | :--- | :--- |
| `age` | int64 | `age` | int64 | Client age in years (range: 17 to 98) |
| `job` | object | `job` | string | Type of job (`admin`, `blue-collar`, `technician`, `services`, `management`, `retired`, `entrepreneur`, `self-employed`, `housemaid`, `unemployed`, `student`, `unknown`) |
| `marital` | object | `marital` | string | Marital status (`married`, `single`, `divorced`, `unknown`) |
| `education` | object | `education` | string | Level of education (`basic_4y`, `basic_6y`, `basic_9y`, `high_school`, `professional_course`, `university_degree`, `illiterate`, `unknown`) |
| `default` | object | `default` | string | Has credit in default? (`no`, `yes`, `unknown`) |
| `housing` | object | `housing` | string | Has housing loan? (`no`, `yes`, `unknown`) |
| `loan` | object | `loan` | string | Has personal loan? (`no`, `yes`, `unknown`) |
| `contact` | object | `contact` | string | Contact communication type (`cellular`, `telephone`) |
| `month` | object | `month` | string | Last contact month of year (`mar`, `apr`, `may`, `jun`, `jul`, `aug`, `sep`, `oct`, `nov`, `dec`) |
| `day_of_week` | object | `day_of_week` | string | Last contact day of the week (`mon`, `tue`, `wed`, `thu`, `fri`) |
| `duration` | int64 | `duration` | int64 | Last contact duration in seconds (post-call metric only; quarantined in precall view) |
| `campaign` | int64 | `campaign` | int64 | Number of contacts performed during this campaign for this client |
| `pdays` | int64 | `pdays` | int64 | Days since client was last contacted from a previous campaign (999 = not previously contacted) |
| `previous` | int64 | `previous` | int64 | Number of contacts performed before this campaign for this client |
| `poutcome` | object | `poutcome` | string | Outcome of previous marketing campaign (`nonexistent`, `failure`, `success`) |
| `emp.var.rate` | float64 | `emp_var_rate` | float64 | Employment variation rate quarterly indicator |
| `cons.price.idx` | float64 | `cons_price_idx` | float64 | Consumer price index monthly indicator |
| `cons.conf.idx` | float64 | `cons_conf_idx` | float64 | Consumer confidence index monthly indicator |
| `euribor3m` | float64 | `euribor3m` | float64 | Euribor 3 month rate daily indicator |
| `nr.employed` | float64 | `nr_employed` | float64 | Number of employees quarterly indicator |
| `y` | object | `is_subscribed` | int64 | Has the client subscribed to a term deposit? Binary target (`1` for `yes`, `0` for `no`) |

---

## 4. The CLEAN Data Engineering Pipeline Protocol

### Stage 1: C (Conceptualize Grain & Temporal Ordering)
* Data Grain: One record represents one outbound campaign evaluation episode per client prospect.
* Deterministic Primary Key: `campaign_record_id` sequentially numbered from `1` to `41188`.
* Temporal Sequence: Records are ordered chronologically from May 2008 through November 2010. By tracking month transitions across sequential rows, the pipeline reconstructs `campaign_year_month` (e.g., `2008-05` through `2010-11`) and `campaign_year`.

### Stage 2: L (Locate & Standardize Formatting Issues)
* Snake-Case Standardization: Rename dot-delimited column headers (`emp.var.rate` to `emp_var_rate`, `cons.price.idx` to `cons_price_idx`, `cons.conf.idx` to `cons_conf_idx`, `nr.employed` to `nr_employed`).
* Categorical Cleaning: Strip trailing periods, dots, and surrounding whitespace (`admin.` to `admin`, `basic.4y` to `basic_4y`, `university.degree` to `university_degree`).
* Binary Target Encoding: Cast `y` (`'yes'` / `'no'`) into integer binary target `is_subscribed` (`1` / `0`).

### Stage 3: E (Evaluate & Quarantine Structural Anomalies)
See Section 5 (Production Issues Log ISS-01 through ISS-05) for full specifications.

### Stage 4: A (Augment Analytical Features)
* `age_bucket`: Categorical demographic segment:
  * `'1. Young (<30)'` (age <= 30)
  * `'2. Core Working (31-45)'` (31 <= age <= 45)
  * `'3. Mature Working (46-60)'` (46 <= age <= 60)
  * `'4. Senior/Retired (60+)'` (age > 60)
* `job_collar_tier`: Operational collar categorization:
  * `'White-Collar'`: `admin`, `management`, `entrepreneur`, `self-employed`
  * `'Blue-Collar & Service'`: `blue-collar`, `services`, `housemaid`, `technician`
  * `'High-Yield Non-Working'`: `retired`, `student`, `unemployed`
  * `'Unknown'`: `unknown`
* `campaign_touch_tier`: Contact volume tier:
  * `'1 Touch'`, `'2 Touches'`, `'3 Touches'`, `'4-5 Touches'`, `'6+ Touches (Fatigue Zone)'`
* `is_over_contact_cap`: Binary flag indicating dialing beyond the 3-touch guardrail (`1` if `campaign > 3`, else `0`).
* `euribor_regime`: Macroeconomic regime classification:
  * `'Low Rate Regime (Euribor <= 3.0%)'` vs. `'High Rate Regime (Euribor > 3.0%)'`
* `duration_minutes`: Post-call labor duration (`duration / 60.0`, operational view only).

### Stage 5: N (Note & Document)
Comprehensive audit reports are written to `reports/etl_cleaning_log.md` detailing record reconciliation, contact fatigue volumes, sentinel value counts, and Parquet storage footprint.

---

## 5. Production Issues Log (ISS-01 through ISS-05)

### ISS-01: Post-Call Duration Data Leakage Quarantine
* Symptom: Call duration (`duration`) is only recorded after a telephone contact is concluded. A call duration of 0 seconds strictly guarantees non-subscription (`is_subscribed == 0`), while long calls strongly correlate with conversion. Using `duration` in predictive lead scoring or pre-dial prioritization produces unrealistic predictive power and severe post-call data leakage.
* Resolution: Create two separate Parquet analytical views:
  1. `data/cleaned/fct_campaign_precall_targeting.parquet`: Strictly excludes `duration` and `duration_minutes`. Enforces realistic pre-call propensity modeling.
  2. `data/cleaned/fct_campaign_full_operational.parquet`: Retains `duration` and `duration_minutes` for retrospective call center agent capacity and Cost-per-Acquisition (CPA) accounting.

### ISS-02: Sentinel Value `pdays == 999` / `-1` Resolution
* Symptom: In `bank-additional-full.csv`, `pdays == 999` represents clients who were never previously contacted (39,673 rows, 96.32% of records). In `bank-full.csv`, this is coded as `-1`. Treating 999 as a continuous numeric variable severely distorts linear models and tree splits.
* Resolution:
  1. Create binary flag `was_previously_contacted` (`1` if `pdays != 999`, `0` if `pdays == 999`).
  2. Create clean continuous variable `pdays_clean` containing true days since last contact for previously contacted leads, and `np.nan` for never-contacted leads.
  3. Create categorical feature `prior_contact_recency_tier`:
     * `'1. Recent (<=7 days)'` (pdays <= 7)
     * `'2. Warm (8-14 days)'` (8 <= pdays <= 14)
     * `'3. Cool (15+ days)'` (pdays > 14 and pdays != 999)
     * `'4. Never Contacted'` (pdays == 999)

### ISS-03: Explicit 'unknown' Category Governance
* Symptom: Missing information is coded as `'unknown'` strings across six categorical columns: `default` (8,597 rows, 20.87%), `education` (1,731 rows, 4.20%), `housing` (990 rows, 2.40%), `loan` (990 rows, 2.40%), `job` (330 rows, 0.80%), and `marital` (80 rows, 0.19%). A total of 10,700 records (25.98%) contain at least one unknown value. Dropping these rows or imputing with modes creates artificial bias.
* Resolution:
  1. Preserve explicit `'unknown'` category levels across all six categorical fields.
  2. Generate audit flag `has_unknown_attributes` (`1` if any of the six columns is `'unknown'`, else `0`).

### ISS-04: Exact Row Deduplication Audit
* Symptom: Identifying exact duplicates across all 21 raw columns reveals 12 redundant rows in `bank-additional-full.csv` (e.g., identical client age, job, marital, education, contact, duration, campaign, and macro attributes).
* Resolution:
  1. Flag exact duplicate records with binary indicator `is_exact_duplicate` (`1` for redundant duplicate rows, `0` for unique rows).
  2. Retain all 41,188 records in benchmark views while enabling clean filtering (`is_exact_duplicate == 0`) yielding 41,176 distinct evaluation episodes.

### ISS-05: Cross-Dataset Balance Enrichment Benchmark
* Symptom: The primary enriched dataset (`bank-additional-full.csv`) contains macroeconomic indicators but lacks client financial asset data (`balance`). Conversely, the legacy dataset (`bank-full.csv`) contains `balance` (median: 448.0 EUR) but lacks macroeconomic indicators and has a slightly different row grain (45,211 rows). Merging them row-by-row causes schema corruption.
* Resolution:
  1. Process `bank-full.csv` as an independent benchmark table `data/cleaned/fct_legacy_balance_benchmark.parquet`.
  2. Create `high_balance_flag` (`1` if `balance > 448.0`, else `0`).
  3. Use this table as a secondary benchmark for financial asset sensitivity analyses without corrupting the primary macroeconomic feature space.
