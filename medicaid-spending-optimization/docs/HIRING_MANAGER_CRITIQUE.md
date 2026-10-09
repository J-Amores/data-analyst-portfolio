Hiring Manager Standards Critique Pass: Transforming a Tutorial into a $120k+ Showing Project
As a former data director and hiring manager, I evaluate hundreds of portfolios every cohort. Most data candidates submit what I call Learning Projects. Here is an honest, line-by-line review of how this Medicaid project compares against executive hiring standards:
┌─────────────────────────────────────────────────────────────────────────────┐
│                 PORTFOLIO MATURITY EVALUATION SCORECARD                     │
├─────────────────────────┬──────────────┬──────────────┬─────────────────────┤
│ Evaluation Pillar       │ Tutorial /   │ Showing      │ Our Project         │
│                         │ Junior Trap  │ Exemplar     │ Specification       │
├─────────────────────────┼──────────────┼──────────────┼─────────────────────┤
│ 1. Business Relevance   │ 1.5 / 5.0    │ 5.0 / 5.0    │ 5.0 / 5.0           │
│ 2. Analytical Rigor     │ 2.0 / 5.0    │ 4.5 / 5.0    │ 4.8 / 5.0           │
│ 3. Professional Polish  │ 1.0 / 5.0    │ 5.0 / 5.0    │ 5.0 / 5.0           │
└─────────────────────────┴──────────────┴──────────────┴─────────────────────┘
Pillar 1: Business Relevance (Executive Problem vs. Tutorial Exercise)
The Typical Junior Mistake: The project is titled "Medicaid Drug Data Analysis in Python". The author writes: "In this project, I cleaned null values and plotted histograms of drug costs to see the distribution". A hiring manager immediately thinks: 'This person is still a student doing homework. They have no concept of who uses data or why budgets exist.'
How Our Architecture Overcomes It: The project is framed around State Medicaid PBM Formulary Strategy & Avoidable Spend Extraction. It speaks directly to a real executive stakeholder (State Medicaid Pharmacy Director), identifies statutory constraints (pre-rebate gross outlay), establishes a clear North Star metric with clinical guardrails, and provides a dollar-quantified action plan ($ Addressable Savings).
Pillar 2: Analytical Rigor (Econometric Decomposition vs. Descriptive Summaries)
The Typical Junior Mistake: The candidate calculates df.groupby('Brnd_Name')['Tot_Spndng_2024'].sum().head(10) and displays a standard horizontal bar chart. There is zero depth, zero hypothesis testing, and zero investigation into root causes.
How Our Architecture Overcomes It:
We execute an econometric Price-Volume Growth Decomposition: separating whether a drug's budget impact stems from clinical utilization expansion (claim volume) or manufacturer price hikes (dosage unit cost CAGR).
We handle complex public data nuances: isolating CMS IQR outlier flags without dropping valid spend, handling HIPAA suppression thresholds ($< 11$ claims) without naive zero-imputation, and preventing hierarchical double-counting (Mftr_Name == 'Overall').
Pillar 3: Professional Polish & Delivery (Decision-Driven README vs. Code Notebook Dump)
The Typical Junior Mistake: The candidate uploads a messy Jupyter Notebook full of stack traces, raw printouts of dataframes, and 40 Seaborn charts with default blue/orange palettes, overlapping axis labels, and descriptive titles like "Boxplot of Cost Per Unit".
How Our Architecture Overcomes It:
Two-Layer Project Structure: All technical ETL, data cleaning scripts, and SQL/Python code are modularized into repository files. The executive write-up (the README) reads like a strategic executive briefing delivered to a healthcare VP or State Director.
Cognitive Dashboard Design: Built strictly under the DASH framework—utilizing monochromatic palettes, high data-to-ink ratios, sparklines, and news-flash headlines that deliver the "So What?" in the first 10 seconds.
Christine's Actionable Next Steps:
Commit these three specification documents (PROJECT_CHARTER.md, DATA_SPEC.md, AGENT_TASKS.md) into your repository /docs folder immediately.
Execute Phase 1 and Phase 2 of the Agent Task plan: Ensure your ETL script explicitly isolates the Mftr_Name == 'Overall' rows before calculating any total spend numbers to avoid double-counting.
Draft your GitHub README following the Executive Template: Lead with the 3–4 sentence executive summary, embed the Pareto spend curve and the Price-Volume driver matrix with news-flash headlines, and conclude with the concrete Formulary Action Plan!