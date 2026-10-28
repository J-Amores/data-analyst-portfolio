# Stage A Audit Report: Portfolio Aggregates & Contact Fatigue Auditing

## 1. Outbound Call Dispersion & Parametric / Non-Parametric Profiling
Analysis of outreach frequency demonstrates extreme positive skewness in outbound calling efforts.

| Feature | Count | Mean | Std Dev | Median (P50) | IQR | Min | P10 | P25 | P75 | P90 | P95 | P99 | Max | Skewness | Pearson Corr (Target) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `age` | 41,188 | 40.0241 | 10.4212 | 38.0000 | 15.0000 | 17.0000 | 28.0000 | 32.0000 | 47.0000 | 55.0000 | 58.0000 | 71.0000 | 98.0000 | 0.7847 | 0.0304 |
| `campaign` | 41,188 | 2.5676 | 2.7700 | 2.0000 | 2.0000 | 1.0000 | 1.0000 | 1.0000 | 3.0000 | 5.0000 | 7.0000 | 14.0000 | 56.0000 | 4.7625 | -0.0664 |
| `pdays_clean` | 1,515 | 6.0145 | 3.8249 | 6.0000 | 4.0000 | 0.0000 | 3.0000 | 3.0000 | 7.0000 | 12.0000 | 14.0000 | 18.0000 | 27.0000 | 1.4586 | -0.0352 |
| `previous` | 41,188 | 0.1730 | 0.4949 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 2.0000 | 7.0000 | 3.8320 | 0.2302 |
| `emp_var_rate` | 41,188 | 0.0819 | 1.5710 | 1.1000 | 3.2000 | -3.4000 | -1.8000 | -1.8000 | 1.4000 | 1.4000 | 1.4000 | 1.4000 | 1.4000 | -0.7241 | -0.2983 |
| `cons_price_idx` | 41,188 | 93.5757 | 0.5788 | 93.7490 | 0.9190 | 92.2010 | 92.8930 | 93.0750 | 93.9940 | 94.4650 | 94.4650 | 94.4650 | 94.7670 | -0.2309 | -0.1362 |
| `cons_conf_idx` | 41,188 | -40.5026 | 4.6282 | -41.8000 | 6.3000 | -50.8000 | -46.2000 | -42.7000 | -36.4000 | -36.1000 | -33.6000 | -26.9000 | -26.9000 | 0.3032 | 0.0549 |
| `euribor3m` | 41,188 | 3.6213 | 1.7344 | 4.8570 | 3.6170 | 0.6340 | 1.0460 | 1.3440 | 4.9610 | 4.9640 | 4.9660 | 4.9680 | 5.0450 | -0.7092 | -0.3078 |
| `nr_employed` | 41,188 | 5167.0359 | 72.2515 | 5191.0000 | 129.0000 | 4963.6000 | 5076.2000 | 5099.1000 | 5228.1000 | 5228.1000 | 5228.1000 | 5228.1000 | 5228.1000 | -1.0443 | -0.3547 |
| `duration` | 41,188 | 258.2850 | 259.2792 | 180.0000 | 217.0000 | 0.0000 | 59.0000 | 102.0000 | 319.0000 | 551.0000 | 752.6500 | 1271.1300 | 4918.0000 | 3.2631 | 0.4053 |
| `duration_minutes` | 41,188 | 4.3048 | 4.3213 | 3.0000 | 3.6167 | 0.0000 | 0.9833 | 1.7000 | 5.3167 | 9.1833 | 12.5442 | 21.1855 | 81.9667 | 3.2631 | 0.4053 |
| `balance` | 45,211 | 1362.2721 | 3044.7658 | 448.0000 | 1356.0000 | -8019.0000 | 0.0000 | 72.0000 | 1428.0000 | 3574.0000 | 5768.0000 | 13164.9000 | 102127.0000 | 8.3603 | 0.0528 |

---

## 2. Discrete Contact Fatigue Ladder & Marginal Conversion Yield
Marginal Conversion Rate = Subscriptions Won at Touch k / Leads Reaching Touch k.

| Touch (k) | Leads Reaching | Leads Evaluated | Dialed Calls | Subscriptions | Marginal Yield (%) | Cohort Yield (%) | Dialing Efficiency (%) | Cum Calls | Cum Subs | Call Share (%) | Sub Share (%) | Guardrail 1 (>=8.0%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Touch 1 | 41,188 | 17,642 | 17,642 | 2,300 | 5.58% | 13.04% | 13.04% | 17,642 | 2,300 | 16.68% | 49.57% | PASS |
| Touch 2 | 23,546 | 10,570 | 21,140 | 1,211 | 5.14% | 11.46% | 5.73% | 38,782 | 3,511 | 19.99% | 26.10% | PASS |
| Touch 3 | 12,976 | 5,341 | 16,023 | 574 | 4.42% | 10.75% | 3.58% | 54,805 | 4,085 | 15.15% | 12.37% | PASS |
| Touch 4 | 7,635 | 2,651 | 10,604 | 249 | 3.26% | 9.39% | 2.35% | 65,409 | 4,334 | 10.03% | 5.37% | PASS |
| Touch 5 | 4,984 | 1,599 | 7,995 | 120 | 2.41% | 7.50% | 1.50% | 73,404 | 4,454 | 7.56% | 2.59% | FAIL |
| Touch 6 | 3,385 | 979 | 5,874 | 75 | 2.22% | 7.66% | 1.28% | 79,278 | 4,529 | 5.55% | 1.62% | FAIL |
| Touch 7 | 2,406 | 629 | 4,403 | 38 | 1.58% | 6.04% | 0.86% | 83,681 | 4,567 | 4.16% | 0.82% | FAIL |
| Touch 8 | 1,777 | 400 | 3,200 | 17 | 0.96% | 4.25% | 0.53% | 86,881 | 4,584 | 3.03% | 0.37% | FAIL |
| Touch 9 | 1,377 | 283 | 2,547 | 17 | 1.23% | 6.01% | 0.67% | 89,428 | 4,601 | 2.41% | 0.37% | FAIL |
| Touch 10 | 1,094 | 225 | 2,250 | 12 | 1.10% | 5.33% | 0.53% | 91,678 | 4,613 | 2.13% | 0.26% | FAIL |
| Touch 11-15 | 869 | 514 | 6,374 | 22 | 2.53% | 4.28% | 0.35% | 98,052 | 4,635 | 6.03% | 0.47% | FAIL |
| Touch 16-56 | 355 | 355 | 7,702 | 5 | 1.41% | 1.41% | 0.06% | 105,754 | 4,640 | 7.28% | 0.11% | FAIL |

### Strategic Fatigue Insights & Guardrail Verification
- Diminishing Yields: Marginal conversion rate declines steadily from 5.58% at Touch 1 to 1.10% at Touch 10 and 1.41% at Touches 16-56.
- Guardrail 1 Violation: Cohort conversion rate falls below the 8.0% threshold at Touch 5 (7.50%) and stays depressed through Touch 16-56 (1.41%).
- Capping Policy Impact (Touches 1-3 Baseline vs. Touches 4+ Fatigue Zone):
  * Baseline Cohort (Touches 1-3): Captures 4,085 subscriptions (88.04% of total acquisitions) using 54,805 calls (51.82% of dialed capacity) at 12.17% conversion rate and 7.45% dialing efficiency.
  * Fatigue Zone (Touches 4+): Burns 50,949 outbound calls (48.18% of call center capacity) to produce only 555 subscriptions (11.96% of volume) at 7.27% conversion rate and 1.09% dialing efficiency (a 6.8x drop in dialing efficiency).
  * Operational Recommendation: Capping outreach at 3 touches preserves 88.04% of subscriptions while liberating 48.18% of total call center capacity.

---

## 3. Post-Hoc Operational Labor & Call Duration Audit
Audited against `fct_campaign_full_operational.parquet` to evaluate agent talk-time economics.

| Operational Dimension | Metric | Value | Unit | Strategic Context |
| :--- | :--- | :--- | :--- | :--- |
| Total Portfolio Talk Time | Total Seconds | 10,638,243 | seconds | Confirmed from operational parquet |
| Total Portfolio Talk Time | Total Minutes | 177,304.05 | minutes | Confirmed from operational parquet |
| Total Portfolio Talk Time | Total Hours | 2,955.07 | hours | Confirmed from operational parquet |
| Converted Prospects (y=1) | Mean Duration | 9.22 | minutes | Confirmed from operational parquet |
| Converted Prospects (y=1) | Median Duration | 7.48 | minutes | Confirmed from operational parquet |
| Converted Prospects (y=1) | IQR Duration | 8.14 | minutes | Confirmed from operational parquet |
| Converted Prospects (y=1) | Total Labor Hours | 713.00 | hours | Confirmed from operational parquet |
| Non-Converted Prospects (y=0) | Mean Duration | 3.68 | minutes | Confirmed from operational parquet |
| Non-Converted Prospects (y=0) | Median Duration | 2.73 | minutes | Confirmed from operational parquet |
| Non-Converted Prospects (y=0) | IQR Duration | 3.07 | minutes | Confirmed from operational parquet |
| Non-Converted Prospects (y=0) | Total Labor Hours | 2,242.07 | hours | Confirmed from operational parquet |
| Baseline Cohort (Touches 1-3) | Dialed Calls | 54,805 | calls | Confirmed from operational parquet |
| Baseline Cohort (Touches 1-3) | Subscriptions Won | 4,085 | subscriptions | Confirmed from operational parquet |
| Baseline Cohort (Touches 1-3) | Labor Hours Expended | 2,479.90 | hours | Confirmed from operational parquet |
| Baseline Cohort (Touches 1-3) | Agent Minutes Per Subscription | 36.42 | minutes/sub | Confirmed from operational parquet |
| Fatigue Zone (Touches 4+) | Dialed Calls Wasted | 50,949 | calls | Confirmed from operational parquet |
| Fatigue Zone (Touches 4+) | Subscriptions Won | 555 | subscriptions | Confirmed from operational parquet |
| Fatigue Zone (Touches 4+) | Labor Hours Expended | 475.17 | hours | Confirmed from operational parquet |
| Fatigue Zone (Touches 4+) | Agent Minutes Per Subscription | 51.37 | minutes/sub | Confirmed from operational parquet |

### Key Labor Takeaways
- Duration Disparity: Converted calls average 9.22 minutes (median: 7.48 min, IQR: 8.14 min) compared to non-converted calls averaging 3.68 minutes (median: 2.73 min, IQR: 3.07 min). This confirms duration is an outcome of customer dialogue rather than a pre-dial targeting feature.
- Labor Burn Beyond 3 Touches: The Fatigue Zone consumed 475.17 agent talk-time hours (28,510.25 talk minutes) across 50,949 dials, requiring 51.37 talk minutes per subscription won compared to 36.42 talk minutes per subscription won in the Baseline Cohort (a 41.0% increase in talk-time cost per acquisition).
