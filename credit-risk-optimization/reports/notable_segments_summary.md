# SCAN Notable Segments Profiling
**Project:** LendingClub Consumer Credit Risk & Underwriting Optimization  
**Framework:** Christine Jiang SCAN EDA Framework (Stage N – Notable Segments)  
**Execution Timestamp:** 2026-10-19 | Runtime: 2.54 seconds  
**Dataset:** Seasoned Closed Cohort (1,345,350 loans)  

---

## Executive Highlights & Key Inflection Findings

1. **Default Rate Inflection Point (Crossing 20.0%):** Occurs at Subgrade **`C2`** (20.72% bad rate), up from `C1` (18.99%).
2. **Cost-of-Capital Breakdown (+4.0% Hurdle):**
   - **Median LAROC:** Declines below +4.0% at Subgrade **`G4`** (3.65%).
   - **Mean LAROC:** Breaks down below +4.0% earlier at Subgrade **`C4`** (3.80%).
   - **Cohort Aggregate LAROC:** Drops below +4.0% at Subgrade **`C4`** (3.44%), turning negative by Subgrade `E5` (-1.34%).
3. **Term Risk Distortion:** 60-month loans exhibit a **32.45% bad rate** (more than 2.0x higher than 36-month loans at 16.00%), reducing cohort net returns from 5.12% down to 2.57%.
4. **Outsized Purpose Risk:** `small_business` originations represent the most toxic major loan purpose: **29.71% bad rate** and a **negative net cohort LAROC (-0.59%)**.
5. **High-Risk Interaction:** Borrowers combining `DTI > 25%` and `Revolving Utilization > 65%` generate a **28.41% default rate** (2.01x relative risk vs. conservative borrowers).

---

## 1. Segment Dimension 1: Loan Grade & Subgrade Profiling

### Loan Grade Summary (A through G)

| Grade | Volume Count | Volume Share (%) | Total Funded ($) | Funded Share (%) | Bad Loan Count | Terminal Bad Rate (%) | Median LAROC (%) | Mean LAROC (%) | Cohort LAROC (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | 235,095 | 17.47% | $3,263,735,050.00 | 16.83% | 14,206 | **6.04%** | 8.58% | 5.56% | **5.69%** |
| **B** | 392,748 | 29.19% | $5,195,857,925.00 | 26.80% | 52,576 | **13.39%** | 12.67% | 6.11% | **6.02%** |
| **C** | 381,694 | 28.37% | $5,413,717,400.00 | 27.92% | 85,657 | **22.44%** | 14.52% | 4.50% | **4.21%** |
| **D** | 200,966 | 14.94% | $3,068,057,125.00 | 15.82% | 61,067 | **30.39%** | 15.25% | 3.26% | **2.64%** |
| **E** | 93,656 | 6.96% | $1,648,265,625.00 | 8.50% | 36,041 | **38.48%** | 13.53% | 1.94% | **1.66%** |
| **F** | 32,059 | 2.38% | $611,075,025.00 | 3.15% | 14,492 | **45.20%** | 10.13% | 0.52% | **-0.18%** |
| **G** | 9,132 | 0.68% | $187,877,125.00 | 0.97% | 4,560 | **49.93%** | 4.72% | -4.80% | **-4.66%** |

### Granular Subgrade Profile (A1 through G5)

| Subgrade | Volume Count | Total Funded ($) | Bad Count | Terminal Bad Rate (%) | Median LAROC (%) | Mean LAROC (%) | Cohort LAROC (%) | Risk Alert |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `A1` | 43,679 | $612,489,525.00 | 1,409 | 3.23% | 7.21% | 5.04% | 5.00% |  |
| `A2` | 37,178 | $497,284,000.00 | 1,734 | 4.66% | 8.46% | 5.30% | 5.40% |  |
| `A3` | 37,997 | $516,719,475.00 | 2,094 | 5.51% | 9.18% | 5.56% | 5.72% |  |
| `A4` | 52,236 | $733,191,250.00 | 3,588 | 6.87% | 9.91% | 5.65% | 5.77% |  |
| `A5` | 64,005 | $904,050,800.00 | 5,381 | 8.41% | 10.86% | 6.00% | 6.24% |  |
| `B1` | 71,154 | $940,350,150.00 | 7,416 | 10.42% | 10.90% | 5.43% | 5.28% |  |
| `B2` | 74,025 | $985,143,750.00 | 8,410 | 11.36% | 12.45% | 6.37% | 6.36% |  |
| `B3` | 81,828 | $1,102,463,925.00 | 10,625 | 12.98% | 13.51% | 6.73% | 6.69% |  |
| `B4` | 83,200 | $1,103,930,025.00 | 12,337 | 14.83% | 13.88% | 6.55% | 6.60% |  |
| `B5` | 82,541 | $1,063,970,075.00 | 13,788 | 16.70% | 13.43% | 5.42% | 5.08% |  |
| `C1` | 85,496 | $1,147,548,475.00 | 16,232 | 18.99% | 14.11% | 5.09% | 4.76% |  |
| `C2` | 79,215 | $1,082,660,275.00 | 16,414 | 20.72% | 14.68% | 5.13% | 5.02% | 🔴 **Crosses 20% Bad Rate** |
| `C3` | 75,000 | $1,075,043,525.00 | 16,894 | 22.53% | 14.81% | 4.75% | 4.64% |  |
| `C4` | 74,422 | $1,105,582,825.00 | 18,547 | 24.92% | 14.62% | 3.80% | 3.44% |  |
| `C5` | 67,561 | $1,002,882,300.00 | 17,570 | 26.01% | 14.52% | 3.49% | 3.10% |  |
| `D1` | 51,323 | $752,555,300.00 | 14,272 | 27.81% | 15.79% | 3.97% | 3.41% |  |
| `D2` | 44,851 | $663,380,075.00 | 13,272 | 29.59% | 15.22% | 3.11% | 2.27% |  |
| `D3` | 39,322 | $597,286,250.00 | 12,013 | 30.55% | 15.04% | 2.96% | 2.05% |  |
| `D4` | 35,568 | $564,736,500.00 | 11,514 | 32.37% | 15.06% | 3.16% | 2.92% |  |
| `D5` | 29,902 | $490,099,000.00 | 9,996 | 33.43% | 14.52% | 2.77% | 2.36% |  |
| `E1` | 23,749 | $402,340,025.00 | 8,565 | 36.06% | 15.05% | 3.05% | 2.86% |  |
| `E2` | 21,378 | $368,750,500.00 | 8,027 | 37.55% | 14.45% | 2.67% | 2.46% |  |
| `E3` | 18,387 | $323,704,725.00 | 7,118 | 38.71% | 13.78% | 2.18% | 2.10% |  |
| `E4` | 15,723 | $288,431,700.00 | 6,307 | 40.11% | 12.56% | 1.64% | 1.24% |  |
| `E5` | 14,419 | $265,038,675.00 | 6,024 | 41.78% | 10.00% | -0.94% | -1.34% | ⛔ **Negative Net Return** |
| `F1` | 9,970 | $185,035,725.00 | 4,217 | 42.30% | 11.59% | 1.69% | 0.45% |  |
| `F2` | 7,198 | $137,709,825.00 | 3,264 | 45.35% | 10.75% | 0.87% | 0.87% |  |
| `F3` | 6,088 | $114,667,025.00 | 2,744 | 45.07% | 10.90% | 1.13% | 0.30% |  |
| `F4` | 4,859 | $94,021,700.00 | 2,327 | 47.89% | 8.51% | -0.47% | -1.56% | ⛔ **Negative Net Return** |
| `F5` | 3,944 | $79,640,750.00 | 1,940 | 49.19% | 6.43% | -2.83% | -2.55% | ⛔ **Negative Net Return** |
| `G1` | 2,997 | $60,821,675.00 | 1,434 | 47.85% | 6.40% | -3.08% | -3.02% | ⛔ **Negative Net Return** |
| `G2` | 2,131 | $42,556,950.00 | 1,047 | 49.13% | 6.66% | -2.98% | -3.16% | ⛔ **Negative Net Return** |
| `G3` | 1,614 | $33,959,575.00 | 829 | 51.36% | 4.65% | -4.36% | -3.76% | ⛔ **Negative Net Return** |
| `G4` | 1,280 | $27,000,825.00 | 655 | 51.17% | 3.65% | -7.60% | -7.34% | ⚠️ **Median LAROC < 4%** |
| `G5` | 1,110 | $23,538,100.00 | 595 | 53.60% | 0.40% | -10.33% | -9.81% | ⛔ **Negative Net Return** |

---

## 2. Segment Dimension 2: Loan Term Profiling (36-Month vs. 60-Month)

| Term Length | Volume Count | Volume Share (%) | Total Funded ($) | Funded Share (%) | Bad Loan Count | Terminal Bad Rate (%) | Median LAROC (%) | Mean LAROC (%) | Cohort LAROC (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **36 Months** | 1,020,768 | 75.87% | $12,804,486,175.00 | 66.04% | 163,277 | **16.00%** | 11.29% | 5.32% | **5.12%** |
| **60 Months** | 324,582 | 24.13% | $6,584,099,100.00 | 33.96% | 105,322 | **32.45%** | 12.69% | 2.47% | **2.57%** |

> [!WARNING]
> **Term Delinquency Differential:** 60-month loans experience a **32.45% bad rate** vs. 16.00% for 36-month contracts (+16.45 percentage points, a 2.03x risk multiplier). This severe delinquency burden halves cohort net profitability from 5.12% to 2.57%, falling well short of institutional yield hurdles.

---

## 3. Segment Dimension 3: Primary Loan Purpose Profiling

| Loan Purpose | Volume Count | Volume Share (%) | Total Funded ($) | Funded Share (%) | Bad Loan Count | Terminal Bad Rate (%) | Median LAROC (%) | Mean LAROC (%) | Cohort LAROC (%) | Risk Profile |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `debt_consolidation` | 780,342 | 58.00% | $11,880,395,625.00 | 61.28% | 165,035 | **21.15%** | 11.76% | 4.57% | 4.37% | Standard Commercial |
| `credit_card` | 295,285 | 21.95% | $4,372,026,350.00 | 22.55% | 49,988 | **16.93%** | 11.26% | 5.57% | 5.51% | 🟢 **High Yield Core** |
| `home_improvement` | 87,507 | 6.50% | $1,236,808,100.00 | 6.38% | 15,505 | **17.72%** | 10.36% | 4.52% | 3.57% | Standard Commercial |
| `other` | 77,877 | 5.79% | $764,771,775.00 | 3.94% | 16,387 | **21.04%** | 11.33% | 3.84% | 1.80% | Standard Commercial |
| `major_purchase` | 29,427 | 2.19% | $347,952,700.00 | 1.79% | 5,475 | **18.61%** | 9.99% | 2.95% | -0.46% | ⚠️ Net Cash Drag |
| `small_business` | 15,416 | 1.15% | $240,101,250.00 | 1.24% | 4,580 | **29.71%** | 12.27% | 1.22% | -0.59% | 🔴 **Severe Risk / Negative Return** |
| `medical` | 15,556 | 1.16% | $139,923,475.00 | 0.72% | 3,389 | **21.79%** | 10.55% | 2.29% | 0.24% | Standard Commercial |
| `car` | 14,588 | 1.08% | $128,946,375.00 | 0.67% | 2,144 | **14.70%** | 10.53% | 5.64% | 4.18% | Standard Commercial |
| `house` | 7,254 | 0.54% | $111,572,125.00 | 0.58% | 1,588 | **21.89%** | 7.89% | 1.51% | 0.27% | Standard Commercial |
| `moving` | 9,480 | 0.70% | $74,462,025.00 | 0.38% | 2,214 | **23.35%** | 11.40% | 2.53% | 0.24% | Standard Commercial |
| `vacation` | 9,065 | 0.67% | $56,101,625.00 | 0.29% | 1,738 | **19.17%** | 10.65% | 3.91% | -0.17% | ⚠️ Net Cash Drag |
| `wedding` | 2,294 | 0.17% | $24,021,125.00 | 0.12% | 279 | **12.16%** | 17.55% | 14.09% | 14.64% | Standard Commercial |
| `renewable_energy` | 933 | 0.07% | $9,325,600.00 | 0.05% | 221 | **23.69%** | 11.62% | 2.60% | 1.74% | Standard Commercial |
| `educational` | 326 | 0.02% | $2,177,125.00 | 0.01% | 56 | **17.18%** | 15.10% | 7.58% | 6.12% | Standard Commercial |

> [!CAUTION]
> **Small Business Toxicity:** `small_business` originations represent $240.10M in funded capital across 15,416 originations. At **29.71% terminal default**, interest income is insufficient to cover write-offs, producing a **-0.59% net cohort return**.

---

## 4. Segment Dimension 4: Multi-Variable Risk Grid (DTI x Revolving Line Utilization)

Cross-tabulation of Debt-to-Income brackets against Revolving Credit Utilization tiers across 1,344,118 loans with complete ratios:

### 4A. Terminal Bad Loan Rate Matrix (%)

| DTI Bracket \ Revolving Utilization | 1. Conservative (<=40%) | 2. Moderate (40-65%) | 3. High (65-85%) | 4. Maxed (>85%) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Low (<=15%)** | 14.11% | 16.31% | 17.29% | **18.68%** |
| **2. Moderate (15-25%)** | 17.77% | 20.69% | 21.61% | **22.73%** |
| **3. High (25-35%)** | 22.88% | 26.86% | 27.81% | **28.02%** |
| **4. Severe (>35%)** | 26.97% | 31.94% | 32.41% | **31.78%** |

### 4B. Loan Origination Volume & Funded Principal Matrix

| DTI Bracket \ Revolving Utilization | 1. Conservative (<=40%) | 2. Moderate (40-65%) | 3. High (65-85%) | 4. Maxed (>85%) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Low (<=15%)** | 213,691 ($2809.5M) | 166,352 ($2392.1M) | 95,265 ($1441.5M) | 43,566 ($637.5M) |
| **2. Moderate (15-25%)** | 157,046 ($2073.3M) | 189,080 ($2829.9M) | 126,726 ($2011.7M) | 56,841 ($891.5M) |
| **3. High (25-35%)** | 66,841 ($860.1M) | 95,396 ($1397.0M) | 68,400 ($1060.8M) | 30,018 ($461.5M) |
| **4. Severe (>35%)** | 8,324 ($109.6M) | 12,744 ($184.5M) | 9,526 ($147.5M) | 4,302 ($64.0M) |

### 4C. Median & Mean LAROC Return Matrix (%)

| DTI Bracket \ Revolving Utilization | 1. Conservative (<=40%) | 2. Moderate (40-65%) | 3. High (65-85%) | 4. Maxed (>85%) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Low (<=15%)** | Med: 9.0% / Avg: 3.9% | Med: 11.9% / Avg: 6.5% | Med: 13.5% / Avg: 8.1% | Med: 14.5% / Avg: 8.2% |
| **2. Moderate (15-25%)** | Med: 9.3% / Avg: 2.8% | Med: 12.1% / Avg: 4.8% | Med: 13.8% / Avg: 6.6% | Med: 14.9% / Avg: 7.3% |
| **3. High (25-35%)** | Med: 9.6% / Avg: 0.7% | Med: 12.2% / Avg: 2.0% | Med: 13.8% / Avg: 3.5% | Med: 14.9% / Avg: 4.4% |
| **4. Severe (>35%)** | Med: 9.0% / Avg: -2.0% | Med: 12.0% / Avg: -0.8% | Med: 13.3% / Avg: -0.0% | Med: 14.6% / Avg: 1.8% |

### 4D. High-Risk Intersection Profile (`DTI > 25%` AND `Revol_Util > 65%`)

| High-Risk Intersection Metric | Value | Comparison vs. Portfolio Baseline |
| :--- | :--- | :--- |
| **High-Risk Segment Volume** | **112,246 loans** | 8.35% of valid seasoned originations |
| **High-Risk Funded Principal** | **$1,733,825,550.00** | 8.95% of total funded principal |
| **Terminal Bad Loan Count** | **31,889 loans** | High loss concentration in 8.35% volume |
| **High-Risk Bad Loan Rate** | **28.41%** | **+9.21 pp vs. Baseline (19.20%)** |
| **Relative Risk vs. Baseline** | **1.48x** | Severe non-linear default multiplication |
| **Relative Risk vs. Prime (Low DTI / Low Util)** | **2.01x** | 2.01x default rate compared to prime tier (14.11%) |
| **High-Risk Mean LAROC** | **3.41%** | Degrades below +4.0% cost of capital hurdle |
| **High-Risk Cohort Net LAROC** | **3.01%** | Thin net margin (3.01%) |

> [!IMPORTANT]
> **Actionable Hard-Stop Target:** The `DTI > 25%` and `Revol_Util > 65%` intersection accounts for 112,246 originations with a **28.41% terminal default rate**. Enforcing an automated hard-stop decline policy on this segment would eliminate 31,889 terminal defaults while **preserving 91.65% of applicant book volume**, comfortably exceeding the 80.0% volume retention guardrail.

---
*Report automatically generated by `src/analytics/scan_segments.py` in 2.54 seconds.*
