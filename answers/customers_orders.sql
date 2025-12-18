WITH detailed_orders AS (
SELECT *
FROM orders
LEFT JOIN details
USING (order_id)
)

SELECT customer_id, customer_name, order_id, product_id, quantity
FROM customers
LEFT JOIN detailed_orders
USING (customer_id)