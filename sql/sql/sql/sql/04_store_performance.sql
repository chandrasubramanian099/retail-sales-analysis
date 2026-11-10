-- ============================================
-- 04_store_performance.sql  |  Store Analysis
-- Revenue and ranking by store and region
-- ============================================

SELECT
    s.store_name,
    s.region,
    s.store_type,
    s.store_city,
    COUNT(*)                                        AS total_transactions,
    ROUND(SUM(f.revenue), 2)                        AS total_revenue,
    ROUND(SUM(f.revenue) / COUNT(*), 2)             AS avg_order_value,
    RANK() OVER (ORDER BY SUM(f.revenue) DESC)      AS revenue_rank,
    RANK() OVER (
        PARTITION BY s.region 
        ORDER BY SUM(f.revenue) DESC
    )                                               AS region_rank
FROM fact_sales f
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY s.store_name, s.region, s.store_type, s.store_city
ORDER BY total_revenue DESC;
