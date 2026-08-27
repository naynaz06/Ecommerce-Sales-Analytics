from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# # Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="*******",
#     database="sales_analysis"
# )

# print("MySQL connection successful!")
# Q2: Monthly Revenue Trend

query = """
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
    SUM(Quantity * UnitPrice) AS monthly_revenue
FROM sales
GROUP BY month
ORDER BY month;
"""

monthly_revenue = pd.read_sql(query, conn)

print(monthly_revenue)
# Create Monthly Revenue Trend chart

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_revenue["month"],
    monthly_revenue["monthly_revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
output_path = os.path.join(
    os.path.dirname(__file__),
    "monthly_revenue.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Chart saved to:", output_path)

plt.show()

# Q3: Top 10 Countries by Revenue

query = """
SELECT
    Country,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;
"""

country_revenue = pd.read_sql(query, conn)

print("\nTop 10 countries by revenue:")
print(country_revenue)
# Create Top 10 Countries by Revenue chart

plt.figure(figsize=(10, 6))

plt.barh(
    country_revenue["Country"],
    country_revenue["revenue"]
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_countries_revenue.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Country revenue chart saved to:", output_path)

plt.show()

# Q4: Top 10 Products by Revenue

query = """
SELECT
    StockCode,
    Description,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE InvoiceNo NOT LIKE 'C%'
  AND StockCode NOT IN (
      'DOT',
      'POST',
      'BANK CHARGES',
      'AMAZONFEE',
      'SAMPLES',
      'M',
      'D'
  )
GROUP BY StockCode, Description
ORDER BY revenue DESC
LIMIT 10;
"""

product_revenue = pd.read_sql(query, conn)

print("\nTop 10 products by revenue:")
print(product_revenue)
# Create Top 10 Products by Revenue chart

plt.figure(figsize=(10, 6))

plt.barh(
    product_revenue["Description"],
    product_revenue["revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_products_revenue.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Product revenue chart saved to:", output_path)

plt.show()

# Q1: Top 10 Customers by Revenue

query = """
SELECT
    CustomerID,
    SUM(Quantity * UnitPrice) AS total_revenue
FROM sales
WHERE CustomerID IS NOT NULL
  AND InvoiceNo NOT LIKE 'C%'
GROUP BY CustomerID
ORDER BY total_revenue DESC
LIMIT 10;
"""

customer_revenue = pd.read_sql(query, conn)

print("\nTop 10 customers by revenue:")
print(customer_revenue)
# Create Top 10 Customers by Revenue chart

plt.figure(figsize=(10, 6))

plt.barh(
    customer_revenue["CustomerID"].astype(str),
    customer_revenue["total_revenue"]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Customer ID")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_customers_revenue.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Customer revenue chart saved to:", output_path)

plt.show()

# Q3: Top 10 Customers by Number of Orders

query = """
SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS total_orders
FROM sales
WHERE CustomerID IS NOT NULL
  AND InvoiceNo NOT LIKE 'C%'
GROUP BY CustomerID
ORDER BY total_orders DESC
LIMIT 10;
"""

customer_orders = pd.read_sql(query, conn)

print("\nTop 10 customers by number of orders:")
print(customer_orders)
# Create Top 10 Customers by Order Frequency chart

plt.figure(figsize=(10, 6))

plt.barh(
    customer_orders["CustomerID"].astype(str),
    customer_orders["total_orders"]
)

plt.title("Top 10 Customers by Number of Orders")
plt.xlabel("Number of Orders")
plt.ylabel("Customer ID")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_customers_orders.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Customer order chart saved to:", output_path)

plt.show()

# Q4: Repeat vs One-Time Customers

query = """
SELECT
    customer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS total_orders
    FROM sales
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
    GROUP BY CustomerID
) AS customer_orders
CROSS JOIN (
    SELECT 'Repeat Customer' AS customer_type
    UNION ALL
    SELECT 'One-Time Customer'
) AS types
WHERE
    (customer_type = 'Repeat Customer' AND total_orders > 1)
    OR
    (customer_type = 'One-Time Customer' AND total_orders = 1)
GROUP BY customer_type;
"""

customer_type = pd.read_sql(query, conn)

print("\nRepeat vs One-Time Customers:")
print(customer_type)
# Create Repeat vs One-Time Customers chart

plt.figure(figsize=(8, 5))

plt.bar(
    customer_type["customer_type"],
    customer_type["customer_count"]
)

plt.title("Repeat vs One-Time Customers")
plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "repeat_vs_onetime_customers.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Customer type chart saved to:", output_path)

plt.show()

# Q1: Month-over-Month Revenue Growth

query = """
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
        SUM(Quantity * UnitPrice) AS revenue
    FROM sales
    WHERE InvoiceNo NOT LIKE 'C%'
    GROUP BY month
)

SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / LAG(revenue) OVER (ORDER BY month) * 100,
        2
    ) AS growth_percentage
FROM monthly_sales
ORDER BY month;
"""

monthly_growth = pd.read_sql(query, conn)

print("\nMonthly revenue growth:")
print(monthly_growth)
# Create Month-over-Month Revenue Growth chart

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_growth["month"],
    monthly_growth["growth_percentage"],
    marker="o"
)

plt.axhline(0, linestyle="--")

plt.title("Month-over-Month Revenue Growth")
plt.xlabel("Month")
plt.ylabel("Growth (%)")
plt.xticks(rotation=45)
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "monthly_revenue_growth.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Monthly growth chart saved to:", output_path)

plt.show()

# Q2: Top 10 Products by Quantity Sold

query = """
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS total_quantity_sold
FROM sales
WHERE InvoiceNo NOT LIKE 'C%'
  AND StockCode NOT IN (
      'DOT',
      'POST',
      'BANK CHARGES',
      'AMAZONFEE',
      'SAMPLES',
      'M',
      'D'
  )
GROUP BY StockCode, Description
ORDER BY total_quantity_sold DESC
LIMIT 10;
"""

product_quantity = pd.read_sql(query, conn)

print("\nTop 10 products by quantity sold:")
print(product_quantity)
# Create Top 10 Products by Quantity Sold chart

plt.figure(figsize=(10, 6))

plt.barh(
    product_quantity["Description"],
    product_quantity["total_quantity_sold"]
)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_products_quantity.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Product quantity chart saved to:", output_path)

plt.show()

# Q3: Revenue by Day of Week

query = """
SELECT
    DAYNAME(InvoiceDate) AS day_of_week,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE InvoiceNo NOT LIKE 'C%'
GROUP BY DAYOFWEEK(InvoiceDate), DAYNAME(InvoiceDate)
ORDER BY DAYOFWEEK(InvoiceDate);
"""

daily_revenue = pd.read_sql(query, conn)

# Add Saturday with 0 revenue because there were no Saturday transactions
all_days = pd.DataFrame({
    "day_of_week": [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]
})

daily_revenue = all_days.merge(
    daily_revenue,
    on="day_of_week",
    how="left"
)

daily_revenue["revenue"] = daily_revenue["revenue"].fillna(0)

print("\nRevenue by day of week:")
print(daily_revenue)
# Create Revenue by Day of Week chart

plt.figure(figsize=(10, 6))

plt.bar(
    daily_revenue["day_of_week"],
    daily_revenue["revenue"]
)

plt.title("Revenue by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "revenue_by_day_of_week.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Day-of-week chart saved to:", output_path)

plt.show()

# Q4: Revenue by Hour

query = """
SELECT
    HOUR(InvoiceDate) AS hour,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE InvoiceNo NOT LIKE 'C%'
GROUP BY HOUR(InvoiceDate)
ORDER BY hour;
"""

hourly_revenue = pd.read_sql(query, conn)

print("\nRevenue by hour:")
print(hourly_revenue)
# Create Revenue by Hour chart

plt.figure(figsize=(10, 6))

plt.plot(
    hourly_revenue["hour"],
    hourly_revenue["revenue"],
    marker="o"
)

plt.title("Revenue by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Revenue")
plt.xticks(hourly_revenue["hour"])
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "revenue_by_hour.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Hourly revenue chart saved to:", output_path)

plt.show()

# Q5: Average Revenue per Customer by Country

query = """
SELECT
    Country,
    ROUND(
        SUM(Quantity * UnitPrice) / COUNT(DISTINCT CustomerID),
        2
    ) AS average_customer_revenue
FROM sales
WHERE CustomerID IS NOT NULL
  AND InvoiceNo NOT LIKE 'C%'
GROUP BY Country
ORDER BY average_customer_revenue DESC
LIMIT 10;
"""

country_customer_value = pd.read_sql(query, conn)

print("\nTop 10 countries by average customer revenue:")
print(country_customer_value)
# Create Average Customer Revenue by Country chart

plt.figure(figsize=(10, 6))

plt.barh(
    country_customer_value["Country"],
    country_customer_value["average_customer_revenue"]
)

plt.title("Top 10 Countries by Average Customer Revenue")
plt.xlabel("Average Revenue per Customer")
plt.ylabel("Country")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_countries_avg_customer_revenue.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Average customer revenue chart saved to:", output_path)

plt.show()

# Q6: Top 10 Customers by Average Order Value

query = """
SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    SUM(Quantity * UnitPrice) AS total_revenue,
    SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo) AS average_order_value
FROM sales
WHERE CustomerID IS NOT NULL
  AND InvoiceNo NOT LIKE 'C%'
GROUP BY CustomerID
HAVING COUNT(DISTINCT InvoiceNo) >= 2
ORDER BY average_order_value DESC
LIMIT 10;
"""

customer_aov = pd.read_sql(query, conn)

print("\nTop 10 customers by average order value:")
print(customer_aov)
# Create Top 10 Customers by Average Order Value chart

plt.figure(figsize=(10, 6))

plt.barh(
    customer_aov["CustomerID"].astype(str),
    customer_aov["average_order_value"]
)

plt.title("Top 10 Customers by Average Order Value")
plt.xlabel("Average Order Value")
plt.ylabel("Customer ID")
plt.gca().invert_yaxis()
plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "top_10_customers_average_order_value.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Customer AOV chart saved to:", output_path)

plt.show()
