SELECT *
FROM orders
LEFT JOIN customers
USING (customer_id)
LEFT JOIN products
USING (product_id);