from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")


def main() -> None:
    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {DATA_DIR.resolve()}")
        print("Download and extract the Olist dataset, then copy CSV files into data/raw/.")
        return

    print(f"Found {len(csv_files)} CSV files\n")

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            print("=" * 72)
            print(f"File: {file.name}")
            print(f"Rows: {len(df):,}")
            print(f"Columns: {len(df.columns)}")
            print("Column names:", df.columns.tolist())
            print("\nMissing values by column:")
            missing = df.isna().sum()
            print(missing[missing > 0].to_string() if missing.any() else "None")
            print(f"Duplicate rows: {df.duplicated().sum():,}")
            print()
        except Exception as exc:
            print(f"Could not inspect {file.name}: {exc}")


if __name__ == "__main__":
    main()
