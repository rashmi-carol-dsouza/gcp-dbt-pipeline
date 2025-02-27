import pandas as pd

def process_task3_supplier_1(df):
    """Cleans and processes Supplier Data 1 for Task 3."""

    # Rename columns
    df = df.rename(columns={
        "Quality/Choice": "quality_choice",
        "Grade": "grade",
        "Finish": "finish",
        "Thickness (mm)": "thickness_mm",
        "Width (mm)": "width_mm",
        "Description": "description",
        "Gross weight (kg)": "gross_weight_kg",
        "RP02": "rp02",
        "RM": "rm",
        "Quantity": "quantity",
        "AG": "ag",
        "AI": "ai"
    })

    # Convert numeric columns to appropriate types
    numeric_columns = ["thickness_mm", "width_mm", "gross_weight_kg", "rp02", "rm", "ag", "ai"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Explicitly convert `quantity` to INTEGER, rounding any decimals
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

    return df
