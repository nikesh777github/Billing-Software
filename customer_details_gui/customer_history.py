from tkinter import *
from tkinter import ttk
import datetime
import json

from customer_details_gui.customer_storage import load_customers

def open_customer_history(customer_name):
    win = Toplevel()
    win.title(f"{customer_name} - History")
    win.geometry("800x500")
    win.configure(bg="#f9f9f9")

    # Load customer data
    customers = load_customers()
    customer = customers.get(customer_name, {})
    history = customer.get("history", [])
    pending = float(customer.get("pending", 0.0))

    # Heading
    Label(win, text=f"📊 History for {customer_name}", font=("Segoe UI", 16, "bold"), bg="#f9f9f9").pack(pady=(15, 5))

    # Pending Amount
    pending_color = "#e74c3c" if pending > 0 else "#2ecc71"
    Label(
        win, text=f"Pending Amount: ₹ {pending:.2f}",
        font=("Segoe UI", 14, "bold"), fg=pending_color, bg="#f9f9f9"
    ).pack(pady=(0, 10))

    # Frame for table
    table_frame = Frame(win, bg="#f9f9f9")
    table_frame.pack(pady=10, fill=BOTH, expand=True, padx=20)

    cols = ("Date", "Invoice", "Status", "Amount")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    for entry in history:
        tree.insert("", "end", values=(
            entry.get("date", ""),
            entry.get("invoice", ""),
            entry.get("status", ""),
            f"₹ {entry.get('amount', 0):.2f}"
        ))

    tree.pack(fill=BOTH, expand=True)

    # Close button
    Button(win, text="Close", command=win.destroy, bg="#3498db", fg="white",
           font=("Segoe UI", 10, "bold"), padx=20, pady=5).pack(pady=15)
