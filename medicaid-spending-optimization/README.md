# Hospital Outpatient Pharmacy Spend Optimization
### 5-Year Claims Review and Formulary Action Plan (2020 to 2024)

[![Presentation](https://img.shields.io/badge/Presentation-7_Slide_Executive_Deck-0F172A.svg)](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/)
[![Decision Tool](https://img.shields.io/badge/Interactive_Tool-Formulary_Decision_Cockpit-059669.svg)](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/dashboard.html)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg)](https://www.python.org/)
[![Parquet](https://img.shields.io/badge/Data-Apache_Parquet-2B579A.svg)](https://parquet.apache.org/)

> **Executive Summary:** Across an **\$85.0M** hospital outpatient pharmacy budget, medication acquisition costs rose **45.6%** between 2020 and 2024 while bundled insurance reimbursement rates stayed flat. Our review identified **\$3.2M in annual operating margin** that the hospital can recover (\$2.56M at an 80% Year 1 target) by locking generic orders to primary contracted suppliers (**\$2.1M**) and turning on automatic generic substitution in the EHR (**\$1.1M**), while keeping chronic patient therapy changes at **1.8%** (well below our 2.5% safety limit).

| Project Deliverable | Purpose | Direct Link |
| :--- | :--- | :--- |
| **1. Executive Slide Deck** | 7-slide presentation covering where the budget goes, what drove cost growth, and our three recommendations. | [View Presentation (`index.html`)](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/) |
| **2. Operational Decision Tool** | Interactive web tool to test generic adoption targets (50% to 100%) and export target medication lists. | [Launch Decision Tool (`dashboard.html`)](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/dashboard.html) |
| **3. Analysis Scripts** | Data cleaning and analysis scripts in Python (`src/etl` and `src/analytics`). | [Browse Code (`src/`)](src/) |

---

## 1. Business Context and Leadership Directive

Between 2020 and 2024, regional hospitals operated on tight 1% to 3% margins. While outpatient reimbursement rates stayed fixed under insurer fee schedules and bundled care contracts, wholesale medication costs climbed steadily.

Our Director of Pharmacy, Chief Financial Officer (CFO), and Pharmacy and Therapeutics (P&T) Committee asked our team to review five years of outpatient and discharge prescription claims. Their directive was straightforward: find out why medication spending kept rising and build a practical plan to recover operating margin without disrupting patient care.

Hospital leadership needed answers to three blind spots:
1. **Unclear spending drivers:** Leadership could not confirm whether budget overruns came from higher patient prescription volume or manufacturer price hikes.
2. **Brand medication leakage:** Outpatient clinics and discharge pharmacies routinely dispensed expensive brand-name medications even when FDA-approved, bioequivalent generics were sitting in hospital inventory.
3. **Price gaps across generic suppliers:** Without consistent tracking across our Group Purchasing Organization (GPO) agreements, buyers regularly paid 35% to 70% more across competing manufacturers for the exact same generic pill.

---

## 2. Core Metrics and Clinical Guardrails

Before looking for cost cuts, we established three core rules with the Pharmacy Director and Chief Medical Officer to define how we measure savings, how we protect patients on long-term medications, and how we filter out billing errors:

1. **Avoidable Brand-to-Generic Spend (Our Primary Savings Target):**
   Whenever the hospital dispenses an expensive brand-name drug that already has an FDA-approved generic equivalent, or buys a generic pill from a high-priced supplier when a cheaper contracted option is available, we calculate the price gap multiplied by the number of doses dispensed. Tracking this across drug classes and suppliers gives the Pharmacy Director and CFO an exact dollar figure for how much recoverable money the hospital left on the table each year.
2. **Patient Therapy Disruption Rate (Our 2.5% Clinical Safety Limit):**
   Saving money cannot come at the expense of patient stability, especially for patients managing chronic conditions like diabetes, epilepsy, or psychiatric care. We tracked the share of chronic prescriptions affected by our proposed changes and set a strict **2.5% ceiling** on adjustments to medications with fewer than two alternative options. Across our proposed plan, chronic therapy changes stay at **1.8%**, and doctors always keep a one-click override when a specific brand is medically necessary.
3. **Packaging and Billing Error Rate (Our 5.0% Data Quality Limit):**
   Pharmacy claims occasionally contain unit-of-measure mix-ups, such as billing a 200-puff inhaler box as 1 unit on one invoice and 200 individual puffs on another. If left unchecked, those billing quirks make unit prices look artificially high and inflate savings estimates. We flagged these abnormal records so they make up less than **5.0%** of our projected savings (currently **2.1%**) and routed them to pharmacy buyers to verify packaging before updating any contracts.

| Metric | What It Measures | Target / Safety Limit | Lead Owner |
| :--- | :--- | :--- | :--- |
| **1. Avoidable Brand-to-Generic Spend** | Annual overpayment from dispensing off-patent brands or higher-priced generics | **\$3.2M** addressable (\$2.56M at 80% rollout) | Director of Pharmacy & CFO |
| **2. Patient Therapy Disruption Rate** | Share of chronic care prescriptions impacted with fewer than 2 alternatives | **Must stay < 2.5%** (Modeled at **1.8%**) | Chief Medical Officer & P&T Chair |
| **3. Packaging & Billing Error Rate** | Share of projected savings coming from flagged unit-of-measure anomalies | **Must stay < 5.0%** (Modeled at **2.1%**) | Pharmacy Purchasing & Inventory Lead |

---

## 3. Data Sources and Preparation

To model five years of hospital pharmacy purchasing from 2020 to 2024, we used outpatient drug spending and clinical reference files from the Centers for Medicare & Medicaid Services (CMS), scaled to an \$85M hospital pharmacy budget. Our data preparation script ([`clean_pipeline.py`](src/etl/clean_pipeline.py)) combines two main files: a five-year spending table that tracks drug prices, prescription counts, and manufacturers, and a clinical reference table that explains what each medication treats.

Before running the analysis, we fixed four data issues in the raw files that would otherwise skew hospital savings estimates:

1. **Separating drug totals from manufacturer rows (preventing double counting):**
   The raw files list an "Overall" summary row for each medication right alongside the individual rows for each manufacturer that makes it. Adding the spending column up directly counts every dollar twice. We split the data into two separate files: one for overall drug trends and one for comparing manufacturer prices.
2. **Leaving privacy-redacted counts blank (fewer than 11 prescriptions):**
   To protect patient privacy under HIPAA, the government hides numbers whenever a drug had fewer than 11 prescriptions in a given year. Instead of filling those blanks with zeros, which makes five-year growth rates look artificially explosive, we left them blank so they would not distort our growth trends.
3. **Filtering out unit-of-measure billing mix-ups:**
   Some records are flagged for billing unit errors, such as when a pharmacy bills a 200-puff inhaler box as 1 unit on one claim and 200 individual puffs on another. We excluded these flagged rows when ranking generic savings targets and added a toggle in the dashboard so buyers can review them separately.
4. **Excluding long-acting injectables from pill comparisons:**
   Some medications share the same active ingredient name across very different delivery forms, such as a monthly injectable shot (`Maintena` or `Sublocade`) versus a daily generic pill. We excluded long-acting injectables and implants from our generic price comparisons so oral tablets are only compared against oral tablets.

---

## 4. Key Findings

| Area Reviewed | Analysis Script | Key Finding |
| :--- | :--- | :--- |
| **1. Budget Concentration** | [`test_h1_capital_allocation.py`](src/analytics/test_h1_capital_allocation.py) | **72.2% (\$61.35M)** of the drug budget goes to just **5% of medications** (239 drugs), with **32.2%** in the top 25 drugs alone. |
| **2. Five-Year Growth Drivers** | [`test_h2_decomposition.py`](src/analytics/test_h2_decomposition.py) | Cost surges split between **unit price hikes on older brands** (23.9% of high-growth drugs) and **rising prescription demand for newer treatments** (76.1%). |
| **3. Generic Price Spread** | [`test_h3_price_spread.py`](src/analytics/test_h3_price_spread.py) | Competing manufacturers charge a **71.6% typical price spread** for identical generic drugs, creating a **\$3.2M** savings opportunity. |

### Finding 1: Most of the budget goes to a small group of medications

![Hospital Pharmacy Spend Flow](assets/medicaid_spend_sankey.png)

As shown in [`test_h1_capital_allocation.py`](src/analytics/test_h1_capital_allocation.py) and the interactive Sankey chart in `index.html`, mapping 2024 spending across nearly 4,800 medications revealed that costs are heavily concentrated at the top:
* Just **5% of medications** (239 drugs) take up **72.2% (\$61.35M)** of the hospital's entire outpatient drug budget.
* Expanding to the **top 10% of medications** covers **84.9% (\$72.17M)** of total spend, leaving the remaining 90% of routine generic medications (over 4,200 drugs) at just **15.1%**.
* A single list of **25 medications** accounts for **32.2% (\$27.33M)** of the entire pharmacy budget, led by **Humira**, **Ozempic**, **Biktarvy**, **Jardiance**, and **Trulicity**.

Broad budget cuts across thousands of cheap floor-stock generics create headaches for nurses and doctors without helping operating margins. Formulary reviews should focus on these top 25 high-cost medications.

### Finding 2: Two distinct forces drove our five-year spending growth
As shown in [`test_h2_decomposition.py`](src/analytics/test_h2_decomposition.py), tracking over 3,700 medications from 2020 to 2024 showed over 1,200 drugs whose total spend grew by more than 50%, driven by two different patterns:
* **Price hikes on established drugs (23.9% of high-growth drugs):** On older brand and specialty drugs, manufacturers raised unit prices even when prescription volume stayed flat or fell. Key examples include **Xifaxan** (74% of spend growth from price hikes), **Emflaza** (66% from price hikes), **Trulicity** (unit price up 107%), **Enbrel** (56% from price hikes), **Cosentyx** (55% from price hikes), and **Vyvanse** (unit price rose 37% while volume dropped 15%).
* **Higher patient demand for newer treatments (76.1% of high-growth drugs):** Newer diabetes and immunology treatments grew because doctors prescribed them to far more patients. **Ozempic** prescriptions grew **929%**, **Jardiance** prescriptions grew **257%**, and **Dupixent** prescriptions grew over **130-fold**.

Hospital leadership cannot use the same rule for both groups. High-demand drugs like Ozempic and Dupixent need clinical order checks in Epic or Cerner to confirm first-line treatments were tried first, while older drugs with steep price hikes like Enbrel and Vyvanse should be switched to generic or biosimilar options.

### Finding 3: Paying different prices for the same generic drug costs the hospital \$3.2M
As shown in [`test_h3_price_spread.py`](src/analytics/test_h3_price_spread.py), there was a price spread of **71.6%** between higher-cost and lower-cost manufacturers (75th vs. 25th percentile) across over 1,350 generic medications with at least two approved suppliers. Nearly two-thirds (65.8%) of these multi-source generic drugs showed a price gap greater than **35%** (after excluding long-acting injectables so oral tablets were only compared against oral tablets).

When pharmacy buyers order stock without locking in our primary contracted supplier, or when discharge pharmacies dispense off-patent brands like **Vyvanse** and **Concerta**, the hospital pays a steep markup for the identical active ingredient. Across these medications, we identified **\$3.89M** in annual overpayment. Capturing a realistic **82%** conversion rate through primary supplier contract locks (**\$2.1M**) and automatic generic substitution (**\$1.1M**) recovers **\$3.2M** in annual operating margin.

---

## 5. Hospital Action Plan

Our proposed plan includes three recommendations to recover **\$3.2M** in annual operating margin while keeping chronic therapy changes at **1.8%** (well below our 2.5% safety limit):

1. **Lock in primary GPO generic suppliers (\$2.1M annual savings):**
   Direct the **Pharmacy Purchasing team** to lock wholesaler ordering profiles to our 25th-percentile contracted generic manufacturers across the 1,350+ multi-source generic drugs where prices vary by more than 35%. Because this happens in the purchasing system for chemically identical generics, it requires zero physician workflow changes and can be tracked through monthly contract compliance audits (target >95% within 30 days).
2. **Turn on automatic generic substitution in the EHR (\$1.1M annual savings):**
   Partner with the **Director of Pharmacy and Clinical Informatics** to enable automatic therapeutic interchange at order entry for off-patent brands that already have FDA-approved generic equivalents in stock, starting with **Vyvanse** (\$472K), **Concerta** (\$367K), **Spiriva Respimat** (\$176K), **Advair Diskus** (\$136K), and **Suboxone**. Clinicians keep a one-click "Dispense as Written" override when a brand is medically necessary, and progress is tracked via our Generic Dispensing Rate (target >93% within 60 days).
3. **Update Epic and Cerner order sets for high-cost specialty drugs (12% to 18% cost growth reduction):**
   Work with the **P&T Committee Chair and Chief Medical Officer** to split management of our top 25 budget drivers based on what drove their cost growth. For volume-driven medications like **Ozempic** and **Dupixent**, add an EHR check confirming first-line treatments were tried first. For mature brands raising unit prices on flat volume like **Enbrel** and **Trulicity**, guide prescribers toward lower-cost biosimilar or therapeutic alternatives.

| Recommendation | Target Medications | Lead Team | Expected Annual Impact | Success Metric |
| :--- | :--- | :--- | :--- | :--- |
| **1. Primary Generic Supplier Locks** | Multi-source generics with 2+ approved suppliers | Pharmacy Purchasing Buyer | **\$2.1M margin recovery** | GPO Contract Compliance (>95%) |
| **2. Automatic EHR Generic Substitution** | Off-patent brands (`Vyvanse`, `Concerta`, `Spiriva`, `Advair`, `Suboxone`) | Pharmacy Director & Clinical Informatics | **\$1.1M brand overpayment recovery** | Generic Dispensing Rate (>93%) |
| **3. Specialty & GLP-1 Order Sets** | High-growth specialty lines (`Ozempic`, `Dupixent`, `Enbrel`, `Trulicity`) | P&T Committee Chair & CMO | **12% to 18% cost growth reduction** | First-Line Guideline Adherence (%) |

### Expected Recovery by Adoption Rate
Because hospital purchasing and prescribing changes happen in phases, we modeled three adoption tiers in our [Operational Decision Cockpit](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/dashboard.html):
* **60% Conservative Adoption:** Recovers **\$1.92M** in annual margin if clinical and purchasing rollout is gradual.
* **80% Target Adoption:** Recovers **\$2.56M** in Year 1 (primary budget target for the Pharmacy Director and CFO).
* **100% Full Adoption:** Recovers the full **\$3.20M** addressable opportunity.

---

## 6. Interactive Decision Tools

To help pharmacy leadership explore the data and test rollout assumptions directly, the repository includes two web tools:
* **Executive Presentation Deck (`index.html`):** A 7-slide visual walkthrough built for asynchronous review by hospital directors and hiring managers.
* **Operational Decision Cockpit (`dashboard.html` and `src/dashboard/app.py`):** An interactive scenario planner where pharmacy buyers and P&T committee members can adjust generic adoption sliders (50% to 100%), filter by therapeutic class, toggle flagged billing outliers, and export target medication lists to CSV.

---

## 7. Operational Assumptions and Scope Boundaries

* **Wholesale Acquisition Costs vs. Net Rebates:** The underlying CMS claims reflect gross pharmacy payments before confidential manufacturer rebates or 340B discounts. Modeled savings represent baseline acquisition cost reductions captured directly at purchasing and order entry.
* **Identical Dosage Form Matching:** All modeled generic substitutions compare matching delivery forms (oral tablets to oral tablets, inhalers to inhalers) with FDA bioequivalence ratings.
* **Clinician Override Protection:** Every automated EHR substitution rule retains a one-click physician override when a specific brand formulation is clinically required for a patient.

---

## 8. Repository Structure

```text
medicaid-spending-optimization/
├── assets/                               # Exported Sankey flow and chart images
├── data/
│   ├── raw/                              # Source CMS drug spending and clinical reference files
│   └── cleaned/                          # Cleaned, split Apache Parquet datasets
├── src/
│   ├── etl/
│   │   └── clean_pipeline.py             # Data preparation, row splitting, and cleaning script
│   ├── analytics/
│   │   ├── test_h1_capital_allocation.py # Spend concentration and Sankey flow analysis
│   │   ├── test_h2_decomposition.py      # 5-year price vs. volume growth analysis
│   │   └── test_h3_price_spread.py       # Multi-source generic price spread analysis
│   └── dashboard/
│       └── app.py                        # Streamlit decision cockpit application
├── index.html                            # 7-Slide Executive Briefing Deck (GitHub Pages)
├── dashboard.html                        # Standalone Operational Decision Cockpit
├── requirements.txt                      # Python 3.11 package dependencies
└── README.md                             # Project overview and methodology
```

---

## 9. Local Setup Guide

```bash
# 1. Clone the repository
git clone https://github.com/J-Amores/data-analyst-portfolio.git
cd data-analyst-portfolio/medicaid-spending-optimization

# 2. Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the data preparation and analysis scripts
python src/etl/clean_pipeline.py
python src/analytics/test_h1_capital_allocation.py
python src/analytics/test_h2_decomposition.py
python src/analytics/test_h3_price_spread.py

# 5. Launch the Streamlit dashboard locally
streamlit run src/dashboard/app.py
```
