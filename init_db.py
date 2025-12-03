# pylint: disable=missing-module-docstring

import io

import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": ["cross_join", "left_join"],
    "exercise_name": ["beverages_and_food", "orders_clients_products_details"],
    "tables": [
        ["beverages", "food_items"],
        ["orders", "clients", "products", "details"],
    ],
    "last_reviewed": ["1970-01-01", "1970-01-01"],
    "title": ["Cross join between two tables", "Left join between three tables"],
    "answer": ["beverages_and_food.sql", "orders_clients_products_details.sql"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

# ------------------------------------------------------------
# LEFT JOIN EXERCISES
# ------------------------------------------------------------

# Orders tables
orders_data = {"order_id": [1, 2, 3, 4, 5], "customer_id": [101, 102, 103, 104, 105]}

df_orders = pd.DataFrame(orders_data)
con.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM df_orders")

# Clients table
clients_data = {
    "customer_id": [101, 102, 103, 104, 105, 106],
    "customer_name": [
        "Toufik",
        "Daniel",
        "Tancrède",
        "Kaouter",
        "Jean-Nicolas",
        "David",
    ],
}

df_customers = pd.DataFrame(clients_data)
con.execute("CREATE TABLE IF NOT EXISTS clients AS SELECT * FROM df_customers")

# Products table
p_names = ["Laptop", "Ipad", "Livre", "Petitos"]
products_data = {
    "product_id": [101, 103, 104, 105],
    "product_name": p_names,
    "product_price": [800, 400, 30, 2],
}

df_products = pd.DataFrame(products_data)
con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM df_products")

# Details table
order_details_data = {
    "order_id": [1, 2, 3, 4, 5],
    "product_id": [102, 104, 101, 103, 105],
    "quantity": [2, 1, 3, 2, 1],
}

df_order_details = pd.DataFrame(order_details_data)
con.execute("CREATE TABLE IF NOT EXISTS details AS SELECT * FROM df_order_details")
