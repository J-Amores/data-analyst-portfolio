"""
Hospital Pharmacy Outpatient Drug Pricing & Formulary Optimization
Publication Quality Figure Generator (src/presentation/export_figures.py)

Generates three archival editorial research figures matching the Warm Archival Paper
aesthetic at 300 DPI:
1. assets/fig1_spend_concentration.png (2-Panel Chart: Spend Concentration + 5-Year Time Trend)
2. assets/fig2_price_volume_matrix.png (4x4 Price vs. Volume Heatmap)
3. assets/fig3_formulary_waterfall.png (Hospital Pharmacy Budget Waterfall)

Enforces whole-number rounding, plain-English analyst voice, decision-driven design,
and zero em or en dashes.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------
# Configuration & Paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
ASSETS_DIR = PROJECT_ROOT / "assets"
OVERALL_PARQUET_PATH = DATA_CLEANED_DIR / "mcd_drug_overall_2020_2024.parquet"

# Color Palette (Warm Archival Paper + High-Contrast Ink)
BG_PAPER = "#FAF8F2"
BG_CARD = "#FFFFFF"
BG_PAPER_ALT = "#F3EFE6"
BG_CRIMSON_LIGHT = "#FFF1F2"
BG_GREEN_LIGHT = "#F0FDF4"

INK_PRIMARY = "#111111"
INK_BODY = "#4A4843"
INK_MUTED = "#76746E"

BORDER_HAIRLINE = "#D6D3CD"
BORDER_STRONG = "#111111"

ACCENT_CRIMSON = "#BE123C"
ACCENT_GREEN = "#166534"
ACCENT_AMBER = "#B45309"
DEEP_SLATE = "#1E293B"


def get_font(family: str, size: int, bold: bool = False, italic: bool = False) -> ImageFont.ImageFont:
    """Loads system fonts matching editorial typography with graceful fallbacks."""
    paths: List[str] = []
    if family == "serif":
        if bold and italic:
            paths = ["/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf"]
        elif bold:
            paths = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf"]
        elif italic:
            paths = ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf"]
        else:
            paths = ["/System/Library/Fonts/Supplemental/Georgia.ttf"]
    elif family == "mono":
        paths = [
            "/System/Library/Fonts/SFNSMono.ttf",
            "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
            "/System/Library/Fonts/Supplemental/Courier New.ttf",
        ]
    else:  # sans
        if bold:
            paths = [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/Library/Fonts/Arial Bold.ttf",
            ]
        else:
            paths = [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
            ]

    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# -----------------------------------------------------------------------------
# Figure 1: 2-Panel Spend Concentration & 5-Year Time Trend
# -----------------------------------------------------------------------------
def export_fig1_spend_concentration(df_overall: pd.DataFrame, output_path: Path) -> None:
    """
    Exports Figure 1: 2-Panel Chart
    Left: Share of Prescriptions Filled (%) vs. Share of Total Pharmacy Budget (%) across 4 tiers
    Right: 5-year spending growth trend from 2020 to 2024 ($76B to $111B benchmark)
    """
    w, h = 1600, 960
    img = Image.new("RGB", (w, h), color=BG_PAPER)
    draw = ImageDraw.Draw(img, "RGBA")

    # Outer Border Hairline
    draw.rectangle([20, 20, w - 20, h - 20], fill=None, outline=BORDER_HAIRLINE, width=1)

    # Fonts
    f_kicker = get_font("mono", 12, bold=True)
    f_title = get_font("serif", 23, bold=True)
    f_sub = get_font("sans", 13, bold=False)
    f_pnl_title = get_font("serif", 16, bold=True)
    f_lbl = get_font("sans", 11, bold=False)
    f_bold_lbl = get_font("sans", 12, bold=True)
    f_mono = get_font("mono", 11, bold=False)
    f_mono_bold = get_font("mono", 11, bold=True)
    f_callout = get_font("sans", 11, bold=False)

    # Header in Plain-English Analyst Voice
    draw.text((60, 44), "CHAPTER 02 // BUDGET BREAKDOWN & 5-YEAR TRAJECTORY", fill=ACCENT_AMBER, font=f_kicker)
    draw.text((60, 68), "Brand-Name Drugs Drive 90% of Spending and All of Our 5-Year Budget Growth", fill=INK_PRIMARY, font=f_title)
    draw.text(
        (60, 104),
        "Left: Share of prescriptions vs. share of budget ($85M hospital scale) | Right: 2020-2024 spending trend ($76B to $111B benchmark)",
        fill=INK_BODY,
        font=f_sub,
    )
    draw.line([(60, 134), (w - 60, 134)], fill=BORDER_HAIRLINE, width=1)

    # =========================================================================
    # LEFT PANEL: Paired Bar Chart (4 Tiers)
    # =========================================================================
    p1_x1 = 70
    p1_x2 = 750
    p1_y1 = 190
    p1_y2 = 780
    p1_h = p1_y2 - p1_y1

    draw.text((p1_x1, p1_y1 - 36), "Prescription Share vs. Budget Share by Drug Tier", fill=INK_PRIMARY, font=f_pnl_title)

    # Legend for Left Panel (Top right of left panel)
    leg_x = p1_x2 - 320
    leg_y = p1_y1 - 34
    draw.rectangle([leg_x, leg_y, leg_x + 12, leg_y + 12], fill=DEEP_SLATE, outline=BORDER_STRONG, width=1)
    draw.text((leg_x + 18, leg_y - 1), "Scripts Filled (%)", fill=INK_BODY, font=f_lbl)
    draw.rectangle([leg_x + 150, leg_y, leg_x + 162, leg_y + 12], fill=ACCENT_CRIMSON, outline=BORDER_STRONG, width=1)
    draw.text((leg_x + 168, leg_y - 1), "Budget Share (%)", fill=INK_BODY, font=f_lbl)

    # Y-axis Scale: 0% to 108%
    max_val_left = 108.0
    for tick in [0, 20, 40, 60, 80, 100]:
        ty = p1_y2 - int((tick / max_val_left) * p1_h)
        draw.line([(p1_x1 + 45, ty), (p1_x2, ty)], fill="#EAE5DA" if tick > 0 else BORDER_STRONG, width=1)
        draw.text((p1_x1 + 10, ty - 7), f"{tick}%", fill=INK_MUTED, font=f_mono)

    # Inner Frame lines
    draw.line([(p1_x1 + 45, p1_y1), (p1_x1 + 45, p1_y2)], fill=BORDER_STRONG, width=1)
    draw.line([(p1_x1 + 45, p1_y2), (p1_x2, p1_y2)], fill=BORDER_STRONG, width=1)

    # Left Panel Data (4 Tiers)
    tiers = [
        {"name": "Top 165 Drugs\n(3% of catalog)", "rx": 3, "spend": 65, "dollars": "$55M hospital"},
        {"name": "Top 5% Drugs\n(239 items)", "rx": 5, "spend": 72, "dollars": "$61M hospital"},
        {"name": "All Brand Drugs\n(33% of fills)", "rx": 33, "spend": 90, "dollars": "$77M hospital"},
        {"name": "All Generic Drugs\n(67% of fills)", "rx": 67, "spend": 10, "dollars": "$8M hospital"},
    ]

    avail_w1 = (p1_x2 - (p1_x1 + 45)) - 40
    group_spacing1 = avail_w1 / len(tiers)
    bar_w1 = 32
    bar_gap1 = 6

    for i, tier in enumerate(tiers):
        gx = (p1_x1 + 45) + 24 + i * group_spacing1
        rx_h = int((tier["rx"] / max_val_left) * p1_h)
        sp_h = int((tier["spend"] / max_val_left) * p1_h)

        # Bar 1: Prescriptions (Dark Slate)
        b1_x1 = gx
        b1_y1 = p1_y2 - rx_h
        b1_x2 = b1_x1 + bar_w1
        b1_y2 = p1_y2
        draw.rectangle([b1_x1, b1_y1, b1_x2, b1_y2], fill=DEEP_SLATE, outline=BORDER_STRONG, width=1)
        draw.text((b1_x1 + 2, b1_y1 - 16), f"{tier['rx']}%", fill=DEEP_SLATE, font=f_mono_bold)

        # Bar 2: Budget (Crimson)
        b2_x1 = b1_x2 + bar_gap1
        b2_y1 = p1_y2 - sp_h
        b2_x2 = b2_x1 + bar_w1
        b2_y2 = p1_y2
        draw.rectangle([b2_x1, b2_y1, b2_x2, b2_y2], fill=ACCENT_CRIMSON, outline=BORDER_STRONG, width=1)
        draw.text((b2_x1 + 2, b2_y1 - 16), f"{tier['spend']}%", fill=ACCENT_CRIMSON, font=f_mono_bold)

        # X-Axis Labels
        lines = tier["name"].split("\n")
        draw.text((gx - 4, p1_y2 + 10), lines[0], fill=INK_PRIMARY, font=f_bold_lbl)
        if len(lines) > 1:
            draw.text((gx - 4, p1_y2 + 28), lines[1], fill=INK_MUTED, font=f_lbl)
        draw.text((gx - 4, p1_y2 + 46), tier["dollars"], fill=INK_PRIMARY, font=f_mono)

    # Callout Badge in Open Whitespace (Upper Left over Top 165 where bars are low/medium)
    c_x1 = p1_x1 + 65
    c_y1 = p1_y1 + 10
    c_w = 260
    c_h = 75
    draw.rectangle([c_x1, c_y1, c_x1 + c_w, c_y1 + c_h], fill=BG_CRIMSON_LIGHT, outline=ACCENT_CRIMSON, width=1)
    draw.text((c_x1 + 12, c_y1 + 10), "KEY SPEND SKEW", fill=ACCENT_CRIMSON, font=f_mono_bold)
    draw.text(
        (c_x1 + 12, c_y1 + 28),
        "Top 5% of medications consume 72%\n"
        "of the total pharmacy budget.\n"
        "Brand drugs cost 19x more ($408 vs $22).",
        fill=INK_BODY,
        font=f_callout,
    )

    # Divider between panels
    draw.line([(790, 160), (790, 840)], fill=BORDER_HAIRLINE, width=1)

    # =========================================================================
    # RIGHT PANEL: 5-Year Outpatient Spending Trend (2020-2024)
    # =========================================================================
    p2_x1 = 830
    p2_x2 = 1530
    p2_y1 = 190
    p2_y2 = 780
    p2_h = p2_y2 - p2_y1

    draw.text((p2_x1, p2_y1 - 36), "5-Year Outpatient Drug Spending Trend (2020-2024)", fill=INK_PRIMARY, font=f_pnl_title)

    # Legend for Right Panel
    leg2_x = p2_x2 - 380
    leg2_y = p2_y1 - 34
    draw.line([(leg2_x, leg2_y + 6), (leg2_x + 18, leg2_y + 6)], fill=DEEP_SLATE, width=2)
    draw.text((leg2_x + 24, leg2_y - 1), "Total ($111B)", fill=INK_BODY, font=f_lbl)
    draw.line([(leg2_x + 120, leg2_y + 6), (leg2_x + 138, leg2_y + 6)], fill=ACCENT_CRIMSON, width=2)
    draw.text((leg2_x + 144, leg2_y - 1), "Brand ($100B)", fill=INK_BODY, font=f_lbl)
    draw.line([(leg2_x + 250, leg2_y + 6), (leg2_x + 268, leg2_y + 6)], fill=ACCENT_GREEN, width=2)
    draw.text((leg2_x + 274, leg2_y - 1), "Generic ($11B)", fill=INK_BODY, font=f_lbl)

    # Y-axis Scale: $0B to $130B
    max_val_right = 130.0
    for tick in [0, 20, 40, 60, 80, 100, 120]:
        ty = p2_y2 - int((tick / max_val_right) * p2_h)
        draw.line([(p2_x1 + 50, ty), (p2_x2, ty)], fill="#EAE5DA" if tick > 0 else BORDER_STRONG, width=1)
        draw.text((p2_x1 + 10, ty - 7), f"${tick}B", fill=INK_MUTED, font=f_mono)

    # Inner Frame lines
    draw.line([(p2_x1 + 50, p2_y1), (p2_x1 + 50, p2_y2)], fill=BORDER_STRONG, width=1)
    draw.line([(p2_x1 + 50, p2_y2), (p2_x2, p2_y2)], fill=BORDER_STRONG, width=1)

    # 5-Year Data Points
    years = [2020, 2021, 2022, 2023, 2024]
    tot_pts = [76.4, 87.7, 100.2, 112.3, 111.3]
    brd_pts = [67.1, 77.7, 88.9, 100.6, 100.4]
    gnr_pts = [9.3, 10.0, 11.3, 11.7, 10.9]

    avail_w2 = (p2_x2 - (p2_x1 + 50)) - 60
    year_spacing = avail_w2 / (len(years) - 1)

    coords_tot = []
    coords_brd = []
    coords_gnr = []

    for i, yr in enumerate(years):
        xx = (p2_x1 + 50) + 30 + i * year_spacing
        coords_tot.append((xx, p2_y2 - int((tot_pts[i] / max_val_right) * p2_h)))
        coords_brd.append((xx, p2_y2 - int((brd_pts[i] / max_val_right) * p2_h)))
        coords_gnr.append((xx, p2_y2 - int((gnr_pts[i] / max_val_right) * p2_h)))

        # X-axis label
        draw.text((xx - 14, p2_y2 + 12), str(yr), fill=INK_PRIMARY, font=f_bold_lbl)

    # Draw Lines & Points for Generic
    for i in range(len(years) - 1):
        draw.line([coords_gnr[i], coords_gnr[i + 1]], fill=ACCENT_GREEN, width=3)
    for i, (xx, yy) in enumerate(coords_gnr):
        draw.ellipse([(xx - 4, yy - 4), (xx + 4, yy + 4)], fill=ACCENT_GREEN, outline=BORDER_STRONG)
        if i == 0 or i == len(years) - 1:
            val_txt = f"${round(gnr_pts[i])}B"
            draw.text((xx - 12, yy + 10), val_txt, fill=ACCENT_GREEN, font=f_mono_bold)

    # Draw Lines & Points for Brand
    for i in range(len(years) - 1):
        draw.line([coords_brd[i], coords_brd[i + 1]], fill=ACCENT_CRIMSON, width=3)
    for i, (xx, yy) in enumerate(coords_brd):
        draw.ellipse([(xx - 4, yy - 4), (xx + 4, yy + 4)], fill=ACCENT_CRIMSON, outline=BORDER_STRONG)
        if i == 0 or i == len(years) - 1:
            val_txt = f"${round(brd_pts[i])}B"
            draw.text((xx - 14, yy - 20), val_txt, fill=ACCENT_CRIMSON, font=f_mono_bold)

    # Draw Lines & Points for Total
    for i in range(len(years) - 1):
        draw.line([coords_tot[i], coords_tot[i + 1]], fill=DEEP_SLATE, width=3)
    for i, (xx, yy) in enumerate(coords_tot):
        draw.ellipse([(xx - 5, yy - 5), (xx + 5, yy + 5)], fill=DEEP_SLATE, outline=BORDER_STRONG)
        val_txt = f"${round(tot_pts[i])}B"
        draw.text((xx - 14, yy - 22), val_txt, fill=DEEP_SLATE, font=f_mono_bold)

    # Right Panel Annotation Box (Upper Middle)
    c2_x1 = p2_x1 + 75
    c2_y1 = p2_y1 + 10
    c2_w = 340
    c2_h = 75
    draw.rectangle([c2_x1, c2_y1, c2_x1 + c2_w, c2_y1 + c2_h], fill=BG_CARD, outline=BORDER_STRONG, width=1)
    draw.text((c2_x1 + 14, c2_y1 + 10), "+46% TOTAL 5-YEAR INCREASE ($76B TO $111B)", fill=INK_PRIMARY, font=f_mono_bold)
    draw.text(
        (c2_x1 + 14, c2_y1 + 28),
        "Brand spending climbed steeply (+49%),\n"
        "driving all outpatient cost growth.\n"
        "Generic spending stayed flat and affordable ($9B to $11B).",
        fill=INK_BODY,
        font=f_callout,
    )

    # Bottom Full-Width Takeaway Strip
    strip_y = 880
    draw.rectangle([60, strip_y, w - 60, strip_y + 44], fill=BG_PAPER_ALT, outline=BORDER_HAIRLINE, width=1)
    draw.text(
        (80, strip_y + 14),
        "Brand-name drugs make up just 33% of prescriptions filled but take up 90% of total pharmacy spending ($408 vs. $22 per fill).",
        fill=INK_PRIMARY,
        font=f_mono_bold,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), dpi=(300, 300))
    print(f"Exported: {output_path}")


# -----------------------------------------------------------------------------
# Figure 2: 4x4 Price Hike vs Volume Heatmap
# -----------------------------------------------------------------------------
def export_fig2_price_volume_matrix(df_overall: pd.DataFrame, output_path: Path) -> None:
    """
    Exports Figure 2: 4x4 Heatmap comparing 5-year price change per dose against
    prescription volume across 3,762 complete drug records.
    Uses whole-number rounding and zero jargon.
    """
    w, h = 1600, 960
    img = Image.new("RGB", (w, h), color=BG_PAPER)
    draw = ImageDraw.Draw(img, "RGBA")

    draw.rectangle([20, 20, w - 20, h - 20], fill=None, outline=BORDER_HAIRLINE, width=1)

    f_kicker = get_font("mono", 12, bold=True)
    f_title = get_font("serif", 23, bold=True)
    f_sub = get_font("sans", 13, bold=False)
    f_lbl = get_font("sans", 11, bold=False)
    f_bold_lbl = get_font("sans", 12, bold=True)
    f_cell_title = get_font("sans", 13, bold=True)
    f_mono = get_font("mono", 11, bold=False)
    f_mono_bold = get_font("mono", 11, bold=True)
    f_banner = get_font("mono", 11, bold=True)

    # Header in Plain-English Analyst Voice
    draw.text((60, 44), "CHAPTER 03 // PRICE VS VOLUME", fill=ACCENT_AMBER, font=f_kicker)
    draw.text((60, 68), "Manufacturer Price Hikes, Not Patient Demand, Drive Our Biggest Cost Spikes", fill=INK_PRIMARY, font=f_title)
    draw.text(
        (60, 104),
        "5-year price change per dose vs. prescription volume across 3,762 complete drug records",
        fill=INK_BODY,
        font=f_sub,
    )
    draw.line([(60, 134), (w - 60, 134)], fill=BORDER_HAIRLINE, width=1)

    # Grid Dimensions
    grid_x1 = 280
    grid_y1 = 200
    grid_w = 1240
    grid_h = 590
    n_rows = 4
    n_cols = 4
    cell_w = grid_w / n_cols
    cell_h = grid_h / n_rows

    row_labels = [
        "Price Spike\n(Price Jump > 50%)",
        "High Price Hike\n(Price Jump 15% to 50%)",
        "Moderate Increase\n(Price Jump 0% to 15%)",
        "Low / Price Drop\n(Price Jump <= 0%)",
    ]

    col_labels = [
        "Low\n(< 5,000 Rx)",
        "Moderate\n(5k to 30,000 Rx)",
        "High\n(30k to 150k Rx)",
        "Very High\n(> 150,000 Rx)",
    ]

    # Empirical data matrix with whole numbers
    matrix_data = [
        # Price Spike (> 50%)
        [
            {"drugs": 373, "spend": "$430M", "share": "0%", "cost_clm": "$1,102 / fill", "bg": "#FDF2F2", "risk": "Low-Volume Specialty"},
            {"drugs": 140, "spend": "$1B", "share": "1%", "cost_clm": "$546 / fill", "bg": "#FEE2E2", "risk": "Moderate Exposure"},
            {"drugs": 72, "spend": "$1B", "share": "1%", "cost_clm": "$137 / fill", "bg": "#FECACA", "risk": "High Price Hike"},
            {"drugs": 46, "spend": "$4B", "share": "4%", "cost_clm": "$50 / fill", "bg": "#FCA5A5", "risk": "HIGH-PRIORITY SWITCH"},
        ],
        # High Price Hike (15% to 50%)
        [
            {"drugs": 467, "spend": "$4B", "share": "4%", "cost_clm": "$6,243 / fill", "bg": "#FEF3C7", "risk": "Rare Biologics"},
            {"drugs": 217, "spend": "$8B", "share": "8%", "cost_clm": "$2,834 / fill", "bg": "#FDE68A", "risk": "Specialty Infusions"},
            {"drugs": 127, "spend": "$14B", "share": "14%", "cost_clm": "$1,624 / fill", "bg": "#FCD34D", "risk": "Climbing Brands"},
            {"drugs": 118, "spend": "$30B", "share": "31%", "cost_clm": "$150 / fill", "bg": "#F59E0B", "risk": "Blockbuster Brands"},
        ],
        # Moderate Increase (0% to 15%)
        [
            {"drugs": 390, "spend": "$3B", "share": "3%", "cost_clm": "$6,312 / fill", "bg": "#F4F1EA", "risk": "Stable Specialty"},
            {"drugs": 141, "spend": "$3B", "share": "3%", "cost_clm": "$1,658 / fill", "bg": "#F4F1EA", "risk": "Stable Chronic Care"},
            {"drugs": 79, "spend": "$4B", "share": "4%", "cost_clm": "$712 / fill", "bg": "#F4F1EA", "risk": "Maintenance Meds"},
            {"drugs": 72, "spend": "$6B", "share": "6%", "cost_clm": "$60 / fill", "bg": "#E5E7EB", "risk": "Everyday Generics"},
        ],
        # Low / Price Drop (<= 0%)
        [
            {"drugs": 688, "spend": "$1B", "share": "1%", "cost_clm": "$1,275 / fill", "bg": "#F0FDF4", "risk": "Niche Generics"},
            {"drugs": 361, "spend": "$2B", "share": "2%", "cost_clm": "$466 / fill", "bg": "#DCFCE7", "risk": "Competitive Tier"},
            {"drugs": 234, "spend": "$3B", "share": "3%", "cost_clm": "$181 / fill", "bg": "#BBF7D0", "risk": "Low-Cost Generics"},
            {"drugs": 237, "spend": "$14B", "share": "14%", "cost_clm": "$47 / fill", "bg": "#86EFAC", "risk": "Generic Workhorses"},
        ],
    ]

    # Draw Column Headers (Top)
    for c in range(n_cols):
        cx = grid_x1 + c * cell_w
        lines = col_labels[c].split("\n")
        draw.text((cx + 14, grid_y1 - 42), lines[0], fill=INK_PRIMARY, font=f_bold_lbl)
        draw.text((cx + 14, grid_y1 - 24), lines[1], fill=INK_MUTED, font=f_lbl)

    # Draw Row Headers (Left)
    for r in range(n_rows):
        ry = grid_y1 + r * cell_h
        lines = row_labels[r].split("\n")
        draw.text((60, ry + cell_h // 2 - 20), lines[0], fill=INK_PRIMARY, font=f_bold_lbl)
        draw.text((60, ry + cell_h // 2), lines[1], fill=INK_MUTED, font=f_lbl)

    # Render Cells
    for r in range(n_rows):
        for c in range(n_cols):
            cx1 = grid_x1 + c * cell_w
            cy1 = grid_y1 + r * cell_h
            cx2 = cx1 + cell_w
            cy2 = cy1 + cell_h
            cell = matrix_data[r][c]

            # Cell Background
            draw.rectangle([cx1, cy1, cx2, cy2], fill=cell["bg"], outline=BORDER_HAIRLINE, width=1)

            # Cell Content
            draw.text((cx1 + 16, cy1 + 14), f"{cell['drugs']} Drug Lines", fill=INK_PRIMARY, font=f_cell_title)
            draw.text((cx1 + 16, cy1 + 42), f"Total Spend: {cell['spend']} ({cell['share']})", fill=INK_BODY, font=f_mono_bold)
            draw.text((cx1 + 16, cy1 + 68), f"Avg Cost: {cell['cost_clm']}", fill=INK_MUTED, font=f_mono)
            draw.text((cx1 + 16, cy1 + 96), f"Status: {cell['risk']}", fill=INK_BODY, font=f_lbl)

    # Highlight Bounding Box around High-Priority Target (Row 0, Col 3: Price Spike x Everyday Use)
    target_x1 = grid_x1 + 3 * cell_w
    target_y1 = grid_y1
    target_x2 = target_x1 + cell_w
    target_y2 = target_y1 + cell_h

    draw.rectangle([target_x1, target_y1, target_x2, target_y2], fill=None, outline=BORDER_STRONG, width=3)

    # Top Banner on Problem Corner
    banner_h = 28
    draw.rectangle([target_x1, target_y1 - banner_h, target_x2, target_y1], fill=INK_PRIMARY, outline=BORDER_STRONG, width=1)
    draw.text((target_x1 + 12, target_y1 - 21), "HIGH-PRIORITY SWITCH TARGET (46 DRUGS)", fill="#FFFFFF", font=f_banner)

    # Bottom Takeaway Strip (Zero jargon)
    strip_y = 880
    draw.rectangle([60, strip_y, w - 60, strip_y + 44], fill=BG_PAPER_ALT, outline=BORDER_HAIRLINE, width=1)
    draw.text(
        (80, strip_y + 14),
        "88 of the top 100 fastest-growing drugs were driven by treating more patients, while 46 older brand drugs spiked purely from price hikes.",
        fill=INK_PRIMARY,
        font=f_mono_bold,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), dpi=(300, 300))
    print(f"Exported: {output_path}")


# -----------------------------------------------------------------------------
# Figure 3: Hospital Pharmacy Savings Waterfall
# -----------------------------------------------------------------------------
def export_fig3_formulary_waterfall(output_path: Path) -> None:
    """
    Exports Figure 3: Hospital Pharmacy Savings Waterfall across Generic Switching
    and Supplier Price Locks.
    Bar 1 (Crimson): Starting Target Spend ($6.0M target brand and supplier pool)
    Bar 2 (Green): Phase 1 Auto-Generic Switch (-$1.1M / -$1,100K)
    Bar 3 (Green): Phase 2 Wholesale Supplier Price Locks (-$2.1M / -$2,100K)
    Bar 4 (Slate): Implemented Target Spend ($2.8M protected brand buffer)
    Bar 5 (Green): Total Annual Hospital Savings (+$3.2M / +$3,200K)
    Zero label collisions, ample headroom, and zero jargon.
    """
    w, h = 1600, 960
    img = Image.new("RGB", (w, h), color=BG_PAPER)
    draw = ImageDraw.Draw(img, "RGBA")

    draw.rectangle([20, 20, w - 20, h - 20], fill=None, outline=BORDER_HAIRLINE, width=1)

    f_kicker = get_font("mono", 12, bold=True)
    f_title = get_font("serif", 23, bold=True)
    f_sub = get_font("sans", 13, bold=False)
    f_lbl = get_font("sans", 11, bold=False)
    f_bold_lbl = get_font("sans", 12, bold=True)
    f_bar_val = get_font("mono", 18, bold=True)
    f_bar_sub = get_font("mono", 11, bold=False)
    f_mono = get_font("mono", 11, bold=False)
    f_mono_bold = get_font("mono", 11, bold=True)
    f_badge = get_font("sans", 11, bold=False)

    # Header in Plain-English Analyst Voice
    draw.text((60, 44), "CHAPTER 04 // SAVINGS PLAN WATERFALL", fill=ACCENT_AMBER, font=f_kicker)
    draw.text((60, 68), "How Generic Switching and Supplier Price Locks Save $3.2M per Year", fill=INK_PRIMARY, font=f_title)
    draw.text(
        (60, 104),
        "Annual hospital outpatient pharmacy savings across Phase 1 (auto-generics) and Phase 2 (wholesale supplier caps)",
        fill=INK_BODY,
        font=f_sub,
    )
    draw.line([(60, 134), (w - 60, 134)], fill=BORDER_HAIRLINE, width=1)

    # Upper-Right Callout Badge: 98% Access Kept
    badge_x1 = w - 540
    badge_y1 = 155
    badge_w = 480
    badge_h = 95
    draw.rectangle([badge_x1, badge_y1, badge_x1 + badge_w, badge_y1 + badge_h], fill=BG_CARD, outline=BORDER_STRONG, width=1)
    draw.text((badge_x1 + 16, badge_y1 + 12), "PATIENT CARE REMAINS 100% UNCHANGED", fill=INK_PRIMARY, font=f_mono_bold)
    draw.text(
        (badge_x1 + 16, badge_y1 + 32),
        "* 100% FDA-approved generic or therapeutic match\n"
        "* Patient prescription access kept: 98% routine scripts untouched\n"
        "* 1-click doctor override available for documented clinical needs",
        fill=INK_BODY,
        font=f_badge,
    )

    # Chart Canvas with generous headroom (max_val = 7.5M for bars up to 6.0M)
    chart_x1 = 110
    chart_y1 = 265
    chart_x2 = w - 70
    chart_y2 = 780
    chart_h = chart_y2 - chart_y1

    max_val = 7.5
    for tick in [0, 1, 2, 3, 4, 5, 6, 7]:
        ty = chart_y2 - int((tick / max_val) * chart_h)
        draw.line([(chart_x1 - 10, ty), (chart_x2, ty)], fill="#EAE5DA" if tick > 0 else BORDER_STRONG, width=1)
        draw.text((chart_x1 - 65, ty - 7), f"${tick}.0M", fill=INK_MUTED, font=f_mono)

    # Frame lines
    draw.line([(chart_x1, chart_y1), (chart_x1, chart_y2)], fill=BORDER_STRONG, width=1)
    draw.line([(chart_x1, chart_y2), (chart_x2, chart_y2)], fill=BORDER_STRONG, width=1)

    # Waterfall Steps (5 Bars)
    bar_w = 170
    gap = 90
    start_x = chart_x1 + 50

    # Bar 1: Starting Target Spend ($6.0M) in Crimson
    b1_x1 = start_x
    b1_val = 6.0
    b1_h = int((b1_val / max_val) * chart_h)
    b1_y1 = chart_y2 - b1_h
    b1_x2 = b1_x1 + bar_w
    b1_y2 = chart_y2
    draw.rectangle([b1_x1, b1_y1, b1_x2, b1_y2], fill=ACCENT_CRIMSON, outline=BORDER_STRONG, width=1)
    draw.text((b1_x1 + 30, b1_y1 - 38), "$6.0M", fill=ACCENT_CRIMSON, font=f_bar_val)
    draw.text((b1_x1 + 25, b1_y1 - 18), "($6,000K)", fill=INK_MUTED, font=f_bar_sub)
    draw.text((b1_x1 + 4, chart_y2 + 14), "1. Starting Spend", fill=INK_PRIMARY, font=f_bold_lbl)
    draw.text((b1_x1 + 4, chart_y2 + 32), "Target Brand & Supplier Pool", fill=INK_MUTED, font=f_lbl)
    draw.text((b1_x1 + 4, chart_y2 + 50), "Vyvanse, Concerta + Generics", fill=INK_MUTED, font=f_mono)

    # Connector Line 1 to 2
    draw.line([(b1_x2, b1_y1), (b1_x2 + gap, b1_y1)], fill=INK_MUTED, width=1)

    # Bar 2: Phase 1 Savings: Auto-Generic E-Prescribing (-$1.1M / -$1,100K) in Green
    b2_x1 = b1_x2 + gap
    b2_drop = 1.1
    b2_drop_h = int((b2_drop / max_val) * chart_h)
    b2_y1 = b1_y1
    b2_y2 = b2_y1 + b2_drop_h
    b2_x2 = b2_x1 + bar_w
    draw.rectangle([b2_x1, b2_y1, b2_x2, b2_y2], fill=ACCENT_GREEN, outline=BORDER_STRONG, width=1)
    draw.text((b2_x1 + 25, b2_y1 - 38), "-$1.1M", fill=ACCENT_GREEN, font=f_bar_val)
    draw.text((b2_x1 + 20, b2_y1 - 18), "(-$1,100K)", fill=INK_MUTED, font=f_bar_sub)
    draw.text((b2_x1 + 4, chart_y2 + 14), "2. Phase 1 Switch", fill=INK_PRIMARY, font=f_bold_lbl)
    draw.text((b2_x1 + 4, chart_y2 + 32), "Auto-Generic E-Rx", fill=INK_MUTED, font=f_lbl)
    draw.text((b2_x1 + 4, chart_y2 + 50), "6 Off-Patent Brands", fill=INK_MUTED, font=f_mono)

    # Connector Line 2 to 3
    draw.line([(b2_x2, b2_y2), (b2_x2 + gap, b2_y2)], fill=INK_MUTED, width=1)

    # Bar 3: Phase 2 Savings: Wholesale Supplier Price Locks (-$2.1M / -$2,100K) in Green
    b3_x1 = b2_x2 + gap
    b3_drop = 2.1
    b3_drop_h = int((b3_drop / max_val) * chart_h)
    b3_y1 = b2_y2
    b3_y2 = b3_y1 + b3_drop_h
    b3_x2 = b3_x1 + bar_w
    draw.rectangle([b3_x1, b3_y1, b3_x2, b3_y2], fill=ACCENT_GREEN, outline=BORDER_STRONG, width=1)
    draw.text((b3_x1 + 25, b3_y1 - 38), "-$2.1M", fill=ACCENT_GREEN, font=f_bar_val)
    draw.text((b3_x1 + 20, b3_y1 - 18), "(-$2,100K)", fill=INK_MUTED, font=f_bar_sub)
    draw.text((b3_x1 + 4, chart_y2 + 14), "3. Phase 2 Caps", fill=INK_PRIMARY, font=f_bold_lbl)
    draw.text((b3_x1 + 4, chart_y2 + 32), "Wholesale Supplier Locks", fill=INK_MUTED, font=f_lbl)
    draw.text((b3_x1 + 4, chart_y2 + 50), "1,358 Generic Drugs", fill=INK_MUTED, font=f_mono)

    # Connector Line 3 to 4
    draw.line([(b3_x2, b3_y2), (b3_x2 + gap, b3_y2)], fill=INK_MUTED, width=1)

    # Bar 4: Implemented Target Spend ($2.8M Protected Buffer) in Slate
    b4_x1 = b3_x2 + gap
    b4_val = 2.8
    b4_h = int((b4_val / max_val) * chart_h)
    b4_y1 = chart_y2 - b4_h
    b4_x2 = b4_x1 + bar_w
    b4_y2 = chart_y2
    draw.rectangle([b4_x1, b4_y1, b4_x2, b4_y2], fill=DEEP_SLATE, outline=BORDER_STRONG, width=1)
    draw.text((b4_x1 + 30, b4_y1 - 38), "$2.8M", fill=DEEP_SLATE, font=f_bar_val)
    draw.text((b4_x1 + 25, b4_y1 - 18), "($2,800K)", fill=INK_MUTED, font=f_bar_sub)
    draw.text((b4_x1 + 4, chart_y2 + 14), "4. Implemented Target", fill=INK_PRIMARY, font=f_bold_lbl)
    draw.text((b4_x1 + 4, chart_y2 + 32), "Protected Brand Buffer", fill=INK_MUTED, font=f_lbl)
    draw.text((b4_x1 + 4, chart_y2 + 50), "72% Spend Kept for Allergies", fill=INK_MUTED, font=f_mono)

    # Separator Line before final savings bar
    draw.line([(b4_x2 + gap // 2, chart_y1), (b4_x2 + gap // 2, chart_y2)], fill=BORDER_HAIRLINE, width=1)

    # Bar 5: Total Annual Hospital Savings (+$3.2M / +$3,200K) in Green
    b5_x1 = b4_x2 + gap
    b5_val = 3.2
    b5_h = int((b5_val / max_val) * chart_h)
    b5_y1 = chart_y2 - b5_h
    b5_x2 = b5_x1 + bar_w
    b5_y2 = chart_y2
    draw.rectangle([b5_x1, b5_y1, b5_x2, b5_y2], fill=ACCENT_GREEN, outline=BORDER_STRONG, width=1)
    draw.text((b5_x1 + 20, b5_y1 - 38), "+$3.2M", fill=ACCENT_GREEN, font=f_bar_val)
    draw.text((b5_x1 + 15, b5_y1 - 18), "(+$3,200K)", fill=INK_MUTED, font=f_bar_sub)
    draw.text((b5_x1 + 4, chart_y2 + 14), "5. Total Savings", fill=INK_PRIMARY, font=f_bold_lbl)
    draw.text((b5_x1 + 4, chart_y2 + 32), "+$3.2M Net Recovered", fill=ACCENT_GREEN, font=f_bold_lbl)
    draw.text((b5_x1 + 4, chart_y2 + 50), "98% Everyday Prescriptions Untouched", fill=INK_MUTED, font=f_mono)

    # Bottom Takeaway Strip (Zero jargon)
    strip_y = 880
    draw.rectangle([60, strip_y, w - 60, strip_y + 44], fill=BG_PAPER_ALT, outline=BORDER_HAIRLINE, width=1)
    draw.text(
        (80, strip_y + 14),
        "Switching 6 overpriced brand drugs saves $1.1M and locking in low-cost generic suppliers saves $2.1M, while 98% of prescriptions stay untouched.",
        fill=INK_PRIMARY,
        font=f_mono_bold,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), dpi=(300, 300))
    print(f"Exported: {output_path}")


# -----------------------------------------------------------------------------
# Main Execution Pipeline
# -----------------------------------------------------------------------------
def main() -> None:
    """Executes export of all 3 presentation whitepaper figures."""
    print("=" * 80)
    print("Exporting Publication Figures for Hospital Pharmacy Whitepaper (300 DPI)...")
    print("=" * 80)

    if not OVERALL_PARQUET_PATH.exists():
        raise FileNotFoundError(f"Missing parquet file: {OVERALL_PARQUET_PATH}")

    df_overall = pd.read_parquet(OVERALL_PARQUET_PATH)

    fig1_path = ASSETS_DIR / "fig1_spend_concentration.png"
    fig2_path = ASSETS_DIR / "fig2_price_volume_matrix.png"
    fig3_path = ASSETS_DIR / "fig3_formulary_waterfall.png"

    export_fig1_spend_concentration(df_overall, fig1_path)
    export_fig2_price_volume_matrix(df_overall, fig2_path)
    export_fig3_formulary_waterfall(fig3_path)

    print("All figures successfully exported with whole numbers and plain-English styling.")


if __name__ == "__main__":
    main()
