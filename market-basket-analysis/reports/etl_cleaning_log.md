# Production ETL Cleaning Log: 5-Step CLEAN Pipeline

## Executive Overview
* **Source Ledger:** `data/raw/Online Retail.xlsx` (Sheet: `Online Retail`)
* **Raw Transaction Grain:** 1 line item per invoice x stock code
* **Total Raw Records:** 541,909 line items across 25,900 invoices (£9,747,747.93 recorded GMV)
* **Clean Commercial Merchandise Ledger:** 522,544 line items across 19,773 invoices (£10,247,610.15 GMV)
* **Overall Cancellation Leakage Rate:** 8.05% of commercial transaction volume (£896,812.49 cancelled)
* **Guest Checkout Volume:** 135,080 raw rows (14.74% of clean merchandise revenue)

---

## 4-Way Ledger Separation Architecture

```
                                  ┌───────────────────────────────┐
                                  │      Raw Transactional        │
                                  │       Ledger (541,909)        │
                                  └───────────────┬───────────────┘
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 ▼                                ▼                                ▼
  ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐
  │   fct_order_items_clean     │  │  fct_cancellations_refunds  │  │ fct_inventory_adjustments   │
  │    522,544 rows / £10.25M   │  │    9,288 rows / -£896.81K   │  │    2,512 net / -£22.12K     │
  │  (Clean Commercial Sales)   │  │   ('C' Credit Note Slips)   │  │ (Damaged/Zero-Price Stocks) │
  └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘
                                                  │
                                                  ▼
                                   ┌─────────────────────────────┐
                                   │     fct_non_merchandise     │
                                   │     2,334 net / £394.50K    │
                                   │  (Postage, Fees, Discounts) │
                                   └─────────────────────────────┘
```

---

## Production Issues Log (ISS-01 through ISS-05)

| Issue ID | Category | Anomaly Description | Raw Rows | Invoices | Value (£) | Pipeline Treatment & Commercial Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ISS-01** | Structural Missingness | **Guest Checkouts (Missing CustomerID):** 135,080 rows lack a registered customer identifier. | 135,080 | 3,710 | £1,447,682.12 | **Retained in Primary Ledger with `is_guest_checkout = True`:** Dropping guest transactions would distort market basket co-occurrence and discard £1.45M (16.29%) in valid storefront purchasing activity. |
| **ISS-02** | Transaction Reversal | **Cancellations & Returns:** Invoices beginning with 'C' indicate credit cancellations and customer returns. | 9,288 | 3,836 | -£896,812.49 | **Isolated into `fct_cancellations_refunds.parquet`:** Preserved exclusively to compute SKU-level and portfolio-level Cancellation Leakage Rates (Guardrail 1). Excluded from forward sales basket mining. |
| **ISS-03** | Inventory Adjustments | **Un-cancelled Negative/Zero Quantities & Zero Prices:** Stock write-offs, damaged inventory adjustments, and unpriced promotional samples. | 2,517 | 2,157 | £-22,124.12 | **Isolated into `fct_inventory_adjustments.parquet`:** Excluded from commercial revenue and basket affinity modeling to prevent inventory audits from polluting product co-occurrence rules. |
| **ISS-04** | Non-Merchandise Fees | **Non-Product Accounting & Postage Codes:** Service line items (POST, DOT, M, BANK CHARGES, C2, D, CRUK, AMAZONFEE, PADS, B, S). | 2,940 | 2,770 | £-45,351.78 | **Isolated into `fct_non_merchandise.parquet`:** Excluded so shipping fees, carriage charges, and manual bookkeeping adjustments do not pollute merchandising association rules. |
| **ISS-05** | Redundant Data | **Exact Duplicate Line Items:** Duplicate order item rows recorded synchronously with identical attributes. | 5,268 | 2,748 | £21,740.98 | **Deduplicated:** Kept first occurrence and dropped exact redundant rows to maintain true line-item invoice grain. |

---

## Cleaned Data Lineage Verification

| Entity Name | Storage Path | Row Count | Primary Key | Key Attributes Added |
| :--- | :--- | :--- | :--- | :--- |
| **Clean Order Items** | `data/cleaned/fct_order_items_clean.parquet` | 522,544 | Composite (`InvoiceNo_str`, `StockCode_str`) | `line_total`, `is_guest_checkout`, `is_registered`, `clean_description` |
| **Orders Summary** | `data/cleaned/fct_orders_summary.parquet` | 19,773 | `InvoiceNo_str` | `basket_size_skus`, `total_units`, `order_revenue`, `basket_tier`, `detailed_basket_tier`, `is_uk` |
| **Cancellations & Refunds** | `data/cleaned/fct_cancellations_refunds.parquet` | 9,288 | Composite (`InvoiceNo_str`, `StockCode_str`) | Cancellation reason, absolute refunded value |
| **Inventory Adjustments** | `data/cleaned/fct_inventory_adjustments.parquet` | 2,512 | Composite (`InvoiceNo_str`, `StockCode_str`) | Adjustment category, quantity deficit |
| **Non-Merchandise Ledger** | `data/cleaned/fct_non_merchandise.parquet` | 2,334 | Composite (`InvoiceNo_str`, `StockCode_str`) | Service fee classification, postal charges |
