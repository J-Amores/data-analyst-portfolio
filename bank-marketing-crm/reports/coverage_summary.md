# Stage S & C Audit Report: Stakeholder Alignment & Coverage Profiling

## 1. Stakeholder Mandate Parameterization (Stage S)
The exploratory data pipeline aligns baseline commercial and operational targets with the VP of Growth Marketing and Head of Outbound Call Center Operations.

| Metric Dimension | Benchmark Target | Reconciled Full (N=41,188) | Deduplicated (N=41,176) | Status |
| :--- | :--- | :--- | :--- | :--- |
| Total Prospects Evaluated | 41,188 | 41,188 | 41,176 | PASS |
| Total Outbound Calls Dialed | 105,754 | 105,754 | 105,735 | PASS |
| Total Subscriptions Won | 4,640 | 4,640 | 4,639 | PASS |
| Lead Conversion Rate | 11.27% | 11.27% | 11.27% | PASS |
| Dialing Efficiency (Per 100 Calls) | 4.39% | 4.39% | 4.39% | PASS |

### Deduplication Sensitivity Audit
- Exact Duplicates Identified: 12 rows (0.029% of benchmark portfolio).
- Outbound Calls in Duplicates: 19 calls.
- Subscriptions Won in Duplicates: 1 subscription.
- Sensitivity Impact: Full conversion rate is 11.2654% vs. deduplicated 11.2663% (absolute delta: 0.0009%).
- Conclusion: The 12 exact duplicates have zero material impact on strategic acquisition OKRs.

---

## 2. Pre-Call Column Profiling & Completeness (Stage C)
Exhaustive profile of all 34 attributes in `fct_campaign_precall_targeting.parquet` across 41,188 client records.

| Column Name | Role | Data Type | Non-Null Count | Null Count | Null Pct (%) | Distinct Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `campaign_record_id` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 41,188 |
| `campaign_year_month` | Engineered Feature | `str` | 41,188 | 0 | 0.00% | 26 |
| `campaign_year` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 3 |
| `age` | Client Demographic | `int64` | 41,188 | 0 | 0.00% | 78 |
| `age_bucket` | Engineered Feature | `str` | 41,188 | 0 | 0.00% | 4 |
| `job` | Client Demographic | `str` | 41,188 | 0 | 0.00% | 12 |
| `job_collar_tier` | Engineered Feature | `str` | 41,188 | 0 | 0.00% | 4 |
| `marital` | Client Demographic | `str` | 41,188 | 0 | 0.00% | 4 |
| `education` | Client Demographic | `str` | 41,188 | 0 | 0.00% | 8 |
| `default` | Client Demographic | `str` | 41,188 | 0 | 0.00% | 3 |
| `housing` | Client Demographic | `str` | 41,188 | 0 | 0.00% | 3 |
| `loan` | Client Demographic | `str` | 41,188 | 0 | 0.00% | 3 |
| `has_unknown_attributes` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 2 |
| `contact` | Campaign History | `str` | 41,188 | 0 | 0.00% | 2 |
| `month` | Campaign History | `str` | 41,188 | 0 | 0.00% | 10 |
| `day_of_week` | Campaign History | `str` | 41,188 | 0 | 0.00% | 5 |
| `campaign` | Campaign History | `int64` | 41,188 | 0 | 0.00% | 42 |
| `campaign_touch_tier` | Engineered Feature | `str` | 41,188 | 0 | 0.00% | 5 |
| `is_over_contact_cap` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 2 |
| `pdays` | Campaign History | `int64` | 41,188 | 0 | 0.00% | 27 |
| `pdays_clean` | Campaign History | `float64` | 1,515 | 39,673 | 96.32% | 27 |
| `was_previously_contacted` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 2 |
| `prior_contact_recency_tier` | Engineered Feature | `str` | 41,188 | 0 | 0.00% | 4 |
| `previous` | Campaign History | `int64` | 41,188 | 0 | 0.00% | 8 |
| `poutcome` | Campaign History | `str` | 41,188 | 0 | 0.00% | 3 |
| `emp_var_rate` | Macroeconomic Indicator | `float64` | 41,188 | 0 | 0.00% | 10 |
| `cons_price_idx` | Macroeconomic Indicator | `float64` | 41,188 | 0 | 0.00% | 26 |
| `cons_conf_idx` | Macroeconomic Indicator | `float64` | 41,188 | 0 | 0.00% | 26 |
| `euribor3m` | Macroeconomic Indicator | `float64` | 41,188 | 0 | 0.00% | 316 |
| `euribor_regime` | Engineered Feature | `str` | 41,188 | 0 | 0.00% | 2 |
| `nr_employed` | Macroeconomic Indicator | `float64` | 41,188 | 0 | 0.00% | 11 |
| `is_exact_duplicate` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 2 |
| `y` | Acquisition Target | `str` | 41,188 | 0 | 0.00% | 2 |
| `is_subscribed` | Engineered Feature | `int64` | 41,188 | 0 | 0.00% | 2 |

---

## 3. Engineered Attributes Null Verification
All 33 pre-call attributes maintain 0 nulls. `pdays_clean` is the sole attribute containing nulls, strictly mapping to uncontacted prospects:

| Attribute | Non-Null Count | Null Count | Null Pct (%) | Governance Rule |
| :--- | :--- | :--- | :--- | :--- |
| `pdays_clean` | 1,515 | 39,673 | 96.32% | Strictly maps to was_previously_contacted == 0 (pdays == 999) |
| Other 33 Columns | 41,188 | 0 | 0.00% | Zero missing values across all operational fields |

---

## 4. Governance of Categorical Unknown Values
Missing client profile attributes are explicitly retained as `'unknown'` categories to preserve sample integrity without imputation bias.

| Attribute Column | Explicit 'unknown' Count | Share of Total Leads (%) | Dialed Calls | Subscriptions | Conversion Rate (%) | Dialing Efficiency (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `default` | 8,597 | 20.87% | 23,604 | 443 | 5.15% | 1.88% |
| `education` | 1,731 | 4.20% | 4,494 | 251 | 14.50% | 5.59% |
| `housing` | 990 | 2.40% | 2,535 | 107 | 10.81% | 4.22% |
| `loan` | 990 | 2.40% | 2,535 | 107 | 10.81% | 4.22% |
| `job` | 330 | 0.80% | 874 | 37 | 11.21% | 4.23% |
| `marital` | 80 | 0.19% | 255 | 12 | 15.00% | 4.71% |

### Composite Governance Flag (`has_unknown_attributes`) Profile

| Governance Cohort | Lead Count | Lead Share (%) | Dialed Calls | Subscriptions | Conversion Rate (%) | Dialing Efficiency (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Fully Known Profiles | 30,488 | 74.02% | 76,874 | 3,859 | 12.66% | 5.02% |
| Has Unknown Attributes | 10,700 | 25.98% | 28,880 | 781 | 7.30% | 2.70% |

Key Governance Finding: Leads with unknown attributes (10,700 leads, 25.98% of portfolio) convert at 7.30% vs. 12.66% for complete profiles (1.73x conversion gap), primarily driven by the `default == 'unknown'` subset.

---

## 5. Reconstructed Chronological Timeline (2008-05 to 2010-11)
The 26-month timeline captures macroeconomic regime shifts from the 2008 financial crisis through low-rate stabilization in 2009 to 2010.

| Month Period | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Mean Euribor 3M |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2008-05 | 7,763 | 18.85% | 19,505 | 240 | 3.09% | 1.23% | 4.8577 |
| 2008-06 | 4,374 | 10.62% | 14,685 | 188 | 4.30% | 1.28% | 4.9316 |
| 2008-07 | 6,685 | 16.23% | 21,631 | 407 | 6.09% | 1.88% | 4.9616 |
| 2008-08 | 5,175 | 12.56% | 14,702 | 271 | 5.24% | 1.84% | 4.9648 |
| 2008-10 | 67 | 0.16% | 67 | 42 | 62.69% | 62.69% | 4.9238 |
| 2008-11 | 3,616 | 8.78% | 6,913 | 190 | 5.25% | 2.75% | 4.1149 |
| 2008-12 | 10 | 0.02% | 10 | 1 | 10.00% | 10.00% | 3.4934 |
| 2009-03 | 282 | 0.68% | 708 | 126 | 44.68% | 17.80% | 1.6462 |
| 2009-04 | 2,458 | 5.97% | 4,758 | 442 | 17.98% | 9.29% | 1.4117 |
| 2009-05 | 5,794 | 14.07% | 13,688 | 524 | 9.04% | 3.83% | 1.2936 |
| 2009-06 | 715 | 1.74% | 1,252 | 264 | 36.92% | 21.09% | 1.2579 |
| 2009-07 | 178 | 0.43% | 389 | 66 | 37.08% | 16.97% | 1.0252 |
| 2009-08 | 770 | 1.87% | 1,328 | 264 | 34.29% | 19.88% | 0.8661 |
| 2009-09 | 267 | 0.65% | 448 | 106 | 39.70% | 23.66% | 0.7831 |
| 2009-10 | 447 | 1.09% | 680 | 180 | 40.27% | 26.47% | 0.7355 |
| 2009-11 | 357 | 0.87% | 686 | 168 | 47.06% | 24.49% | 0.7161 |
| 2009-12 | 172 | 0.42% | 383 | 88 | 51.16% | 22.98% | 0.7125 |
| 2010-03 | 264 | 0.64% | 495 | 150 | 56.82% | 30.30% | 0.6463 |
| 2010-04 | 174 | 0.42% | 367 | 97 | 55.75% | 26.43% | 0.6455 |
| 2010-05 | 212 | 0.51% | 400 | 122 | 57.55% | 30.50% | 0.6863 |
| 2010-06 | 229 | 0.56% | 401 | 107 | 46.72% | 26.68% | 0.7330 |
| 2010-07 | 311 | 0.76% | 657 | 176 | 56.59% | 26.79% | 0.8500 |
| 2010-08 | 233 | 0.57% | 444 | 120 | 51.50% | 27.03% | 0.8992 |
| 2010-09 | 303 | 0.74% | 563 | 150 | 49.50% | 26.64% | 0.8803 |
| 2010-10 | 204 | 0.50% | 363 | 93 | 45.59% | 25.62% | 0.9952 |
| 2010-11 | 128 | 0.31% | 231 | 58 | 45.31% | 25.11% | 1.0422 |

---

## 6. Post-Call Duration Quarantine Validation
- Column `duration`: Strictly absent from precall targeting table (PASS).
- Column `duration_minutes`: Strictly absent from precall targeting table (PASS).
- Architecture Enforcement: Pre-call targeting dataset prevents predictive leakage by restricting access strictly to pre-dial attributes.
