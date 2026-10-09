"""
Validation tests for raw CMS Medicaid Drug Utilization datasets.
Asserts that all 34 CMS Data Dictionary columns and key clinical schemas
exist across the raw .xlsx files in data/raw/.
"""

from pathlib import Path
import openpyxl
import pytest

DATA_RAW_DIR = Path("data/raw")
BGM_FILE = DATA_RAW_DIR / "DSD_MCD_RY26_P06_V20_D24_BGM.xlsx"
DBEXPORT_FILE = DATA_RAW_DIR / "DSD_MCD_RY26_P04_V10_YTD24_DBExport - 20260603.xlsx"
DICTIONARY_PDF = DATA_RAW_DIR / "Medicaid Spending by Drug Data Dictionary 508.pdf"

# 34 Core CMS Data Dictionary Columns (4 dimensions + 5 years * 6 annual measures)
CMS_CORE_34_COLUMNS = [
    # Core Entity Identifiers & Dimensions (4)
    "Brnd_Name",
    "Gnrc_Name",
    "Tot_Mftr",
    "Mftr_Name",
    # 2020 Annual Measures (6)
    "Tot_Spndng_2020",
    "Tot_Dsg_Unts_2020",
    "Tot_Clms_2020",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2020",
    "Avg_Spnd_Per_Clm_2020",
    "Outlier_Flag_2020",
    # 2021 Annual Measures (6)
    "Tot_Spndng_2021",
    "Tot_Dsg_Unts_2021",
    "Tot_Clms_2021",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2021",
    "Avg_Spnd_Per_Clm_2021",
    "Outlier_Flag_2021",
    # 2022 Annual Measures (6)
    "Tot_Spndng_2022",
    "Tot_Dsg_Unts_2022",
    "Tot_Clms_2022",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2022",
    "Avg_Spnd_Per_Clm_2022",
    "Outlier_Flag_2022",
    # 2023 Annual Measures (6)
    "Tot_Spndng_2023",
    "Tot_Dsg_Unts_2023",
    "Tot_Clms_2023",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2023",
    "Avg_Spnd_Per_Clm_2023",
    "Outlier_Flag_2023",
    # 2024 Annual Measures (6)
    "Tot_Spndng_2024",
    "Tot_Dsg_Unts_2024",
    "Tot_Clms_2024",
    "Avg_Spnd_Per_Dsg_Unt_Wghtd_2024",
    "Avg_Spnd_Per_Clm_2024",
    "Outlier_Flag_2024",
]

# Additional CMS longitudinal trend metrics present in the BGM file
CMS_TREND_METRICS = [
    "Chg_Avg_Spnd_Per_Dsg_Unt_23_24",
    "CAGR_Avg_Spnd_Per_Dsg_Unt_20_24",
]

# DBExport schema requirements for clinical indications and normalization
DBEXPORT_KEY_COLUMNS = [
    "Manufacturer Desc",
    "Brand Name Desc",
    "Generic Name",
    "Year",
    "Number of Manufacturers",
    "Cost Per Unit",
    "Cost Per Unit, All Mfg",
    "Cost Per Unit, Previous Year",
    "Annual Change in Cost Per Unit",
    "Compound Annual Growth Rate (CAGR) in Cost Per Unit through Current Year",
    "Total Payments",
    "Total Service Units",
    "Total Claim Count",
    "Average Cost per Claim",
    "Uses",
]


def test_raw_files_exist():
    """Verify that all raw source files exist in data/raw/."""
    assert BGM_FILE.is_file(), f"Missing raw BGM matrix file: {BGM_FILE}"
    assert DBEXPORT_FILE.is_file(), f"Missing raw DBExport file: {DBEXPORT_FILE}"
    assert DICTIONARY_PDF.is_file(), f"Missing Data Dictionary PDF: {DICTIONARY_PDF}"


def test_bgm_raw_schema_contains_34_cms_columns():
    """Assert that all 34 CMS Data Dictionary columns exist in the raw BGM Excel file."""
    wb = openpyxl.load_workbook(BGM_FILE, read_only=True)
    ws = wb.active
    header_row = next(ws.iter_rows(values_only=True))
    wb.close()

    bgm_columns = [col for col in header_row if col is not None]

    # Verify all 34 core CMS columns are present
    missing_core = [col for col in CMS_CORE_34_COLUMNS if col not in bgm_columns]
    assert not missing_core, f"BGM file missing {len(missing_core)} core CMS columns: {missing_core}"
    assert len(CMS_CORE_34_COLUMNS) == 34, "CMS_CORE_34_COLUMNS definition must contain exactly 34 columns"

    # Also verify the full 36-column schema including trend metrics
    for trend_col in CMS_TREND_METRICS:
        assert trend_col in bgm_columns, f"BGM file missing trend metric: {trend_col}"
    assert len(bgm_columns) >= 36, f"Expected at least 36 columns in BGM file, found {len(bgm_columns)}"


def test_dbexport_schema_contains_clinical_enrichment_columns():
    """Assert that DBExport contains clinical 'Uses' and required entity keys."""
    wb = openpyxl.load_workbook(DBEXPORT_FILE, read_only=True)
    ws = wb.active
    header_row = next(ws.iter_rows(values_only=True))
    wb.close()

    dbexport_columns = [col for col in header_row if col is not None]

    missing_cols = [col for col in DBEXPORT_KEY_COLUMNS if col not in dbexport_columns]
    assert not missing_cols, f"DBExport file missing required columns: {missing_cols}"
    assert "Uses" in dbexport_columns, "DBExport must contain 'Uses' column for clinical indication enrichment"


def test_bgm_hierarchy_contains_overall_and_detail_rows():
    """Assert that raw BGM data contains both 'Overall' summary rows and manufacturer rows."""
    wb = openpyxl.load_workbook(BGM_FILE, read_only=True)
    ws = wb.active

    has_overall = False
    has_non_overall = False

    # Check first 50 rows for hierarchy markers
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            mftr_idx = row.index("Mftr_Name")
            continue
        mftr = row[mftr_idx]
        if mftr == "Overall":
            has_overall = True
        elif mftr and mftr != "Overall":
            has_non_overall = True
        if has_overall and has_non_overall:
            break
        if i > 100:
            break

    wb.close()
    assert has_overall, "Raw BGM dataset must contain 'Overall' rollup rows"
    assert has_non_overall, "Raw BGM dataset must contain individual manufacturer detail rows"
