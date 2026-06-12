# Vendor Performance Analysis

End-to-end analysis of vendor performance across ~15 million records (~2 GB), identifying procurement inefficiencies and actionable insights for pricing and purchasing strategy.

## Overview

Raw vendor transaction data is ingested into a PostgreSQL database, explored through EDA, tested statistically, and visualized in Power BI. The core question: which vendors are underperforming on volume but overperforming on margin — and what should be done about it?

**Key findings:**
- Several brands show significantly higher profit margins despite lower sales volumes — prime targets for promotional investment
- Correlation analysis surfaced vendor-level inventory risk patterns not visible in aggregate reporting
- Hypothesis tests confirmed profitability differences across vendor tiers are statistically significant

## Stack

| Layer | Tools |
|-------|-------|
| Storage | SQL (PostgreSQL) |
| Analysis | Python — Pandas, NumPy |
| Statistics | SciPy (t-tests, ANOVA) |
| Visualization | Seaborn, Matplotlib, Power BI |
| Notebook | Jupyter |

## Project Structure

```
├── ingestion_db.py                    # Data ingestion pipeline into PostgreSQL
├── Creating_db.ipynb                  # Database schema creation
├── exploratory_data_analysis.ipynb    # EDA — distributions, correlations, outliers
├── vendor_performance_Analysis.ipynb  # Core analysis — profitability, vendor ranking
└── get_vendor_summary.py              # Summary report generator
```

## Methodology

1. **Ingestion** — `ingestion_db.py` loads raw CSVs into a normalized SQL schema
2. **EDA** — correlation matrices, distribution analysis, missing value audit across all records
3. **Hypothesis testing** — t-tests and ANOVA to compare profitability across vendor groups
4. **Vendor ranking** — composite score using margin, volume, and delivery metrics
5. **Reporting** — Power BI dashboard for business-facing summary

## Setup

```bash
pip install pandas numpy seaborn matplotlib scipy sqlalchemy jupyter
```

1. Set your database connection string in `ingestion_db.py`
2. Run `Creating_db.ipynb` to initialize the schema
3. Run `ingestion_db.py` to load data
4. Open `exploratory_data_analysis.ipynb` → `vendor_performance_Analysis.ipynb`
