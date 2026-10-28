# Project Charter: Outbound Acquisition Funnel & Contact Fatigue Optimization (Bank Direct Marketing)

## 1. Executive Context & Business Mandate
* Executive Stakeholders: VP of Growth Marketing, Head of Outbound Call Center Operations, and Director of Retail Banking.
* Business Problem: Direct outbound telemarketing remains a core driver for retail term deposit acquisition at Banco de Portugal. However, outbound call center operations suffer from four critical operational bottlenecks:
  1. Unbounded Call Frequency and Diminishing Returns: Outbound sales agents repeatedly contact leads up to 56 times in a single campaign cycle. Calling beyond 3 attempts burns valuable agent capacity on exhausted leads where conversion yields plummet.
  2. Channel Misallocation: Outbound dialers continue routing high call volumes through fixed landline channels despite cellular contact demonstrating significantly higher responsiveness.
  3. Demographic and Macroeconomic Misalignment: Outreach lists disproportionately target working-age prospects (ages 31-45) with sub-10% conversion rates, under-allocating bandwidth to high-affinity segments (retirees, students, prior campaign responders) and failing to adapt to macroeconomic interest rate shifts.
  4. Post-Hoc Modeling Leakage Trap: Call center analytics historically relied on retrospective call duration to explain conversion. Because call duration is unknown prior to dialing, this creates severe data leakage and invalidates predictive lead targeting.

## 2. Decision-Driven Methodology: The READY Framework
* R: Representative Data: Primary dataset comprises 41,188 outbound campaign records from May 2008 to November 2010 (`bank-additional-full.csv`), enriched with client demographics, campaign contact histories, and 5 macroeconomic indicators. Secondary balance benchmark comprises 45,211 records (`bank-full.csv`).
* E: Exec-Driven Questions:
  * At what exact contact attempt does outbound calling reach diminishing returns (the Contact Fatigue Threshold)?
  * What is the true efficiency gain of prioritizing cellular channels over fixed landlines?
  * How much outbound agent capacity is preserved by enforcing a 3-touch contact cap, and does term deposit volume remain above 85%?
* A: Analytical Frameworks: Two-Layer Architecture, CLEAN Data Transformation Pipeline, Contact Diminishing Returns and Marginal Yield Modeling, Stratified Chi-Square Independence Testing, and Executive Dashboards.
* D: Data Best Practices: Strict quarantine of call duration from pre-call targeting models; transformation of sentinel code `pdays == 999` into explicit recency flags; explicit governance of unknown categorical attributes; exact row deduplication tracking.
* Y: Your Insights and Strategic Impact: Delivery of a 3-tier Outbound Policy Matrix establishing a 3-touch hard stop, cellular-first dialer routing, and macroeconomic interest rate cohort targeting.

## 3. Four-Layer Metric Model

### Layer 1: North Star Metrics (Commercial & Operational Efficiency)
* Metric 1A: Outbound Campaign Conversion Rate
  $$\text{Campaign Conversion Rate} = \left( \frac{\sum (y = \text{'yes'})}{\text{Total Client Records}} \right) \times 100$$
  Baseline: 11.27% (4,640 subscriptions across 41,188 client records).
* Metric 1B: Outbound Call Efficiency
  $$\text{Outbound Call Efficiency} = \left( \frac{\sum (y = \text{'yes'})}{\sum \text{campaign touches}} \right) \times 100$$
  Baseline: 4.39% (4,640 subscriptions across 105,754 total outbound calls dialed).
* Executive Owner: VP of Growth Marketing and Head of Outbound Call Center Operations.

### Layer 2: Guardrail Metrics (Fatigue Boundaries & Volume Protection)
* Guardrail Metric 1: Contact Fatigue Threshold (Marginal Conversion Yield)
  $$\text{Marginal Yield at Touch } k = \left( \frac{\text{Subscriptions Won at Touch } k}{\text{Leads Contacted at Touch } k} \right) \times 100$$
  Operational Guardrail: Marginal conversion yield at contact attempt $k$ must remain $\ge 8.0\%$. Any contact tier dropping below 8.0% is classified as operational contact fatigue.
  Executive Owner: Head of Outbound Call Center Operations.
* Guardrail Metric 2: Pipeline Volume Preservation
  $$\text{Pipeline Volume Preservation} = \left( \frac{\text{Retained Subscriptions Under Capping Policy}}{\text{Baseline Total Subscriptions}} \right) \times 100$$
  Commercial Guardrail: Retained term deposit subscriptions under contact-capping policies must remain $\ge 85.0\%$ of baseline volume.
  Executive Owner: Director of Retail Banking Products.

### Layer 3: Secondary Operational Metrics
* Touch Capacity Allocation Share: Proportion of total outbound calls consumed by contact tiers (Touches 1-3 vs. Touches 4+).
* Cost per Acquisition (CPA) Proxy: Outbound call touches and duration minutes consumed per confirmed subscription.
* Channel Conversion Ratio: Cellular conversion rate divided by fixed telephone conversion rate.

### Layer 4: Data Quality & Integrity Guardrails
* Zero Post-Call Leakage: Exclude call duration from pre-call targeting views.
* Sentinel Code Resolution: 100% of `pdays == 999` mapped to `was_previously_contacted == 0`.
* Categorical Completeness: Preserve explicit 'unknown' records across job, education, default, housing, loan, and marital attributes without naive imputation.

## 4. Three Falsifiable Executive Hypotheses

| Hypothesis ID | Statement | Null Hypothesis ($H_0$) | Analytical Test & Threshold | Action if Supported |
| :--- | :--- | :--- | :--- | :--- |
| H1: Contact Fatigue Boundary | Contact attempts beyond 3 touches exhibit severe diminishing returns (< 8.0% marginal conversion), consuming > 48% of outbound call touches while generating < 12% of subscriptions. | Marginal conversion yield is invariant across contact touches 1 through 6+ ($\chi^2$ test $p \ge 0.05$). | Chi-square goodness-of-fit and log-linear regression across touches 1-3 vs. 4+. Decision Threshold: Marginal yield at Touch 4+ < 8.0% ($p < 0.001$). | Implement an automated hard stop at 3 contact attempts per client per campaign cycle. |
| H2: Channel & Prior-Outcome Multiplier | Cellular outreach converts at $\ge 2.5\times$ the rate of landline telephone outreach, and prior campaign responders (`poutcome == 'success'`) convert at > 60%. | Conversion rates are equal between cellular and landline channels ($p \ge 0.05$). | Two-sample proportion Z-test and Mantel-Haenszel odds ratio. Decision Threshold: Odds Ratio $\ge 2.5$ and success rate > 60% ($p < 0.001$). | Mandate cellular-first dialer routing; prioritize prior campaign responders at top of outbound queues. |
| H3: Macroeconomic Rate & Demographic Affinity | Low Euribor regimes (`euribor3m <= 3.0%`) and high-affinity cohorts (Retirees/Age 60+ and Students) convert at > 3.0x the rate of working-age (31-45) cohorts. | Term deposit conversion is independent of Euribor interest rates and demographic cohorts ($p \ge 0.05$). | Two-sample Welch t-test and stratified relative risk. Decision Threshold: Relative Risk > 3.0 ($p < 0.001$). | Dynamically modulate campaign marketing budget and agent staffing based on interest rate cycles and age affinity tiers. |
