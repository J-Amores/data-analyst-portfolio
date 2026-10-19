# Data Specification & Quality Engineering: LendingClub Consumer Loan Portfolio
# ==============================================================================
# docs/DATA_SPEC.md
# ==============================================================================

## 1. Data Grain & Architecture Overview
[Framework: Decision-Driven Design][cite: 3, 4]

The analytical asset originates from the longitudinal LendingClub accepted loan performance records (2007–2018Q4), comprising approximately 2.26 million borrower records and over \$30B in cumulative funded principal.

*   **Primary Physical Grain:** 1 row = 1 funded loan origination (`id` / `loan_id`)[cite: 4, 6].
*   **Analytical Split Architecture:** To avoid survival and right-censoring bias, the ETL pipeline splits the raw ingestion table into two dedicated analytical views:
    1.  `fct_closed_loans_seasoned`: Contains strictly mature originations with definitive terminal resolution (`loan_status IN ('Fully Paid', 'Charged Off', 'Default')`)[cite: 4, 6]. This serves as the single source of truth for default rate baselines, risk grid cross-tabulations, and loss-adjusted return calculations[cite: 4, 6].
    2.  `fct_active_portfolio`: Contains ongoing loans (`loan_status IN ('Current', 'In Grace Period', 'Late (16-30 days)', 'Late (31-120 days)')`)[cite: 4]. Used exclusively for monitoring total active capital exposure and near-term delinquency roll rates[cite: 4, 6].

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          raw_lendingclub_accepted                           │
│                          (2.26M Origination Rows)                           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                   Filter by Terminal Status Resolution
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│     fct_closed_loans_seasoned        │  │       fct_active_portfolio        │
│   (~1.35M Rows: Fully Paid / Default)│  │   (~890K Rows: Current / Late)    │
├──────────────────────────────────────┤  ├───────────────────────────────────┤
│ • Terminal Bad Loan Rate             │  │ • Active Capital at Risk          │
│ • Loss-Adjusted Return (LAROC)       │  │ • 30-Day / 60-Day Roll Tracking   │
│ • Underwriting Risk Grids & Rules    │  │ • Pipeline Exposure Monitoring    │
└──────────────────────────────────────┘  └───────────────────────────────────┘
```

---

## 2. Column Definitions & Physical Schema
[Principle: 4-Layer Metric Standard][cite: 4, 6]

### Core Entity Identifiers & Dimensions
*   `id` (VARCHAR(64), Non-Null, Primary Key): Unique platform-assigned loan origination identifier[cite: 4].
*   `member_id` (VARCHAR(64), Nullable): Unique borrower account identifier (anonymized/suppressed in later vintages)[cite: 4].
*   `issue_d` (DATE, Non-Null): Month and year the loan was funded and originated[cite: 4].
*   `grade` (CHAR(1), Non-Null): LendingClub assigned proprietary risk tier (`A` through `G`)[cite: 4].
*   `sub_grade` (CHAR(2), Non-Null): Granular subgrade breakdown (`A1` through `G5`)[cite: 4].
*   `term` (INT64, Non-Null): Amortization term length in months (`36` or `60`)[cite: 4].
*   `purpose` (VARCHAR(32), Non-Null): Self-reported primary loan reason (`debt_consolidation`, `credit_card`, `home_improvement`, `small_business`, `major_purchase`, `medical`, etc.)[cite: 4].
*   `home_ownership` (VARCHAR(16), Non-Null): Residential status (`RENT`, `OWN`, `MORTGAGE`, `OTHER`)[cite: 4].
*   `verification_status` (VARCHAR(32), Non-Null): Income validation level (`Not Verified`, `Source Verified`, `Verified`)[cite: 4].
*   `addr_state` (CHAR(2), Non-Null): Two-letter US postal state code[cite: 4].

### Underwriting Risk Attributes
*   `int_rate` (DECIMAL(6,4), Non-Null, $\ge 0.0500$): Borrower interest rate as a numeric decimal (e.g., `0.1349` for 13.49%)[cite: 4].
*   `installment` (DECIMAL(10,2), Non-Null, $> 0.00$): Required monthly payment amount[cite: 4].
*   `annual_inc` (DECIMAL(12,2), Non-Null, $> 0.00$): Self-reported annual income[cite: 4].
*   `dti` (DECIMAL(6,2), Nullable): Debt-to-income ratio calculated as $\frac{\text{Monthly Non-Mortgage Debt Obligations}}{\text{Monthly Gross Income}} \times 100$[cite: 4].
*   `fico_range_low` (INT64, Non-Null, $[300, 850]$): Lower bound of borrower's FICO score range at origination[cite: 4].
*   `fico_range_high` (INT64, Non-Null, $[300, 850]$): Upper bound of borrower's FICO score range at origination[cite: 4].
*   `revol_bal` (DECIMAL(12,2), Non-Null, $\ge 0.00$): Total active revolving credit balance[cite: 4].
*   `revol_util` (DECIMAL(6,4), Nullable): Revolving credit utilization rate expressed as a numeric decimal ($[0.0000, 1.0000+]$)[cite: 4].
*   `open_acc` (INT64, Non-Null, $\ge 0$): Number of open credit lines on borrower's credit profile[cite: 4].
*   `total_acc` (INT64, Non-Null, $\ge 0$): Total credit lines ever recorded on credit profile[cite: 4].
*   `delinq_2yrs` (INT64, Non-Null, $\ge 0$): Count of 30+ day delinquencies in the past 24 months[cite: 4].
*   `inq_last_6mths` (INT64, Non-Null, $\ge 0$): Count of hard credit inquiries in the past 6 months (excluding auto and mortgage)[cite: 4].
*   `pub_rec` (INT64, Non-Null, $\ge 0$): Number of derogatory public records (bankruptcies, tax liens)[cite: 4].

### Financial Performance & Cash Flow Measures
*   `loan_amnt` (DECIMAL(10,2), Non-Null, $> 0.00$): Total loan amount requested[cite: 4].
*   `funded_amnt` (DECIMAL(10,2), Non-Null, $> 0.00$): Total principal amount funded by investors[cite: 4].
*   `loan_status` (VARCHAR(32), Non-Null): Terminal or active loan outcome (`Fully Paid`, `Charged Off`, `Default`, `Current`, `Late (31-120 days)`, `Late (16-30 days)`, `In Grace Period`)[cite: 4].
*   `total_pymnt` (DECIMAL(12,2), Non-Null, $\ge 0.00$): Total gross cash payments received to date (principal + interest + late fees)[cite: 4].
*   `total_rec_prncp` (DECIMAL(12,2), Non-Null, $\ge 0.00$): Cumulative principal repaid[cite: 4].
*   `total_rec_int` (DECIMAL(12,2), Non-Null, $\ge 0.00$): Cumulative interest received[cite: 4].
*   `recoveries` (DECIMAL(12,2), Non-Null, $\ge 0.00$): Post-charge-off gross cash recoveries collected through debt collection agencies[cite: 4].
*   `collection_recovery_fee` (DECIMAL(10,2), Non-Null, $\ge 0.00$): Third-party collection fees deducted from recoveries[cite: 4].

---

## 3. Data Cleaning Pipeline: The CLEAN Framework Implementation
[Framework: CLEAN][cite: 4, 6]

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            THE CLEAN FRAMEWORK                              │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ C - Conceptualize   │ Establish grain, measures, dimensions, critical cols  │
│ L - Locate Solvable │ Clean strings, parse dates, cast types, deduplicate   │
│ E - Evaluate Hard   │ Right-censoring, missing DTIs, platform recovery fees │
│ A - Augment Data    │ LAROC, bad loan flag, FICO midpoint, risk brackets    │
│ N - Note & Document │ Change logs, magnitude benchmarks, policy exceptions  │
└─────────────────────┴───────────────────────────────────────────────────────┘
```

### C – Conceptualize the Data
*   **Grain Integrity:** Verify that each row represents a distinct loan origination (`id` uniqueness = 100%)[cite: 4, 6].
*   **Critical vs. Non-Critical Columns:**
    *   *Critical Columns ($> 98\%$ completeness required):* `loan_amnt`, `funded_amnt`, `term`, `int_rate`, `grade`, `loan_status`, `issue_d`, `total_pymnt`, `total_rec_prncp`, `fico_range_low`, `fico_range_high`[cite: 4, 6].
    *   *Non-Critical / Secondary:* `emp_title`, `title`, `desc`, `next_pymnt_d`, `hardship_type`[cite: 4].

### L – Locate Solvable Issues
1.  **String Sanitization and Type Coercion:**
    *   `term`: Strip leading whitespace and text (`' 36 months'` $\rightarrow$ `36`, `' 60 months'` $\rightarrow$ `60` as INT64)[cite: 4].
    *   `int_rate` & `revol_util`: Strip trailing `%` symbols and divide by 100 to cast as numeric decimals (e.g., `'13.49%'` $\rightarrow$ `0.1349`)[cite: 4].
    *   `emp_length`: Map ordinal text to integer years:
        $$\text{emp\_length} = \begin{cases} 0 & \text{if } \text{emp\_length} \in (\text{'< 1 year'}, \text{'<1 year'}) \\ 10 & \text{if } \text{emp\_length} = \text{'10+ years'} \\ k & \text{for } k \in [1, 9] \\ \text{NULL} & \text{if missing or } \text{'n/a'} \end{cases}$$[cite: 4]
2.  **Date Normalization:**
    *   Convert `issue_d`, `last_pymnt_d`, and `earliest_cr_line` from `MMM-YYYY` strings (e.g., `'Dec-2015'`) into standard ISO format (`YYYY-MM-01`)[cite: 4, 6].
3.  **Deduplication Harness:**
    *   Assert uniqueness on `id`. Drop duplicate header artifacts or re-indexed Kaggle rows where `funded_amnt` is null or zero[cite: 4, 6].

### E – Evaluate Unsolvable Issues
1.  **Right-Censoring & Vintage Maturity Bias:**
    *   *Phenomenon:* `loan_status == 'Current'` accounts for ~38% of total rows in the unsegmented table[cite: 4]. Computing default rates across active loans introduces severe survival bias, artificially diluting the aggregate default rate to ~7.4%[cite: 4].
    *   *Handling Policy:* Segregate all open loans (`Current`, `Late`, `Grace Period`) into `fct_active_portfolio`[cite: 4]. **All default rate and LAROC underwriting policies must be calibrated exclusively on `fct_closed_loans_seasoned` (`loan_status IN ('Fully Paid', 'Charged Off', 'Default')`)**[cite: 4, 6].
2.  **Missing and Anomalous Debt-to-Income (DTI) Ratios:**
    *   *Phenomenon:* Approximately 0.08% of records contain null DTIs or extreme values ($> 100\%$ or negative values)[cite: 4, 6].
    *   *Handling Policy:* Do NOT impute with cohort averages (which skews risk underwriting)[cite: 4, 6]. Cap valid DTIs at $100.0\%$ for risk binning; isolate records where $\text{dti} < 0$ or null with an audit flag `invalid_dti_flag = 1` and exclude them from DTI cross-tabulations[cite: 4, 6].
3.  **Self-Reported Annual Income Outliers:**
    *   *Phenomenon:* Self-reported income contains extreme outliers (e.g., annual incomes of $10M+) and zero-income records[cite: 4, 6].
    *   *Handling Policy:* Retain original entries in the data store, but winsorize annual income at the 99.5th percentile for distribution modeling[cite: 4, 6]. Flag `annual_inc == 0` records with `zero_income_flag = 1`[cite: 4, 6].
4.  **Investor Servicing Fee Accounting:**
    *   *Phenomenon:* LendingClub charges a 1.00% servicing fee on borrower principal payments that is unrecorded in the borrower-level payment columns[cite: 4].
    *   *Handling Policy:* Scope explicitly in executive methodology notes[cite: 4, 6]. Cash flow formulas reflect gross borrower cash yield; note an institutional net-yield adjustment of $-100 \text{ bps}$ across portfolio projections[cite: 4, 6].

### A – Augment the Data (Engineered Analytical Features)
1.  `is_bad_loan` (INT64, Allowed: $\{0, 1\}$):
    $$\text{is\_bad\_loan} = \begin{cases} 1 & \text{if } \text{loan\_status} \in (\text{'Charged Off'}, \text{'Default'}) \\ 0 & \text{if } \text{loan\_status} = \text{'Fully Paid'} \\ \text{NULL} & \text{otherwise} \end{cases}$$[cite: 4]
2.  `net_cash_flow` (DECIMAL(12,2)):
    $$\text{net\_cash\_flow} = \text{total\_pymnt} + \text{recoveries} - \text{collection\_recovery\_fee} - \text{funded\_amnt}$$[cite: 4]
3.  `laroc` (DECIMAL(8,4)): Loss-Adjusted Return on Originated Capital:
    $$\text{laroc} = \left( \frac{\text{net\_cash\_flow}}{\text{funded\_amnt}} \right) \times 100$$[cite: 4]
4.  `fico_midpoint` (FLOAT64):
    $$\text{fico\_midpoint} = \frac{\text{fico\_range\_low} + \text{fico\_range\_high}}{2}$$[cite: 4]
5.  `vintage_year` (INT64): Extracted year of origination:
    $$\text{vintage\_year} = \text{EXTRACT}(\text{YEAR FROM } \text{issue\_d})$$[cite: 4]
6.  `dti_bracket` (VARCHAR(16)): Categorical risk tier:
    $$\text{dti\_bracket} = \begin{cases} \text{'1. Low (<=15%)'} & \text{if } \text{dti} \le 15.0 \\ \text{'2. Moderate (15-25%)'} & \text{if } \text{dti} > 15.0 \text{ and } \text{dti} \le 25.0 \\ \text{'3. High (25-35%)'} & \text{if } \text{dti} > 25.0 \text{ and } \text{dti} \le 35.0 \\ \text{'4. Severe (>35%)'} & \text{if } \text{dti} > 35.0 \end{cases}$$[cite: 4]
7.  `revol_util_bracket` (VARCHAR(16)): Categorical liquidity pressure tier:
    $$\text{revol\_util\_bracket} = \begin{cases} \text{'1. Conservative (<=40%)'} & \text{if } \text{revol\_util} \le 0.40 \\ \text{'2. Moderate (40-65%)'} & \text{if } \text{revol\_util} > 0.40 \text{ and } \text{revol\_util} \le 0.65 \\ \text{'3. High (65-85%)'} & \text{if } \text{revol\_util} > 0.65 \text{ and } \text{revol\_util} \le 0.85 \\ \text{'4. Maxed (>85%)'} & \text{if } \text{revol\_util} > 0.85 \end{cases}$$[cite: 4]

### N – Note and Document (The Production Issues Log)
[Principle: Production Issues Log][cite: 4, 6]

| Issue ID | Column / Feature | Detected Anomaly | Severity & Magnitude | Final Resolution Strategy | Downstream Impact on Analysis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ISS-01**[cite: 4, 6] | `loan_status` | Active loans (`Current`, `Late`) mixed with mature loans[cite: 4]. | ~38% of total table records[cite: 4]. | Forked into two physical views: `fct_closed_loans_seasoned` vs. `fct_active_portfolio`[cite: 4]. | Prevents survival bias; unmasks true ~20% default rate on mature cohorts[cite: 4]. |
| **ISS-02**[cite: 4, 6] | `term`, `int_rate`, `revol_util` | Numeric measures stored as formatted text strings (`%`, `months`)[cite: 4]. | 100% of rows for these three critical columns[cite: 4]. | Regex parsing and decimal float conversion in the ETL pipeline (`strip('%') / 100`)[cite: 4]. | Enables mathematical aggregation and rate spread calculations[cite: 4]. |
| **ISS-03**[cite: 4, 6] | `dti` | Missing and extreme ratio entries ($> 100\%$ or negative)[cite: 4]. | ~0.08% of total records[cite: 4]. | Filtered negative values; capped visual brackets at 100%; tagged invalid rows as null[cite: 4]. | Prevents regression leverage distortion without dropping valid originations[cite: 4, 6]. |
| **ISS-04**[cite: 4, 6] | `emp_length` | Missing values and non-standard string bounds (`< 1 year`, `10+ years`)[cite: 4]. | ~5.8% null entries[cite: 4]. | Transformed to integer years with null preserved as `'Unemployed / Unknown'`[cite: 4]. | Allows segmented stability modeling without fabricating tenure data[cite: 4, 6]. |
| **ISS-05**[cite: 4, 6] | `member_id` | Field completely suppressed by LendingClub in post-2015 vintages[cite: 4]. | ~55% missing across full longitudinal span[cite: 4]. | Switched primary entity foreign key to `id` exclusively[cite: 4]. | Eliminates broken join keys across longitudinal tables[cite: 4, 6]. |