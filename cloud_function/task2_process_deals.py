import pandas as pd

def process_deals(df):
    """Cleans and processes Deals CSV data before loading into BigQuery."""
    
    # Define correct column names mapping
    column_mapping = {
        "deal_id": "deal_id",
        "opportunity_id": "opportunity_id",
        "deal_type": "deal_type",
        "buyer_company": "buyer_company",
        "supplier_company": "supplier_company",
        "buyer_name": "buyer_name",
        "buyer_am": "buyer_am",
        "supplier_name": "supplier_name",
        "supplier_am": "supplier_am",
        "supplier_user_id": "supplier_user_id",
        "deal_stage": "deal_stage",
        "buyer_country": "buyer_country",
        "supplier_country": "supplier_country",
        "buyer_region": "buyer_region",
        "supplier_region": "supplier_region",
        "deal_created_at": "deal_created_at",
        "buyer_company_id": "buyer_company_id",
        "supplier_company_id": "supplier_company_id",
        "buyer_user_id": "buyer_user_id",
        "buyer_am_id": "buyer_am_id",
        "supplier_am_id": "supplier_am_id",
        "buyer_country_id": "buyer_country_id",
        "supplier_country_id": "supplier_country_id",
        "buyer_payment_term": "buyer_payment_term",
        "supplier_payment_term": "supplier_payment_term",
        "buyer_incoterms_name": "buyer_incoterms_name",
        "supplier_incoterms_name": "supplier_incoterms_name",
        "opportunity_source_name": "opportunity_source_name",
        "sale_order_number": "sale_order_number",
        "purchase_order_number": "purchase_order_number",
        "booked_tonnage": "booked_tonnage",
        "booked_buyer_price_per_ton": "booked_buyer_price_per_ton",
        "booked_supplier_price_per_ton": "booked_supplier_price_per_ton",
        "booked_gross_revenue": "booked_gross_revenue",
        "booked_material_cost": "booked_material_cost",
        "booked_supplier_fee_percent": "booked_supplier_fee_percent",
        "booked_supplier_fee_euro": "booked_supplier_fee_euro",
        "booked_gross_profit": "booked_gross_profit",
        "booked_gross_profit_margin_percent": "booked_gross_profit_margin_percent",
        "booked_truck_price": "booked_truck_price",
        "booked_total_trucks": "booked_total_trucks",
        "booked_logistic_cost": "booked_logistic_cost",
        "booked_financing_cost": "booked_financing_cost",
        "confirmed_tonnage": "confirmed_tonnage",
        "confirmed_gross_revenue": "confirmed_gross_revenue",
        "confirmed_gross_profit": "confirmed_gross_profit",
        "confirmed_buyer_price_per_ton": "confirmed_buyer_price_per_ton",
        "confirmed_supplier_price_per_ton": "confirmed_supplier_price_per_ton",
        "confirmed_supplier_tonnage": "confirmed_supplier_tonnage",
        "confirmed_material_cost": "confirmed_material_cost",
        "confirmed_logistics_cost": "confirmed_logistics_cost",
        "confirmed_financing_cost": "confirmed_financing_cost",
        "confirmed_supplier_fee": "confirmed_supplier_fee",
        "confirmed_gross_profit_margin": "confirmed_gross_profit_margin"
    }

    # Rename columns
    df = df.rename(columns=column_mapping)

    # Convert data types
    numeric_cols = [
        "booked_tonnage", "booked_buyer_price_per_ton", "booked_supplier_price_per_ton",
        "booked_gross_revenue", "booked_material_cost", "booked_supplier_fee_percent",
        "booked_supplier_fee_euro", "booked_gross_profit", "booked_gross_profit_margin_percent",
        "booked_truck_price", "booked_total_trucks", "booked_logistic_cost",
        "booked_financing_cost", "confirmed_tonnage", "confirmed_gross_revenue",
        "confirmed_gross_profit", "confirmed_buyer_price_per_ton", "confirmed_supplier_price_per_ton",
        "confirmed_supplier_tonnage", "confirmed_material_cost", "confirmed_logistics_cost",
        "confirmed_financing_cost", "confirmed_supplier_fee", "confirmed_gross_profit_margin"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert timestamps
    df["deal_created_at"] = pd.to_datetime(df["deal_created_at"], errors="coerce")

    return df