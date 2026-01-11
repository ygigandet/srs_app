# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd

# Connect to DuckDB
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# Global exercise definitions
# ------------------------------------------------------------
data = {
    "theme": [
        "cross_join",
        "cross_join",
        "left_join",
        "left_join",
        "inner_join",
        "inner_join",
        "full_outer_join"
    ],
    "exercise_name": [
        "beverages_and_food",
        "sizes_trademarks",
        "orders_details",
        "customers_orders",
        "orders_details_ij",
        "salaries_seniority",
        "stores_products_details",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["orders", "customers", "products", "details"],
        ["orders", "customers", "products", "details"],
        ["orders", "customers", "products", "details"],
        ["salaries", "seniority"],
        ["customers_stores_products", "products_fo"],
    ],
    "instructions": [
        "beverages_and_food.txt",
        "sizes_trademarks.txt",
        "orders_details.txt",
        "customers_orders.txt",
        "orders_details_ij.txt",
        "salary_seniority.txt",
        "stores_products_details.txt",
    ],
    "answer": [
        "beverages_and_food.sql",
        "sizes_trademarks.sql",
        "orders_details.sql",
        "customers_orders.sql",
        "orders_details_ij.sql",
        "salary_seniority.sql",
        "stores_products_details.sql",
    ],
}

exercises_df = pd.DataFrame(data)

# Create exercises table
con.execute(
    """
CREATE TABLE IF NOT EXISTS exercises (
    theme TEXT,
    exercise_name TEXT,
    tables TEXT[],
    instructions TEXT,
    answer TEXT,
    PRIMARY KEY (theme, exercise_name)
)
"""
)

# Insert exercises
con.execute("INSERT OR IGNORE INTO exercises SELECT * FROM exercises_df")

# ------------------------------------------------------------
# USER PROGRESS TABLE
# ------------------------------------------------------------
con.execute(
    """
CREATE TABLE IF NOT EXISTS user_progress (
    user_id TEXT,
    exercise_name TEXT,
    last_reviewed DATE,
    PRIMARY KEY (user_id, exercise_name)
)
"""
)

# ------------------------------------------------------------
# EXERCISES TABLES
# ------------------------------------------------------------

# CROSS JOIN exercises
BEVERAGES_CSV = """beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(BEVERAGES_CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

FOOD_CSV = """food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(FOOD_CSV))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

SIZES_CSV = """size
XS
S
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(SIZES_CSV))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

TRADEMARKS_CSV = """trademark
Patagonia
Picture
Nike
"""
trademarks = pd.read_csv(io.StringIO(TRADEMARKS_CSV))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

# LEFT JOIN exercises
ORDERS_DF = pd.DataFrame(
    {"order_id": [1, 2, 3, 4, 5], "customer_id": [101, 102, 103, 104, 105]}
)
con.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM ORDERS_DF")

CUSTOMERS_DF = pd.DataFrame(
    {
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
)
con.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM CUSTOMERS_DF")

PRODUCTS_DF = pd.DataFrame(
    {
        "product_id": [101, 103, 104, 105],
        "product_name": ["Laptop", "Ipad", "Livre", "Petitos"],
        "product_price": [800, 400, 30, 2],
    }
)
con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM PRODUCTS_DF")

DETAILS_DF = pd.DataFrame(
    {
        "order_id": [1, 2, 3, 4, 5],
        "product_id": [102, 104, 101, 103, 105],
        "quantity": [2, 1, 3, 2, 1],
    }
)
con.execute("CREATE TABLE IF NOT EXISTS details AS SELECT * FROM DETAILS_DF")

# INNER JOIN exercises
SALARIES_DF = """salary,employee_id
5000,1
6000,2
6200,3
"""
salaries = pd.read_csv(io.StringIO(SALARIES_DF))
con.execute("CREATE TABLE IF NOT EXISTS salaries AS SELECT * FROM salaries")

SENIORITY_CSV = """employee_id,seniority
1,2
2,5
"""
seniority = pd.read_csv(io.StringIO(SENIORITY_CSV))
con.execute("CREATE TABLE IF NOT EXISTS seniority AS SELECT * FROM seniority")

# FULL OUTER JOIN exercises
CUSTOMERS_STORES_PRODUCTS_DATA_DF = {
    "customer_id": [11, 11, 11, 12, 12, 13, 14, 15],
    "customer_name": [
        "Zeinaba",
        "Zeinaba",
        "Zeinaba",
        "Tancrède",
        "Tancrède",
        "Israel",
        "Kaouter",
        "Alan",
    ],
    "store_id": [1, 1, 1, 2, 2, 3, None, 4],
    "product_id": [101, 103, 105, 101, 103, 104, None, 105],
}

customers_stores_products_fo = pd.DataFrame(CUSTOMERS_STORES_PRODUCTS_DATA_DF)
con.execute(
    "CREATE TABLE IF NOT EXISTS customers_stores_products AS "
    "SELECT * FROM customers_stores_products_fo"
)

PRODUCTS_DATA_DF = {
    "product_id": [100, 101, 103, 104],
    "product_name": ["Cherry coke", "Laptop", "Ipad", "Livre"],
    "product_price": [3, 800, 400, 30],
}

products_fo = pd.DataFrame(PRODUCTS_DATA_DF)
con.execute("CREATE TABLE IF NOT EXISTS products_fo AS SELECT * FROM products_fo")

con.close()
