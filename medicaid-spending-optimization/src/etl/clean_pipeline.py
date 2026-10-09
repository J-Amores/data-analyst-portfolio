"""
CMS Medicaid Outpatient Drug Spend Optimization (CY2020-CY2024)
ETL Cleaning and Normalization Pipeline

Adheres to docs/DATA_SPEC.md (The CLEAN Framework):
- Conceptualize: Isolates summary ('Overall') from manufacturer detail to eliminate double-counting.
- Locate & Clean: Trims and uppercases entity names, standardizes delimiters, coerces data types.
- Evaluate Hard Issues: Handles HIPAA suppressed cells (< 11 fills) without invalid zero-imputation;
  flags CMS statistical outliers ({0, 1}).
- Augment: Adds brand/generic indicator, log price-volume decomposition driver,
  absolute/percentage spend growth, and regex-derived macro therapeutic class.
- Note & Export: Exports validated partitioned datasets to data/cleaned/*.parquet.
"""

from pathlib import Path
import re
import numpy as np
import pandas as pd

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"

BGM_RAW_PATH = DATA_RAW_DIR / "DSD_MCD_RY26_P06_V20_D24_BGM.xlsx"
DBEXPORT_RAW_PATH = DATA_RAW_DIR / "DSD_MCD_RY26_P04_V10_YTD24_DBExport - 20260603.xlsx"

OVERALL_PARQUET_PATH = DATA_CLEANED_DIR / "mcd_drug_overall_2020_2024.parquet"
DETAIL_PARQUET_PATH = DATA_CLEANED_DIR / "mcd_mftr_detail_2020_2024.parquet"

# Years
YEARS = [2020, 2021, 2022, 2023, 2024]


def classify_therapeutic_class(uses: str, brand: str, generic: str) -> str:
    """
    Classifies a drug entity into clinical macro therapeutic categories
    using rule-based regex parsing across clinical narrative (Uses),
    Brand Name, and Generic Name.
    """
    text = f"{brand} {generic} {uses}".lower()

    # 1. Antidiabetic & GLP-1 Metabolic
    if re.search(
        r"glp-1|semaglutide|tirzepatide|dulaglutide|liraglutide|exenatide|empagliflozin|"
        r"dapagliflozin|canagliflozin|sitagliptin|linagliptin|metformin|insulin|glipizide|"
        r"glimepiride|pioglitazone|diabet|glycemic|blood sugar",
        text,
    ):
        return "Antidiabetic / GLP-1"

    # 2. Immunology & Biologic Immunomodulators
    if re.search(
        r"adalimumab|humira|dupixent|stelara|tremfya|skyrizi|enbrel|rinvoq|xeljanz|"
        r"cosentyx|taltz|actemra|cimzia|orencia|entyvio|simponi|rheumatoid arthritis|"
        r"plaque psoriasis|psoriatic arthritis|crohn|ulcerative colitis|atopic dermatitis|"
        r"ankylosing spondylitis|immunosuppressive|immunosuppressant|immunomodulator|biologic response",
        text,
    ):
        return "Immunology / Immunomodulator"

    # 3. Infectious Disease: HIV / Antiretroviral
    if re.search(
        r"hiv|bictegravir|biktarvy|triumeq|truvada|descovy|genvoya|tivicay|isentress|"
        r"symtuza|juluca|dovato|cabenuva|emtricitabine|tenofovir|efavirenz|dolutegravir|"
        r"antiretroviral|protease inhibitor|reverse transcriptase",
        text,
    ):
        return "Infectious Disease / Antiretroviral"

    # 4. Oncology & Antineoplastic
    if re.search(
        r"keytruda|opdivo|revlimid|imbruvica|ibrutinib|pembrolizumab|darzalex|tagrisso|"
        r"erleada|xtandi|verzenio|ibrance|jakafi|sprycel|tasigna|venclexta|chemotherapy|"
        r"antineoplastic|carcinoma|lymphoma|leukemia|myeloma|melanoma|sarcoma|solid tumor|"
        r"metastatic|oncology",
        text,
    ):
        return "Oncology / Antineoplastic"

    # 5. Cardiovascular & Hematology / Anticoagulants
    if re.search(
        r"eliquis|xarelto|pradaxa|plavix|brilinta|apixaban|rivaroxaban|clopidogrel|"
        r"warfarin|anticoagulant|antiplatelet|blood thinner|thrombosis|embolism|entresto|"
        r"sacubitril|valsartan|losartan|lisinopril|amlodipine|metoprolol|carvedilol|"
        r"atorvastatin|rosuvastatin|hypertension|blood pressure|heart failure|cholesterol|"
        r"angina|arrhythmia|hemlibra|factor viii|coagulation factor",
        text,
    ):
        return "Cardiovascular / Hematologic"

    # 6. Central Nervous System & Psychotropic / Neurologic
    if re.search(
        r"invega|vraylar|vyvanse|abilify|rexulti|latuda|caplyta|seroquel|risperidone|"
        r"quetiapine|olanzapine|aripiprazole|lurasidone|cariprazine|antipsychotic|schizophrenia|"
        r"bipolar|antidepressant|depression|sertraline|fluoxetine|escitalopram|duloxetine|"
        r"venlafaxine|bupropion|adhd|amphetamine|methylphenidate|adderall|lisdexamfetamine|"
        r"anticonvulsant|epilepsy|seizure|levetiracetam|lamotrigine|topiramate|valproic|"
        r"gabapentin|pregabalin|parkinson|alzheimer|donepezil|memantine|migraine|ubrelvy|"
        r"nurtec|emgality|aimovig|ajovy",
        text,
    ):
        return "Central Nervous System / Psychotropic"

    # 7. Respiratory & Pulmonary
    if re.search(
        r"trikafta|symbicort|trelegy|advair|breo|albuterol|levalbuterol|fluticasone|"
        r"budesonide|tiotropium|spiriva|wixela|dulera|asthma|copd|bronchospasm|bronchodilator|"
        r"inhaler|pulmonary|cystic fibrosis|ivacaftor|elexacaftor",
        text,
    ):
        return "Respiratory / Pulmonary"

    # 8. Pain & Musculoskeletal / Substance Use Disorder
    if re.search(
        r"suboxone|buprenorphine|naloxone|methadone|vivitrol|naltrexone|oxycodone|"
        r"hydrocodone|fentanyl|morphine|tramadol|tapentadol|hydromorphone|analgesic|"
        r"opioid|pain relief|anti-inflammatory|nsaid|meloxicam|celecoxib|diclofenac|"
        r"ibuprofen|acetaminophen",
        text,
    ):
        return "Pain & Substance Use Disorder"

    # 9. Other Infectious Disease / Antimicrobials
    if re.search(
        r"antibiotic|antibacterial|antifungal|antiviral|hepatitis|sofosbuvir|epclusa|"
        r"mavyret|amoxicillin|azithromycin|ciprofloxacin|doxycycline|vancomycin|fluconazole|"
        r"acyclovir|valacyclovir|bacterial infection|fungal infection",
        text,
    ):
        return "Infectious Disease / Antimicrobial"

    # 10. Gastrointestinal
    if re.search(
        r"gerd|acid reflux|proton pump|omeprazole|pantoprazole|esomeprazole|lansoprazole|"
        r"ulcer|gastrointestinal|constipation|linzess|motegrity|laxative|antiemetic|ondansetron|nausea",
        text,
    ):
        return "Gastrointestinal"

    # 11. Dermatologic & Sensory (Ophthalmic / Otic)
    if re.search(
        r"eye|ophthalmic|glaucoma|latanoprost|timolol|dry eye|restasis|xiidra|topical|"
        r"dermatitis|eczema|psoriasis|acne|tretinoin|hydrocortisone",
        text,
    ):
        return "Dermatologic & Sensory"

    return "Other / Specialized Care"


def load_clinical_uses_lookup(dbexport_path: Path) -> dict:
    """
    Loads and normalizes the clinical Uses narrative lookup from DBExport.
    Returns mapping: (normalized_brand, normalized_generic) -> Uses text.
    """
    print(f"Loading clinical indications from {dbexport_path.name}...")
    df_db = pd.read_excel(
        dbexport_path,
        usecols=["Brand Name Desc", "Generic Name", "Uses"],
    )

    # Normalize entity keys
    df_db["b_norm"] = (
        df_db["Brand Name Desc"]
        .astype(str)
        .str.strip()
        .str.rstrip("^ *#@†‡")
        .str.strip()
        .str.upper()
    )
    df_db["g_norm"] = (
        df_db["Generic Name"]
        .astype(str)
        .str.strip()
        .str.replace("/", ", ")
        .str.strip()
        .str.upper()
    )

    lookup = (
        df_db.dropna(subset=["Uses"])
        .drop_duplicates(subset=["b_norm", "g_norm"])
        .set_index(["b_norm", "g_norm"])["Uses"]
        .to_dict()
    )
    print(f"Loaded {len(lookup):,} distinct clinical indication entries.")
    return lookup


def clean_and_augment_data(bgm_path: Path, uses_lookup: dict) -> pd.DataFrame:
    """
    Loads raw BGM file, enforces data types, applies text standardization,
    joins clinical descriptions, and calculates analytical augmentations.
    """
    print(f"Loading raw BGM matrix from {bgm_path.name}...")
    df = pd.read_excel(bgm_path)

    print(f"Raw BGM records loaded: {len(df):,} rows x {len(df.columns)} columns.")

    # 1. Text Sanitation & Normalization (TRIM(UPPER(col)))
    df["Brnd_Name"] = (
        df["Brnd_Name"]
        .astype(str)
        .str.strip()
        .str.rstrip("^ *#@†‡")
        .str.strip()
        .str.upper()
    )
    df["Gnrc_Name"] = (
        df["Gnrc_Name"]
        .astype(str)
        .str.strip()
        .str.replace("/", ", ")
        .str.strip()
        .str.upper()
    )
    df["Mftr_Name"] = df["Mftr_Name"].astype(str).str.strip().str.upper()

    # 2. Type Coercion & Financial Casting
    df["Tot_Mftr"] = pd.to_numeric(df["Tot_Mftr"], errors="coerce").fillna(1).astype("int64")

    for yr in YEARS:
        # Currency / Volume metrics: float64
        df[f"Tot_Spndng_{yr}"] = pd.to_numeric(df[f"Tot_Spndng_{yr}"], errors="coerce").astype("float64")
        df[f"Tot_Dsg_Unts_{yr}"] = pd.to_numeric(df[f"Tot_Dsg_Unts_{yr}"], errors="coerce").astype("float64")
        df[f"Avg_Spnd_Per_Dsg_Unt_Wghtd_{yr}"] = pd.to_numeric(df[f"Avg_Spnd_Per_Dsg_Unt_Wghtd_{yr}"], errors="coerce").astype("float64")
        df[f"Avg_Spnd_Per_Clm_{yr}"] = pd.to_numeric(df[f"Avg_Spnd_Per_Clm_{yr}"], errors="coerce").astype("float64")

        # Claims & Outliers: nullable Int64 to preserve HIPAA missingness
        df[f"Tot_Clms_{yr}"] = pd.to_numeric(df[f"Tot_Clms_{yr}"], errors="coerce").astype("Int64")
        df[f"Outlier_Flag_{yr}"] = pd.to_numeric(df[f"Outlier_Flag_{yr}"], errors="coerce").astype("Int64")

    # Longitudinal trend metrics
    df["Chg_Avg_Spnd_Per_Dsg_Unt_23_24"] = pd.to_numeric(
        df["Chg_Avg_Spnd_Per_Dsg_Unt_23_24"], errors="coerce"
    ).astype("float64")
    df["CAGR_Avg_Spnd_Per_Dsg_Unt_20_24"] = pd.to_numeric(
        df["CAGR_Avg_Spnd_Per_Dsg_Unt_20_24"], errors="coerce"
    ).astype("float64")

    # 3. HIPAA Privacy Redaction Metadata Flag
    # True if any historical claims were suppressed (< 11 claims suppressed by CMS)
    hist_claim_cols = [f"Tot_Clms_{yr}" for yr in [2020, 2021, 2022, 2023]]
    df["has_hipaa_suppression"] = df[hist_claim_cols].isna().any(axis=1)

    # 4. Clinical Indications Enrichment
    df["Uses"] = [
        uses_lookup.get((b, g), "Clinical indication not documented in DBExport.")
        for b, g in zip(df["Brnd_Name"], df["Gnrc_Name"])
    ]

    # 5. Macro Therapeutic Class
    df["therapeutic_class_macro"] = [
        classify_therapeutic_class(u, b, g)
        for u, b, g in zip(df["Uses"], df["Brnd_Name"], df["Gnrc_Name"])
    ]

    # 6. Brand vs. Generic Status Flag
    # Brand if Brnd_Name != Gnrc_Name
    df["is_brand_flag"] = df["Brnd_Name"] != df["Gnrc_Name"]

    # 7. Absolute and Percentage Spend Growth (2020 to 2024)
    df["spend_growth_abs_20_24"] = df["Tot_Spndng_2024"] - df["Tot_Spndng_2020"]
    df["spend_growth_pct_20_24"] = (
        df["spend_growth_abs_20_24"] / df["Tot_Spndng_2020"]
    )

    # 8. Econometric Price-Volume Growth Driver (Logarithmic Decomposition)
    p20 = df["Avg_Spnd_Per_Dsg_Unt_Wghtd_2020"].astype(float)
    p24 = df["Avg_Spnd_Per_Dsg_Unt_Wghtd_2024"].astype(float)
    q20 = df["Tot_Clms_2020"].astype(float)
    q24 = df["Tot_Clms_2024"].astype(float)

    valid_decomp = (
        (p20 > 0)
        & (p24 > 0)
        & (q20 > 0)
        & (q24 > 0)
        & p20.notna()
        & p24.notna()
        & q20.notna()
        & q24.notna()
    )

    # Calculate log changes avoiding division by zero warnings
    d_ln_p = np.full(len(df), np.nan)
    d_ln_q = np.full(len(df), np.nan)
    valid_idx = valid_decomp[valid_decomp].index

    d_ln_p[valid_idx] = np.log(p24.loc[valid_idx] / p20.loc[valid_idx])
    d_ln_q[valid_idx] = np.log(q24.loc[valid_idx] / q20.loc[valid_idx])

    drivers = np.where(
        ~valid_decomp,
        "New Launch / Insufficient Baseline",
        np.where(d_ln_p > d_ln_q, "Price-Driven", "Volume-Driven"),
    )
    df["price_vs_volume_driver"] = drivers

    return df


def execute_pipeline():
    """
    Executes the end-to-end data pipeline:
    1. Loads DBExport clinical indications.
    2. Cleans and augments the BGM longitudinal fact matrix.
    3. Forks the dataset into 'Overall' composite rollup and labeler detail views.
    4. Saves to data/cleaned/*.parquet.
    5. Runs reconciliation assertions.
    """
    DATA_CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    uses_lookup = load_clinical_uses_lookup(DBEXPORT_RAW_PATH)
    cleaned_df = clean_and_augment_data(BGM_RAW_PATH, uses_lookup)

    # Fork datasets: Double-counting elimination rule
    # Mftr_Name == 'OVERALL' is the composite rollup
    overall_mask = cleaned_df["Mftr_Name"] == "OVERALL"
    df_overall = cleaned_df[overall_mask].copy().reset_index(drop=True)
    df_detail = cleaned_df[~overall_mask].copy().reset_index(drop=True)

    print("\n--- Pipeline Partitioning Summary ---")
    print(f"Total processed records: {len(cleaned_df):,}")
    print(f"Composite 'OVERALL' rows: {len(df_overall):,}")
    print(f"Manufacturer detail rows: {len(df_detail):,}")

    # Financial Reconciliation Check
    spend_overall_2024 = df_overall["Tot_Spndng_2024"].sum()
    spend_detail_2024 = df_detail["Tot_Spndng_2024"].sum()
    naive_spend_2024 = cleaned_df["Tot_Spndng_2024"].sum()

    print(f"\n--- Spend Reconciliation (CY2024) ---")
    print(f"Composite Outlay (Pre-Rebate):  ${spend_overall_2024:,.2f}")
    print(f"Labeler Detail Sum:             ${spend_detail_2024:,.2f}")
    print(f"Unpartitioned Naive Total:      ${naive_spend_2024:,.2f} (Double-counts!)")

    # Assert budget reconciliation parity within $1.00 tolerance (floating point rounding)
    assert abs(spend_overall_2024 - spend_detail_2024) < 1.0, (
        f"Reconciliation error: Overall spend (${spend_overall_2024:,.2f}) != "
        f"Detail spend (${spend_detail_2024:,.2f})"
    )

    # Save to Parquet
    df_overall.to_parquet(OVERALL_PARQUET_PATH, index=False, engine="pyarrow")
    df_detail.to_parquet(DETAIL_PARQUET_PATH, index=False, engine="pyarrow")

    print(f"\nSuccessfully wrote:")
    print(f"  -> {OVERALL_PARQUET_PATH} ({OVERALL_PARQUET_PATH.stat().st_size / 1024:.1f} KB)")
    print(f"  -> {DETAIL_PARQUET_PATH} ({DETAIL_PARQUET_PATH.stat().st_size / 1024:.1f} KB)")

    return df_overall, df_detail


if __name__ == "__main__":
    execute_pipeline()
