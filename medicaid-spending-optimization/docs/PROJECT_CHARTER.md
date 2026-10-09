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
Technical Definition:$$\text{Avoidable Spend Wedge} = \sum_{i \in \text{Multi-Source Drugs}} \left( \text{Avg_Spnd_Per_Dsg_Unt_Wghtd}{\text{Brand}, i} - \min{m} (\text{Avg_Spnd_Per_Dsg_Unt_Wghtd}{\text{Generic}, m, i}) \right) \times \text{Tot_Dsg_Unts}{\text{Brand}, i}$$
Plain-English Definition: The exact dollar amount Medicaid overpays by reimbursing higher-cost brand medications when bioequivalent generic equivalents from verified manufacturers were actively dispensed in the same benefit year.
Executive Owner: State Medicaid Pharmacy Director / PBM Contract Negotiator.
Guardrail Metric 1 (Clinical / Patient Access)
Metric Name: Formulary Access & Clinical Disruption Rate
Technical Definition: Percentage of total Medicaid claims (Tot_Clms) in chronic disease therapeutic categories (e.g., Antidiabetic, Antipsychotic, Anticonvulsant) where aggressive tier-shifting or prior-authorization restrictions would impact regimens with fewer than two FDA-approved therapeutic alternatives.
Threshold / Guardrail: Must remain $< 2.5%$ of total chronic claims to prevent administrative provider burden, therapy abandonment, or adverse clinical events.
Guardrail Metric 2 (Data Integrity / Budget Risk)
Metric Name: Outlier Distortion & Data Reliability Index
Technical Definition: Percentage of targeted savings derived from records flagged with Outlier_Flag == 1 (CMS IQR outlier boundary violations: spending difference $> 10%$ and $> $1.00$ per unit).
Threshold / Guardrail: Must remain $< 5.0%$ of total projected fiscal savings. Any policy decision involving outlier-flagged records must undergo individual NDC-level review to prevent false-positive budget forecasts caused by dosage reporting anomalies (e.g., milliliter vs. each discrepancies).
4. Testable Executive Hypotheses
Hypothesis ID
Statement
Null Hypothesis ($H_0$)
Analytical Test & Decision Threshold
Executive Action if Supported
H1: Cost Concentration
Pareto Budget Asymmetry: Over 65% of total CY2024 gross Medicaid drug spending is concentrated within the top 5% of distinct drug entities, primarily driven by specialty biologics and GLP-1 antidiabetics.
Drug spending is uniformly distributed; top 5% of drug entities account for $\le 25%$ of gross program reimbursement.
Cumulative distribution function (Lorenz Curve / Gini Coefficient) of Tot_Spndng_2024. Threshold: Cumulative share $> 60%$ at the 95th percentile rank.
Restructure clinical reviews to focus negotiation and prior authorizations on the top 25 budget-draining entities.
H2: Spend Driver Decomposition
Price Gouging vs. Volume: For drugs exhibiting $> 50%$ net spending growth between 2020 and 2024, unit cost inflation (CAGR_Avg_Spnd_Per_Dsg_Unt_20_24) accounts for $> 70%$ of spending expansion, while claim volume growth (Tot_Clms) accounts for $< 30%$.
Unit cost CAGR contributes $\le 50%$ of overall expenditure growth across top-accelerating drug categories.
Logarithmic decomposition of expenditure: $\ln(\Delta Spend) = \ln(\Delta Price) + \ln(\Delta Quantity)$. Welch’s t-test comparing price contribution vs. quantity contribution ($p < 0.01$).
Refer top price-inflating manufacturers to the State Attorney General / Legislative Oversight Committee for anti-competitive pricing scrutiny.
H3: Multi-Source Price Wedge
Generic Substitution Wedge: In multi-manufacturer generic markets (Tot_Mftr \ge 2), the average price dispersion between the 75th percentile and 25th percentile manufacturer unit price exceeds 35%, generating $> $100\text{M}$ in state-wide avoidable spread.
Manufacturer unit price variance within multi-source generics is $\le 10%$ ($p \ge 0.05$).
Two-sample Kolmogorov-Smirnov test of manufacturer unit prices; calculation of State Maximum Allowable Cost (MAC) ceiling savings.
Implement mandatory State MAC price ceilings at the 25th percentile of multi-source manufacturer cost.