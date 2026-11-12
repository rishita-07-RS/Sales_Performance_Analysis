
import pandas as pd

# 1. Load CSV dataset
df = pd.read_csv("data/cleaned_sales.csv")

# 2. Display first 5 records
print("\nFIRST 5 RECORDS")
print(df.head())

# 3. Check dataset dimensions
print("\nDATASET SHAPE")
print(df.shape)

# 4. Check column names and data types
print("\nDATASET INFORMATION")
df.info()

# 5. Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# 6. Check duplicate records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# 7. Generate statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())


# STEP: DATA CLEANING

# Create a working copy
df_clean = df.copy()

# 1. Remove extra spaces from text columns
text_columns = df_clean.select_dtypes(include="object").columns

for column in text_columns:
    df_clean[column] = df_clean[column].str.strip()

# 2. Convert Date column into datetime format
df_clean["Date"] = pd.to_datetime(
    df_clean["Date"], errors="coerce"
)

# 3. Convert numerical columns into numeric format
numeric_columns = [
    "Age",
    "Quantity",
    "Price per Unit",
    "Total Amount"
]

for column in numeric_columns:
    df_clean[column] = pd.to_numeric(
        df_clean[column], errors="coerce"
    )

# 4. Check missing values after conversion
print("\nMISSING VALUES AFTER CONVERSION")
print(df_clean.isnull().sum())

# 5. Check and remove exact duplicate rows
print("\nDUPLICATES BEFORE CLEANING")
print(df_clean.duplicated().sum())

df_clean = df_clean.drop_duplicates()

print("\nDUPLICATES AFTER CLEANING")
print(df_clean.duplicated().sum())

# 6. Check duplicate transaction IDs
print("\nDUPLICATE TRANSACTION IDs")
print(df_clean["Transaction ID"].duplicated().sum())

# 7. Check whether Total Amount is correct
calculated_amount = (
    df_clean["Quantity"] * df_clean["Price per Unit"]
)

incorrect_amounts = (
    (df_clean["Total Amount"] - calculated_amount).abs() > 0.01
).sum()

print("\nINCORRECT TOTAL AMOUNTS")
print(incorrect_amounts)

# 8. Save cleaned dataset
df_clean.to_csv(
    "data/retail_sales_cleaned.csv",
    index=False
)

print("\nCLEANED DATASET SAVED SUCCESSFULLY!")


# STEP 7: BUSINESS KPI ANALYSIS

print("\n========== BUSINESS KPIs ==========")

# Total revenue
total_revenue = df_clean["Total Amount"].sum()

# Total transactions
total_transactions = df_clean["Transaction ID"].nunique()

# Average transaction value
average_transaction_value = (
    total_revenue / total_transactions
)

# Total quantity sold
total_quantity = df_clean["Quantity"].sum()

print("Total Revenue:", total_revenue)
print("Total Transactions:", total_transactions)
print("Average Transaction Value:", round(average_transaction_value, 2))
print("Total Quantity Sold:", total_quantity)

print("\n========== CATEGORY-WISE REVENUE ==========")

category_sales = (
    df_clean.groupby("Product Category")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
)

print(category_sales)

print("\n========== GENDER-WISE REVENUE ==========")

gender_sales = (
    df_clean.groupby("Gender")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
)

print(gender_sales)

print("\n========== MONTHLY REVENUE ==========")

monthly_sales = (
    df_clean.groupby(df_clean["Date"].dt.to_period("M"))
    .agg(
        total_transactions=("Transaction ID", "nunique"),
        monthly_revenue=("Total Amount", "sum"),
        average_transaction_value=("Total Amount", "mean")
    )
)

print(monthly_sales.round(2))

#data visualization
import matplotlib.pyplot as plt

# CHART 1: Revenue by Product Category

category_sales = (
    df_clean.groupby("Product Category")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
)

category_sales.plot(kind="bar")

plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/category_revenue.png",dpi=300)
plt.show()


# CHART 2: Revenue by Gender

gender_sales = (
    df_clean.groupby("Gender")["Total Amount"]
    .sum()
)

gender_sales.plot(kind="pie", autopct="%1.1f%%")

plt.title("Revenue Distribution by Gender")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/gender_revenue.png",dpi=300)
plt.show()


# CHART 3: Monthly Revenue Trend

monthly_revenue = (
    df_clean.groupby(df_clean["Date"].dt.to_period("M"))["Total Amount"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

monthly_revenue.plot(kind="line", marker="o")

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png",dpi=300)
plt.show()


# CHART 4: Top 10 Customers by Revenue

top_customers = (
    df_clean.groupby("Customer ID")["Total Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

top_customers.plot(kind="barh")

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.savefig("charts/top_customers.png",dpi=300)
plt.show()
