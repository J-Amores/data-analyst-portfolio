"""
Tests for cleaned dataset outputs and pipeline integrity.
Validates that output parquet files in data/cleaned/ adhere to DATA_SPEC.md.
"""

from pathlib import Path
import pandas as pd
import pytest

DATA_CLEANED_DIR = Path("data/cleaned")
OVERALL_PARQUET = DATA_CLEANED_DIR / "mcd_drug_overall_2020_2024.parquet"
DETAIL_PARQUET = DATA_CLEANED_DIR / "mcd_mftr_detail_2020_2024.parquet"

EXPECTED_CMS_34_COLUMNS = [
    "Brnd_Name",
    "Gnrc_Name",
    "Tot_Mftr",
    "Mftr_Name",
    "Tot_Spndng_2020",
    "Tot_Dsg_Unts_2020",
    "Tot_Clms_2020",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2020",
    "Avg_Spnd_Per_Clm_2020",
    "Outlier_Flag_2020",
    "Tot_Spndng_2021",
    "Tot_Dsg_Unts_2021",
    "Tot_Clms_2021",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2021",
    "Avg_Spnd_Per_Clm_2021",
    "Outlier_Flag_2021",
    "Tot_Spndng_2022",
    "Tot_Dsg_Unts_2022",
    "Tot_Clms_2022",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2022",
    "Avg_Spnd_Per_Clm_2022",
    "Outlier_Flag_2022",
    "Tot_Spndng_2023",
    "Tot_Dsg_Unts_2023",
    "Tot_Clms_2023",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2023",
    "Avg_Spnd_Per_Clm_2023",
    "Outlier_Flag_2023",
    "Tot_Spndng_2024",
    "Tot_Dsg_Unts_2024",
    "Tot_Clms_2024",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2024",
    "Avg_Spnd_Per_Clm_2024",
    "Outlier_Flag_2024",
]

EXPECTED_AUGMENTATIONS = [
    "is_brand_flag",
    "spend_growth_abs_20_24",
    "spend_growth_pct_20_24",
    "price_vs_volume_driver",
    "therapeutic_class_macro",
    "has_hipaa_suppression",
    "Uses",
]


def test_cleaned_parquet_files_exist():
    """Verify that both cleaned parquet datasets exist."""
    assert OVERALL_PARQUET.is_file(), f"Missing {OVERALL_PARQUET}"
    assert DETAIL_PARQUET.is_file(), f"Missing {DETAIL_PARQUET}"


def test_row_counts_and_partition_isolation():
    """Verify exact row counts and strict Mftr_Name separation."""
    df_overall = pd.read_parquet(OVERALL_PARQUET)
    df_detail = pd.read_parquet(DETAIL_PARQUET)

    assert len(df_overall) == 4774, f"Expected 4,774 overall rows, found {len(df_overall)}"
    assert len(df_detail) == 13737, f"Expected 13,737 detail rows, found {len(df_detail)}"

    # Check isolation: df_overall has ONLY OVERALL, df_detail has NO OVERALL
    assert (df_overall["Mftr_Name"] == "OVERALL").all(), "All rows in overall dataset must be 'OVERALL'"
    assert (df_detail["Mftr_Name"] != "OVERALL").all(), "No rows in detail dataset can be 'OVERALL'"


def test_double_counting_budget_reconciliation():
    """Verify spend reconciliation parity between overall rollup and detail sum."""
    df_overall = pd.read_parquet(OVERALL_PARQUET)
    df_detail = pd.read_parquet(DETAIL_PARQUET)

    overall_spend_2024 = df_overall["Tot_Spndng_2024"].sum()
    detail_spend_2024 = df_detail["Tot_Spndng_2024"].sum()

    # Reconciles within 1 dollar floating point tolerance
    assert abs(overall_spend_2024 - detail_spend_2024) < 1.0, (
        f"Reconciliation mismatch: overall={overall_spend_2024}, detail={detail_spend_2024}"
    )

    # Sanity check total program spend range (~$111B)
    assert 1.0e11 < overall_spend_2024 < 1.3e11, (
        f"Unexpected CY2024 gross spend magnitude: ${overall_spend_2024:,.2f}"
    )


def test_schema_contains_cms_columns_and_augmentations():
    """Verify that all 34 CMS Data Dictionary columns and analytical augmentations are present."""
    df_overall = pd.read_parquet(OVERALL_PARQUET)

    missing_cms = [c for c in EXPECTED_CMS_34_COLUMNS if c not in df_overall.columns]
    assert not missing_cms, f"Missing CMS core columns: {missing_cms}"

    missing_aug = [c for c in EXPECTED_AUGMENTATIONS if c not in df_overall.columns]
    assert not missing_aug, f"Missing augmentation columns: {missing_aug}"


def test_data_types_and_domain_constraints():
    """Verify data types and allowed values."""
    df = pd.read_parquet(OVERALL_PARQUET)

    # is_brand_flag must be boolean
    assert df["is_brand_flag"].dtype == bool

    # Outlier flags must be 0 or 1 when non-null
    for yr in [2020, 2021, 2022, 2023, 2024]:
        non_null_flags = df[f"Outlier_Flag_{yr}"].dropna()
        assert set(non_null_flags.unique()).issubset({0, 1})

    # Therapeutic class macro must have no nulls
    assert df["therapeutic_class_macro"].isna().sum() == 0

    # Price vs volume driver allowed set
    allowed_drivers = {"Price-Driven", "Volume-Driven", "New Launch / Insufficient Baseline"}
    assert set(df["price_vs_volume_driver"].unique()).issubset(allowed_drivers)
