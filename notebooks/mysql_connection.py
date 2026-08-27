import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# Read Excel file
file_path = "C:\E-Commerce-DataAnalysis\data\Online_Retail.xlsx"
df = pd.read_excel(file_path)

print("Excel file loaded successfully!")
print(df.head())
print(df.shape)
print(df.columns)
load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
# # my sql connection
# import mysql.connector

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="******",
#     database="sales_analysis"
# )

# print("MySQL connection successful!")
# Create cursor
cursor = conn.cursor()

# Create sales table
create_table_query = """
CREATE TABLE IF NOT EXISTS sales (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10,2),
    CustomerID INT,
    Country VARCHAR(100)
)
"""

cursor.execute(create_table_query)
conn.commit()

print("Sales table created successfully!")
# Insert Excel data into MySQL
insert_query = """
INSERT INTO sales
(InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = df.astype(object).where(pd.notnull(df), None).values.tolist()

cursor.executemany(insert_query, data)
conn.commit()

print("Data imported successfully!")
print("Rows inserted:", cursor.rowcount)

cursor.close()
conn.close()

