# Retail star schema

A dimensional model to practise joins and BI on: one fact table and four dimensions, 47,051 rows, free and public
domain. A chain of 20 stores across four US regions sells general merchandise to 2,000 loyalty members over
two years, 2024 and 2025.

## The model

    dim_date (731) ─────────┐
    dim_product (400) ──────┼──> fact_sales (43,900)
    dim_customer (2,000) ───┤
    dim_store (20) ─────────┘

`fact_sales` holds one line per product sold, with its date and time of day, quantity, discount, unit price and revenue.
`dim_date` is a full calendar with US holidays.

## What holds, and how it was checked

Measured with DuckDB against these exact files. Full output in `INTEGRITY.txt`.

- **Zero orphaned rows** on all four joins and **zero duplicate keys** in any dimension.
- **Category share of revenue over the two years is exact**: Electronics 42.00%, Home 26.00%, Apparel 20.00%,
  Grocery 12.00%. Each month keeps its own mix around that (electronics run from 32% of a month's revenue to
  57% in December).
- **Monthly revenue lands exactly** on a declared two-year curve, all 24 months to the cent: 82,000.00 in January
  2024, 115,000.00 in December 2024, 148,000.00 in December 2025.
- **Every line adds up**: revenue = quantity × unit_price × (1 − discount_pct) on 100.00% of rows, and the price paid
  stays near the product's list price (5th to 95th percentile 0.91× to 1.21×). 1.3% of lines sell under
  cost after their discount.
- **Dates are in order**: no customer joins before their home store opened, and no sale comes before its customer joined.

That is the point of it: your `GROUP BY` has an answer that is known to be right, so you can check your own SQL instead
of eyeballing whether it looks plausible.

## How it behaves

- The busiest 20% of customers place 61% of the sale lines, and the best-selling product sells 162× as
  often as the median one.
- 89% of lines are at a store in the customer's own city; the rest are visits elsewhere.
- Stores trade 9:00 to 21:00 Monday to Saturday and 10:00 to 18:00 on Sunday. Saturday is the busiest day.
- Seasons move what sells: desk fans peak in July, space heaters in February, gaming consoles and string lights in
  November and December.

The products, prices, costs, seasonal lifts and the revenue curve were authored for this dataset. They are estimates of
how a general-merchandise chain behaves, not figures from a real retailer.

## Things to try

- Revenue by category and region, joining the fact table to two dimensions.
- Month-over-month growth, which should trace the declared curve.
- Gross margin by brand tier (`subcategory` is Premium, Standard or Budget): revenue against quantity × unit_cost.
- Which customers shop away from home, and at which stores?
- Deliberately write the join wrong and watch the totals stop matching.

## Make your own

Made by the Misata engine (seed 21) from a designed world, then turned into a star. To get one shaped like your own
business, with the totals you state, describe it at https://www.misata.studio/app.

## Provenance

No real customer, product, store or transaction exists here, and nothing was sampled from a real dataset. Names and
emails are invented.

Public domain (CC0). No signup, no attribution required.

## The full version

This is a sample. The full version, **Retail Data Warehouse**, is 2,790,852 rows in a star schema of 9 dimensions and 5 facts: 10 stores, 240 products in 31 subcategories, 36,000 loyalty members, 1,163,432 store-item-days, 372,583 baskets, 1,101,202 receipt lines and 10,601 returns, fiscal 2024 and 2025 (4 February 2024 to 31 January 2026) on the NRF 4-5-4 calendar.

See what is in it, with a free preview to load first: https://www.misata.studio/datasets/premium/retail-warehouse?utm_source=free_dataset&utm_medium=readme&utm_content=retail-star-schema
