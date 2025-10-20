# pos_stream.py
import random
import time
from datetime import datetime
from name_generator import generate_county_based_name

# Product categories and towns (your full version truncated for brevity)
categories = {
    "Electronics": {
        "products": ["Samsung 43'' Smart TV", "Hisense 32'' TV", "Tecno Camon 30"],
        "brands": ["Samsung", "Hisense", "Tecno"]
    },
    "Grocery": {
        "products": ["Jogoo Maize Flour 2kg", "Daawat Basmati Rice 5kg", "Kabras Sugar 2kg"],
        "brands": ["Jogoo", "Daawat", "Kabras"]
    }
}

kenyan_towns = [
    ("Karen", "Nairobi"), ("Likoni", "Mombasa"), ("Kisumu", "Kisumu"), ("Nakuru", "Nakuru")
]

def generate_transaction(transaction_id):
    town, county = random.choice(kenyan_towns)
    person = generate_county_based_name(county)
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category]["products"])
    brand = random.choice(categories[category]["brands"])
    price = round(random.uniform(100, 5000), 2)
    units = random.randint(1, 5)
    discount = round(random.uniform(0, 0.2), 2)
    revenue = round(price * units * (1 - discount), 2)

    return {
        "TransactionID": transaction_id,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "CustomerName": person["full_name"],
        "Age": person["age"],
        "Gender": person["gender"],
        "Town": town,
        "County": county,
        "Category": category,
        "Product": product,
        "Brand": brand,
        "UnitsSold": units,
        "Discount": discount,
        "Revenue": revenue
    }

def transaction_stream():
    transaction_id = 1
    while True:
        yield generate_transaction(transaction_id)
        transaction_id += 1
        time.sleep(1)
