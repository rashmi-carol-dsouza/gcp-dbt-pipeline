import pandas as pd
import re
from task1_column_mapping import COLUMN_MAPPING_SUPPLIER_2, NUMERIC_COLUMNS_SUPPLIER_2
from task1_process_supplier_1 import clean_numeric_column

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

    #Handling Missing Values
    categorical_cols = ["product_type", "order_id", "site", "material_name", "material_number",
                        "material_quality_norm", "surface_coating", "defect_notes", "incoterm"]
    numeric_cols = NUMERIC_COLUMNS_SUPPLIER_2

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")  # Replace missing categorical values with "Unknown"

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)  # Replace missing numeric values with 0

    #Data Type Corrections
    for col in numeric_cols:
        if col in df.columns:
            df[col] = clean_numeric_column(df[col])  # Clean and convert numeric values

    # Convert date columns properly
    date_cols = ["delivery_earliest", "delivery_latest", "valid_until"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Data Type Correnctions - datetime
    date_cols = ["delivery_earliest", "delivery_latest", "valid_until"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True) 
            df[col] = df[col].fillna(pd.NaT)
        

    #Removing Duplicates
    df.drop_duplicates(inplace=True)

    print("Cleaning completed for Supplier 2 dataset!")

    return df
