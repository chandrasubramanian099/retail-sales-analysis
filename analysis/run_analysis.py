import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Setup ──────────────────────────────────────────────────────
DB_PATH     = r"C:\Users\chand\Downloads\retail-star-schema\retail-star-schema\retail.db"
CHARTS_DIR  = r"C:\Users\chand\Downloads\retail-star-schema\retail-star-schema\charts"

con = sqlite3.connect(DB_PATH)

DARK   = "#0f1117"
CARD   = "#1a1d27"
ACCENT = "#6c8ebf"
GREEN  = "#5cb85c"
ORANGE = "#f0ad4e"
RED    = "#d9534f"
PURPLE = "#9b59b6"
TEXT   = "#e0e0e0"
GRID   = "#2a2d3a"

plt.rcParams.update({
    "figure.facecolor":  DARK,
    "axes.facecolor":    CARD,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   TEXT,
    "axes.titlecolor":   TEXT,
    "xtick.color":       TEXT,
    "ytick.color":       TEXT,
    "text.color":        TEXT,
    "grid.color":        GRID,
    "grid.linewidth":    0.6,
    "font.family":       "DejaVu Sans",
    "font.size":         11,
})

def save(fig, name):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK)
    plt.close(fig)
    print(f"Saved: {name}")

# ── Chart 1: Revenue by Category ──────────────────────────────
df1 = pd.read_sql("""
    SELECT category,
           ROUND(SUM(revenue), 2) AS total_revenue
    FROM   fact_sales
    GROUP  BY category
    ORDER  BY total_revenue DESC
""", con)

fig, ax = plt.subplots(figsize=(8, 5))
colors = [ACCENT, GREEN, ORANGE, RED]
bars = ax.bar(df1["category"], df1["total_revenue"], color=colors, width=0.5)
ax.bar_label(bars, fmt="$%.0f", padding=5, color=TEXT, fontsize=10)
ax.set_title("Revenue by Category", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Category")
ax.set_ylabel("Total Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
save(fig, "chart_01_category.png")

# ── Chart 2: Revenue by Region ─────────────────────────────────
df2 = pd.read_sql("""
    SELECT ds.region,
           ROUND(SUM(fs.revenue), 2) AS total_revenue
    FROM   fact_sales AS fs
    JOIN   dim_store  AS ds ON fs.store_key = ds.store_key
    GROUP  BY ds.region
    ORDER  BY total_revenue DESC
""", con)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df2["region"], df2["total_revenue"], color=ACCENT, width=0.5)
ax.bar_label(bars, fmt="$%.0f", padding=5, color=TEXT, fontsize=10)
ax.set_title("Revenue by Region", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Region")
ax.set_ylabel("Total Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
save(fig, "chart_02_region.png")

# ── Chart 3: Monthly Revenue Trend ─────────────────────────────
df3 = pd.read_sql("""
    SELECT dd.year, dd.month,
           dd.month_name,
           ROUND(SUM(fs.revenue), 2) AS total_revenue
    FROM   fact_sales AS fs
    JOIN   dim_date   AS dd ON fs.date_key = dd.date_key
    GROUP  BY dd.year, dd.month, dd.month_name
    ORDER  BY dd.year, dd.month
""", con)

df3["label"] = df3["month_name"].str[:3] + " " + df3["year"].astype(str).str[-2:]

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df3["label"], df3["total_revenue"], color=ACCENT,
        linewidth=2.5, marker="o", markersize=5)
ax.fill_between(range(len(df3)), df3["total_revenue"],
                alpha=0.15, color=ACCENT)
ax.set_title("Monthly Revenue Trend — 2024 & 2025",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Month")
ax.set_ylabel("Total Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_xticks(range(len(df3)))
ax.set_xticklabels(df3["label"], rotation=45, ha="right", fontsize=9)
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
save(fig, "chart_03_monthly_trend.png")

# ── Chart 4: Gross Margin by Brand Tier ────────────────────────
df4 = pd.read_sql("""
    SELECT dp.subcategory AS brand_tier,
           ROUND(SUM(fs.revenue - dp.unit_cost * fs.quantity)
                 * 100.0 / SUM(fs.revenue), 1) AS gross_margin_pct
    FROM   fact_sales  AS fs
    JOIN   dim_product AS dp ON fs.product_key = dp.product_key
    GROUP  BY dp.subcategory
    ORDER  BY gross_margin_pct DESC
""", con)

fig, ax = plt.subplots(figsize=(7, 5))
bar_colors = [GREEN, ORANGE, RED]
bars = ax.bar(df4["brand_tier"], df4["gross_margin_pct"],
              color=bar_colors, width=0.4)
ax.bar_label(bars, fmt="%.1f%%", padding=5, color=TEXT, fontsize=11)
ax.set_title("Gross Margin % by Brand Tier", fontsize=14,
             fontweight="bold", pad=15)
ax.set_xlabel("Brand Tier")
ax.set_ylabel("Gross Margin (%)")
ax.set_ylim(0, 45)
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
save(fig, "chart_04_gross_margin.png")

# ── Chart 5: Revenue by Day of Week ────────────────────────────
df5 = pd.read_sql("""
    SELECT dd.day_name, dd.day_of_week,
           ROUND(SUM(fs.revenue) / COUNT(DISTINCT dd.date_key), 2)
               AS revenue_per_day
    FROM   fact_sales AS fs
    JOIN   dim_date   AS dd ON fs.date_key = dd.date_key
    GROUP  BY dd.day_name, dd.day_of_week
    ORDER  BY dd.day_of_week
""", con)

fig, ax = plt.subplots(figsize=(9, 5))
day_colors = [ACCENT if d < 5 else GREEN for d in df5["day_of_week"]]
bars = ax.bar(df5["day_name"], df5["revenue_per_day"],
              color=day_colors, width=0.5)
ax.bar_label(bars, fmt="$%.0f", padding=5, color=TEXT, fontsize=9)
ax.set_title("Average Revenue per Day of Week",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Day")
ax.set_ylabel("Avg Revenue per Day ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)

from matplotlib.patches import Patch
legend = [Patch(color=ACCENT, label="Weekday"),
          Patch(color=GREEN,  label="Weekend")]
ax.legend(handles=legend, loc="upper left")
save(fig, "chart_05_day_of_week.png")

# ── Chart 6: Customer Segment CLV ──────────────────────────────
df6 = pd.read_sql("""
    SELECT dc.segment,
           ROUND(SUM(fs.revenue)
                 / COUNT(DISTINCT dc.customer_key), 2) AS clv
    FROM   fact_sales   AS fs
    JOIN   dim_customer AS dc ON fs.customer_key = dc.customer_key
    GROUP  BY dc.segment
    ORDER  BY clv DESC
""", con)

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(df6["segment"], df6["clv"],
              color=[ACCENT, GREEN, ORANGE], width=0.4)
ax.bar_label(bars, fmt="$%.0f", padding=5, color=TEXT, fontsize=11)
ax.set_title("Customer Lifetime Value by Segment",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Segment")
ax.set_ylabel("Revenue per Customer ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
save(fig, "chart_06_customer_clv.png")

con.close()
print("\n✅ All 6 charts saved to charts/ folder.")