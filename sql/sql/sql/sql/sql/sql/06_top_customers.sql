-- ============================================
-- 06_top_customers.sql  |  Top 10 Customers
-- Highest value customers by total revenue
-- ============================================

SELECT
    f.customer_key,
    c.customer_segment,
    c.city,
    c.region,
    COUNT(*)                                        AS total_transactions,
    ROUND(SUM(f.revenue), 2)                        AS total_revenue,
    ROUND(SUM(f.revenue) / COUNT(*), 2)             AS avg_order_value,
    ROUND(SUM(f.quantity), 0)                       AS total_units,
    RANK() OVER (ORDER BY SUM(f.revenue) DESC)      AS customer_rank
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY f.customer_key, c.customer_segment, c.city, c.region
ORDER BY total_revenue DESC
LIMIT 10;
