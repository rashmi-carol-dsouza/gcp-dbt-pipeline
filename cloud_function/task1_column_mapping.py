# column_mapping.py

COLUMN_MAPPING_SUPPLIER_1 = {
    "Werksgüte": "grade",
    "Bestellgütentext": "finish",
    "Nenndicke NNN.NN mm mit Dezimalpunkt": "thickness_mm",
    "Breite": "width_mm",
    "Länge": "length_mm",
    "Gewicht (kg)": "weight_kg",
    "Cluster": "quantity",
    "Si-Gehalt": "si_content",
    "Mn-Gehalt": "mn_content",
    "P-Gehalt": "p_content",
    "S-Gehalt": "s_content",
    "Cr-Gehalt": "cr_content",
    "Ni-Gehalt": "ni_content",
    "Mo-Gehalt": "mo_content",
    "V-Gehalt": "v_content",
    "Cu-Gehalt": "cu_content",
    "Nb-Gehalt": "nb_content",
    "Ti-Gehalt": "ti_content",
    "Al-Gehalt": "al_content",
    "B-Gehalt": "b_content",
    "Streckgrenze": "yield_strength",
    "Zugfestigkeit": "tensile_strength",
    "Dehnung": "elongation",
}

COLUMN_MAPPING_SUPPLIER_2 = {
    "PRODUCT_TYPE": "product_type",
    "ORDER_ID": "order_id",
    "SITE": "site",
    "MATERIAL_NAME": "material_name",
    "MATERIAL_NUMBER": "material_number",
    "MATERIAL_QUALITY_NORM": "material_quality_norm",
    "SURFACE_COATING": "surface_coating",
    "DEFECT_NOTES": "defect_notes",
    "NOMINAL_THICKNESS_MM": "thickness_mm",
    "WIDTH_MM": "width_mm",
    "LENGTH_MM": "length_mm",
    "HEIGHT_MM": "height_mm",
    "MASS_MIN_KG": "weight_kg",
    "NUMBER_OF_COILS": "num_coils",
    "DELIVERY_EARLIEST": "delivery_earliest",
    "DELIVERY_LATEST": "delivery_latest",
    "INCO_TERM": "incoterm",
    "BUY_NOW_EUR_PER_TON": "buy_now_eur_per_ton",
    "MIN/MAX_BID_EUR_PER_TON": "min_max_bid_eur_per_ton",
    "CO2_PER_TON_MAX_KG": "co2_per_ton_max_kg",
    "VALID_UNTIL": "valid_until"
}

NUMERIC_COLUMNS_SUPPLIER_1 = [
    "thickness_mm", "width_mm", "length_mm", "weight_kg", "quantity",
    "si_content", "mn_content", "p_content", "s_content", "cr_content",
    "ni_content", "mo_content", "v_content", "cu_content", "nb_content",
    "ti_content", "al_content", "b_content", "yield_strength", "tensile_strength", "elongation"
]

NUMERIC_COLUMNS_SUPPLIER_2 = [
    "thickness_mm", "width_mm", "length_mm", "height_mm", "weight_kg",
    "num_coils", "buy_now_eur_per_ton", "min_max_bid_eur_per_ton", "co2_per_ton_max_kg"
]