# E-Commerce Sales Analytics

## Project Overview

This project analyzes e-commerce transaction data to understand sales performance, revenue trends, product performance, and customer purchasing behavior.

The project uses Python for data analysis, MySQL for SQL-based analysis, and data visualizations to turn raw sales data into meaningful business insights.


## Dataset

The dataset contains e-commerce transactions with information about:

- Invoice number
- Product code
- Product description
- Quantity purchased
- Invoice date
- Unit price
- Customer ID
- Country

The dataset contains **541,909 transaction records** covering sales from **December 2010 to December 2011** across **38 countries**.


## Tools & Technologies

- **Python** — Data cleaning, analysis, and exploratory data analysis
- **Pandas** — Data manipulation and analysis
- **NumPy** — Numerical operations
- **Matplotlib** — Data visualization
- **MySQL** — SQL-based data analysis
- **Jupyter Notebook** — Analysis workflow and documentation
- **GitHub** — Project version control and portfolio presentation


## Analysis Performed

### Python EDA
- Data inspection and data type analysis
- Missing value analysis
- Duplicate and cancelled transaction analysis
- Revenue calculation and sales trends
- Product and customer-level analysis
- Country-wise sales analysis
- Exploratory visualizations

### SQL Analysis
- Overall sales and revenue analysis
- Monthly revenue trends and growth
- Product performance analysis
- Customer revenue and order behavior
- Revenue by day of week and hour
- Average order value analysis
- Customer segmentation


## Key Business Insights

- Total revenue generated was approximately **9.75 million**.
- **November 2011** recorded the highest monthly revenue at approximately **1.46 million**.
- Revenue increased strongly during **September to November 2011**, with November being the strongest month.
- **Thursday** generated the highest revenue among the observed days of the week.
- **10:00 AM** was the highest-revenue hour, followed closely by **12:00 PM**.
- **REGENCY CAKESTAND 3 TIER** was the highest-revenue product after excluding non-product transaction codes.
- **PAPER CRAFT, LITTLE BIRDIE** had the highest quantity sold, with approximately **81,000 units**.
- The analysis identified **2,845 repeat customers** and **1,494 one-time customers**.
- Customer analysis showed significant differences in purchasing frequency, total revenue, and average order value across customers.


## Visualizations

The project includes visualizations covering:

- Monthly revenue trends
- Revenue by country
- Top products by revenue
- Top customers by revenue
- Top customers by number of orders
- Repeat vs one-time customers
- Month-over-month revenue growth
- Top products by quantity sold
- Revenue by day of week
- Revenue by hour
- Average customer revenue by country
- Top customers by average order value

All visualizations are generated using Python and Matplotlib and are stored in the `visualization/` folder.

## Project Structure

Ecommerce-Sales-Analytics/
│
├── data/
│   └── Online_Retail.xlsx
│
├── notebooks/
│   ├── analysis.ipynb
│   └── mysql_connection.py
│
├── sql/
│   ├── 01_data_overview.sql
│   ├── 02_sales_analysis.sql
│   ├── 03_customer_analysis.sql
│   └── 04_advanced_analysis.sql
│
├── visualization/
│   ├── sql_visualizations.py
│   └── visualization files (.png)
│
└── README.md

