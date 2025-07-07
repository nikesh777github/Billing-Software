import uuid
from tkinter import *

from product_details_gui.product_storage import load_products, save_products


def save_product_details(entries, form_window, product_id, refresh_callback):
    data = {label: entry.get() for label, entry in entries.items()}
    products = load_products()
    products[product_id] = data
    save_products(products)
    form_window.destroy()
    refresh_callback()

def open_product_form(parent_window, refresh_callback, existing_data=None, product_id=None):
    form = Toplevel(parent_window)
    form.title("Add/Edit Product")

    fields = ["Product Name", "HSN", "Pack Of", "Batch", "Expiry", "MRP", "Qty", "GST %", "Rate"]
    entries = {}

    field_key_map = {
        "Product Name": "product-name",
        "HSN": "hsn",
        "Pack Of": "pack",
        "Batch": "batch",
        "Expiry": "exp",
        "MRP": "mrp",
        "Qty": "qty",
        "GST %": "gst",
        "Rate": "rate"
    }
    for idx, field in enumerate(fields):
        Label(form, text=field).grid(row=idx, column=0, padx=10, pady=5, sticky=W)
        entry = Entry(form, width=40)

        json_key = field_key_map.get(field, field.lower().replace(" ", "-").replace("/", "-"))  # fallback
        entry.insert(0, existing_data[json_key] if existing_data and json_key in existing_data else "")
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[json_key] = entry

    # for idx, field in enumerate(fields):
    #     Label(form, text=field).grid(row=idx, column=0, padx=10, pady=5, sticky=W)
    #     entry = Entry(form, width=40)
    #     entry.insert(0, existing_data[field] if existing_data and field in existing_data else "")
    #     entry.grid(row=idx, column=1, padx=10, pady=5)
    #     entries[field] = entry

    if not product_id:
        product_id = str(uuid.uuid4())

    Button(
        form,
        text="💾 Save",
        command=lambda: save_product_details(entries, form, product_id, refresh_callback)
    ).grid(row=len(fields), columnspan=2, pady=10)
