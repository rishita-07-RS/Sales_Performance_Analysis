
import pandas as pd
import sqlite3

# 1. Read the CSV file
df = pd.read_csv("data/cleaned_sales.csv")

# 2. Connect to SQLite database
conn = sqlite3.connect("database/sales.db")

# 3. Rename columns for SQL convenience
df.columns = [
    "transaction_id",
    "date",
    "customer_id",
    "gender",
    "age",
    "product_category",
    "quantity",
    "price_per_unit",
    "total_amount"
]

# 4. Import data into SQLite
df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

# 5. Check number of records
count = pd.read_sql_query(
    "SELECT COUNT(*) AS total_records FROM sales",
    conn
)

print(count)

# 6. Close connection
conn.close()

print("CSV imported successfully!")
