"""
Raw schema pre-flight unit tests for Banco de Portugal marketing campaign datasets.
Validates file presence, dimensions, delimiter formatting, expected columns, and target integrity.
"""

from pathlib import Path
import pandas as pd
import pytest

DATA_RAW_DIR = Path("data/raw")
BANK_ADDITIONAL_FULL_PATH = DATA_RAW_DIR / "bank-additional-full.csv"
BANK_FULL_PATH = DATA_RAW_DIR / "bank-full.csv"

EXPECTED_ADDITIONAL_COLUMNS = [
    "age", "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "duration", "campaign", "pdays",
    "previous", "poutcome", "emp.var.rate", "cons.price.idx", "cons.conf.idx",
    "euribor3m", "nr.employed", "y"
]

EXPECTED_FULL_COLUMNS = [
    "age", "job", "marital", "education", "default", "balance", "housing",
    "loan", "contact", "day", "month", "duration", "campaign", "pdays",
    "previous", "poutcome", "y"
]


def test_bank_additional_full_exists():
    assert BANK_ADDITIONAL_FULL_PATH.is_file(), (
        f"Missing primary raw file: {BANK_ADDITIONAL_FULL_PATH}"
    )


def test_bank_full_exists():
    assert BANK_FULL_PATH.is_file(), (
        f"Missing benchmark raw file: {BANK_FULL_PATH}"
    )


def test_bank_additional_full_schema():
    df = pd.read_csv(BANK_ADDITIONAL_FULL_PATH, sep=";")
    assert df.shape == (41188, 21), (
        f"Expected shape (41188, 21), got {df.shape}"
    )
    assert list(df.columns) == EXPECTED_ADDITIONAL_COLUMNS, (
        f"Columns mismatch in bank-additional-full.csv. Got: {list(df.columns)}"
    )


def test_bank_full_schema():
    df = pd.read_csv(BANK_FULL_PATH, sep=";")
    assert df.shape == (45211, 17), (
        f"Expected shape (45211, 17), got {df.shape}"
    )
    assert list(df.columns) == EXPECTED_FULL_COLUMNS, (
        f"Columns mismatch in bank-full.csv. Got: {list(df.columns)}"
    )
    assert "balance" in df.columns, "Expected 'balance' column in bank-full.csv"
    assert "day" in df.columns, "Expected 'day' column in bank-full.csv"


def test_target_column_integrity():
    df_add = pd.read_csv(BANK_ADDITIONAL_FULL_PATH, sep=";")
    assert df_add["y"].isnull().sum() == 0, "Null values detected in target 'y' of bank-additional-full.csv"
    assert set(df_add["y"].unique()) == {"yes", "no"}, (
        f"Unexpected values in target 'y' of bank-additional-full.csv: {df_add['y'].unique()}"
    )

    df_full = pd.read_csv(BANK_FULL_PATH, sep=";")
    assert df_full["y"].isnull().sum() == 0, "Null values detected in target 'y' of bank-full.csv"
    assert set(df_full["y"].unique()) == {"yes", "no"}, (
        f"Unexpected values in target 'y' of bank-full.csv: {df_full['y'].unique()}"
    )
