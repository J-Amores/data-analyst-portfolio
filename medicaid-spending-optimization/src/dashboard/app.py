"""
Medicaid Outpatient Drug Spend Optimization & Formulary Stewardship Dashboard
=============================================================================
Governing Specifications:
  - docs/PROJECT_CHARTER.md
  - docs/DATA_SPEC.md
  - docs/AGENT_TASKS.md (Phase 4: The DASH Framework)
  - docs/HIRING_MANAGER_CRITIQUE.md

Executive Stakeholders:
  - State Medicaid Pharmacy Director
  - Chief Medical Officer (CMO)
  - Pharmacy & Therapeutics (P&T) Formulary Committee
  - Legislative Budget Analysts

Primary Decisions Supported:
  1. Preferred Drug List (PDL) Brand-to-Generic Tiering & Substitution Mandates.
  2. State Maximum Allowable Cost (MAC) Price Ceiling Updates.
  3. Utilization Prior Authorization & Step-Therapy Protocol Optimization.
"""

from __future__ import annotations

import sys
import io
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Ensure project root is in sys.path regardless of execution working directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Medicaid Drug Spend Optimization | Executive Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def _resolve_data_paths() -> Tuple[Path, Path]:
    """Resolves parquet dataset paths across direct, sub-repo, and portfolio deployments."""
    candidates = [
        PROJECT_ROOT / "data" / "cleaned",
        Path.cwd() / "medicaid-spending-optimization" / "data" / "cleaned",
        Path.cwd() / "data" / "cleaned",
        Path(__file__).resolve().parent.parent / "data" / "cleaned",
    ]
    for candidate in candidates:
        ov = candidate / "mcd_drug_overall_2020_2024.parquet"
        dt = candidate / "mcd_mftr_detail_2020_2024.parquet"
        if ov.exists() and dt.exists():
            return ov, dt
    default_dir = PROJECT_ROOT / "data" / "cleaned"
    return default_dir / "mcd_drug_overall_2020_2024.parquet", default_dir / "mcd_mftr_detail_2020_2024.parquet"

OVERALL_PARQUET_PATH, DETAIL_PARQUET_PATH = _resolve_data_paths()
DATA_DIR = OVERALL_PARQUET_PATH.parent

# Design Tokens: Strict Palette (Slate/Navy with Emerald Accent)
COLOR_NAVY_DARK = "#0F172A"       # Slate 900
COLOR_NAVY_PRIMARY = "#1E293B"    # Slate 800
COLOR_SLATE_MUTED = "#64748B"     # Slate 500
COLOR_SLATE_LIGHT = "#94A3B8"     # Slate 400
COLOR_BORDER = "#E2E8F0"          # Slate 200
COLOR_BG_CARD = "#F8FAFC"         # Slate 50
COLOR_EMERALD = "#059669"         # Emerald 600 (North Star Savings Accent)
COLOR_EMERALD_LIGHT = "#D1FAE5"   # Emerald 100
COLOR_EMERALD_BORDER = "#10B981"  # Emerald 500
COLOR_CRIMSON = "#E11D48"         # Rose 600 (Price Risk Alert)
COLOR_CRIMSON_LIGHT = "#FFE4E6"   # Rose 100
COLOR_BLUE = "#2563EB"            # Blue 600 (Secondary Marker)

# Custom CSS for Executive Polish & Cognitive Ergonomics (Adaptive Light, Dark & System Modes)
st.markdown(
    """
    <style>
        /* Base typography & container sizing (safe top padding for Streamlit toolbar) */
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2.5rem;
            max-width: 98%;
        }
        
        /* -----------------------------------------------------------------
           1. Core Design Tokens: Default Executive Light Theme
           ----------------------------------------------------------------- */
        :root {
            --card-bg: #FFFFFF;
            --card-border: #E2E8F0;
            --card-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px 0 rgba(15, 23, 42, 0.03);
            --card-shadow-hover: 0 4px 12px 0 rgba(15, 23, 42, 0.08);
            --card-border-hover: #CBD5E1;
            
            --card-title-color: #64748B;
            --card-val-color: #0F172A;
            --card-subtext-color: #64748B;
            
            /* Emerald Card (North Star Wedge) */
            --wedge-card-bg: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 100%);
            --wedge-card-border: #10B981;
            --wedge-card-shadow: 0 2px 8px 0 rgba(5, 150, 105, 0.10), 0 1px 3px 0 rgba(5, 150, 105, 0.05);
            --wedge-card-shadow-hover: 0 4px 14px 0 rgba(5, 150, 105, 0.18);
            --wedge-card-title: #047857;
            --wedge-card-val: #059669;
            --wedge-card-subtext: #065F46;
            --wedge-badge-bg: #D1FAE5;
            --wedge-badge-text: #065F46;
            --wedge-badge-border: #6EE7B7;
            
            /* Badges */
            --badge-neutral-bg: #F1F5F9;
            --badge-neutral-text: #334155;
            --badge-neutral-border: #CBD5E1;
            
            --badge-positive-bg: #ECFDF5;
            --badge-positive-text: #065F46;
            --badge-positive-border: #A7F3D0;
            
            --badge-alert-bg: #FFF1F2;
            --badge-alert-text: #BE123C;
            --badge-alert-border: #FDA4AF;
            
            /* Newsflash Banners */
            --newsflash-bg: #F8FAFC;
            --newsflash-border-left: #1E293B;
            --newsflash-border-box: #E2E8F0;
            --newsflash-title: #0F172A;
            --newsflash-sub: #64748B;
            
            /* Divider */
            --divider-color: #E2E8F0;
        }

        /* -----------------------------------------------------------------
           2. Dark Mode Overrides: Applied when OS or Streamlit is in Dark Mode
           ----------------------------------------------------------------- */
        @media (prefers-color-scheme: dark) {
            :root {
                --card-bg: #1E293B;
                --card-border: #334155;
                --card-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.25);
                --card-shadow-hover: 0 6px 16px 0 rgba(0, 0, 0, 0.35);
                --card-border-hover: #475569;
                
                --card-title-color: #94A3B8;
                --card-val-color: #F8FAFC;
                --card-subtext-color: #CBD5E1;
                
                /* Emerald Card in Dark Mode (Luminous Deep Emerald & High Contrast Mint) */
                --wedge-card-bg: linear-gradient(135deg, rgba(6, 78, 59, 0.45) 0%, rgba(15, 23, 42, 0.85) 100%);
                --wedge-card-border: #10B981;
                --wedge-card-shadow: 0 2px 10px 0 rgba(16, 185, 129, 0.20);
                --wedge-card-shadow-hover: 0 6px 18px 0 rgba(16, 185, 129, 0.30);
                --wedge-card-title: #34D399;
                --wedge-card-val: #10B981;
                --wedge-card-subtext: #A7F3D0;
                --wedge-badge-bg: rgba(16, 185, 129, 0.25);
                --wedge-badge-text: #6EE7B7;
                --wedge-badge-border: rgba(52, 211, 153, 0.45);
                
                /* Badges in Dark Mode */
                --badge-neutral-bg: #334155;
                --badge-neutral-text: #F1F5F9;
                --badge-neutral-border: #475569;
                
                --badge-positive-bg: rgba(5, 150, 105, 0.25);
                --badge-positive-text: #6EE7B7;
                --badge-positive-border: rgba(16, 185, 129, 0.4);
                
                --badge-alert-bg: rgba(225, 29, 72, 0.25);
                --badge-alert-text: #FDA4AF;
                --badge-alert-border: rgba(251, 113, 133, 0.4);
                
                /* Newsflash Banners in Dark Mode */
                --newsflash-bg: #1E293B;
                --newsflash-border-left: #10B981;
                --newsflash-border-box: #334155;
                --newsflash-title: #F8FAFC;
                --newsflash-sub: #94A3B8;
                
                /* Divider */
                --divider-color: #334155;
            }
        }

        /* -----------------------------------------------------------------
           3. Metric Card Styling (Adaptive using CSS variables)
           ----------------------------------------------------------------- */
        .kpi-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 1.05rem 1rem;
            box-shadow: var(--card-shadow);
            transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out, border-color 0.15s ease-in-out;
            height: 100%;
            min-height: 162px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .kpi-card:hover {
            box-shadow: var(--card-shadow-hover);
            border-color: var(--card-border-hover);
            transform: translateY(-1px);
        }
        
        /* Emerald Highlighted Card (North Star Avoidable Spend Wedge) */
        .kpi-card-emerald {
            background: var(--wedge-card-bg);
            border: 1.5px solid var(--wedge-card-border);
            border-radius: 10px;
            padding: 1.05rem 1rem;
            box-shadow: var(--wedge-card-shadow);
            transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out, border-color 0.15s ease-in-out;
            height: 100%;
            min-height: 162px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .kpi-card-emerald:hover {
            box-shadow: var(--wedge-card-shadow-hover);
            border-color: #059669;
            transform: translateY(-1px);
        }
        
        .kpi-title {
            font-size: 0.74rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            color: var(--card-title-color);
            margin-bottom: 0.35rem;
            line-height: 1.25;
            min-height: 2.1em;
            display: flex;
            align-items: center;
        }
        
        .kpi-title-emerald {
            font-size: 0.74rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            color: var(--wedge-card-title);
            margin-bottom: 0.35rem;
            line-height: 1.25;
            min-height: 2.1em;
            display: flex;
            align-items: center;
        }
        
        .kpi-value {
            font-size: clamp(1.4rem, 1.9vw, 1.85rem);
            font-weight: 800;
            line-height: 1.15;
            color: var(--card-val-color);
            margin-bottom: 0.45rem;
            font-feature-settings: "tnum";
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .kpi-value-emerald {
            font-size: clamp(1.4rem, 1.9vw, 1.85rem);
            font-weight: 800;
            line-height: 1.15;
            color: var(--wedge-card-val);
            margin-bottom: 0.45rem;
            font-feature-settings: "tnum";
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .kpi-badge {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.2rem 0.5rem;
            border-radius: 5px;
            margin-right: 0.3rem;
            margin-bottom: 0.2rem;
            white-space: nowrap;
        }
        .badge-positive {
            background-color: var(--badge-positive-bg);
            color: var(--badge-positive-text);
            border: 1px solid var(--badge-positive-border);
        }
        .badge-neutral {
            background-color: var(--badge-neutral-bg);
            color: var(--badge-neutral-text);
            border: 1px solid var(--badge-neutral-border);
        }
        .badge-alert {
            background-color: var(--badge-alert-bg);
            color: var(--badge-alert-text);
            border: 1px solid var(--badge-alert-border);
        }
        
        .kpi-subtext {
            font-size: 0.73rem;
            color: var(--card-subtext-color);
            margin-top: 0.4rem;
            line-height: 1.35;
        }
        .kpi-card-emerald .kpi-subtext {
            color: var(--wedge-card-subtext);
            font-weight: 500;
        }
        .kpi-card-emerald .badge-positive {
            background-color: var(--wedge-badge-bg);
            color: var(--wedge-badge-text);
            border: 1px solid var(--wedge-badge-border);
            font-weight: 700;
        }
        
        /* Newsflash container banner */
        .newsflash-banner {
            background-color: var(--newsflash-bg);
            border-left: 4px solid var(--newsflash-border-left);
            border-top: 1px solid var(--newsflash-border-box);
            border-right: 1px solid var(--newsflash-border-box);
            border-bottom: 1px solid var(--newsflash-border-box);
            padding: 0.65rem 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 0.85rem;
        }
        .newsflash-headline {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--newsflash-title);
            margin: 0;
        }
        .newsflash-caption {
            font-size: 0.76rem;
            color: var(--newsflash-sub);
            margin: 0.2rem 0 0 0;
        }
        
        /* Table polish */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--card-border);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Data Ingestion & Caching
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading Medicaid drug utilization datasets...")
def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads cleaned overall and manufacturer detail parquet datasets."""
    if not OVERALL_PARQUET_PATH.exists() or not DETAIL_PARQUET_PATH.exists():
        raise FileNotFoundError(
            f"Required datasets not found in {DATA_DIR}. "
            "Please ensure clean ETL pipeline has run."
        )
    df_overall = pd.read_parquet(OVERALL_PARQUET_PATH)
    df_detail = pd.read_parquet(DETAIL_PARQUET_PATH)
    return df_overall, df_detail


# -----------------------------------------------------------------------------
# Core Calculation Engines
# -----------------------------------------------------------------------------
def compute_kpis(
    df_ov: pd.DataFrame,
    df_dt: pd.DataFrame,
    year: int,
    exclude_outliers: bool,
    selected_classes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Computes the 4 Core Executive KPI values and trend badges.
    """
    spend_col = f"Tot_Spndng_{year}"
    claims_col = f"Tot_Clms_{year}"
    units_col = f"Tot_Dsg_Unts_{year}"
    unit_cost_col = f"Avg_Spnd_Per_Dsg_Unt_Wghtd_{year}"
    outlier_col = f"Outlier_Flag_{year}"

    # Base unfiltered overall view for outlier risk index calculation
    base_ov = df_ov.copy()
    if selected_classes:
        base_ov = base_ov[base_ov["therapeutic_class_macro"].isin(selected_classes)]

    # Compute Outlier Risk Index (Share of gross spend tied to Outlier_Flag == 1)
    base_spend = float(base_ov[spend_col].sum())
    outlier_spend = float(base_ov.loc[base_ov[outlier_col] == 1, spend_col].sum())
    outlier_records_count = int((base_ov[outlier_col] == 1).sum())
    outlier_risk_pct = (outlier_spend / base_spend * 100.0) if base_spend > 0 else 0.0

    # Apply outlier filter if enabled
    filtered_ov = base_ov.copy()
    filtered_dt = df_dt.copy()
    if selected_classes:
        filtered_dt = filtered_dt[filtered_dt["therapeutic_class_macro"].isin(selected_classes)]

    if exclude_outliers:
        filtered_ov = filtered_ov[filtered_ov[outlier_col] == 0]
        filtered_dt = filtered_dt[filtered_dt[outlier_col] == 0]

    # Card 1: Gross Medicaid Spend
    tot_spend = float(filtered_ov[spend_col].sum())
    spend_2020 = float(filtered_ov["Tot_Spndng_2020"].sum())
    spend_5yr_pct = (
        ((tot_spend - spend_2020) / spend_2020 * 100.0) if spend_2020 > 0 else 0.0
    )

    # Card 3: Total Prescription Claim Volume
    tot_claims = int(filtered_ov[claims_col].sum())
    prev_year = year - 1 if year > 2020 else 2020
    prev_claims_col = f"Tot_Clms_{prev_year}"
    claims_prev = int(filtered_ov[prev_claims_col].sum())
    claims_yoy_pct = (
        ((tot_claims - claims_prev) / claims_prev * 100.0) if (claims_prev > 0 and year > 2020) else 0.0
    )

    # Card 2: North Star Avoidable Brand-to-Generic Spend Wedge
    # Wedge = Sum [ (Brand_Unit_Cost - Lowest_Generic_Unit_Cost) * Brand_Dosage_Units ]
    brand_sub = filtered_ov[
        filtered_ov["is_brand_flag"] & (filtered_ov[units_col] > 0) & (filtered_ov[unit_cost_col] > 0)
    ].copy()
    gen_dt = filtered_dt[
        (~filtered_dt["is_brand_flag"]) & (filtered_dt[unit_cost_col] > 0) & (filtered_dt[units_col] > 0)
    ]
    min_gen_cost = gen_dt.groupby("Gnrc_Name")[unit_cost_col].min().to_dict()

    total_wedge = 0.0
    wedge_drug_count = 0
    total_brand_spend_affected = 0.0

    for _, row in brand_sub.iterrows():
        gnrc = row["Gnrc_Name"]
        if gnrc in min_gen_cost:
            b_cost = float(row[unit_cost_col])
            g_cost = float(min_gen_cost[gnrc])
            b_units = float(row[units_col])
            if b_cost > g_cost and b_units > 0:
                spread = b_cost - g_cost
                wedge_val = spread * b_units
                total_wedge += wedge_val
                wedge_drug_count += 1
                total_brand_spend_affected += float(row[spend_col])

    brand_tot_spend = float(filtered_ov.loc[filtered_ov["is_brand_flag"], spend_col].sum())
    wedge_share_of_brand = (
        (total_wedge / brand_tot_spend * 100.0) if brand_tot_spend > 0 else 0.0
    )

    return {
        "year": year,
        "tot_spend": tot_spend,
        "spend_5yr_pct": spend_5yr_pct,
        "spend_2020": spend_2020,
        "total_wedge": total_wedge,
        "wedge_drug_count": wedge_drug_count,
        "wedge_share_of_brand": wedge_share_of_brand,
        "total_brand_spend_affected": total_brand_spend_affected,
        "tot_claims": tot_claims,
        "claims_yoy_pct": claims_yoy_pct,
        "prev_year": prev_year,
        "outlier_risk_pct": outlier_risk_pct,
        "outlier_spend": outlier_spend,
        "outlier_records_count": outlier_records_count,
        "exclude_outliers_active": exclude_outliers,
    }


def compute_formulary_action_table(
    df_ov: pd.DataFrame,
    df_dt: pd.DataFrame,
    year: int,
    exclude_outliers: bool,
    selected_classes: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Builds the sortable Actionable Formulary Grid containing the addressable
    Brand-to-Generic spend wedge for formulary tiering and MAC cap decisions.
    """
    unit_col = f"Avg_Spnd_Per_Dsg_Unt_Wghtd_{year}"
    units_col = f"Tot_Dsg_Unts_{year}"
    spend_col = f"Tot_Spndng_{year}"
    claims_col = f"Tot_Clms_{year}"
    outlier_col = f"Outlier_Flag_{year}"

    sub_ov = df_ov.copy()
    sub_dt = df_dt.copy()

    if exclude_outliers:
        sub_ov = sub_ov[sub_ov[outlier_col] == 0]
        sub_dt = sub_dt[sub_dt[outlier_col] == 0]

    if selected_classes:
        sub_ov = sub_ov[sub_ov["therapeutic_class_macro"].isin(selected_classes)]
        sub_dt = sub_dt[sub_dt["therapeutic_class_macro"].isin(selected_classes)]

    brand_df = sub_ov[
        sub_ov["is_brand_flag"] & (sub_ov[units_col] > 0) & (sub_ov[unit_col] > 0)
    ].copy()
    gen_dt = sub_dt[
        (~sub_dt["is_brand_flag"]) & (sub_dt[unit_col] > 0) & (sub_dt[units_col] > 0)
    ]

    min_gen_cost = gen_dt.groupby("Gnrc_Name")[unit_col].min().to_dict()
    mftr_counts = gen_dt.groupby("Gnrc_Name")["Mftr_Name"].nunique().to_dict()

    records = []
    for _, row in brand_df.iterrows():
        gnrc = row["Gnrc_Name"]
        if gnrc in min_gen_cost:
            b_cost = float(row[unit_col])
            g_cost = float(min_gen_cost[gnrc])
            b_units = float(row[units_col])
            b_spend = float(row[spend_col])
            b_claims = int(row[claims_col])

            if b_cost > g_cost and b_units > 0:
                spread = b_cost - g_cost
                savings = spread * b_units
                records.append({
                    "Brand Name": row["Brnd_Name"],
                    "Generic Name": gnrc,
                    "Therapeutic Class": row["therapeutic_class_macro"],
                    "Competing Manufacturers": int(mftr_counts.get(gnrc, 1)),
                    "Current Unit Cost": round(b_cost, 2),
                    "Lowest Generic Unit Cost": round(g_cost, 2),
                    "Addressable Annual Savings ($)": round(savings, 2),
                    "Brand Gross Spend ($)": round(b_spend, 2),
                    "Prescription Claims": b_claims,
                    "Savings Share (%)": round((savings / b_spend * 100.0) if b_spend > 0 else 0.0, 1),
                    "Primary Driver": row.get("price_vs_volume_driver", "N/A"),
                })

    df_action = pd.DataFrame(records)
    if not df_action.empty:
        df_action = df_action.sort_values(
            by="Addressable Annual Savings ($)", ascending=False
        ).reset_index(drop=True)
    return df_action


# -----------------------------------------------------------------------------
# Chart Builders (Plotly with Slate/Navy & Emerald Palette, Zero Chartjunk)
# -----------------------------------------------------------------------------
def build_pareto_distribution_chart(
    df_ov: pd.DataFrame,
    year: int,
    exclude_outliers: bool,
    selected_classes: Optional[List[str]] = None,
    top_n: int = 20,
) -> go.Figure:
    """
    Renders the Pareto spend distribution chart of top budget-draining drugs
    with cumulative outlay share on secondary y-axis.
    """
    spend_col = f"Tot_Spndng_{year}"
    outlier_col = f"Outlier_Flag_{year}"

    sub = df_ov.copy()
    if exclude_outliers:
        sub = sub[sub[outlier_col] == 0]
    if selected_classes:
        sub = sub[sub["therapeutic_class_macro"].isin(selected_classes)]

    tot_market_spend = float(sub[spend_col].sum())
    top_drugs = sub.sort_values(by=spend_col, ascending=False).head(top_n).copy()

    top_drugs["spend_billions"] = top_drugs[spend_col] / 1e9
    top_drugs["cum_spend"] = top_drugs[spend_col].cumsum()
    top_drugs["cum_share_pct"] = (top_drugs["cum_spend"] / tot_market_spend) * 100.0

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar trace: Gross spend by drug
    fig.add_trace(
        go.Bar(
            x=top_drugs["Brnd_Name"],
            y=top_drugs["spend_billions"],
            name="Gross Drug Spend ($B)",
            marker=dict(
                color=COLOR_NAVY_PRIMARY,
                line=dict(color=COLOR_NAVY_DARK, width=0.75),
            ),
            hovertemplate=(
                "<b>%{x}</b> (%{customdata[0]})<br>"
                "Therapeutic Class: %{customdata[1]}<br>"
                "Gross Spend: $%{y:.2f}B<br>"
                "Program Share: %{customdata[2]:.2f}%<extra></extra>"
            ),
            customdata=np.stack((
                top_drugs["Gnrc_Name"],
                top_drugs["therapeutic_class_macro"],
                (top_drugs[spend_col] / tot_market_spend * 100.0),
            ), axis=-1),
        ),
        secondary_y=False,
    )

    # Line trace: Cumulative share curve
    fig.add_trace(
        go.Scatter(
            x=top_drugs["Brnd_Name"],
            y=top_drugs["cum_share_pct"],
            name="Cumulative Spend Share (%)",
            mode="lines+markers",
            line=dict(color=COLOR_EMERALD, width=2.5),
            marker=dict(size=6, color=COLOR_EMERALD),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Cumulative Spend Share: %{y:.1f}%<extra></extra>"
            ),
        ),
        secondary_y=True,
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=390,
        margin=dict(l=45, r=45, t=30, b=85),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLOR_NAVY_PRIMARY),
        ),
        xaxis=dict(
            tickangle=-40,
            tickfont=dict(size=10, color=COLOR_NAVY_PRIMARY),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(
                text="Gross Medicaid Spend ($B)",
                font=dict(size=11, color=COLOR_NAVY_PRIMARY),
            ),
            tickprefix="$",
            ticksuffix="B",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
        ),
        yaxis2=dict(
            title=dict(
                text="Cumulative Outlay Share (%)",
                font=dict(size=11, color=COLOR_EMERALD),
            ),
            ticksuffix="%",
            range=[0, max(40.0, float(top_drugs["cum_share_pct"].max()) * 1.15)],
            showgrid=False,
            zeroline=False,
        ),
    )
    return fig


def build_lorenz_curve_chart(
    df_ov: pd.DataFrame,
    year: int,
    exclude_outliers: bool,
    selected_classes: Optional[List[str]] = None,
) -> go.Figure:
    """
    Renders the Macro Population Lorenz Curve showing overall spend inequality.
    """
    spend_col = f"Tot_Spndng_{year}"
    outlier_col = f"Outlier_Flag_{year}"

    sub = df_ov.copy()
    if exclude_outliers:
        sub = sub[sub[outlier_col] == 0]
    if selected_classes:
        sub = sub[sub["therapeutic_class_macro"].isin(selected_classes)]

    sub_sorted = sub[sub[spend_col] > 0].sort_values(by=spend_col, ascending=True).reset_index(drop=True)
    n = len(sub_sorted)
    if n == 0:
        return go.Figure()

    spends = sub_sorted[spend_col].values
    tot_spend = np.sum(spends)

    # Gini coefficient
    index = np.arange(1, n + 1)
    gini = float((np.sum((2 * index - n - 1) * spends)) / (n * tot_spend))

    cum_spend = np.cumsum(spends) / tot_spend
    cum_pop = np.arange(1, n + 1) / n

    # Find cutoff for top drugs driving 65% of spend
    # That is where cumulative spend from bottom reaches 35% (1 - 0.65)
    idx_65 = np.searchsorted(cum_spend, 0.35)
    drugs_for_65 = n - idx_65
    pct_drugs_for_65 = (drugs_for_65 / n) * 100.0

    fig = go.Figure()

    # Line of equality
    fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            line=dict(color=COLOR_SLATE_LIGHT, dash="dash", width=1.5),
            name="Equality Line (Gini = 0.0)",
            hovertemplate="Equal Distribution: %{x:.0%}<extra></extra>",
        )
    )

    # Actual Lorenz curve
    fig.add_trace(
        go.Scatter(
            x=cum_pop,
            y=cum_spend,
            mode="lines",
            line=dict(color=COLOR_NAVY_PRIMARY, width=2.5),
            name=f"Spend Lorenz Curve (Gini = {gini:.3f})",
            fill="tonexty",
            fillcolor="rgba(30, 41, 59, 0.05)",
            hovertemplate="Cumulative Drugs: %{x:.1%}<br>Cumulative Spend: %{y:.1%}<extra></extra>",
        )
    )

    # Marker for top drugs driving 65% of spend
    if idx_65 < n:
        fig.add_trace(
            go.Scatter(
                x=[cum_pop[idx_65]],
                y=[cum_spend[idx_65]],
                mode="markers+text",
                marker=dict(color=COLOR_CRIMSON, size=10, symbol="circle"),
                text=[f"65% Outlay Threshold (Top {pct_drugs_for_65:.1f}% of Drugs)"],
                textposition="top left",
                textfont=dict(size=10, color=COLOR_CRIMSON),
                name="65% Outlay Concentration Marker",
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=390,
        margin=dict(l=45, r=45, t=30, b=50),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLOR_NAVY_PRIMARY),
        ),
        xaxis=dict(
            title="Cumulative Share of Drug Entities (Lowest to Highest Spend)",
            tickformat=".0%",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
        ),
        yaxis=dict(
            title="Cumulative Share of Gross Spend",
            tickformat=".0%",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
        ),
    )
    return fig


def build_quadrant_scatter_chart(
    df_ov: pd.DataFrame,
    selected_classes: Optional[List[str]] = None,
    exclude_outliers: bool = False,
    cohort_size: int = 75,
) -> go.Figure:
    """
    Renders the Price vs. Volume Growth Quadrant Plot:
      X: 5-Year Prescription Claim Volume Growth (%)
      Y: 5-Year Unit Cost CAGR (%)
      Bubble Size: CY2024 Gross Spend ($)
    """
    sub = df_ov.copy()
    if exclude_outliers:
        sub = sub[sub["Outlier_Flag_2024"] == 0]
    if selected_classes:
        sub = sub[sub["therapeutic_class_macro"].isin(selected_classes)]

    # Filter to active longitudinal records with positive claims and spend
    valid = sub[
        (sub["Tot_Clms_2020"] > 0)
        & (sub["Tot_Clms_2024"] > 0)
        & (sub["Tot_Spndng_2024"] > 0)
    ].copy()

    valid["claims_growth_pct"] = (
        (valid["Tot_Clms_2024"] - valid["Tot_Clms_2020"]) / valid["Tot_Clms_2020"]
    ) * 100.0
    valid["unit_cost_cagr_pct"] = valid["CAGR_Avg_Spnd_Per_Dsg_Unt_20_24"] * 100.0

    cohort = valid.sort_values(by="Tot_Spndng_2024", ascending=False).head(cohort_size).copy()

    fig = go.Figure()

    driver_palette = {
        "Volume-Driven": (COLOR_EMERALD, "Volume Expansion (Claims Dominant)"),
        "Price-Driven": (COLOR_CRIMSON, "Price Escalation (CAGR Dominant)"),
        "Dual Pressure": (COLOR_NAVY_PRIMARY, "Dual Expansion (Volume + Price)"),
    }

    for driver, (color, label) in driver_palette.items():
        subset = cohort[cohort["price_vs_volume_driver"] == driver]
        if subset.empty:
            continue

        fig.add_trace(
            go.Scatter(
                x=subset["claims_growth_pct"],
                y=subset["unit_cost_cagr_pct"],
                mode="markers+text",
                name=f"{label} ({len(subset)})",
                text=subset["Brnd_Name"],
                textposition="top center",
                textfont=dict(size=8.5, color=COLOR_NAVY_PRIMARY),
                marker=dict(
                    size=np.clip(np.sqrt(subset["Tot_Spndng_2024"] / 1e6) * 1.55, 9, 36),
                    color=color,
                    opacity=0.82,
                    line=dict(color=COLOR_NAVY_DARK, width=0.75),
                ),
                hovertemplate=(
                    "<b>%{text}</b> (%{customdata[0]})<br>"
                    "Therapeutic Class: %{customdata[1]}<br>"
                    "2024 Gross Spend: $%{customdata[2]:,.2f}B<br>"
                    "5-Yr Claim Volume Growth: +%{x:.1f}%<br>"
                    "Unit Cost CAGR: %{y:.1f}%<br>"
                    "Driver: " + driver + "<extra></extra>"
                ),
                customdata=np.stack((
                    subset["Gnrc_Name"],
                    subset["therapeutic_class_macro"],
                    subset["Tot_Spndng_2024"] / 1e9,
                ), axis=-1),
            )
        )

    # Zero crosshairs for 4 Quadrants
    fig.add_vline(x=0, line=dict(color=COLOR_SLATE_LIGHT, dash="dash", width=1.2))
    fig.add_hline(y=0, line=dict(color=COLOR_SLATE_LIGHT, dash="dash", width=1.2))

    # Quadrant Watermark Annotations
    fig.add_annotation(
        x=280, y=28,
        text="<b>QUADRANT 1: DUAL PRESSURE</b><br>Volume & Price Escalation",
        showarrow=False,
        font=dict(size=9, color=COLOR_SLATE_MUTED),
        opacity=0.6,
    )
    fig.add_annotation(
        x=-30, y=28,
        text="<b>QUADRANT 2: PRICE ESCALATION</b><br>Price Gouging / Low Utilization",
        showarrow=False,
        font=dict(size=9, color=COLOR_CRIMSON),
        opacity=0.6,
    )
    fig.add_annotation(
        x=280, y=-15,
        text="<b>QUADRANT 4: VOLUME DRIVEN</b><br>Utilization Surge / Price Restraint",
        showarrow=False,
        font=dict(size=9, color=COLOR_EMERALD),
        opacity=0.6,
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=390,
        margin=dict(l=45, r=45, t=30, b=50),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=COLOR_NAVY_PRIMARY),
        ),
        xaxis=dict(
            title="5-Year Claim Volume Growth (%) [CY2020 to CY2024]",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
            range=[-50, 480],  # Default executive zoom range; user can zoom/pan
            ticksuffix="%",
        ),
        yaxis=dict(
            title="Unit Cost CAGR (%) [CY2020 to CY2024]",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
            range=[-25, 35],
            ticksuffix="%",
        ),
    )
    return fig


# -----------------------------------------------------------------------------
# Main Application Layout & Controller
# -----------------------------------------------------------------------------
def main() -> None:
    # Load cached parquet tables
    try:
        df_overall, df_detail = load_datasets()
    except Exception as exc:
        st.error(f"Failed to load dataset: {exc}")
        st.stop()

    # -------------------------------------------------------------------------
    # Header Tier: Executive Mandate & Title
    # -------------------------------------------------------------------------
    header_col1, header_col2 = st.columns([3.4, 1.6])
    with header_col1:
        st.title("Medicaid Outpatient Drug Spend Optimization")
        st.caption(
            "Executive Formulary Stewardship & Spend Extraction System | "
            "Governing Framework: READY & DASH | State Medicaid P&T Committee Briefing"
        )
    with header_col2:
        st.markdown(
            """
            <div style="text-align: right; padding-top: 0.85rem;">
                <span class="kpi-badge badge-neutral" style="font-size: 0.78rem; padding: 0.28rem 0.65rem; font-weight: 600;">CMS SDUD: CY2020–CY2024</span>
                <div style="font-size: 0.75rem; color: var(--card-subtext-color); margin-top: 0.35rem; font-weight: 500;">Statutory Gross Pre-Rebate Outlay</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='margin: 0.4rem 0 1.2rem 0; border: 0; border-top: 1px solid var(--divider-color);'>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Sidebar: Filter Controls (Task 4.3)
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.subheader("Formulary Filter Controls")
        st.caption("Adjust policy parameters and therapeutic scope.")

        # Filter 1: Benefit Year Selector (Default: 2024)
        available_years = [2024, 2023, 2022, 2021, 2020]
        selected_year = st.selectbox(
            "Benefit Year",
            options=available_years,
            index=0,
            help="Select the Medicaid benefit reporting calendar year.",
        )

        # Filter 2: Outlier Sensitivity Toggle (Default: False)
        exclude_outliers = st.toggle(
            "Exclude CMS Outlier Records",
            value=False,
            help=(
                "Excludes records where Outlier_Flag == 1 (CMS IQR bounds violations: "
                "Weighted dosage unit price shifted by > 10% and > $1.00)."
            ),
        )

        st.markdown("<hr style='margin: 0.75rem 0;'>", unsafe_allow_html=True)

        # Filter 3: Therapeutic Class Multi-Select
        all_therapeutic_classes = sorted(
            [c for c in df_overall["therapeutic_class_macro"].dropna().unique() if c != "Other / Specialized Care"]
        ) + ["Other / Specialized Care"]

        select_all_classes = st.checkbox("Select All Therapeutic Classes", value=True)
        if select_all_classes:
            selected_classes = all_therapeutic_classes
            st.info(f"All {len(all_therapeutic_classes)} therapeutic classes active.")
        else:
            selected_classes = st.multiselect(
                "Therapeutic Classes",
                options=all_therapeutic_classes,
                default=[
                    "Antidiabetic / GLP-1",
                    "Central Nervous System / Psychotropic",
                    "Immunology / Immunomodulator",
                    "Respiratory / Pulmonary",
                ],
                help="Filter analysis to specific clinical therapeutic indications.",
            )
            if not selected_classes:
                st.warning("Please select at least one therapeutic class.")
                selected_classes = all_therapeutic_classes

        st.markdown("<hr style='margin: 0.75rem 0;'>", unsafe_allow_html=True)

        # Executive Metadata & Audit Stamp
        st.caption("Data Architecture Auditing:")
        st.caption(f"• Drug Entities (Overall): {len(df_overall):,} records")
        st.caption(f"• Manufacturer Detail: {len(df_detail):,} labeler lines")
        st.caption("• HIPAA Small-Cell Rule: < 11 claims non-zero imputed")

    # -------------------------------------------------------------------------
    # Top Tier: 4 Core KPI Callout Cards (Task 4.1 & 4.2)
    # -------------------------------------------------------------------------
    kpis = compute_kpis(
        df_overall,
        df_detail,
        year=selected_year,
        exclude_outliers=exclude_outliers,
        selected_classes=selected_classes,
    )

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    # Card 1: Gross Medicaid Spend
    with kpi_col1:
        spend_val_b = kpis["tot_spend"] / 1e9
        spend_5yr_badge = f"{kpis['spend_5yr_pct']:+.1f}% 5-Yr Growth"
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">{kpis['year']} Gross Medicaid Spend</div>
                <div class="kpi-value">${spend_val_b:.2f}B</div>
                <div>
                    <span class="kpi-badge badge-neutral">{spend_5yr_badge}</span>
                </div>
                <div class="kpi-subtext">Pre-rebate outpatient pharmacy payments across all participating state agencies.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card 2: Avoidable Brand-to-Generic Spend Wedge (North Star Highlighted in Emerald)
    with kpi_col2:
        wedge_val_m = kpis["total_wedge"] / 1e6
        wedge_val_b = kpis["total_wedge"] / 1e9
        st.markdown(
            f"""
            <div class="kpi-card-emerald">
                <div class="kpi-title-emerald">Avoidable Spend Wedge</div>
                <div class="kpi-value-emerald">${wedge_val_m:,.1f}M</div>
                <div>
                    <span class="kpi-badge badge-positive">${wedge_val_b:.2f}B Addressable</span>
                    <span class="kpi-badge badge-positive">{kpis['wedge_drug_count']:,} Brand Drugs</span>
                </div>
                <div class="kpi-subtext">Addressable savings from reimbursing brand drugs when bioequivalent generics were dispensed.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card 3: Total Prescription Claim Volume
    with kpi_col3:
        claims_val_m = kpis["tot_claims"] / 1e6
        claims_badge = (
            f"{kpis['claims_yoy_pct']:+.1f}% YoY vs {kpis['prev_year']}"
            if kpis["year"] > 2020
            else "Baseline Year"
        )
        badge_style = "badge-neutral" if kpis["claims_yoy_pct"] <= 0 else "badge-alert"
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Prescription Claim Volume</div>
                <div class="kpi-value">{claims_val_m:.1f}M</div>
                <div>
                    <span class="kpi-badge {badge_style}">{claims_badge}</span>
                </div>
                <div class="kpi-subtext">Total Medicaid prescription fills tracking statewide clinical patient utilization.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card 4: Outlier Distortion Risk Index
    with kpi_col4:
        outlier_pct = kpis["outlier_risk_pct"]
        if kpis["exclude_outliers_active"]:
            outlier_display = "0.00%"
            outlier_badge = "Active: Filtered"
            badge_class = "badge-positive"
            subtext = f"Audit toggle active: {kpis['outlier_records_count']:,} CMS outlier-flagged records excluded from view."
        else:
            outlier_display = f"{outlier_pct:.2f}%"
            outlier_badge = f"${kpis['outlier_spend'] / 1e9:.2f}B Flagged Spend"
            badge_class = "badge-alert" if outlier_pct > 5.0 else "badge-neutral"
            subtext = f"Guardrail Metric: {kpis['outlier_records_count']:,} records violating CMS IQR dosage price bounds."

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Outlier Distortion Risk</div>
                <div class="kpi-value">{outlier_display}</div>
                <div>
                    <span class="kpi-badge {badge_class}">{outlier_badge}</span>
                </div>
                <div class="kpi-subtext">{subtext}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Middle Tier: Macro Strategy & Drivers (Task 4.3 - 2 Columns)
    # -------------------------------------------------------------------------
    mid_col_left, mid_col_right = st.columns(2)

    # Left Column: Cumulative Spend Concentration (Lorenz / Pareto Distribution)
    with mid_col_left:
        st.markdown(
            """
            <div class="newsflash-banner">
                <div class="newsflash-headline">Top 20 Drugs Consume ~29% of Program Outlay; Top 3.5% Drive 65% of Total Spend</div>
                <div class="newsflash-caption">Pareto Distribution & Lorenz Inequality Analysis across Outpatient Drug Entities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_pareto, tab_lorenz = st.tabs(["Top 20 Drug Pareto Analysis", "Full Market Lorenz Curve"])
        with tab_pareto:
            fig_pareto = build_pareto_distribution_chart(
                df_overall,
                year=selected_year,
                exclude_outliers=exclude_outliers,
                selected_classes=selected_classes,
                top_n=20,
            )
            st.plotly_chart(fig_pareto, width="stretch", config={"displayModeBar": False})
        with tab_lorenz:
            fig_lorenz = build_lorenz_curve_chart(
                df_overall,
                year=selected_year,
                exclude_outliers=exclude_outliers,
                selected_classes=selected_classes,
            )
            st.plotly_chart(fig_lorenz, width="stretch", config={"displayModeBar": False})

    # Right Column: Price vs. Volume Growth Quadrant Plot
    with mid_col_right:
        st.markdown(
            """
            <div class="newsflash-banner">
                <div class="newsflash-headline">Medicaid Outlay Growth Is Overwhelmingly Utilization-Driven (Paired Wilcoxon p &lt; 10⁻¹⁴)</div>
                <div class="newsflash-caption">5-Year Growth Quadrant: Claim Volume vs. Unit Cost CAGR (Bubble Size: 2024 Gross Spend)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        quadrant_cohort_col, _ = st.columns([2, 1])
        with quadrant_cohort_col:
            cohort_selection = st.selectbox(
                "Display Cohort",
                options=["Top 50 Drugs by Gross Spend", "Top 100 Drugs by Gross Spend", "Top 200 Drugs by Gross Spend"],
                index=1,
                label_visibility="collapsed",
            )
        cohort_n = int(cohort_selection.split()[1])

        fig_quadrant = build_quadrant_scatter_chart(
            df_overall,
            selected_classes=selected_classes,
            exclude_outliers=exclude_outliers,
            cohort_size=cohort_n,
        )
        st.plotly_chart(fig_quadrant, width="stretch", config={"displayModeBar": True})

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Bottom Tier: Actionable Formulary Grid (Task 4.3 & 4.4)
    # -------------------------------------------------------------------------
    df_action_full = compute_formulary_action_table(
        df_overall,
        df_detail,
        year=selected_year,
        exclude_outliers=exclude_outliers,
        selected_classes=selected_classes,
    )

    tot_action_savings = df_action_full["Addressable Annual Savings ($)"].sum() if not df_action_full.empty else 0.0
    tot_action_drugs = len(df_action_full)

    st.markdown(
        f"""
        <div class="newsflash-banner">
            <div class="newsflash-headline">Formulary Action Plan: ${tot_action_savings / 1e6:,.1f}M in Annual Addressable Savings Identified Across {tot_action_drugs:,} Brand Medications</div>
            <div class="newsflash-caption">Actionable Target List for PDL Non-Preferred Tiering, Step Therapy, and State MAC Price Ceilings</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search & Table Controls
    grid_ctrl1, grid_ctrl2, grid_ctrl3 = st.columns([2.5, 1.5, 1.5])
    with grid_ctrl1:
        search_query = st.text_input(
            "Search Drug or Chemical Entity",
            placeholder="Type brand name (e.g. ABILIFY, VYVANSE, CONCERTA) or generic ingredient...",
            label_visibility="collapsed",
        )
    with grid_ctrl2:
        min_savings_cutoff = st.selectbox(
            "Savings Filter",
            options=["All Savings Opportunities", "Savings > $1M", "Savings > $10M", "Savings > $50M"],
            index=0,
            label_visibility="collapsed",
        )
    with grid_ctrl3:
        # Download Button (Task 4.3)
        csv_buffer = io.StringIO()
        df_action_full.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Export Action Plan (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"medicaid_formulary_action_plan_{selected_year}.csv",
            mime="text/csv",
            width="stretch",
            help="Download complete targeted formulary action list for P&T Committee and actuarial modeling.",
        )

    # Apply search and minimum savings filters
    filtered_table = df_action_full.copy()
    if search_query:
        query_upper = search_query.strip().upper()
        filtered_table = filtered_table[
            filtered_table["Brand Name"].str.upper().str.contains(query_upper, na=False)
            | filtered_table["Generic Name"].str.upper().str.contains(query_upper, na=False)
        ]

    if min_savings_cutoff == "Savings > $1M":
        filtered_table = filtered_table[filtered_table["Addressable Annual Savings ($)"] >= 1e6]
    elif min_savings_cutoff == "Savings > $10M":
        filtered_table = filtered_table[filtered_table["Addressable Annual Savings ($)"] >= 1e7]
    elif min_savings_cutoff == "Savings > $50M":
        filtered_table = filtered_table[filtered_table["Addressable Annual Savings ($)"] >= 5e7]

    # Display sortable, styled dataframe
    st.dataframe(
        filtered_table,
        width="stretch",
        hide_index=True,
        height=400,
        column_config={
            "Brand Name": st.column_config.TextColumn("Brand Name", width="medium"),
            "Generic Name": st.column_config.TextColumn("Generic Name", width="large"),
            "Therapeutic Class": st.column_config.TextColumn("Therapeutic Class", width="medium"),
            "Competing Manufacturers": st.column_config.NumberColumn(
                "Competing Mftrs",
                help="Number of distinct manufacturers actively dispensing the bioequivalent generic in Medicaid.",
                format="%d",
                width="small",
            ),
            "Current Unit Cost": st.column_config.NumberColumn(
                "Current Unit Cost",
                help="Weighted average Medicaid reimbursement per dosage unit for brand name.",
                format="$%.2f",
                width="small",
            ),
            "Lowest Generic Unit Cost": st.column_config.NumberColumn(
                "Lowest Generic Unit Cost",
                help="Lowest weighted unit cost among active competing generic manufacturers.",
                format="$%.2f",
                width="small",
            ),
            "Addressable Annual Savings ($)": st.column_config.NumberColumn(
                "Addressable Annual Savings ($)",
                help="Projected state-level savings if brand volume transitions to lowest available generic tier.",
                format="$%,.0f",
                width="medium",
            ),
            "Brand Gross Spend ($)": st.column_config.NumberColumn(
                "Brand Gross Spend ($)",
                format="$%,.0f",
                width="small",
            ),
            "Prescription Claims": st.column_config.NumberColumn(
                "Claims",
                format="%,d",
                width="small",
            ),
            "Savings Share (%)": st.column_config.NumberColumn(
                "Savings %",
                format="%.1f%%",
                width="small",
            ),
            "Primary Driver": st.column_config.TextColumn("Primary Driver", width="small"),
        },
    )

    st.caption(
        f"Displaying {len(filtered_table):,} of {tot_action_drugs:,} addressable brand medications. "
        "Sort any column by clicking the header. Data is updated in real-time according to active sidebar filters."
    )

    # -------------------------------------------------------------------------
    # Footer: Executive Documentation & Methodological Governance
    # -------------------------------------------------------------------------
    with st.expander("Methodology, Statutory Boundaries & Formulary Implementation Guidance"):
        st.markdown(
            """
            ### Governing Methodology & Governance Standards
            
            1. **Pre-Rebate Gross Spend Scope**:
               Reimbursements reported represent payments to dispensing pharmacies and do not reflect confidential
               statutory manufacturer rebates under the Medicaid Drug Rebate Program (MDRP) or state supplemental rebate agreements.
               Net effective state savings may vary depending on existing rebate contracts.
               
            2. **The North Star Metric (Avoidable Spend Wedge)**:
               $$\\text{Avoidable Spend Wedge} = \\sum_{i \\in \\text{Multi-Source Brand}} \\left( \\text{Brand\\_Unit\\_Cost}_i - \\min_m(\\text{Generic\\_Unit\\_Cost}_{m,i}) \\right) \\times \\text{Brand\\_Units}_i$$
               Calculated strictly for brand medications with verifiable active generic labelers dispensing during the same calendar year.
               
            3. **Clinical Access Guardrail (< 2.5% Disruption)**:
               Formulary tiering adjustments should prioritize high-volume chronic conditions with 3+ validated bioequivalent alternatives
               to prevent therapy disruption, adverse clinical events, or provider prior authorization burden.
               
            4. **CMS IQR Outlier Flag Auditing**:
               Records flagged with `Outlier_Flag == 1` violate CMS interquartile pricing bounds (cost shift > 10% and > \\$1.00/unit).
               These records represent 8.16% of gross CY2024 spend (\\$9.08B) and should undergo NDC-level verification before binding legislative forecasts.
            """
        )


if __name__ == "__main__":
    main()
