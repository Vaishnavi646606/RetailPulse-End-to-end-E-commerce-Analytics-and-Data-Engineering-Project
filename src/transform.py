
from pathlib import Path
import logging
import pandas as pd

from extract import extract_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
    "reviews": [
        "review_creation_date",
        "review_answer_timestamp",
    ],
}

NUMERIC_COLUMNS = {
    "order_items": ["price", "freight_value"],
    "payments": [
        "payment_sequential",
        "payment_installments",
        "payment_value",
    ],
    "products": [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "reviews": ["review_score"],
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def transform_data(data):
    """Clean extracted DataFrames without discarding valid records."""
    cleaned_data = {}

    for table_name, original_df in data.items():
        df = original_df.copy()

        rows_before = len(df)

        # Remove only fully identical rows.
        df = df.drop_duplicates()

        duplicates_removed = rows_before - len(df)

        # Standardize text columns without changing missing values.
        
        for column in df.select_dtypes(include=["object", "str"]).columns:
            df[column] = df[column].map(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

        # Convert known date columns.
        for column in DATE_COLUMNS.get(table_name, []):
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce",
                )

        # Convert known numeric columns.
        for column in NUMERIC_COLUMNS.get(table_name, []):
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce",
                )

        cleaned_data[table_name] = df

        logging.info(
            "%s | Before: %s | After: %s | "
            "Exact duplicates removed: %s",
            table_name,
            rows_before,
            len(df),
            duplicates_removed,
        )

        # Report missing values instead of deleting valid records.
        missing = df.isna().sum()
        missing = missing[missing > 0]

        if not missing.empty:
            logging.info(
                "%s | Missing values: %s",
                table_name,
                missing.to_dict(),
            )

    return cleaned_data


def save_processed_data(data):
    """Save each cleaned DataFrame as a CSV file."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for table_name, df in data.items():
        output_path = PROCESSED_DIR / f"{table_name}.csv"

        df.to_csv(output_path, index=False)

        logging.info(
            "Saved %s | Rows: %s | File: %s",
            table_name,
            len(df),
            output_path,
        )


if __name__ == "__main__":
    extracted_data = extract_data()
    transformed_data = transform_data(extracted_data)
    save_processed_data(transformed_data)

    print("\n--- Transformation Complete ---")

    for table_name, df in transformed_data.items():
        print(f"{table_name}: {df.shape}")
