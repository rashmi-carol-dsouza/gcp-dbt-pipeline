WITH supplier_1 AS (
    SELECT
        'Supplier 1' AS supplier,
        quality_choice AS quality,
        grade,
        finish,
        thickness_mm AS thickness,
        width_mm AS width,
        description,
        gross_weight_kg,
        rp02,
        rm,
        quantity,
        ag,
        ai,
        CAST(NULL AS STRING) AS material,
        CAST(NULL AS STRING) AS surface_treatment,
        CAST(NULL AS STRING) AS article_id,
        CAST(NULL AS STRING) AS reserved
    FROM {{ source('vanilla_steel', 'supplier_data_1') }}
),

supplier_2 AS (
    SELECT
        'Supplier 2' AS supplier,
        CAST(NULL AS STRING) AS quality,
        CAST(NULL AS STRING) AS grade,
        CAST(NULL AS STRING) AS finish,
        CAST(NULL AS FLOAT64) AS thickness,
        CAST(NULL AS FLOAT64) AS width,
        description,
        weight_kg AS gross_weight_kg,
        CAST(NULL AS FLOAT64) AS rp02,
        CAST(NULL AS FLOAT64) AS rm,
        quantity,
        CAST(NULL AS FLOAT64) AS ag,
        CAST(NULL AS FLOAT64) AS ai,
        material,
        CASE 
            WHEN description LIKE '%Oiled%' THEN 'Oiled'
            WHEN description LIKE '%Painted%' THEN 'Painted'
            WHEN description LIKE '%Not Oiled%' THEN 'Not Oiled'
            ELSE NULL
        END AS surface_treatment,
        article_id,
        reserved
    FROM {{ source('vanilla_steel', 'supplier_data_2') }}
)

SELECT *
FROM supplier_1
UNION ALL
SELECT *
FROM supplier_2
