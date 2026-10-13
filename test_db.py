
import psycopg

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="retailpulse",
        user="postgres",
        password=input("Enter your PostgreSQL password: ")
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print("\nDatabase connection successful!")
            print(cur.fetchone()[0])

            cur.execute("SELECT current_database();")
            print("Connected database:", cur.fetchone()[0])

except psycopg.OperationalError as error:
    print("\nDatabase connection failed.")
    print("Check your password, server and database settings.")
    print("Details:", error)
