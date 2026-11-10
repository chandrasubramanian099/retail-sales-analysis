-- ============================================
-- 02_monthly_revenue.sql  |  Monthly Trend
-- Revenue and growth rate month over month
-- ============================================

SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.revenue), 2)                        AS monthly_revenue,
    ROUND(SUM(f.revenue) - LAG(SUM(f.revenue)) 
        OVER (ORDER BY d.year, d.month), 2)         AS revenue_change,
    ROUND(
        (SUM(f.revenue) - LAG(SUM(f.revenue)) 
        OVER (ORDER BY d.year, d.month))
        / LAG(SUM(f.revenue)) 
        OVER (ORDER BY d.year, d.month) * 100, 1
    )                                               AS growth_pct
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
