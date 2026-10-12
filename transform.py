from pyspark.sql.functions import col, dayofmonth, month, year, weekofyear
from utils import spark_session, jdbc_url, properties, logger

def run_transform(spark=None):
    """
    Reads staging tables from retail_stg, transforms data into a Dimensional Star Schema
    (Dimensions & Fact Table), and writes them to the data warehouse schema (retail_dw).
    """
    if spark is None:
        spark = spark_session("ETL-Transform")

    logger.info("Starting Transform phase...")

    # Load data from staging tables
    logger.info("Reading data from PostgreSQL staging schema (retail_stg)...")
    df_store = spark.read.jdbc(jdbc_url, "retail_stg.stores", properties=properties)
    df_sales = spark.read.jdbc(jdbc_url, "retail_stg.sales", properties=properties)
    df_features = spark.read.jdbc(jdbc_url, "retail_stg.features", properties=properties)

    # 1. Dimension: Store
    logger.info("Building dim_store dimension...")
    dim_store = df_store.dropDuplicates(["store"])

    # 2. Dimension: Department
    logger.info("Building dim_dept dimension...")
    dim_dept = df_sales.select("dept").dropDuplicates(["dept"])

    # 3. Dimension: Date
    logger.info("Building dim_date dimension...")
    dim_date = df_features.select("date").dropDuplicates(["date"]) \
        .withColumn("day", dayofmonth("date")) \
        .withColumn("month", month("date")) \
        .withColumn("year", year("date")) \
        .withColumn("week", weekofyear("date")) \
        .withColumn("date", col("date").cast("string"))

    # 4. Dimension: Feature (Store & Date Economic Environment)
    logger.info("Building dim_feature dimension...")
    dim_features = df_features.select(
        "store",
        col("date").cast("string").alias("date"),
        "temperature", "fuel_price", "markdown1", "markdown2",
        "markdown3", "markdown4", "markdown5", "cpi", "unemployment", "isholiday"
    )

    # 5. Fact Table: Sales
    logger.info("Building fact_sales fact table...")
    fact_sales = df_sales.alias("s").join(
        df_features.alias("f"),
        on=["store", "date"],
        how="left"
    ).select(
        col("s.store"),
        col("s.date").cast("string").alias("date"),
        col("s.dept"),
        col("s.weekly_sales"),
        col("f.temperature"),
        col("f.fuel_price"),
        col("f.markdown1"),
        col("f.markdown2"),
        col("f.markdown3"),
        col("f.markdown4"),
        col("f.markdown5"),
        col("f.cpi"),
        col("f.unemployment"),
        col("f.isholiday")
    )

    # Write transformed star schema tables to retail_dw schema
    logger.info("Writing dimension and fact tables to PostgreSQL data warehouse (retail_dw)...")
    dim_store.write.jdbc(jdbc_url, "retail_dw.dim_store", mode="overwrite", properties=properties)
    dim_dept.write.jdbc(jdbc_url, "retail_dw.dim_dept", mode="overwrite", properties=properties)
    dim_date.write.jdbc(jdbc_url, "retail_dw.dim_date", mode="overwrite", properties=properties)
    dim_features.write.jdbc(jdbc_url, "retail_dw.dim_feature", mode="overwrite", properties=properties)
    fact_sales.write.jdbc(jdbc_url, "retail_dw.fact_sales", mode="overwrite", properties=properties)

    logger.info("Transform phase completed successfully.")

if __name__ == "__main__":
    run_transform()
