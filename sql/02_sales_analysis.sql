USE sales_analysis;

-- Q1: What is the total revenue generated?
SELECT
    SUM(Quantity * UnitPrice) AS total_revenue
FROM sales;


-- Q2: What is the monthly revenue trend?
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
    SUM(Quantity * UnitPrice) AS monthly_revenue
FROM sales
GROUP BY month
ORDER BY month;


-- Q3: Which countries generate the highest revenue?
SELECT
    Country,
    SUM(Quantity * UnitPrice) AS revenue
FROM sales
GROUP BY Country
ORDER BY revenue DESC;


-- Q4: What are the top 10 products by revenue?
-- Q4: What are the top 10 products by revenue?

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