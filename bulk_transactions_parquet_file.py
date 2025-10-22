# generate_transactions_to_csv_and_parquet.py
import random
import csv
import os
import pandas as pd
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
    county = random.choice(list(county_name_mapping.keys()))
    person = generate_county_based_name(county)
    town = county
    store_name = f"TechMart {town}"
    store_location = f"{town} County"
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category]["products"])
    brand = random.choice(categories[category]["brands"])
    price = round(random.uniform(100, 5000), 2)
    units = random.randint(1, 5)
    discount = round(random.uniform(0, 0.2), 2)
    revenue = round(price * units * (1 - discount), 2)
    rand_val = random.random()
    payment = "Loyalty Points" if rand_val < 0.02 else random.choice(["Mpesa", "Cash"])

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

def generate_transactions_to_files(total_transactions=400000):
    # Define the time range: January 1, 2022 to October 30, 2025
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 10, 30)
    total_days = (end_date - start_date).days + 1

    # Calculate transactions per day
    transactions_per_day = total_transactions // total_days

    # File paths in the current directory
    csv_file = os.path.join(os.getcwd(), "techmart_transactions_2022_to_2025.csv")
    parquet_file = os.path.join(os.getcwd(), "techmart_transactions_2022_to_2025.parquet")

    # Initialize headers and transaction list for Parquet
    headers = [
        "TransactionID", "Timestamp", "CustomerName", "Age", "Gender", "County",
        "Town", "StoreName", "StoreLocation", "Category", "Product", "Brand",
        "UnitsSold", "Discount", "Revenue", "PaymentMethod"
    ]
    transactions = []

    # Write CSV and collect transactions
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            transaction_id = 1
            current_date = start_date

            while current_date <= end_date:
                for _ in range(transactions_per_day):
                    random_hour = random.randint(8, 20)
                    random_minute = random.randint(0, 59)
                    random_second = random.randint(0, 59)
                    timestamp = current_date.replace(hour=random_hour, minute=random_minute, second=random_second)

                    transaction = generate_transaction(transaction_id, timestamp)
                    writer.writerow(transaction)
                    transactions.append(transaction)
                    transaction_id += 1
                current_date += timedelta(days=1)

            # Handle remaining transactions
            while transaction_id <= total_transactions:
                random_hour = random.randint(8, 20)
                random_minute = random.randint(0, 59)
                random_second = random.randint(0, 59)
                timestamp = end_date.replace(hour=random_hour, minute=random_minute, second=random_second)

                transaction = generate_transaction(transaction_id, timestamp)
                writer.writerow(transaction)
                transactions.append(transaction)
                transaction_id += 1

        print(f"Generated {total_transactions} transactions and saved to {csv_file}")

        # Convert transactions to DataFrame and write to Parquet
        df = pd.DataFrame(transactions)
        df.to_parquet(parquet_file, engine='pyarrow', index=False)
        print(f"Generated {total_transactions} transactions and saved to {parquet_file}")

    except Exception as e:
        print(f"Error writing files: {e}")

if __name__ == "__main__":
    generate_transactions_to_files()