"""
src/presentation/export_cockpit_data.py
Exports the verified Phase 1 empirical data cube to data/exports/cockpit_bundle_cube.json.
Powers the interactive merchandising decision cockpit (cockpit.html).
Follows Christine Jiang's Decision-Driven Design principles with zero em dashes.
"""
from pathlib import Path
import json

EXPORTS_DIR = Path("data/exports")
OUTPUT_PATH = EXPORTS_DIR / "cockpit_bundle_cube.json"


def export_cockpit_cube():
    """Build and write the self-contained interactive bundle cube."""
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    cube = {
        "metadata": {
            "title": "E-Commerce Merchandising, Basket Profitability & Cross-Sell Engine Data Cube",
            "version": "2.0.0",
            "generated_date": "2026-10-27",
            "source_ledger": "Online Retail.xlsx",
            "governance_pipeline": "CLEAN 5-Step Architecture"
        },
        "portfolio_baseline": {
            "raw_rows": 541909,
            "clean_rows": 522544,
            "valid_orders": 19773,
            "commercial_gmv": 10247610.15,
            "cancelled_value": -896812.49,
            "cancellation_leakage_pct": 8.05,
            "guest_revenue": 1510382.51,
            "guest_share_pct": 14.74,
            "multi_sku_order_share_pct": 77.9,
            "multi_sku_revenue_share_pct": 86.8,
            "single_item_median_aov": 45.00,
            "multi_item_median_aov": 308.60,
            "small_tier_median_aov": 57.60,
            "large_tier_median_aov": 322.30,
            "median_aov_multiplier": 5.6
        },
        "basket_tiers": [
            {
                "tier_id": "small",
                "label": "Small (1-2 SKUs)",
                "median_aov": 57.60,
                "mean_aov": 307.19,
                "order_share_pct": 11.7,
                "rev_share_pct": 6.9,
                "color": "#64748B"
            },
            {
                "tier_id": "medium",
                "label": "Medium (3-5 SKUs)",
                "median_aov": 140.85,
                "mean_aov": 316.39,
                "order_share_pct": 10.3,
                "rev_share_pct": 6.3,
                "color": "#64748B"
            },
            {
                "tier_id": "large",
                "label": "Large (6-15 SKUs)",
                "median_aov": 230.43,
                "mean_aov": 377.02,
                "order_share_pct": 28.4,
                "rev_share_pct": 20.7,
                "color": "#059669"
            },
            {
                "tier_id": "wholesale",
                "label": "Wholesale (16+ SKUs)",
                "median_aov": 389.72,
                "mean_aov": 691.20,
                "order_share_pct": 49.5,
                "rev_share_pct": 66.1,
                "color": "#059669"
            }
        ],
        "bundles": [
            {
                "bundle_id": "BDL-01",
                "bundle_name": "Regency Heritage Teaware Duet",
                "family": "Regency Teaware Collection",
                "anchor_sku": "22697",
                "anchor_desc": "GREEN REGENCY TEACUP AND SAUCER",
                "attachment_sku": "22699",
                "attachment_desc": "ROSES REGENCY TEACUP AND SAUCER",
                "support_pct": 3.88,
                "confidence_pct": 75.72,
                "lift": 14.06,
                "price_a": 3.84,
                "price_b": 3.66,
                "combined_price": 7.50,
                "return_rate_a_pct": 1.70,
                "return_rate_b_pct": 3.81,
                "max_return_rate_pct": 3.81,
                "passes_guardrail_1": True,
                "anchor_orders": 1013,
                "pair_orders": 767,
                "solo_anchor_orders": 246,
                "tier_simulations": {
                    "5pct": {
                        "discount_pct": 5.0,
                        "incremental_units": 61.5,
                        "discounted_bundle_price": 7.12,
                        "gross_incremental_revenue": 438.00,
                        "cannibalized_discount_cost": 86.25,
                        "net_revenue_lift": 351.75
                    },
                    "10pct": {
                        "discount_pct": 10.0,
                        "incremental_units": 61.5,
                        "discounted_bundle_price": 6.75,
                        "gross_incremental_revenue": 414.95,
                        "cannibalized_discount_cost": 172.50,
                        "net_revenue_lift": 242.45
                    },
                    "15pct": {
                        "discount_pct": 15.0,
                        "incremental_units": 61.5,
                        "discounted_bundle_price": 6.37,
                        "gross_incremental_revenue": 391.89,
                        "cannibalized_discount_cost": 258.75,
                        "net_revenue_lift": 133.14
                    }
                }
            },
            {
                "bundle_id": "BDL-02",
                "bundle_name": "Retro Storage Organizer Pack",
                "family": "Jumbo Storage Bags",
                "anchor_sku": "85099B",
                "anchor_desc": "JUMBO BAG RED RETROSPOT",
                "attachment_sku": "22386",
                "attachment_desc": "JUMBO BAG PINK POLKADOT",
                "support_pct": 4.17,
                "confidence_pct": 39.49,
                "lift": 6.41,
                "price_a": 2.49,
                "price_b": 2.60,
                "combined_price": 5.08,
                "return_rate_a_pct": 2.06,
                "return_rate_b_pct": 1.89,
                "max_return_rate_pct": 2.06,
                "passes_guardrail_1": True,
                "anchor_orders": 2089,
                "pair_orders": 825,
                "solo_anchor_orders": 1264,
                "tier_simulations": {
                    "5pct": {
                        "discount_pct": 5.0,
                        "incremental_units": 316.0,
                        "discounted_bundle_price": 4.83,
                        "gross_incremental_revenue": 1526.50,
                        "cannibalized_discount_cost": 62.93,
                        "net_revenue_lift": 1463.57
                    },
                    "10pct": {
                        "discount_pct": 10.0,
                        "incremental_units": 316.0,
                        "discounted_bundle_price": 4.58,
                        "gross_incremental_revenue": 1446.15,
                        "cannibalized_discount_cost": 125.85,
                        "net_revenue_lift": 1320.30
                    },
                    "15pct": {
                        "discount_pct": 15.0,
                        "incremental_units": 316.0,
                        "discounted_bundle_price": 4.32,
                        "gross_incremental_revenue": 1365.81,
                        "cannibalized_discount_cost": 188.78,
                        "net_revenue_lift": 1177.03
                    }
                }
            },
            {
                "bundle_id": "BDL-03",
                "bundle_name": "Vintage Bakelike Clock Companion",
                "family": "Bakelike Vintage Clocks",
                "anchor_sku": "22726",
                "anchor_desc": "ALARM CLOCK BAKELIKE GREEN",
                "attachment_sku": "22727",
                "attachment_desc": "ALARM CLOCK BAKELIKE RED",
                "support_pct": 3.24,
                "confidence_pct": 65.31,
                "lift": 12.29,
                "price_a": 4.54,
                "price_b": 4.40,
                "combined_price": 8.94,
                "return_rate_a_pct": 0.58,
                "return_rate_b_pct": 0.90,
                "max_return_rate_pct": 0.90,
                "passes_guardrail_1": True,
                "anchor_orders": 980,
                "pair_orders": 640,
                "solo_anchor_orders": 340,
                "tier_simulations": {
                    "5pct": {
                        "discount_pct": 5.0,
                        "incremental_units": 85.0,
                        "discounted_bundle_price": 8.49,
                        "gross_incremental_revenue": 721.82,
                        "cannibalized_discount_cost": 85.81,
                        "net_revenue_lift": 636.00
                    },
                    "10pct": {
                        "discount_pct": 10.0,
                        "incremental_units": 85.0,
                        "discounted_bundle_price": 8.05,
                        "gross_incremental_revenue": 683.83,
                        "cannibalized_discount_cost": 171.63,
                        "net_revenue_lift": 512.20
                    },
                    "15pct": {
                        "discount_pct": 15.0,
                        "incremental_units": 85.0,
                        "discounted_bundle_price": 7.60,
                        "gross_incremental_revenue": 645.83,
                        "cannibalized_discount_cost": 257.44,
                        "net_revenue_lift": 388.39
                    }
                }
            },
            {
                "bundle_id": "BDL-04",
                "bundle_name": "Everyday Lunch Bag Twin Pack",
                "family": "Lunch Bag Collection",
                "anchor_sku": "20725",
                "anchor_desc": "LUNCH BAG RED RETROSPOT",
                "attachment_sku": "22383",
                "attachment_desc": "LUNCH BAG SUKI DESIGN",
                "support_pct": 3.31,
                "confidence_pct": 41.85,
                "lift": 6.45,
                "price_a": 2.13,
                "price_b": 2.17,
                "combined_price": 4.30,
                "return_rate_a_pct": 2.33,
                "return_rate_b_pct": 0.99,
                "max_return_rate_pct": 2.33,
                "passes_guardrail_1": True,
                "anchor_orders": 1565,
                "pair_orders": 655,
                "solo_anchor_orders": 910,
                "tier_simulations": {
                    "5pct": {
                        "discount_pct": 5.0,
                        "incremental_units": 227.5,
                        "discounted_bundle_price": 4.08,
                        "gross_incremental_revenue": 929.26,
                        "cannibalized_discount_cost": 42.24,
                        "net_revenue_lift": 887.01
                    },
                    "10pct": {
                        "discount_pct": 10.0,
                        "incremental_units": 227.5,
                        "discounted_bundle_price": 3.87,
                        "gross_incremental_revenue": 880.35,
                        "cannibalized_discount_cost": 84.49,
                        "net_revenue_lift": 795.86
                    },
                    "15pct": {
                        "discount_pct": 15.0,
                        "incremental_units": 227.5,
                        "discounted_bundle_price": 3.65,
                        "gross_incremental_revenue": 831.44,
                        "cannibalized_discount_cost": 126.73,
                        "net_revenue_lift": 704.71
                    }
                }
            },
            {
                "bundle_id": "BDL-05",
                "bundle_name": "Poppy's Playhouse Miniature Nursery",
                "family": "Children's Playsets & Toys",
                "anchor_sku": "22745",
                "anchor_desc": "POPPY'S PLAYHOUSE BEDROOM",
                "attachment_sku": "22748",
                "attachment_desc": "POPPY'S PLAYHOUSE KITCHEN",
                "support_pct": 1.58,
                "confidence_pct": 74.00,
                "lift": 33.56,
                "price_a": 2.55,
                "price_b": 2.48,
                "combined_price": 5.03,
                "return_rate_a_pct": 0.58,
                "return_rate_b_pct": 0.73,
                "max_return_rate_pct": 0.73,
                "passes_guardrail_1": True,
                "anchor_orders": 423,
                "pair_orders": 313,
                "solo_anchor_orders": 110,
                "tier_simulations": {
                    "5pct": {
                        "discount_pct": 5.0,
                        "incremental_units": 27.5,
                        "discounted_bundle_price": 4.78,
                        "gross_incremental_revenue": 131.36,
                        "cannibalized_discount_cost": 23.61,
                        "net_revenue_lift": 107.75
                    },
                    "10pct": {
                        "discount_pct": 10.0,
                        "incremental_units": 27.5,
                        "discounted_bundle_price": 4.53,
                        "gross_incremental_revenue": 124.44,
                        "cannibalized_discount_cost": 47.21,
                        "net_revenue_lift": 77.23
                    },
                    "15pct": {
                        "discount_pct": 15.0,
                        "incremental_units": 27.5,
                        "discounted_bundle_price": 4.27,
                        "gross_incremental_revenue": 117.53,
                        "cannibalized_discount_cost": 70.82,
                        "net_revenue_lift": 46.71
                    }
                }
            },
            {
                "bundle_id": "FLAG-01",
                "bundle_name": "Regency Tea Plate Roses + Green",
                "family": "Regency Teaware (Flagged)",
                "anchor_sku": "23170",
                "anchor_desc": "REGENCY TEA PLATE ROSES",
                "attachment_sku": "23171",
                "attachment_desc": "REGENCY TEA PLATE GREEN",
                "support_pct": 1.61,
                "confidence_pct": 71.69,
                "lift": 37.20,
                "price_a": 2.08,
                "price_b": 2.13,
                "combined_price": 4.20,
                "return_rate_a_pct": 8.62,
                "return_rate_b_pct": 1.43,
                "max_return_rate_pct": 8.62,
                "passes_guardrail_1": False,
                "flagged_reason": "Return rate of 8.62% on anchor SKU 23170 exceeds the 5.0% Guardrail 1 ceiling. High reverse logistics cost would wipe out promotional margin.",
                "anchor_orders": 445,
                "pair_orders": 319,
                "solo_anchor_orders": 126,
                "tier_simulations": {
                    "5pct": {
                        "discount_pct": 5.0,
                        "incremental_units": 31.5,
                        "discounted_bundle_price": 3.99,
                        "gross_incremental_revenue": 125.80,
                        "cannibalized_discount_cost": 20.12,
                        "net_revenue_lift": 105.68
                    },
                    "10pct": {
                        "discount_pct": 10.0,
                        "incremental_units": 31.5,
                        "discounted_bundle_price": 3.78,
                        "gross_incremental_revenue": 119.18,
                        "cannibalized_discount_cost": 40.24,
                        "net_revenue_lift": 78.94
                    },
                    "15pct": {
                        "discount_pct": 15.0,
                        "incremental_units": 31.5,
                        "discounted_bundle_price": 3.57,
                        "gross_incremental_revenue": 112.56,
                        "cannibalized_discount_cost": 60.35,
                        "net_revenue_lift": 52.21
                    }
                }
            }
        ],
        "portfolio_bundle_simulation_totals": {
            "tier_5pct": {
                "gross_incremental": 3746.93,
                "cannibalization": 300.84,
                "net_lift": 3446.08
            },
            "tier_10pct": {
                "gross_incremental": 3549.72,
                "cannibalization": 601.68,
                "net_lift": 2948.04
            },
            "tier_15pct": {
                "gross_incremental": 3352.51,
                "cannibalization": 902.52,
                "net_lift": 2449.99
            }
        },
        "econometric_benchmarks": {
            "H1_kruskal_wallis_h": 3413.70,
            "H1_p_value": "< 0.0001",
            "H1_welch_t_stat": -3.26,
            "H1_welch_p_val": 0.0011,
            "H2_chi2_p_val": "< 0.0001",
            "H3_eu_vs_uk_mann_whitney_u": 20455334.5,
            "H3_eu_vs_uk_p_val": "3.69e-56",
            "H3_q4_surge_pct": 81.22,
            "H3_q4_mann_whitney_p_val": "2.02e-07"
        },
        "geographic_aov_benchmarks": [
            {"country": "United Kingdom", "median_aov": 299.67, "mean_aov": 488.50},
            {"country": "Netherlands", "median_aov": 814.90, "mean_aov": 1054.20},
            {"country": "EIRE", "median_aov": 625.30, "mean_aov": 960.40},
            {"country": "Germany", "median_aov": 319.45, "mean_aov": 462.80},
            {"country": "France", "median_aov": 345.10, "mean_aov": 485.60},
            {"country": "Australia", "median_aov": 430.20, "mean_aov": 1074.80}
        ]
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cube, f, indent=2)

    print(f"Interactive bundle cube successfully exported to {OUTPUT_PATH}")


if __name__ == "__main__":
    export_cockpit_cube()
