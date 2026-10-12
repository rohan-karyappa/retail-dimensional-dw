from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

def spark_session(app_name):
    import os
    os.environ["HADOOP_HOME"] = "/DirectoryTo/hadoop-3.2.2"
    return SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.2") \
        .config("spark.hadoop.hadoop.native.io", "false") \
        .getOrCreate()

jdbc_url = "jdbc:postgresql://IP:5432/postgres"
properties = {
    "user": "dbusername",
    "password": "dbpassword",
    "driver": "org.postgresql.Driver"
}

def clean_feature_columns(df):
    columns = ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5", "CPI", "Unemployment"]
    for col_name in columns:
        df = df.withColumn(
            col_name,
            when((col(col_name) == "NULL") | (col(col_name) == "NA"), None).otherwise(col(col_name)).cast("float")
        )
    return df
