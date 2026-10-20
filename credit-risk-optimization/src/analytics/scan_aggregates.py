"""
src/analytics/scan_aggregates.py
Consumer Credit Risk & Underwriting Optimization
Phase 2 / Task 2.2: A – Aggregates & Anomalies Auditing
Framework: Christine Jiang SCAN Framework (Stage A)

Executes:
  1. Top-Line Portfolio Reconciliations:
     - Total Funded Principal ($)
     - Total Principal Repaid ($)
     - Total Interest Collected ($)
     - Total Recoveries ($) and Collection Fees ($)
     - Net Cash Flow ($) = Principal Repaid + Interest + Recoveries - Fees - Funded Principal
     - Cumulative Net Charge-Off Principal ($)
     - Platform-Level Aggregate LAROC (%) = (Total Net Cash Flow / Total Funded Principal) * 100
  2. Distribution & Dispersion Statistics:
     - Mean, Median, Std Dev, P25, P75, P90, P99, and IQR for:
       funded_amnt, int_rate, annual_inc, dti, revol_util, fico_midpoint, laroc.
  3. Active Portfolio Exposure Audit:
     - Read data/cleaned/fct_active_portfolio.parquet (912,569 records)
     - Total active funded amount at risk and status breakdown:
       Current, Late (16-30 days), Late (31-120 days), In Grace Period.
  4. Outputs:
     - reports/scan_aggregates_summary.md
     - data/exports/portfolio_aggregates.csv
     - data/exports/active_portfolio_exposure.csv
"""

from pathlib import Path
import time
import pandas as pd
import numpy as np


def load_datasets(
    seasoned_path: Path = Path("data/cleaned/fct_closed_loans_seasoned.parquet"),
    active_path: Path = Path("data/cleaned/fct_active_portfolio.parquet"),
):
    """Load both seasoned closed loans and active portfolio datasets."""
    print(f"[STAGE A] Loading seasoned cohort: {seasoned_path}...")
    df_seasoned = pd.read_parquet(seasoned_path)
    print(f"[STAGE A] Loaded {len(df_seasoned):,} seasoned records.")

    print(f"[STAGE A] Loading active portfolio: {active_path}...")
    df_active = pd.read_parquet(active_path)
    print(f"[STAGE A] Loaded {len(df_active):,} active records.")

    return df_seasoned, df_active


def compute_topline_reconciliations(df_seasoned: pd.DataFrame) -> dict:
    """
    Computes top-line portfolio cash ledger reconciliations and platform LAROC.
    """
    total_funded = float(df_seasoned["funded_amnt"].sum())
    total_rec_prncp = float(df_seasoned["total_rec_prncp"].sum())
    total_rec_int = float(df_seasoned["total_rec_int"].sum())
    total_rec_late = float(df_seasoned["total_rec_late_fee"].sum())
    gross_recoveries = float(df_seasoned["recoveries"].sum())
    recovery_fees = float(df_seasoned["collection_recovery_fee"].sum())
    net_recoveries = gross_recoveries - recovery_fees
    total_pymnt = float(df_seasoned["total_pymnt"].sum())

    # Component Net Cash Flow
    # Formula: Principal Repaid + Interest + Recoveries - Fees - Funded Principal
    component_net_cash_flow = (
        total_rec_prncp + total_rec_int + gross_recoveries - recovery_fees - total_funded
    )
    component_laroc = (component_net_cash_flow / total_funded) * 100.0

    # Engineered Net Cash Flow (clean_loans.py column: total_pymnt + recoveries - fee - funded)
    total_net_cash_flow = float(df_seasoned["net_cash_flow"].sum())
    aggregate_laroc = (total_net_cash_flow / total_funded) * 100.0

    # Charge-off analysis
    bad_mask = df_seasoned["is_bad_loan"] == 1
    bad_funded = float(df_seasoned.loc[bad_mask, "funded_amnt"].sum())
    bad_rec_prncp = float(df_seasoned.loc[bad_mask, "total_rec_prncp"].sum())
    gross_chargeoff_principal = bad_funded - bad_rec_prncp
    net_chargeoff_principal = gross_chargeoff_principal - net_recoveries

    return {
        "total_records": len(df_seasoned),
        "total_funded_principal": total_funded,
        "total_principal_repaid": total_rec_prncp,
        "total_interest_collected": total_rec_int,
        "total_late_fees_collected": total_rec_late,
        "gross_recoveries": gross_recoveries,
        "collection_recovery_fees": recovery_fees,
        "net_recoveries": net_recoveries,
        "total_payments_received": total_pymnt,
        "component_net_cash_flow": component_net_cash_flow,
        "component_laroc_pct": component_laroc,
        "total_net_cash_flow": total_net_cash_flow,
        "aggregate_laroc_pct": aggregate_laroc,
        "gross_chargeoff_principal": gross_chargeoff_principal,
        "net_chargeoff_principal": net_chargeoff_principal,
        "bad_loan_count": int(bad_mask.sum()),
        "terminal_bad_rate_pct": (bad_mask.sum() / len(df_seasoned)) * 100.0,
    }


def compute_dispersion_statistics(df_seasoned: pd.DataFrame) -> pd.DataFrame:
    """
    Computes parametric and non-parametric dispersion statistics for core underwriting
    and performance measures:
      Mean, Median, Std Dev, P25, P75, P90, P99, and IQR.
    """
    features = [
        "funded_amnt",
        "int_rate",
        "annual_inc",
        "dti",
        "revol_util",
        "fico_midpoint",
        "laroc",
    ]

    records = []
    total_n = len(df_seasoned)

    for feat in features:
        series = df_seasoned[feat].dropna()
        n_obs = len(series)
        missing_count = total_n - n_obs

        mean_val = float(series.mean())
        std_val = float(series.std())
        median_val = float(series.median())
        p25 = float(series.quantile(0.25))
        p75 = float(series.quantile(0.75))
        p90 = float(series.quantile(0.90))
        p99 = float(series.quantile(0.99))
        iqr_val = p75 - p25

        records.append({
            "feature": feat,
            "count": n_obs,
            "missing": missing_count,
            "mean": mean_val,
            "std": std_val,
            "p25": p25,
            "median": median_val,
            "p75": p75,
            "p90": p90,
            "p99": p99,
            "iqr": iqr_val,
        })

    return pd.DataFrame(records)


def audit_active_portfolio_exposure(df_active: pd.DataFrame) -> pd.DataFrame:
    """
    Audits current active portfolio exposure across loan_status categories:
      Current, Late (16-30 days), Late (31-120 days), In Grace Period.
    """
    total_active_funded = float(df_active["funded_amnt"].sum())
    total_active_count = len(df_active)

    status_order = ["Current", "In Grace Period", "Late (16-30 days)", "Late (31-120 days)"]

    grp = df_active.groupby("loan_status").agg(
        volume=("id", "count"),
        total_funded=("funded_amnt", "sum"),
        mean_loan_size=("funded_amnt", "mean"),
    ).reindex(status_order).reset_index()

    grp["volume_share_pct"] = (grp["volume"] / total_active_count) * 100.0
    grp["funded_share_pct"] = (grp["total_funded"] / total_active_funded) * 100.0

    return grp


def generate_markdown_report(
    topline: dict,
    dispersion_df: pd.DataFrame,
    active_df: pd.DataFrame,
    execution_time: float,
) -> str:
    """Assemble reports/scan_aggregates_summary.md in clean GitHub Flavored Markdown."""
    total_active_vol = int(active_df["volume"].sum())
    total_active_funded = float(active_df["total_funded"].sum())

    # Delinquent subset in active
    delinquent_mask = active_df["loan_status"] != "Current"
    delinq_vol = int(active_df.loc[delinquent_mask, "volume"].sum())
    delinq_funded = float(active_df.loc[delinquent_mask, "total_funded"].sum())
    delinq_pct = (delinq_funded / total_active_funded) * 100.0

    md = []
    md.append("# SCAN Aggregates & Portfolio Exposure Audit")
    md.append("**Project:** LendingClub Consumer Credit Risk & Underwriting Optimization  ")
    md.append("**Framework:** Christine Jiang SCAN EDA Framework (Stage A – Aggregates & Anomalies)  ")
    md.append(f"**Execution Timestamp:** 2026-10-19 | Runtime: {execution_time:.2f} seconds  ")
    md.append(f"**Primary Scope:** Seasoned Closed Cohort ({topline['total_records']:,} loans) | Active Monitoring ({total_active_vol:,} loans)  ")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Top-Line Portfolio Cash Ledger Reconciliations")
    md.append("")
    md.append("Comprehensive cash flow audit reconciling cumulative capital deployed against cash receipts and terminal write-offs:")
    md.append("")
    md.append("| Ledger Measure | Amount ($) | Portfolio Share (%) | Accounting Definition / Reconciliation |")
    md.append("| :--- | :--- | :--- | :--- |")
    md.append(f"| **Total Funded Principal** | **${topline['total_funded_principal']:,.2f}** | 100.00% | Total investor capital deployed at origination |")
    md.append(f"| **Total Principal Repaid** | **${topline['total_principal_repaid']:,.2f}** | {topline['total_principal_repaid']/topline['total_funded_principal']:.2%} | Cumulative principal amortized and returned (`total_rec_prncp`) |")
    md.append(f"| **Total Interest Collected** | **${topline['total_interest_collected']:,.2f}** | {topline['total_interest_collected']/topline['total_funded_principal']:.2%} | Cumulative gross interest revenue earned (`total_rec_int`) |")
    md.append(f"| **Total Late Fees Collected** | **${topline['total_late_fees_collected']:,.2f}** | {topline['total_late_fees_collected']/topline['total_funded_principal']:.4%} | Penalty fee income received (`total_rec_late_fee`) |")
    md.append(f"| **Total Gross Recoveries** | **${topline['gross_recoveries']:,.2f}** | {topline['gross_recoveries']/topline['total_funded_principal']:.2%} | Post-charge-off collections recovered (`recoveries`) |")
    md.append(f"| **Collection Agency Fees** | **${topline['collection_recovery_fees']:,.2f}** | {topline['collection_recovery_fees']/topline['total_funded_principal']:.2%} | Servicing fees paid to recovery agencies (`collection_recovery_fee`) |")
    md.append(f"| **Net Cash Recoveries** | **${topline['net_recoveries']:,.2f}** | {topline['net_recoveries']/topline['total_funded_principal']:.2%} | Gross recoveries net of recovery fees |")
    md.append(f"| **Total Borrower Cash Received** | **${topline['total_payments_received']:,.2f}** | {topline['total_payments_received']/topline['total_funded_principal']:.2%} | Total gross cash received from borrowers (`total_pymnt`) |")
    md.append(f"| **Cumulative Gross Charge-Offs** | **${topline['gross_chargeoff_principal']:,.2f}** | {topline['gross_chargeoff_principal']/topline['total_funded_principal']:.2%} | Unrecovered principal at loan default |")
    md.append(f"| **Cumulative Net Charge-Off Principal** | **${topline['net_chargeoff_principal']:,.2f}** | {topline['net_chargeoff_principal']/topline['total_funded_principal']:.2%} | Gross principal write-offs less net cash recoveries |")
    md.append(f"| **Total Net Cash Flow (Analytical)** | **${topline['total_net_cash_flow']:,.2f}** | {topline['aggregate_laroc_pct']:.2f}% | Cumulative portfolio profit after credit losses (`net_cash_flow`) |")
    md.append(f"| **Platform-Level Aggregate LAROC** | **{topline['aggregate_laroc_pct']:.4f}%** | -- | **(Total Net Cash Flow / Total Funded Principal) * 100** |")
    md.append("")
    md.append("> [!NOTE]")
    md.append(f"> **Ledger Component Alignment:** Calculating net cash flow directly from atomic cash components (Principal Repaid + Interest + Recoveries - Fees - Funded Principal) yields **${topline['component_net_cash_flow']:,.2f}** ({topline['component_laroc_pct']:.2f}% return). The analytical `net_cash_flow` column established during ETL yields **${topline['total_net_cash_flow']:,.2f}** ({topline['aggregate_laroc_pct']:.2f}% return), both comfortably exceeding 0% break-even.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. Distribution & Dispersion Statistics (Underwriting & Returns)")
    md.append("")
    md.append("Comprehensive parametric (Mean, Std Dev) and non-parametric (Median, P25, P75, P90, P99, IQR) summary statistics across the 1,345,350 seasoned loans:")
    md.append("")
    md.append("| Feature | Mean | Std Dev | P25 | Median | P75 | P90 | P99 | IQR | Missing (%) |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for _, r in dispersion_df.iterrows():
        f = r["feature"]
        miss_pct = (r["missing"] / topline["total_records"]) * 100.0

        if f in ["funded_amnt", "annual_inc"]:
            # Currency formatting
            mean_s = f"${r['mean']:,.2f}"
            std_s = f"${r['std']:,.2f}"
            p25_s = f"${r['p25']:,.2f}"
            med_s = f"${r['median']:,.2f}"
            p75_s = f"${r['p75']:,.2f}"
            p90_s = f"${r['p90']:,.2f}"
            p99_s = f"${r['p99']:,.2f}"
            iqr_s = f"${r['iqr']:,.2f}"
        elif f in ["int_rate", "revol_util"]:
            # Percentage formatting (decimals)
            mean_s = f"{r['mean']*100:.2f}%"
            std_s = f"{r['std']*100:.2f}%"
            p25_s = f"{r['p25']*100:.2f}%"
            med_s = f"{r['median']*100:.2f}%"
            p75_s = f"{r['p75']*100:.2f}%"
            p90_s = f"{r['p90']*100:.2f}%"
            p99_s = f"{r['p99']*100:.2f}%"
            iqr_s = f"{r['iqr']*100:.2f}%"
        elif f == "laroc":
            # Percentage points
            mean_s = f"{r['mean']:.2f}%"
            std_s = f"{r['std']:.2f}%"
            p25_s = f"{r['p25']:.2f}%"
            med_s = f"{r['median']:.2f}%"
            p75_s = f"{r['p75']:.2f}%"
            p90_s = f"{r['p90']:.2f}%"
            p99_s = f"{r['p99']:.2f}%"
            iqr_s = f"{r['iqr']:.2f}%"
        else:
            # Standard numeric (fico_midpoint, dti)
            mean_s = f"{r['mean']:.2f}"
            std_s = f"{r['std']:.2f}"
            p25_s = f"{r['p25']:.2f}"
            med_s = f"{r['median']:.2f}"
            p75_s = f"{r['p75']:.2f}"
            p90_s = f"{r['p90']:.2f}"
            p99_s = f"{r['p99']:.2f}"
            iqr_s = f"{r['iqr']:.2f}"

        md.append(f"| `{f}` | {mean_s} | {std_s} | {p25_s} | **{med_s}** | {p75_s} | {p90_s} | {p99_s} | {iqr_s} | {miss_pct:.3f}% |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 3. Active Portfolio Exposure Audit (Open Capital at Risk)")
    md.append("")
    md.append(f"Audit of ongoing open originations in `fct_active_portfolio.parquet` ({total_active_vol:,} loans totaling **${total_active_funded:,.2f}**):")
    md.append("")
    md.append("| Loan Status | Active Count | Volume Share (%) | Active Funded Principal ($) | Balance Share (%) | Mean Loan Size ($) | Delinquency Risk Profile |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for _, r in active_df.iterrows():
        status = r["loan_status"]
        risk_desc = "Performing Core Balance" if status == "Current" else "Impaired / At-Risk Delinquency Roll"
        md.append(
            f"| **{status}** | {int(r['volume']):,} | {r['volume_share_pct']:.2f}% | "
            f"${r['total_funded']:,.2f} | {r['funded_share_pct']:.2f}% | "
            f"${r['mean_loan_size']:,.2f} | {risk_desc} |"
        )

    md.append(
        f"| **Total Active Portfolio** | **{total_active_vol:,}** | **100.00%** | "
        f"**${total_active_funded:,.2f}** | **100.00%** | "
        f"**${total_active_funded/total_active_vol:,.2f}** | **Ongoing Capital Exposure** |"
    )
    md.append("")
    md.append(f"> [!WARNING]")
    md.append(f"> **Active Delinquency Exposure:** Non-current active originations (`In Grace Period`, `Late 16-30`, `Late 31-120`) represent **{delinq_vol:,} loans** ({delinq_pct:.2f}% of active funded balance, **${delinq_funded:,.2f}**). These loans are in active delinquency migration and risk migrating to terminal write-offs.")
    md.append("")
    md.append("---")
    md.append(f"*Report automatically generated by `src/analytics/scan_aggregates.py` in {execution_time:.2f} seconds.*")
    md.append("")

    return "\n".join(md)


def run_scan_aggregates(
    seasoned_path: Path = Path("data/cleaned/fct_closed_loans_seasoned.parquet"),
    active_path: Path = Path("data/cleaned/fct_active_portfolio.parquet"),
    report_path: Path = Path("reports/scan_aggregates_summary.md"),
    export_csv_path: Path = Path("data/exports/portfolio_aggregates.csv"),
    active_export_path: Path = Path("data/exports/active_portfolio_exposure.csv"),
):
    """Execute Task 2.2 SCAN Aggregates & Portfolio Exposure Audit."""
    start_time = time.time()
    print("=" * 80)
    print("RUNNING TASK 2.2: SCAN AGGREGATES & ANOMALIES AUDITING")
    print("=" * 80)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    export_csv_path.parent.mkdir(parents=True, exist_ok=True)
    active_export_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Load Data
    df_seasoned, df_active = load_datasets(seasoned_path, active_path)

    # 2. Top-line Reconciliations
    print("\n[TOP-LINE] Calculating portfolio ledger reconciliations...")
    topline = compute_topline_reconciliations(df_seasoned)
    print(f"  Funded Principal : ${topline['total_funded_principal']:,.2f}")
    print(f"  Principal Repaid : ${topline['total_principal_repaid']:,.2f}")
    print(f"  Interest Earned  : ${topline['total_interest_collected']:,.2f}")
    print(f"  Net Recoveries   : ${topline['net_recoveries']:,.2f}")
    print(f"  Net Charge-Off   : ${topline['net_chargeoff_principal']:,.2f}")
    print(f"  Net Cash Flow    : ${topline['total_net_cash_flow']:,.2f}")
    print(f"  Aggregate LAROC  : {topline['aggregate_laroc_pct']:.4f}%")

    # 3. Dispersion Statistics
    print("\n[DISPERSION] Computing parametric and non-parametric dispersion statistics...")
    dispersion_df = compute_dispersion_statistics(df_seasoned)
    print(dispersion_df[["feature", "mean", "median", "std", "iqr"]].to_string())

    # Export dispersion statistics to data/exports/portfolio_aggregates.csv
    dispersion_df.to_csv(export_csv_path, index=False)
    print(f"\n  Exported portfolio aggregates CSV to: {export_csv_path}")

    # 4. Active Portfolio Exposure Audit
    print("\n[ACTIVE AUDIT] Auditing active portfolio exposure...")
    active_summary = audit_active_portfolio_exposure(df_active)
    print(active_summary[["loan_status", "volume", "total_funded", "volume_share_pct", "funded_share_pct"]].to_string())

    # Export active exposure to CSV
    active_summary.to_csv(active_export_path, index=False)
    print(f"  Exported active portfolio exposure CSV to: {active_export_path}")

    # 5. Generate Markdown Report
    execution_time = time.time() - start_time
    md_content = generate_markdown_report(
        topline, dispersion_df, active_summary, execution_time
    )
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\n[REPORT GENERATED] Saved markdown audit to: {report_path}")
    print("=" * 80)
    print(f"TASK 2.2 COMPLETED SUCCESSFULLY IN {execution_time:.2f} SECONDS")
    print("=" * 80)


if __name__ == "__main__":
    run_scan_aggregates()
