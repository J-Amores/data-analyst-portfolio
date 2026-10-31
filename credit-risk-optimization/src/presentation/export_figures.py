"""
src/presentation/export_figures.py
Consumer Credit Risk & Underwriting Optimization
Figure Generation Pipeline: Warm Editorial Paper Binder Aesthetic

Generates three high-resolution static PNG figures (300 DPI, #FAF8F2 warm paper canvas,
crisp 1px solid #111111 lines) into assets/:
  1. assets/fig1_loss_contribution.png: Paired bar chart contrasting Lending Share vs. Unpaid Loss Share across Grades A to G.
  2. assets/fig2_risk_grid_heatmap.png: 2D Heatmap across Monthly Debt Ratio (DTI) vs. Credit Card Usage with bounding callout.
  3. assets/fig3_capital_waterfall.png: Financial impact waterfall illustrating Phase 1 capital recovery.

Guardrail Compliance: Zero em dashes, zero en dashes, zero statistical test jargon, whole-number rounding.
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
        "text.parse_math": False,
        "text.usetex": False,
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
    Highlights Subprime loss skew (28% Lending vs. 51% Losses).
    """
    print("[TASK] Generating Figure 1: Loss Contribution Asymmetry...")
    csv_path = Path("data/exports/h1_loss_contribution_by_grade.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing data source: {csv_path}")

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(9.8, 7.6), dpi=300)

    grades = df["grade"].tolist()
    capital_share = df["capital_share_pct"].tolist()
    loss_share = df["net_charge_off_share_pct"].tolist()

    x = np.arange(len(grades))
    bar_width = 0.38

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

    # Headline and subtitle in plain workplace English
    plt.suptitle(
        "Subprime Grades D to G Get 28% of Lending Money but Cause 51% of Unpaid Losses",
        fontsize=13.5,
        fontweight="bold",
        fontfamily="Georgia",
        color=COLOR_INK_BLACK,
        x=0.08,
        y=0.97,
        ha="left",
    )
    ax.set_title(
        "Share of dollars lent vs. share of unpaid write-offs across 1.35M completed loans ($19.4B book)",
        fontsize=9.8,
        fontfamily="DejaVu Sans",
        color=COLOR_INK_MUTED,
        pad=12,
        loc="left",
    )

    # Bar value labels rounded to whole percentages
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(
            f"{round(h):.0f}%",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.0,
            fontweight="bold",
            color=COLOR_LENDING_CHARCOAL,
        )

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(
            f"{round(h):.0f}%",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.0,
            fontweight="bold",
            color=COLOR_LOSS_CRIMSON,
        )

    # Subprime callout bracket across Grades D, E, F, G (indices 3, 4, 5, 6)
    x_subprime_start = x[3] - bar_width - 0.08
    x_subprime_end = x[6] + bar_width + 0.08
    y_bracket = 34.0

    # Shaded lavender highlight for Subprime Grades D to G
    subprime_patch = patches.Rectangle(
        (x_subprime_start, 0),
        x_subprime_end - x_subprime_start,
        38.0,
        linewidth=1.0,
        edgecolor=COLOR_INK_BLACK,
        facecolor=COLOR_CALLOUT_LAVENDER,
        alpha=0.45,
        linestyle="--",
        zorder=1,
    )
    ax.add_patch(subprime_patch)

    # Annotated badge for Subprime loss skew (plain English, no academic jargon)
    ax.annotate(
        "Subprime (Grades D-G): 28% of Lending vs. 51% of Losses\n(1.8x Loss Imbalance | $1.4B Lost)",
        xy=((x_subprime_start + x_subprime_end) / 2, y_bracket),
        xytext=(0, 0),
        textcoords="offset points",
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.45", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.0),
        zorder=5,
    )

    # Axes configuration: ylim 0 to 42 for plenty of whitespace above Grade C bars
    ax.set_xticks(x)
    ax.set_xticklabels([f"Grade {g}" for g in grades], fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Share of Portfolio (%)", fontsize=10.5, fontweight="bold", labelpad=8)
    ax.set_ylim(0, 42.0)

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
        bbox_to_anchor=(0.02, 0.98),
        ncol=2,
        frameon=True,
        facecolor=COLOR_BG_CARD,
        edgecolor=COLOR_INK_BLACK,
        fontsize=9.0,
    )

    # Bottom Strip (Plain English)
    fig.text(
        0.08,
        0.025,
        "Safer borrowers in Grades A to C bring in +$857M in net profit, which is currently eaten up by $1.4B in subprime write-offs.",
        fontsize=8.8,
        fontfamily="DejaVu Sans",
        fontstyle="italic",
        color=COLOR_INK_MUTED,
        ha="left",
    )

    plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.93])
    out_file = assets_dir / "fig1_loss_contribution.png"
    plt.savefig(out_file, dpi=300, facecolor=COLOR_BG_PAPER)
    plt.close()
    print(f"[TASK] Saved: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")


def generate_fig2_risk_grid_heatmap(assets_dir: Path):
    """
    Figure 2: 2D Risk Grid Heatmap across Monthly Debt Ratio (DTI) and Credit Card Usage.
    Displays Terminal Default Rate (%) and loan counts in each cell.
    Highlights high-risk intersection (DTI > 25% and Card Usage > 65% at 28% default rate).
    """
    print("[TASK] Generating Figure 2: Multi-Variable Risk Grid Heatmap...")
    csv_path = Path("data/exports/segment_risk_grid.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing data source: {csv_path}")

    df = pd.read_csv(csv_path)

    # Concise display labels for brackets so text never touches
    dti_display_labels = [
        "Low (<=15%)",
        "Moderate (15-25%)",
        "High (25-35%)",
        "Severe (>35%)",
    ]
    util_display_labels = [
        "Low (<=40%)",
        "Moderate (41-65%)",
        "High (66-85%)",
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

    fig, ax = plt.subplots(figsize=(9.8, 7.8), dpi=300)

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

    # Headline and subtitle in plain English
    plt.suptitle(
        "High Monthly Debt (>25%) and High Card Usage (>65%) Double Default Rates to 28%",
        fontsize=13.5,
        fontweight="bold",
        fontfamily="Georgia",
        color=COLOR_INK_BLACK,
        x=0.08,
        y=0.97,
        ha="left",
    )
    ax.set_title(
        "Default rate (%) and loan count across 4x4 borrower debt and credit card usage grid (1.35M completed loans)",
        fontsize=9.8,
        fontfamily="DejaVu Sans",
        color=COLOR_INK_MUTED,
        pad=14,
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
                f"{round(val):.0f}%",
                ha="center",
                va="center",
                color=text_color,
                fontsize=12.0,
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

    # High-risk annotation banner placed cleanly above the quadrant
    ax.annotate(
        "High-Stress Group (DTI > 25% & Card Usage > 65%):\n112K Total Loans at 28% Default | 47,705 Subprime Loans at 39% Default",
        xy=(2.5, 1.5),
        xytext=(2.5, -0.80),
        ha="center",
        va="center",
        fontsize=8.0,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.35", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.0),
        arrowprops=dict(arrowstyle="->", color=COLOR_INK_BLACK, lw=1.2),
        zorder=12,
    )

    # Benchmark callout on top left cell (clean whole-number percentage)
    ax.annotate(
        "Low-Risk Baseline: 14% Default",
        xy=(0.0, 0.40),
        xytext=(0.0, 0.40),
        ha="center",
        va="center",
        fontsize=8.0,
        fontweight="bold",
        color=COLOR_INK_BLACK,
        bbox=dict(boxstyle="square,pad=0.25", facecolor=COLOR_BG_CARD, edgecolor=COLOR_INK_BLACK, linewidth=1.0),
        zorder=11,
    )

    ax.set_xticks(np.arange(ncols))
    ax.set_yticks(np.arange(nrows))
    ax.set_xticklabels(util_display_labels, fontsize=9.2, fontweight="bold")
    ax.set_yticklabels(dti_display_labels, fontsize=10.0, fontweight="bold")
    ax.tick_params(axis="x", pad=6)
    ax.set_ylim(3.5, -1.15)

    ax.set_xlabel("Credit Card Usage (Revolving Line Utilization)", fontsize=10.5, fontweight="bold", labelpad=8)
    ax.set_ylabel("Monthly Debt Ratio (DTI Bracket)", fontsize=10.5, fontweight="bold", labelpad=8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)

    cbar = plt.colorbar(cax, ax=ax, fraction=0.035, pad=0.04)
    cbar.set_label("Completed Default Rate (%)", fontsize=9.5, fontweight="bold", labelpad=8, color=COLOR_INK_BLACK)
    cbar.outline.set_edgecolor(COLOR_INK_BLACK)
    cbar.outline.set_linewidth(1.0)
    cbar.ax.tick_params(color=COLOR_INK_BLACK, labelcolor=COLOR_INK_BLACK)

    # Bottom Strip (Plain English)
    fig.text(
        0.08,
        0.025,
        "Borrowers with both high monthly debt payments and maxed-out credit cards default twice as often as low-risk borrowers (28% vs. 14%).",
        fontsize=8.8,
        fontfamily="DejaVu Sans",
        fontstyle="italic",
        color=COLOR_INK_MUTED,
        ha="left",
    )

    plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.93])
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
    Badge: 96% of Lending Volume Kept ($18.6B Preserved)
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
    gross_saved = sim["gross_charge_off_dollars_eliminated"] / 1e6       # $254.10M

    fig, ax = plt.subplots(figsize=(9.8, 7.6), dpi=300)

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

    # Headline and subtitle in plain workplace English
    plt.suptitle(
        "Automated Decline Rules Save $230.0M in Unpaid Losses While Keeping 96% of Volume",
        fontsize=13.5,
        fontweight="bold",
        fontfamily="Georgia",
        color=COLOR_INK_BLACK,
        x=0.08,
        y=0.97,
        ha="left",
    )
    ax.set_title(
        "Impact of Phase 1 decline rule (blocking Grades D-G with DTI > 25% and Card Usage > 65%) on subprime write-offs",
        fontsize=9.8,
        fontfamily="DejaVu Sans",
        color=COLOR_INK_MUTED,
        pad=12,
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
        "Current Losses\n(336K loans)",
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
        "Preserved Book\n(-16% write-offs)",
        xy=(x[2], post_policy_losses / 2),
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#FFFFFF",
        zorder=4,
    )

    # Bordered callout note matching exact specification with zero LaTeX collisions
    card_x = 1.18
    card_y = 1800
    badge_text = (
        "96% of Lending Volume Kept ($18.6B Preserved)\n"
        f"- Defaults Prevented: {defaults_eliminated:,} bad loans stopped\n"
        f"- Net Losses Saved: ${hard_stop_savings:,.1f}M (${gross_saved:,.1f}M gross)\n"
        "- Loans Declined: Only 3.6% of book (47,705 loans)\n"
        "- Portfolio Net Return: Lifted from +4.3% to +4.4%"
    )

    ax.annotate(
        badge_text,
        xy=(card_x, card_y),
        xytext=(0, 0),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=8.3,
        fontweight="bold",
        linespacing=1.45,
        color=COLOR_INK_BLACK,
        parse_math=False,
        bbox=dict(
            boxstyle="square,pad=0.5",
            facecolor=COLOR_BG_CARD,
            edgecolor=COLOR_INK_BLACK,
            linewidth=1.0,
        ),
        zorder=5,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Unpaid Net Losses ($ Millions)", fontsize=10.5, fontweight="bold", labelpad=8)
    ax.set_ylim(0, 1860)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_INK_BLACK)
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["bottom"].set_color(COLOR_INK_BLACK)
    ax.spines["bottom"].set_linewidth(1.0)
    ax.grid(False)

    # Bottom Strip (Plain English)
    fig.text(
        0.08,
        0.025,
        "Subprime unpaid write-offs drop by 16% (from $1,404.1M to $1,174.1M) while keeping 96% of total lending volume ($18.6B).",
        fontsize=8.8,
        fontfamily="DejaVu Sans",
        fontstyle="italic",
        color=COLOR_INK_MUTED,
        ha="left",
    )

    plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.93])
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

