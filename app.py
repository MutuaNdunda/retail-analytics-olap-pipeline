import os
import json
import psycopg2
import threading
from flask import Flask, render_template, Response, request, jsonify
from dotenv import load_dotenv
from pos_stream import transaction_stream

load_dotenv()

app = Flask(__name__)
ADMIN_PIN = os.getenv("ADMIN_PIN")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

is_streaming_to_db = False  # Global flag

def stream_to_db():
    """Continuously writes POS transactions to Supabase PostgreSQL."""
    global is_streaming_to_db
    conn = psycopg2.connect(SUPABASE_DB_URL)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            customer_name TEXT,
            age INT,
            gender TEXT,
            county TEXT,
            town TEXT,
            store_name TEXT,
            category TEXT,
            product TEXT,
            units_sold INT,
            discount FLOAT,
            revenue FLOAT,
            payment_method TEXT
        );
    """)
    conn.commit()

    for record in transaction_stream():
        if not is_streaming_to_db:
            break

        cursor.execute("""
            INSERT INTO transactions (timestamp, customer_name, age, gender, county, town,
            store_name, category, product, units_sold, discount, revenue, payment_method)
            VALUES (%(Timestamp)s, %(CustomerName)s, %(Age)s, %(Gender)s, %(County)s,
            %(Town)s, %(StoreName)s, %(Category)s, %(Product)s, %(UnitsSold)s,
            %(Discount)s, %(Revenue)s, %(PaymentMethod)s);
        """, record)
        conn.commit()

    cursor.close()
    conn.close()


@app.route("/start_db_stream", methods=["POST"])
def start_db_stream():
    global is_streaming_to_db
    data = request.get_json()
    if data.get("pin") != ADMIN_PIN:
        return jsonify({"error": "Unauthorized"}), 403

    if not is_streaming_to_db:
        is_streaming_to_db = True
        threading.Thread(target=stream_to_db, daemon=True).start()
        return jsonify({"status": "DB streaming started"})
    else:
        return jsonify({"status": "Already streaming"})


@app.route("/stop_db_stream", methods=["POST"])
def stop_db_stream():
    global is_streaming_to_db
    data = request.get_json()
    if data.get("pin") != ADMIN_PIN:
        return jsonify({"error": "Unauthorized"}), 403

    is_streaming_to_db = False
    return jsonify({"status": "DB streaming stopped"})


@app.route("/stream")
def stream():
    """Live stream for dashboard (EventSource in HTML)."""
    def generate():
        for record in transaction_stream():
            yield f"data: {json.dumps(record)}\n\n"
    return Response(generate(), mimetype="text/event-stream")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
# county_name_mapping from name_generator.py