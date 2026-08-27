USE sales_analysis;

SELECT COUNT(*) AS total_records
FROM sales;
SELECT
    MIN(InvoiceDate) AS first_order,
    MAX(InvoiceDate) AS last_order
FROM sales;