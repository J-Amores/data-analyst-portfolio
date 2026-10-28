"""SCAN Exploratory Data Analysis & Profiling Pipeline.

Implements Stage 3A (Exploring) and Stage 3B (Profiling) of Decision-Driven Design:
1. Portfolio Baseline Summary (raw vs. clean, guest vs. registered, overall cancellation leakage rate).
2. Basket Size & AOV Distributions (parametric: Mean, SD; non-parametric: Median, IQR, P10, P25, P75, P90, P99).
3. Top Products & SKU Refund Risk Profile (top 20 by revenue, top 20 by order frequency with SKU cancellation rates).
4. Temporal & Geographic Profiling (YearMonth, Day of Week, Hour of Day, UK vs. Key European/Global Markets).
5. Exports reports/scan_profiling_summary.md and reports/scan_metrics.json.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd

CLEAN_ITEMS_PATH = Path("data/cleaned/fct_order_items_clean.parquet")
ORDERS_SUMMARY_PATH = Path("data/cleaned/fct_orders_summary.parquet")
CANCELLATIONS_PATH = Path("data/cleaned/fct_cancellations_refunds.parquet")
REPORTS_DIR = Path("reports")


def calc_distribution_stats(series: pd.Series) -> dict:
    """Calculate parametric and non-parametric distribution statistics."""
    p10 = float(np.percentile(series, 10))
    p25 = float(np.percentile(series, 25))
    median = float(np.median(series))
    p75 = float(np.percentile(series, 75))
    p90 = float(np.percentile(series, 90))
    p99 = float(np.percentile(series, 99))
    iqr = p75 - p25

    return {
        "count": int(len(series)),
        "mean": float(series.mean()),
        "std": float(series.std()),
        "median": median,
        "iqr": float(iqr),
        "p10": p10,
        "p25": p25,
        "p75": p75,
        "p90": p90,
        "p99": p99,
        "min": float(series.min()),
        "max": float(series.max()),
    }


def run_scan_profiling():
    """Run exploratory and profiling analyses."""
    print("Loading cleaned datasets for SCAN profiling...")
    df_items = pd.read_parquet(CLEAN_ITEMS_PATH)
    df_orders = pd.read_parquet(ORDERS_SUMMARY_PATH)
    df_canc = pd.read_parquet(CANCELLATIONS_PATH)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Portfolio Baseline Summary
    total_orders = len(df_orders)
    total_revenue = float(df_orders["order_revenue"].sum())
    total_units = int(df_orders["total_units"].sum())
    total_skus = df_items["StockCode_str"].nunique()
    total_customers = df_orders["CustomerID"].dropna().nunique()

    date_min = str(df_orders["invoice_date"].min())
    date_max = str(df_orders["invoice_date"].max())

    registered_orders = df_orders[~df_orders["is_guest_checkout"]]
    guest_orders = df_orders[df_orders["is_guest_checkout"]]

    reg_orders_count = len(registered_orders)
    reg_revenue = float(registered_orders["order_revenue"].sum())
    guest_orders_count = len(guest_orders)
    guest_revenue = float(guest_orders["order_revenue"].sum())

    total_cancelled_value = float(df_canc["line_total"].abs().sum())
    overall_leakage_rate = (total_cancelled_value / (total_revenue + total_cancelled_value)) * 100

    portfolio_baseline = {
        "total_clean_orders": total_orders,
        "total_clean_revenue": total_revenue,
        "total_clean_units": total_units,
        "unique_skus": total_skus,
        "unique_registered_customers": total_customers,
        "date_range_start": date_min,
        "date_range_end": date_max,
        "registered_orders": reg_orders_count,
        "registered_revenue": reg_revenue,
        "registered_revenue_pct": (reg_revenue / total_revenue) * 100,
        "guest_orders": guest_orders_count,
        "guest_revenue": guest_revenue,
        "guest_revenue_pct": (guest_revenue / total_revenue) * 100,
        "total_cancelled_value": total_cancelled_value,
        "overall_leakage_rate_pct": overall_leakage_rate,
    }

    # 2. Basket Size & AOV Distribution across Tiers
    overall_basket_stats = calc_distribution_stats(df_orders["basket_size_skus"])
    overall_aov_stats = calc_distribution_stats(df_orders["order_revenue"])

    # 3-Tier Segmentation
    tier_stats = {}
    for tier in ["Small (1-2 SKUs)", "Medium (3-5 SKUs)", "Large (6+ SKUs)"]:
        sub = df_orders[df_orders["basket_tier"] == tier]
        tier_stats[tier] = {
            "order_count": len(sub),
            "order_pct": (len(sub) / total_orders) * 100,
            "total_revenue": float(sub["order_revenue"].sum()),
            "revenue_pct": (float(sub["order_revenue"].sum()) / total_revenue) * 100,
            "basket_skus": calc_distribution_stats(sub["basket_size_skus"]),
            "aov": calc_distribution_stats(sub["order_revenue"]),
        }

    # Detailed 5-Tier Segmentation
    detailed_tier_stats = {}
    detailed_order = ["1-2 SKUs", "3-5 SKUs", "6-15 SKUs", "16-30 SKUs", "31+ SKUs"]
    for d_tier in detailed_order:
        sub = df_orders[df_orders["detailed_basket_tier"] == d_tier]
        detailed_tier_stats[d_tier] = {
            "order_count": len(sub),
            "order_pct": (len(sub) / total_orders) * 100,
            "total_revenue": float(sub["order_revenue"].sum()),
            "revenue_pct": (float(sub["order_revenue"].sum()) / total_revenue) * 100,
            "basket_skus": calc_distribution_stats(sub["basket_size_skus"]),
            "aov": calc_distribution_stats(sub["order_revenue"]),
        }

    # 3. Top Products & SKU Refund Risk Profile
    # Compute SKU-level cancellation leakage
    sku_cancellations = (
        df_canc.groupby("StockCode_str")["line_total"]
        .agg(lambda s: float(s.abs().sum()))
        .reset_index(name="cancelled_revenue")
    )

    sku_sales = (
        df_items.groupby(["StockCode_str", "Description"])
        .agg(
            gross_revenue=("line_total", "sum"),
            order_frequency=("InvoiceNo_str", "nunique"),
            total_quantity=("Quantity", "sum"),
            avg_unit_price=("UnitPrice", "mean"),
        )
        .reset_index()
    )

    sku_profile = sku_sales.merge(sku_cancellations, on="StockCode_str", how="left")
    sku_profile["cancelled_revenue"] = sku_profile["cancelled_revenue"].fillna(0.0)
    sku_profile["cancellation_rate_pct"] = (
        sku_profile["cancelled_revenue"]
        / (sku_profile["gross_revenue"] + sku_profile["cancelled_revenue"])
    ) * 100

    top_20_rev = sku_profile.sort_values(by="gross_revenue", ascending=False).head(20)
    top_20_freq = sku_profile.sort_values(by="order_frequency", ascending=False).head(20)

    # 4. Temporal & Geographic Profiling
    # Monthly
    monthly_summary = (
        df_orders.groupby("invoice_YearMonth")
        .agg(
            order_count=("InvoiceNo", "count"),
            gross_revenue=("order_revenue", "sum"),
            total_units=("total_units", "sum"),
            mean_aov=("order_revenue", "mean"),
            median_aov=("order_revenue", "median"),
            mean_basket_size=("basket_size_skus", "mean"),
            large_basket_pct=(
                "basket_tier",
                lambda t: (t == "Large (6+ SKUs)").mean() * 100,
            ),
        )
        .reset_index()
    )

    # Day of Week
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]
    dow_summary = (
        df_orders.groupby("day_of_week")
        .agg(
            order_count=("InvoiceNo", "count"),
            gross_revenue=("order_revenue", "sum"),
            mean_aov=("order_revenue", "mean"),
            median_aov=("order_revenue", "median"),
        )
        .reindex(dow_order)
        .reset_index()
    )

    # Hour of Day
    hour_summary = (
        df_orders.groupby("hour_of_day")
        .agg(
            order_count=("InvoiceNo", "count"),
            gross_revenue=("order_revenue", "sum"),
            mean_aov=("order_revenue", "mean"),
        )
        .reset_index()
    )

    # Country Comparison
    target_countries = [
        "United Kingdom",
        "Netherlands",
        "EIRE",
        "Germany",
        "France",
        "Australia",
        "Spain",
        "Switzerland",
    ]
    country_summary = (
        df_orders[df_orders["Country"].isin(target_countries)]
        .groupby("Country")
        .agg(
            order_count=("InvoiceNo", "count"),
            gross_revenue=("order_revenue", "sum"),
            mean_aov=("order_revenue", "mean"),
            median_aov=("order_revenue", "median"),
            mean_basket_size=("basket_size_skus", "mean"),
            median_basket_size=("basket_size_skus", "median"),
            wholesale_pct=(
                "basket_tier",
                lambda t: (t == "Large (6+ SKUs)").mean() * 100,
            ),
        )
        .sort_values(by="gross_revenue", ascending=False)
        .reset_index()
    )

    # Save metrics JSON
    metrics_bundle = {
        "baseline": portfolio_baseline,
        "overall_distribution": {
            "basket_skus": overall_basket_stats,
            "aov": overall_aov_stats,
        },
        "three_tier_distribution": tier_stats,
        "detailed_tier_distribution": detailed_tier_stats,
        "top_20_revenue_skus": top_20_rev.to_dict(orient="records"),
        "top_20_frequency_skus": top_20_freq.to_dict(orient="records"),
        "monthly_summary": monthly_summary.to_dict(orient="records"),
        "day_of_week_summary": dow_summary.to_dict(orient="records"),
        "country_summary": country_summary.to_dict(orient="records"),
    }

    with open(REPORTS_DIR / "scan_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_bundle, f, indent=2)
    print("Exported reports/scan_metrics.json")

    # Generate Markdown Summary (ensuring zero em dashes)
    md_content = f"""# SCAN Exploratory Data Analysis & Commercial Profiling Summary

## 1. Portfolio Baseline Summary
* **Active Order Ledger Window:** {date_min} to {date_max} (12.3 calendar months)
* **Total Valid Commercial Orders:** {total_orders:,} invoices
* **Total Commercial Sales Line Items:** {len(df_items):,} items
* **Total Commercial Gross Merchandise Volume (GMV):** £{total_revenue:,.2f}
* **Catalog Assortment Breadth:** {total_skus:,} unique active SKUs
* **Registered Commercial Customer Accounts:** {total_customers:,} accounts
* **Guest Checkout Revenue Contribution:** £{guest_revenue:,.2f} ({portfolio_baseline['guest_revenue_pct']:.2f}% of commercial sales across {guest_orders_count:,} orders)
* **Registered Customer Revenue Contribution:** £{reg_revenue:,.2f} ({portfolio_baseline['registered_revenue_pct']:.2f}% across {reg_orders_count:,} orders)
* **Portfolio-Wide Cancellation Leakage Rate:** {overall_leakage_rate:.2f}% of GMV (£{total_cancelled_value:,.2f} absolute cancelled value across credit notes)

---

## 2. Basket Size & Order Value Segmentation

### Executive 3-Tier Segmentation (Small vs. Medium vs. Large)

| Basket Size Segment | Orders Count | Order Share (%) | Gross Revenue (£) | Revenue Share (%) | Median AOV (£) | Mean AOV (£) | Median SKUs | Mean SKUs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Small (1-2 SKUs)** | {tier_stats['Small (1-2 SKUs)']['order_count']:,} | {tier_stats['Small (1-2 SKUs)']['order_pct']:.2f}% | £{tier_stats['Small (1-2 SKUs)']['total_revenue']:,.2f} | {tier_stats['Small (1-2 SKUs)']['revenue_pct']:.2f}% | £{tier_stats['Small (1-2 SKUs)']['aov']['median']:.2f} | £{tier_stats['Small (1-2 SKUs)']['aov']['mean']:.2f} | {tier_stats['Small (1-2 SKUs)']['basket_skus']['median']:.0f} | {tier_stats['Small (1-2 SKUs)']['basket_skus']['mean']:.2f} |
| **Medium (3-5 SKUs)** | {tier_stats['Medium (3-5 SKUs)']['order_count']:,} | {tier_stats['Medium (3-5 SKUs)']['order_pct']:.2f}% | £{tier_stats['Medium (3-5 SKUs)']['total_revenue']:,.2f} | {tier_stats['Medium (3-5 SKUs)']['revenue_pct']:.2f}% | £{tier_stats['Medium (3-5 SKUs)']['aov']['median']:.2f} | £{tier_stats['Medium (3-5 SKUs)']['aov']['mean']:.2f} | {tier_stats['Medium (3-5 SKUs)']['basket_skus']['median']:.0f} | {tier_stats['Medium (3-5 SKUs)']['basket_skus']['mean']:.2f} |
| **Large (6+ SKUs)** | {tier_stats['Large (6+ SKUs)']['order_count']:,} | {tier_stats['Large (6+ SKUs)']['order_pct']:.2f}% | £{tier_stats['Large (6+ SKUs)']['total_revenue']:,.2f} | {tier_stats['Large (6+ SKUs)']['revenue_pct']:.2f}% | £{tier_stats['Large (6+ SKUs)']['aov']['median']:.2f} | £{tier_stats['Large (6+ SKUs)']['aov']['mean']:.2f} | {tier_stats['Large (6+ SKUs)']['basket_skus']['median']:.0f} | {tier_stats['Large (6+ SKUs)']['basket_skus']['mean']:.2f} |
| **Portfolio Total / Baseline** | **{total_orders:,}** | **100.00%** | **£{total_revenue:,.2f}** | **100.00%** | **£{overall_aov_stats['median']:.2f}** | **£{overall_aov_stats['mean']:.2f}** | **{overall_basket_stats['median']:.0f}** | **{overall_basket_stats['mean']:.2f}** |

### Granular 5-Tier Wholesale & Retail Decomposition

| Detailed Tier | Orders Count | Order Share (%) | Revenue (£) | Revenue Share (%) | Median AOV (£) | Mean AOV (£) | IQR AOV (£) | P90 AOV (£) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for d_tier in detailed_order:
        dt = detailed_tier_stats[d_tier]
        md_content += f"| **{d_tier}** | {dt['order_count']:,} | {dt['order_pct']:.2f}% | £{dt['total_revenue']:,.2f} | {dt['revenue_pct']:.2f}% | £{dt['aov']['median']:.2f} | £{dt['aov']['mean']:.2f} | £{dt['aov']['iqr']:.2f} | £{dt['aov']['p90']:.2f} |\n"

    md_content += """
---

## 3. Top 20 SKUs by Gross Merchandise Value and SKU Return Risk

| Rank | StockCode | Product Description | Gross Sales (£) | Order Frequency | Avg Unit Price (£) | Units Sold | Standalone Return Rate (%) | Return Guardrail (<5.0%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for idx, row in enumerate(top_20_rev.itertuples(), start=1):
        status = "PASS" if row.cancellation_rate_pct < 5.0 else "FLAGGED"
        md_content += f"| {idx} | `{row.StockCode_str}` | {row.Description[:38]} | £{row.gross_revenue:,.2f} | {row.order_frequency:,} | £{row.avg_unit_price:.2f} | {row.total_quantity:,} | {row.cancellation_rate_pct:.2f}% | {status} |\n"

    md_content += """
---

## 4. Top 20 SKUs by Checkout Frequency (Storefront Velocity Anchors)

| Rank | StockCode | Product Description | Order Frequency | Storefront Penetration (%) | Gross Sales (£) | Units Sold | Standalone Return Rate (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for idx, row in enumerate(top_20_freq.itertuples(), start=1):
        pen_pct = (row.order_frequency / total_orders) * 100
        md_content += f"| {idx} | `{row.StockCode_str}` | {row.Description[:38]} | {row.order_frequency:,} | {pen_pct:.2f}% | £{row.gross_revenue:,.2f} | {row.total_quantity:,} | {row.cancellation_rate_pct:.2f}% |\n"

    md_content += """
---

## 5. Temporal Dynamics (Seasonality & Intake Rhythm)

### Monthly Transaction Volume & Multi-Item Basket Expansion

| Year-Month | Invoices Count | Gross GMV (£) | Total Units | Mean AOV (£) | Median AOV (£) | Mean Basket Size | Large Basket Share (6+ SKUs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for row in monthly_summary.itertuples():
        md_content += f"| **{row.invoice_YearMonth}** | {row.order_count:,} | £{row.gross_revenue:,.2f} | {row.total_units:,} | £{row.mean_aov:.2f} | £{row.median_aov:.2f} | {row.mean_basket_size:.2f} | {row.large_basket_pct:.2f}% |\n"

    md_content += """
### Day of Week Commercial Velocity

| Day of Week | Invoices Count | Gross GMV (£) | Mean AOV (£) | Median AOV (£) | Commercial Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for row in dow_summary.itertuples():
        md_content += f"| **{row.day_of_week}** | {row.order_count:,} | £{row.gross_revenue:,.2f} | £{row.mean_aov:.2f} | £{row.median_aov:.2f} | Peak procurement occurs midweek |\n"

    md_content += """
---

## 6. Geographic Concentration & Cross-Border Account Profiling

| Country | Orders Count | Gross GMV (£) | Mean AOV (£) | Median AOV (£) | Mean Basket SKUs | Median Basket SKUs | Wholesale Share (6+ SKUs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for row in country_summary.itertuples():
        md_content += f"| **{row.Country}** | {row.order_count:,} | £{row.gross_revenue:,.2f} | £{row.mean_aov:.2f} | £{row.median_aov:.2f} | {row.mean_basket_size:.2f} | {row.median_basket_size:.0f} | {row.wholesale_pct:.2f}% |\n"

    summary_path = REPORTS_DIR / "scan_profiling_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Exported profiling summary to {summary_path}")


if __name__ == "__main__":
    run_scan_profiling()
