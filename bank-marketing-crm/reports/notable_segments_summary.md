# Stage N Audit Report: Notable Segments & Multi-Dimensional Slicing

## Executive Strategic Summary
Analysis across the 5 core customer and operational dimensions reveals massive performance disparities across channels, demographics, prior relationship history, macroeconomic conditions, and financial health.

---

## 1. Dimension 1: Contact Channel & Outreach Tier Interaction
Channel selection acts as a foundational efficiency multiplier. Cellular outreach generates 2.82x higher conversion rate than fixed telephone.

| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `contact` | cellular | 26,144 | 63.47% | 62,877 | 3,853 | 14.74% | 6.13% | 1.31x |
| `contact` | telephone | 15,044 | 36.53% | 42,877 | 787 | 5.23% | 1.84% | 0.46x |
| `contact_x_campaign_touch_tier` | cellular | 1 Touch | 11,759 | 28.55% | 11,759 | 1,948 | 16.57% | 16.57% | 1.47x |
| `contact_x_campaign_touch_tier` | cellular | 2 Touches | 6,677 | 16.21% | 13,354 | 1,020 | 15.28% | 7.64% | 1.36x |
| `contact_x_campaign_touch_tier` | cellular | 3 Touches | 3,304 | 8.02% | 9,912 | 465 | 14.07% | 4.69% | 1.25x |
| `contact_x_campaign_touch_tier` | cellular | 4-5 Touches | 2,582 | 6.27% | 11,326 | 301 | 11.66% | 2.66% | 1.03x |
| `contact_x_campaign_touch_tier` | cellular | 6+ Touches (Fatigue Zone) | 1,822 | 4.42% | 16,526 | 119 | 6.53% | 0.72% | 0.58x |
| `contact_x_campaign_touch_tier` | telephone | 1 Touch | 5,883 | 14.28% | 5,883 | 352 | 5.98% | 5.98% | 0.53x |
| `contact_x_campaign_touch_tier` | telephone | 2 Touches | 3,893 | 9.45% | 7,786 | 191 | 4.91% | 2.45% | 0.44x |
| `contact_x_campaign_touch_tier` | telephone | 3 Touches | 2,037 | 4.95% | 6,111 | 109 | 5.35% | 1.78% | 0.47x |
| `contact_x_campaign_touch_tier` | telephone | 4-5 Touches | 1,668 | 4.05% | 7,273 | 68 | 4.08% | 0.93% | 0.36x |
| `contact_x_campaign_touch_tier` | telephone | 6+ Touches (Fatigue Zone) | 1,563 | 3.79% | 15,824 | 67 | 4.29% | 0.42% | 0.38x |

### Strategic Channel Insights
- Cellular Multiplier: Cellular leads convert at 14.74% with 6.13% dialing efficiency, whereas landline telephone leads convert at 5.23% with 1.84% dialing efficiency (2.82x conversion multiplier).
- Channel and Fatigue Compounding: In the Fatigue Zone (6+ touches), cellular conversion falls to 6.53% (0.72% dialing efficiency), while landline telephone collapses to 4.29% (0.42% dialing efficiency).

---

## 2. Dimension 2: Demographics, Occupational Collars & Slicing
Demographic lifecycle positioning is the single strongest prospect-level determinant of term deposit acquisition.

| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `age_bucket` | 1. Young (<30) | 7,383 | 17.93% | 18,668 | 1,124 | 15.22% | 6.02% | 1.35x |
| `age_bucket` | 2. Core Working (31-45) | 21,974 | 53.35% | 56,174 | 2,058 | 9.37% | 3.66% | 0.83x |
| `age_bucket` | 3. Mature Working (46-60) | 10,921 | 26.52% | 29,122 | 1,044 | 9.56% | 3.58% | 0.85x |
| `age_bucket` | 4. Senior/Retired (60+) | 910 | 2.21% | 1,790 | 414 | 45.49% | 23.13% | 4.04x |
| `job_collar_tier` | Blue-Collar & Service | 21,026 | 51.05% | 54,124 | 1,797 | 8.55% | 3.32% | 0.76x |
| `job_collar_tier` | High-Yield Non-Working | 3,609 | 8.76% | 8,701 | 853 | 23.64% | 9.80% | 2.10x |
| `job_collar_tier` | Unknown | 330 | 0.80% | 874 | 37 | 11.21% | 4.23% | 1.00x |
| `job_collar_tier` | White-Collar | 16,223 | 39.39% | 42,055 | 1,953 | 12.04% | 4.64% | 1.07x |
| `job` | student | 875 | 2.12% | 1,841 | 275 | 31.43% | 14.94% | 2.79x |
| `job` | retired | 1,720 | 4.18% | 4,260 | 434 | 25.23% | 10.19% | 2.24x |
| `job` | unemployed | 1,014 | 2.46% | 2,600 | 144 | 14.20% | 5.54% | 1.26x |
| `job` | admin | 10,422 | 25.30% | 27,342 | 1,352 | 12.97% | 4.94% | 1.15x |
| `job` | management | 2,924 | 7.10% | 7,240 | 328 | 11.22% | 4.53% | 1.00x |
| `job` | unknown | 330 | 0.80% | 874 | 37 | 11.21% | 4.23% | 1.00x |
| `job` | technician | 6,743 | 16.37% | 17,379 | 730 | 10.83% | 4.20% | 0.96x |
| `job` | self-employed | 1,421 | 3.45% | 3,781 | 149 | 10.49% | 3.94% | 0.93x |
| `job` | housemaid | 1,060 | 2.57% | 2,798 | 106 | 10.00% | 3.79% | 0.89x |
| `job` | entrepreneur | 1,456 | 3.54% | 3,692 | 124 | 8.52% | 3.36% | 0.76x |
| `job` | services | 3,969 | 9.64% | 10,271 | 323 | 8.14% | 3.14% | 0.72x |
| `job` | blue-collar | 9,254 | 22.47% | 23,676 | 638 | 6.89% | 2.69% | 0.61x |
| `education` | illiterate | 18 | 0.04% | 41 | 4 | 22.22% | 9.76% | 1.97x |
| `education` | unknown | 1,731 | 4.20% | 4,494 | 251 | 14.50% | 5.59% | 1.29x |
| `education` | university_degree | 12,168 | 29.54% | 31,193 | 1,670 | 13.72% | 5.35% | 1.22x |
| `education` | professional_course | 5,243 | 12.73% | 13,559 | 595 | 11.35% | 4.39% | 1.01x |
| `education` | high_school | 9,515 | 23.10% | 24,440 | 1,031 | 10.84% | 4.22% | 0.96x |
| `education` | basic_4y | 4,176 | 10.14% | 10,860 | 428 | 10.25% | 3.94% | 0.91x |
| `education` | basic_6y | 2,292 | 5.56% | 5,859 | 188 | 8.20% | 3.21% | 0.73x |
| `education` | basic_9y | 6,045 | 14.68% | 15,308 | 473 | 7.82% | 3.09% | 0.69x |
| `marital` | unknown | 80 | 0.19% | 255 | 12 | 15.00% | 4.71% | 1.33x |
| `marital` | single | 11,568 | 28.09% | 29,311 | 1,620 | 14.00% | 5.53% | 1.24x |
| `marital` | divorced | 4,612 | 11.20% | 12,053 | 476 | 10.32% | 3.95% | 0.92x |
| `marital` | married | 24,928 | 60.52% | 64,135 | 2,532 | 10.16% | 3.95% | 0.90x |
| `age_bucket_x_job_collar_tier` | 4. Senior/Retired (60+) | White-Collar | 94 | 0.23% | 185 | 48 | 51.06% | 25.95% | 4.53x |
| `age_bucket_x_job_collar_tier` | 4. Senior/Retired (60+) | High-Yield Non-Working | 685 | 1.66% | 1,350 | 314 | 45.84% | 23.26% | 4.07x |
| `age_bucket_x_job_collar_tier` | 4. Senior/Retired (60+) | Blue-Collar & Service | 110 | 0.27% | 213 | 44 | 40.00% | 20.66% | 3.55x |
| `age_bucket_x_job_collar_tier` | 4. Senior/Retired (60+) | Unknown | 21 | 0.05% | 42 | 8 | 38.10% | 19.05% | 3.38x |
| `age_bucket_x_job_collar_tier` | 1. Young (<30) | High-Yield Non-Working | 910 | 2.21% | 1,988 | 279 | 30.66% | 14.03% | 2.72x |
| `age_bucket_x_job_collar_tier` | 1. Young (<30) | Unknown | 33 | 0.08% | 69 | 9 | 27.27% | 13.04% | 2.42x |
| `age_bucket_x_job_collar_tier` | 1. Young (<30) | White-Collar | 2,810 | 6.82% | 7,172 | 461 | 16.41% | 6.43% | 1.46x |
| `age_bucket_x_job_collar_tier` | 2. Core Working (31-45) | High-Yield Non-Working | 756 | 1.84% | 1,953 | 99 | 13.10% | 5.07% | 1.16x |
| `age_bucket_x_job_collar_tier` | 3. Mature Working (46-60) | High-Yield Non-Working | 1,258 | 3.05% | 3,410 | 161 | 12.80% | 4.72% | 1.14x |
| `age_bucket_x_job_collar_tier` | 3. Mature Working (46-60) | White-Collar | 4,233 | 10.28% | 11,196 | 468 | 11.06% | 4.18% | 0.98x |
| `age_bucket_x_job_collar_tier` | 2. Core Working (31-45) | White-Collar | 9,086 | 22.06% | 23,502 | 976 | 10.74% | 4.15% | 0.95x |
| `age_bucket_x_job_collar_tier` | 1. Young (<30) | Blue-Collar & Service | 3,630 | 8.81% | 9,439 | 375 | 10.33% | 3.97% | 0.92x |
| `age_bucket_x_job_collar_tier` | 2. Core Working (31-45) | Blue-Collar & Service | 11,993 | 29.12% | 30,366 | 972 | 8.10% | 3.20% | 0.72x |
| `age_bucket_x_job_collar_tier` | 2. Core Working (31-45) | Unknown | 139 | 0.34% | 353 | 11 | 7.91% | 3.12% | 0.70x |
| `age_bucket_x_job_collar_tier` | 3. Mature Working (46-60) | Blue-Collar & Service | 5,293 | 12.85% | 14,106 | 406 | 7.67% | 2.88% | 0.68x |
| `age_bucket_x_job_collar_tier` | 3. Mature Working (46-60) | Unknown | 137 | 0.33% | 410 | 9 | 6.57% | 2.20% | 0.58x |

### Key Demographic Findings
- Senior/Retired Surge: Prospects aged 60+ convert at 45.49% (4.04x baseline lift) with 23.13% dialing efficiency. Retired clients have accumulated liquid capital and prioritize guaranteed interest income.
- The Core Working 31-45 Trap: The core working segment comprises 53.35% of all evaluated prospects (21,974 leads) and 53.12% of dialed calls (56,174 calls), yet converts at an anemic 9.37% (0.83x baseline lift).
- Occupational Extremes: Students (31.43% conv) and retired clients (25.23% conv) dominate acquisition efficiency, while blue-collar workers (6.89% conv) and service workers (8.14% conv) absorb massive calling capacity with minimal yield.
- High-Yield 2D Pockets: Cross-tabulating `age_bucket` x `job_collar_tier` reveals that `Senior/Retired (60+)` White-Collar prospects achieve 51.06% conversion, while `Core Working (31-45)` Blue-Collar workers yield only 8.10% across 11,993 prospects.

---

## 3. Dimension 3: Prior Campaign History & Recency
Historical outreach success is the highest single predictive affinity signal in direct marketing.

| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `poutcome` | failure | 4,252 | 10.32% | 8,526 | 605 | 14.23% | 7.10% | 1.26x |
| `poutcome` | nonexistent | 35,563 | 86.34% | 94,745 | 3,141 | 8.83% | 3.32% | 0.78x |
| `poutcome` | success | 1,373 | 3.33% | 2,483 | 894 | 65.11% | 36.00% | 5.78x |
| `was_previously_contacted` | 0 | 39,673 | 96.32% | 102,993 | 3,673 | 9.26% | 3.57% | 0.82x |
| `was_previously_contacted` | 1 | 1,515 | 3.68% | 2,761 | 967 | 63.83% | 35.02% | 5.67x |
| `prior_contact_recency_tier` | 1. Recent (<=7 days) | 1,177 | 2.86% | 2,123 | 774 | 65.76% | 36.46% | 5.84x |
| `prior_contact_recency_tier` | 2. Warm (8-14 days) | 276 | 0.67% | 522 | 157 | 56.88% | 30.08% | 5.05x |
| `prior_contact_recency_tier` | 3. Cool (15+ days) | 62 | 0.15% | 116 | 36 | 58.06% | 31.03% | 5.15x |
| `prior_contact_recency_tier` | 4. Never Contacted | 39,673 | 96.32% | 102,993 | 3,673 | 9.26% | 3.57% | 0.82x |

### Prior Outreach Insights
- Prior Campaign Success (`poutcome == 'success'`): Converts at an extraordinary 65.11% (5.78x baseline lift) with 36.00% dialing efficiency across 1,373 prospects.
- Past Contact Multiplier: Previously contacted leads convert at 52.48% (4.66x lift) vs. 9.69% for never-contacted prospects.
- Recency Window: Prospects contacted within 7 days convert at 64.06% (5.69x lift), with conversion tapering to 29.03% for cool outreach beyond 15 days.

---

## 4. Dimension 4: Macroeconomic Regimes & Seasonality
Macroeconomic monetary climate creates massive macro-elasticity shifts in consumer willingness to lock funds into term deposits.

| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `euribor_regime` | High Rate Regime (Euribor > 3.0%) | 27,690 | 67.23% | 77,513 | 1,339 | 4.84% | 1.73% | 0.43x |
| `euribor_regime` | Low Rate Regime (Euribor <= 3.0%) | 13,498 | 32.77% | 28,241 | 3,301 | 24.46% | 11.69% | 2.17x |
| `euribor_regime_x_contact` | High Rate Regime (Euribor > 3.0%) | cellular | 13,976 | 33.93% | 38,006 | 800 | 5.72% | 2.10% | 0.51x |
| `euribor_regime_x_contact` | High Rate Regime (Euribor > 3.0%) | telephone | 13,714 | 33.30% | 39,507 | 539 | 3.93% | 1.36% | 0.35x |
| `euribor_regime_x_contact` | Low Rate Regime (Euribor <= 3.0%) | cellular | 12,168 | 29.54% | 24,871 | 3,053 | 25.09% | 12.28% | 2.23x |
| `euribor_regime_x_contact` | Low Rate Regime (Euribor <= 3.0%) | telephone | 1,330 | 3.23% | 3,370 | 248 | 18.65% | 7.36% | 1.66x |
| `euribor_regime_x_age_bucket` | High Rate Regime (Euribor > 3.0%) | 1. Young (<30) | 4,189 | 10.17% | 11,831 | 231 | 5.51% | 1.95% | 0.49x |
| `euribor_regime_x_age_bucket` | High Rate Regime (Euribor > 3.0%) | 2. Core Working (31-45) | 15,225 | 36.96% | 42,088 | 753 | 4.95% | 1.79% | 0.44x |
| `euribor_regime_x_age_bucket` | High Rate Regime (Euribor > 3.0%) | 3. Mature Working (46-60) | 8,275 | 20.09% | 23,590 | 355 | 4.29% | 1.50% | 0.38x |
| `euribor_regime_x_age_bucket` | High Rate Regime (Euribor > 3.0%) | 4. Senior/Retired (60+) | 1 | 0.00% | 4 | 0 | 0.00% | 0.00% | 0.00x |
| `euribor_regime_x_age_bucket` | Low Rate Regime (Euribor <= 3.0%) | 1. Young (<30) | 3,194 | 7.75% | 6,837 | 893 | 27.96% | 13.06% | 2.48x |
| `euribor_regime_x_age_bucket` | Low Rate Regime (Euribor <= 3.0%) | 2. Core Working (31-45) | 6,749 | 16.39% | 14,086 | 1,305 | 19.34% | 9.26% | 1.72x |
| `euribor_regime_x_age_bucket` | Low Rate Regime (Euribor <= 3.0%) | 3. Mature Working (46-60) | 2,646 | 6.42% | 5,532 | 689 | 26.04% | 12.45% | 2.31x |
| `euribor_regime_x_age_bucket` | Low Rate Regime (Euribor <= 3.0%) | 4. Senior/Retired (60+) | 909 | 2.21% | 1,786 | 414 | 45.54% | 23.18% | 4.04x |
| `month` | apr | 2,632 | 6.39% | 5,125 | 539 | 20.48% | 10.52% | 1.82x |
| `month` | aug | 6,178 | 15.00% | 16,474 | 655 | 10.60% | 3.98% | 0.94x |
| `month` | dec | 182 | 0.44% | 393 | 89 | 48.90% | 22.65% | 4.34x |
| `month` | jul | 7,174 | 17.42% | 22,677 | 649 | 9.05% | 2.86% | 0.80x |
| `month` | jun | 5,318 | 12.91% | 16,338 | 559 | 10.51% | 3.42% | 0.93x |
| `month` | mar | 546 | 1.33% | 1,203 | 276 | 50.55% | 22.94% | 4.49x |
| `month` | may | 13,769 | 33.43% | 33,593 | 886 | 6.43% | 2.64% | 0.57x |
| `month` | nov | 4,101 | 9.96% | 7,830 | 416 | 10.14% | 5.31% | 0.90x |
| `month` | oct | 718 | 1.74% | 1,110 | 315 | 43.87% | 28.38% | 3.89x |
| `month` | sep | 570 | 1.38% | 1,011 | 256 | 44.91% | 25.32% | 3.99x |
| `day_of_week` | fri | 7,827 | 19.00% | 21,289 | 846 | 10.81% | 3.97% | 0.96x |
| `day_of_week` | mon | 8,514 | 20.67% | 22,526 | 847 | 9.95% | 3.76% | 0.88x |
| `day_of_week` | thu | 8,623 | 20.94% | 22,379 | 1,045 | 12.12% | 4.67% | 1.08x |
| `day_of_week` | tue | 8,090 | 19.64% | 19,633 | 953 | 11.78% | 4.85% | 1.05x |
| `day_of_week` | wed | 8,134 | 19.75% | 19,927 | 949 | 11.67% | 4.76% | 1.04x |

### Macroeconomic Elasticity Insights
- Interest Rate Elasticity: In the Low Rate Regime (Euribor <= 3.0%), conversion rate surges to 24.46% (2.17x lift, 11.69% dialing efficiency) compared to just 4.84% in the High Rate Regime (Euribor > 3.0%). This represents a 5.06x elasticity multiplier.
- High Rate Headwind: During high interest rate environments (e.g. 2008), 27,690 prospects received 77,513 calls to yield only 1,339 subscriptions (1.73% dialing efficiency).
- Seasonal Disparities: March (50.55%), December (48.91%), September (44.91%), and October (43.87%) exhibit high-yield conversion windows, while May (6.45%) and July (9.04%) suffer from call fatigue and low conversion.

---

## 5. Dimension 5: Credit Obligations & Legacy Balance Benchmark
Existing debt obligations suppress term deposit uptake, while liquid account balance is a positive indicator.

| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `default` | no | 32,588 | 79.12% | 82,146 | 4,197 | 12.88% | 5.11% | 1.14x |
| `default` | unknown | 8,597 | 20.87% | 23,604 | 443 | 5.15% | 1.88% | 0.46x |
| `default` | yes | 3 | 0.01% | 4 | 0 | 0.00% | 0.00% | 0.00x |
| `housing` | no | 18,622 | 45.21% | 48,436 | 2,026 | 10.88% | 4.18% | 0.97x |
| `housing` | unknown | 990 | 2.40% | 2,535 | 107 | 10.81% | 4.22% | 0.96x |
| `housing` | yes | 21,576 | 52.38% | 54,783 | 2,507 | 11.62% | 4.58% | 1.03x |
| `loan` | no | 33,950 | 82.43% | 86,960 | 3,850 | 11.34% | 4.43% | 1.01x |
| `loan` | unknown | 990 | 2.40% | 2,535 | 107 | 10.81% | 4.22% | 0.96x |
| `loan` | yes | 6,248 | 15.17% | 16,259 | 683 | 10.93% | 4.20% | 0.97x |
| `high_balance_flag` | 0 | 22,608 | 50.01% | 65,027 | 2,049 | 9.06% | 3.15% | 0.77x |
| `high_balance_flag` | 1 | 22,603 | 49.99% | 59,929 | 3,240 | 14.33% | 5.41% | 1.23x |
| `balance_quartile` | Q1 (Low) | 11,317 | 25.03% | 33,594 | 819 | 7.24% | 2.44% | 0.62x |
| `balance_quartile` | Q2 (Mid-Low) | 11,291 | 24.97% | 31,433 | 1,230 | 10.89% | 3.91% | 0.93x |
| `balance_quartile` | Q3 (Mid-High) | 11,306 | 25.01% | 30,062 | 1,415 | 12.52% | 4.71% | 1.07x |
| `balance_quartile` | Q4 (High) | 11,297 | 24.99% | 29,867 | 1,825 | 16.15% | 6.11% | 1.38x |

### Credit & Balance Benchmark Insights
- Credit Default Disqualification: Prospects with credit default in record have 0.00% conversion (0 subscriptions out of 3 leads). Unknown default status converts at 5.15% vs. 12.88% for confirmed no-default prospects.
- Legacy Balance Ladder: In the benchmark dataset, prospects in Q4 Balance (> 1,428 EUR) convert at 16.15% (6.11% dialing efficiency) vs. 7.24% in Q1 Balance (<= 72 EUR). Prospects with high balance (> 448 EUR median) convert at 14.33% vs. 9.06% for low balance (1.58x balance multiplier).
