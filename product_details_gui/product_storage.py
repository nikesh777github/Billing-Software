import json
import os

DATA_DIR = "data"
PRODUCT_FILE = os.path.join(DATA_DIR, "products.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_products():
    if not os.path.exists(PRODUCT_FILE):
        return {}
    with open(PRODUCT_FILE, "r") as f:
        return json.load(f)

def save_products(data):
    with open(PRODUCT_FILE, "w") as f:
        json.dump(data, f, indent=4)
