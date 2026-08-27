USE sales_analysis;

-- Q1: How did monthly revenue change compared with the previous month?

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
        LAG(revenue) OVER (ORDER BY month),
        2
    ) AS previous_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / LAG(revenue) OVER (ORDER BY month) * 100,
        2
    ) AS growth_percentage
FROM monthly_sales
ORDER BY month;

-- Q2: Which products have the highest quantity sold?

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

-- Q3: Which day of the week generates the most revenue?

SELECT
    DAYNAME(InvoiceDate) AS day_of_week,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE InvoiceNo NOT LIKE 'C%'
GROUP BY DAYOFWEEK(InvoiceDate), DAYNAME(InvoiceDate)
ORDER BY revenue DESC;

-- Q4: Which hour of the day generates the most revenue?

SELECT
    HOUR(InvoiceDate) AS hour,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
WHERE InvoiceNo NOT LIKE 'C%'
GROUP BY HOUR(InvoiceDate)
ORDER BY revenue DESC;

-- Q5: What is the average revenue per customer by country?

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
ORDER BY average_customer_revenue DESC;

-- Q6: Which customers have the highest average order value?

SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    ROUND(SUM(Quantity * UnitPrice), 2) AS total_revenue,
    ROUND(
        SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo),
        2
    ) AS average_order_value
FROM sales
WHERE CustomerID IS NOT NULL
  AND InvoiceNo NOT LIKE 'C%'
GROUP BY CustomerID
HAVING COUNT(DISTINCT InvoiceNo) >= 2
ORDER BY average_order_value DESC
LIMIT 10;