import os
import psycopg2
import time
from dotenv import load_dotenv
from pos_stream import generate_transaction  # uses your existing generator

load_dotenv()
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

conn = psycopg2.connect(SUPABASE_DB_URL)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions_stream_test (
    transaction_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    customer_name TEXT,
    county TEXT,
    category TEXT,
    product TEXT,
    revenue FLOAT,
    payment_method TEXT
);
""")
conn.commit()

for i in range(10):
    record = generate_transaction(i)
    cursor.execute("""
        INSERT INTO transactions_stream_test (timestamp, customer_name, county, category, product, revenue, payment_method)
        VALUES (%(Timestamp)s, %(CustomerName)s, %(County)s, %(Category)s, %(Product)s, %(Revenue)s, %(PaymentMethod)s)
    """, record)
    conn.commit()
    print(f"✅ Inserted transaction {i+1}")
    time.sleep(0.5)

cursor.close()
conn.close()
