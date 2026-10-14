
from pathlib import Path
import logging
import pandas as pd

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Tables needed for RetailPulse
TABLE_FILES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def extract_data():
    """Read the required raw CSV files into Pandas DataFrames."""
    data = {}

    for table_name, filename in TABLE_FILES.items():
        file_path = RAW_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing file: {file_path}\n"
                "Check that the Olist CSV files are in data/raw/."
            )

        df = pd.read_csv(file_path, low_memory=False)

        data[table_name] = df

        logging.info(
            "Extracted %s | Rows: %s | Columns: %s",
            table_name,
            len(df),
            len(df.columns),
        )

    return data


if __name__ == "__main__":
    extracted_data = extract_data()

    print("\n--- Extraction Summary ---")

    for table_name, df in extracted_data.items():
        print(f"{table_name}: {df.shape}")
