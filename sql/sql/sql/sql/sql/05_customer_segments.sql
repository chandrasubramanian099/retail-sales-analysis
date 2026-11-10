-- ============================================
-- 05_customer_segments.sql  |  Customer Segments
-- Revenue and behaviour by customer segment
-- ============================================

SELECT
    c.customer_segment,
    COUNT(DISTINCT f.customer_key)                  AS total_customers,
    COUNT(*)                                        AS total_transactions,
    ROUND(SUM(f.revenue), 2)                        AS total_revenue,
    ROUND(SUM(f.revenue) / COUNT(*), 2)             AS avg_order_value,
    ROUND(SUM(f.revenue) / 
        COUNT(DISTINCT f.customer_key), 2)          AS revenue_per_customer,
    ROUND(
        COUNT(*) * 1.0 / 
        COUNT(DISTINCT f.customer_key), 1
    )                                               AS avg_transactions_per_customer,
    ROUND(
        SUM(f.revenue) * 100.0
        / SUM(SUM(f.revenue)) OVER (), 1
    )                                               AS revenue_share_pct
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
