SELECT 
    buyer_company, 
    buyer_country,
    SUM(booked_gross_revenue) AS total_revenue,
    COUNT(DISTINCT deal_id) AS total_deals,
    DATE_TRUNC(DATE(deal_created_at), MONTH) AS deal_month 
FROM {{ source('vanilla_steel', 'deals') }}  
WHERE deal_stage IS NOT NULL
GROUP BY buyer_company, buyer_country, deal_month
ORDER BY total_revenue DESC