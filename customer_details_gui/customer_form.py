import uuid
from tkinter import *

from customer_details_gui.customer_storage import load_customers, save_customers


def save_customer_details(entries, form_window, customer_id, refresh_callback):
    data = {label: entry.get() for label, entry in entries.items()}
    customers = load_customers()
    customers[customer_id] = data
    save_customers(customers)
    form_window.destroy()
    refresh_callback()

def open_customer_form(parent_window, refresh_callback, existing_data=None, customer_id=None):
    form = Toplevel(parent_window)
    form.title("Add/Edit Customer")

    fields = ["Customer Name", "Address Line 1", "Address Line 2", "Contact", "GST No", "DL No"]
    entries = {}

    for idx, field in enumerate(fields):
        Label(form, text=field).grid(row=idx, column=0, padx=10, pady=5, sticky=W)
        entry = Entry(form, width=40)
        entry.insert(0, existing_data[field] if existing_data and field in existing_data else "")
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[field] = entry

    if not customer_id:
        customer_id = str(uuid.uuid4())

    Button(
        form,
        text="💾 Save",
        command=lambda: save_customer_details(entries, form, customer_id, refresh_callback)
    ).grid(row=len(fields), columnspan=2, pady=10)
