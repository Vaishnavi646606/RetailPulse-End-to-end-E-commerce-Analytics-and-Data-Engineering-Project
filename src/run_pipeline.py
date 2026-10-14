
import logging
import sys
from pathlib import Path

# Allow imports from the src directory
SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from extract import extract_data
from transform import transform_data, save_processed_data
from load import load_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run_pipeline():
    logging.info("Starting RetailPulse ETL pipeline.")

    # 1. Extract
    extracted_data = extract_data()

    # 2. Transform
    transformed_data = transform_data(extracted_data)
    save_processed_data(transformed_data)

    # 3. Load
    load_data(transformed_data)

    logging.info("RetailPulse ETL pipeline completed successfully.")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception:
        logging.exception("RetailPulse ETL pipeline failed.")
        raise
