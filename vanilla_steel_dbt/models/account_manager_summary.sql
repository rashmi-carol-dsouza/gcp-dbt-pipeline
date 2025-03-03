SELECT 
    COALESCE(buyer_am, supplier_am) AS account_manager, 
    COUNT(DISTINCT deal_id) AS total_deals,
    SUM(
        CASE 
            WHEN buyer_am IS NOT NULL AND supplier_am IS NOT NULL THEN booked_gross_revenue 
            ELSE booked_gross_revenue / 2 
        END
    ) AS revenue_managed
FROM {{ source('vanilla_steel', 'deals') }}
WHERE deal_stage IS NOT NULL
GROUP BY account_manager
ORDER BY revenue_managed DESC