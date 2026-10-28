# Econometric Validation Report: Hypothesis 3 (Macro Elasticity, Demographics & Policy Simulation)

## Executive Summary
This evaluation formally tests Hypothesis 3 and presents an executive simulation of outbound dialer capping policies.
Hypothesis 3 posits that low Euribor regimes (`euribor3m <= 3.0%`) and high-affinity demographic cohorts (Senior/Retired and Students)
convert at > 3.0x the rate of working-age (31-45) prospects in high interest rate regimes.

> [!IMPORTANT]
> **Hypothesis 3 Status: FULLY SUPPORTED (p < 0.0001)**.
> Prospects in the Low Rate Regime convert at 24.46% vs 4.84% in the High Rate Regime (Relative Risk = 5.0573x > 3.0x, Dialing Efficiency = 6.77x).
> Senior/Retired prospects (60+) achieve 45.49% conversion (4.86x higher than the Core Working 31-45 cohort at 9.37%).
> The clean multivariate pre-call propensity model (zero duration leakage) achieves an ROC-AUC of 0.7704 (> 0.75 threshold).

## 1. Macroeconomic Interest Rate Regime Elasticity

| Macroeconomic Regime | Lead Count | Dialed Calls | Subscriptions Won | Conversion Rate (%) | Dialing Efficiency (%) | Relative Risk (Conversion) | Relative Risk (Efficiency) | Odds Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Low Rate Regime (`euribor3m <= 3.0%`) | 13,498 | 28,241 | 3,301 | 24.4555% | 11.6887% | 5.0573x [95% CI: 4.7624, 5.3704] | 6.7664x | 6.3707x [95% CI: 5.9550, 6.8155] |
| High Rate Regime (`euribor3m > 3.0%`) | 27,690 | 77,513 | 1,339 | 4.8357% | 1.7275% | Reference (1.0000x) | Reference (1.0000x) | Reference (1.0000x) |

* Pearson Chi-Square Test: `chi2 = 3492.4196` (df = 1, `p = 0.0000e+00`).

### Continuous Macroeconomic Indicator Differentials (Subscribers vs Non-Subscribers)

| Macro Indicator | Subscriber Mean | Non-Subscriber Mean | Welch t-statistic | p-value (t-test) | Mann-Whitney U | p-value (MW U) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `euribor3m` | 2.1231 | 3.8115 | -62.5799 | 0.0000e+00 | 43,501,741.5 | 0.0000e+00 |
| `emp_var_rate` | -1.2334 | 0.2489 | -59.1367 | 0.0000e+00 | 48,033,797.0 | 0.0000e+00 |
| `nr_employed` | 5095.1160 | 5176.1666 | -60.9752 | 0.0000e+00 | 42,565,804.0 | 0.0000e+00 |
| `cons_price_idx` | 93.3544 | 93.6038 | -24.0825 | 6.9165e-122 | 66,041,971.5 | 9.5726e-136 |
| `cons_conf_idx` | -39.7898 | -40.5931 | 8.6365 | 7.5882e-18 | 91,117,811.5 | 5.9020e-17 |

## 2. Demographic & Socio-Economic Misallocation (The 31-45 Volume Trap)

| Demographic Cohort | Lead Count | Total Calls | Subscriptions Won | Conversion Rate (%) | Dialing Efficiency (%) | Call Share (%) | Lift vs Core Working |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1. Young (<30) | 7,383 | 18,668 | 1,124 | 15.22% | 6.02% | 17.65% | 1.63x |
| 2. Core Working (31-45) | 21,974 | 56,174 | 2,058 | 9.37% | 3.66% | 53.12% | 1.00x |
| 3. Mature Working (46-60) | 10,921 | 29,122 | 1,044 | 9.56% | 3.58% | 27.54% | 1.02x |
| 4. Senior/Retired (60+) | 910 | 1,790 | 414 | 45.49% | 23.13% | 1.69% | 4.86x |

* Age Bucket Omnibus Chi-Square: `chi2 = 1293.4527` (df = 3, `p = 3.8767e-280`).
* Core Working Trap: Prospects aged 31-45 absorb 56,174 calls (53.12% of total dialer volume) while converting at only 9.37% (dialing efficiency: 3.66%).
* Senior/Retired Disparity: Prospects aged 60+ convert at 45.49% (4.86x higher than core working) but receive only 1,790 calls (1.69% of dialer bandwidth).

### Financial Benchmark Cross-Validation (`fct_legacy_balance_benchmark.parquet`, N=45,211)
* High Balance (`balance > 448 EUR`): 22,603 leads, 3,240 subs (14.33% conv) vs Low Balance: 22,608 leads, 2,049 subs (9.06% conv).
* Financial Liquidity Multiplier: `1.58x` conversion lift (Chi-Square = `303.51`, `p = 5.6514e-68`; Mann-Whitney U = `511,008,624.0`, `p < 0.0001`).

## 3. Multivariate Pre-Call Propensity Model (Zero Duration Leakage)
A multivariate logistic regression was estimated on all 41,188 leads strictly using pre-call attributes (ROC-AUC = `0.7704`, Pseudo R2 = `0.1710`).

| Feature | Coefficient | Std Err | z-statistic | p-value | Odds Ratio | 95% Confidence Interval | Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `const` | -2.8991 | 0.0755 | -38.3822 | 0.0000e+00 | 0.0551x | [0.0475, 0.0639] | Baseline intercept log-odds |
| `has_unknown_attributes` | -0.2640 | 0.0458 | -5.7684 | 8.0004e-09 | 0.7680x | [0.7021, 0.8401] | Penalty for leads with missing/unknown profile data |
| `campaign` | -0.0638 | 0.0094 | -6.7558 | 1.4207e-11 | 0.9382x | [0.9210, 0.9557] | Monotonic decay per additional contact dial attempt |
| `euribor_regime_Low Rate Regime (Euribor <= 3.0%)` | 1.3801 | 0.0417 | 33.0799 | 5.7833e-240 | 3.9754x | [3.6632, 4.3141] | Macroeconomic tailwind in low interest rate regimes |
| `contact_telephone` | -0.3730 | 0.0462 | -8.0825 | 6.3447e-16 | 0.6887x | [0.6291, 0.7538] | Penalty for dialing fixed landline vs cellular reference |
| `poutcome_nonexistent` | 0.3559 | 0.0513 | 6.9398 | 3.9254e-12 | 1.4275x | [1.2910, 1.5784] | Lift for prospects with no prior campaign history vs prior failure |
| `poutcome_success` | 2.2047 | 0.0733 | 30.0869 | 7.1999e-199 | 9.0671x | [7.8541, 10.4675] | Massive lift for prior campaign successful conversions vs prior failure |
| `age_bucket_2. Core Working (31-45)` | -0.2480 | 0.0443 | -5.6034 | 2.1015e-08 | 0.7804x | [0.7155, 0.8511] | Discount for core working-age cohort vs young (<30) reference |
| `age_bucket_3. Mature Working (46-60)` | -0.1503 | 0.0509 | -2.9548 | 3.1286e-03 | 0.8605x | [0.7788, 0.9507] | Discount for mature working-age cohort vs young (<30) reference |
| `age_bucket_4. Senior/Retired (60+)` | 0.5436 | 0.0866 | 6.2771 | 3.4501e-10 | 1.7222x | [1.4533, 2.0408] | Affinity lift for senior/retiree cohort vs young (<30) reference |
| `job_collar_tier_High-Yield Non-Working` | 0.4958 | 0.0585 | 8.4759 | 2.3336e-17 | 1.6418x | [1.4639, 1.8412] | Lift for students, retirees, and non-working high-affinity leads |
| `job_collar_tier_Unknown` | 0.3218 | 0.2053 | 1.5679 | 1.1690e-01 | 1.3797x | [0.9227, 2.0630] | Adjustment for unspecified occupation |
| `job_collar_tier_White-Collar` | 0.2610 | 0.0373 | 7.0051 | 2.4679e-12 | 1.2982x | [1.2068, 1.3966] | Lift for management, professional, and tech workers vs blue-collar |

## 4. Executive Outbound Policy Simulation Matrix
Comparison of operational scenarios reconciling to 41,188 total pipeline leads and 105,754 historical calls.

| Scenario ID | Scenario Description | Dialed Calls | Calls Saved (%) | Subscriptions Won | Retention (%) | Incremental Subs | Conversion (%) | Efficiency (%) | Labor Hours Saved | Min / Sub | Guardrail 1 (Conv >= 8%) | Guardrail 2 (Ret >= 85%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Scenario 0 | Historical Baseline (Uncapped Outreach) | 105,754 | 0 (0.0%) | 4,640 | 100.00% | 0 | 11.27% | 4.39% | 0.0 hrs | 38.21 min | PASS | PASS |
| Scenario 1A | Policy P0 (Strict 3-Touch Cap - Cohort Pruning) | 54,805 | 50,949 (48.2%) | 4,085 | 88.04% | -555 | 12.17% | 7.45% | 475.2 hrs | 36.42 min | PASS | PASS |
| Scenario 1B | Policy P0 (Strict 3-Touch Cap - Truncated Cap) | 77,710 | 28,044 (26.5%) | 4,085 | 88.04% | -555 | 9.92% | 5.26% | 475.2 hrs | 36.42 min | PASS | PASS |
| Scenario 2A | Policy P0 + P1/P2 Reallocation (Reinvest 28k Calls at 7.45%) | 105,754 | 0 (0.0%) | 6,175 | 133.08% | +1,535 | 12.17% | 5.84% | 0.0 hrs | 28.71 min | PASS | PASS |
| Scenario 2B | Policy P0 + P1/P2 Reallocation (Reinvest 28k Calls at 11.69% Low Rate) | 105,754 | 0 (0.0%) | 7,362 | 158.66% | +2,722 | 24.46% | 6.96% | 0.0 hrs | 24.08 min | PASS | PASS |
| Scenario 2C | Policy P0 + P1/P2 Reallocation (Reinvest 51k Calls at 7.45%) | 105,754 | 0 (0.0%) | 7,882 | 169.87% | +3,242 | 12.17% | 7.45% | 0.0 hrs | 22.49 min | PASS | PASS |

### Key Policy Findings
1. Policy P0 (Hard-Stop Cap at 3 Touches): Preserves 4,085 subscriptions (88.04% volume retention, passing the >= 85.0% Guardrail 2).
   Eliminates up to 50,949 wasted calls (Cohort Pruning) or 28,044 unproductive 4th+ dials (Truncated Cap) and frees 475.17 agent talk hours.
2. Policy P0 + P1/P2 Reallocation: Reinvesting 28,044 saved calls into Tier-1 priority segments (cellular, low-rate regime, and prior-contact leads) yields +1,535 to +2,723 incremental subscriptions (+33.1% to +58.7% commercial lift) while reducing acquisition talk time from 38.21 to 24.08 minutes per subscription.