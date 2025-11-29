SELECT *
FROM clients
LEFT JOIN orders
USING (customer_id)