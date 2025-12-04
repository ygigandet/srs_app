SELECT *
FROM orders
LEFT JOIN details
USING (order_id)