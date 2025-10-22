# generate_transactions_to_csv.py
import random
import csv
from datetime import datetime, timedelta
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

def generate_transaction(transaction_id, timestamp):
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
        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
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

def generate_transactions_to_csv(total_transactions=400000):
    # Define the time range: January 1, 2022 to December 31, 2025
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 10, 30)
    total_days = (end_date - start_date).days + 1

    # Calculate transactions per day to reach ~400,000 transactions
    transactions_per_day = total_transactions // total_days

    # CSV file setup
    csv_file = "techmart_transactions_2022_to_2025.csv"
    headers = [
        "TransactionID", "Timestamp", "CustomerName", "Age", "Gender", "County",
        "Town", "StoreName", "StoreLocation", "Category", "Product", "Brand",
        "UnitsSold", "Discount", "Revenue", "PaymentMethod"
    ]

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        transaction_id = 1
        current_date = start_date

        while current_date <= end_date:
            # Generate transactions for the current day
            for _ in range(transactions_per_day):
                # Randomize time within the day (between 8 AM and 8 PM for store hours)
                random_hour = random.randint(8, 20)
                random_minute = random.randint(0, 59)
                random_second = random.randint(0, 59)
                timestamp = current_date.replace(hour=random_hour, minute=random_minute, second=random_second)

                transaction = generate_transaction(transaction_id, timestamp)
                writer.writerow(transaction)
                transaction_id += 1

            # Move to the next day
            current_date += timedelta(days=1)

        # Handle any remaining transactions to reach exactly 400,000
        while transaction_id <= total_transactions:
            # Use the last day for remaining transactions
            random_hour = random.randint(8, 20)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            timestamp = end_date.replace(hour=random_hour, minute=random_minute, second=random_second)

            transaction = generate_transaction(transaction_id, timestamp)
            writer.writerow(transaction)
            transaction_id += 1

    print(f"Generated {total_transactions} transactions and saved to {csv_file}")

if __name__ == "__main__":
    generate_transactions_to_csv()