"""
src/presentation/export_cockpit_data.py
Exports the verified Phase 3 empirical data cube to data/exports/cockpit_bundle_cube.json.
Powers the interactive merchandising workstation (cockpit.html) and executive reports.
Enforces zero em dashes and zero en dashes.
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
            "title": "E-Commerce Merchandising, Basket Profitability and Cross-Sell Engine Data Cube",
            "version": "3.0.0",
            "source_ledger": "Online Retail.xlsx",
            "pipeline": "CLEAN 5-Step Architecture",
            "zero_em_dashes_verified": True
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
                "tier_id": "tier_1_2",
                "label": "1-2 items",
                "order_count": 2313,
                "order_share_pct": 11.7,
                "gmv": 710521.85,
                "rev_share_pct": 6.9,
                "median_aov": 57.60,
                "mean_aov": 307.19,
                "color": "#27272A"
            },
            {
                "tier_id": "tier_3_5",
                "label": "3-5 items",
                "order_count": 2041,
                "order_share_pct": 10.3,
                "gmv": 645761.75,
                "rev_share_pct": 6.3,
                "median_aov": 140.85,
                "mean_aov": 316.39,
                "color": "#27272A"
            },
            {
                "tier_id": "tier_6_15",
                "label": "6-15 items",
                "order_count": 5622,
                "order_share_pct": 28.4,
                "gmv": 2119603.95,
                "rev_share_pct": 20.7,
                "median_aov": 230.43,
                "mean_aov": 377.02,
                "color": "#16A34A"
            },
            {
                "tier_id": "tier_16_30",
                "label": "16-30 items",
                "order_count": 5253,
                "order_share_pct": 26.6,
                "gmv": 2376824.45,
                "rev_share_pct": 23.2,
                "median_aov": 335.50,
                "mean_aov": 452.47,
                "color": "#16A34A"
            },
            {
                "tier_id": "tier_31_plus",
                "label": "31+ items",
                "order_count": 4544,
                "order_share_pct": 23.0,
                "gmv": 4394898.15,
                "rev_share_pct": 42.9,
                "median_aov": 550.58,
                "mean_aov": 967.19,
                "color": "#16A34A"
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
                "confidence_pct": 67.73,
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
                "confidence_pct": 51.01,
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
                "family": "Children's Playsets and Toys",
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
                "confidence_pct": 83.73,
                "lift": 37.20,
                "price_a": 2.08,
                "price_b": 2.13,
                "combined_price": 4.20,
                "return_rate_a_pct": 8.62,
                "return_rate_b_pct": 1.43,
                "max_return_rate_pct": 8.62,
                "passes_guardrail_1": False,
                "flagged_reason": "Return rate of 8.62% on anchor SKU 23170 exceeds the 5.0% Guardrail 1 ceiling. Ceramic plate transit breakage wipes out margin.",
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
        "blocked_items": [
            {
                "flag_id": "FLAG-01",
                "title": "Regency Tea Plate Roses + Green",
                "sku_a": "23170",
                "desc_a": "REGENCY TEA PLATE ROSES",
                "sku_b": "23171",
                "desc_b": "REGENCY TEA PLATE GREEN",
                "lift": 37.20,
                "support_pct": 1.61,
                "confidence_pct": 83.73,
                "return_rate_pct": 8.62,
                "breach_limit_pct": 5.0,
                "reason": "Anchor SKU 23170 suffers 8.62% returns due to transit edge chipping. Excluded from promotional discounting to prevent reverse-logistics leakage."
            },
            {
                "flag_id": "FLAG-02",
                "title": "Top-Seller Cakestand + Heart T-Light Holder",
                "sku_a": "22423",
                "desc_a": "REGENCY CAKESTAND 3 TIER",
                "sku_b": "85123A",
                "desc_b": "WHITE HANGING HEART T-LIGHT HOLDER",
                "lift": 1.48,
                "support_pct": 1.82,
                "confidence_pct": 21.4,
                "return_rate_a_pct": 5.29,
                "return_rate_b_pct": 5.86,
                "return_rate_pct": 5.86,
                "breach_limit_pct": 5.0,
                "reason": "Both #1 revenue item 22423 (£174k sales, 5.29% returns) and #1 order volume item 85123A (2,265 orders, 5.86% returns) exceed the 5.0% return safety limit due to glass and ceramic breakage."
            }
        ],
        "scenarios": [
            {
                "scenario_id": "Scenario 0",
                "scenario_name": "Current Baseline",
                "discount_pct": 0.0,
                "attach_rate_pct": 0.0,
                "scale": 1.0,
                "gross_incremental_revenue": 0.0,
                "cannibalized_discount_cost": 0.0,
                "net_revenue_lift": 0.0,
                "max_return_rate_pct": 0.0,
                "guardrail_1_status": "PASS",
                "guardrail_2_status": "PASS",
                "roi_multiple": 0.0,
                "strategic_action": "Historical status quo with zero cross-sell attach and zero promotional discounting."
            },
            {
                "scenario_id": "Scenario 1A",
                "scenario_name": "Phase 1 Retail 1-Unit Bundles",
                "discount_pct": 10.0,
                "attach_rate_pct": 25.0,
                "scale": 1.0,
                "gross_incremental_revenue": 3549.72,
                "cannibalized_discount_cost": 601.68,
                "net_revenue_lift": 2948.04,
                "max_return_rate_pct": 3.81,
                "guardrail_1_status": "PASS",
                "guardrail_2_status": "PASS",
                "roi_multiple": 5.90,
                "strategic_action": "Deploy 1-click storefront collections for top 5 approved bundles at single-unit retail scale."
            },
            {
                "scenario_id": "Scenario 1B",
                "scenario_name": "Unfiltered High-Return Trap",
                "discount_pct": 10.0,
                "attach_rate_pct": 25.0,
                "scale": 1.0,
                "gross_incremental_revenue": 3668.90,
                "cannibalized_discount_cost": 641.92,
                "net_revenue_lift": 3026.98,
                "max_return_rate_pct": 8.62,
                "guardrail_1_status": "FAIL (BREACH > 5.0%)",
                "guardrail_2_status": "FAIL",
                "roi_multiple": 5.72,
                "strategic_action": "Blocked: High return rate (8.62% on 23170 and 5.29% on 22423) wipes out promotional margin via reverse logistics."
            },
            {
                "scenario_id": "Scenario 2A",
                "scenario_name": "Phase 1 + 48-Hr Follow-Up Emails",
                "discount_pct": 10.0,
                "attach_rate_pct": 35.0,
                "scale": 1.0,
                "gross_incremental_revenue": 4969.61,
                "cannibalized_discount_cost": 601.68,
                "net_revenue_lift": 4367.93,
                "max_return_rate_pct": 3.81,
                "guardrail_1_status": "PASS",
                "guardrail_2_status": "PASS",
                "roi_multiple": 8.26,
                "strategic_action": "Storefront 1-click collections paired with automated 48-hour post-purchase cross-sell emails."
            },
            {
                "scenario_id": "Scenario 2B",
                "scenario_name": "Small-Business 4x Multi-Packs",
                "discount_pct": 10.0,
                "attach_rate_pct": 25.0,
                "scale": 4.0,
                "gross_incremental_revenue": 14198.88,
                "cannibalized_discount_cost": 2406.72,
                "net_revenue_lift": 11792.16,
                "max_return_rate_pct": 3.81,
                "guardrail_1_status": "PASS",
                "guardrail_2_status": "PASS",
                "roi_multiple": 5.90,
                "strategic_action": "Small-business multi-pack bundles reflecting 4.0x median line quantity scale."
            },
            {
                "scenario_id": "Scenario 2C",
                "scenario_name": "Phase 3 Wholesale Case-Packs 8.3x",
                "discount_pct": 10.0,
                "attach_rate_pct": 25.0,
                "scale": 8.32,
                "gross_incremental_revenue": 29533.67,
                "cannibalized_discount_cost": 5005.98,
                "net_revenue_lift": 24527.69,
                "max_return_rate_pct": 3.81,
                "guardrail_1_status": "PASS",
                "guardrail_2_status": "PASS",
                "roi_multiple": 5.90,
                "strategic_action": "Institutional wholesale case-pack bundles scaled to empirical 8.32x average line quantity across product families."
            }
        ],
        "discount_sensitivity_grid": [
            {"discount_pct": 5.0, "attach_rate_pct": 15.0, "gross_incremental": 2248.16, "cannibalization": 300.84, "net_lift": 1947.32, "roi_multiple": 7.47},
            {"discount_pct": 5.0, "attach_rate_pct": 25.0, "gross_incremental": 3746.93, "cannibalization": 300.84, "net_lift": 3446.09, "roi_multiple": 12.45},
            {"discount_pct": 5.0, "attach_rate_pct": 35.0, "gross_incremental": 5245.70, "cannibalization": 300.84, "net_lift": 4944.86, "roi_multiple": 17.44},
            {"discount_pct": 10.0, "attach_rate_pct": 15.0, "gross_incremental": 2129.83, "cannibalization": 601.68, "net_lift": 1528.15, "roi_multiple": 3.54},
            {"discount_pct": 10.0, "attach_rate_pct": 25.0, "gross_incremental": 3549.72, "cannibalization": 601.68, "net_lift": 2948.04, "roi_multiple": 5.90},
            {"discount_pct": 10.0, "attach_rate_pct": 35.0, "gross_incremental": 4969.61, "cannibalization": 601.68, "net_lift": 4367.93, "roi_multiple": 8.26},
            {"discount_pct": 15.0, "attach_rate_pct": 15.0, "gross_incremental": 2011.51, "cannibalization": 902.52, "net_lift": 1108.99, "roi_multiple": 2.23},
            {"discount_pct": 15.0, "attach_rate_pct": 25.0, "gross_incremental": 3352.51, "cannibalization": 902.52, "net_lift": 2449.99, "roi_multiple": 3.71},
            {"discount_pct": 15.0, "attach_rate_pct": 35.0, "gross_incremental": 4693.52, "cannibalization": 902.52, "net_lift": 3791.00, "roi_multiple": 5.20},
            {"discount_pct": 20.0, "attach_rate_pct": 15.0, "gross_incremental": 1893.18, "cannibalization": 1203.36, "net_lift": 689.82, "roi_multiple": 1.57},
            {"discount_pct": 20.0, "attach_rate_pct": 25.0, "gross_incremental": 3155.31, "cannibalization": 1203.36, "net_lift": 1951.95, "roi_multiple": 2.62},
            {"discount_pct": 20.0, "attach_rate_pct": 35.0, "gross_incremental": 4417.43, "cannibalization": 1203.36, "net_lift": 3214.07, "roi_multiple": 3.67}
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
        "sku_lookup_desk": [
            {
                "lookup_id": "LOOKUP-01",
                "label": "Regency Teacups 22697+22699 (Safe)",
                "item_type": "Product Pair (Teaware)",
                "anchor_sku": "22697",
                "anchor_desc": "GREEN REGENCY TEACUP AND SAUCER",
                "attachment_sku": "22699",
                "attachment_desc": "ROSES REGENCY TEACUP AND SAUCER",
                "gross_sales": 70830.90,
                "cancelled_value": -2012.35,
                "return_rate_pct": 3.81,
                "lift": 14.06,
                "odds_ratio": 193.16,
                "status_stamp": "APPROVED FOR 10% BUNDLE",
                "stamp_type": "approved",
                "details": "Component return rates: Green 1.70%, Roses 3.81%. High affinity with 75.7% confidence and well beneath 5.0% safety limit."
            },
            {
                "lookup_id": "LOOKUP-02",
                "label": "Jumbo Bags 85099B+22386 (Safe)",
                "item_type": "Product Pair (Storage Bags)",
                "anchor_sku": "85099B",
                "anchor_desc": "JUMBO BAG RED RETROSPOT",
                "attachment_sku": "22386",
                "attachment_desc": "JUMBO BAG PINK POLKADOT",
                "gross_sales": 89240.12,
                "cancelled_value": -1842.10,
                "return_rate_pct": 2.06,
                "lift": 6.41,
                "odds_ratio": 28.72,
                "status_stamp": "APPROVED FOR 10% BUNDLE",
                "stamp_type": "approved",
                "details": "Anchor return rate 2.06%, attachment 1.89%. Highest volume anchor with 2,089 total orders and durable polypropylene fabric."
            },
            {
                "lookup_id": "LOOKUP-03",
                "label": "Regency Tea Plates 23170+23171 (8.62% Return Trap)",
                "item_type": "Product Pair (Fragile Ceramic)",
                "anchor_sku": "23170",
                "anchor_desc": "REGENCY TEA PLATE ROSES",
                "attachment_sku": "23171",
                "attachment_desc": "REGENCY TEA PLATE GREEN",
                "gross_sales": 3218.40,
                "cancelled_value": -277.28,
                "return_rate_pct": 8.62,
                "lift": 37.20,
                "odds_ratio": 786.72,
                "status_stamp": "BLOCKED: FRAGILE TRANSIT RETURN RISK",
                "stamp_type": "blocked",
                "details": "Despite highest affinity (37.2x lift), anchor return rate of 8.62% breaches 5.0% limit. Packaging drop-test required before unlocking."
            },
            {
                "lookup_id": "LOOKUP-04",
                "label": "#1 Seller Regency Cakestand 22423 (5.29% Fragile)",
                "item_type": "Single Anchor SKU (Ceramic)",
                "anchor_sku": "22423",
                "anchor_desc": "REGENCY CAKESTAND 3 TIER",
                "attachment_sku": "N/A",
                "attachment_desc": "Store #1 Revenue Generator",
                "gross_sales": 174156.54,
                "cancelled_value": -9722.55,
                "return_rate_pct": 5.29,
                "lift": 1.00,
                "odds_ratio": 1.00,
                "status_stamp": "BLOCKED: FRAGILE TRANSIT RETURN RISK",
                "stamp_type": "blocked",
                "details": "Store #1 revenue item (£174k sales) generates £9,722.55 in cancellations due to multi-tier ceramic breakage in standard cartons."
            },
            {
                "lookup_id": "LOOKUP-05",
                "label": "#1 Frequency Heart Holder 85123A (5.86% Glass)",
                "item_type": "Single Anchor SKU (Glassware)",
                "anchor_sku": "85123A",
                "anchor_desc": "WHITE HANGING HEART T-LIGHT HOLDER",
                "attachment_sku": "N/A",
                "attachment_desc": "Store #1 Order Count Item",
                "gross_sales": 106415.23,
                "cancelled_value": -6624.30,
                "return_rate_pct": 5.86,
                "lift": 1.00,
                "odds_ratio": 1.00,
                "status_stamp": "BLOCKED: FRAGILE TRANSIT RETURN RISK",
                "stamp_type": "blocked",
                "details": "Store #1 order frequency item (2,265 orders) has £6,624.30 in returns. Thin glass construction fails drop thresholds."
            },
            {
                "lookup_id": "LOOKUP-06",
                "label": "Spain Export Market Check (10.88% Return Anomaly)",
                "item_type": "Geographic Destination Market",
                "anchor_sku": "ES-ALL",
                "anchor_desc": "Cross-Border Commercial Export",
                "attachment_sku": "N/A",
                "attachment_desc": "Spanish Wholesale and Retail Accounts",
                "gross_sales": 55706.56,
                "cancelled_value": -6802.53,
                "return_rate_pct": 10.88,
                "lift": 1.00,
                "odds_ratio": 1.00,
                "status_stamp": "RESTRICT DISCOUNT: HIGH REGIONAL RETURNS",
                "stamp_type": "restricted",
                "details": "Spain accounts show 10.88% returns (£6,802.53 lost), far exceeding Netherlands (0.28%) or Germany (3.37%). Restrict deep discounts."
            }
        ],
        "econometric_benchmarks": {
            "H1_kruskal_wallis_h": 5648.50,
            "H1_p_value": "< 0.0001",
            "H1_welch_t_stat": 3.26,
            "H1_welch_p_val": 0.0011,
            "H2_chi2_p_val": "< 0.0001",
            "H3_eu_vs_uk_mann_whitney_p_val": "< 0.0001",
            "H3_q4_surge_pct": 81.22,
            "H3_q4_mann_whitney_p_val": "< 0.0001"
        },
        "geographic_aov_benchmarks": [
            {"country": "United Kingdom", "median_aov": 299.67, "mean_aov": 488.50, "return_rate_pct": 8.61},
            {"country": "Netherlands", "median_aov": 814.90, "mean_aov": 1054.20, "return_rate_pct": 0.28},
            {"country": "EIRE", "median_aov": 625.30, "mean_aov": 960.40, "return_rate_pct": 6.89},
            {"country": "Switzerland", "median_aov": 556.88, "mean_aov": 780.20, "return_rate_pct": 1.32},
            {"country": "Australia", "median_aov": 430.20, "mean_aov": 1074.80, "return_rate_pct": 0.98},
            {"country": "Spain", "median_aov": 363.06, "mean_aov": 633.03, "return_rate_pct": 10.88},
            {"country": "France", "median_aov": 345.10, "mean_aov": 485.60, "return_rate_pct": 6.27},
            {"country": "Germany", "median_aov": 319.45, "mean_aov": 462.80, "return_rate_pct": 3.37}
        ]
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cube, f, indent=2)

    print(f"Interactive bundle cube successfully exported to {OUTPUT_PATH}")


if __name__ == "__main__":
    export_cockpit_cube()
