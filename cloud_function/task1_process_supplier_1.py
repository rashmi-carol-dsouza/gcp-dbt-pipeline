import pandas as pd
import re
from task1_column_mapping import COLUMN_MAPPING_SUPPLIER_1, NUMERIC_COLUMNS_SUPPLIER_1

def clean_numeric_column(series):
    """Cleans and converts numeric columns properly."""
    if series.dtype == "object":
        series = series.astype(str)  # Ensure string type
        series = series.str.replace("[^0-9.,]", "", regex=True)  # Remove non-numeric chars
        series = series.str.replace(",", ".", regex=False)  # Convert commas to dots

        def fix_misplaced_decimals(value):
            if not value or value in ["..", ".", ""]:  # Handle empty or invalid values
                return 0
            matches = re.findall(r"\d+", value)  # Extract numeric parts
            if len(matches) > 1:  # If multiple number groups exist
                return float("".join(matches[:-1]) + "." + matches[-1])  # Merge digits, keeping last as decimal
            return float(value)  # Convert to float
        
        series = series.apply(fix_misplaced_decimals)
    
    return series

def process_supplier_1(df):
    """Cleans and standardizes Supplier 1 data."""
    
    # Rename columns using mapping
    df = df.rename(columns=COLUMN_MAPPING_SUPPLIER_1)

    # Ensure all expected columns exist
    expected_cols = list(COLUMN_MAPPING_SUPPLIER_1.values())
    for col in expected_cols:
        if col not in df.columns:
            df[col] = pd.NA  # Assign empty values for missing columns

    # Keep only expected columns
    df = df[expected_cols]

  
    # Handling Missing Values
    categorical_cols = ["grade", "finish", "cluster"]
    numeric_cols = NUMERIC_COLUMNS_SUPPLIER_1

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")  # Replace missing categorical values with "Unknown"

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)  # Replace missing numeric values with 0

    # Data Type Corrections
    for col in numeric_cols:
        if col in df.columns:
            df[col] = clean_numeric_column(df[col])  # Clean and convert numeric values

    # Removing Duplicates
    df.drop_duplicates(inplace=True)

    print("Cleaning completed for Supplier 1 dataset!")

    return df 