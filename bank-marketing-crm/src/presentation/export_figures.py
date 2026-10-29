"""
Static Chart Export Module (Phase 4).
Generates publication-quality 300-DPI charts for the Bank Direct Marketing executive report.

Follows strict editorial design rules:
- Archival paper background (#FAF8F2)
- Zero em dashes or en dashes
- Zero priority code labels (uses Phase 1, Phase 2, Phase 3)
- Sentence case titles
- Clean headroom and legible annotations
- Whole-number rounding for percentages, minutes, and multipliers
"""

import os
from pathlib import Path

# Set matplotlib cache directory to avoid permissions issues in sandboxes
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Paths
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "exports"
REPORTS_DIR = ROOT_DIR / "reports"
ASSETS_DIR = ROOT_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Visual Identity Palette
BG_CANVAS = "#FAF8F2"
BG_CARD = "#FFFFFF"
BORDER_GRID = "#111111"
COLOR_INK = "#111111"
COLOR_CHARCOAL = "#27272A"
COLOR_EMERALD = "#16A34A"
COLOR_CRIMSON = "#BE123C"
COLOR_AMBER = "#D97706"
COLOR_MUTED = "#71717A"
COLOR_LIGHT_ACCENT = "#E4DCD0"

# Matplotlib global defaults
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
plt.rcParams["figure.facecolor"] = BG_CANVAS
plt.rcParams["axes.facecolor"] = BG_CANVAS
plt.rcParams["text.color"] = COLOR_INK
plt.rcParams["axes.labelcolor"] = COLOR_INK
plt.rcParams["xtick.color"] = COLOR_INK
plt.rcParams["ytick.color"] = COLOR_INK


def export_figure_1():
    """
    Figure 1: Contact Fatigue Cliff.
    Left Panel: Paired comparison of Calls 1 to 3 vs Calls 4 to 56.
    Right Panel: Monotonic decay across call attempts with 8% guardrail.
    """
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(15, 6.8), dpi=300)

    # ------------------ LEFT PANEL ------------------
    # Data: Calls 1 to 3 vs Calls 4 to 56
    categories = ["Calls 1 to 3\n(Recommended limit)", "Calls 4 to 56\n(Fatigue zone)"]
    call_shares = [51.82, 48.18]
    sub_shares = [88.04, 11.96]

    x = np.arange(len(categories))
    width = 0.32

    rects1 = ax_left.bar(x - width / 2, call_shares, width, label="Share of calls dialed", color=COLOR_CHARCOAL, edgecolor=BORDER_GRID)
    rects2 = ax_left.bar(x + width / 2, sub_shares, width, label="Share of sign-ups won", color=[COLOR_EMERALD, COLOR_CRIMSON], edgecolor=BORDER_GRID)

    # Value labels rounded to whole numbers
    for rect in rects1:
        h = rect.get_height()
        ax_left.annotate(f"{round(h):.0f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                         fontsize=11, fontweight="bold", color=COLOR_CHARCOAL)

    for i, rect in enumerate(rects2):
        h = rect.get_height()
        c = COLOR_EMERALD if i == 0 else COLOR_CRIMSON
        ax_left.annotate(f"{round(h):.0f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                         fontsize=11, fontweight="bold", color=c)

    # Additional text callouts in left panel rounded to whole numbers
    ax_left.text(0, -18, "Yield: 7% per call\nTalk time: 36 min/sign-up", ha="center", va="top",
                 fontsize=10, bbox=dict(boxstyle="round,pad=0.4", facecolor=BG_CARD, edgecolor=COLOR_EMERALD, linewidth=1.2))
    ax_left.text(1, -18, "Yield: 1% per call\nTalk time: 51 min/sign-up\n(+41% agent labor penalty)", ha="center", va="top",
                 fontsize=10, bbox=dict(boxstyle="round,pad=0.4", facecolor=BG_CARD, edgecolor=COLOR_CRIMSON, linewidth=1.2))

    ax_left.set_ylabel("Share of portfolio total (%)", fontsize=11, fontweight="bold")
    ax_left.set_xticks(x)
    ax_left.set_xticklabels(categories, fontsize=11, fontweight="bold")
    ax_left.set_ylim(0, 108)
    ax_left.legend(frameon=True, facecolor=BG_CARD, edgecolor=BORDER_GRID, loc="upper right")
    ax_left.spines["top"].set_visible(False)
    ax_left.spines["right"].set_visible(False)
    ax_left.grid(axis="y", linestyle=":", alpha=0.5, color=COLOR_MUTED)

    # ------------------ RIGHT PANEL ------------------
    # Data: Conversion rate by call attempt
    attempts = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11-15", "16-56"]
    rates = [13.04, 11.46, 10.75, 9.39, 7.50, 7.66, 6.04, 4.25, 6.01, 5.33, 4.28, 1.41]
    bar_colors = [COLOR_EMERALD if r >= 8.0 else COLOR_CRIMSON for r in rates]

    bars = ax_right.bar(attempts, rates, color=bar_colors, edgecolor=BORDER_GRID, width=0.62)

    # Label on bars rounded to whole numbers
    for bar in bars:
        h = bar.get_height()
        ax_right.annotate(f"{round(h):.0f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                          xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                          fontsize=9, fontweight="bold")

    # Guardrail line at 8%
    ax_right.axhline(8.0, color=COLOR_AMBER, linestyle="--", linewidth=1.8, label="8% conversion goal (Guardrail 1)")

    # Annotation for attempt 5 breach
    ax_right.annotate("Attempt 5 (8%):\nDrops below 8% goal\nOdds drop 12% per call",
                      xy=(4, 7.50), xytext=(4.2, 11.5),
                      arrowprops=dict(facecolor=COLOR_AMBER, edgecolor=COLOR_AMBER, shrink=0.08, width=1.5, headwidth=6),
                      fontsize=9.5, fontweight="bold",
                      bbox=dict(boxstyle="square,pad=0.35", facecolor=BG_CARD, edgecolor=COLOR_AMBER, linewidth=1.2))

    ax_right.set_ylabel("Cohort conversion rate (%)", fontsize=11, fontweight="bold")
    ax_right.set_xlabel("Outbound call attempt", fontsize=11, fontweight="bold")
    ax_right.set_ylim(0, 16.5)
    ax_right.legend(frameon=True, facecolor=BG_CARD, edgecolor=BORDER_GRID, loc="upper right")
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["right"].set_visible(False)
    ax_right.grid(axis="y", linestyle=":", alpha=0.5, color=COLOR_MUTED)

    # Master Figure Headers (Clean sentence case without jargon)
    fig.suptitle("Calling prospects past 3 attempts uses 48% of phone time for just 12% of sign-ups",
                 fontsize=15.5, fontweight="bold", color=COLOR_INK, y=0.98)
    fig.text(0.5, 0.925,
             "Share of outbound calls vs. share of sign-ups and conversion rate by call attempt (41,188 prospects; 105,754 calls)",
             ha="center", fontsize=11, color=COLOR_CHARCOAL)

    plt.tight_layout(rect=[0.02, 0.08, 0.98, 0.91])
    out_path = ASSETS_DIR / "fig1_contact_fatigue_cliff.png"
    plt.savefig(out_path, dpi=300, facecolor=BG_CANVAS)
    plt.close()
    print(f"Saved: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def export_figure_2():
    """
    Figure 2: Channel and Prior Outcome Matrix.
    Left Panel: Cellular mobile vs Telephone landline comparison.
    Right Panel: Prior campaign outcome and 7-day recency speed comparison.
    """
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(15, 6.8), dpi=300)

    # ------------------ LEFT PANEL: Channel ------------------
    channels = ["Cellular mobile", "Telephone landline"]
    conv_rates = [14.74, 5.23]
    call_yields = [6.13, 1.84]

    x = np.arange(len(channels))
    width = 0.32

    rects1 = ax_left.bar(x - width / 2, conv_rates, width, label="Conversion rate per lead (%)",
                         color=[COLOR_EMERALD, COLOR_CHARCOAL], edgecolor=BORDER_GRID)
    rects2 = ax_left.bar(x + width / 2, call_yields, width, label="Yield per 100 calls dialed (%)",
                         color=["#86EFAC", "#A1A1AA"], edgecolor=BORDER_GRID)

    for rect in rects1:
        h = rect.get_height()
        ax_left.annotate(f"{round(h):.0f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                         fontsize=11, fontweight="bold")

    for rect in rects2:
        h = rect.get_height()
        ax_left.annotate(f"{round(h):.0f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                         fontsize=10, fontweight="bold")

    # Ratio callout with whole numbers
    ax_left.text(0.5, 12.0, "Mobile Advantage:\n3x conversion lift\n(15% vs. 5% conversion)",
                 ha="center", va="center", fontsize=10.5, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor=BG_CARD, edgecolor=BORDER_GRID, linewidth=1.2))

    ax_left.set_ylabel("Rate (%)", fontsize=11, fontweight="bold")
    ax_left.set_xticks(x)
    ax_left.set_xticklabels(channels, fontsize=11, fontweight="bold")
    ax_left.set_ylim(0, 18.5)
    ax_left.legend(frameon=True, facecolor=BG_CARD, edgecolor=BORDER_GRID, loc="upper right")
    ax_left.spines["top"].set_visible(False)
    ax_left.spines["right"].set_visible(False)
    ax_left.grid(axis="y", linestyle=":", alpha=0.5, color=COLOR_MUTED)

    # ------------------ RIGHT PANEL: Prior Outcome & Recency ------------------
    segments = [
        "Past buyer\n(Overall: 65%)",
        "Fast contact\n(Within 7 days)",
        "Later contact\n(8 to 14 days)",
        "Past failure\n(Overall: 14%)",
        "Never called\n(Overall: 9%)"
    ]
    poutcome_rates = [65.11, 65.76, 56.88, 14.23, 8.83]
    colors = [COLOR_EMERALD, "#15803D", "#86EFAC", COLOR_AMBER, COLOR_CHARCOAL]

    bars = ax_right.bar(segments, poutcome_rates, color=colors, edgecolor=BORDER_GRID, width=0.58)

    for bar in bars:
        h = bar.get_height()
        ax_right.annotate(f"{round(h):.0f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                          xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                          fontsize=10, fontweight="bold")

    ax_right.annotate("7-Day Fast-Lane Rule:\nLeads called within 7 days\nconvert at 66%",
                      xy=(1, 65.76), xytext=(1.5, 74.0),
                      arrowprops=dict(facecolor=COLOR_EMERALD, edgecolor=COLOR_EMERALD, shrink=0.08, width=1.5, headwidth=6),
                      fontsize=10, fontweight="bold",
                      bbox=dict(boxstyle="square,pad=0.4", facecolor=BG_CARD, edgecolor=COLOR_EMERALD, linewidth=1.2))

    ax_right.set_ylabel("Lead conversion rate (%)", fontsize=11, fontweight="bold")
    ax_right.set_ylim(0, 84.0)
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["right"].set_visible(False)
    ax_right.grid(axis="y", linestyle=":", alpha=0.5, color=COLOR_MUTED)

    # Master Figure Headers (Sentence case)
    fig.suptitle("Mobile calls convert at 3x the rate of landlines, and past buyers convert at 65%",
                 fontsize=15.5, fontweight="bold", color=COLOR_INK, y=0.98)
    fig.text(0.5, 0.925,
             "Conversion rate and sign-ups per 100 calls by phone type, past campaign result, and follow-up timing",
             ha="center", fontsize=11, color=COLOR_CHARCOAL)

    plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.91])
    out_path = ASSETS_DIR / "fig2_channel_poutcome_matrix.png"
    plt.savefig(out_path, dpi=300, facecolor=BG_CANVAS)
    plt.close()
    print(f"Saved: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def export_figure_3():
    """
    Figure 3: Macroeconomic and Demographic Matrix.
    Left Panel: 4x4 heatmap of Age Group by Job Tier conversion rates.
    Right Panel: Euribor interest rate periods and bank balance comparison.
    """
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(15.5, 7.0), dpi=300)

    # ------------------ LEFT PANEL: 4x4 Heatmap ------------------
    row_labels = ["Senior 60+", "Young (<30)", "Mature (46-60)", "Core (31-45)"]
    col_labels = ["White-Collar", "Students/Retirees", "Blue-Collar", "Unknown"]

    matrix = np.array([
        [51.1, 45.8, 40.0, 38.1],
        [16.4, 30.7, 10.3, 27.3],
        [11.1, 12.8,  7.7,  6.6],
        [10.7, 13.1,  8.1,  7.9]
    ])

    im = ax_left.imshow(matrix, cmap="YlGn", vmin=5.0, vmax=55.0, aspect="auto")

    # Ticks and labels
    ax_left.set_xticks(np.arange(len(col_labels)))
    ax_left.set_yticks(np.arange(len(row_labels)))
    ax_left.set_xticklabels(col_labels, fontsize=10.5, fontweight="bold")
    ax_left.set_yticklabels(row_labels, fontsize=10.5, fontweight="bold")

    # Annotate whole numbers in cells
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = matrix[i, j]
            text_color = "white" if val > 28.0 else COLOR_INK
            ax_left.text(j, i, f"{round(val):.0f}%", ha="center", va="center",
                         fontsize=11.5, fontweight="bold", color=text_color)

    # Clean borders
    for spine in ax_left.spines.values():
        spine.set_edgecolor(BORDER_GRID)
        spine.set_linewidth(1.0)

    ax_left.set_title("Conversion rate by age group and job tier", fontsize=12, fontweight="bold", pad=12)
    cbar = fig.colorbar(im, ax=ax_left, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Conversion rate (%)", fontsize=10, fontweight="bold")

    # ------------------ RIGHT PANEL: Macro & Balance ------------------
    categories = [
        "Low Euribor rate\n(<= 3% period)",
        "High Euribor rate\n(> 3% period)",
        "Balance > 448 EUR\n(Above median)",
        "Balance <= 448 EUR\n(Below median)"
    ]
    rates = [24.46, 4.84, 14.33, 9.06]
    bar_colors = [COLOR_EMERALD, COLOR_CRIMSON, COLOR_EMERALD, COLOR_CHARCOAL]

    bars = ax_right.bar(categories, rates, color=bar_colors, edgecolor=BORDER_GRID, width=0.55)

    for bar in bars:
        h = bar.get_height()
        ax_right.annotate(f"{round(h):.0f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                          xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                          fontsize=10.5, fontweight="bold")

    # Annotations with clean whole numbers
    ax_right.text(0.5, 20.0, "Interest Rate Impact:\n5x conversion lift\n(24% vs. 5% conversion)",
                  ha="center", va="center", fontsize=10, fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.4", facecolor=BG_CARD, edgecolor=BORDER_GRID, linewidth=1.1))

    ax_right.text(2.5, 12.0, "Account Balance Check:\n1.6x conversion lift\n(14% vs. 9% conversion)",
                  ha="center", va="center", fontsize=10, fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.4", facecolor=BG_CARD, edgecolor=BORDER_GRID, linewidth=1.1))

    ax_right.set_ylabel("Conversion rate (%)", fontsize=11, fontweight="bold")
    ax_right.set_ylim(0, 30.0)
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["right"].set_visible(False)
    ax_right.grid(axis="y", linestyle=":", alpha=0.5, color=COLOR_MUTED)

    # Master Figure Headers (Sentence case)
    fig.suptitle("Over half of calls go to 31-45 year olds (9% conversion), while seniors (45%) and low-rate periods (24%) lead",
                 fontsize=14.5, fontweight="bold", color=COLOR_INK, y=0.98)
    fig.text(0.5, 0.925,
             "Conversion rate by age group and job type alongside 2008 to 2010 interest rate periods",
             ha="center", fontsize=11, color=COLOR_CHARCOAL)

    plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.91])
    out_path = ASSETS_DIR / "fig3_macro_demographic_heatmap.png"
    plt.savefig(out_path, dpi=300, facecolor=BG_CANVAS)
    plt.close()
    print(f"Saved: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def export_figure_4():
    """
    Figure 4: Policy Reallocation Waterfall.
    Step-by-step comparison across baseline, 3-call cap, and reallocation scenarios.
    """
    fig, ax1 = plt.subplots(figsize=(14.5, 7.0), dpi=300)

    scenarios = [
        "Current Baseline\n(Uncapped calls)",
        "Phase 1: 3-Call Cap\n(Cap only; 475h saved)",
        "Scenario 2A\n(Conservative: +33%)",
        "Scenario 2B\n(Low-rate priority: +59%)",
        "Scenario 2C\n(Full bandwidth: +70%)"
    ]
    signups = [4640, 4085, 6175, 7362, 7882]
    talk_minutes = [38.2, 36.4, 28.7, 24.1, 22.5]
    colors = [COLOR_CHARCOAL, "#60A5FA", COLOR_EMERALD, "#15803D", "#047857"]

    x = np.arange(len(scenarios))
    bars = ax1.bar(x, signups, color=colors, edgecolor=BORDER_GRID, width=0.55, label="Total sign-ups won")

    # Baseline comparison reference line
    ax1.axhline(4640, color=COLOR_MUTED, linestyle=":", linewidth=1.5, label="Current baseline (4,640 sign-ups)")
    # 85% retention threshold line
    ax1.axhline(4640 * 0.85, color=COLOR_AMBER, linestyle="--", linewidth=1.5, label="85% volume goal (3,944 sign-ups)")

    # Sign-up labels on top of bars
    for i, bar in enumerate(bars):
        h = bar.get_height()
        diff = h - 4640
        diff_str = f" ({diff:+d})" if diff != 0 else ""
        ax1.annotate(f"{h:,}{diff_str}", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 5), textcoords="offset points", ha="center", va="bottom",
                     fontsize=10.5, fontweight="bold")

    # Secondary axis for talk time per sign-up
    ax2 = ax1.twinx()
    ax2.plot(x, talk_minutes, color=COLOR_CRIMSON, marker="o", linewidth=2.5, markersize=8, label="Agent talk minutes per sign-up")

    for i, val in enumerate(talk_minutes):
        ax2.annotate(f"{round(val):.0f} min", xy=(x[i], val),
                     xytext=(0, -18 if i in [0, 1] else 10), textcoords="offset points", ha="center",
                     fontsize=10, fontweight="bold", color=COLOR_CRIMSON,
                     bbox=dict(boxstyle="round,pad=0.25", facecolor=BG_CARD, edgecolor=COLOR_CRIMSON, linewidth=1.0))

    ax1.set_ylabel("Total term deposit sign-ups", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Agent talk minutes per sign-up", fontsize=11, fontweight="bold", color=COLOR_CRIMSON)
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, fontsize=10.5, fontweight="bold")
    ax1.set_ylim(0, 9400)
    ax2.set_ylim(15, 45)

    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax1.grid(axis="y", linestyle=":", alpha=0.5, color=COLOR_MUTED)

    # Combine legends cleanly
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=True, facecolor=BG_CARD, edgecolor=BORDER_GRID, loc="upper left")

    # Master Figure Headers (Sentence case)
    fig.suptitle("Capping calls at 3 attempts and redirecting saved time adds 1,535 to 3,242 extra sign-ups",
                 fontsize=15.5, fontweight="bold", color=COLOR_INK, y=0.98)
    fig.text(0.5, 0.925,
             "Total term deposit sign-ups and agent talk minutes per sign-up across our rollout options",
             ha="center", fontsize=11, color=COLOR_CHARCOAL)

    plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.91])
    out_path = ASSETS_DIR / "fig4_policy_reallocation_waterfall.png"
    plt.savefig(out_path, dpi=300, facecolor=BG_CANVAS)
    plt.close()
    print(f"Saved: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def main():
    print("Generating Phase 4 static chart export figures with whole numbers...")
    export_figure_1()
    export_figure_2()
    export_figure_3()
    export_figure_4()
    print("All 4 figures successfully exported to assets/ at 300 DPI.")


if __name__ == "__main__":
    main()
