import pandas as pd

def process_task3_supplier_2(df):
    """Cleans and processes Supplier Data 2 for Task 3."""

    # Rename columns to match expected BigQuery schema
    df = df.rename(columns={
        "Material": "material",
        "Description": "description",
        "Article ID": "article_id",
        "Weight (kg)": "weight_kg",
        "Quantity": "quantity",
        "Reserved": "reserved"
    })

    # Convert numeric columns to appropriate types
    numeric_columns = ["weight_kg", "quantity"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure reserved is standardized (optional)
    df["reserved"] = df["reserved"].str.strip().str.upper()

    return df
