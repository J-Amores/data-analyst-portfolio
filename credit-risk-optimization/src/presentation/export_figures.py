"""
src/presentation/export_figures.py
Consumer Credit Risk & Underwriting Optimization
Figure Generation Pipeline: Warm Editorial Paper Binder Aesthetic

Generates three high-resolution static PNG figures (300 DPI, #FAF8F2 warm paper canvas,
crisp 1px solid #111111 lines) into assets/:
  1. assets/fig1_loss_contribution.png: Paired bar chart contrasting Lending Share vs. Unpaid Loss Share across Grades A to G.
  2. assets/fig2_risk_grid_heatmap.png: 2D Heatmap across Monthly Debt Ratio (DTI) vs. Credit Card Usage with bounding callout.
  3. assets/fig3_capital_waterfall.png: Financial impact waterfall illustrating Phase 1 capital recovery.

Guardrail Compliance: Zero em dashes, zero en dashes, zero priority code or Act labels in code, comments, and figure annotations.
"""

import os
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib_cache"

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap


# Editorial Paper Canvas Color Palette
COLOR_BG_PAPER = "#FAF8F2"       # Warm archival off-white paper canvas
COLOR_BG_CARD = "#FDFBF3"        # Pure cream card highlight
COLOR_INK_BLACK = "#111111"      # Primary ink black for text, spines, and hairlines
COLOR_INK_MUTED = "#4A4843"      # Secondary body copy and subtitles
COLOR_LENDING_CHARCOAL = "#27272A"# Deep charcoal for lending share / baseline
COLOR_LOSS_CRIMSON = "#E11D48"   # Warm crimson for unpaid losses / default risk
COLOR_SAVED_GREEN = "#16A34A"    # Kelly green for saved capital / recoveries
COLOR_CALLOUT_LAVENDER = "#F3E8FF"# Soft lavender callout fill


def setup_figure_style():
    """Configures global matplotlib styling for warm editorial paper binder exports."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        "font.serif": ["Georgia", "DejaVu Serif"],
        "figure.facecolor": COLOR_BG_PAPER,
        "axes.facecolor": COLOR_BG_PAPER,
        "axes.edgecolor": COLOR_INK_BLACK,
        "axes.linewidth": 1.0,
        "grid.color": "#E5E1D8",
        "text.color": COLOR_INK_BLACK,
        "axes.labelcolor": COLOR_INK_BLACK,
        "xtick.color": COLOR_INK_BLACK,
        "ytick.color": COLOR_INK_BLACK,
        "savefig.facecolor": COLOR_BG_PAPER,
        "figure.autolayout": False,
    })


def generate_fig1_loss_contribution(assets_dir: Path):
    """
    Figure 1: Paired bar chart across Loan Grades A through G.
    Compares Lending Share (%) vs. Unpaid Loss Share (%).
    Highlights Subprime loss skew (28.5% Lending vs. 51.5% Losses).
    """
    print("[TASK] Generating Figure 1: Loss Contribution Asymmetry...")
    csv_path = Path("data/exports/h1_loss_contribution_by_grade.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing data source: {csv_path}")

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)

    grades = df["grade"].tolist()
    capital_share = df["capital_share_pct"].tolist()
    loss_share = df["net_charge_off_share_pct"].tolist()

    x = np.arange(len(grades))
    bar_width = 0.36

    # Plot paired bars with crisp 1px hairline edges
    rects1 = ax.bar(
        x - bar_width / 2,
        capital_share,
        bar_width,
        label="Lending Share (%)",
        color=COLOR_LENDING_CHARCOAL,
        edgecolor=COLOR_INK_BLACK,
        linewidth=1.0,
        zorder=3,
    )
    rects2 = ax.bar(
        x + bar_width / 2,
        loss_share,
        bar_width,
        label="Unpaid Loss Share (%)",
        color=COLOR_LOSS_CRIMSON,
        edgecolor=COLOR_INK_BLACK,
        linewidth=1.0,
        zorder=3,
    )

    # Headline and subtitle
    plt.suptitle(
        "Subprime Tiers Receive 28.5% of Lending but Cause 51.5% of Unpaid Losses",
        fontsize=14.5,
        fontweight="bold",
        fontfamily="Georgia",
        color=COLOR_INK_BLACK,
        x=0.08,
        y=0.98,
        ha="left",
    )
    ax.set_title(
        "Comparison of Funded Principal vs. Net Charge-Off Dollars Across Credit Grades A to G (1.35M Completed Loans)",
        fontsize=10.5,
        fontfamily="DejaVu Sans",
        color=COLOR_INK_MUTED,
        pad=18,
        loc="left",
    )

    # Bar value labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=COLOR_LENDING_CHARCOAL,
        )

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=COLOR_LOSS_CRIMSON,
        )

    # Subprime callout bracket across Grades D, E, F, G (indices 3, 4, 5, 6)
    x_subprime_start = x[3] - bar_width - 0.1
    x_subprime_end = x[6] + bar_width + 0.1
    y_bracket = 31.5

    # Shaded lavender highlight for Subprime Grades D to G
    subprime_patch = patches.Rectangle(
        (x_subprime_start, 0),
        x_subprime_end - x_subprime_start,
        34.5,
        linewidth=1.0,
        edgecolor=COLOR_INK_BLACK,
        facecolor=COLOR_CALLOUT_LAVENDER,
        alpha=0.45,
        linestyle="--",
        zorder=1,
    )
    ax.add_patch(subprime_patch)

    # Annotated badge for Subprime loss skew
    ax.annotate(
        "Subprime (Grades D-G): 28.5% of Lending vs. 51.5% of Losses (1.81x Imbalance)\nChi-Square = 1.02B (p < 0.001) | $1.40B Unpaid Losses",
        xy=((x_subprime_start + x_subprime_end) / 2, y_bracket),
        xytext=(0, 0),
        textcoords="offset points",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.55", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.0),
        zorder=5,
    )

    # Prime label
    ax.annotate(
        "Prime Tiers (Grades A to C):\n71.6% Lending | 48.6% Losses",
        xy=(1.0, 31.5),
        xytext=(0, 0),
        textcoords="offset points",
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.5", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.0),
        zorder=5,
    )

    # Axes configuration
    ax.set_xticks(x)
    ax.set_xticklabels([f"Grade {g}" for g in grades], fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Share of Portfolio (%)", fontsize=10.5, fontweight="bold", labelpad=8)
    ax.set_ylim(0, 36.5)

    # Exposed 1px solid #111111 hairlines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_INK_BLACK)
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["bottom"].set_color(COLOR_INK_BLACK)
    ax.spines["bottom"].set_linewidth(1.0)
    ax.grid(False)

    ax.legend(
        loc="upper left",
        frameon=True,
        facecolor=COLOR_BG_CARD,
        edgecolor=COLOR_INK_BLACK,
        fontsize=9.5,
    )

    plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.93])
    out_file = assets_dir / "fig1_loss_contribution.png"
    plt.savefig(out_file, dpi=300, facecolor=COLOR_BG_PAPER)
    plt.close()
    print(f"[TASK] Saved: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")


def generate_fig2_risk_grid_heatmap(assets_dir: Path):
    """
    Figure 2: 2D Risk Grid Heatmap across Monthly Debt Ratio (DTI) and Credit Card Usage.
    Displays Terminal Default Rate (%) and loan counts in each cell.
    Highlights high-risk intersection (DTI > 25% and Card Usage > 65% at 28.41% default rate).
    """
    print("[TASK] Generating Figure 2: Multi-Variable Risk Grid Heatmap...")
    csv_path = Path("data/exports/segment_risk_grid.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing data source: {csv_path}")

    df = pd.read_csv(csv_path)

    # Display labels for brackets
    dti_display_labels = [
        "Low (<=15%)",
        "Moderate (15-25%)",
        "High (25-35%)",
        "Severe (>35%)",
    ]
    util_display_labels = [
        "Conservative (<=40%)",
        "Moderate (40-65%)",
        "High (65-85%)",
        "Maxed (>85%)",
    ]

    rate_pivot = df.pivot(
        index="dti_bracket",
        columns="revol_util_bracket",
        values="terminal_bad_rate_pct",
    )
    vol_pivot = df.pivot(
        index="dti_bracket",
        columns="revol_util_bracket",
        values="volume",
    )

    rate_matrix = rate_pivot.values
    vol_matrix = vol_pivot.values

    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)

    # Warm cream-to-coral-red colormap matching paper aesthetic
    custom_cmap = LinearSegmentedColormap.from_list(
        "WarmPaperRisk",
        ["#FAF8F2", "#FDE8E8", "#FCA5A5", "#FB7185", "#E11D48", "#9F1239"],
        N=256,
    )

    cax = ax.imshow(
        rate_matrix,
        cmap=custom_cmap,
        aspect="auto",
        vmin=12.0,
        vmax=34.0,
    )

    # Headline and subtitle
    plt.suptitle(
        "Combined Borrower Stress: High Debt and Card Usage Double Default Rates to 28.4%",
        fontsize=14.5,
        fontweight="bold",
        fontfamily="Georgia",
        color=COLOR_INK_BLACK,
        x=0.08,
        y=0.98,
        ha="left",
    )
    ax.set_title(
        "Terminal Default Rate (%) and Loan Count Across 4x4 Debt Ratio and Credit Card Usage Segments (1.34M Completed Loans)",
        fontsize=10.5,
        fontfamily="DejaVu Sans",
        color=COLOR_INK_MUTED,
        pad=18,
        loc="left",
    )

    nrows, ncols = rate_matrix.shape

    # Draw crisp 1px solid #111111 borders around every single cell
    for i in range(nrows):
        for j in range(ncols):
            cell_rect = patches.Rectangle(
                (j - 0.5, i - 0.5),
                1.0,
                1.0,
                linewidth=1.0,
                edgecolor=COLOR_INK_BLACK,
                facecolor="none",
                zorder=4,
            )
            ax.add_patch(cell_rect)

            val = rate_matrix[i, j]
            vol = vol_matrix[i, j]
            text_color = "#FFFFFF" if val > 27.0 else COLOR_INK_BLACK
            ax.text(
                j,
                i - 0.12,
                f"{val:.2f}%",
                ha="center",
                va="center",
                color=text_color,
                fontsize=11.5,
                fontweight="bold",
                zorder=5,
            )
            ax.text(
                j,
                i + 0.18,
                f"({vol:,} loans)",
                ha="center",
                va="center",
                color=text_color,
                fontsize=8.5,
                alpha=0.92,
                zorder=5,
            )

    # Bold 2.5px solid #111111 box around the high-risk intersection
    # DTI > 25% (rows 2, 3) and Util > 65% (cols 2, 3)
    high_risk_rect = patches.Rectangle(
        (1.5, 1.5),
        2.0,
        2.0,
        linewidth=2.5,
        edgecolor=COLOR_INK_BLACK,
        facecolor="none",
        linestyle="-",
        zorder=10,
    )
    ax.add_patch(high_risk_rect)

    # High-risk annotation badge
    ax.annotate(
        "High-Risk Intersection (DTI > 25% & Card Usage > 65%)\n112,246 Loans | 28.41% Default Rate\nRelative Risk = 2.01x vs. Baseline (Odds Ratio = 1.67x, Chi-Square = 5,464.86, p < 0.001)",
        xy=(2.5, 1.5),
        xytext=(2.5, 1.15),
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.5", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.5),
        arrowprops=dict(arrowstyle="->", color=COLOR_INK_BLACK, lw=1.5),
        zorder=12,
    )

    # Benchmark callout on top left cell
    ax.annotate(
        "Low-Risk Baseline: 14.11%",
        xy=(0.0, 0.42),
        xytext=(0.0, 0.42),
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.25", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.0),
        zorder=11,
    )

    ax.set_xticks(np.arange(ncols))
    ax.set_yticks(np.arange(nrows))
    ax.set_xticklabels(util_display_labels, fontsize=10.0, fontweight="bold")
    ax.set_yticklabels(dti_display_labels, fontsize=10.0, fontweight="bold")

    ax.set_xlabel("Credit Card Usage (Revolving Line Utilization)", fontsize=10.5, fontweight="bold", labelpad=8)
    ax.set_ylabel("Monthly Debt Ratio (DTI Bracket)", fontsize=10.5, fontweight="bold", labelpad=8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)

    cbar = plt.colorbar(cax, ax=ax, fraction=0.035, pad=0.04)
    cbar.set_label("Terminal Default Rate (%)", fontsize=9.5, fontweight="bold", labelpad=8, color=COLOR_INK_BLACK)
    cbar.outline.set_edgecolor(COLOR_INK_BLACK)
    cbar.outline.set_linewidth(1.0)
    cbar.ax.tick_params(color=COLOR_INK_BLACK, labelcolor=COLOR_INK_BLACK)

    plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.93])
    out_file = assets_dir / "fig2_risk_grid_heatmap.png"
    plt.savefig(out_file, dpi=300, facecolor=COLOR_BG_PAPER)
    plt.close()
    print(f"[TASK] Saved: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")


def generate_fig3_capital_waterfall(assets_dir: Path):
    """
    Figure 3: Financial Impact Waterfall Step Chart on Warm Paper Canvas.
    Step 1: Current Subprime Losses ($1,404.1M in Warm Crimson)
    Step 2: Phase 1 Decline Rule Savings (-$230.0M in Kelly Green)
    Step 3: Remaining Subprime Losses ($1,174.1M in Deep Charcoal)
    Badge: 95.81% of Lending Volume Kept ($18.58B Preserved)
    """
    print("[TASK] Generating Figure 3: Capital Recovery Waterfall...")
    json_path = Path("reports/h3_validation_results.json")
    if not json_path.exists():
        raise FileNotFoundError(f"Missing data source: {json_path}")

    with open(json_path, "r") as f:
        h3_data = json.load(f)

    sim = h3_data["policy_simulation"]
    base_subprime_losses = 1404.103  # $1,404.1M
    hard_stop_savings = sim["net_charge_off_dollars_eliminated"] / 1e6  # $230.04M
    post_policy_losses = base_subprime_losses - hard_stop_savings       # $1,174.06M

    retained_pct = sim["retained_capital_retention_rate_pct"]            # 95.81%
    retained_funded_b = sim["retained_funded_dollars"] / 1e9             # $18.58B
    defaults_eliminated = sim["avoided_defaults_count"]                  # 18,548
    laroc_bps = sim["post_policy_laroc_delta_bps"]                       # +14.9 bps

    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)

    categories = [
        "Current Subprime Losses\n(Grades D to G)",
        "Phase 1 Decline Savings\n(Targeted Hard-Stop)",
        "Remaining Subprime Losses\n(Preserved Book)",
    ]

    x = np.arange(len(categories))
    bar_width = 0.52

    # Step 1: Current Subprime Losses (Crimson)
    bar1 = ax.bar(
        x[0],
        base_subprime_losses,
        bar_width,
        color=COLOR_LOSS_CRIMSON,
        edgecolor=COLOR_INK_BLACK,
        linewidth=1.0,
        zorder=3,
    )

    # Step 2: Phase 1 Decline Savings (Kelly Green floating bar)
    bar2 = ax.bar(
        x[1],
        hard_stop_savings,
        bar_width,
        bottom=post_policy_losses,
        color=COLOR_SAVED_GREEN,
        edgecolor=COLOR_INK_BLACK,
        linewidth=1.0,
        zorder=3,
    )

    # Step 3: Remaining Subprime Losses (Deep Charcoal)
    bar3 = ax.bar(
        x[2],
        post_policy_losses,
        bar_width,
        color=COLOR_LENDING_CHARCOAL,
        edgecolor=COLOR_INK_BLACK,
        linewidth=1.0,
        zorder=3,
    )

    # Connectors between waterfall bars
    ax.plot(
        [x[0] + bar_width / 2, x[1] - bar_width / 2],
        [base_subprime_losses, base_subprime_losses],
        color=COLOR_INK_BLACK,
        linestyle="--",
        linewidth=1.0,
        zorder=2,
    )
    ax.plot(
        [x[1] + bar_width / 2, x[2] - bar_width / 2],
        [post_policy_losses, post_policy_losses],
        color=COLOR_INK_BLACK,
        linestyle="--",
        linewidth=1.0,
        zorder=2,
    )

    # Headline and subtitle
    plt.suptitle(
        "Automated Decline Rules Save $230M in Net Losses While Keeping 95.8% of Lending Volume",
        fontsize=14.5,
        fontweight="bold",
        fontfamily="Georgia",
        color=COLOR_INK_BLACK,
        x=0.08,
        y=0.98,
        ha="left",
    )
    ax.set_title(
        "Financial Impact of Targeted Decline Rule (Grades D-G with DTI > 25% and Card Usage > 65%) on Subprime Write-Offs",
        fontsize=10.5,
        fontfamily="DejaVu Sans",
        color=COLOR_INK_MUTED,
        pad=18,
        loc="left",
    )

    # Value annotations on bars
    ax.annotate(
        f"${base_subprime_losses:,.1f}M",
        xy=(x[0], base_subprime_losses),
        xytext=(0, 6),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=11.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
    )
    ax.annotate(
        "Baseline 51.5% Loss Share\n(335.8K loans)",
        xy=(x[0], base_subprime_losses / 2),
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#FFFFFF",
        zorder=4,
    )

    ax.annotate(
        f"-${hard_stop_savings:,.1f}M",
        xy=(x[1], base_subprime_losses),
        xytext=(0, 6),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=11.5,
        fontweight="bold",
        color=COLOR_SAVED_GREEN,
    )
    ax.annotate(
        f"Saved Losses\n({defaults_eliminated:,} defaults)",
        xy=(x[1], post_policy_losses + hard_stop_savings / 2),
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#FFFFFF",
        zorder=4,
    )

    ax.annotate(
        f"${post_policy_losses:,.1f}M",
        xy=(x[2], post_policy_losses),
        xytext=(0, 6),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=11.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
    )
    ax.annotate(
        "-16.4% Unpaid Losses\n(Preserved Book)",
        xy=(x[2], post_policy_losses / 2),
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#FFFFFF",
        zorder=4,
    )

    # Bordered callout note matching specification
    card_x = 1.35
    card_y = 1350
    badge_text = (
        "95.81% of Lending Volume Kept ($18.58B Preserved)\n"
        f"* Avoided Defaults: {defaults_eliminated:,} terminal bad loans\n"
        f"* Saved Net Losses: ${hard_stop_savings:.2f}M ($254.10M gross)\n"
        f"* Pruned Loan Volume: 3.55% (47,705 originations)\n"
        f"* Platform Return Lift: +{laroc_bps:.1f} bps (+4.26% to +4.40%)\n"
        f"* Solvency Guardrail: Preserved (>= 80.0% threshold)"
    )

    ax.annotate(
        badge_text,
        xy=(card_x, card_y),
        xytext=(0, 0),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=9.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(
            boxstyle="square,pad=0.7",
            facecolor=COLOR_BG_CARD,
            edgecolor=COLOR_INK_BLACK,
            linewidth=1.0,
        ),
        zorder=5,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Unpaid Net Losses ($ Millions)", fontsize=10.5, fontweight="bold", labelpad=8)
    ax.set_ylim(0, 1680)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_INK_BLACK)
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["bottom"].set_color(COLOR_INK_BLACK)
    ax.spines["bottom"].set_linewidth(1.0)
    ax.grid(False)

    plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.93])
    out_file = assets_dir / "fig3_capital_waterfall.png"
    plt.savefig(out_file, dpi=300, facecolor=COLOR_BG_PAPER)
    plt.close()
    print(f"[TASK] Saved: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")


def main():
    """Main execution function for figure generation."""
    setup_figure_style()
    assets_dir = Path("assets")
    assets_dir.mkdir(parents=True, exist_ok=True)

    print("================================================================================")
    print("FIGURE GENERATION PIPELINE: WARM PAPER BINDER AESTHETIC")
    print("================================================================================")

    generate_fig1_loss_contribution(assets_dir)
    generate_fig2_risk_grid_heatmap(assets_dir)
    generate_fig3_capital_waterfall(assets_dir)

    print("================================================================================")
    print("ALL THREE FIGURES SUCCESSFULLY EXPORTED TO assets/")
    print("================================================================================")


if __name__ == "__main__":
    main()
