from pyspark.sql.functions import *
from utils import spark_session, jdbc_url, properties

spark = spark_session("ETL-Transform")

# Load data from staging
df_store = spark.read.jdbc(jdbc_url, "retail_stg.stores", properties=properties)
df_sales = spark.read.jdbc(jdbc_url, "retail_stg.sales", properties=properties)
df_features = spark.read.jdbc(jdbc_url, "retail_stg.features", properties=properties)

# Transformations
dim_store = df_store.dropDuplicates(['store'])
dim_dept = df_sales.select('dept').dropDuplicates(['dept'])
dim_date = df_features.select('date').dropDuplicates(['date']) \
    .withColumn("date", col("date").cast("string")) \
    .withColumn("day", dayofmonth("date")) \
    .withColumn("month", month("date")) \
    .withColumn("year", year("date")) \
    .withColumn("week", weekofyear("date"))

dim_features = df_features.select(
    "store",
    col("date").cast("string").alias("date"),
    "temperature", "fuel_price", "markdown1", "markdown2",
    "markdown3", "markdown4", "markdown5", "cpi", "unemployment", "isholiday"
)

fact_sales = df_sales.alias("s").join(df_features.alias("f"), on=["store", "date"], how="left").select(
    col("s.store"), col("s.date").cast("string").alias("date"), col("s.dept"),
    col("s.weekly_sales"), col("f.temperature"), col("f.fuel_price"),
    col("f.markdown1"), col("f.markdown2"), col("f.markdown3"),
    col("f.markdown4"), col("f.markdown5"), col("f.cpi"),
    col("f.unemployment"), col("f.isholiday")
)

# Load transformed data into data warehouse
dim_store.write.jdbc(jdbc_url, "retail_dw.dim_store", mode="append", properties=properties)
dim_dept.write.jdbc(jdbc_url, "retail_dw.dim_dept", mode="append", properties=properties)
dim_date.write.jdbc(jdbc_url, "retail_dw.dim_date", mode="append", properties=properties)
dim_features.write.jdbc(jdbc_url, "retail_dw.dim_feature", mode="append", properties=properties)
fact_sales.write.jdbc(jdbc_url, "retail_dw.fact_sales", mode="append", properties=properties)
