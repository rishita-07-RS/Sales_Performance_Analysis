--count records
SELECT COUNT(*) AS total_records FROM sales;

--calculate total revenue
SELECT SUM(total_amount) AS total_revenue FROM sales;

--calculate average transaction value
SELECT ROUND(AVG(total_amount),2) AS average_transaction FROM sales;

--revenue by category
SELECT product_category, SUM(total_amount) AS revenue 
    FROM sales
    GROUP BY product_category
    ORDER BY revenue DESC;