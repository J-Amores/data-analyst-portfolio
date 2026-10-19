# Project Charter: Consumer Credit Risk & Underwriting Optimization (LendingClub Originated Book)

## 1. Executive Context & Business Problem
*   **Executive Stakeholders:** Chief Risk Officer (CRO), VP of Credit Underwriting Policy, and Credit Risk Committee[cite: 2, 6].
*   **Business Mandate:** Consumer lending institutions and fintech balance sheets operate under strict loss-provisioning capital requirements while pursuing originations growth[cite: 2, 6]. Credit leadership faces an acute operational blind spot:
    1. Leadership struggles to balance **origination volume expansion** against **terminal credit loss leakage**; top-line gross interest yield from subprime tiers (Grades D through G) creates an illusion of profitability that masks catastrophic principal write-offs[cite: 2, 6].
    2. Underwriting models suffer from "subprime adverse selection," where high-interest rate tiers experience delinquency roll rates that outstrip the pricing premium, generating an active net margin drag on the balance sheet[cite: 2, 6].
    3. The Credit Risk Committee requires defensible, empirical risk thresholds to establish automated hard-stops on toxic borrower segments, re-price vulnerable risk tiers, and protect institutional Return on Capital without choking off prime lending volume[cite: 2, 6].

---

## 2. The READY Framework Foundation
*   **R – Representative Data:** Official LendingClub loan performance dataset covering seasoned multi-year origination vintages (over 1.5 million records, multi-billion-dollar funded principal volume, tracking loan status, actual cash repayments, debt-to-income ratios, revolving credit utilization, FICO bands, and loss recoveries)[cite: 2, 24].
*   **E – Exec-Driven Questions:**
    *   Which borrower risk segments and loan grades account for the top 70% of cumulative net charge-offs[cite: 2, 6, 13]?
    *   In which subprime loan tiers does nominal interest income fail to cover principal write-offs, resulting in a negative net loss-adjusted yield[cite: 2, 6, 13]?
    *   What specific multi-variable underwriting cutoffs (combining Debt-to-Income and Revolving Credit Utilization) maximize default reduction while preserving at least 80% of originated book capacity[cite: 2, 6, 13]?
*   **A – Analytical Frameworks:** SCAN Exploratory Data Analysis[cite: 2, 20], Mature Vintage Seasoning Cohort Analysis[cite: 2, 15], Loss-Adjusted Return on Capital (LAROC) Modeling[cite: 2, 6], and DASH Interactive Delivery[cite: 2, 21].
*   **D – Data Best Practices:** Strict isolation of closed, mature loans (`loan_status IN ('Fully Paid', 'Charged Off', 'Default')`) to eliminate right-censoring bias from active loans[cite: 2, 10]; clean casting of terms, interest rates, and employment length; and separation of raw from cleaned feature layers.
*   **Y – Your Insights & Impact:** Direct delivery of an Executive Underwriting Policy Matrix (P0–P2) quantifying addressable capital recovery and default prevention while retaining prime conversion capacity[cite: 2, 6].

---

## 3. Metrics Architecture

```
                               ┌──────────────────────────────────────────────┐
                               │              NORTH STAR METRIC               │
                               │          Loss-Adjusted Return on             │
                               │          Originated Capital (LAROC)          │
                               └──────────────────────┬───────────────────────┘
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
       ┌───────────────────────────────┐                             ┌───────────────────────────────┐
       │      GUARDRAIL METRIC 1       │                             │      GUARDRAIL METRIC 2       │
       │    Cumulative Terminal Bad    │                             │  Origination Volume Capacity  │
       │     Loan Rate (< 14.0%)       │                             │      Retention (≥ 80.0%)      │
       └───────────────────────────────┘                             └───────────────────────────────┘
```

### North Star Metric
*   **Metric Name:** Loss-Adjusted Return on Originated Capital (LAROC)[cite: 2, 6, 14]
*   **Technical Definition:**
    $$\text{LAROC} = \left( \frac{\text{Total Principal Received} + \text{Total Interest Received} + \text{Recoveries} - \text{Funded Principal}}{\text{Funded Principal}} \right) \times 100$$
*   **Plain-English Definition:** The net cash profit generated per dollar of funded loan principal after subtracting all credit default losses and principal write-offs, demonstrating true portfolio profitability rather than gross interest illusions[cite: 2, 6, 14].
*   **Executive Owner:** Chief Risk Officer (CRO) / Head of Portfolio Management[cite: 2, 6].

### Guardrail Metric 1 (Credit Risk / Solvency)
*   **Metric Name:** Cumulative Terminal Bad Loan / Charge-Off Rate[cite: 2, 6]
*   **Technical Definition:**
    $$\text{Terminal Bad Loan Rate} = \left( \frac{\sum \text{Loans with Status in } (\text{'Charged Off'}, \text{'Default'})}{\sum \text{Closed Loans in } (\text{'Fully Paid'}, \text{'Charged Off'}, \text{'Default'})} \right) \times 100$$
*   **Threshold / Guardrail:** Must remain **$< 14.0\%$** across the aggregate portfolio to ensure compliance with institutional credit loss reserves and institutional investor return hurdles[cite: 2, 6].
*   **Executive Owner:** VP of Credit Underwriting Policy[cite: 2, 6].

### Guardrail Metric 2 (Commercial Growth / Volume Capacity)
*   **Metric Name:** Origination Volume Capacity Retention Rate[cite: 2, 6]
*   **Technical Definition:**
    $$\text{Volume Retention Rate} = \left( \frac{\text{Funded Principal of Retained Policy Segments}}{\text{Total Historical Funded Principal}} \right) \times 100$$
*   **Threshold / Guardrail:** Must remain **$\ge 80.0\%$** of total applicant book capacity, ensuring underwriting tightening eliminates bad debt without starving the enterprise of revenue-generating loan originations[cite: 2, 6].
*   **Executive Owner:** VP of Consumer Lending Growth[cite: 2, 6].

---

## 4. Testable Executive Hypotheses

| Hypothesis ID | Statement | Null Hypothesis ($H_0$) | Analytical Test & Decision Threshold | Executive Action if Supported |
| :--- | :--- | :--- | :--- | :--- |
| **H1: Loss Concentration**[cite: 2, 6] | **Pareto Risk Asymmetry:** Over 65% of total cumulative net charge-off dollars are concentrated in subprime tiers (Grades D through G), despite these grades accounting for less than 30% of total originated capital[cite: 2, 6]. | Cumulative net charge-offs are uniformly distributed across loan grades; Grades D–G account for $\le 35\%$ of total portfolio write-offs[cite: 2]. | Lorenz Curve / Gini coefficient decomposition of total net charge-offs by Loan Grade and Subgrade. Threshold: Cumulative write-off share $> 65\%$ at Grade D cutoff ($p < 0.001$)[cite: 2, 6]. | Restructure underwriting criteria to introduce automated rejection triggers on bottom-tier subgrades (F and G)[cite: 2, 6]. |
| **H2: Net Margin Breakdown**[cite: 2, 6] | **Nominal Spread Illusion:** For loans in Grades D and E, higher gross interest rates fail to compensate for credit losses, resulting in a negative net LAROC and creating a margin drag that subsidizes subprime losses with prime yields[cite: 2, 6]. | Net LAROC across Grades D and E is equal to or greater than the platform cost of capital ($+4.0\%$)[cite: 2]. | Segment-level cash flow reconciliation: $(\text{Total Payments} + \text{Recoveries} - \text{Funded Principal}) / \text{Funded Principal}$. Two-sample Welch’s t-test comparing LAROC of Grade C vs. Grade D ($p < 0.01$)[cite: 2]. | Cease originations in specific subgrade cells exhibiting negative net yield; reallocate lending liquidity to prime Grade B/C consolidation loans[cite: 2, 6]. |
| **H3: Multi-Variable Risk Interaction**[cite: 2, 6] | **Non-Linear Default Multiplication:** The interaction between elevated Debt-to-Income ($\text{DTI} > 25\%$) and high Revolving Utilization ($\text{Revol\_Util} > 65\%$) causes terminal default rates to spike non-linearly ($> 2.2\times$ baseline), creating an addressable elimination target[cite: 2, 6]. | Default rates for borrowers with $\text{DTI} > 25\%$ and $\text{Revol\_Util} > 65\%$ do not significantly exceed the additive baseline risk ($p \ge 0.05$)[cite: 2]. | Chi-Square Test of Independence and 2D Risk Grid cross-tabulation across DTI brackets ($\le 15\%$, $15\text{--}25\%$, $> 25\%$) and Utilization tiers ($\le 40\%$, $40\text{--}65\%$, $> 65\%$). Threshold: Relative Risk ratio $> 2.0$[cite: 2, 6]. | Establish an automated hard-stop policy: reject any applicant where DTI $> 25\%$ and Revolving Line Utilization $> 65\%$ regardless of self-reported income[cite: 2, 6]. |