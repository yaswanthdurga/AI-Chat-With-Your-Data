import pandas as pd
import random
from datetime import datetime, timedelta

# Make results reproducible
random.seed(42)

# Lists used to generate realistic data
customers = [
    "Rahul Sharma", "Priya Patel", "Amit Kumar", "Sneha Reddy",
    "Arjun Singh", "Ananya Gupta", "Rohan Mehta", "Kavya Nair",
    "Vikram Rao", "Neha Joshi"
]

locations = {
    "North": ["Delhi", "Jaipur", "Chandigarh"],
    "South": ["Bangalore", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Bhubaneswar", "Patna"],
    "West": ["Mumbai", "Pune", "Ahmedabad"]
}

products = {
    "Electronics": {
        "Laptop": 60000,
        "Smartphone": 30000,
        "Monitor": 18000,
        "Tablet": 25000,
        "Headphones": 5000
    },
    "Accessories": {
        "Keyboard": 2500,
        "Mouse": 1500,
        "Webcam": 4000,
        "USB Hub": 2000,
        "Laptop Stand": 3000
    },
    "Office": {
        "Office Chair": 12000,
        "Desk": 15000,
        "Desk Lamp": 3000,
        "Notebook": 500,
        "Backpack": 2500
    }
}

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash"
]

start_date = datetime(2025, 1, 1)

records = []

for order_id in range(1, 1001):

    region = random.choice(list(locations.keys()))
    city = random.choice(locations[region])

    category = random.choice(list(products.keys()))
    product = random.choice(list(products[category].keys()))

    base_price = products[category][product]

    quantity = random.randint(1, 5)

    discount = random.choice([
        0,
        0.05,
        0.10,
        0.15,
        0.20
    ])

    unit_price = base_price

    sales = unit_price * quantity
    discount_amount = sales * discount
    final_sales = sales - discount_amount

    cost = final_sales * random.uniform(0.60, 0.85)
    profit = final_sales - cost

    order_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    records.append({
        "Order_ID": order_id,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer": random.choice(customers),
        "Region": region,
        "City": city,
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": round(final_sales, 2),
        "Profit": round(profit, 2),
        "Payment_Method": random.choice(payment_methods)
    })


# Create DataFrame
df = pd.DataFrame(records)

# Save dataset
output_path = "data/sales.csv"

df.to_csv(output_path, index=False)

print("Sales dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")