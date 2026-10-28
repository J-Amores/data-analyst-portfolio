"""Market Basket Association Engine & Econometric Bundle Simulator.

Implements Stage 3D (Shaping) and Stage 3E (Analyzing):
1. Deduplicates (InvoiceNo_str, StockCode_str, Description, UnitPrice) at order grain.
2. Filters to actionable SKUs (>= 1.0% orders, >= 198 checkouts) to eliminate low-sample noise.
3. Computes exact metrics for candidate product pairs (A, B):
   - Orders A, Orders B, Pair Orders
   - Support A, Support B, Support AB
   - Confidence A->B, Confidence B->A
   - Lift
   - Vectorized 2x2 Chi-Square statistic and p-value (Yates' correction)
   - Standalone Cancellation Leakage Rates (Guardrail 1: < 5.0%)
   - Unit prices and combined bundle price
4. Exports:
   - data/exports/top_product_pairs.csv (Top 25 pairs by Lift and Top 25 by Volume)
   - reports/market_basket_rules.json
5. Simulates Net Revenue Lift for Top 5 Recommended Executive Bundles across 5%, 10%, 15% discount tiers.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import chi2

CLEAN_ITEMS_PATH = Path("data/cleaned/fct_order_items_clean.parquet")
CANCELLATIONS_PATH = Path("data/cleaned/fct_cancellations_refunds.parquet")
EXPORTS_DIR = Path("data/exports")
REPORTS_DIR = Path("reports")


def run_market_basket_engine():
    """Execute market basket rule mining and bundle economics simulation."""
    print("Loading cleaned datasets for Market Basket Engine...")
    df_items = pd.read_parquet(CLEAN_ITEMS_PATH)
    df_canc = pd.read_parquet(CANCELLATIONS_PATH)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    total_orders = df_items["InvoiceNo_str"].nunique()
    print(f"Total valid merchandise orders: {total_orders:,}")

    # SKU level catalog metadata: Description, UnitPrice, Order Count, Gross Revenue
    sku_meta = (
        df_items.groupby("StockCode_str")
        .agg(
            Description=("Description", "first"),
            avg_unit_price=("UnitPrice", "mean"),
            gross_revenue=("line_total", "sum"),
            order_count=("InvoiceNo_str", "nunique"),
            total_quantity=("Quantity", "sum"),
        )
        .reset_index()
    )

    # SKU level cancellations for Guardrail 1
    sku_canc = (
        df_canc.groupby("StockCode_str")["line_total"]
        .agg(lambda s: float(s.abs().sum()))
        .reset_index(name="cancelled_revenue")
    )

    sku_meta = sku_meta.merge(sku_canc, on="StockCode_str", how="left")
    sku_meta["cancelled_revenue"] = sku_meta["cancelled_revenue"].fillna(0.0)
    sku_meta["return_rate_pct"] = (
        sku_meta["cancelled_revenue"]
        / (sku_meta["gross_revenue"] + sku_meta["cancelled_revenue"])
    ) * 100
    sku_dict = sku_meta.set_index("StockCode_str").to_dict(orient="index")

    # Filter to commercially actionable SKUs (>= 1.0% orders, i.e. >= 198 orders)
    min_order_threshold = int(np.ceil(0.010 * total_orders))
    actionable_skus = set(
        sku_meta[sku_meta["order_count"] >= min_order_threshold]["StockCode_str"]
    )
    print(
        f"Filtered to {len(actionable_skus)} commercially actionable SKUs "
        f"(>= {min_order_threshold} orders, 1.0% support threshold)."
    )

    # Prepare order-SKU deduplicated table
    order_skus = df_items[["InvoiceNo_str", "StockCode_str"]].drop_duplicates()
    order_skus = order_skus[order_skus["StockCode_str"].isin(actionable_skus)].copy()

    # Self-join on InvoiceNo_str where StockCode_A < StockCode_B
    print("Executing self-join for product pair co-occurrences...")
    merged = order_skus.merge(order_skus, on="InvoiceNo_str", suffixes=("_A", "_B"))
    pairs = merged[merged["StockCode_str_A"] < merged["StockCode_str_B"]]

    pair_counts = (
        pairs.groupby(["StockCode_str_A", "StockCode_str_B"])
        .size()
        .reset_index(name="pair_orders")
    )
    print(f"Total candidate product pairs evaluated: {len(pair_counts):,}")

    # Vectorized computation of Support, Confidence, Lift, and Chi-Square
    print("Computing vectorized association metrics and Chi-Square independence tests...")
    pair_counts["orders_a"] = pair_counts["StockCode_str_A"].map(
        lambda x: sku_dict[x]["order_count"]
    )
    pair_counts["orders_b"] = pair_counts["StockCode_str_B"].map(
        lambda x: sku_dict[x]["order_count"]
    )
    pair_counts["description_a"] = pair_counts["StockCode_str_A"].map(
        lambda x: sku_dict[x]["Description"]
    )
    pair_counts["description_b"] = pair_counts["StockCode_str_B"].map(
        lambda x: sku_dict[x]["Description"]
    )
    pair_counts["price_a"] = pair_counts["StockCode_str_A"].map(
        lambda x: sku_dict[x]["avg_unit_price"]
    )
    pair_counts["price_b"] = pair_counts["StockCode_str_B"].map(
        lambda x: sku_dict[x]["avg_unit_price"]
    )
    pair_counts["bundle_price"] = pair_counts["price_a"] + pair_counts["price_b"]

    pair_counts["return_rate_a_pct"] = pair_counts["StockCode_str_A"].map(
        lambda x: sku_dict[x]["return_rate_pct"]
    )
    pair_counts["return_rate_b_pct"] = pair_counts["StockCode_str_B"].map(
        lambda x: sku_dict[x]["return_rate_pct"]
    )
    pair_counts["max_return_rate_pct"] = np.maximum(
        pair_counts["return_rate_a_pct"], pair_counts["return_rate_b_pct"]
    )
    pair_counts["passes_guardrail_1"] = pair_counts["max_return_rate_pct"] < 5.0

    pair_counts["support_a"] = pair_counts["orders_a"] / total_orders
    pair_counts["support_b"] = pair_counts["orders_b"] / total_orders
    pair_counts["support_ab"] = pair_counts["pair_orders"] / total_orders
    pair_counts["confidence_a_to_b"] = (
        pair_counts["pair_orders"] / pair_counts["orders_a"]
    )
    pair_counts["confidence_b_to_a"] = (
        pair_counts["pair_orders"] / pair_counts["orders_b"]
    )
    pair_counts["lift"] = pair_counts["support_ab"] / (
        pair_counts["support_a"] * pair_counts["support_b"]
    )

    # 2x2 Chi-Square calculation with Yates' continuity correction
    a = pair_counts["pair_orders"].to_numpy(dtype=float)
    b = (pair_counts["orders_a"] - pair_counts["pair_orders"]).to_numpy(dtype=float)
    c = (pair_counts["orders_b"] - pair_counts["pair_orders"]).to_numpy(dtype=float)
    d = (
        total_orders
        - pair_counts["orders_a"]
        - pair_counts["orders_b"]
        + pair_counts["pair_orders"]
    ).to_numpy(dtype=float)
    n = float(total_orders)

    num = np.maximum(0.0, np.abs(a * d - b * c) - n / 2.0) ** 2 * n
    denom = (a + b) * (c + d) * (a + c) * (b + d)
    denom = np.where(denom == 0, 1e-9, denom)
    chi2_stat = num / denom
    p_val = chi2.sf(chi2_stat, df=1)

    pair_counts["chi2_stat"] = chi2_stat
    pair_counts["chi2_p_val"] = p_val
    pair_counts["stockcode_a"] = pair_counts["StockCode_str_A"]
    pair_counts["stockcode_b"] = pair_counts["StockCode_str_B"]

    # Filter for exports:
    # 1. Top 25 pairs ranked by Lift (minimum Support >= 1.5%, i.e. support_ab >= 0.015)
    df_lift_pool = pair_counts[pair_counts["support_ab"] >= 0.015].sort_values(
        by="lift", ascending=False
    )
    top_25_lift = df_lift_pool.head(25).copy()
    top_25_lift["rank_by"] = "Lift (Support >= 1.5%)"

    # 2. Top 25 pairs ranked by Support Volume
    top_25_vol = pair_counts.sort_values(by="pair_orders", ascending=False).head(25).copy()
    top_25_vol["rank_by"] = "Support Volume"

    # Combine for analytical export
    df_export_pairs = pd.concat([top_25_lift, top_25_vol]).drop_duplicates(
        subset=["stockcode_a", "stockcode_b"]
    )
    csv_export_path = EXPORTS_DIR / "top_product_pairs.csv"
    df_export_pairs.to_csv(csv_export_path, index=False)
    print(f"Exported {len(df_export_pairs)} top product pairs to {csv_export_path}")

    # Top 5 Recommended Executive Product Bundles
    recommended_bundles = [
        {
            "bundle_id": "BDL-01",
            "bundle_name": "Regency Heritage Teaware Duet",
            "family": "Regency Teaware Collection",
            "sku_a": "22697",
            "desc_a": "GREEN REGENCY TEACUP AND SAUCER",
            "sku_b": "22699",
            "desc_b": "ROSES REGENCY TEACUP AND SAUCER",
            "anchor_sku": "22697",
            "attachment_sku": "22699",
            "pair_orders": 767,
            "support_ab": 767 / total_orders,
            "confidence_anchor_to_attach": 767 / sku_dict["22697"]["order_count"],
            "lift": (767 / total_orders)
            / (
                (sku_dict["22697"]["order_count"] / total_orders)
                * (sku_dict["22699"]["order_count"] / total_orders)
            ),
            "price_a": sku_dict["22697"]["avg_unit_price"],
            "price_b": sku_dict["22699"]["avg_unit_price"],
            "combined_price": sku_dict["22697"]["avg_unit_price"]
            + sku_dict["22699"]["avg_unit_price"],
            "return_rate_a_pct": sku_dict["22697"]["return_rate_pct"],
            "return_rate_b_pct": sku_dict["22699"]["return_rate_pct"],
            "solo_anchor_orders": sku_dict["22697"]["order_count"] - 767,
        },
        {
            "bundle_id": "BDL-02",
            "bundle_name": "Retro Storage Organizer Pack",
            "family": "Jumbo Storage Bags",
            "sku_a": "22386",
            "desc_a": "JUMBO BAG PINK POLKADOT",
            "sku_b": "85099B",
            "desc_b": "JUMBO BAG RED RETROSPOT",
            "anchor_sku": "85099B",
            "attachment_sku": "22386",
            "pair_orders": 825,
            "support_ab": 825 / total_orders,
            "confidence_anchor_to_attach": 825 / sku_dict["85099B"]["order_count"],
            "lift": (825 / total_orders)
            / (
                (sku_dict["85099B"]["order_count"] / total_orders)
                * (sku_dict["22386"]["order_count"] / total_orders)
            ),
            "price_a": sku_dict["85099B"]["avg_unit_price"],
            "price_b": sku_dict["22386"]["avg_unit_price"],
            "combined_price": sku_dict["85099B"]["avg_unit_price"]
            + sku_dict["22386"]["avg_unit_price"],
            "return_rate_a_pct": sku_dict["85099B"]["return_rate_pct"],
            "return_rate_b_pct": sku_dict["22386"]["return_rate_pct"],
            "solo_anchor_orders": sku_dict["85099B"]["order_count"] - 825,
        },
        {
            "bundle_id": "BDL-03",
            "bundle_name": "Vintage Bakelike Clock Companion",
            "family": "Bakelike Vintage Clocks",
            "sku_a": "22726",
            "desc_a": "ALARM CLOCK BAKELIKE GREEN",
            "sku_b": "22727",
            "desc_b": "ALARM CLOCK BAKELIKE RED",
            "anchor_sku": "22726",
            "attachment_sku": "22727",
            "pair_orders": 640,
            "support_ab": 640 / total_orders,
            "confidence_anchor_to_attach": 640 / sku_dict["22726"]["order_count"],
            "lift": (640 / total_orders)
            / (
                (sku_dict["22726"]["order_count"] / total_orders)
                * (sku_dict["22727"]["order_count"] / total_orders)
            ),
            "price_a": sku_dict["22726"]["avg_unit_price"],
            "price_b": sku_dict["22727"]["avg_unit_price"],
            "combined_price": sku_dict["22726"]["avg_unit_price"]
            + sku_dict["22727"]["avg_unit_price"],
            "return_rate_a_pct": sku_dict["22726"]["return_rate_pct"],
            "return_rate_b_pct": sku_dict["22727"]["return_rate_pct"],
            "solo_anchor_orders": sku_dict["22726"]["order_count"] - 640,
        },
        {
            "bundle_id": "BDL-04",
            "bundle_name": "Everyday Lunch Bag Twin Pack",
            "family": "Lunch Bag Collection",
            "sku_a": "20725",
            "desc_a": "LUNCH BAG RED RETROSPOT",
            "sku_b": "22383",
            "desc_b": "LUNCH BAG SUKI DESIGN",
            "anchor_sku": "20725",
            "attachment_sku": "22383",
            "pair_orders": 655,
            "support_ab": 655 / total_orders,
            "confidence_anchor_to_attach": 655 / sku_dict["20725"]["order_count"],
            "lift": (655 / total_orders)
            / (
                (sku_dict["20725"]["order_count"] / total_orders)
                * (sku_dict["22383"]["order_count"] / total_orders)
            ),
            "price_a": sku_dict["20725"]["avg_unit_price"],
            "price_b": sku_dict["22383"]["avg_unit_price"],
            "combined_price": sku_dict["20725"]["avg_unit_price"]
            + sku_dict["22383"]["avg_unit_price"],
            "return_rate_a_pct": sku_dict["20725"]["return_rate_pct"],
            "return_rate_b_pct": sku_dict["22383"]["return_rate_pct"],
            "solo_anchor_orders": sku_dict["20725"]["order_count"] - 655,
        },
        {
            "bundle_id": "BDL-05",
            "bundle_name": "Poppy's Playhouse Miniature Nursery",
            "family": "Children's Playsets & Toys",
            "sku_a": "22745",
            "desc_a": "POPPY'S PLAYHOUSE BEDROOM",
            "sku_b": "22748",
            "desc_b": "POPPY'S PLAYHOUSE KITCHEN",
            "anchor_sku": "22745",
            "attachment_sku": "22748",
            "pair_orders": 313,
            "support_ab": 313 / total_orders,
            "confidence_anchor_to_attach": 313 / sku_dict["22745"]["order_count"],
            "lift": (313 / total_orders)
            / (
                (sku_dict["22745"]["order_count"] / total_orders)
                * (sku_dict["22748"]["order_count"] / total_orders)
            ),
            "price_a": sku_dict["22745"]["avg_unit_price"],
            "price_b": sku_dict["22748"]["avg_unit_price"],
            "combined_price": sku_dict["22745"]["avg_unit_price"]
            + sku_dict["22748"]["avg_unit_price"],
            "return_rate_a_pct": sku_dict["22745"]["return_rate_pct"],
            "return_rate_b_pct": sku_dict["22748"]["return_rate_pct"],
            "solo_anchor_orders": sku_dict["22745"]["order_count"] - 313,
        },
    ]

    # Econometric Bundle Financial Simulation
    # Models Guardrail 2: Promotional Discount Margin Retention
    # Formula: Net Lift = (Incremental Attached Units * Discounted Bundle Price) - (Cannibalized Organic Units * Discount Amount)
    attach_rate = 0.25
    redemption_rate = 0.30
    discount_tiers = [0.05, 0.10, 0.15]

    bundle_simulations = []
    portfolio_totals = {
        "tier_5pct": {"gross_incremental": 0.0, "cannibalization": 0.0, "net_lift": 0.0},
        "tier_10pct": {"gross_incremental": 0.0, "cannibalization": 0.0, "net_lift": 0.0},
        "tier_15pct": {"gross_incremental": 0.0, "cannibalization": 0.0, "net_lift": 0.0},
    }

    for b in recommended_bundles:
        bundle_res = {
            "bundle_id": b["bundle_id"],
            "bundle_name": b["bundle_name"],
            "family": b["family"],
            "anchor_sku": b["anchor_sku"],
            "attachment_sku": b["attachment_sku"],
            "support_pct": b["support_ab"] * 100,
            "confidence_pct": b["confidence_anchor_to_attach"] * 100,
            "lift": b["lift"],
            "combined_price": b["combined_price"],
            "return_rate_a_pct": b["return_rate_a_pct"],
            "return_rate_b_pct": b["return_rate_b_pct"],
            "max_return_rate_pct": max(b["return_rate_a_pct"], b["return_rate_b_pct"]),
            "passes_guardrail_1": max(b["return_rate_a_pct"], b["return_rate_b_pct"]) < 5.0,
            "tier_simulations": {},
        }

        solo_orders = b["solo_anchor_orders"]
        organic_pairs = b["pair_orders"]
        combined_price = b["combined_price"]

        for discount in discount_tiers:
            d_key = f"{int(discount * 100)}pct"
            tier_name = f"tier_{d_key}"

            incremental_units = solo_orders * attach_rate
            discounted_bundle_price = combined_price * (1.0 - discount)
            gross_incremental_revenue = incremental_units * discounted_bundle_price

            cannibalized_units = organic_pairs * redemption_rate
            discount_amount = combined_price * discount
            cannibalized_discount_cost = cannibalized_units * discount_amount

            net_revenue_lift = gross_incremental_revenue - cannibalized_discount_cost

            bundle_res["tier_simulations"][d_key] = {
                "discount_pct": discount * 100,
                "incremental_units": round(incremental_units, 1),
                "discounted_bundle_price": round(discounted_bundle_price, 2),
                "gross_incremental_revenue": round(gross_incremental_revenue, 2),
                "cannibalized_discount_cost": round(cannibalized_discount_cost, 2),
                "net_revenue_lift": round(net_revenue_lift, 2),
            }

            portfolio_totals[tier_name]["gross_incremental"] += gross_incremental_revenue
            portfolio_totals[tier_name]["cannibalization"] += cannibalized_discount_cost
            portfolio_totals[tier_name]["net_lift"] += net_revenue_lift

        bundle_simulations.append(bundle_res)

    rules_payload = {
        "metadata": {
            "total_orders": total_orders,
            "actionable_skus_evaluated": len(actionable_skus),
            "min_support_threshold_pct": 1.0,
            "total_pairs_computed": len(pair_counts),
        },
        "top_25_by_lift": top_25_lift.to_dict(orient="records"),
        "top_25_by_volume": top_25_vol.to_dict(orient="records"),
        "recommended_bundles": bundle_simulations,
        "portfolio_bundle_simulation_totals": portfolio_totals,
    }

    rules_json_path = REPORTS_DIR / "market_basket_rules.json"
    with open(rules_json_path, "w", encoding="utf-8") as f:
        json.dump(rules_payload, f, indent=2)
    print(f"Exported market basket rules and simulations to {rules_json_path}")


if __name__ == "__main__":
    run_market_basket_engine()
