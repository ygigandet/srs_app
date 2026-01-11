SELECT *
FROM customers_stores_products
FULL OUTER JOIN products_fo
USING (product_id)