import os
import json

DATA_FILE = "data/businesses.json"


def load_businesses():
    if not os.path.exists("data"):
        os.makedirs("data")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_businesses(businesses):
    with open(DATA_FILE, "w") as f:
        json.dump(businesses, f, indent=4)


def delete_business(business_id, refresh_callback):
    businesses = load_businesses()
    if business_id in businesses:
        del businesses[business_id]
        save_businesses(businesses)
        refresh_callback()
