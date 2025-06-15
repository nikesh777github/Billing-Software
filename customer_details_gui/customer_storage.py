import json
import os

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
