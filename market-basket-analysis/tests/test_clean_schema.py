"""Cleaned Data Lineage and Integrity Unit Tests.

Validates that:
1. fct_order_items_clean.parquet has zero 'C' invoices, zero Quantity <= 0,
   zero UnitPrice <= 0, zero non-merchandise StockCodes, and exactly 522,544 rows.
2. fct_orders_summary.parquet has unique InvoiceNo keys and exactly 19,773 orders.
3. All required augmented features exist.
"""

from pathlib import Path
import pandas as pd
import pytest

CLEAN_ITEMS_PATH = Path("data/cleaned/fct_order_items_clean.parquet")
ORDERS_SUMMARY_PATH = Path("data/cleaned/fct_orders_summary.parquet")
CANCELLATIONS_PATH = Path("data/cleaned/fct_cancellations_refunds.parquet")

NON_MERCHANDISE_CODES = {
    "POST",
    "D",
    "M",
    "BANK CHARGES",
    "C2",
    "DOT",
    "PADS",
    "AMAZONFEE",
    "B",
    "CRUK",
    "S",
    "DCGSSGIRL",
    "DCGSSBOY",
}


@pytest.fixture(scope="module")
def clean_items_df():
    """Load clean order items table."""
    assert CLEAN_ITEMS_PATH.exists(), f"Clean items file missing at {CLEAN_ITEMS_PATH}"
    return pd.read_parquet(CLEAN_ITEMS_PATH)


@pytest.fixture(scope="module")
def orders_summary_df():
    """Load orders summary table."""
    assert ORDERS_SUMMARY_PATH.exists(), f"Orders summary file missing at {ORDERS_SUMMARY_PATH}"
    return pd.read_parquet(ORDERS_SUMMARY_PATH)


def test_clean_items_row_and_order_counts(clean_items_df):
    """Verify clean line items row count is 522,544 and invoice count is 19,773."""
    assert len(clean_items_df) == 522544, f"Expected 522,544 rows, got {len(clean_items_df):,}"
    assert clean_items_df["InvoiceNo_str"].nunique() == 19773, (
        f"Expected 19,773 invoices, got {clean_items_df['InvoiceNo_str'].nunique():,}"
    )


def test_no_cancellation_invoices_in_clean_items(clean_items_df):
    """Verify zero 'C' prefix invoices in commercial sales items."""
    c_mask = clean_items_df["InvoiceNo_str"].str.startswith("C")
    assert c_mask.sum() == 0, f"Found {c_mask.sum()} cancellation invoices in clean items"


def test_positive_quantities_and_prices(clean_items_df):
    """Verify all line items have strictly positive quantities and unit prices."""
    invalid_qty = clean_items_df["Quantity"] <= 0
    invalid_price = clean_items_df["UnitPrice"] <= 0
    assert invalid_qty.sum() == 0, f"Found {invalid_qty.sum()} non-positive Quantity rows"
    assert invalid_price.sum() == 0, f"Found {invalid_price.sum()} non-positive UnitPrice rows"


def test_zero_non_merchandise_codes(clean_items_df):
    """Verify exclusion of postage, freight, and accounting adjustment codes."""
    non_merch_matches = clean_items_df["StockCode_str"].isin(NON_MERCHANDISE_CODES)
    assert non_merch_matches.sum() == 0, (
        f"Found {non_merch_matches.sum()} non-merchandise rows in clean items"
    )


def test_orders_summary_primary_key_uniqueness(orders_summary_df):
    """Verify that InvoiceNo is a unique primary key in orders summary."""
    assert len(orders_summary_df) == 19773, f"Expected 19,773 orders, got {len(orders_summary_df):,}"
    assert orders_summary_df["InvoiceNo"].is_unique, "InvoiceNo is not unique in orders summary"


def test_orders_summary_required_columns(orders_summary_df):
    """Verify presence of analytical features in orders summary."""
    required_cols = [
        "InvoiceNo",
        "basket_size_skus",
        "total_units",
        "order_revenue",
        "basket_tier",
        "detailed_basket_tier",
        "Country",
        "is_uk",
        "is_guest_checkout",
        "invoice_YearMonth",
    ]
    for col in required_cols:
        assert col in orders_summary_df.columns, f"Missing required column '{col}' in summary"


def test_cancellations_table_integrity():
    """Verify cancellations table exists and contains credit notes."""
    assert CANCELLATIONS_PATH.exists(), f"Cancellations file missing at {CANCELLATIONS_PATH}"
    df_canc = pd.read_parquet(CANCELLATIONS_PATH)
    assert len(df_canc) == 9288, f"Expected 9,288 cancellation rows, got {len(df_canc):,}"
    assert df_canc["InvoiceNo_str"].str.startswith("C").all(), (
        "Non-cancellation invoice found in cancellations table"
    )
