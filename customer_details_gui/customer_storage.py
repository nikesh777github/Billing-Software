import json
import os
from datetime import datetime

DATA_DIR = "data"
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_customers():
    if not os.path.exists(CUSTOMER_FILE):
        return {}
    with open(CUSTOMER_FILE, "r") as f:
        return json.load(f)

def save_customers(data):
    with open(CUSTOMER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_customer_history_and_pending(name, invoice_no, status, amount):
    data = load_customers()
    if name not in data:
        return

    customer = data[name]

    # Initialize fields if they don't exist
    if "history" not in customer:
        customer["history"] = []
    if "pending" not in customer:
        customer["pending"] = 0

    # Add entry to history
    customer["history"].append({
        "date": datetime.now().strftime("%d-%m-%Y"),
        "invoice": invoice_no,
        "status": status,
        "amount": float(amount)
    })

    # If CREDIT, increase pending
    if status.upper() == "CREDIT":
        customer["pending"] += float(amount)

    save_customers(data)
