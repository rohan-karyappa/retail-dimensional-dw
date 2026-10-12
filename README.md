# 🛒 Retail Analytics: Data Pipeline, Star Schema Warehouse & Power BI

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboarding-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![SQL](https://img.shields.io/badge/SQL-Analytics-orange.svg?logo=sqlite&logoColor=white)](https://en.wikipedia.org/wiki/SQL)
[![Apache Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-teal.svg)](https://parquet.apache.org/)

An end-to-end retail data analytics project demonstrating data ingestion, data warehousing (Star Schema design), SQL business analytics, and Power BI reporting. The pipeline ingests multi-source retail datasets, cleanses null values and date formats, models the data into a **Kimball Star Schema in PostgreSQL**, and exports analytical tables into columnar **Parquet** files for dashboard consumption.

---

## 🏗️ Project Architecture & Data Flow

```text
       ┌────────────────────────┐
       │   Raw Retail Datasets   │  (Sales, Features, Stores CSVs)
       └───────────┬────────────┘
                   │
                   ▼ [1. Ingestion & Cleansing - Python / PySpark]
       ┌────────────────────────┐
       │  PostgreSQL (Staging)  │  Schema: `retail_stg`
       │  - retail_stg.stores   │  (Standardized dates, cleaned nulls, typed metrics)
       │  - retail_stg.features │
       │  - retail_stg.sales    │
       └───────────┬────────────┘
                   │
                   ▼ [2. Dimensional Modeling - Star Schema]
       ┌────────────────────────┐
       │ PostgreSQL (Warehouse) │  Schema: `retail_dw`
       │  - fact_sales          │  Central fact table (weekly_sales, markdowns)
       │  - dim_store           │  Store types and sizes
       │  - dim_dept            │  Department numbers
       │  - dim_date            │  Calendar attributes (day, month, year, week)
       │  - dim_feature         │  Economic conditions (CPI, Fuel Price, Unemployment)
       └───────────┬────────────┘
                   │
                   ├───────────────────────────────────┐
                   ▼ [3. SQL Analytics]               ▼ [4. BI Consumption]
       ┌────────────────────────┐         ┌────────────────────────┐
       │  Analytical SQL Queries │         │  Power BI Dashboards   │
       │  (Holiday lift, trends, │         │  (Exported Parquet /   │
       │  department revenue)    │         │  Live PostgreSQL DW)   │
       └────────────────────────┘         └────────────────────────┘
```

---

## 📐 Dimensional Data Model (Star Schema)

This data model follows Kimball dimensional modeling to optimize query performance and make DAX calculations simple:

| Table | Type | Primary / Foreign Keys | Description |
| :--- | :--- | :--- | :--- |
| **`fact_sales`** | Fact | `store`, `date`, `dept` | Stores metrics including `weekly_sales`, temperature, fuel price, and markdown promotions. |
| **`dim_store`** | Dimension | `store` | Contains store categorization (`type` A/B/C) and square footage (`size`). |
| **`dim_dept`** | Dimension | `dept` | Department lookup dimension. |
| **`dim_date`** | Dimension | `date` | Calendar dimension with `day`, `month`, `year`, and `week` of the year. |
| **`dim_feature`** | Dimension | `store`, `date` | Regional macroeconomic conditions (CPI, Unemployment, Fuel Price). |

---

## 📊 Business Questions Answered via SQL

The repository includes a ready-to-run analytical SQL suite in [`sql/analysis_queries.sql`](sql/analysis_queries.sql):

1. **Store Performance Analysis**: Compare total revenue and average weekly sales across store formats (`Type A`, `Type B`, `Type C`).
2. **Holiday Impact Analysis**: Quantify sales lift during holiday weeks vs normal operating weeks.
3. **Department Profitability**: Identify the top 10 revenue-generating departments across all retail branches.
4. **Monthly Seasonality**: Track month-over-month revenue trends to identify seasonal peak periods (e.g. Q4 spikes).
5. **Promotional Markdown Effectiveness**: Evaluate the correlation between active promotional markdown campaigns and sales volume.

---

## 📁 Repository Structure

```text
retail-dimensional-dw/
├── Retail Store Datasets/
│   └── Dataset 1/                 # Raw retail CSV files (sales, features, stores)
├── sql/
│   ├── init.sql                   # DDL to initialize retail_stg and retail_dw schemas
│   └── analysis_queries.sql       # Business analytical SQL queries
├── output/
│   └── parquet/                   # Columnar Parquet exports for Power BI
├── extract.py                     # Stage 1: Ingests raw CSVs -> PostgreSQL retail_stg
├── transform.py                   # Stage 2: Transforms staging data -> Star Schema retail_dw
├── load.py                        # Stage 3: Exports retail_dw tables -> Parquet format
├── utils.py                       # Database connection configuration & data cleansing
├── main.py                        # Pipeline runner with execution timings
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.9+
- PostgreSQL database
- Power BI Desktop (for visualizations)

### 2. Setup Environment & Dependencies
```bash
# Clone the repository
git clone https://github.com/rohan-karyappa/retail-dimensional-dw.git
cd retail-dimensional-dw

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install required Python libraries
pip install -r requirements.txt
```

### 3. Configure Database
1. In PostgreSQL, run [`sql/init.sql`](sql/init.sql) to create the schemas:
   ```sql
   CREATE SCHEMA IF NOT EXISTS retail_stg;
   CREATE SCHEMA IF NOT EXISTS retail_dw;
   ```
2. Database connection defaults in `utils.py` point to:
   - Host: `localhost:5432`
   - User: `postgres`
   - Password: `postgres`
   - Database: `postgres`  
   *(You can update credentials in `utils.py` or set standard environment variables).*

### 4. Run the Pipeline
Run the full pipeline with a single command:
```bash
python main.py
```
Or run each stage independently:
```bash
python extract.py     # Ingest CSVs into staging
python transform.py   # Transform staging into Star Schema warehouse
python load.py        # Export analytical tables to Parquet
```

---

## 📈 Power BI Integration

1. Open **Power BI Desktop**.
2. **Connect via Database**: Choose `PostgreSQL database` ➔ connect to `localhost:5432/postgres` ➔ select tables under `retail_dw`.
3. **Connect via Parquet (Offline)**: Choose `Get Data` ➔ `Parquet` ➔ select files from `output/parquet/`.
4. Establish 1-to-many relationships from dimension tables (`dim_store`, `dim_date`, `dim_dept`) to `fact_sales`.

---

## 👤 Author

**Rohan Karyappa**  
- GitHub: [@rohan-karyappa](https://github.com/rohan-karyappa)
