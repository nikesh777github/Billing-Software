import uuid
from tkinter import *

from add_personal_data_gui.business_storage import load_businesses, save_businesses


def save_personal_details(entries, form_window, business_id, refresh_callback):
    data = {label: entry.get() for label, entry in entries.items()}
    businesses = load_businesses()
    businesses[business_id] = data
    save_businesses(businesses)
    form_window.destroy()
    refresh_callback()


def open_personal_details_form(parent_window, refresh_callback, existing_data=None, business_id=None):
    form = Toplevel(parent_window)
    form.title("Add/Edit Business")

    # Include invoice-no
    fields = ["Business Name", "Addr line 1", "Addr line 2", "Contact", "email", "GSTIN", "invoice-no"]
    entries = {}

    for idx, field in enumerate(fields):
        Label(form, text=field).grid(row=idx, column=0, padx=10, pady=5, sticky=W)
        entry = Entry(form, width=40)

        # Initialize invoice-no to "1" if not present
        if field == "invoice-no":
            default_value = existing_data.get(field, "1") if existing_data else "1"
        else:
            default_value = existing_data.get(field, "") if existing_data else ""

        entry.insert(0, default_value)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[field] = entry

    if not business_id:
        business_id = str(uuid.uuid4())

    Button(
        form, text="💾 Save",
        command=lambda: save_personal_details(entries, form, business_id, refresh_callback)
    ).grid(row=len(fields), columnspan=2, pady=10)
