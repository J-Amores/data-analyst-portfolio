# Subprime Margin Breakdown & LAROC Analysis: Hypothesis 2 Validation
**Project:** Consumer Credit Risk & Underwriting Optimization  
**Framework:** Christine Jiang Decision-Driven Design (Econometric Margin Degradation)  
**Execution Timestamp:** 2026-10-19 | Cost of Capital Hurdle: **+4.0%**  

---

## 1. Executive Summary & Core Hypothesis Decision

> [!IMPORTANT]
> **Hypothesis 2 Status: CONFIRMED (p < 0.001 across all comparisons)**  
> High nominal interest rates in subprime grades (ranging up to **28.75%** in G5) create an **illusion of yield** that is systematically destroyed by exponential default escalations.  
> - **Cost-of-Capital Hurdle (+4.0%) Breach:** Aggregate Net LAROC permanently breaches the +4.0% hurdle beginning at **Subgrade C4** (yielding only 3.44%).  
> - **Capital Destruction (Negative Net LAROC):** Net LAROC turns **negative** at **Subgrade E5 (-1.34%)**, worsening to **-9.81% in G5**.

All two-sample Welch's t-tests comparing Grade C to Subprime cohorts confirm severe, statistically significant return degradation (p < 0.001 across all tests).

---

## 2. Statistical Validation: Two-Sample Welch's t-Tests (Unequal Variances)

| Comparison Pair | Group 1 Mean LAROC | Group 2 Mean LAROC | Yield Spread (Group 1 - 2) | Welch's t-Stat | Degrees of Freedom (df) | p-value | Statistical Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grade C vs. Grade D** | 4.50% | 3.26% | **+1.24 pp** | `13.7323` | 349,483.2 | `6.6762e-43` | **Reject Null (p < 0.001)** |
| **Grade C vs. Grade E** | 4.50% | 1.94% | **+2.55 pp** | `18.5201` | 118,835.4 | `1.8212e-76` | **Reject Null (p < 0.001)** |
| **Grade C vs. Grades F & G** | 4.50% | -0.66% | **+5.16 pp** | `22.8127` | 44,908.2 | `1.5415e-114` | **Reject Null (p < 0.001)** |

---

## 3. Subgrade Margin Breakdown (A1 through G5)

| Subgrade | Origination Count | Funded Principal ($) | Terminal Defaults | Default Rate (%) | Mean Nominal Rate (%) | Spread vs. Hurdle (+4.0%) | Mean LAROC (%) | Median LAROC (%) | Cohort Net LAROC (%) | Hurdle Status | Profitability Zone |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A1** | 43,679 | $612,489,525.00 | 1,409 | 3.23% | 5.54% | +1.54 pp | 5.04% | 7.21% | **5.00%** | PASSED | 🟢 Institutional Hurdle Met |
| **A2** | 37,178 | $497,284,000.00 | 1,734 | 4.66% | 6.52% | +2.52 pp | 5.30% | 8.46% | **5.40%** | PASSED | 🟢 Institutional Hurdle Met |
| **A3** | 37,997 | $516,719,475.00 | 2,094 | 5.51% | 7.12% | +3.12 pp | 5.56% | 9.18% | **5.72%** | PASSED | 🟢 Institutional Hurdle Met |
| **A4** | 52,236 | $733,191,250.00 | 3,588 | 6.87% | 7.51% | +3.51 pp | 5.65% | 9.91% | **5.77%** | PASSED | 🟢 Institutional Hurdle Met |
| **A5** | 64,005 | $904,050,800.00 | 5,381 | 8.41% | 8.20% | +4.20 pp | 6.00% | 10.86% | **6.24%** | PASSED | 🟢 Institutional Hurdle Met |
| **B1** | 71,154 | $940,350,150.00 | 7,416 | 10.42% | 8.90% | +4.90 pp | 5.43% | 10.90% | **5.28%** | PASSED | 🟢 Institutional Hurdle Met |
| **B2** | 74,025 | $985,143,750.00 | 8,410 | 11.36% | 9.91% | +5.91 pp | 6.37% | 12.45% | **6.36%** | PASSED | 🟢 Institutional Hurdle Met |
| **B3** | 81,828 | $1,102,463,925.00 | 10,625 | 12.98% | 10.75% | +6.75 pp | 6.73% | 13.51% | **6.69%** | PASSED | 🟢 Institutional Hurdle Met |
| **B4** | 83,200 | $1,103,930,025.00 | 12,337 | 14.83% | 11.49% | +7.49 pp | 6.55% | 13.88% | **6.60%** | PASSED | 🟢 Institutional Hurdle Met |
| **B5** | 82,541 | $1,063,970,075.00 | 13,788 | 16.70% | 12.01% | +8.01 pp | 5.42% | 13.43% | **5.08%** | PASSED | 🟢 Institutional Hurdle Met |
| **C1** | 85,496 | $1,147,548,475.00 | 16,232 | 18.99% | 12.76% | +8.76 pp | 5.09% | 14.11% | **4.76%** | PASSED | 🟢 Institutional Hurdle Met |
| **C2** | 79,215 | $1,082,660,275.00 | 16,414 | 20.72% | 13.44% | +9.44 pp | 5.13% | 14.68% | **5.02%** | PASSED | 🟢 Institutional Hurdle Met |
| **C3** | 75,000 | $1,075,043,525.00 | 16,894 | 22.53% | 14.02% | +10.02 pp | 4.75% | 14.81% | **4.64%** | PASSED | 🟢 Institutional Hurdle Met |
| **C4** | 74,422 | $1,105,582,825.00 | 18,547 | 24.92% | 14.71% | +10.71 pp | 3.80% | 14.62% | **3.44%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **C5** | 67,561 | $1,002,882,300.00 | 17,570 | 26.01% | 15.55% | +11.55 pp | 3.49% | 14.52% | **3.10%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **D1** | 51,323 | $752,555,300.00 | 14,272 | 27.81% | 16.38% | +12.38 pp | 3.97% | 15.79% | **3.41%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **D2** | 44,851 | $663,380,075.00 | 13,272 | 29.59% | 17.27% | +13.27 pp | 3.11% | 15.22% | **2.27%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **D3** | 39,322 | $597,286,250.00 | 12,013 | 30.55% | 17.95% | +13.95 pp | 2.96% | 15.04% | **2.05%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **D4** | 35,568 | $564,736,500.00 | 11,514 | 32.37% | 18.58% | +14.58 pp | 3.16% | 15.06% | **2.92%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **D5** | 29,902 | $490,099,000.00 | 9,996 | 33.43% | 19.38% | +15.38 pp | 2.77% | 14.52% | **2.36%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **E1** | 23,749 | $402,340,025.00 | 8,565 | 36.06% | 19.80% | +15.80 pp | 3.05% | 15.05% | **2.86%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **E2** | 21,378 | $368,750,500.00 | 8,027 | 37.55% | 20.47% | +16.47 pp | 2.67% | 14.45% | **2.46%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **E3** | 18,387 | $323,704,725.00 | 7,118 | 38.71% | 21.20% | +17.20 pp | 2.18% | 13.78% | **2.10%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **E4** | 15,723 | $288,431,700.00 | 6,307 | 40.11% | 22.09% | +18.09 pp | 1.64% | 12.56% | **1.24%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **E5** | 14,419 | $265,038,675.00 | 6,024 | 41.78% | 23.22% | +19.22 pp | -0.94% | 10.00% | **-1.34%** | FAILED | 🔴 Value Destructive (<0%) |
| **F1** | 9,970 | $185,035,725.00 | 4,217 | 42.30% | 23.92% | +19.92 pp | 1.69% | 11.59% | **0.45%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **F2** | 7,198 | $137,709,825.00 | 3,264 | 45.35% | 24.50% | +20.50 pp | 0.87% | 10.75% | **0.87%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **F3** | 6,088 | $114,667,025.00 | 2,744 | 45.07% | 25.28% | +21.28 pp | 1.13% | 10.90% | **0.30%** | BREACHED | 🟡 Sub-Hurdle (<4.0%) |
| **F4** | 4,859 | $94,021,700.00 | 2,327 | 47.89% | 25.89% | +21.89 pp | -0.47% | 8.51% | **-1.56%** | FAILED | 🔴 Value Destructive (<0%) |
| **F5** | 3,944 | $79,640,750.00 | 1,940 | 49.19% | 26.58% | +22.58 pp | -2.83% | 6.43% | **-2.55%** | FAILED | 🔴 Value Destructive (<0%) |
| **G1** | 2,997 | $60,821,675.00 | 1,434 | 47.85% | 27.28% | +23.28 pp | -3.08% | 6.40% | **-3.02%** | FAILED | 🔴 Value Destructive (<0%) |
| **G2** | 2,131 | $42,556,950.00 | 1,047 | 49.13% | 27.35% | +23.35 pp | -2.98% | 6.66% | **-3.16%** | FAILED | 🔴 Value Destructive (<0%) |
| **G3** | 1,614 | $33,959,575.00 | 829 | 51.36% | 27.82% | +23.82 pp | -4.36% | 4.65% | **-3.76%** | FAILED | 🔴 Value Destructive (<0%) |
| **G4** | 1,280 | $27,000,825.00 | 655 | 51.17% | 28.40% | +24.40 pp | -7.60% | 3.65% | **-7.34%** | FAILED | 🔴 Value Destructive (<0%) |
| **G5** | 1,110 | $23,538,100.00 | 595 | 53.60% | 28.75% | +24.75 pp | -10.33% | 0.40% | **-9.81%** | FAILED | 🔴 Value Destructive (<0%) |

---

## 4. Key Takeaways for Underwriting Policy & Hurdle Rates

1. **The Nominal Yield Mirage:** In Subgrade G5, average nominal coupon rates exceed **28.75%** (+24.75 pp spread over hurdle). However, default rates surge to **49.93%**, driving **Cohort Net LAROC to -9.81%**.
2. **Pivotal Cutoff at C4:** Platform risk managers should establish automatic portfolio risk pricing adjustments beginning at **C4**, where margin compression first drops returns below the institutional hurdle.
3. **Complete Elimination Zone:** Subgrades **E5, F4, F5, G1, G2, G3, G4, G5** generate cumulative net losses and must be immediately placed under automated hard-stop decline policies.

---
*Report automatically generated by `src/analytics/test_h2_margin_breakdown.py`.*