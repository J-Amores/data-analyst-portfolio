# Cutting Consumer Loan Losses by $230M Without Turning Away Good Borrowers
### Balancing Loss Reduction Against Lending Volume Across $19.4B in Consumer Loans

[![Live Visual Report](https://img.shields.io/badge/Live_Report-Editorial_Case_Study-2563EB?style=for-the-badge)](https://j-amores.github.io/data-analyst-portfolio/credit-risk-optimization/)
[![Interactive Simulator](https://img.shields.io/badge/Live_Tool-Underwriting_Simulator-059669?style=for-the-badge)](https://j-amores.github.io/data-analyst-portfolio/credit-risk-optimization/underwriting-simulator.html)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-334155?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Pytest Suite](https://img.shields.io/badge/Pytest-33_Passed-16A34A?style=for-the-badge&logo=pytest&logoColor=white)](tests/)

High default rates in lower credit grades and underpriced 5-year loans quietly drain hundreds of millions from our lending margins. By auditing **1,345,350 completed consumer loans ($19.4B funded)** to block high-stress subprime applications and adjust borderline Grade C4 interest rates, the platform recovers **$244.2M ($230.0M in saved write-offs plus $14.2M in rate revenue)** while keeping **96% of lending volume ($18.6B)** intact.

---

### Live Deliverables & Reports
* **[Read the Live Editorial Visual Report](https://j-amores.github.io/data-analyst-portfolio/credit-risk-optimization/)** (Full stakeholder briefing, visual charts, and 90-day rollout plan)
* **[Launch the Interactive Underwriting Simulator](https://j-amores.github.io/data-analyst-portfolio/credit-risk-optimization/underwriting-simulator.html)** (Test real borrower profiles, approval cutoffs, and rollout levels in real time)

---

## 1. Business Problem & Executive Overview

Between 2007 and 2018, LendingClub funded over 2.26 million consumer loans totaling $34B. As the platform pushed for faster growth, it approved hundreds of thousands of higher-risk borrowers in Grades D through G at 18% to 29% interest rates. On paper, those high rates looked profitable, and basic company dashboards showed a safe **12%** default rate because 912,569 newer loans ($14.6B) were still in the middle of making monthly payments.

Our Chief Risk Officer (CRO) and Head of Underwriting face a practical business decision: **which high-risk loan applications should we stop approving or reprice so we protect our profit margins without shutting down our lending volume?**

When we separated out the unfinished active loans and looked strictly at the **1,345,350 completed loans ($19.4B)**, we found that 1 in 5 borrowers actually defaulted (**20%**), and unpaid write-offs in Grades D through G were eating up the profits earned from safer borrowers:
1. **Unpaid Subprime Losses Wipe Out High Interest Rates:** Subprime Grades D through G received **28% of our lending money ($5.5B)** but caused **51% of all unpaid write-offs ($1.4B)**. Charging 18% to 29% interest was not enough when 30% to 50% of borrowers defaulted early.
2. **Where We Lose Money on Rates and Terms:** Net cash return after losses drops below our **+4.0%** profit goal at **Subgrade C4 (+3.4%)** and starts losing money at **Subgrade E5 (-1.3%)**, falling to **-9.8% in G5**. In addition, 5-year loans default twice as often as 3-year loans (**32% vs. 16%**).

### Executive Summary Grid

| The Subprime & Pricing Leak | The Fix: Targeted Cutoffs & Rates | The Upside: +$244.2M Recovered |
| :--- | :--- | :--- |
| **Subprime Grades D to G get 28% of lending money** ($5.5B) but cause 51% of all unpaid write-offs ($1.4B).<br><br>* Unfiltered reports hid risk at 12% vs. 20% true default rate.<br>* Net return drops below our +4.0% goal at Subgrade C4 (+3.4%).<br>* Subgrades E5 to G5 lose money (-1.3% down to -9.8% return). | **Decline only subprime applicants with both high debt and maxed-out cards**, and update Subgrade C4 pricing.<br><br>* Auto-decline Grades D to G when monthly debt > 25% and card usage > 65%.<br>* Add +1.5% (+150 bps) interest rate to Subgrade C4 loans.<br>* Cap 5-year terms at 680+ FICO and verify small business taxes. | **Recovers $244.2M in combined value** while keeping 96% of our lending volume ($18.6B) moving smoothly.<br><br>* Saves +$230.0M in unpaid losses (18,548 defaults prevented).<br>* Adds +$14.2M in interest revenue across 74,422 C4 loans.<br>* Lifts portfolio net return from +4.3% to +4.4% (+15 bps). |

### The 4-Question Decision Summary

| Executive Question | Finding & Recommended Action |
| :--- | :--- |
| **1. What did we find?** | Standard reports included 912,569 unfinished active loans, making default risk look like **12%**. Separating completed loans showed the true default rate is **20%** (268,599 defaults across 1.35M loans), meaning basic reports underestimated default risk by **1.7x**. |
| **2. Why is this happening?** | Higher interest rates in lower credit grades did not cover early defaults. Subprime Grades D through G took **28% of lending money ($5.5B)** but drove **51% of unpaid write-offs ($1.4B)**. Defaults spiked when borrowers had both high monthly debt (>25% DTI) and maxed-out credit cards (>65% usage), defaulting at **28% overall** and **39% in subprime**. |
| **3. What does it cost us?** | Net cash return after losses (LAROC) drops below our **+4.0%** profit hurdle starting at **Subgrade C4 (+3.4%)** and turns negative at **Subgrade E5 (-1.3%)**. In addition, 5-year loans default at double the rate of 3-year loans (32% vs. 16%), and unsecured small business loans lose money (-0.6% return). |
| **4. What should we change?** | Roll out a 3-phase underwriting update: **(Phase 1)** auto-decline Grade D through G applicants with DTI > 25% and card usage > 65%, saving **+$230.0M in net losses** (18,548 defaults prevented) while keeping **96% of lending volume ($18.6B)**; **(Phase 2)** add +1.5% (+150 bps) to Subgrade C4 rates to add **+$14.2M** and cap 5-year terms at 680+ FICO; and **(Phase 3)** verify small business tax returns and offer payment plans to late active accounts. |

---

## 2. North Star Metrics & Portfolio Guardrails

Rather than relying on vanity numbers like total loans issued or advertised interest rates, we evaluate every underwriting rule against three North Star guardrails:

```
+-----------------------------------------------------------------------------+
|                       PORTFOLIO METRIC ARCHITECTURE                         |
+-----------------------------------------------------------------------------+
|  1. NORTH STAR METRIC                                                       |
|     Net Cash Return After Losses (LAROC) -> Goal: > +4.0% Net Return        |
|                                                                             |
|  2. RISK GUARDRAIL                                                          |
|     Completed Default Rate -> Goal: Reduce below 19.3% (from 20% base)      |
|                                                                             |
|  3. BUSINESS VOLUME GUARDRAIL                                               |
|     Lending Volume Kept -> Goal: Retain >= 80% of funded lending volume     |
|                                                                             |
|  4. BORROWER RISK DRIVERS                                                   |
|     Monthly Debt (DTI), Credit Card Usage, Credit Score (FICO), Loan Term   |
+-----------------------------------------------------------------------------+
```

1. **North Star Metric - Net Cash Return After Losses (LAROC):** Measures the actual cash profit we keep per dollar lent after subtracting unpaid principal write-offs and collection agency fees:
   `LAROC = (Total Payments Received + Post-Default Recoveries - Collection Fees - Funded Loan Amount) / Funded Loan Amount`
   * **Target Hurdle:** **> +4.0%**. Any loan tier earning under 4.0% fails to cover our cost of capital and operating expenses. Across all 1.35M completed loans, our baseline return is **+4.3%** ($825.1M net profit on $19.4B lent), which rises to **+4.4%** under our new rules.
2. **Risk Guardrail - Completed Default Rate (< 19.3% Goal):** The percentage of completed loans that ended in a default or charge-off (`Defaulted Loans / Total Completed Loans`). Our Phase 1 rule brings the portfolio default rate down from **20%** (`19.96%`) to **19.0%**, clearing our 19.3% ceiling.
3. **Business Volume Guardrail - Lending Volume Kept (>= 80% Goal):** The share of historical lending dollars we keep after turning on our new decline filter (`Retained Lending Dollars / Total Historical Lending Dollars`). This ensures we never set rules so strict that we choke off loan growth. Our targeted rule keeps **96% of lending volume ($18.6B)** while declining only 3.6% of applications.

---

## 3. Key Findings & Visual Evidence

### Finding 1: Subprime Grades D to G Get 28% of Lending Money but Cause 51% of Unpaid Losses

![Figure 1: Loss Contribution Asymmetry Across Loan Grades](assets/fig1_loss_contribution.png)

When we compared where our lending dollars went against where our unpaid write-offs came from, a clear imbalance stood out. Safer borrowers in **Prime Grades A through C** received **72% of our lending capital ($13.9B across 1,009,537 loans)** and accounted for **49% of losses ($1.3B)**. Because their default rates stayed low to moderate (6% in Grade A, 13% in Grade B, and 22% in Grade C), prime borrowers generated **+$857M in net cash profit** for the platform.

In contrast, **Subprime Grades D through G** received only **28% of our lending capital ($5.5B across 335,813 loans)**, but they caused **51% of all unpaid write-offs ($1.4B)**. That is a **1.8x loss-to-lending imbalance**, meaning the profits earned from reliable prime borrowers were quietly being used to pay for subprime losses.

---

### Finding 2: Why High Interest Rates & 5-Year Terms Fail to Cover Defaults

Charging 18% to 29% interest on lower credit grades looks profitable on paper, but when 30% to 50% of those borrowers stop paying early on, we lose the original loan balance before collecting enough interest to make up for it.

| Loan Grade | Completed Loans | Funded Principal | Default Rate | Net Cash Profit / Loss | Net Return (LAROC) | Profit Goal Status (+4.0% Target) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grade A** | 235,095 | $3.26B | 6% | +$186M | **+5.7%** | Clears goal (+1.7% buffer) |
| **Grade B** | 392,748 | $5.20B | 13% | +$313M | **+6.0%** | Clears goal (+2.0% buffer) |
| **Grade C** | 381,694 | $5.41B | 22% | +$228M | **+4.2%** | Clears goal (+0.2% buffer) |
| **Grade D** | 200,966 | $3.07B | 30% | +$80M | **+2.6%** | **Misses goal (-1.4% short)** |
| **Grade E** | 93,656 | $1.65B | 38% | +$27M | **+1.6%** | **Misses goal (-2.4% short)** |
| **Grade F** | 32,059 | $611M | 45% | -$1.1M | **-0.2%** | **Loses money** |
| **Grade G** | 9,132 | $188M | 50% | -$7.6M | **-4.1%** | **Loses money** |

Looking closer at individual subgrades and loan terms reveals three specific places where we leak money:
* **Borderline Subgrade C4 Misses Our +4.0% Goal:** While Grade C overall earns +4.2%, net return drops below our +4.0% target starting at **Subgrade C4 (+3.4% return across 74,422 loans)** and **C5 (+3.1%)**. Raising interest rates by +1.5% (+150 bps) on Subgrade C4 brings its return back above +4.0% and adds **+$14.2M** in revenue.
* **Subgrades E5 to G5 Lose Money Outright:** Starting at **Subgrade E5 (-1.3% return)**, the platform loses money on average. Losses deepen through **F4 (-1.6%)** and **F5 (-2.6%)**, reaching **-9.8% in Subgrade G5** (losing $98 for every $1,000 lent).
* **5-Year Loans & Unsecured Small Business Loans:** Five-year (60-month) loans default at **32%**, double the **16%** default rate of 3-year (36-month) loans, which cuts our net return in half (**+2.6% vs. +5.1%**). Similarly, while credit card refinancing earns a strong **+5.5% return** ($4.4B lent, 17% default rate), unsecured **small business loans ($240.1M lent)** hit a **30% default rate** and lose money (**-0.6% return**) because borrowers do not have to submit tax returns to verify business income.

---

### Finding 3: Combining Monthly Debt and Credit Card Usage to Find Our Cutoff

![Figure 2: Multi-Variable Risk Interaction Heatmap](assets/fig2_risk_grid_heatmap.png)

If we simply banned all subprime loans (Grades D through G), we would lose **28% of our lending volume ($5.5B)**, breaking our **80%** volume floor and turning away $4.1B in loans that actually get paid back. 

To find a smarter cutoff that keeps good borrowers while blocking the worst defaults, we grouped all 1.35M completed loans by two everyday financial stress signals: **Monthly Debt-to-Income (DTI)** and **Credit Card Usage (Revolving Utilization)**.

When a borrower has only one stress signal, they usually manage to pay their loan: someone with high monthly debt can use an open credit card to cover a surprise car repair, and someone with high card balances can pay them down if their monthly debt is low. However, when a borrower has **both monthly debt over 25% of their income AND credit cards over 65% full**, they have no backup cushion left:
* **Low-Risk Baseline (DTI <= 15% and Card Usage <= 40%):** Defaults only **14%** of the time across 213,691 loans.
* **High-Stress Group (DTI > 25% and Card Usage > 65%):** Defaults jump to **28%** across 112,246 loans (double the low-risk rate).
* **Our Targeted Subprime Cutoff:** Inside that high-stress corner, **Grade D through G applicants default 39% of the time (47,705 loans)**. Declining only that specific subprime group removes the worst losses while leaving 96% of all applications untouched.

---

### Policy Simulation: Saving $230.0M While Keeping 96% of Lending Volume

![Figure 3: Capital Recovery Waterfall](assets/fig3_capital_waterfall.png)

Testing our Phase 1 automated decline rule and Phase 2 Subgrade C4 rate adjustment across the completed loan book shows we can capture **+$244.2M in combined value** while comfortably meeting all three of our executive guardrails:

| Rollout Scenario | Phase 1 Saved Losses | Phase 2 Rate Revenue | Total Value Created | Defaults Prevented | Lending Volume Kept |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **60% Cautious Pilot (Gradual Test)** | +$138.0M | +$8.5M | **+$146.5M** | 11,129 | 97% |
| **80% Year-1 Target (Realistic Goal)** | +$184.0M | +$11.4M | **+$195.4M** | 14,838 | 97% |
| **100% Full Automated Rule** | **+$230.0M** | **+$14.2M** | **+$244.2M** | **18,548** | **96% ($18.6B)** |

Even after subtracting the interest we give up on the performing loans inside that declined group ($24.1M in foregone interest subtracted from $254.1M in prevented gross write-offs), our net savings come out to **+$230.0M** at full rollout (or **+$184.0M** at an 80% Year-1 rollout).

---

## 4. 90-Day Rollout Plan (Phases 1 to 3)

| Rollout Phase & Timeline | What We Do | Who It Covers | Team Owner | Expected Financial Impact | Tracking Goal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Immediate**<br> | **Turn On Automated Dual-Risk Decline Filter:** Set the application filter to auto-decline Grade D to G applicants when DTI > 25% and card usage > 65%. | High-stress subprime applicants (47,705 past loans; $813M volume; 39% default rate). | **Underwriting Team** | **+$230.0M Net Losses Saved**<br>(+$184.0M at 80% rollout); prevents 18,548 defaults while keeping 96% of volume. | **Default Rate < 19.3%**<br>Volume kept >= 80%. |
| **Phase 2: Near-Term**<br> | **Update Subgrade C4 Rates & Cap 5-Year Terms:** Add +1.5% (+150 bps) interest rate to Subgrade C4 loans and require a 680+ credit score for 5-year loans. | Borderline Subgrade C4 loans (74,422 loans at +3.4% return) and subprime 5-year requests. | **Pricing Team** | **+$14.2M Interest Revenue**<br>Lifts C4 return back above +4.0% and cuts the 32% default rate on 5-year loans. | **Subgrade C4 LAROC > +4.0%**<br>5-year default rate < 25%. |
| **Phase 3: Ongoing**<br> | **Verify Small Business Taxes & Contact Late Accounts:** Require 2 years of IRS tax transcripts (Form 4506-C) for business loans and send early payment plans to accounts 16-120 days late. | Unsecured business loans ($240.1M book, 30% default rate) and 38,114 late active loans ($588.5M). | **Servicing Team** | **Stops -0.6% Small Business Loss**<br>Protects $240.1M exposure and improves recovery on late active accounts by 15%. | **Small Business Default < 20%**<br>Late loan roll rate < 3.5%. |

### Four Practical Safeguards for Implementation
1. **Clear Adverse Action Reasons for Declined Applicants:** Whenever the Phase 1 filter declines an application, the system automatically sends clear, specific credit bureau reasons (*"monthly debt obligations relative to income"* and *"revolving credit line usage"*).
2. **Subgrade C4 Conversion Monitoring:** After adding +1.5% (+150 bps) to Subgrade C4 rates, the pricing team checks application acceptance rates each month to make sure volume stays steady.
3. **3-Year Term Offer When 5-Year Requests Are Capped:** When a Grade D or E applicant with a credit score under 680 asks for a 5-year loan, the system does not reject them outright; instead, it automatically offers them a safer 3-year (36-month) loan option.
4. **Early Payment Plans at 16 Days Late:** Rather than waiting for accounts to charge off at 120+ days late, the servicing team reaches out to the 38,114 late active borrowers ($588.5M) as soon as they hit 16 days past due.

---

## 5. Data Scope, Caveats & Cleaning Pipeline

To make sure unfinished loans and formatting quirks did not skew our numbers, our cleaning script (`src/etl/clean_loans.py`) audits the raw 1.6 GB LendingClub file (`2,260,701` rows from 2007 to 2018Q4) and splits it into two separate Parquet files:

```
Raw CSV Dataset (2,260,701 rows | 1.6 GB)
         |
         v
 Step 1: Row Validation (2,260,668 valid unique loans; 33 empty footer rows removed)
         |
         v
 Step 2: Text & Type Cleaning (term -> integer months, rates -> decimals, dates -> ISO)
         |
         v
 Step 3: Separating Completed Loans from Active Loans
         |--> fct_closed_loans_seasoned.parquet (1,345,350 completed loans | 222.8 MB)
         |    [Fully Paid, Charged Off, Default -> 20% Default Rate, +4.3% LAROC]
         |
         +--> fct_active_portfolio.parquet (912,569 ongoing loans | 148.4 MB)
              [Current, Grace Period, Late 16-120 Days -> Monitored for early outreach]
```

### Data Caveats & Cleaning Log

| Check ID | Column | Reporting Trap Found in Raw Data | How We Fixed It | Why It Matters for Our Analysis |
| :--- | :--- | :--- | :--- | :--- |
| **ISS-01** | `loan_status` | 912,569 active loans were mixed with 1.35M completed loans, making the default rate look like 12% instead of 20%. | Split the dataset into two separate Parquet files (`seasoned` vs. `active`). | Prevents unfinished payment schedules from hiding the real 20% default rate. |
| **ISS-02** | `term`, `int_rate`, `revol_util` | Numbers stored as text strings with `%` signs and `' months'`. | Stripped text characters and converted to clean integers and decimal floats. | Allows us to calculate exact cash returns, rate spreads, and credit card brackets. |
| **ISS-03** | `dti` | Negative debt ratios (2 rows) and missing values (374 rows). | Added an `invalid_dti_flag` column and capped chart brackets at 100%. | Keeps corrupted values out of our debt grid without deleting valid loan records. |
| **ISS-04** | `annual_inc` | Unverified self-reported incomes up to $10M+. | Capped at the 99.5th percentile ($350,000) for income distribution checks. | Stops extreme unverified entries from skewing average borrower income. |
| **ISS-05** | `member_id` | Borrower member IDs were removed by LendingClub after 2015. | Used the unique loan `id` (100% complete) as the primary key across all tables. | Prevents broken table joins across later loan years. |

*Storage & Speed:* Converting the raw CSV (1.6 GB) into Snappy Parquet files (371.3 MB total) cut file size by **77% (4.3x smaller)** and made our Python analysis scripts run over 10x faster.

---

## 6. How to Run This Project Locally

### 1. Clone the Repo & Set Up Your Environment

```bash
# Clone the repository and navigate into the project directory
git clone https://github.com/J-Amores/data-analyst-portfolio.git
cd data-analyst-portfolio/credit-risk-optimization

# Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

*(Note: The cleaned Parquet files are included in the repository. Place `accepted_2007_to_2018Q4.csv` inside `data/raw/` only if you want to re-run the raw ETL pipeline from scratch.)*

### 2. Run the Pipeline, Tests, and Charts

```bash
# 1. Verify schema contracts and cleaned Parquet files
./.venv/bin/pytest tests/test_raw_schema.py tests/test_clean_schema.py

# 2. Run exploratory scans and segment breakdowns
./.venv/bin/python src/analytics/scan_coverage.py
./.venv/bin/python src/analytics/scan_aggregates.py
./.venv/bin/python src/analytics/scan_segments.py

# 3. Run validation hypotheses and policy simulations
./.venv/bin/python src/analytics/test_h1_loss_concentration.py
./.venv/bin/python src/analytics/test_h2_margin_breakdown.py
./.venv/bin/python src/analytics/test_h3_risk_interaction.py

# 4. Generate the 3 executive charts (assets/) and interactive simulator data cube
./.venv/bin/python src/presentation/export_figures.py
./.venv/bin/python src/presentation/export_underwriting_simulator_data.py

# 5. Build the standalone interactive underwriting simulator HTML
./.venv/bin/python src/presentation/build_underwriting_simulator_html.py

# 6. Run the full automated test suite
./.venv/bin/pytest -v

# 7. View the visual report and interactive underwriting simulator
open index.html
open underwriting-simulator.html
```