from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from utils import spark_session, jdbc_url, properties, clean_feature_columns

spark = spark_session("ETL-Extract")

# Read and rename sales data
df_sales = spark.read.csv("/DirectoryTo/Dataset 1/sales data-set.csv", header=True, inferSchema=True)
df_sales_renamed = df_sales.select(
    col("Store").alias("store"),
    col("Dept").alias("dept"),
    to_date(col("Date"), "dd/MM/yyyy").alias("date"),
    col("Weekly_Sales").alias("weekly_sales"),
    col("IsHoliday").alias("isholiday")
)

# Read and rename features data
df_features = spark.read.csv("/DirectoryTo/Dataset 1/Features data set.csv", header=True, inferSchema=True)
df_features_cleaned = clean_feature_columns(df_features)

df_features_renamed = df_features_cleaned.select(
    col('Store').alias('store'),
    to_date(col('Date'), "dd/MM/yyyy").alias('date'),
    col('Temperature').alias('temperature'),
    col('Fuel_Price').alias('fuel_price'),
    col('MarkDown1').alias('markdown1'),
    col('MarkDown2').alias('markdown2'),
    col('MarkDown3').alias('markdown3'),
    col('MarkDown4').alias('markdown4'),
    col('MarkDown5').alias('markdown5'),
    col('CPI').alias('cpi'),
    col('Unemployment').alias('unemployment'),
    col('IsHoliday').alias('isholiday')
)

# Read and rename store data
df_store = spark.read.csv("/DirectoryTo/Dataset 1/stores data-set.csv", header=True, inferSchema=True)
df_store_renamed = df_store.select(
    col('Store').alias('store'),
    col('Type').alias('type'),
    col('Size').alias('size')
)

# Write to staging tables (Run once)
df_store_renamed.write.jdbc(jdbc_url, "retail_stg.stores", mode="append", properties=properties)
df_features_renamed.write.jdbc(jdbc_url, "retail_stg.features", mode="append", properties=properties)
df_sales_renamed.write.jdbc(jdbc_url, "retail_stg.sales", mode="append", properties=properties)