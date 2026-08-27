import pandas as pd

from database import create_database, execute_query


# Load our sales dataset
df = pd.read_csv("data/sales.csv")


# Create DuckDB database
connection = create_database(df)


# Test SQL query
query = """
SELECT
    Region,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC
"""


result = execute_query(connection, query)


print("\nSales by Region:")
print(result)