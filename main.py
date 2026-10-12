import time
import sys
from utils import spark_session, logger
from extract import run_extract
from transform import run_transform
from load import run_load

def run_pipeline():
    """
    End-to-end Retail ETL Pipeline Orchestrator.
    Executes Extract, Transform, and Load sequentially using a single SparkSession.
    """
    total_start_time = time.time()
    logger.info("==================================================================")
    logger.info("   Starting Retail Dataset ETL Pipeline (Extract -> Transform -> Load)")
    logger.info("==================================================================")

    spark = None
    try:
        # Initialize single Spark session across all stages
        logger.info("Initializing Apache Spark Session...")
        spark = spark_session("Retail-Dimensional-ETL-Pipeline")

        # 1. Extract Phase
        stage_start = time.time()
        logger.info("--- [STAGE 1/3] EXTRACT: Ingesting CSVs -> PostgreSQL Staging (retail_stg) ---")
        run_extract(spark=spark)
        logger.info(f"--- [STAGE 1/3] Extract completed in {time.time() - stage_start:.2f} seconds ---")

        # 2. Transform Phase
        stage_start = time.time()
        logger.info("--- [STAGE 2/3] TRANSFORM: Building Star Schema -> PostgreSQL DW (retail_dw) ---")
        run_transform(spark=spark)
        logger.info(f"--- [STAGE 2/3] Transform completed in {time.time() - stage_start:.2f} seconds ---")

        # 3. Load Phase
        stage_start = time.time()
        logger.info("--- [STAGE 3/3] LOAD: Exporting Star Schema Tables -> Parquet Files ---")
        run_load(spark=spark)
        logger.info(f"--- [STAGE 3/3] Load completed in {time.time() - stage_start:.2f} seconds ---")

        total_duration = time.time() - total_start_time
        logger.info("==================================================================")
        logger.info(f"Pipeline executed successfully in {total_duration:.2f} seconds!")
        logger.info("==================================================================")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if spark is not None:
            logger.info("Stopping Apache Spark Session...")
            spark.stop()

if __name__ == "__main__":
    run_pipeline()
