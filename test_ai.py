from src.ai_engine import generate_sql

schema = """
Order_ID INTEGER,
Order_Date DATE,
Customer VARCHAR,
Region VARCHAR,
City VARCHAR,
Product VARCHAR,
Category VARCHAR,
Quantity INTEGER,
Unit_Price DOUBLE,
Discount DOUBLE,
Sales DOUBLE,
Profit DOUBLE,
Payment_Method VARCHAR
"""

question = "What are the total sales by region?"

result = generate_sql(question, schema)

print("\nGenerated SQL:")
print(result)