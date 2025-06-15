from tkinter import messagebox

from customer_details_gui.customer_storage import load_customers, save_customers


def delete_customer(customer_id, refresh_callback):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?")
    if confirm:
        customers = load_customers()
        if customer_id in customers:
            del customers[customer_id]
            save_customers(customers)
            refresh_callback()
