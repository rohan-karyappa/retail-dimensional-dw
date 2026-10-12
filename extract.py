import logging
from pyspark.sql.functions import col, to_date
from utils import spark_session, jdbc_url, properties, DATA_DIR, clean_feature_columns, logger

def run_extract(spark=None):
    """
    Ingests raw CSV retail files, cleans schema and data types,
    and writes them into PostgreSQL staging tables (retail_stg schema).
    """
    if spark is None:
        spark = spark_session("ETL-Extract")

    logger.info("Starting Extract phase...")

    # Read and process sales data
    sales_csv = str(DATA_DIR / "sales data-set.csv")
    logger.info(f"Loading sales data from {sales_csv}")
    df_sales = spark.read.csv(sales_csv, header=True, inferSchema=True)
    df_sales_renamed = df_sales.select(
        col("Store").alias("store"),
        col("Dept").alias("dept"),
        to_date(col("Date"), "dd/MM/yyyy").alias("date"),
        col("Weekly_Sales").alias("weekly_sales"),
        col("IsHoliday").alias("isholiday")
    )

    # Read and process features data
    features_csv = str(DATA_DIR / "Features data set.csv")
    logger.info(f"Loading features data from {features_csv}")
    df_features = spark.read.csv(features_csv, header=True, inferSchema=True)
    df_features_cleaned = clean_feature_columns(df_features)

    df_features_renamed = df_features_cleaned.select(
        col("Store").alias("store"),
        to_date(col("Date"), "dd/MM/yyyy").alias("date"),
        col("Temperature").alias("temperature"),
        col("Fuel_Price").alias("fuel_price"),
        col("MarkDown1").alias("markdown1"),
        col("MarkDown2").alias("markdown2"),
        col("MarkDown3").alias("markdown3"),
        col("MarkDown4").alias("markdown4"),
        col("MarkDown5").alias("markdown5"),
        col("CPI").alias("cpi"),
        col("Unemployment").alias("unemployment"),
        col("IsHoliday").alias("isholiday")
    )

    # Read and process store data
    stores_csv = str(DATA_DIR / "stores data-set.csv")
    logger.info(f"Loading store data from {stores_csv}")
    df_store = spark.read.csv(stores_csv, header=True, inferSchema=True)
    df_store_renamed = df_store.select(
        col("Store").alias("store"),
        col("Type").alias("type"),
        col("Size").alias("size")
    )

    # Write to staging layer in PostgreSQL (overwrite ensures idempotency)
    logger.info("Writing cleaned data to PostgreSQL staging layer (retail_stg)...")
    df_store_renamed.write.jdbc(jdbc_url, "retail_stg.stores", mode="overwrite", properties=properties)
    df_features_renamed.write.jdbc(jdbc_url, "retail_stg.features", mode="overwrite", properties=properties)
    df_sales_renamed.write.jdbc(jdbc_url, "retail_stg.sales", mode="overwrite", properties=properties)

    logger.info("Extract phase completed successfully.")

if __name__ == "__main__":
    run_extract()