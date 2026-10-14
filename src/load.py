
import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

load_dotenv(PROJECT_ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def get_engine():
    """Create a PostgreSQL connection using environment variables."""
    required = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise ValueError(
            f"Missing environment variables in .env: {missing}"
        )

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    return create_engine(database_url, pool_pre_ping=True)


def load_data(data=None):
    """Load processed DataFrames into separate RetailPulse tables."""
    engine = get_engine()

    table_names = [
        "orders",
        "order_items",
        "customers",
        "products",
        "payments",
        "reviews",
    ]

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logging.info("PostgreSQL connection successful.")

        for table_name in table_names:
            if data is not None:
                if table_name not in data:
                    raise ValueError(
                        f"Missing DataFrame for {table_name}"
                    )
                df = data[table_name]
            else:
                csv_path = PROCESSED_DIR / f"{table_name}.csv"

                if not csv_path.exists():
                    raise FileNotFoundError(
                        f"Processed CSV not found: {csv_path}"
                    )

                df = pd.read_csv(csv_path, low_memory=False)

            if df.empty:
                raise ValueError(
                    f"{table_name} is empty; refusing to load it."
                )

            destination = f"retailpulse_{table_name}"

            # Replace only our dedicated reporting table.
            # Existing olist_* tables remain untouched.
            df.to_sql(
                name=destination,
                con=engine,
                schema="public",
                if_exists="replace",
                index=False,
                chunksize=5000,
                method="multi",
            )

            with engine.connect() as connection:
                database_count = connection.execute(
                    text(
                        f'SELECT COUNT(*) FROM public."{destination}"'
                    )
                ).scalar_one()

            if database_count != len(df):
                raise RuntimeError(
                    f"Row-count mismatch for {destination}: "
                    f"expected {len(df)}, got {database_count}"
                )

            logging.info(
                "Loaded %s | Rows verified: %s",
                destination,
                database_count,
            )

        logging.info("All six tables loaded successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    load_data()
