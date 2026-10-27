Project Charter: Medicaid Outpatient Drug Spend Optimization & Formulary Stewardship (CY2020–CY2024)
1. Executive Context & Business Problem
Executive Stakeholders: State Medicaid Pharmacy Director, Chief Medical Officer (CMO), and Pharmacy & Therapeutics (P&T) Formulary Committee.
Business Mandate: State Medicaid programs operate under strict statutory annual budget caps while outpatient prescription drug expenditures continue to surge nationwide. Pharmacy leadership faces an acute executive blind spot:
Leadership cannot easily discern whether annual spending spikes are driven by utilization expansion (legitimate epidemiological need and claim volume growth) or unit cost escalation (monopolistic manufacturer price increases and brand-to-generic pricing wedges).
Formularies experience significant "generic substitution leakage," where higher-cost brand drugs or premium single-source manufacturers are reimbursed despite equivalent multi-source generic alternatives being available on the market.
Leadership requires actionable, defensible targeting to revise Preferred Drug Lists (PDLs), mandate step-therapy protocols, and negotiate state supplemental rebates ahead of the upcoming benefit fiscal cycle.
2. The READY Framework Foundation
R – Representative Data: Official CMS Medicaid Drug Spending dataset covering benefit years 2020–2024 (over 5 years of longitudinal outpatient reimbursement data across brand, generic, and manufacturer levels, totaling millions of claims and tens of billions of dollars in taxpayer reimbursements).
E – Exec-Driven Questions:
Which therapeutic drug classes and manufacturer monopolies account for the top 80% of net Medicaid budget growth from 2020 to 2024?
How much annual spend is driven strictly by price inflation (CAGR_Avg_Spnd_Per_Dsg_Unt_20_24) versus claim volume growth (Tot_Clms)?
Where does multi-source manufacturer competition fail to reduce unit prices, presenting an immediate opportunity for Maximum Allowable Cost (MAC) state price caps?
A – Analytical Frameworks: SCAN Exploratory Data Analysis, Price-Volume Growth Decomposition, Multi-Source Manufacturer Price Dispersion Modeling, and DASH Interactive Delivery.
D – Data Best Practices: Fully reproducible ETL pipeline, isolation of CMS suppression boundaries (<11 claims), separation of raw and cleaned layers, and rigorous prevention of hierarchical double-counting (Mftr_Name == 'Overall').
Y – Your Insights & Impact: Direct delivery of a prioritized Formulary Action Plan quantifying addressable dollar savings across step-therapy and generic substitution tiers.
3. Metrics Architecture
                               ┌──────────────────────────────────────────────┐
                               │              NORTH STAR METRIC               │
                               │   Annual Avoidable Brand-to-Generic Spend    │
                               │       Wedge ($ Addressable Savings)          │
                               └──────────────────────┬───────────────────────┘
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
       ┌───────────────────────────────┐                             ┌───────────────────────────────┐
       │      GUARDRAIL METRIC 1       │                             │      GUARDRAIL METRIC 2       │
       │  Formulary Access & Clinical  │                             │  Outlier Distortion & Data    │
       │    Disruption Rate (< 2.5%)   │                             │    Reliability Index (< 5.0%) │
       └───────────────────────────────┘                             └───────────────────────────────┘
North Star Metric
Metric Name: Annual Avoidable Brand-to-Generic Spend Wedge ($ Addressable Savings)
Technical Definition:$$\text{Avoidable Spend Wedge} = \sum_{i \in \text{Multi-Source Drugs}} \left( \text{Avg_Spnd_Per_Dsg_Unt_Wghtd}_{\text{Brand}, i} - \min_{m} (\text{Avg_Spnd_Per_Dsg_Unt_Wghtd}_{\text{Generic}, m, i}) \right) \times \text{Tot_Dsg_Unts}_{\text{Brand}, i}$$
Plain-English Definition: The exact dollar amount Medicaid overpays by reimbursing higher-cost brand medications when bioequivalent generic equivalents from verified manufacturers were actively dispensed in the same benefit year.
National-to-Hospital Scaling Bridge: National CMS RY2026 outpatient drug claims ($111.28B across 4,774 formulations, up +45.61% / +$34.85B from $76.42B in CY2020) are normalized by a 0.076386% health system scaling factor ($85.0M / $111.28B) to model a representative $85.0M regional hospital outpatient pharmacy budget. The clean depot-filtered brand-to-generic spend wedge is $5.09B nationally ($5,086,071,053.40) across non-outlier oral/inhaler formulations ($7.27B national / $5.56M hospital before depot filtering), which scales to $3.89M ($3,885,064) at the hospital level and yields $3.2M in net recoverable operating margin at an 82.4% target formulary capture rate.
Executive Owner: State Medicaid Pharmacy Director / Chief Medical Officer / Hospital Pharmacy Director.
Guardrail Metric 1 (Clinical / Patient Access)
Metric Name: Formulary Access & Clinical Disruption Rate
Technical Definition: Percentage of total Medicaid claims (Tot_Clms) in chronic disease therapeutic categories (e.g., Antidiabetic, Antipsychotic, Anticonvulsant) where aggressive tier-shifting or prior-authorization restrictions would impact regimens with fewer than two FDA-approved therapeutic alternatives.
Threshold / Guardrail: Must remain $< 2.5%$ of total chronic claims (modeled at 1.8%) to prevent administrative provider burden, therapy abandonment, or adverse clinical events.
Guardrail Metric 2 (Data Integrity / Budget Risk)
Metric Name: Outlier Distortion & Data Reliability Index
Technical Definition: Percentage of targeted savings derived from records flagged with Outlier_Flag == 1 (CMS IQR outlier boundary violations: spending difference $> 10%$ and $> $1.00$ per unit). Across the catalog, 1,738 of 4,774 formulations (36.41% of lines, representing $9.08B / 8.16% of gross spend) are flagged, accounting for 5.07% of the raw brand-to-generic spend wedge ($388.5M of $7.66B).
Threshold / Guardrail: Must remain $< 5.0%$ of total projected fiscal savings. Filtering flagged records drops outlier distortion in modeled savings from 5.07% to 0.00% (strictly meeting the Guardrail 2 ceiling).
4. Testable Executive Hypotheses
Hypothesis ID
Statement
Null Hypothesis ($H_0$)
Analytical Test & Decision Threshold
Executive Action if Supported
H1: Cost Concentration
Pareto Budget Asymmetry & Capital Flow: The top 5% of formulations (239 drugs) drive 72.18% ($80.31B national / $61.35M hospital) of total CY2024 gross spend (Gini = 0.9028, Chi-Square p < 0.001). The top 10% (478 drugs) account for 84.90% ($94.48B national / $72.17M hospital), leaving the bottom 90% of routine maintenance generics (4,296 drugs) at just 15.10%. The top 25 individual drugs (0.5% of lines) account for 32.15% ($35.78B national / $27.33M hospital), led by Humira(Cf) Pen ($3.45B), Ozempic ($3.41B), Biktarvy ($3.22B), Jardiance ($2.24B), and Trulicity ($2.17B).
Drug spending is uniformly distributed; top 5% of drug entities account for $\le 25%$ of gross program reimbursement.
Cumulative distribution function (Lorenz Curve / Gini = 0.9028 / Sankey Flow) of Tot_Spndng_2024. Threshold: Cumulative share $> 60%$ at the 95th percentile rank (Observed: 72.18%, KS p < 0.001).
Restructure clinical reviews to focus negotiation, structured order sets, and prior authorizations on the top 25 budget-draining entities.
H2: Spend Driver Decomposition
Dual-Track Logarithmic Price-Volume Growth Engines: Across 3,765 complete longitudinal formulations (2020 to 2024), 1,210 formulations grew >50% in gross spend. Structural growth bifurcates into two distinct cohorts:
- Cohort A (Manufacturer Price-Inflation Drivers, 23.9% of high-growth lines / 289 drugs): Unit price hikes drove majority of log spend growth: Xifaxan (74.1% price-driven), Emflaza (66.0% price-driven), Trulicity (+264.9% spend growth driven by a +106.6% unit cost surge; 56.1% price-led), Enbrel Sureclick (55.6% price-led), Cosentyx (55.1% price-led), Vyvanse (+36.6% unit price vs. -14.8% volume).
- Cohort B (Epidemiological Volume Drivers, 76.1% of high-growth lines / 921 drugs): Rapid clinical adoption led by Ozempic (+1,143.0% spend surge driven by +928.7% prescription claim growth from 322K to 3.31M fills; -25.5% unit cost/mL), Jardiance (+385.6% spend growth; +256.7% claims), Dupixent Pen (+13,082.5% claims).
Unit cost CAGR contributes $\le 50%$ of overall expenditure growth across top-accelerating drug categories uniformly.
Logarithmic decomposition of expenditure: $\ln(\Delta Spend) = \ln(\Delta Price) + \ln(\Delta Quantity)$. Paired Wilcoxon and Student's t-test comparing price vs. volume contributions.
Deploy dual formulary governance: enforce manufacturer price caps and mandatory substitution on Cohort A; implement clinical step-therapy and indication prior authorization on Cohort B.
H3: Multi-Source Price Wedge
Generic Dispersion & State MAC / Hospital Recovery: Across 1,358 multi-manufacturer molecules (Tot_Mftr >= 2), the median interquartile price spread (P75 - P25) / P25 across competing labelers is 71.55% (65.76% of multi-source molecules exceed the 35% price spread threshold, K-S test p < 0.001). Clean depot-filtered brand-to-generic spend wedge yields $5.09B national / $3.89M hospital gross wedge, unlocking $3.2M in net recoverable operating margin at an 82.4% target formulary capture rate.
Manufacturer unit price variance within multi-source generics is $\le 10%$ ($p \ge 0.05$).
Two-sample Kolmogorov-Smirnov test of manufacturer unit prices; Wilcoxon signed-rank test against 35% threshold; calculation of State MAC price ceiling savings and hospital formulary recovery.
Implement mandatory State MAC price ceilings at 25th percentile of multi-source manufacturer cost; turn on automated EHR generic substitution across top non-outlier leakage targets (Vyvanse, Concerta, Spiriva Respimat, Advair Diskus, Banzel, Jornay PM).