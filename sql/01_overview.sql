-- ============================================
-- 01_overview.sql  |  Business Overview
-- Total revenue, transactions, AOV, margin
-- ============================================

SELECT
    COUNT(*)                                        AS total_transactions,
    ROUND(SUM(revenue), 2)                          AS total_revenue,
    ROUND(SUM(revenue) / COUNT(*), 2)               AS avg_order_value,
    ROUND(SUM(quantity), 0)                         AS total_units_sold,
    ROUND(
        (SUM(revenue) - SUM(quantity * p.unit_cost))
        / SUM(revenue) * 100, 1
    )                                               AS gross_margin_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key;
