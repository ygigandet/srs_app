# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": [
        "cross_join",
        "cross_join",
        "left_join",
        "left_join",
        "inner_join",
        "inner_join",
    ],
    "exercise_name": [
        "beverages_and_food",
        "sizes_trademarks",
        "orders_details",
        "customers_orders",
        "orders_details",
        "salaries_seniority",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["orders", "customers", "products", "details"],
        ["orders", "customers", "products", "details"],
        ["orders", "customers", "products", "details"],
        ["salaries", "seniority"],
    ],
    "last_reviewed": [
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
    ],
    "instructions": [
        "beverages_and_food.txt",
        "sizes_trademarks.txt",
        "orders_details.txt",
        "customers_orders.txt",
        "orders_details_ij.txt",
        "salary_seniority.txt",
    ],
    "answer": [
        "beverages_and_food.sql",
        "sizes_trademarks.sql",
        "orders_details.sql",
        "customers_orders.sql",
        "orders_details_ij.sql",
        "salary_seniority.sql",
    ],
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

CSV3 = """
size
XS
S
M
L
XL
"""

sizes = pd.read_csv(io.StringIO(CSV3))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

CSV4 = """
trademark
Patagonia
Picture
Nike
"""

trademarks = pd.read_csv(io.StringIO(CSV4))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

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
con.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM df_customers")

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

# ------------------------------------------------------------
# INNER JOIN EXERCISES
# ------------------------------------------------------------

CSV5 = """
salary,employee_id
5000,1
6000,2
6200,3
"""

salaries = pd.read_csv(io.StringIO(CSV5))
con.execute("CREATE TABLE IF NOT EXISTS salaries AS SELECT * FROM salaries")

CSV6 = """
employee_id,seniority
1,2
2,5
"""

seniority = pd.read_csv(io.StringIO(CSV6))
con.execute("CREATE TABLE IF NOT EXISTS seniority AS SELECT * FROM seniority")

con.close()
