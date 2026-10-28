"""
Stage N Analytics Pipeline: Notable Segments & Multi-Dimensional Slicing.
Implements Christine Jiang's SCAN methodology for bank marketing outbound campaigns.
Profiles multi-dimensional performance across channel, demographics, prior campaign history,
macroeconomic regimes, and financial credit/balance benchmarks.
Strictly quarantines post-call duration leakage.
"""

from pathlib import Path
import pandas as pd
import numpy as np

DATA_CLEANED_DIR = Path("data/cleaned")
PRECALL_PARQUET_FILE = DATA_CLEANED_DIR / "fct_campaign_precall_targeting.parquet"
BENCHMARK_PARQUET_FILE = DATA_CLEANED_DIR / "fct_legacy_balance_benchmark.parquet"
EXPORTS_DIR = Path("data/exports")
REPORTS_DIR = Path("reports")

BASELINE_CONV_RATE = 4640 / 41188 * 100.0  # 11.265417%
TOTAL_PORTFOLIO_LEADS = 41188
TOTAL_PORTFOLIO_CALLS = 105754
TOTAL_PORTFOLIO_SUBS = 4640


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads precall targeting and legacy benchmark datasets with strict leakage checks.
    """
    assert PRECALL_PARQUET_FILE.is_file(), f"Missing {PRECALL_PARQUET_FILE}"
    assert BENCHMARK_PARQUET_FILE.is_file(), f"Missing {BENCHMARK_PARQUET_FILE}"

    df_pre = pd.read_parquet(PRECALL_PARQUET_FILE)
    df_bench = pd.read_parquet(BENCHMARK_PARQUET_FILE)

    # Quarantine validation
    assert "duration" not in df_pre.columns, "Leakage: duration found in precall targeting table!"
    assert "duration_minutes" not in df_pre.columns, "Leakage: duration_minutes found in precall targeting table!"
    assert len(df_pre) == TOTAL_PORTFOLIO_LEADS, f"Expected {TOTAL_PORTFOLIO_LEADS} leads, got {len(df_pre)}"

    return df_pre, df_bench


def build_segment_table(
    df: pd.DataFrame,
    dim_name: str,
    group_cols: str | list[str],
    total_leads: int = TOTAL_PORTFOLIO_LEADS,
    total_calls: int = TOTAL_PORTFOLIO_CALLS,
    total_subs: int = TOTAL_PORTFOLIO_SUBS,
    baseline_conv_rate: float = BASELINE_CONV_RATE,
    sort_by_conv: bool = False,
) -> pd.DataFrame:
    """
    Computes standard 9 metrics for any 1D or 2D segmentation breakdown:
    lead_count, lead_share_pct, total_calls, call_share_pct, subscriptions,
    sub_share_pct, conversion_rate_pct, dialing_efficiency_pct, relative_lift_vs_baseline.
    """
    if isinstance(group_cols, list):
        grouped = df.groupby(group_cols, observed=True).agg(
            lead_count=("is_subscribed", "count"),
            total_calls=("campaign", "sum"),
            subscriptions=("is_subscribed", "sum"),
        ).reset_index()
        grouped["segment_value"] = grouped[group_cols].astype(str).agg(" | ".join, axis=1)
    else:
        grouped = df.groupby(group_cols, observed=True).agg(
            lead_count=("is_subscribed", "count"),
            total_calls=("campaign", "sum"),
            subscriptions=("is_subscribed", "sum"),
        ).reset_index()
        grouped["segment_value"] = grouped[group_cols].astype(str)

    grouped["segment_dimension"] = dim_name
    grouped["lead_share_pct"] = (grouped["lead_count"] / total_leads) * 100.0
    grouped["call_share_pct"] = (grouped["total_calls"] / total_calls) * 100.0
    grouped["sub_share_pct"] = (grouped["subscriptions"] / total_subs) * 100.0
    grouped["conversion_rate_pct"] = (grouped["subscriptions"] / grouped["lead_count"]) * 100.0
    grouped["dialing_efficiency_pct"] = (grouped["subscriptions"] / grouped["total_calls"]) * 100.0
    grouped["relative_lift_vs_baseline"] = grouped["conversion_rate_pct"] / baseline_conv_rate

    if sort_by_conv:
        grouped = grouped.sort_values("conversion_rate_pct", ascending=False).reset_index(drop=True)

    cols = [
        "segment_dimension",
        "segment_value",
        "lead_count",
        "lead_share_pct",
        "total_calls",
        "call_share_pct",
        "subscriptions",
        "sub_share_pct",
        "conversion_rate_pct",
        "dialing_efficiency_pct",
        "relative_lift_vs_baseline",
    ]
    return grouped[cols]


def generate_channel_dimension(df_pre: pd.DataFrame) -> pd.DataFrame:
    """
    Dimension 1: Contact Channel & Touch Interaction.
    """
    t_1d = build_segment_table(df_pre, "contact", "contact")
    t_2d = build_segment_table(df_pre, "contact_x_campaign_touch_tier", ["contact", "campaign_touch_tier"])
    return pd.concat([t_1d, t_2d], ignore_index=True)


def generate_demographics_dimension(df_pre: pd.DataFrame) -> pd.DataFrame:
    """
    Dimension 2: Demographics & Socio-Economic Tiers.
    """
    t_age = build_segment_table(df_pre, "age_bucket", "age_bucket")
    t_collar = build_segment_table(df_pre, "job_collar_tier", "job_collar_tier")
    t_job = build_segment_table(df_pre, "job", "job", sort_by_conv=True)
    t_edu = build_segment_table(df_pre, "education", "education", sort_by_conv=True)
    t_mar = build_segment_table(df_pre, "marital", "marital", sort_by_conv=True)
    t_2d = build_segment_table(df_pre, "age_bucket_x_job_collar_tier", ["age_bucket", "job_collar_tier"], sort_by_conv=True)

    return pd.concat([t_age, t_collar, t_job, t_edu, t_mar, t_2d], ignore_index=True)


def generate_poutcome_dimension(df_pre: pd.DataFrame) -> pd.DataFrame:
    """
    Dimension 3: Prior Campaign History & Recency.
    """
    t_pout = build_segment_table(df_pre, "poutcome", "poutcome")
    t_prev = build_segment_table(df_pre, "was_previously_contacted", "was_previously_contacted")
    t_rec = build_segment_table(df_pre, "prior_contact_recency_tier", "prior_contact_recency_tier")

    return pd.concat([t_pout, t_prev, t_rec], ignore_index=True)


def generate_macro_dimension(df_pre: pd.DataFrame) -> pd.DataFrame:
    """
    Dimension 4: Macroeconomic Regimes & Seasonality.
    """
    t_eur = build_segment_table(df_pre, "euribor_regime", "euribor_regime")
    t_2d_contact = build_segment_table(df_pre, "euribor_regime_x_contact", ["euribor_regime", "contact"])
    t_2d_age = build_segment_table(df_pre, "euribor_regime_x_age_bucket", ["euribor_regime", "age_bucket"])
    t_month = build_segment_table(df_pre, "month", "month")
    t_dow = build_segment_table(df_pre, "day_of_week", "day_of_week")

    return pd.concat([t_eur, t_2d_contact, t_2d_age, t_month, t_dow], ignore_index=True)


def generate_financial_profile_dimension(df_pre: pd.DataFrame, df_bench: pd.DataFrame) -> pd.DataFrame:
    """
    Dimension 5: Credit Obligations & Legacy Balance Benchmark.
    """
    t_def = build_segment_table(df_pre, "default", "default")
    t_house = build_segment_table(df_pre, "housing", "housing")
    t_loan = build_segment_table(df_pre, "loan", "loan")

    # Benchmark dataset computations
    bench_leads = len(df_bench)
    bench_calls = int(df_bench["campaign"].sum())
    bench_subs = int(df_bench["is_subscribed"].sum())
    bench_conv_rate = (bench_subs / bench_leads) * 100.0  # 11.6985%

    t_hbal = build_segment_table(
        df_bench,
        "high_balance_flag",
        "high_balance_flag",
        total_leads=bench_leads,
        total_calls=bench_calls,
        total_subs=bench_subs,
        baseline_conv_rate=bench_conv_rate,
    )

    df_bench_copy = df_bench.copy()
    df_bench_copy["balance_quartile"] = pd.qcut(
        df_bench_copy["balance"],
        4,
        labels=["Q1 (Low)", "Q2 (Mid-Low)", "Q3 (Mid-High)", "Q4 (High)"],
    )

    t_bq = build_segment_table(
        df_bench_copy,
        "balance_quartile",
        "balance_quartile",
        total_leads=bench_leads,
        total_calls=bench_calls,
        total_subs=bench_subs,
        baseline_conv_rate=bench_conv_rate,
    )

    return pd.concat([t_def, t_house, t_loan, t_hbal, t_bq], ignore_index=True)


def generate_notable_segments_report(
    channel_df: pd.DataFrame,
    demographics_df: pd.DataFrame,
    poutcome_df: pd.DataFrame,
    macro_df: pd.DataFrame,
    financial_df: pd.DataFrame,
) -> str:
    """
    Generates markdown report for Stage N notable segments narrative. Strictly avoids em dashes.
    """
    lines = []
    lines.append("# Stage N Audit Report: Notable Segments & Multi-Dimensional Slicing")
    lines.append("")
    lines.append("## Executive Strategic Summary")
    lines.append("Analysis across the 5 core customer and operational dimensions reveals massive performance disparities across channels, demographics, prior relationship history, macroeconomic conditions, and financial health.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Dimension 1: Contact Channel & Outreach Tier Interaction")
    lines.append("Channel selection acts as a foundational efficiency multiplier. Cellular outreach generates 2.82x higher conversion rate than fixed telephone.")
    lines.append("")
    lines.append("| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for _, r in channel_df.iterrows():
        lines.append(
            f"| `{r['segment_dimension']}` | {r['segment_value']} | {int(r['lead_count']):,} | "
            f"{r['lead_share_pct']:.2f}% | {int(r['total_calls']):,} | {int(r['subscriptions']):,} | "
            f"{r['conversion_rate_pct']:.2f}% | {r['dialing_efficiency_pct']:.2f}% | {r['relative_lift_vs_baseline']:.2f}x |"
        )
    lines.append("")
    lines.append("### Strategic Channel Insights")
    lines.append("- Cellular Multiplier: Cellular leads convert at 14.74% with 6.13% dialing efficiency, whereas landline telephone leads convert at 5.23% with 1.84% dialing efficiency (2.82x conversion multiplier).")
    lines.append("- Channel and Fatigue Compounding: In the Fatigue Zone (6+ touches), cellular conversion falls to 6.53% (0.72% dialing efficiency), while landline telephone collapses to 4.29% (0.42% dialing efficiency).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Dimension 2: Demographics, Occupational Collars & Slicing")
    lines.append("Demographic lifecycle positioning is the single strongest prospect-level determinant of term deposit acquisition.")
    lines.append("")
    lines.append("| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for _, r in demographics_df.iterrows():
        lines.append(
            f"| `{r['segment_dimension']}` | {r['segment_value']} | {int(r['lead_count']):,} | "
            f"{r['lead_share_pct']:.2f}% | {int(r['total_calls']):,} | {int(r['subscriptions']):,} | "
            f"{r['conversion_rate_pct']:.2f}% | {r['dialing_efficiency_pct']:.2f}% | {r['relative_lift_vs_baseline']:.2f}x |"
        )
    lines.append("")
    lines.append("### Key Demographic Findings")
    lines.append("- Senior/Retired Surge: Prospects aged 60+ convert at 45.49% (4.04x baseline lift) with 23.13% dialing efficiency. Retired clients have accumulated liquid capital and prioritize guaranteed interest income.")
    lines.append("- The Core Working 31-45 Trap: The core working segment comprises 53.35% of all evaluated prospects (21,974 leads) and 53.12% of dialed calls (56,174 calls), yet converts at an anemic 9.37% (0.83x baseline lift).")
    lines.append("- Occupational Extremes: Students (31.43% conv) and retired clients (25.23% conv) dominate acquisition efficiency, while blue-collar workers (6.89% conv) and service workers (8.14% conv) absorb massive calling capacity with minimal yield.")
    lines.append("- High-Yield 2D Pockets: Cross-tabulating `age_bucket` x `job_collar_tier` reveals that `Senior/Retired (60+)` White-Collar prospects achieve 51.06% conversion, while `Core Working (31-45)` Blue-Collar workers yield only 8.10% across 11,993 prospects.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Dimension 3: Prior Campaign History & Recency")
    lines.append("Historical outreach success is the highest single predictive affinity signal in direct marketing.")
    lines.append("")
    lines.append("| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for _, r in poutcome_df.iterrows():
        lines.append(
            f"| `{r['segment_dimension']}` | {r['segment_value']} | {int(r['lead_count']):,} | "
            f"{r['lead_share_pct']:.2f}% | {int(r['total_calls']):,} | {int(r['subscriptions']):,} | "
            f"{r['conversion_rate_pct']:.2f}% | {r['dialing_efficiency_pct']:.2f}% | {r['relative_lift_vs_baseline']:.2f}x |"
        )
    lines.append("")
    lines.append("### Prior Outreach Insights")
    lines.append("- Prior Campaign Success (`poutcome == 'success'`): Converts at an extraordinary 65.11% (5.78x baseline lift) with 36.00% dialing efficiency across 1,373 prospects.")
    lines.append("- Past Contact Multiplier: Previously contacted leads convert at 52.48% (4.66x lift) vs. 9.69% for never-contacted prospects.")
    lines.append("- Recency Window: Prospects contacted within 7 days convert at 64.06% (5.69x lift), with conversion tapering to 29.03% for cool outreach beyond 15 days.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Dimension 4: Macroeconomic Regimes & Seasonality")
    lines.append("Macroeconomic monetary climate creates massive macro-elasticity shifts in consumer willingness to lock funds into term deposits.")
    lines.append("")
    lines.append("| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for _, r in macro_df.iterrows():
        lines.append(
            f"| `{r['segment_dimension']}` | {r['segment_value']} | {int(r['lead_count']):,} | "
            f"{r['lead_share_pct']:.2f}% | {int(r['total_calls']):,} | {int(r['subscriptions']):,} | "
            f"{r['conversion_rate_pct']:.2f}% | {r['dialing_efficiency_pct']:.2f}% | {r['relative_lift_vs_baseline']:.2f}x |"
        )
    lines.append("")
    lines.append("### Macroeconomic Elasticity Insights")
    lines.append("- Interest Rate Elasticity: In the Low Rate Regime (Euribor <= 3.0%), conversion rate surges to 24.46% (2.17x lift, 11.69% dialing efficiency) compared to just 4.84% in the High Rate Regime (Euribor > 3.0%). This represents a 5.06x elasticity multiplier.")
    lines.append("- High Rate Headwind: During high interest rate environments (e.g. 2008), 27,690 prospects received 77,513 calls to yield only 1,339 subscriptions (1.73% dialing efficiency).")
    lines.append("- Seasonal Disparities: March (50.55%), December (48.91%), September (44.91%), and October (43.87%) exhibit high-yield conversion windows, while May (6.45%) and July (9.04%) suffer from call fatigue and low conversion.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Dimension 5: Credit Obligations & Legacy Balance Benchmark")
    lines.append("Existing debt obligations suppress term deposit uptake, while liquid account balance is a positive indicator.")
    lines.append("")
    lines.append("| Segment Dimension | Segment Value | Leads | Lead Share (%) | Dialed Calls | Subscriptions | Conv Rate (%) | Dialing Eff (%) | Lift vs. Baseline |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for _, r in financial_df.iterrows():
        lines.append(
            f"| `{r['segment_dimension']}` | {r['segment_value']} | {int(r['lead_count']):,} | "
            f"{r['lead_share_pct']:.2f}% | {int(r['total_calls']):,} | {int(r['subscriptions']):,} | "
            f"{r['conversion_rate_pct']:.2f}% | {r['dialing_efficiency_pct']:.2f}% | {r['relative_lift_vs_baseline']:.2f}x |"
        )
    lines.append("")
    lines.append("### Credit & Balance Benchmark Insights")
    lines.append("- Credit Default Disqualification: Prospects with credit default in record have 0.00% conversion (0 subscriptions out of 3 leads). Unknown default status converts at 5.15% vs. 12.88% for confirmed no-default prospects.")
    lines.append("- Legacy Balance Ladder: In the benchmark dataset, prospects in Q4 Balance (> 1,428 EUR) convert at 16.15% (6.11% dialing efficiency) vs. 7.24% in Q1 Balance (<= 72 EUR). Prospects with high balance (> 448 EUR median) convert at 14.33% vs. 9.06% for low balance (1.58x balance multiplier).")
    lines.append("")

    return "\n".join(lines)


def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Executing Task 2.3: N Analytics Pipeline...")
    df_pre, df_bench = load_datasets()

    # Dimension 1: Channel
    channel_df = generate_channel_dimension(df_pre)
    channel_csv_path = EXPORTS_DIR / "segment_channel.csv"
    channel_df.to_csv(channel_csv_path, index=False)
    print(f"Exported segment channel table: {channel_csv_path} ({len(channel_df)} rows)")

    # Dimension 2: Demographics
    demographics_df = generate_demographics_dimension(df_pre)
    demographics_csv_path = EXPORTS_DIR / "segment_demographics.csv"
    demographics_df.to_csv(demographics_csv_path, index=False)
    print(f"Exported segment demographics table: {demographics_csv_path} ({len(demographics_df)} rows)")

    # Dimension 3: Prior History
    poutcome_df = generate_poutcome_dimension(df_pre)
    poutcome_csv_path = EXPORTS_DIR / "segment_poutcome.csv"
    poutcome_df.to_csv(poutcome_csv_path, index=False)
    print(f"Exported segment prior outcome table: {poutcome_csv_path} ({len(poutcome_df)} rows)")

    # Dimension 4: Macroeconomic
    macro_df = generate_macro_dimension(df_pre)
    macro_csv_path = EXPORTS_DIR / "segment_macro.csv"
    macro_df.to_csv(macro_csv_path, index=False)
    print(f"Exported segment macro table: {macro_csv_path} ({len(macro_df)} rows)")

    # Dimension 5: Financial Profile & Legacy Benchmark
    financial_df = generate_financial_profile_dimension(df_pre, df_bench)
    financial_csv_path = EXPORTS_DIR / "segment_financial_profile.csv"
    financial_df.to_csv(financial_csv_path, index=False)
    print(f"Exported segment financial profile table: {financial_csv_path} ({len(financial_df)} rows)")

    # Comprehensive Markdown Narrative Report
    report_content = generate_notable_segments_report(
        channel_df, demographics_df, poutcome_df, macro_df, financial_df
    )
    report_path = REPORTS_DIR / "notable_segments_summary.md"
    report_path.write_text(report_content, encoding="utf-8")
    print(f"Exported notable segments summary report: {report_path}")

    # Console Summary
    cell_row = channel_df[channel_df["segment_value"] == "cellular"].iloc[0]
    tel_row = channel_df[channel_df["segment_value"] == "telephone"].iloc[0]
    senior_row = demographics_df[demographics_df["segment_value"] == "4. Senior/Retired (60+)"].iloc[0]
    core_row = demographics_df[demographics_df["segment_value"] == "2. Core Working (31-45)"].iloc[0]
    succ_row = poutcome_df[poutcome_df["segment_value"] == "success"].iloc[0]
    low_rate_row = macro_df[macro_df["segment_value"] == "Low Rate Regime (Euribor <= 3.0%)"].iloc[0]
    high_rate_row = macro_df[macro_df["segment_value"] == "High Rate Regime (Euribor > 3.0%)"].iloc[0]

    print("\n--- N AUDIT VERIFICATION SUMMARY ---")
    print(f"Channel Multiplier:    Cellular ({cell_row['conversion_rate_pct']:.2f}%) vs. Telephone ({tel_row['conversion_rate_pct']:.2f}%) -> {cell_row['conversion_rate_pct'] / tel_row['conversion_rate_pct']:.2f}x lift")
    print(f"Demographic Lift:      Senior/Retired 60+ ({senior_row['conversion_rate_pct']:.2f}%) vs. Core Working 31-45 ({core_row['conversion_rate_pct']:.2f}%)")
    print(f"Prior Outcome Surge:   Success ({succ_row['conversion_rate_pct']:.2f}%) with {succ_row['dialing_efficiency_pct']:.2f}% dialing efficiency")
    print(f"Macro Elasticity:      Low Rate ({low_rate_row['conversion_rate_pct']:.2f}%) vs. High Rate ({high_rate_row['conversion_rate_pct']:.2f}%) -> {low_rate_row['conversion_rate_pct'] / high_rate_row['conversion_rate_pct']:.2f}x elasticity")
    print("------------------------------------\n")


if __name__ == "__main__":
    main()
