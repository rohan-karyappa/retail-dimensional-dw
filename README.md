# 🛒 Retail ETL Data Pipeline Project

## 📌 Overview

This project demonstrates an **ETL (Extract, Transform, Load)** pipeline built using **PySpark** for processing retail data. It ingests raw CSV files, transforms them into a **star schema**, and stores the results in **PostgreSQL** and **Parquet** format. The transformed data is then ready to be visualized using tools like **Power BI**.

---

## 🗂️ Dataset Sources

The pipeline processes three retail-related datasets:
- `sales data-set.csv` – Weekly sales data by store and department
- `Features data set.csv` – Store-specific promotional and economic data
- `stores data-set.csv` – Store metadata including type and size

---

## ⚙️ Technologies Used

- **PySpark** – Data processing and transformation
- **PostgreSQL** – Relational database used for staging and star schema layers
- **Parquet** – Columnar format for optimized storage
- **Power BI** – Business intelligence tool for dashboarding (optional)
- **Hive/HDFS (optional)** – Extendable for big data storage and analytics
- **pandas** – Used for final Parquet conversion due to Windows compatibility issues

  ---

## 🏗️ Project Workflow

```text
            Raw CSV Files
                   ↓
       ┌─────────────────────┐
       │   Extract (PySpark) │
       └─────────────────────┘
                   ↓
   PostgreSQL (retail_stg schema - staging layer)
                   ↓
       ┌──────────────────────┐
       │  Transform (PySpark) │
       └──────────────────────┘
                   ↓
    PostgreSQL (retail_dw schema - star schema)
                   ↓
       ┌─────────────────────┐
       │   Load (Parquet)    │
       └─────────────────────┘
                   ↓
      Power BI (Visualization)
```

## 📁 Repository Structure
retail-etl-pipeline/
- ├── extract.py                 # Ingests and cleans CSVs, loads into staging
- ├── transform.py              # Transforms staging data to star schema
- ├── load.py                   # Converts PostgreSQL tables to Parquet
- ├── utils.py                  # Reusable Spark & DB config + data cleaning
- ├── /DirectoryTo/Dataset 1/   # Raw input CSV files
- ├── /DirectoryTo/ETL/         # Output Parquet files
- ├── README.md                 # Project documentation


## 🚀 How to Run the Pipeline
⚙️ 1. Configure Database Connection
- Edit utils.py and replace with your PostgreSQL credentials:
jdbc_url = "jdbc:postgresql://<HOST>:5432/<DB_NAME>"
properties = {
    "user": "<USERNAME>",
    "password": "<PASSWORD>",
    "driver": "org.postgresql.Driver"
}

## 📥 2. Extract and Load to Staging (retail_stg)
- python extract.py
- Loads raw CSVs
- Cleans nulls and bad formats
- Writes cleaned data to retail_stg schema in PostgreSQL


## 🔄 3. Transform into Star Schema (retail_dw)
- python transform.py
- Joins and transforms staging tables
- Builds dimension and fact tables
- Loads them into retail_dw schema in PostgreSQL

## 💾 4. Convert Tables to Parquet Format
- python load.py
- Reads tables from retail_dw
- Converts to Parquet using Pandas
- Stores files in /DirectoryTo/ETL/

## 📊 Visualize with Power BI
- Open Power BI Desktop.
- Connect to:
- PostgreSQL → Load tables from retail_dw for live querying.
- Parquet files → Load locally exported Parquet data for offline analysis.
- Build visualizations using dimensions like store, dept, and date, and measures like weekly_sales


## 📬 Contact
- For questions or improvements, feel free to reach out via LinkedIn or raise an issue in the repository.

