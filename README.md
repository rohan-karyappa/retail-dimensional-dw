# 🛒 Retail Dimensional Data Warehouse & PySpark ETL Pipeline

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-E25A1C.svg?logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Apache Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-teal.svg)](https://parquet.apache.org/)

An enterprise-grade, end-to-end **ETL (Extract, Transform, Load)** data engineering pipeline built using **PySpark** and **PostgreSQL**. The pipeline processes multi-source retail operational datasets, cleanses and stages raw records, models the data into a **Star Schema Data Warehouse**, and exports analytical tables into columnar **Apache Parquet** format ready for BI visualization and OLAP queries.

---

## 🏗️ Architecture & Data Flow

```text
       ┌────────────────────────┐
       │   Raw Retail Datasets   │  (Sales, Features, Stores CSVs)
       └───────────┬────────────┘
                   │
                   ▼ [1. Extract Phase - PySpark]
       ┌────────────────────────┐
       │  PostgreSQL (Staging)  │  Schema: `retail_stg`
       │  - retail_stg.stores   │  (Cleaned nulls, normalized dates, typed schemas)
       │  - retail_stg.features │
       │  - retail_stg.sales    │
       └───────────┬────────────┘
                   │
                   ▼ [2. Transform Phase - PySpark Dimensional Modeling]
       ┌────────────────────────┐
       │ PostgreSQL (Warehouse) │  Schema: `retail_dw` (Star Schema)
       │  - fact_sales          │  Fact table containing revenue & metrics
       │  - dim_store           │  Store metadata & attributes
       │  - dim_dept            │  Department lookup
       │  - dim_date            │  Calendar dimensions (day, month, year, week)
       │  - dim_feature         │  Economic conditions (CPI, Fuel, Markdowns)
       └───────────┬────────────┘
                   │
                   ▼ [3. Load Phase - Export to Columnar Parquet]
       ┌────────────────────────┐
       │ Analytical Parquet DW  │  Stored in `output/parquet/`
       │  - dim_*.parquet       │  High compression, columnar read performance
       │  - fact_sales.parquet  │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │  Power BI / Analytics  │  Dashboards, KPI tracking, and trend analysis
       └────────────────────────┘
```

---

## 📐 Dimensional Data Model (Star Schema)

The analytical data warehouse follows Kimball star schema methodology to support fast slice-and-dice queries:

| Table | Type | Key Columns | Description |
| :--- | :--- | :--- | :--- |
| **`fact_sales`** | Fact | `store`, `date`, `dept` | Contains `weekly_sales` grain combined with corresponding environmental variables (CPI, Unemployment, Markdowns). |
| **`dim_store`** | Dimension | `store` | Contains store classification (`type`) and square footage (`size`). |
| **`dim_dept`** | Dimension | `dept` | Department lookup dimension. |
| **`dim_date`** | Dimension | `date` | Expanded calendar attributes (`day`, `month`, `year`, `week of year`). |
| **`dim_feature`** | Dimension | `store`, `date` | Regional economic & promotional conditions (temperature, fuel price, markdown promotions 1–5). |

---

## ⚙️ Tech Stack & Key Design Choices

- **PySpark**: Distributed data processing engine utilized for schema inference, data cleansing, feature parsing, and relational star schema modeling.
- **PostgreSQL 15**: Relational staging (`retail_stg`) and data warehouse layer (`retail_dw`).
- **Apache Parquet & PyArrow**: Columnar analytical storage format offering high compression ratios and fast columnar scans for downstream BI tools.
- **Docker Compose**: One-command reproducible local infrastructure containerizing PostgreSQL with automated schema initialization.
- **python-dotenv**: Environment configuration decoupling database credentials from application source code.

---

## 📁 Repository Structure

```text
retail-dimensional-dw/
├── Retail Store Datasets/
│   └── Dataset 1/               # Raw input CSV datasets (sales, features, stores)
├── sql/
│   └── init.sql                 # DDL script initializing staging & dw schemas
├── output/
│   └── parquet/                 # Output directory for exported Parquet tables
├── extract.py                   # Stage 1: Ingests raw CSVs -> PostgreSQL retail_stg
├── transform.py                 # Stage 2: Transforms staging data -> Star schema retail_dw
├── load.py                      # Stage 3: Converts retail_dw tables -> Parquet files
├── utils.py                     # Reusable SparkSession factory, DB configs & cleansing
├── main.py                      # Unified pipeline orchestrator with stage timings
├── docker-compose.yml           # Local PostgreSQL service container
├── requirements.txt             # Python project dependencies
├── .env.example                 # Environment configuration template
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- Docker & Docker Compose (or a local PostgreSQL instance)
- Java 8, 11, or 17 (required by Apache Spark)

### 2. Clone the Repository
```bash
git clone https://github.com/rohan-karyappa/retail-dimensional-dw.git
cd retail-dimensional-dw
```

### 3. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4. Start PostgreSQL with Docker
Spin up PostgreSQL with the required `retail_stg` and `retail_dw` schemas automatically created:
```bash
docker compose up -d
```

### 5. Configure Environment Variables
Copy the environment template:
```bash
cp .env.example .env
```
*(Default settings match the Docker Compose configuration: `localhost:5432`, `user: postgres`, `password: postgres`)*.

---

## 🏃 Running the Pipeline

### Option A: Run the End-to-End Orchestrator (Recommended)
Execute all three stages in sequence with timing metrics and unified SparkSession:
```bash
python main.py
```

### Option B: Run Individual Pipeline Stages
You can also run each stage independently:
```bash
# 1. Ingest raw CSVs to PostgreSQL staging
python extract.py

# 2. Transform staging into Dimensional Data Warehouse
python transform.py

# 3. Export Data Warehouse tables to Parquet
python load.py
```

---

## 📊 Analytics & BI Integration

Once the pipeline completes, analytical tables are available in two formats:
1. **Live PostgreSQL Connection**: Connect Power BI, Tableau, or Metabase directly to the `retail_dw` schema.
2. **Offline Columnar Parquet**: Parquet files stored in `output/parquet/` can be imported directly into Power BI, DuckDB, or AWS Athena for high-speed OLAP queries.

---

## 👤 Author

**Rohan Karyappa**  
- GitHub: [@rohan-karyappa](https://github.com/rohan-karyappa)
