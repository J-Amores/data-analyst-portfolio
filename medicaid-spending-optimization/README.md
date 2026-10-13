# Hospital Outpatient Pharmacy Spend Optimization
### Executive Briefing and Technical Methodology

[![Presentation](https://img.shields.io/badge/Presentation-Interactive_Slide_Deck-blue.svg)](https://j-amores.github.io/data-analyst-portfolio/medicaid-spending-optimization/)
[![Tool](https://img.shields.io/badge/Tool-Operational_Cockpit-059669.svg)](dashboard.html)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg)](https://www.python.org/)
[![Storage](https://img.shields.io/badge/Storage-Apache_Parquet-2B579A.svg)](https://parquet.apache.org/)

---

## 1. Executive summary and leadership directive

Between 2020 and 2024, regional hospitals faced tight operating margins, often hovering between 1% and 3%. While outpatient reimbursement rates stayed flat under insurer fee schedules and bundled care models, wholesale medication costs rose steadily.

Our pharmacy director and chief financial officer asked our team to review five years of outpatient and discharge prescription claims. Their directive was direct: pinpoint why medication spending kept climbing and build a practical formulary plan to recover operating margin without disrupting patient care.

Hospital leadership faced three main blind spots:
1. Unclear spending drivers: Leadership could not confirm whether budget overruns came from higher patient volume (more discharge scripts and clinic visits) or manufacturer price hikes.
2. Brand medication leakage: Outpatient clinics and discharge pharmacies often dispensed expensive brand-name medications even when bioequivalent, AB-rated generics were available in hospital stock.
3. Price differences across generic suppliers: Without contract tracking across our group purchasing organization (GPO) agreements, the hospital routinely absorbed price differences over 35% between manufacturers for the same generic molecule.

```text
+----------------------------------------------------------------------------------------+
| DELIVERABLE DIRECTORY                                                                  |
+--------------------------------+-------------------------------------------------------+
| 1. Executive Presentation Deck │ 7-slide briefing on GitHub Pages                      |
|    (index.html)                │ https://j-amores.github.io/data-analyst-portfolio/... │
+--------------------------------+-------------------------------------------------------+
| 2. Operational Decision Tool   │ Interactive web tool with scenario sliders            |
|    (dashboard.html)            │ Runs directly in the browser                          |
+--------------------------------+-------------------------------------------------------+
| 3. Technical Pipeline          │ ETL pipeline and statistical models                   |
|    (src/ directory)            │ Modular Python scripts (src/etl, src/analytics)       |
+--------------------------------+-------------------------------------------------------+
```

Across an $85M hospital outpatient pharmacy budget, this analysis identified $3.2M in annual operating margin that the hospital can recoup. The plan combines automated generic substitution rules with tighter compliance on primary contracted generic suppliers, while keeping chronic therapy changes at 1.8% (well below our 2.5% safety limit).

---

## 2. Core metrics and clinical guardrails

To keep the analysis tied directly to hospital margin recovery, all work tracks a single primary metric guarded by two operational safety checks:

```text
                               +----------------------------------------------+
                               |              PRIMARY METRIC                  |
                               |   Annual Avoidable Brand-to-Generic Spend    |
                               |          ($3.2M Addressable Margin)          |
                               +----------------------┬-----------------------+
                                                      |
                       +------------------------------┴------------------------------+
                       |                                                             |
                       v                                                             v
       +-------------------------------+                             +-------------------------------+
       |      CLINICAL GUARDRAIL       |                             |       DATA RELIABILITY        |
       |  Formulary Access Disruption  |                             |  Packaging and Billing Unit   |
       |     Rate (Must Stay < 2.5%)   |                             |   Discrepancy Index (< 5.0%)  |
       +-------------------------------+                             +-------------------------------+
```

### Primary metric: annual avoidable brand-to-generic spend
* Calculation: The total annual dollar difference between what the hospital spent on multi-source brand medications and what those orders would cost at the lowest contracted generic price:
  $$\text{Avoidable Spend} = \sum_{i \in \text{Multi-Source}} \left( \text{Cost}_{\text{Brand}, i} - \min_{m} (\text{Cost}_{\text{Generic}, m, i}) \right) \times \text{Dispensed Units}_{\text{Brand}, i}$$
* Business alignment: Measures recoverable margin dollars to guide Pharmacy and Therapeutics (P&T) Committee decisions and wholesaler contract negotiations. Lead owners: Director of Pharmacy and Chief Financial Officer.
* Slicing dimensions: Monitored across five benefit years (2020 to 2024), therapeutic categories (parsed from FDA indications), and supplier counts (markets with two or more approved generic suppliers).
* Action item: Remove off-patent brand drugs from physician order sets and turn on automated generic substitution at order entry.

### Clinical guardrail: formulary access disruption rate
* Calculation: The share of total outpatient and discharge prescriptions in chronic disease categories (such as diabetes, psychiatric care, and seizure disorders) where formulary changes affect medications with fewer than two therapeutic alternatives.
* Business alignment: Protects patient adherence, avoids readmissions, and reduces physician friction. Lead owners: Chief Medical Officer and P&T Committee Chair.
* Slicing dimensions: Monitored across chronic care clinics, inpatient discharge orders, and vulnerable patient populations.
* Action item: Hard stop: disruption must remain strictly under 2.5% (our modeled plan reached 1.8%). Any medication without therapeutic generic equivalence is exempt from automated substitution.

### Data reliability check: packaging and billing outlier index
* Calculation: The share of modeled savings tied to records flagged for packaging unit discrepancies (CMS interquartile range checks: cost variance over 10% and greater than $1.00 per unit).
* Business alignment: Prevents inventory miscalculations caused by package-level billing errors, such as billing an entire inhaler box as individual actuations. Lead owner: Pharmacy Purchasing and Inventory Lead.
* Slicing dimensions: Tracked across dosage forms (oral tablets, liquids, inhalers, and injectable vials).
* Action item: Flagged savings must stay under 5.0% of the total projection. Any flagged items go to a manual packaging review queue before purchasing contracts are updated.

---

## 3. Data pipeline and quality controls

The pipeline processes longitudinal claims benchmarked against federal reference files to reflect hospital purchasing patterns. All ETL logic runs in `src/etl/clean_pipeline.py`:

```text
+--------------------------------------------------------+
|               Table A: mcd_spending_bgm                |
|       (Longitudinal Drug and Manufacturer Matrix)      |
+--------------------------------------------------------+
| Primary Key: [Brnd_Name, Gnrc_Name, Mftr_Name]         |
| Tot_Spndng_2020 ... Tot_Spndng_2024                    |
| Tot_Clms_2020   ... Tot_Clms_2024                      |
| Tot_Dsg_Unts_2020 ... Tot_Dsg_Unts_2024                |
| Avg_Spnd_Per_Dsg_Unt_Wghtd_2020 ... 2024               |
| Outlier_Flag_2020 ... Outlier_Flag_2024                |
| CAGR_Avg_Spnd_Per_Dsg_Unt_20_24                        |
+---------------------------┬----------------------------+
                            |
                            | 1:Many Join on Composite Key
                            v
+--------------------------------------------------------+
|             Table B: mcd_spending_dbexport             |
|               (Clinical Indication Fact)               |
+--------------------------------------------------------+
| Primary Key: [Brand Name, Generic Name, Mftr, Year]    |
| Total Payments, Total Claim Count, Total Service Units |
| Cost Per Unit, Cost Per Unit All Mfg                   |
| Uses (Clinical indications and unstructured text)      |
+--------------------------------------------------------+
```

### Pipeline data handling rules
1. Preventing double counts:
   * The issue: Public benchmark files place national summary rows (`Mftr_Name == 'Overall'`) in the same column as individual manufacturer records. A simple sum across that column doubles total expenditure.
   * Pipeline fix: The ETL code splits records into two separate Apache Parquet files: `data/cleaned/mcd_drug_overall_2020_2024.parquet` for overall drug trends and `data/cleaned/mcd_mftr_detail_2020_2024.parquet` for manufacturer pricing.
2. Low-volume claim suppression:
   * The issue: Claim counts below 11 are redacted under HIPAA privacy standards.
   * Pipeline fix: The pipeline keeps suppressed records as nulls rather than replacing them with zeros. Zero-imputation causes artificial multi-thousand-percent spikes in 5-year growth rates.
3. Packaging error checks:
   * Records with packaging or unit count anomalies are flagged and routed to a toggle filter in the dashboard, letting clinical teams verify savings numbers with and without borderline records.

---

## 4. Key findings and data analysis

```text
+-----------------------------------------------------------------------------------------+
| SUMMARY OF STATISTICAL FINDINGS (2020 TO 2024 PANEL)                                    |
+-------------------+----------------------------+-----------------------+----------------+
| Area              | Analytical Method          | Observed Result       | Status         |
+-------------------+----------------------------+-----------------------+----------------+
| H1: Concentration | Multi-Tier Quantile Flow   | 65.4% of Spend in Top | Confirmed      |
|     (Sankey Flow) | and Clinical Grouping      | 5% of Lines (p<0.001) |                |
| H2: Cost Drivers  | Logarithmic Decomposition  | 72.4% Price vs. 27.6% | Confirmed      |
|                   |                            | Volume (p < 0.01)     |                |
| H3: Generic Spread| Interquartile Price Spread | Over 35% Spread       | Confirmed      |
|                   | Across Approved Suppliers  | Across Labels (p<0.001|                |
+-------------------+----------------------------+-----------------------+----------------+
```

```text
                                                                +--> Specialty Biologics and Infusions (38%)
                                +--> Top 5% High-Cost Lines ----+--> GLP-1 and Diabetes Treatments (28%)
                                |    (65.4% of Pharmacy Spend)  +--> Oncology and CNS Maintenance (34%)
Total Outpatient Pharmacy Spend -+
($85M Hospital Medication Cost) |
                                +--> Remaining 95% of Formulary ----> Thousands of Low-Cost Generic Fills
                                     (34.6% of Spend)                 (Predictable, Stable Pricing)
```

### Finding 1: Spending concentrates in a small fraction of medications
* Method: Multi-tier spend flow analysis across unique formulations and therapeutic classes, displayed in the interactive Sankey chart in `index.html`.
* Data result:
  * Just 5% of order lines account for 65.4% of the hospital's total outpatient drug budget, while the other 95% of orders (thousands of everyday maintenance generics) make up only 34.6%.
  * In that top group, spending flows into two main categories: specialty biologics and immunology (38%) and GLP-1 diabetes medications (28%).
  * More than half of the hospital's financial exposure sits in just 25 medications.
* Practical takeaway: Broad budget cuts across everyday floor stock frustrate clinical staff without helping operating margins. Formulary reviews should focus on these top 25 high-cost medications.

### Finding 2: Unit price increases drove budget growth, not patient volume
* Method: Log-additive growth decomposition over the five-year window, separating unit price changes from prescription volume (`src/analytics/test_h2_decomposition.py`):
  $$\Delta \ln(\text{Spend}) = \ln\left(\frac{\text{Spend}_{2024}}{\text{Spend}_{2020}}\right) = \ln\left(\frac{\text{Price}_{2024}}{\text{Price}_{2020}}\right) + \ln\left(\frac{\text{Units}_{2024}}{\text{Units}_{2020}}\right)$$
* Data result: For medications where spending rose more than 50%, wholesale price increases caused 72.4% of that expansion, while patient volume accounted for only 27.6% (paired Wilcoxon test, p < 0.01). In GLP-1 therapies, prescription volume rose 18% while cost per dose surged 84%.
* Practical takeaway: Shows executive leadership that hospital budget overruns were not caused by clinicians overprescribing, but by wholesale price increases from drug makers. This gives clinical leadership solid ground to update physician order sets.

### Finding 3: Generic price variation creates a $3.2M margin opportunity
* Method: Price spread analysis across competing generic manufacturers under hospital purchasing agreements (`src/analytics/test_h3_price_spread.py`).
* Data result: For multi-source generic drugs with two or more approved suppliers, wholesale prices between the 75th and 25th percentiles differ by more than 35% (p < 0.001).
* What happens: When pharmacy buyers order stock without checking contracted primary supplier tiers, the hospital frequently pays a 35% premium for the identical active chemical ingredient.
* Practical takeaway: Enforcing Tier-1 contracted generic suppliers recovers $2.1M, and setting automatic generic substitution on brand discharge orders recovers $1.1M, totaling $3.2M in annual operating margin relief.

---

## 5. Prioritized hospital action plan

```text
+----------------------------------------------------------------------------------------------------+
| HOSPITAL PHARMACY ACTION MATRIX                                                                    |
+----------+----------------------------+-----------------------+-------------+----------------------+
| Priority | Strategic Initiative       | Scope                 | Lead Owner  | Annual Impact        |
+----------+----------------------------+-----------------------+-------------+----------------------+
| P0       | Enforce Tier-1 GPO         | Multi-source generic  | Pharmacy    | $2.1M margin         |
|          | Generic Purchasing Tiers   | lines (2+ suppliers)  | Buyer       | recovery             |
| P1       | Build EHR Order Sets for   | High-cost biologics   | P&T Chair / | 12% to 18% cost      |
|          | Biologics and GLP-1s       | and GLP-1 therapies   | CMO         | growth reduction     |
| P2       | Turn on Automatic Generic  | Discharge and clinic  | Pharmacy    | $1.1M brand          |
|          | Substitution in the EHR    | multi-source brands   | Director    | leakage recovery     |
+----------+----------------------------+-----------------------+-------------+----------------------+
```

| Priority | Initiative | Scope | Lead Owner | Expected Annual Impact | Tracking Metric and Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P0** | **Enforce primary GPO generic contracts** | Multi-source generic lines with two or more approved manufacturers | Pharmacy Purchasing Buyer | **$2.1M margin recovery** | Contract tier compliance over 95%; 30-day review cycle |
| **P1** | **Introduce structured order sets in Epic and Cerner** | High-cost specialty biologics and GLP-1 therapies | P&T Committee Chair and CMO | **12% to 18% cost growth reduction** on target classes | First-line clinical guideline adherence; 60 days |
| **P2** | **Turn on automated generic substitution at order entry** | Outpatient and discharge orders written for multi-source brands | Pharmacy Director and Clinical Informatics Lead | **$1.1M brand overpayment recovery** | Generic dispensing rate over 93%; 90 days |

---

## 6. Interactive decision tools

The findings connect to two lightweight tools: a 7-slide executive presentation (`index.html`) on GitHub Pages and a dedicated operational decision cockpit (`dashboard.html` / Streamlit):

```text
+-----------------------------------------------------------------------------------------+
| HOSPITAL PHARMACY FORMULARY COCKPIT                                                     |
| Controls: [Panel Year: 2024]   [Clinical Class: All]   [x] Exclude Packaging Outliers    |
+-----------------------------------------------------------------------------------------+
| [ $85.0M Total Spend ]  [ $3.2M Margin Recovery ]  [ 840K Total Fills ] [ 1.8% Risk ]   |
+------------------------------------------------------------+----------------------------+
| CUMULATIVE CAPITAL FLOW (SANKEY MODEL)                     | UNIT COST VS VOLUME SPREAD |
| "Top 5% of lines account for 65.4% of pharmacy budget"     | "Unit price increases out- |
|                                                            |  paced fills by 2.6 to 1"  |
| Total Spend ======> Top 5% Lines ===> Biologics (38%)      |      Acquisition Cost CAGR |
|             ======> Bottom 95%   ===> GLP-1s (28%)         |    o       o   * Target    |
|                                                            | ---------------------------|
|                                                            |          o   Script Volume |
+-----------------------------------------------------------------------------------------+
| TARGETED HOSPITAL FORMULARY ACTION MATRIX (EXPORTABLE TO CSV)                           |
| [Search...]                                                                             |
| Drug Formulation | Class         | Current Acq Cost  | Lowest Generic | Net Recovery    |
|------------------+---------------+-------------------+----------------+-----------------|
| Triamcinolone    | Allergy/Nasal | $1.12             | $0.46          | $42,000         |
| Methylphenidate  | CNS/ADHD      | $3.40             | $1.20          | $115,000        |
| Fluticasone      | Respiratory   | $2.15             | $0.85          | $88,000         |
+-----------------------------------------------------------------------------------------+
```

### Interface capabilities
* Clear hierarchy: Key recovery totals and clinical safety numbers sit at the top, followed by the Sankey spend breakdown and the sortable drug table.
* Clean visual style: Uses neutral slate gray with green reserved exclusively for verified savings opportunities.
* Summary headlines: Every chart leads with its takeaway rather than an abstract label.
* Scenario testing: Pharmacy buyers can test generic adoption targets between 70% and 95% and adjust pricing percentiles to stress-test numbers before committee meetings.

---

## 7. Operational assumptions and clinical boundaries

* Wholesale costs compared to net rebates: Hospital purchasing data models gross wholesale acquisition figures. While 340B discounts or manufacturer rebates provide additional savings, modeled dollars reflect baseline acquisition reductions achievable directly at order entry.
* Dosage form matching: Modeled generic substitutions require identical dosage forms (for example, tablet-to-tablet or inhaler-to-inhaler) with FDA therapeutic equivalence ratings.
* Physician override option: All automated order rules include an override button so clinicians can keep specific brand formulations when medically necessary.

---

## 8. Repository structure

```text
medicaid-spending-optimization/
├── data/
│   ├── raw/                              # Source claims and benchmark reference files
│   └── cleaned/                          # Partitioned Apache Parquet datasets
├── src/
│   ├── etl/
│   │   └── clean_pipeline.py             # Data cleaning, text normalization, and Parquet staging
│   ├── analytics/
│   │   ├── test_h1_capital_allocation.py # Sankey spend flow and concentration modeling
│   │   ├── test_h2_decomposition.py      # Logarithmic price-volume growth decomposition
│   │   └── test_h3_price_spread.py       # Multi-source generic spread and purchasing simulation
│   └── dashboard/
│       └── app.py                        # Streamlit operational decision cockpit
├── index.html                            # 7-Slide Executive Briefing Deck (GitHub Pages)
├── dashboard.html                        # Standalone Operational Decision Cockpit
├── requirements.txt                      # Pinned production dependencies
└── README.md                             # Executive briefing and technical documentation
```

---

## 9. Local setup and reproduction guide

```bash
# 1. Clone repository
git clone https://github.com/J-Amores/data-analyst-portfolio.git
cd data-analyst-portfolio/medicaid-spending-optimization

# 2. Activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run data cleaning and statistical models
python src/etl/clean_pipeline.py
python src/analytics/test_h1_capital_allocation.py
python src/analytics/test_h2_decomposition.py
python src/analytics/test_h3_price_spread.py

# 5. Launch interactive hospital decision cockpit
streamlit run src/dashboard/app.py
```
