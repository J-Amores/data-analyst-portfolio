"""
src/presentation/export_figures.py
Calibrated Archival-Paper Chart Export Pipeline (Warm Archival Paper Identity).
Generates 4 300-DPI publication figures matching the portfolio brand:
- Canvas background: #FAF8F2
- Grid and borders: Crisp structural lines with zero em/en dashes
- High-contrast ink palette: #111111, #27272A, #16A34A, #E11D48, #D97706
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Ensure assets directory exists
Path("assets").mkdir(parents=True, exist_ok=True)

# Global Typography and Styling
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Plus Jakarta Sans", "Helvetica Neue", "Arial", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = "#111111"
plt.rcParams["axes.linewidth"] = 0.9

# Color Constants matching Medicaid & Credit Risk Design System and Editorial Tables
BG_CANVAS = "#FAF8F2"
BG_CARD = "#FFFFFF"
BG_PAPER_ALT = "#F3EFE6"
COLOR_INK = "#111111"
COLOR_CHARCOAL = "#27272A"
COLOR_MUTED = "#4A4843"
COLOR_SUBTLE = "#76746E"
COLOR_LIGHT_DIVIDER = "#D6D3CD"
COLOR_EMERALD = "#166534"
COLOR_LIGHT_GREEN = "#BBF7D0"
COLOR_CRIMSON = "#BE123C"
COLOR_LIGHT_CRIMSON = "#FFF1F2"
COLOR_SLATE = "#64748B"
COLOR_AMBER = "#B45309"


# ==============================================================================
# FIGURE 1: BASKET TIER SEGMENTATION & AOV SKEW
# ==============================================================================
def export_fig1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.8), dpi=300)
    fig.patch.set_facecolor(BG_CANVAS)
    ax1.set_facecolor(BG_CANVAS)
    ax2.set_facecolor(BG_CANVAS)

    # Titles with generous vertical headroom
    fig.text(0.04, 0.942, "Orders with 6+ items bring in 87% of revenue and have a 6x higher median order value than 1-2 item carts",
             fontsize=13.5, weight="bold", color=COLOR_INK)
    fig.text(0.04, 0.902, "Share of orders vs. share of revenue and median order value (£) by basket size across 19,773 clean orders",
             fontsize=10.5, color=COLOR_MUTED)

    tiers = [
        "1-2 items (Small)",
        "3-5 items (Medium)",
        "6+ items (Large)",
    ]
    y_pos = np.arange(len(tiers))
    bar_height = 0.32

    # Panel A: Share of Orders vs. Share of Revenue (rounded whole numbers: 12% vs 7%, 10% vs 6%, 78% vs 87%)
    order_shares = [12, 10, 78]
    rev_shares = [7, 6, 87]

    rects1 = ax1.barh(y_pos - bar_height / 2, rev_shares, height=bar_height, color=COLOR_EMERALD, edgecolor=COLOR_INK, linewidth=1.0, label="Share of revenue (%)")
    rects2 = ax1.barh(y_pos + bar_height / 2, order_shares, height=bar_height, color=COLOR_LIGHT_GREEN, edgecolor=COLOR_EMERALD, linewidth=1.0, label="Share of orders (%)")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(tiers, fontsize=10.5, weight="bold", color=COLOR_INK)
    ax1.set_xlabel("Share of store total (%)", fontsize=10, weight="bold", color=COLOR_INK, labelpad=8)
    ax1.set_xlim(0, 98)
    ax1.set_title("Panel A: Volume vs. revenue share across basket tiers", fontsize=11.5, weight="bold", color=COLOR_INK, loc="left", pad=14)
    ax1.legend(loc="lower right", frameon=False, fontsize=9.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.xaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_LIGHT_DIVIDER)
    ax1.set_axisbelow(True)

    # Value Labels Panel A
    for rect in rects1:
        w = rect.get_width()
        ax1.text(w + 1.2, rect.get_y() + rect.get_height() / 2, f"{w:.0f}%", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_EMERALD)
    for rect in rects2:
        w = rect.get_width()
        ax1.text(w + 1.2, rect.get_y() + rect.get_height() / 2, f"{w:.0f}%", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_INK)

    # Panel B: Median vs. Mean Order Value (rounded to whole numbers: £58 vs £307, £141 vs £316, £322 vs £582)
    mean_aov = [307, 316, 582]
    median_aov = [58, 141, 322]

    rects3 = ax2.barh(y_pos - bar_height / 2, mean_aov, height=bar_height, color=COLOR_LIGHT_GREEN, edgecolor=COLOR_EMERALD, linewidth=1.0, label="Average order value (£)")
    rects4 = ax2.barh(y_pos + bar_height / 2, median_aov, height=bar_height, color=COLOR_EMERALD, edgecolor=COLOR_INK, linewidth=1.0, label="Median order value (£)")

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.set_xlabel("Order value in £", fontsize=10, weight="bold", color=COLOR_INK, labelpad=8)
    ax2.set_xlim(0, 720)
    ax2.set_title("Panel B: Median vs. average order value", fontsize=11.5, weight="bold", color=COLOR_INK, loc="left", pad=14)
    ax2.legend(loc="lower right", frameon=False, fontsize=9.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.xaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_LIGHT_DIVIDER)
    ax2.set_axisbelow(True)

    # Value Labels Panel B
    for rect in rects3:
        w = rect.get_width()
        ax2.text(w + 10, rect.get_y() + rect.get_height() / 2, f"£{w:.0f}", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_INK)
    for rect in rects4:
        w = rect.get_width()
        ax2.text(w + 10, rect.get_y() + rect.get_height() / 2, f"£{w:.0f}", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_EMERALD)

    # Strategic Multiplier Callout Box
    ax2.annotate(
        "Why median spend is more reliable:\n"
        "Median order value jumps 6x (£58 to £322).\n"
        "Average on 1-2 items (£307) is skewed\n"
        "by single-item wholesale checkouts.",
        xy=(40, 0.32), xytext=(380, 0.52),
        bbox=dict(boxstyle="round,pad=0.5", facecolor=BG_CARD, edgecolor=COLOR_INK, linewidth=1.1),
        fontsize=9, weight="medium", color=COLOR_INK,
        arrowprops=dict(arrowstyle="->", color=COLOR_INK, lw=1.1)
    )

    # Bottom caption
    fig.text(0.04, 0.025, "22% of customers check out with just 1 to 5 items (£58 to £141 median order value), representing our biggest cross-sell opportunity.",
             fontsize=9.5, color=COLOR_MUTED, style="italic")

    plt.tight_layout(rect=[0.04, 0.055, 0.96, 0.86])
    plt.savefig("assets/fig1_basket_tier_aov.png", dpi=300)
    plt.close()


# ==============================================================================
# FIGURE 2: PRODUCT PAIR MATRIX & SAFETY GUARDRAIL
# ==============================================================================
def export_fig2():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor(BG_CANVAS)
    ax.set_facecolor(BG_CANVAS)

    # Titles with generous vertical headroom
    fig.text(0.04, 0.942, "Regency teaware and jumbo bag sets convert 65% to 84% of buyers at 6x to 37x normal pairing rates",
             fontsize=13.5, weight="bold", color=COLOR_INK)
    fig.text(0.04, 0.902, "Order share (% of all orders) vs. attach rate (% adding second item), sized by pairing multiplier",
             fontsize=10.5, color=COLOR_MUTED)

    # Points configuration with whole numbers
    pairs = [
        {
            "id": "BDL-01",
            "name": "Green + Roses Regency Teacups",
            "x": 4.0, "y": 76.0, "lift": 14, "color": COLOR_EMERALD,
            "ox": 18, "oy": 14, "is_flagged": False,
            "pairing_text": "14x", "attach_text": "76%"
        },
        {
            "id": "BDL-02",
            "name": "Pink + Green Regency Teacups",
            "x": 3.2, "y": 83.0, "lift": 16, "color": COLOR_EMERALD,
            "ox": 18, "oy": 16, "is_flagged": False,
            "pairing_text": "16x", "attach_text": "83%"
        },
        {
            "id": "BDL-03",
            "name": "Pink Polkadot + Red Retrospot Jumbo Bags",
            "x": 4.2, "y": 68.0, "lift": 6, "color": COLOR_EMERALD,
            "ox": 18, "oy": -20, "is_flagged": False,
            "pairing_text": "6x", "attach_text": "68%"
        },
        {
            "id": "BDL-04",
            "name": "Green + Red Bakelike Alarm Clocks",
            "x": 3.2, "y": 65.0, "lift": 12, "color": COLOR_EMERALD,
            "ox": 18, "oy": -22, "is_flagged": False,
            "pairing_text": "12x", "attach_text": "65%"
        },
        {
            "id": "BDL-05",
            "name": "Suki + Red Retrospot Lunch Bags",
            "x": 3.3, "y": 51.0, "lift": 6, "color": COLOR_EMERALD,
            "ox": 18, "oy": -16, "is_flagged": False,
            "pairing_text": "6x", "attach_text": "51%"
        },
        {
            "id": "FLAG-01",
            "name": "Roses + Green Regency Tea Plates",
            "x": 1.6, "y": 84.0, "lift": 37, "color": COLOR_CRIMSON,
            "ox": 22, "oy": 22, "is_flagged": True,
            "pairing_text": "37x", "attach_text": "84%"
        },
    ]

    for p in pairs:
        ax.scatter(p["x"], p["y"], s=p["lift"] * 48, color=p["color"], alpha=0.88,
                   edgecolors=COLOR_INK, linewidth=1.2, zorder=3)
        if p["is_flagged"]:
            callout_text = f"{p['name']} ({p['attach_text']} attach, {p['pairing_text']} pairing)\nBLOCKED: 9% return rate (exceeds 5% limit)"
            ax.annotate(callout_text,
                        xy=(p["x"], p["y"]), xytext=(p["ox"], p["oy"]), textcoords="offset points",
                        fontsize=8.5, weight="bold", color=COLOR_CRIMSON,
                        bbox=dict(boxstyle="round,pad=0.35", facecolor=COLOR_LIGHT_CRIMSON, edgecolor=COLOR_CRIMSON, linewidth=1.2),
                        arrowprops=dict(arrowstyle="->", color=COLOR_CRIMSON, lw=1.1),
                        zorder=4)
        else:
            ax.annotate(f"{p['name']}\nPairing: {p['pairing_text']} | Attach Rate: {p['attach_text']}",
                        xy=(p["x"], p["y"]), xytext=(p["ox"], p["oy"]), textcoords="offset points",
                        fontsize=8.5, weight="medium", color=COLOR_INK,
                        bbox=dict(boxstyle="round,pad=0.25", facecolor=BG_CARD, edgecolor=COLOR_LIGHT_DIVIDER, alpha=0.95),
                        arrowprops=dict(arrowstyle="->", color=COLOR_MUTED, lw=0.8),
                        zorder=4)

    # Reference lines
    ax.axhline(60, linestyle="--", color=COLOR_MUTED, linewidth=1.0, alpha=0.6)
    ax.text(1.15, 60.8, "High attach rate threshold (60%)", fontsize=8.5, style="italic", color=COLOR_MUTED)

    ax.axvline(2.5, linestyle="--", color=COLOR_MUTED, linewidth=1.0, alpha=0.6)
    ax.text(2.54, 44, "High order volume line (2.5% of store carts)", fontsize=8.5, style="italic", color=COLOR_MUTED)

    ax.set_xlim(1.0, 5.0)
    ax.set_ylim(40, 96)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["1%", "2%", "3%", "4%", "5%"], fontsize=9.5, weight="bold", color=COLOR_INK)
    ax.set_yticks([40, 50, 60, 70, 80, 90])
    ax.set_yticklabels(["40%", "50%", "60%", "70%", "80%", "90%"], fontsize=9.5, weight="bold", color=COLOR_INK)
    ax.set_xlabel("Order share (% of all orders)", fontsize=10, weight="bold", color=COLOR_INK, labelpad=8)
    ax.set_ylabel("Attach rate (% adding second item)", fontsize=10, weight="bold", color=COLOR_INK, labelpad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle="--", alpha=0.4, color=COLOR_LIGHT_DIVIDER)

    # Legend in lower right clear of all bubbles
    cats = [
        ("Approved 1-unit bundles (Phase 1)", COLOR_EMERALD),
        ("Blocked high-return pair (5% limit)", COLOR_CRIMSON),
    ]
    for cat_label, cat_col in cats:
        ax.scatter([], [], s=120, color=cat_col, alpha=0.88, edgecolors=COLOR_INK, label=cat_label)
    ax.legend(loc="lower right", frameon=True, facecolor=BG_CARD, edgecolor=COLOR_INK,
              title="Bundle classification", title_fontsize=9.5, fontsize=8.5)

    # Bottom caption
    fig.text(0.04, 0.025, "When a customer puts a Pink Regency Teacup in their cart, 83% also buy the matching Green Regency Teacup (16x pairing multiplier).",
             fontsize=9.5, color=COLOR_MUTED, style="italic")

    plt.tight_layout(rect=[0.04, 0.055, 0.96, 0.86])
    plt.savefig("assets/fig2_product_pair_matrix.png", dpi=300)
    plt.close()


# ==============================================================================
# FIGURE 3: COUNTRY SEASONALITY & REGIONAL ORDER VALUES
# ==============================================================================
def export_fig3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.8), dpi=300)
    fig.patch.set_facecolor(BG_CANVAS)
    ax1.set_facecolor(BG_CANVAS)
    ax2.set_facecolor(BG_CANVAS)

    # Titles with generous vertical headroom
    fig.text(0.04, 0.942, "Fall holiday shopping nearly doubles monthly sales while European wholesale buyers spend 3x to 5x more per order",
             fontsize=13.5, weight="bold", color=COLOR_INK)
    fig.text(0.04, 0.902, "Monthly store revenue (Dec 2010 to Nov 2011) and median order value (£) across top countries",
             fontsize=10.5, color=COLOR_MUTED)

    # Panel A: Monthly Revenue Bars
    months = ["Dec '10", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec*"]
    rev_k = [776, 673, 507, 691, 511, 742, 740, 690, 728, 1024, 1098, 1453, 615]
    bar_cols = [COLOR_LIGHT_GREEN] * 9 + [COLOR_EMERALD] * 3 + [COLOR_LIGHT_GREEN]
    bar_edges = [COLOR_EMERALD] * 9 + [COLOR_INK] * 3 + [COLOR_EMERALD]

    bars = ax1.bar(months, rev_k, color=bar_cols, width=0.62, edgecolor=bar_edges, linewidth=1.0)
    ax1.set_ylabel("Monthly store sales (£ in thousands)", fontsize=10, weight="bold", color=COLOR_INK)
    ax1.set_ylim(0, 1750)
    ax1.set_title("Panel A: Monthly store sales trend and Q4 surge", fontsize=11.5, weight="bold", color=COLOR_INK, loc="left", pad=14)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_LIGHT_DIVIDER)
    ax1.set_axisbelow(True)

    # Q4 Callout Box
    ax1.annotate(
        "Q4 holiday stocking: +81% over Q1-Q3\n"
        "Sep: £1,024K | Oct: £1,098K | Nov: £1,453K\n"
        "78% of orders arrive 10:00 to 15:00 weekdays",
        xy=(11, 1453), xytext=(4.2, 1520),
        bbox=dict(boxstyle="round,pad=0.45", facecolor=BG_CARD, edgecolor=COLOR_EMERALD, linewidth=1.1),
        fontsize=8.8, weight="medium", color=COLOR_INK,
        arrowprops=dict(arrowstyle="->", color=COLOR_EMERALD, lw=1.1)
    )

    # Panel B: Top 8 Markets Median Order Value
    countries = [
        "United Kingdom",
        "Germany",
        "France",
        "Spain",
        "Australia",
        "Switzerland",
        "EIRE (Ireland)",
        "Netherlands"
    ]
    median_aov = [300, 319, 345, 363, 430, 557, 625, 815]
    labels_by_country = [
        "United Kingdom £300 [9% returns]",
        "Germany £319 [3% returns]",
        "France £345 [6% returns]",
        "Spain £363 [11% returns: High Return Alert]",
        "Australia £430 [1% returns]",
        "Switzerland £557 [1% returns]",
        "EIRE £625 [7% returns]",
        "Netherlands £815 [<1% returns]"
    ]
    y_pos = np.arange(len(countries))
    h = 0.55

    bar_cols = [
        COLOR_LIGHT_GREEN,
        COLOR_LIGHT_GREEN,
        COLOR_LIGHT_GREEN,
        COLOR_CRIMSON,  # Spain flagged
        COLOR_LIGHT_GREEN,
        COLOR_LIGHT_GREEN,
        COLOR_LIGHT_GREEN,
        COLOR_EMERALD,  # Netherlands top wholesale
    ]
    bar_edges = [
        COLOR_EMERALD,
        COLOR_EMERALD,
        COLOR_EMERALD,
        COLOR_CRIMSON,
        COLOR_EMERALD,
        COLOR_EMERALD,
        COLOR_EMERALD,
        COLOR_INK,
    ]

    rects_med = ax2.barh(y_pos, median_aov, height=h, color=bar_cols, edgecolor=bar_edges, linewidth=1.0)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(countries, fontsize=10, weight="bold", color=COLOR_INK)
    ax2.set_xlabel("Median order value in £", fontsize=10, weight="bold", color=COLOR_INK, labelpad=8)
    ax2.set_xlim(0, 1080)
    ax2.set_title("Panel B: Median order value and return rates by market", fontsize=11.5, weight="bold", color=COLOR_INK, loc="left", pad=14)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.xaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_LIGHT_DIVIDER)
    ax2.set_axisbelow(True)

    for i, rect in enumerate(rects_med):
        w = rect.get_width()
        label_text = labels_by_country[i]
        if "Spain" in countries[i]:
            col = COLOR_CRIMSON
            weight = "bold"
        elif "Netherlands" in countries[i]:
            col = COLOR_EMERALD
            weight = "bold"
        else:
            col = COLOR_INK
            weight = "medium"
        ax2.text(w + 12, rect.get_y() + rect.get_height() / 2, label_text, va="center", ha="left", fontsize=9, weight=weight, color=col)

    # Bottom caption
    fig.text(0.04, 0.025, "September to November holiday stocking drives peak store volume, while wholesale accounts in the Netherlands, Ireland, Germany, and France place much larger bulk orders than UK retail shoppers.",
             fontsize=9.5, color=COLOR_MUTED, style="italic")

    plt.tight_layout(rect=[0.04, 0.055, 0.96, 0.86])
    plt.savefig("assets/fig3_country_seasonality_regime.png", dpi=300)
    plt.close()


# ==============================================================================
# FIGURE 4: BUNDLE REVENUE WATERFALL & SCENARIO POLICY COMPARISON
# ==============================================================================
def export_fig4():
    fig, ax = plt.subplots(figsize=(15, 8.2), dpi=300)
    fig.patch.set_facecolor(BG_CANVAS)
    ax.set_facecolor(BG_CANVAS)

    # Titles with generous vertical headroom
    fig.text(0.04, 0.942, "Adding 5 low-return product bundles with a 10% discount grows net store revenue while keeping returns under 2%",
             fontsize=13.5, weight="bold", color=COLOR_INK)
    fig.text(0.04, 0.902, "Projected annual revenue bridge from new cross-sell bundle sales minus the 10% promotional discount cost",
             fontsize=10.5, color=COLOR_MUTED)

    scenarios = [
        "Option 0\nCurrent Store",
        "Phase 1\n5 Retail Bundles",
        "What-If\nFragile Tea Plates",
        "Phase 2\nCart Drawer & Emails",
        "Phase 3A\n4x Multi-Packs",
        "Phase 3B\nWholesale Case-Packs (8x)",
    ]
    vals = [0, 2948, 3027, 4368, 11792, 24528]
    bar_cols = [
        COLOR_INK,
        COLOR_EMERALD,
        COLOR_CRIMSON,  # What-If blocked
        COLOR_EMERALD,
        COLOR_EMERALD,  # Phase 3A is Green, matching Phase 1, 2, and 3B
        COLOR_EMERALD,
    ]

    x_pos = np.arange(len(scenarios))
    bars = ax.bar(x_pos, vals, width=0.55, color=bar_cols, edgecolor=COLOR_INK, linewidth=1.1)

    # Value Labels above bars (clean whole numbers)
    labels = [
        "£0",
        "+£2,948",
        "+£3,027 [BLOCKED: 9% returns]",
        "+£4,368",
        "+£11,792",
        "+£24,528",
    ]

    for i, bar in enumerate(bars):
        h = bar.get_height()
        col = bar_cols[i]
        if i == 0:
            ax.text(bar.get_x() + bar.get_width() / 2, 900, labels[i], ha="center", va="bottom", fontsize=8.8, weight="bold", color=COLOR_INK)
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 700, labels[i], ha="center", va="bottom", fontsize=8.8, weight="bold", color=col)

    # Scenario details annotation card
    card_text = (
        "Bundle rollout rules:\n"
        "* 5% return limit: Maximum 5% return rate per item (passed by BDL-01 to BDL-05; averaging under 2% returns)\n"
        "* Profitable after discounts: Added sales exceed 10% discount given to existing buyers\n"
        "* What-If option is blocked: 9% return rate on rose tea plates causes shipping losses"
    )
    ax.text(0.04, 0.94, card_text, transform=ax.transAxes, fontsize=9.2, verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.55", facecolor=BG_CARD, edgecolor=COLOR_INK, lw=1.1),
            color=COLOR_INK, linespacing=1.35)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(scenarios, fontsize=9.8, weight="bold", color=COLOR_INK)
    ax.set_ylabel("Net revenue gain (£)", fontsize=10, weight="bold", color=COLOR_INK, labelpad=8)
    ax.set_ylim(0, 36000)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_LIGHT_DIVIDER)
    ax.set_axisbelow(True)

    # Bottom caption
    fig.text(0.04, 0.025, "Every recommended bundle stays well below our 5% maximum return rate goal (averaging under 2% returns).",
             fontsize=9.5, color=COLOR_MUTED, style="italic")

    plt.tight_layout(rect=[0.04, 0.055, 0.96, 0.86])
    plt.savefig("assets/fig4_bundle_revenue_waterfall.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    print("Re-rendering calibrated presentation figures (warm archival paper identity)...")
    export_fig1()
    export_fig2()
    export_fig3()
    export_fig4()
    print("All 4 figures successfully exported to assets/ at 300 DPI.")
