# John Amores | Data Analyst Portfolio

[![Live Portfolio Hub](https://img.shields.io/badge/Live%20Portfolio%20Hub-j--amores.github.io-111111?style=for-the-badge)](https://j-amores.github.io/data-analyst-portfolio/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQL & Parquet](https://img.shields.io/badge/Storage-SQL%20%7C%20Parquet-166534?style=for-the-badge)](https://github.com/J-Amores/data-analyst-portfolio)
[![Pytest Suite](https://img.shields.io/badge/Pytest-166%20Passed%20(100%25)-B45309?style=for-the-badge)](https://github.com/J-Amores/data-analyst-portfolio)

Data Analyst specializing in turning large, messy operational datasets into clear financial decisions, stakeholder-ready case studies, and interactive decision simulators.

Every project in this repository is built around a real leadership decision, governed by North Star metrics and safety guardrails, and structured in two layers:
1. **Stakeholder Deliverables (1-Click Live Web Apps):** Publication-grade editorial case studies and interactive scenario simulators built for non-technical executives.
2. **Reproducible Analytics Pipelines:** Clean ETL pipelines, multi-table Apache Parquet storage, hypothesis validation scripts, and 166 automated `pytest` checks.

**Explore the Interactive Portfolio Hub:** **[https://j-amores.github.io/data-analyst-portfolio/](https://j-amores.github.io/data-analyst-portfolio/)**

---

## Featured Case Studies & Interactive Simulators

| Domain & Stakeholder | Case Study & Business Mandate | Quantified Impact & Guardrails | One-Click Deliverables |
| :--- | :--- | :--- | :--- |
| **Fintech & Credit Risk**<br>*(Chief Risk Officer & Underwriting)* | **Consumer Credit Risk & Underwriting Optimization**<br>Audited **1.35M completed loans (\$19.4B)** after separating 912K unfinished active accounts (unmasking a **20%** true default rate vs. **12%** unfiltered) to stop subprime losses. | **+\$244.2M Annual Value**<br>• **+\$230.0M** saved loan write-offs<br>• **+\$14.2M** Subgrade C4 repricing<br>• **96%** of lending volume kept | • **[Read Case Study](https://j-amores.github.io/data-analyst-portfolio/credit-risk-optimization/)**<br>• **[Launch Underwriting Simulator](https://j-amores.github.io/data-analyst-portfolio/credit-risk-optimization/underwriting-simulator.html)**<br>• **[View Code & README](./credit-risk-optimization/)** |
| **Healthcare Operations**<br>*(Hospital Pharmacy Director & CFO)* | **Outpatient Pharmacy Drug Spend Optimization**<br>Audited **4,774 medications (\$85M hospital budget / \$111B CMS benchmark)** to separate manufacturer price hikes from patient volume growth and cap wholesale generic markups. | **+\$3.2M Annual Savings**<br>• **+\$1.1M** auto-generic switch (6 brands)<br>• **+\$2.1M** wholesale supplier caps<br>• **98%** of prescriptions untouched | • **[Read Case Study](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/)**<br>• **[Launch Cost Simulator](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/cost-simulator.html)**<br>• **[View Code & README](./medicaid-spending-optimization/)** |
| **E-Commerce & Retail**<br>*(VP of Merchandising & Growth)* | **Online Store Basket Size & Product Bundle Engine**<br>Audited **541,909 order lines (19,773 clean orders / £10.2M sales)**, preserving **25%** guest checkouts and isolating **£897K (9%)** in returns to grow 1-to-5 item carts. | **+£25K Net Bundle Profit**<br>• **65% to 84%** natural attach rates<br>• **6x to 37x** pairing multipliers<br>• **Under 2%** bundle return rate | • **[Read Case Study](https://j-amores.github.io/data-analyst-portfolio/market-basket-analysis/)**<br>• **[Launch Bundle Builder](https://j-amores.github.io/data-analyst-portfolio/market-basket-analysis/bundle-builder.html)**<br>• **[View Code & README](./market-basket-analysis/)** |
| **Growth & Marketing CRM**<br>*(VP of Growth & Call Center Ops)* | **Outbound Bank Marketing & Call Fatigue Optimization**<br>Audited **41,188 prospects and 105,754 outbound calls** to eliminate wasted repeat dialing (calls 4 to 56 eat **48%** of dials for **12%** of sign-ups) and prioritize high-odds leads. | **+3,200+ New Deposits (+70%)**<br>• **475 talk hours** (28K to 51K calls) saved<br>• **88%** of baseline sign-ups kept<br>• Cuts rep time from **38 to 22 min/sale** | • **[Read Case Study](https://j-amores.github.io/data-analyst-portfolio/bank-marketing-crm/)**<br>• **[Launch Lead Qualifier](https://j-amores.github.io/data-analyst-portfolio/bank-marketing-crm/lead-qualifier.html)**<br>• **[View Code & README](./bank-marketing-crm/)** |

---

## Executive Summaries by Case Study

### 1. Consumer Credit Risk & Underwriting Optimization ([`credit-risk-optimization/`](./credit-risk-optimization/))
* **Business Problem:** Subprime Grades D through G take up **28%** of lending capital (**\$5.5B**) but drive **51%** of all unpaid loan write-offs (**\$1.4B**). Meanwhile, standard reporting mixed 912,569 unfinished active loans into the total book, making a **20%** true completed default rate look like a safe **12%**.
* **Key Finding:** Defaults jump to **39%** when subprime borrowers carry both a Debt-to-Income (DTI) ratio above **25%** and credit card utilization above **65%**. In addition, borderline Subgrade C4 loans earn **+3.4%** net return after losses (LAROC), missing the credit committee's **+4.0%** profit hurdle, while 5-year loans default at double the rate of 3-year loans (**32% vs. 16%**).
* **90-Day Recommendation:** Turn on an automated decline rule for Grade D to G applicants with DTI > 25% and Card Usage > 65% (**Phase 1:** prevents 18,548 defaults and saves **+\$230.0M** while keeping **96%** of loan volume), add **+1.5%** (+150 bps) interest to Subgrade C4 loans and cap 5-year terms (**Phase 2:** adds **+\$14.2M** in interest revenue), and require tax verification on small business applications (**Phase 3**).

### 2. Outpatient Pharmacy Drug Spend Optimization ([`medicaid-spending-optimization/`](./medicaid-spending-optimization/))
* **Business Problem:** Outpatient drug spending rose **46%** over five years, with just **5%** of medications (239 drugs) consuming **72% (\$61M)** of an **\$85M** regional hospital pharmacy budget. Brand-name drugs cost **19x more** per prescription than generics (**\$408 vs. \$22**), and wholesale prices for identical generics vary by a median of **72%**.
* **Key Finding:** Separating 5-year manufacturer price hikes from patient volume growth across 3,762 complete drugs proved that 88 of the top 100 growing drugs expanded because doctors treated more patients (such as Ozempic and Jardiance), while 46 older brand drugs spiked purely from price hikes on flat or falling volume.
* **90-Day Recommendation:** Turn on automatic generic substitution in e-prescribing for 6 off-patent habit brands (Vyvanse, Concerta, Spiriva Respimat, Advair Diskus, Banzel, Jornay PM) to save **+\$1.1M/year** (**Phase 1**), lock wholesale generic contracts to 25th-percentile low-cost suppliers across 1,358 generics to save **+\$2.1M/year** (**Phase 2**), and run quarterly price-spike audits (**Phase 3**) while keeping **98%** of routine prescriptions untouched.

### 3. Online Store Basket Size & Product Bundle Engine ([`market-basket-analysis/`](./market-basket-analysis/))
* **Business Problem:** Across **19,773 completed orders (£10.2M sales)**, large wholesale baskets (6+ items) generate **87%** of store revenue (**£322** median order value), while **22%** of checkouts (4,354 carts) leave with only 1 to 5 items (**£58 to £141** median order value) because product pages lack cross-sell prompts. At the same time, customer returns and cancellations drain **£897K (9% of gross sales)**.
* **Key Finding:** Preserving **135,080 guest checkout lines (25% of shopping carts)** and screening out high-return products uncovered 5 matching product collections (Regency Teaware, Jumbo Storage Bags, Bakelike Alarm Clocks, Lunch Bags, and Wooden Picture Frames) that shoppers naturally buy together **65% to 84%** of the time (**6x to 37x** more often than random chance) with return rates **under 2%**.
* **90-Day Recommendation:** Launch 1-click "Complete the Set" bundle boxes with a 10% bundle discount on the top 5 product sets (**Phase 1:** **+£3K** net annual profit after discount giveback), add a checkout-drawer cross-sell prompt for 1-to-2 item carts (**Phase 2:** **+£4K** net profit), and offer pre-packed Q4 holiday wholesale cases for European gift shops (**Phase 3:** **+£25K** net profit).

### 4. Outbound Bank Marketing & Call Fatigue Optimization ([`bank-marketing-crm/`](./bank-marketing-crm/))
* **Business Problem:** Across **105,754 outbound phone calls** made to **41,188 bank prospects**, overall term-deposit sign-ups sit at **11% (4,640 deposits)**. However, call attempts 1 through 3 bring in **88%** of all deposits, while repeat attempts 4 through 56 burn **48% of all phone dials (50,949 calls / 475 hours of agent talk time)** for just **12%** of sign-ups.
* **Key Finding:** More than half of all outbound calls (**53%**) go to 31-to-45-year-olds (who convert at just **9%**) and **36%** go to home landlines (**5%** conversion). Meanwhile, seniors over 60 (**45%** conversion), students (**31%**), mobile phones (**15%**), and past buyers called back within 7 days (**66%**) are heavily under-dialed.
* **90-Day Recommendation:** Cap outbound outreach at 3 calls per prospect (**Phase 1:** saves **28K to 51K calls** and **475 talk hours** while keeping **88%** of sign-ups), route calls to mobile numbers first and call past buyers within 7 days (**Phase 2**), and redirect saved calls to seniors, students, and low-rate months using our pre-call lead checklist to add **over 3K new deposits (+1,535 to +3,242 net gain, or +33% to +70%)** with existing staff (**Phase 3**).

---

## Analytical Workflow & Core Competencies

* **Decision-Driven Framing:** Every analysis starts by defining the executive decision, North Star metric, and operational guardrails so recommendations never violate business or clinical constraints.
* **Data Hygiene & Caveat Isolation:** Preventing real-world reporting traps before modeling, including active-loan survival bias (`12%` vs. `20%` default rate), duplicate summary lines (`$223B` vs. `$111B`), HIPAA `<11` privacy blanks, guest checkout deletions (`25%` of orders), and post-call duration leakage.
* **Technical Stack:** Python (`pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`), SQL, Apache Parquet, Pytest (`166` automated checks), HTML/CSS/JS interactive decision simulators, and Git.

---

## Repository Architecture & Local Quickstart

```text
data-analyst-portfolio/
├── index.html                          # Interactive Portfolio Hub Landing Page
├── README.md                           # Master Portfolio Overview
├── credit-risk-optimization/           # Case Study 1: Consumer Credit Risk (+\$244.2M)
│   ├── index.html                      # Editorial Case Study Report
│   ├── underwriting-simulator.html     # Interactive Underwriting Simulator
│   ├── README.md                       # Technical Documentation & Findings
│   ├── src/                            # ETL, Analytics & 300 DPI Chart Scripts
│   └── tests/                          # 33 Automated Pytest Checks
├── medicaid-spending-optimization/     # Case Study 2: Hospital Pharmacy Spend (+\$3.2M)
│   ├── index.html                      # Editorial Case Study Report
│   ├── cost-simulator.html             # Interactive Pharmacy Cost Simulator
│   ├── README.md                       # Technical Documentation & Findings
│   ├── src/                            # ETL, Analytics & 300 DPI Chart Scripts
│   └── tests/                          # 55 Automated Pytest Checks
├── market-basket-analysis/             # Case Study 3: E-Commerce Bundling (+£25K)
│   ├── index.html                      # Editorial Case Study Report
│   ├── bundle-builder.html             # Interactive Bundle Builder Workbench
│   ├── README.md                       # Technical Documentation & Findings
│   ├── src/                            # ETL, Analytics & 300 DPI Chart Scripts
│   └── tests/                          # 32 Automated Pytest Checks
└── bank-marketing-crm/                 # Case Study 4: Outbound Call Center CRM (+3K+ Deposits)
    ├── index.html                      # Editorial Case Study Report
    ├── lead-qualifier.html             # Interactive Call Cap & Lead Qualifier Simulator
    ├── README.md                       # Technical Documentation & Findings
    ├── src/                            # ETL, Analytics & 300 DPI Chart Scripts
    └── tests/                          # 46 Automated Pytest Checks
```

### Running the Test Suites Locally

```bash
# Clone the monorepo
git clone https://github.com/J-Amores/data-analyst-portfolio.git
cd data-analyst-portfolio

# Run automated verification suites across all 4 case studies (166 total tests)
for dir in credit-risk-optimization medicaid-spending-optimization market-basket-analysis bank-marketing-crm; do
  echo "=== Testing \$dir ==="
  (cd "\$dir" && ./.venv/bin/pytest -v)
done
```
