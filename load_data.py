
import csv
import getpass
import re
from pathlib import Path

import psycopg2
from psycopg2 import sql

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"

FILES = {
    "olist_customers": "olist_customers_dataset.csv",
    "olist_geolocation": "olist_geolocation_dataset.csv",
    "olist_order_items": "olist_order_items_dataset.csv",
    "olist_order_payments": "olist_order_payments_dataset.csv",
    "olist_order_reviews": "olist_order_reviews_dataset.csv",
    "olist_orders": "olist_orders_dataset.csv",
    "olist_products": "olist_products_dataset.csv",
    "olist_sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv",
}


def main():
    password = getpass.getpass("PostgreSQL password: ")

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="retailpulse",
        user="postgres",
        password=password,
    )

    try:
        with conn:
            with conn.cursor() as cur:
                for table_name, filename in FILES.items():
                    path = DATA_DIR / filename

                    if not path.is_file():
                        raise FileNotFoundError(f"Missing file: {path}")

                    with path.open(
                        "r", encoding="utf-8-sig", newline=""
                    ) as f:
                        headers = next(csv.reader(f))

                    columns = [
                        re.sub(r"[^a-zA-Z0-9_]", "_", h.strip()).lower()
                        for h in headers
                    ]

                    if len(columns) != len(set(columns)):
                        raise ValueError(
                            f"Duplicate column names in {filename}"
                        )

                    definitions = sql.SQL(", ").join(
                        sql.SQL("{} TEXT").format(sql.Identifier(col))
                        for col in columns
                    )

                    cur.execute(
                        sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
                            sql.Identifier(table_name), definitions
                        )
                    )

                    # Safe to rerun: reload each raw table from its CSV.
                    cur.execute(
                        sql.SQL("TRUNCATE TABLE {}").format(
                            sql.Identifier(table_name)
                        )
                    )

                    copy_query = sql.SQL(
                        "COPY {} ({}) FROM STDIN "
                        "WITH (FORMAT CSV, HEADER TRUE, NULL '')"
                    ).format(
                        sql.Identifier(table_name),
                        sql.SQL(", ").join(
                            sql.Identifier(col) for col in columns
                        ),
                    )

                    with path.open(
                        "r", encoding="utf-8-sig", newline=""
                    ) as f:
                        cur.copy_expert(copy_query.as_string(conn), f)

                    cur.execute(
                        sql.SQL("SELECT COUNT(*) FROM {}").format(
                            sql.Identifier(table_name)
                        )
                    )
                    count = cur.fetchone()[0]
                    print(f"Loaded {table_name}: {count:,} rows")

        print("\nSUCCESS: All 9 CSV files loaded into retailpulse.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
