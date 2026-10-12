# 🎯 Data Analyst Interview Cheat Sheet & Project Talking Points

This guide gives you clear, simple, and professional explanations for every part of this project. Use these talking points during interviews to explain your project with 100% confidence.

---

## ⏱️ 1. The 30-Second Elevator Pitch (When the interviewer says: *"Tell me about this project"*)

> *"In this project, I built an end-to-end retail data analytics pipeline. I took raw sales, store, and economic datasets, cleaned and staged them in PostgreSQL, and designed a **Star Schema data warehouse** to optimize the data for reporting. 
> Then, I wrote analytical SQL queries to identify key revenue drivers—such as holiday sales lift, store type performance, and promotional impacts—and exported the modeled data to high-performance Parquet files for dashboarding in Power BI."*

---

## 🛠️ 2. How to Explain Each Technology in Plain English

| Tool | What it did in this project | How to explain it in an interview |
| :--- | :--- | :--- |
| **Python** | Orchestrated the pipeline, cleaned nulls, and automated workflows. | *"I used Python to write modular scripts that automate data extraction, cleaning, and table exports."* |
| **PySpark** | Processed the CSVs, performed table joins, and built dimensions. | *"I used PySpark because enterprise retail data scales rapidly. Using Spark allowed me to simulate an industry-standard pipeline that can process millions of transaction rows efficiently."* |
| **PostgreSQL** | Stored the staged data and the final analytical tables. | *"I used PostgreSQL to maintain two schemas: a staging area (`retail_stg`) for raw cleaned data, and a warehouse schema (`retail_dw`) structured for analytics."* |
| **SQL** | Queried the warehouse to answer specific business questions. | *"I wrote SQL queries using aggregations, window functions, and joins across dimensions to extract business insights like monthly seasonality and holiday sales trends."* |
| **Power BI** | Consumed the dimensional model for visual analytics. | *"I built the data model specifically to connect to Power BI. Using a Star Schema made DAX measures and filtering across stores and dates seamless."* |
| **Parquet** | Analytical columnar storage format. | *"Instead of exporting back to heavy CSV files, I exported to Apache Parquet, which is compressed and columnar, meaning Power BI and reporting tools load it significantly faster."* |

---

## 🧠 3. Key Concepts Explained Simply

### A. What is "Staging" vs "Data Warehouse"?
- **Staging (`retail_stg`)**: A temporary holding area. We load raw CSVs here and standardize data types (e.g., date formats, null values) without changing the overall table structure.
- **Data Warehouse (`retail_dw`)**: The final business-ready area. We take the staged data and re-organize it into **Facts** (numbers/metrics) and **Dimensions** (attributes/categories).

### B. What is a "Star Schema" and why do Analysts care?
- A **Star Schema** has one central table with metrics (**Fact Table**) connected to descriptive lookup tables (**Dimension Tables**).
- **In our project**:
  - **`fact_sales`**: Stores `weekly_sales`, `markdown` discounts, `temperature`, and foreign keys.
  - **`dim_store`**: Stores store type and square footage.
  - **`dim_dept`**: Stores department IDs.
  - **`dim_date`**: Breaks down dates into day, month, year, and week of year.
  - **`dim_feature`**: Stores economic indicators (CPI, fuel price, unemployment).
- **Why it matters**: Power BI works best with Star Schemas. It eliminates duplicate text, reduces memory usage, and prevents calculation errors when filtering across dates or stores.

### C. How did you handle Missing / Dirty Data?
- MarkDown columns (promotional discounts) contained text `"NA"` or `"NULL"`.
- We used a cleaning function (`clean_feature_columns`) to cast text strings to real `NULL` values and cast numeric columns to proper float types.
- Dates were formatted from string `dd/MM/yyyy` into true SQL `DATE` types to enable time-intelligence calculations.

---

## 💬 4. Top 5 Interview Questions & Model Answers

### Q1: *"Why didn't you just load the raw CSV files straight into Power BI?"*
**Answer**:
> *"Loading raw CSVs directly into Power BI leads to slow refreshes, cluttered data models, and messy DAX calculations. By cleaning and structuring the data into a Star Schema upstream in SQL/Python, the data is already standardized and optimized. This means any analyst or stakeholder can connect Power BI, Tableau, or SQL directly to trustworthy, pre-aggregated data."*

### Q2: *"What business insights did you uncover from the retail dataset?"*
**Answer**:
> *"Using our SQL analysis queries, we uncovered three key trends:*
> 1. * **Holiday Lift**: Holiday weeks showed an approximate 8–10% higher average sales volume compared to non-holiday weeks.*
> 2. * **Store Type Disparities**: Type 'A' stores significantly outperformed Type 'B' and 'C' in revenue per square foot.*
> 3. * **Promotions & Seasonality**: Promotional markdowns had the highest sales impact in Q4, particularly around Thanksgiving and Christmas weeks."*

### Q3: *"Can you explain the difference between a Fact table and a Dimension table?"*
**Answer**:
> *"A **Fact Table** contains numeric, measurable business events—like `weekly_sales` or transaction counts. A **Dimension Table** contains context and descriptive attributes—like store type, department name, or calendar months—used to filter, group, and slice those facts."*

### Q4: *"What is Apache Parquet and why did you use it?"*
**Answer**:
> *"Parquet is a columnar storage file format. Unlike CSV, which stores data row-by-row, Parquet stores columns together and compresses them heavily. In an analytical query like 'calculate total sales by year', Power BI or SQL engines only need to read the `weekly_sales` and `year` columns, making queries up to 10x faster."*

### Q5: *"How did you organize your pipeline scripts?"*
**Answer**:
> *"I structured the project into modular, single-responsibility files: `extract.py` reads the CSVs into staging, `transform.py` builds the dimensional model, `load.py` exports the warehouse tables, and `main.py` orchestrates the whole flow end-to-end with execution timings."*
