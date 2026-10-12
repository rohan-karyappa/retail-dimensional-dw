import pandas as pd
from pyspark.sql.functions import col
from utils import spark_session, jdbc_url, properties, OUTPUT_DIR, logger

def run_load(spark=None):
    """
    Reads dimensional and fact tables from retail_dw schema in PostgreSQL,
    and exports them into high-performance Apache Parquet format.
    Pandas + PyArrow is utilized for local file output to ensure seamless cross-platform
    execution (bypassing native Hadoop winutils filesystem bindings on Windows).
    """
    if spark is None:
        spark = spark_session("ETL-Load")

    logger.info("Starting Load phase (Export to Parquet)...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    tables = ["dim_store", "dim_dept", "dim_date", "dim_feature", "fact_sales"]

    for table in tables:
        logger.info(f"Extracting retail_dw.{table} and converting to Parquet...")
        df = spark.read.jdbc(jdbc_url, f"retail_dw.{table}", properties=properties)

        if "date" in df.columns:
            df = df.withColumn("date", col("date").cast("string"))

        df_pd = df.toPandas()
        output_path = OUTPUT_DIR / f"{table}.parquet"
        df_pd.to_parquet(str(output_path), index=False, engine="pyarrow")
        logger.info(f"Saved {table}.parquet ({len(df_pd):,} rows) to {output_path}")

    logger.info(f"Load phase completed successfully. All Parquet datasets stored in: {OUTPUT_DIR}")

if __name__ == "__main__":
    run_load()