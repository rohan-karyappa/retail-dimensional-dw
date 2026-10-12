import os
import logging
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("RetailETL")

# Load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Retail Store Datasets" / "Dataset 1"
OUTPUT_DIR = BASE_DIR / "output" / "parquet"

# Database Configuration from environment variables with defaults
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

jdbc_url = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
properties = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "driver": "org.postgresql.Driver"
}

def spark_session(app_name="Retail-ETL"):
    """
    Initializes and returns an optimized SparkSession with PostgreSQL JDBC driver.
    """
    hadoop_home = os.getenv("HADOOP_HOME")
    if hadoop_home and os.path.exists(hadoop_home):
        os.environ["HADOOP_HOME"] = hadoop_home

    builder = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.2") \
        .config("spark.hadoop.hadoop.native.io", "false") \
        .config("spark.sql.legacy.timeParserPolicy", "LEGACY")

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark

def clean_feature_columns(df):
    """
    Cleans string representation of nulls ('NULL', 'NA') and casts metrics to float.
    """
    columns = ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5", "CPI", "Unemployment"]
    for col_name in columns:
        if col_name in df.columns:
            df = df.withColumn(
                col_name,
                when((col(col_name) == "NULL") | (col(col_name) == "NA"), None)
                .otherwise(col(col_name))
                .cast("float")
            )
    return df
