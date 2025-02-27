import pandas as pd
from task1_column_mapping import COLUMN_MAPPING_SUPPLIER_2, NUMERIC_COLUMNS_SUPPLIER_2


def process_supplier_2(df):
    """Cleans and standardizes Supplier 2 data."""

    # Rename columns using mapping
    df = df.rename(columns=COLUMN_MAPPING_SUPPLIER_2)

    # Ensure all expected columns exist
    expected_cols = list(COLUMN_MAPPING_SUPPLIER_2.values())
    for col in expected_cols:
        if col not in df.columns:
            df[col] = pd.NA  # Assign empty values for missing columns

    # Keep only expected columns
    df = df[expected_cols]

    # Convert numeric columns safely
    for col in NUMERIC_COLUMNS_SUPPLIER_2:
        if col in df.columns:
            # Only apply string operations on object columns
            if df[col].dtype == "object":
                # Replace commas in numbers
                df[col] = df[col].str.replace(",", ".", regex=False)

            # Convert to float/int
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing values with None to prevent type errors
    df = df.where(pd.notna(df), None)

    return df
