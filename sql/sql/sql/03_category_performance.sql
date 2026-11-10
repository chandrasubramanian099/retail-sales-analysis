-- ============================================
-- 03_category_performance.sql  |  Category Analysis
-- Revenue, margin and share by product category
-- ============================================

SELECT
    p.category,
    COUNT(*)                                        AS total_transactions,
    ROUND(SUM(f.revenue), 2)                        AS total_revenue,
    ROUND(SUM(f.quantity), 0)                       AS total_units,
    ROUND(SUM(f.revenue) / COUNT(*), 2)             AS avg_order_value,
    ROUND(
        (SUM(f.revenue) - SUM(f.quantity * p.unit_cost))
        / SUM(f.revenue) * 100, 1
    )                                               AS gross_margin_pct,
    ROUND(
        SUM(f.revenue) * 100.0
        / SUM(SUM(f.revenue)) OVER (), 1
    )                                               AS revenue_share_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue DESC;
