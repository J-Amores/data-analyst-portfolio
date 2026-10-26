"""
src/presentation/export_cockpit_data.py
Consumer Credit Risk & Underwriting Optimization
Export Real Empirical Cube and Lookup Tables for Interactive Cockpit

Aggregates 1,345,350 seasoned closed loans into:
  1. 3D Policy Cube (grade x dti_bracket x revol_util_bracket)
  2. 16-Cell Risk Grid (dti_bracket x revol_util_bracket)
  3. Subgrade Lookup Table (A1 through G5)
  4. Term & Purpose Summary (36m/60m and top loan purposes)
  5. Baseline Portfolio Totals and Guardrail Metrics

Outputs:
  data/exports/cockpit_cube.json

Guardrail Compliance: Zero em dashes, zero en dashes.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import pyarrow.dataset as ds


def export_cockpit_cube():
    print("[TASK] Loading data/cleaned/fct_closed_loans_seasoned.parquet...")
    parquet_path = Path("data/cleaned/fct_closed_loans_seasoned.parquet")
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    dataset = ds.dataset(str(parquet_path), format="parquet")
    cols = [
        "grade",
        "sub_grade",
        "dti_bracket",
        "revol_util_bracket",
        "term",
        "purpose",
        "fico_midpoint",
        "funded_amnt",
        "int_rate",
        "is_bad_loan",
        "net_cash_flow",
        "total_rec_prncp",
        "recoveries",
        "collection_recovery_fee",
    ]
    df = dataset.to_table(columns=cols).to_pandas()

    print(f"[TASK] Read {len(df):,} seasoned loans. Calculating loss dimensions...")

    # Accurate gross and net charge-off losses
    df["gross_loss"] = np.where(
        df["is_bad_loan"] == 1,
        df["funded_amnt"] - df["total_rec_prncp"],
        0.0,
    )
    df["net_loss"] = np.where(
        df["is_bad_loan"] == 1,
        df["funded_amnt"] - df["total_rec_prncp"] - df["recoveries"] + df["collection_recovery_fee"],
        0.0,
    )

    # 1. Baseline Portfolio Metrics (exact whole book: 1,345,350 loans)
    total_loans = int(len(df))
    total_funded = float(df["funded_amnt"].sum())
    total_bad_loans = int(df["is_bad_loan"].sum())
    baseline_bad_rate_pct = float((total_bad_loans / total_loans) * 100.0)
    baseline_net_cash_flow = float(df["net_cash_flow"].sum())
    baseline_net_laroc_pct = float((baseline_net_cash_flow / total_funded) * 100.0)
    baseline_gross_loss = float(df["gross_loss"].sum())
    baseline_net_loss = float(df["net_loss"].sum())

    subprime_df = df[df["grade"].isin(["D", "E", "F", "G"])]
    subprime_loan_count = int(len(subprime_df))
    subprime_funded = float(subprime_df["funded_amnt"].sum())
    subprime_net_loss = float(subprime_df["net_loss"].sum())

    c4_df = df[df["sub_grade"] == "C4"]
    c4_loan_count = int(len(c4_df))
    c4_funded = float(c4_df["funded_amnt"].sum())
    c4_bad_rate_pct = float((c4_df["is_bad_loan"].sum() / c4_loan_count) * 100.0)
    c4_net_laroc_pct = float((c4_df["net_cash_flow"].sum() / c4_funded) * 100.0)
    c4_avg_int_rate = float(c4_df["int_rate"].mean())

    # Recommended Policy verification (Grades D-G, DTI > 25%, Card Usage > 65%)
    rec_decline_mask = (
        df["grade"].isin(["D", "E", "F", "G"])
        & df["dti_bracket"].isin(["3. High (25-35%)", "4. Severe (>35%)"])
        & df["revol_util_bracket"].isin(["3. High (65-85%)", "4. Maxed (>85%)"])
    )
    rec_declined_df = df[rec_decline_mask]
    rec_declined_count = int(len(rec_declined_df))
    rec_avoided_defaults = int(rec_declined_df["is_bad_loan"].sum())
    rec_declined_funded = float(rec_declined_df["funded_amnt"].sum())
    rec_gross_saved = float(rec_declined_df["gross_loss"].sum())
    rec_net_saved = float(rec_declined_df["net_loss"].sum())

    print(f"  Verified Recommended Hard-Stop: {rec_declined_count:,} loans declined, {rec_avoided_defaults:,} defaults avoided, ${rec_net_saved/1e6:.2f}M net losses saved.")

    # 2. 3D Policy Cube (grade x dti_bracket x revol_util_bracket)
    # We clean null brackets for grid aggregations
    cube_df = df.dropna(subset=["dti_bracket", "revol_util_bracket"])
    cube_grp = (
        cube_df.groupby(["grade", "dti_bracket", "revol_util_bracket"], observed=True)
        .agg(
            loan_count=("funded_amnt", "count"),
            bad_loan_count=("is_bad_loan", "sum"),
            funded_amnt_sum=("funded_amnt", "sum"),
            net_cash_flow_sum=("net_cash_flow", "sum"),
            gross_loss_sum=("gross_loss", "sum"),
            net_loss_sum=("net_loss", "sum"),
        )
        .reset_index()
    )

    cube_records = []
    for _, row in cube_grp.iterrows():
        cube_records.append({
            "grade": str(row["grade"]),
            "dti_bracket": str(row["dti_bracket"]),
            "revol_util_bracket": str(row["revol_util_bracket"]),
            "loan_count": int(row["loan_count"]),
            "bad_loan_count": int(row["bad_loan_count"]),
            "funded_amnt_sum": round(float(row["funded_amnt_sum"]), 2),
            "net_cash_flow_sum": round(float(row["net_cash_flow_sum"]), 2),
            "gross_loss_sum": round(float(row["gross_loss_sum"]), 2),
            "net_loss_sum": round(float(row["net_loss_sum"]), 2),
        })

    # 3. 16-Cell Risk Grid (Portfolio-wide across DTI and Card Usage)
    grid_grp = (
        cube_df.groupby(["dti_bracket", "revol_util_bracket"], observed=True)
        .agg(
            loan_count=("funded_amnt", "count"),
            bad_loan_count=("is_bad_loan", "sum"),
            funded_amnt_sum=("funded_amnt", "sum"),
            net_cash_flow_sum=("net_cash_flow", "sum"),
            gross_loss_sum=("gross_loss", "sum"),
            net_loss_sum=("net_loss", "sum"),
        )
        .reset_index()
    )

    grid_16 = []
    for _, row in grid_grp.iterrows():
        vol = int(row["loan_count"])
        bad = int(row["bad_loan_count"])
        fnd = float(row["funded_amnt_sum"])
        ncf = float(row["net_cash_flow_sum"])
        grid_16.append({
            "dti_bracket": str(row["dti_bracket"]),
            "revol_util_bracket": str(row["revol_util_bracket"]),
            "loan_count": vol,
            "bad_loan_count": bad,
            "bad_rate_pct": round((bad / vol) * 100.0, 2) if vol > 0 else 0.0,
            "funded_amnt_sum": round(fnd, 2),
            "net_cash_flow_sum": round(ncf, 2),
            "net_laroc_pct": round((ncf / fnd) * 100.0, 2) if fnd > 0 else 0.0,
            "gross_loss_sum": round(float(row["gross_loss_sum"]), 2),
            "net_loss_sum": round(float(row["net_loss_sum"]), 2),
        })

    # 4. Subgrade Lookup Table (A1 to G5, ordered)
    subgrades = [f"{g}{n}" for g in ["A", "B", "C", "D", "E", "F", "G"] for n in range(1, 6)]
    sub_grp = (
        df.groupby("sub_grade", observed=True)
        .agg(
            loan_count=("funded_amnt", "count"),
            funded_amnt_sum=("funded_amnt", "sum"),
            avg_int_rate=("int_rate", "mean"),
            bad_count=("is_bad_loan", "sum"),
            net_cf_sum=("net_cash_flow", "sum"),
        )
        .reset_index()
    )
    sub_lookup = {}
    for _, row in sub_grp.iterrows():
        sg = str(row["sub_grade"])
        vol = int(row["loan_count"])
        fnd = float(row["funded_amnt_sum"])
        bad = int(row["bad_count"])
        ncf = float(row["net_cf_sum"])
        sub_lookup[sg] = {
            "sub_grade": sg,
            "loan_count": vol,
            "funded_amnt_sum": round(fnd, 2),
            "avg_int_rate": round(float(row["avg_int_rate"]) * 100.0, 2),
            "bad_rate_pct": round((bad / vol) * 100.0, 2) if vol > 0 else 0.0,
            "net_laroc_pct": round((ncf / fnd) * 100.0, 2) if fnd > 0 else 0.0,
        }

    subgrade_list = [sub_lookup[sg] for sg in subgrades if sg in sub_lookup]

    # 5. Term Summary (36m vs 60m)
    term_grp = (
        df.groupby("term", observed=True)
        .agg(
            loan_count=("funded_amnt", "count"),
            funded_amnt_sum=("funded_amnt", "sum"),
            avg_int_rate=("int_rate", "mean"),
            bad_count=("is_bad_loan", "sum"),
            net_cf_sum=("net_cash_flow", "sum"),
        )
        .reset_index()
    )
    terms_dict = {}
    for _, row in term_grp.iterrows():
        t = str(int(row["term"]))
        vol = int(row["loan_count"])
        fnd = float(row["funded_amnt_sum"])
        bad = int(row["bad_count"])
        ncf = float(row["net_cf_sum"])
        terms_dict[t] = {
            "term_months": int(t),
            "loan_count": vol,
            "funded_amnt_sum": round(fnd, 2),
            "avg_int_rate": round(float(row["avg_int_rate"]) * 100.0, 2),
            "bad_rate_pct": round((bad / vol) * 100.0, 2),
            "net_laroc_pct": round((ncf / fnd) * 100.0, 2),
        }

    # 6. Purpose Summary (top loan purposes)
    major_purposes = [
        "debt_consolidation",
        "credit_card",
        "home_improvement",
        "small_business",
        "major_purchase",
        "other",
    ]
    purp_grp = (
        df.groupby("purpose", observed=True)
        .agg(
            loan_count=("funded_amnt", "count"),
            funded_amnt_sum=("funded_amnt", "sum"),
            avg_int_rate=("int_rate", "mean"),
            bad_count=("is_bad_loan", "sum"),
            net_cf_sum=("net_cash_flow", "sum"),
        )
        .reset_index()
    )
    purp_dict = {}
    for _, row in purp_grp.iterrows():
        p = str(row["purpose"])
        if p in major_purposes:
            vol = int(row["loan_count"])
            fnd = float(row["funded_amnt_sum"])
            bad = int(row["bad_count"])
            ncf = float(row["net_cf_sum"])
            purp_dict[p] = {
                "purpose": p,
                "loan_count": vol,
                "funded_amnt_sum": round(fnd, 2),
                "avg_int_rate": round(float(row["avg_int_rate"]) * 100.0, 2),
                "bad_rate_pct": round((bad / vol) * 100.0, 2),
                "net_laroc_pct": round((ncf / fnd) * 100.0, 2),
            }

    # 7. FICO Score Bands Summary
    fico_bins = [0, 659, 679, 699, 719, 749, 850]
    fico_labels = [
        "< 660",
        "660-679",
        "680-699",
        "700-719",
        "720-749",
        "750+",
    ]
    df["fico_band"] = pd.cut(df["fico_midpoint"], bins=fico_bins, labels=fico_labels)
    fico_grp = (
        df.groupby("fico_band", observed=True)
        .agg(
            loan_count=("funded_amnt", "count"),
            bad_count=("is_bad_loan", "sum"),
            funded_sum=("funded_amnt", "sum"),
            ncf_sum=("net_cash_flow", "sum"),
            avg_int_rate=("int_rate", "mean"),
        )
        .reset_index()
    )
    fico_list = []
    for _, row in fico_grp.iterrows():
        fb = str(row["fico_band"])
        vol = int(row["loan_count"])
        fnd = float(row["funded_sum"])
        bad = int(row["bad_count"])
        ncf = float(row["ncf_sum"])
        fico_list.append({
            "band": fb,
            "loan_count": vol,
            "pct_of_portfolio": round((vol / total_loans) * 100.0, 2),
            "funded_amnt_sum": round(fnd, 2),
            "bad_rate_pct": round((bad / vol) * 100.0, 2) if vol > 0 else 0.0,
            "net_laroc_pct": round((ncf / fnd) * 100.0, 2) if fnd > 0 else 0.0,
            "avg_int_rate": round(float(row["avg_int_rate"]) * 100.0, 2),
        })

    cockpit_data = {
        "metadata": {
            "dataset": "data/cleaned/fct_closed_loans_seasoned.parquet",
            "total_loans": total_loans,
            "total_funded_dollars": round(total_funded, 2),
            "total_bad_loans": total_bad_loans,
            "baseline_bad_rate_pct": round(baseline_bad_rate_pct, 4),
            "baseline_net_cash_flow": round(baseline_net_cash_flow, 2),
            "baseline_net_laroc_pct": round(baseline_net_laroc_pct, 4),
            "baseline_gross_loss_dollars": round(baseline_gross_loss, 2),
            "baseline_net_loss_dollars": round(baseline_net_loss, 2),
            "subprime_loan_count": subprime_loan_count,
            "subprime_funded_dollars": round(subprime_funded, 2),
            "subprime_net_loss_dollars": round(subprime_net_loss, 2),
            "c4_loan_count": c4_loan_count,
            "c4_funded_dollars": round(c4_funded, 2),
            "c4_bad_rate_pct": round(c4_bad_rate_pct, 4),
            "c4_net_laroc_pct": round(c4_net_laroc_pct, 4),
            "c4_avg_int_rate": round(c4_avg_int_rate * 100.0, 2),
            "recommended_declined_loans": rec_declined_count,
            "recommended_avoided_defaults": rec_avoided_defaults,
            "recommended_net_saved_dollars": round(rec_net_saved, 2),
            "recommended_gross_saved_dollars": round(rec_gross_saved, 2),
        },
        "policy_cube": cube_records,
        "risk_grid_16": grid_16,
        "subgrades": subgrade_list,
        "terms": terms_dict,
        "purposes": purp_dict,
        "fico_bands": fico_list,
    }

    out_path = Path("data/exports/cockpit_cube.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cockpit_data, f, indent=2)

    print(f"[TASK] Saved empirical cube to {out_path} ({out_path.stat().st_size / 1024:.1f} KB).")
    return cockpit_data


if __name__ == "__main__":
    export_cockpit_cube()
