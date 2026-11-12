--product category that generates highest revenue
SELECT product_category, SUM(total_amount) AS revenue
    FROM sales GROUP BY product_category ORDER BY revenue DESC;

--gender that contributes more to revenue
SELECT gender, SUM(total_amount) AS revenue
    FROM sales GROUP BY gender ORDER BY revenue DESC;

--age group that spends more
SELECT
    CASE
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '56+'
    END AS age_group,
    SUM(total_amount) AS total_revenue
    FROM sales GROUP BY age_group ORDER BY total_revenue DESC;

--top 10 highest value transactions
SELECT transaction_id,customer_id,product_category,total_amount
    FROM sales ORDER BY total_amount DESC LIMIT 10;

--revenue of each customer
SELECT customer_id, SUM(total_amount) AS customer_revenue,
    COUNT(*) AS total_transactions FROM sales 
    GROUP BY customer_id ORDER BY customer_revenue DESC LIMIT 10;

--month-wise revenue
SELECT
    strftime('%Y-%m',date) AS sales_month, COUNT(*) AS total_transactions,
    SUM(total_amount) AS monthly_revenue
FROM sales GROUP BY sales_month ORDER BY sales_month;

--month-wise average transaction value
SELECT
    strftime('%Y-%m',date) AS sales_month, COUNT(*) AS total_transactions,
    SUM(total_amount) AS monthly_revenue, ROUND(AVG(total_amount),2) AS average_transaction_value
FROM sales GROUP BY sales_month ORDER BY sales_month;

--average spending per customer
SELECT ROUND(AVG(customer_revenue),2) AS average_customer_spending
FROM (
    SELECT 
        customer_id, SUM(total_amount) AS customer_revenue
    FROM sales GROUP BY customer_id
    );

--average trasaction value of each category
SELECT 
    product_category,ROUND(AVG(total_amount),2) AS average_transaction_value
FROM sales
GROUP BY product_category ORDER by average_transaction_value DESC;
