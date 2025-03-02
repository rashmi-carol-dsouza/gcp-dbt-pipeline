WITH buyers AS (
    SELECT 
        buyer_id,
        preferred_grade,
        preferred_finish,
        preferred_thickness_mm,
        preferred_width_mm,
        max_weight_kg,
        min_quantity
    FROM {{ ref('buyers') }}
),

suppliers AS (
    SELECT 
        supplier AS supplier_name,
        grade,
        finish,
        thickness,
        width,
        gross_weight_kg,
        quantity
    FROM {{ ref('suppliers') }}
)

SELECT
    b.buyer_id,
    s.supplier_name,
    s.grade,
    s.finish,
    s.thickness,
    s.width,
    s.gross_weight_kg,
    s.quantity
FROM buyers b
JOIN suppliers s
ON TRIM(b.preferred_grade) = TRIM(s.grade)
AND TRIM(s.finish) LIKE '%' || TRIM(b.preferred_finish) || '%'
AND (s.thickness IS NULL OR s.thickness >= b.preferred_thickness_mm)
AND (s.width IS NULL OR s.width >= b.preferred_width_mm)
AND (s.gross_weight_kg IS NULL OR s.gross_weight_kg <= b.max_weight_kg)
AND (s.quantity IS NULL OR s.quantity >= b.min_quantity)
ORDER BY 
    (s.thickness - b.preferred_thickness_mm) ASC,
    (s.width - b.preferred_width_mm) ASC
