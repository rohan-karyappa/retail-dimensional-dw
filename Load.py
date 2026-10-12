import pandas as pd
from utils import spark_session, jdbc_url, properties
from pyspark.sql.functions import col

spark = spark_session("ETL-Load")

# List of tables to convert to Parquet
tables = ["dim_store", "dim_dept", "dim_date", "dim_feature", "fact_sales"]

for table in tables:
    df = spark.read.jdbc(jdbc_url, f"retail_dw.{table}", properties=properties)
    if "date" in df.columns:
        df = df.withColumn("date", col("date").cast("string"))
    df_pd = df.toPandas()
    df_pd.to_parquet(f"/DirectoryTo/ETL/{table}.parquet", index=False, engine="pyarrow")