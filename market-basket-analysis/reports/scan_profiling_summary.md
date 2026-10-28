# SCAN Exploratory Data Analysis & Commercial Profiling Summary

## 1. Portfolio Baseline Summary
* **Active Order Ledger Window:** 2010-12-01 to 2011-12-09 (12.3 calendar months)
* **Total Valid Commercial Orders:** 19,773 invoices
* **Total Commercial Sales Line Items:** 522,544 items
* **Total Commercial Gross Merchandise Volume (GMV):** £10,247,610.15
* **Catalog Assortment Breadth:** 3,801 unique active SKUs
* **Registered Commercial Customer Accounts:** 4,334 accounts
* **Guest Checkout Revenue Contribution:** £1,510,382.51 (14.74% of commercial sales across 1,371 orders)
* **Registered Customer Revenue Contribution:** £8,737,227.64 (85.26% across 18,402 orders)
* **Portfolio-Wide Cancellation Leakage Rate:** 8.05% of GMV (£896,812.49 absolute cancelled value across credit notes)

---

## 2. Basket Size & Order Value Segmentation

### Executive 3-Tier Segmentation (Small vs. Medium vs. Large)

| Basket Size Segment | Orders Count | Order Share (%) | Gross Revenue (£) | Revenue Share (%) | Median AOV (£) | Mean AOV (£) | Median SKUs | Mean SKUs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Small (1-2 SKUs)** | 2,313 | 11.70% | £710,521.85 | 6.93% | £57.60 | £307.19 | 1 | 1.35 |
| **Medium (3-5 SKUs)** | 2,041 | 10.32% | £645,761.75 | 6.30% | £140.85 | £316.39 | 4 | 3.99 |
| **Large (6+ SKUs)** | 15,419 | 77.98% | £8,891,326.55 | 86.76% | £322.30 | £576.65 | 20 | 32.82 |
| **Portfolio Total / Baseline** | **19,773** | **100.00%** | **£10,247,610.15** | **100.00%** | **£302.20** | **£518.26** | **15** | **26.16** |

### Granular 5-Tier Wholesale & Retail Decomposition

| Detailed Tier | Orders Count | Order Share (%) | Revenue (£) | Revenue Share (%) | Median AOV (£) | Mean AOV (£) | IQR AOV (£) | P90 AOV (£) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1-2 SKUs** | 2,313 | 11.70% | £710,521.85 | 6.93% | £57.60 | £307.19 | £181.50 | £429.92 |
| **3-5 SKUs** | 2,041 | 10.32% | £645,761.75 | 6.30% | £140.85 | £316.39 | £253.78 | £596.70 |
| **6-15 SKUs** | 5,622 | 28.43% | £2,119,603.95 | 20.68% | £230.43 | £377.02 | £189.82 | £590.25 |
| **16-30 SKUs** | 5,253 | 26.57% | £2,376,824.45 | 23.19% | £335.50 | £452.47 | £211.34 | £675.46 |
| **31+ SKUs** | 4,544 | 22.98% | £4,394,898.15 | 42.89% | £550.58 | £967.19 | £674.68 | £1838.61 |

---

## 3. Top 20 SKUs by Gross Merchandise Value and SKU Return Risk

| Rank | StockCode | Product Description | Gross Sales (£) | Order Frequency | Avg Unit Price (£) | Units Sold | Standalone Return Rate (%) | Return Guardrail (<5.0%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `22423` | REGENCY CAKESTAND 3 TIER | £174,156.54 | 1,988 | £13.98 | 13,851 | 5.29% | FLAGGED |
| 2 | `23843` | PAPER CRAFT , LITTLE BIRDIE | £168,469.60 | 1 | £2.08 | 80,995 | 50.00% | FLAGGED |
| 3 | `85123A` | WHITE HANGING HEART T-LIGHT HOLDER | £106,415.23 | 2,265 | £3.22 | 37,933 | 5.86% | FLAGGED |
| 4 | `47566` | PARTY BUNTING | £99,445.23 | 1,685 | £5.80 | 18,283 | 1.19% | PASS |
| 5 | `85099B` | JUMBO BAG RED RETROSPOT | £94,159.81 | 2,089 | £2.49 | 48,371 | 2.06% | PASS |
| 6 | `23166` | MEDIUM CERAMIC TOP STORAGE JAR | £81,700.92 | 247 | £1.47 | 78,033 | 48.67% | FLAGGED |
| 7 | `23084` | RABBIT NIGHT LIGHT | £66,870.03 | 994 | £2.39 | 30,739 | 0.31% | PASS |
| 8 | `22086` | PAPER CHAIN KIT 50'S CHRISTMAS | £64,875.59 | 1,160 | £3.36 | 19,329 | 1.76% | PASS |
| 9 | `84879` | ASSORTED COLOUR BIRD ORNAMENT | £58,927.62 | 1,455 | £1.72 | 36,362 | 0.23% | PASS |
| 10 | `79321` | CHILLI LIGHTS | £54,096.36 | 661 | £6.80 | 10,302 | 0.64% | PASS |
| 11 | `22502` | PICNIC BASKET WICKER SMALL | £51,408.77 | 463 | £10.30 | 1,937 | 0.74% | PASS |
| 12 | `22197` | POPCORN HOLDER | £51,334.47 | 1,392 | £1.04 | 56,898 | 0.71% | PASS |
| 13 | `23298` | SPOTTY BUNTING | £43,148.18 | 1,146 | £5.52 | 8,466 | 1.11% | PASS |
| 14 | `22386` | JUMBO BAG PINK POLKADOT | £42,401.01 | 1,218 | £2.60 | 21,448 | 1.89% | PASS |
| 15 | `23203` | JUMBO BAG VINTAGE DOILY | £42,030.34 | 1,231 | £2.28 | 20,485 | 2.50% | PASS |
| 16 | `21137` | BLACK RECORD COVER FRAME | £40,633.38 | 375 | £4.22 | 11,651 | 0.14% | PASS |
| 17 | `23284` | DOORMAT KEEP CALM AND COME IN | £38,133.64 | 728 | £8.78 | 5,487 | 4.03% | PASS |
| 18 | `22720` | SET OF 3 CAKE TINS PANTRY DESIGN | £38,108.89 | 1,385 | £5.83 | 7,483 | 1.92% | PASS |
| 19 | `22960` | JAM MAKING SET WITH JARS | £37,082.13 | 1,132 | £5.08 | 8,695 | 2.66% | PASS |
| 20 | `82484` | WOOD BLACK BOARD ANT WHITE FINISH | £35,966.92 | 685 | £8.44 | 6,012 | 0.47% | PASS |

---

## 4. Top 20 SKUs by Checkout Frequency (Storefront Velocity Anchors)

| Rank | StockCode | Product Description | Order Frequency | Storefront Penetration (%) | Gross Sales (£) | Units Sold | Standalone Return Rate (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `85123A` | WHITE HANGING HEART T-LIGHT HOLDER | 2,265 | 11.46% | £106,415.23 | 37,933 | 5.86% |
| 2 | `85099B` | JUMBO BAG RED RETROSPOT | 2,089 | 10.56% | £94,159.81 | 48,371 | 2.06% |
| 3 | `22423` | REGENCY CAKESTAND 3 TIER | 1,988 | 10.05% | £174,156.54 | 13,851 | 5.29% |
| 4 | `47566` | PARTY BUNTING | 1,685 | 8.52% | £99,445.23 | 18,283 | 1.19% |
| 5 | `20725` | LUNCH BAG RED RETROSPOT | 1,565 | 7.91% | £35,862.36 | 19,432 | 2.33% |
| 6 | `84879` | ASSORTED COLOUR BIRD ORNAMENT | 1,455 | 7.36% | £58,927.62 | 36,362 | 0.23% |
| 7 | `22197` | POPCORN HOLDER | 1,392 | 7.04% | £51,334.47 | 56,898 | 0.71% |
| 8 | `22720` | SET OF 3 CAKE TINS PANTRY DESIGN | 1,385 | 7.00% | £38,108.89 | 7,483 | 1.92% |
| 9 | `21212` | PACK OF 72 RETROSPOT CAKE CASES | 1,320 | 6.68% | £21,246.45 | 36,396 | 0.93% |
| 10 | `22383` | LUNCH BAG SUKI DESIGN | 1,284 | 6.49% | £22,486.34 | 12,518 | 0.99% |
| 11 | `20727` | LUNCH BAG  BLACK SKULL. | 1,273 | 6.44% | £22,346.96 | 12,195 | 0.90% |
| 12 | `22457` | NATURAL SLATE HEART CHALKBOARD | 1,249 | 6.32% | £27,991.61 | 9,119 | 0.54% |
| 13 | `23203` | JUMBO BAG VINTAGE DOILY | 1,231 | 6.23% | £42,030.34 | 20,485 | 2.50% |
| 14 | `22386` | JUMBO BAG PINK POLKADOT | 1,218 | 6.16% | £42,401.01 | 21,448 | 1.89% |
| 15 | `22469` | HEART OF WICKER SMALL | 1,201 | 6.07% | £32,094.60 | 17,963 | 0.64% |
| 16 | `21931` | JUMBO STORAGE BAG SUKI | 1,184 | 5.99% | £30,764.01 | 13,651 | 1.92% |
| 17 | `22411` | JUMBO SHOPPER VINTAGE RED PAISLEY | 1,175 | 5.94% | £28,577.10 | 12,574 | 2.13% |
| 18 | `22961` | JAM MAKING SET PRINTED | 1,162 | 5.88% | £25,637.78 | 16,396 | 1.63% |
| 19 | `22086` | PAPER CHAIN KIT 50'S CHRISTMAS | 1,160 | 5.87% | £64,875.59 | 19,329 | 1.76% |
| 20 | `22382` | LUNCH BAG SPACEBOY DESIGN | 1,157 | 5.85% | £18,031.31 | 10,427 | 1.33% |

---

## 5. Temporal Dynamics (Seasonality & Intake Rhythm)

### Monthly Transaction Volume & Multi-Item Basket Expansion

| Year-Month | Invoices Count | Gross GMV (£) | Total Units | Mean AOV (£) | Median AOV (£) | Mean Basket Size | Large Basket Share (6+ SKUs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2010-12** | 1,550 | £775,714.95 | 357,531 | £500.46 | £254.39 | 26.04 | 73.16% |
| **2011-01** | 1,081 | £670,439.46 | 386,741 | £620.20 | £305.07 | 31.15 | 79.65% |
| **2011-02** | 1,093 | £507,850.09 | 282,625 | £464.64 | £303.00 | 24.25 | 78.13% |
| **2011-03** | 1,440 | £689,716.82 | 376,145 | £478.97 | £292.78 | 24.32 | 77.15% |
| **2011-04** | 1,235 | £515,463.08 | 307,653 | £417.38 | £300.12 | 23.13 | 77.89% |
| **2011-05** | 1,668 | £740,000.14 | 394,646 | £443.65 | £304.42 | 21.29 | 75.12% |
| **2011-06** | 1,525 | £737,683.99 | 388,129 | £483.73 | £283.95 | 23.15 | 76.72% |
| **2011-07** | 1,452 | £688,178.12 | 399,264 | £473.95 | £301.23 | 26.13 | 78.65% |
| **2011-08** | 1,339 | £724,288.42 | 420,695 | £540.92 | £305.34 | 25.29 | 77.60% |
| **2011-09** | 1,818 | £1,028,338.80 | 568,699 | £565.64 | £323.42 | 26.57 | 80.80% |
| **2011-10** | 2,005 | £1,103,327.63 | 619,597 | £550.29 | £311.76 | 28.67 | 80.20% |
| **2011-11** | 2,751 | £1,452,112.69 | 746,951 | £527.85 | £297.65 | 29.22 | 79.46% |
| **2011-12** | 816 | £614,495.96 | 312,647 | £753.06 | £295.46 | 29.87 | 77.21% |

### Day of Week Commercial Velocity

| Day of Week | Invoices Count | Gross GMV (£) | Mean AOV (£) | Median AOV (£) | Commercial Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Monday** | 3,076 | £1,682,958.17 | £547.13 | £304.99 | Peak procurement occurs midweek |
| **Tuesday** | 3,509 | £2,085,029.78 | £594.19 | £309.35 | Peak procurement occurs midweek |
| **Wednesday** | 3,667 | £1,782,370.47 | £486.06 | £303.15 | Peak procurement occurs midweek |
| **Thursday** | 4,209 | £2,131,735.86 | £506.47 | £300.84 | Peak procurement occurs midweek |
| **Friday** | 3,109 | £1,767,204.37 | £568.42 | £303.91 | Peak procurement occurs midweek |
| **Sunday** | 2,203 | £798,311.50 | £362.37 | £262.42 | Peak procurement occurs midweek |

---

## 6. Geographic Concentration & Cross-Border Account Profiling

| Country | Orders Count | Gross GMV (£) | Mean AOV (£) | Median AOV (£) | Mean Basket SKUs | Median Basket SKUs | Wholesale Share (6+ SKUs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **United Kingdom** | 17,901 | £8,724,834.50 | £487.39 | £299.67 | 26.46 | 15 | 77.44% |
| **Netherlands** | 93 | £283,889.34 | £3052.57 | £814.62 | 24.97 | 13 | 76.34% |
| **EIRE** | 282 | £270,850.86 | £960.46 | £624.71 | 27.54 | 22 | 84.75% |
| **Germany** | 443 | £205,381.15 | £463.61 | £318.85 | 19.49 | 14 | 81.04% |
| **France** | 382 | £184,493.00 | £482.97 | £344.57 | 21.11 | 17 | 87.17% |
| **Australia** | 56 | £138,103.81 | £2466.14 | £430.45 | 21.05 | 10 | 66.07% |
| **Spain** | 88 | £55,706.56 | £633.03 | £363.06 | 27.28 | 21 | 85.23% |
| **Switzerland** | 50 | £53,065.60 | £1061.31 | £557.18 | 38.28 | 25 | 84.00% |
