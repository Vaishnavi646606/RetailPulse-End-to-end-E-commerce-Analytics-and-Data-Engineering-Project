# RetailPulse — End-to-End E-Commerce Analytics & Data Engineering Platform

RetailPulse is a portfolio project for analyzing e-commerce performance and building a repeatable Python ETL pipeline with PostgreSQL and Power BI.

## Tech stack
- Python, Pandas
- PostgreSQL, SQL, pgAdmin
- Power BI Desktop
- Git and GitHub

## Project structure
```text
RetailPulse/
├── data/
│   ├── raw/          # Put the original Olist CSV files here (not committed)
│   └── processed/    # Cleaned/intermediate files (not committed)
├── src/              # Python ETL scripts
├── sql/              # SQL analysis and schema scripts
├── docs/             # Notes, assumptions, architecture
├── screenshots/      # Power BI report screenshots
├── inspect_data.py   # Inspect CSV files in data/raw
├── requirements.txt
├── .gitignore
└── README.md
```

## Day 1 setup (Windows PowerShell)
1. Download and extract the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Copy the extracted CSV files into `data/raw/`.
3. Open this folder in VS Code.
4. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Inspect the CSV files:
   ```powershell
   python inspect_data.py
   ```

## Dataset tables
The Olist dataset includes orders, order items, customers, products, payments, reviews, sellers, geolocation, and category translation data. We will choose and load the core tables during Day 1.

## Current status
- [ ] Dataset downloaded and placed in `data/raw/`
- [ ] Python environment created
- [ ] PostgreSQL database created
- [ ] Core tables loaded
- [ ] SQL analysis queries completed
- [ ] Two Power BI report pages completed

## Notes
- Do not commit API keys, passwords, virtual environments, or raw dataset files.
- Check data quality before dropping or modifying records.
- Validate revenue definitions and joins to avoid double-counting.
