# Retail Sales Analysis — Star Schema & SQL Analytics

**Author:** Chandra Subramanian  
**Tools:** SQLite · Python · Pandas · Matplotlib  
**Data:** 43,900 transactions · 20 stores · 2,000 customers · 2 years (2024–2025)

---

## Project Overview

End-to-end retail analytics project built on a star schema database.  
I designed and ran 12 business SQL queries across revenue, margin, customer behaviour and store performance — then visualised the findings in Python with dark-mode charts.

---

## Schema — Star Model

**fact_sales:** sale_id, customer_key, store_key, product_key, date_key, time_of_day, category, quantity, discount_pct, revenue, unit_price

---

## Key Findings

### Revenue Overview
| Metric | Value |
|--------|-------|
| Total Revenue | ~$2.9 M |
| Total Transactions | 43,900 |
| Average Order Value | ~$66 |
| Date Range | Jan 2024 – Dec 2025 |

### Revenue by Category
| Category | Revenue Share |
|----------|--------------|
| Electronics | 42% |
| Home | 26% |
| Apparel | 20% |
| Grocery | 12% |

### Revenue by Region
| Region | Revenue | Stores | Rev/Store |
|--------|---------|--------|-----------|
| South | Highest | 5 | Highest |
| East | 2nd | 5 | 2nd |
| West | 3rd | 5 | 3rd |
| North | Lowest | 5 | Lowest |

**Key Insight:** South earns ~3× more per store than North — driven by ONE Flagship store in the South generating $433,654 alone.

### Gross Margin by Tier
| Tier | Margin % |
|------|----------|
| Standard | 35.3% |
| Premium | 32.3% |
| Budget | 29.5% |

### Day of Week Revenue
Saturday is the highest-revenue day. Sunday is lowest.

### Customer Segments
| Segment | Revenue Share |
|---------|--------------|
| Consumer | ~50% |
| Corporate | ~30% |
| Home Office | ~20% |

---

## SQL Queries Written

| # | Business Question |
|---|-------------------|
| Q1 | Total revenue, transactions, AOV |
| Q2 | Revenue by product category |
| Q3 | Monthly revenue trend (MoM growth with LAG) |
| Q4 | Gross margin % by brand tier |
| Q5 | Revenue per store by region |
| Q6 | Top 10 products by revenue |
| Q7 | Gross margin % by subcategory |
| Q8 | Top 10 products by quantity sold |
| Q9 | Top 10 customers by lifetime value |
| Q10 | Store type mix by region (Standard/Outlet/Flagship) |
| Q11 | Revenue by day of week |
| Q12 | Revenue by customer segment |

---

## Charts Generated

| Chart | Description |
|-------|-------------|
| chart_01_category.png | Bar chart — Revenue by Category |
| chart_02_region.png | Bar chart — Revenue by Region |
| chart_03_monthly_trend.png | Line chart — Monthly Revenue Trend |
| chart_04_gross_margin.png | Bar chart — Gross Margin % by Tier |
| chart_05_day_of_week.png | Bar chart — Revenue by Day of Week |
| chart_06_customer_clv.png | Bar chart — Top 10 Customers by CLV |

All charts use a dark-mode design with custom colour palette.

---

## How to Run

**Requirements:** Python 3.x, pandas, matplotlib

```bash
pip install pandas matplotlib
python analysis/run_analysis.py
```

Charts are saved to the `charts/` folder automatically.

---

## Business Takeaways

1. **Electronics dominates** — 42% of revenue; prioritise stock and promotions here
2. **Flagship stores punch far above their weight** — one South Flagship earns more than multiple Standard stores combined
3. **Saturday is peak day** — schedule maximum staff and promotions for Saturday
4. **Standard tier has highest margin** — better profitability than Premium despite lower price
5. **Revenue grew consistently** — MoM growth trend confirms healthy store performance 2024–2025
