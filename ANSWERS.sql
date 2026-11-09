-- The questions on misata.studio/datasets/retail-star-schema, each with the query that answers it.
-- Run in DuckDB from this folder: duckdb < ANSWERS.sql

create view dim_customer as select * from 'dim_customer.csv';
create view dim_date as select * from 'dim_date.csv';
create view dim_product as select * from 'dim_product.csv';
create view dim_store as select * from 'dim_store.csv';
create view fact_sales as select * from 'fact_sales.csv';

-- 1. Which category earns most in which region?
-- Top category by region: East Electronics (40.5%), North Electronics (41.7%), South Electronics (43.1%), West Electronics (41.7%).
with r as (
  select s.region, f.category, sum(f.revenue) as revenue
  from fact_sales f
  join dim_store s on s.store_key = f.store_key
  group by s.region, f.category
)
select region, category, round(revenue, 2) as revenue,
       round(100 * revenue / sum(revenue) over (partition by region), 1) as share_pct
from r
order by region, revenue desc;

-- 2. How does revenue grow month over month across two years?
-- $82,000 in 2024-01 to $148,000 in 2025-12, 1.80x over 24 months.
with m as (
  select d.year, d.month, sum(f.revenue) as revenue
  from fact_sales f
  join dim_date d on d.date_key = f.date_key
  group by d.year, d.month
)
select year, month, round(revenue, 2) as revenue,
       round(100 * (revenue / lag(revenue) over (order by year, month) - 1), 1) as growth_pct
from m
order by year, month;

-- 3. What is the gross margin by brand tier (Premium, Standard, Budget)?
-- Standard 35.3%, Premium 32.3%, Budget 29.5% gross margin.
select p.subcategory as tier,
       round(sum(f.revenue), 2) as revenue,
       round(sum(f.quantity * p.unit_cost), 2) as cost,
       round(100 * (1 - sum(f.quantity * p.unit_cost) / sum(f.revenue)), 1) as gross_margin_pct
from fact_sales f
join dim_product p on p.product_key = f.product_key
group by p.subcategory
order by gross_margin_pct desc;

-- 4. Which customers shop away from their home city, and where?
-- The busiest away trip is from Hartford to Austin (60 lines by 23 customers).
select c.city as home_city, s.city as store_city,
       count(*) as lines, count(distinct f.customer_key) as customers
from fact_sales f
join dim_customer c on c.customer_key = f.customer_key
join dim_store s on s.store_key = f.store_key
where c.city <> s.city
group by c.city, s.city
order by lines desc
limit 10;
