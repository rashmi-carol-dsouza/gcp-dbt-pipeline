SELECT
    buyer_id,
    preferred_grade,
    preferred_finish,
    preferred_thickness_mm,
    preferred_width_mm,
    max_weight_kg,
    min_quantity
FROM {{ source('vanilla_steel', 'buyer_preferences') }}
