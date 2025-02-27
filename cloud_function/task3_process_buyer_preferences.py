import pandas as pd

def process_buyer_preferences(df):
    """Cleans and processes Buyer Preferences data."""
    
    # Rename columns according to buyer preferences mapping
    df = df.rename(columns={
        "Buyer ID": "buyer_id",
        "Preferred Grade": "preferred_grade",
        "Preferred Finish": "preferred_finish",
        "Preferred Thickness (mm)": "preferred_thickness_mm",
        "Preferred Width (mm)": "preferred_width_mm",
        "Max Weight (kg)": "max_weight_kg",
        "Min Quantity": "min_quantity"
    })
    
    # Convert numeric columns to appropriate types
    numeric_columns = ["preferred_thickness_mm", "preferred_width_mm", "max_weight_kg", "min_quantity"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
