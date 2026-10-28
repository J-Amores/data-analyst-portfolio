"""
src/presentation/export_figures.py
Publication-Grade Visual Assets Pipeline (Decision-Driven Design Standard)
Monochromatic slate foundation with emerald growth and crimson risk accents.
Calibrated layout eliminating all text collisions and label overlaps.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Ensure assets directory exists
Path("assets").mkdir(parents=True, exist_ok=True)

# Global Typography and Styling
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8

# Color Palette Constants
COLOR_NAVY = "#0F172A"       # Primary text and titles
COLOR_DARK_SLATE = "#1E293B" # Primary volume / median bars
COLOR_MUTED_SLATE = "#64748B"# Baseline secondary comparisons
COLOR_LIGHT_SLATE = "#94A3B8"# Reference lines and ticks
COLOR_EMERALD = "#059669"    # Net positive growth, revenue share, mean AOV
COLOR_CRIMSON = "#DC2626"    # Cancellation leakage, promotional discount cost, flagged items
COLOR_AMBER = "#D97706"      # Secondary product categories
COLOR_BLUE = "#0284C7"       # Storage bags / utility lines


# ==============================================================================
# FIGURE 1: BASKET TIER SEGMENTATION & AOV SKEW
# ==============================================================================
def export_fig1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax1.set_facecolor("#FFFFFF")
    ax2.set_facecolor("#FFFFFF")

    # Titles and Headers with calibrated vertical separation (Task 2.1.1)
    fig.text(0.04, 0.950, "Multi-SKU Baskets (6+ Items) Drive 86.8% of Revenue With a 5.6x Higher Median AOV Than Small Checkouts",
             fontsize=14, weight="bold", color=COLOR_NAVY)
    fig.text(0.04, 0.905, "Transaction portfolio segmentation reveals extreme monetization polarization between retail checkouts and multi-line wholesale orders",
             fontsize=11, color=COLOR_MUTED_SLATE)

    tiers = ["Small (1-2 SKUs)", "Medium (3-5 SKUs)", "Large (6-15 SKUs)", "Wholesale (16+ SKUs)"]
    y_pos = np.arange(len(tiers))
    bar_height = 0.35

    # Panel A: Volume vs. Revenue Skew
    order_shares = [11.7, 10.3, 28.4, 49.5]
    rev_shares = [6.9, 6.3, 20.7, 66.1]

    rects1 = ax1.barh(y_pos - bar_height / 2, rev_shares, height=bar_height, color=COLOR_EMERALD, label="Share of Revenue (%)")
    rects2 = ax1.barh(y_pos + bar_height / 2, order_shares, height=bar_height, color=COLOR_MUTED_SLATE, label="Share of Orders (%)")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(tiers, fontsize=10.5, weight="bold", color=COLOR_DARK_SLATE)
    ax1.set_xlabel("Percentage Share (%)", fontsize=10, weight="bold", color=COLOR_DARK_SLATE, labelpad=10)
    ax1.set_xlim(0, 80)
    ax1.set_title("Panel A: Volume vs. Revenue Skew", fontsize=12, weight="bold", color=COLOR_DARK_SLATE, loc="left", pad=15)
    ax1.legend(loc="upper right", frameon=False, fontsize=9.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.xaxis.grid(True, linestyle="--", alpha=0.3, color=COLOR_LIGHT_SLATE)
    ax1.set_axisbelow(True)

    # Value Labels Panel A
    for rect in rects1:
        w = rect.get_width()
        ax1.text(w + 1.2, rect.get_y() + rect.get_height() / 2, f"{w:.1f}%", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_EMERALD)
    for rect in rects2:
        w = rect.get_width()
        ax1.text(w + 1.2, rect.get_y() + rect.get_height() / 2, f"{w:.1f}%", va="center", ha="left", fontsize=9.5, color=COLOR_DARK_SLATE)

    # Panel B: Average Order Value Profile (Calibrated xlim=860 and lower right legend)
    mean_aov = [307.19, 316.39, 377.02, 691.20]
    median_aov = [57.60, 140.85, 230.43, 389.72]

    rects3 = ax2.barh(y_pos - bar_height / 2, mean_aov, height=bar_height, color=COLOR_EMERALD, label="Mean AOV (£)")
    rects4 = ax2.barh(y_pos + bar_height / 2, median_aov, height=bar_height, color=COLOR_DARK_SLATE, label="Median AOV (£)")

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.set_xlabel("Order Value in £", fontsize=10, weight="bold", color=COLOR_DARK_SLATE, labelpad=10)
    ax2.set_xlim(0, 860)
    ax2.set_title("Panel B: Average Order Value (AOV) Profile", fontsize=12, weight="bold", color=COLOR_DARK_SLATE, loc="left", pad=15)
    ax2.legend(loc="lower right", frameon=False, fontsize=9.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.xaxis.grid(True, linestyle="--", alpha=0.3, color=COLOR_LIGHT_SLATE)
    ax2.set_axisbelow(True)

    # Value Labels Panel B
    for rect in rects3:
        w = rect.get_width()
        ax2.text(w + 12, rect.get_y() + rect.get_height() / 2, f"£{w:.2f}", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_EMERALD)
    for rect in rects4:
        w = rect.get_width()
        ax2.text(w + 12, rect.get_y() + rect.get_height() / 2, f"£{w:.2f}", va="center", ha="left", fontsize=9.5, weight="bold", color=COLOR_DARK_SLATE)

    # Strategic Multiplier Callout Box (Positioned with generous breathing room)
    ax2.annotate("5.6x Median AOV Surge\nSmall (£57.60) vs. Multi-SKU (£322.30)",
                 xy=(322.30, 2.0), xytext=(450, 1.55),
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#ECFDF5", edgecolor=COLOR_EMERALD, linewidth=1.2),
                 fontsize=9.5, weight="bold", color=COLOR_EMERALD,
                 arrowprops=dict(arrowstyle="->", color=COLOR_EMERALD, lw=1.2))

    plt.tight_layout(rect=[0.04, 0.04, 0.96, 0.85])
    plt.savefig("assets/fig1_basket_tier_aov.png", dpi=300)
    plt.close()


# ==============================================================================
# FIGURE 2: CROSS-SELL AFFINITY & ASSOCIATION MATRIX
# ==============================================================================
def export_fig2():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Titles and Headers with calibrated vertical separation
    fig.text(0.04, 0.950, "Regency Teaware and Jumbo Bag Collections Deliver 60% to 84% Cross-Sell Confidence at 6x to 37x Lift",
             fontsize=14, weight="bold", color=COLOR_NAVY)
    fig.text(0.04, 0.905, "Bubble size reflects association Lift ratio relative to independent purchase probability; positioned by portfolio Support and conditional Confidence",
             fontsize=11, color=COLOR_MUTED_SLATE)

    # Curated Top Association Rules with zero-collision coordinates and offsets
    rules = [
        {
            "name": "Regency Teacup Duet (Green + Rose)",
            "x": 3.88, "y": 75.7, "lift": 14.06, "color": COLOR_EMERALD,
            "ox": 16, "oy": 8, "is_flagged": False
        },
        {
            "name": "Bakelike Alarm Clock Pair",
            "x": 3.24, "y": 65.3, "lift": 12.29, "color": COLOR_AMBER,
            "ox": 16, "oy": -14, "is_flagged": False
        },
        {
            "name": "Retrospot Jumbo Storage Bags",
            "x": 4.17, "y": 39.5, "lift": 6.41, "color": COLOR_BLUE,
            "ox": 16, "oy": 8, "is_flagged": False
        },
        {
            "name": "Red Retrospot Lunch Bag Pair",
            "x": 3.31, "y": 41.9, "lift": 6.45, "color": COLOR_AMBER,
            "ox": 16, "oy": -14, "is_flagged": False
        },
        {
            "name": "Poppy's Playhouse Nursery Set",
            "x": 1.58, "y": 74.0, "lift": 33.56, "color": COLOR_MUTED_SLATE,
            "ox": -145, "oy": 18, "is_flagged": False
        },
        {
            "name": "Red Spotty Cups & Paper Plates",
            "x": 1.77, "y": 81.8, "lift": 30.68, "color": COLOR_MUTED_SLATE,
            "ox": 18, "oy": 10, "is_flagged": False
        },
        {
            "name": "Scandinavian Heart & Star Duet",
            "x": 1.96, "y": 72.1, "lift": 27.85, "color": COLOR_MUTED_SLATE,
            "ox": 18, "oy": -18, "is_flagged": False
        },
        {
            "name": "Fairy Cake & Mini Loaf Cases",
            "x": 1.55, "y": 55.4, "lift": 24.69, "color": COLOR_MUTED_SLATE,
            "ox": 16, "oy": -12, "is_flagged": False
        },
        {
            "name": "Owl & Scotty Dog Hand Warmers",
            "x": 1.69, "y": 51.2, "lift": 18.48, "color": COLOR_MUTED_SLATE,
            "ox": 16, "oy": 8, "is_flagged": False
        },
        {
            "name": "Regency Tea Plate Roses + Green",
            "x": 1.61, "y": 71.7, "lift": 37.20, "color": COLOR_CRIMSON,
            "ox": 24, "oy": 28, "is_flagged": True
        },
    ]

    for r in rules:
        ax.scatter(r["x"], r["y"], s=r["lift"] * 42, color=r["color"], alpha=0.85,
                   edgecolors=COLOR_DARK_SLATE, linewidth=1.2, zorder=3)
        if r["is_flagged"]:
            # Distinct crimson-bordered callout annotation for Guardrail 1 flagged pair
            callout_text = (
                f"{r['name']} ({r['lift']:.1f}x Lift)\n"
                "FLAGGED by Guardrail 1 (8.62% Return Rate -> Excluded from Bundles)"
            )
            ax.annotate(callout_text,
                        xy=(r["x"], r["y"]), xytext=(r["ox"], r["oy"]), textcoords="offset points",
                        fontsize=8.5, weight="bold", color=COLOR_CRIMSON,
                        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEF2F2", edgecolor=COLOR_CRIMSON, linewidth=1.3),
                        arrowprops=dict(arrowstyle="->", color=COLOR_CRIMSON, lw=1.1),
                        zorder=4)
        else:
            ax.annotate(f"{r['name']}\nLift: {r['lift']:.1f}x | Conf: {r['y']:.1f}%",
                        xy=(r["x"], r["y"]), xytext=(r["ox"], r["oy"]), textcoords="offset points",
                        fontsize=8.5, weight="bold", color=COLOR_DARK_SLATE,
                        bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.92),
                        arrowprops=dict(arrowstyle="->", color=COLOR_MUTED_SLATE, lw=0.8),
                        zorder=4)

    # Reference Thresholds
    ax.axhline(60, linestyle="--", color=COLOR_LIGHT_SLATE, linewidth=1.1, alpha=0.7)
    ax.text(1.25, 60.8, "High Confidence Threshold (60%)", fontsize=9, style="italic", color=COLOR_MUTED_SLATE)

    ax.axvline(2.5, linestyle="--", color=COLOR_LIGHT_SLATE, linewidth=1.1, alpha=0.7)
    ax.text(2.54, 32, "High Volume Threshold (2.5% Storefront Orders)", fontsize=9, style="italic", color=COLOR_MUTED_SLATE)

    ax.set_xlim(1.2, 4.8)
    ax.set_ylim(28, 94)
    ax.set_xlabel("Support (% of Total Valid Commercial Orders)", fontsize=10.5, weight="bold", color=COLOR_DARK_SLATE, labelpad=10)
    ax.set_ylabel("Confidence (% Attachment Probability A -> B)", fontsize=10.5, weight="bold", color=COLOR_DARK_SLATE, labelpad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle="--", alpha=0.25, color=COLOR_LIGHT_SLATE)

    # Clean Legend moved to lower left outside the high-lift cluster (Task 2.1.3)
    categories = [
        ("Regency Teaware", COLOR_EMERALD),
        ("Jumbo Bags", COLOR_BLUE),
        ("Tableware / Clocks", COLOR_AMBER),
        ("Sets & Seasonal", COLOR_MUTED_SLATE),
        ("Flagged SKU (Guardrail 1)", COLOR_CRIMSON),
    ]
    for cat_label, cat_col in categories:
        ax.scatter([], [], s=120, color=cat_col, alpha=0.85, edgecolors=COLOR_DARK_SLATE, label=cat_label)
    ax.legend(loc="lower left", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1",
              title="Merchandise Category", title_fontsize=9.5, fontsize=8.5)

    plt.tight_layout(rect=[0.04, 0.04, 0.96, 0.85])
    plt.savefig("assets/fig2_product_pair_matrix.png", dpi=300)
    plt.close()


# ==============================================================================
# FIGURE 3: GEOGRAPHIC REGIMES & Q4 SEASONAL EXPANSION
# ==============================================================================
def export_fig3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax1.set_facecolor("#FFFFFF")
    ax2.set_facecolor("#FFFFFF")

    # Titles and Headers with calibrated vertical separation (Task 2.1.1)
    fig.text(0.04, 0.950, "Q4 Holiday Demand Nearly Doubles Monthly Revenue While EU Wholesale Baskets Outperform Domestic UK AOV",
             fontsize=14, weight="bold", color=COLOR_NAVY)
    fig.text(0.04, 0.905, "Temporal demand surges from September to November; Continental European markets present significantly higher wholesale scale than UK retail",
             fontsize=11, color=COLOR_MUTED_SLATE)

    # Panel A: Monthly Revenue Profile (Calibrated ylim=1680 for zero collision with title)
    months = ["Dec '10", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec*"]
    rev_k = [776.4, 672.8, 506.7, 691.3, 510.9, 741.9, 739.7, 689.8, 727.6, 1024.1, 1098.3, 1452.8, 614.9]
    colors = [COLOR_DARK_SLATE] * 9 + [COLOR_EMERALD] * 3 + [COLOR_DARK_SLATE]

    bars = ax1.bar(months, rev_k, color=colors, width=0.62)
    ax1.set_ylabel("Monthly Revenue (£ in Thousands)", fontsize=10, weight="bold", color=COLOR_DARK_SLATE)
    ax1.set_ylim(0, 1680)
    ax1.set_title("Panel A: Monthly Revenue & Holiday Demand Surge", fontsize=12, weight="bold", color=COLOR_DARK_SLATE, loc="left", pad=15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.3, color=COLOR_LIGHT_SLATE)
    ax1.set_axisbelow(True)

    # Callout for Q4 Surge placed cleanly above November bar without touching title
    ax1.annotate("Q4 Peak: £1,452k\n(+81.2% Surge)",
                 xy=(11, 1452.8), xytext=(8.0, 1510),
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor=COLOR_EMERALD, linewidth=1.1),
                 fontsize=9, weight="bold", color=COLOR_EMERALD,
                 arrowprops=dict(arrowstyle="->", color=COLOR_EMERALD, lw=1.1))

    # Panel B: Geographic AOV Comparison (Calibrated xlim=1250 and upper right legend)
    countries = ["United Kingdom", "Netherlands", "EIRE", "Germany", "France", "Australia"]
    median_aov = [299.67, 814.90, 625.30, 319.45, 345.10, 430.20]
    mean_aov = [488.50, 1054.20, 960.40, 462.80, 485.60, 1074.80]
    y_pos = np.arange(len(countries))
    h = 0.35

    rects_med = ax2.barh(y_pos - h / 2, median_aov, height=h, color=COLOR_EMERALD, label="Median AOV (£)")
    rects_mean = ax2.barh(y_pos + h / 2, mean_aov, height=h, color=COLOR_MUTED_SLATE, label="Mean AOV (£)")

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(countries, fontsize=10.5, weight="bold", color=COLOR_DARK_SLATE)
    ax2.set_xlabel("Order Value in £", fontsize=10, weight="bold", color=COLOR_DARK_SLATE, labelpad=10)
    ax2.set_xlim(0, 1250)
    ax2.set_title("Panel B: Cross-Border Wholesale vs. UK Domestic AOV", fontsize=12, weight="bold", color=COLOR_DARK_SLATE, loc="left", pad=15)
    ax2.legend(loc="upper right", frameon=False, fontsize=9.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.xaxis.grid(True, linestyle="--", alpha=0.3, color=COLOR_LIGHT_SLATE)
    ax2.set_axisbelow(True)

    for rect in rects_med:
        w = rect.get_width()
        ax2.text(w + 14, rect.get_y() + rect.get_height() / 2, f"£{w:.0f}", va="center", ha="left", fontsize=9, weight="bold", color=COLOR_EMERALD)

    plt.tight_layout(rect=[0.04, 0.04, 0.96, 0.85])
    plt.savefig("assets/fig3_country_seasonality_regime.png", dpi=300)
    plt.close()


# ==============================================================================
# FIGURE 4: BUNDLE REVENUE WATERFALL & MARGIN SIMULATION
# ==============================================================================
def export_fig4():
    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Titles and Headers with calibrated vertical separation (Task 2.1.1)
    fig.text(0.04, 0.950, "Deploying Five High-Affinity Bundles Captures Incremental Cross-Sell Margin Without Breaching Return Guardrails",
             fontsize=14, weight="bold", color=COLOR_NAVY)
    fig.text(0.04, 0.905, "Financial policy simulation under 10% promotional discount confirms £2,948 net incremental profit per cycle with low return risk",
             fontsize=11, color=COLOR_MUTED_SLATE)

    steps = ["Gross Incremental\nCross-Sell Attach", "Less Promotional\nDiscount Cost", "Net Incremental\nRevenue Lift"]
    vals = [3549.72, -601.68, 2948.04]

    # Bar Positions and Running Levels
    bottoms = [0, 3549.72 - 601.68, 0]
    heights = [3549.72, -601.68, 2948.04]
    bar_cols = [COLOR_EMERALD, COLOR_CRIMSON, COLOR_EMERALD]

    bars = ax.bar([0, 1, 2], [abs(h) for h in heights], bottom=[bottoms[0], bottoms[1], 0],
                  width=0.52, color=bar_cols, edgecolor=COLOR_DARK_SLATE, linewidth=1.1)

    # Step Connector Lines
    ax.plot([0, 1], [3549.72, 3549.72], color=COLOR_MUTED_SLATE, linestyle=":", lw=1.4)
    ax.plot([1, 2], [2948.04, 2948.04], color=COLOR_MUTED_SLATE, linestyle=":", lw=1.4)

    # Value Labels
    ax.text(0, 3549.72 / 2, "+£3,549.72", ha="center", va="center", color="#FFFFFF", fontsize=11, weight="bold")
    ax.text(1, 2948.04 + (601.68 / 2), "-£601.68", ha="center", va="center", color="#FFFFFF", fontsize=11, weight="bold")
    ax.text(2, 2948.04 / 2, "+£2,948.04", ha="center", va="center", color="#FFFFFF", fontsize=11, weight="bold")

    # Guardrail Callout Card with proper typographic bullets (Task 2.1.5)
    card_text = (
        "Guardrail 1: SKU Return Safety\n"
        "• Regency Teaware: 1.70% / 1.34% Return Rate\n"
        "• Jumbo Storage Bags: 1.39% / 1.48% Return Rate\n"
        "• Bakelike Clocks: 1.90% / 2.05% Return Rate\n"
        "• Lunch Bags: 1.83% / 1.32% Return Rate\n"
        "• Poppy's Playhouse: 0.58% / 0.73% Return Rate\n"
        "Status: 100% Pass (< 5.0% Risk Limit)"
    )
    # Positioned cleanly above waterfall connectors with generous clearance
    ax.text(0.04, 0.94, card_text, transform=ax.transAxes, fontsize=9.2, verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.55", facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1.1),
            color=COLOR_DARK_SLATE, linespacing=1.4)

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(steps, fontsize=10.5, weight="bold", color=COLOR_DARK_SLATE)
    ax.set_ylabel("Revenue Impact (£ at 10% Bundle Discount)", fontsize=10.5, weight="bold", color=COLOR_DARK_SLATE, labelpad=10)
    ax.set_ylim(0, 4800)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.3, color=COLOR_LIGHT_SLATE)
    ax.set_axisbelow(True)

    plt.tight_layout(rect=[0.04, 0.04, 0.96, 0.85])
    plt.savefig("assets/fig4_bundle_revenue_waterfall.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    print("Re-rendering calibrated presentation figures...")
    export_fig1()
    export_fig2()
    export_fig3()
    export_fig4()
    print("All figures successfully exported to assets/ at 300 DPI.")
