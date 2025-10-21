# pos_stream.py
import random
import time
from datetime import datetime
from name_generator import generate_county_based_name, county_name_mapping

# Product categories aligned with realistic Kenyan brands
categories = {
    "Electronics": {
        "products": [
            "Samsung 43'' Smart TV", "Hisense 32'' TV", "Tecno Camon 30",
            "Infinix Note 40", "Oppo A18"
        ],
        "brands": ["Samsung", "Hisense", "Tecno", "Infinix", "Oppo"]
    },
    "Grocery": {
        "products": [
            "Jogoo Maize Flour 2kg", "Daawat Basmati Rice 5kg", "Kabras Sugar 2kg",
            "Brookside Milk 500ml", "Supa Loaf Bread 400g"
        ],
        "brands": ["Jogoo", "Daawat", "Kabras", "Brookside", "Supa Loaf"]
    },
    "Furniture": {
        "products": ["Wooden Dining Table", "Office Chair", "Sofa Set", "Coffee Table"],
        "brands": ["Victoria Furnitures", "Odds & Ends", "Furniture Palace"]
    },
    "Clothing": {
        "products": ["Safari Boot", "Kitenge Dress", "School Uniform", "Sports Jersey"],
        "brands": ["Bata", "Woolworths", "Mr. Price", "LC Waikiki"]
    },
    "Beverages": {
        "products": [
            "Coca-Cola 500ml", "Keringet Water 1L", "Tusker Lager 500ml",
            "Alvaro 330ml", "Minute Maid Juice 1L"
        ],
        "brands": ["Coca-Cola", "Keringet", "EABL", "Alvaro", "Minute Maid"]
    }
}

def generate_transaction(transaction_id):
    # Pick a random county (which will also act as the town key)
    county = random.choice(list(county_name_mapping.keys()))

    # Generate name based on county
    person = generate_county_based_name(county)

    # Use county name directly as town
    town = county

    # Define store name and store location
    store_name = f"TechMart {town}"
    store_location = f"{town} County"

    # Pick random product category, product, brand
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category]["products"])
    brand = random.choice(categories[category]["brands"])

    # Simulate realistic sale values
    price = round(random.uniform(100, 5000), 2)
    units = random.randint(1, 5)
    discount = round(random.uniform(0, 0.2), 2)
    revenue = round(price * units * (1 - discount), 2)

    # Weighted payment methods (2% Loyalty Points, rest Mpesa or Cash)
    rand_val = random.random()
    if rand_val < 0.02:
        payment = "Loyalty Points"
    else:
        payment = random.choice(["Mpesa", "Cash"])

    return {
        "TransactionID": transaction_id,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "CustomerName": person["full_name"],
        "Age": person["age"],
        "Gender": person["gender"],
        "County": county,
        "Town": town,
        "StoreName": store_name,
        "StoreLocation": store_location,
        "Category": category,
        "Product": product,
        "Brand": brand,
        "UnitsSold": units,
        "Discount": discount,
        "Revenue": revenue,
        "PaymentMethod": payment
    }

def transaction_stream():
    transaction_id = 1
    while True:
        yield generate_transaction(transaction_id)
        transaction_id += 1
        time.sleep(1)

