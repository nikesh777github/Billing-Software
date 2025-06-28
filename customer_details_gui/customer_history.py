# user_history_gui.py

from tkinter import *
from tkinter import messagebox

def open_customer_history(customer_name):
    win = Toplevel()
    win.title(f"{customer_name} - History")
    win.geometry("700x500")

    Label(win, text=f"📊 History for {customer_name}", font=("Segoe UI", 14, "bold")).pack(pady=10)

    # Later: You can add chart, table of invoices, total paid/pending etc
    Label(win, text="(Here you can show graphs, invoice logs, payments, pending etc)").pack(pady=20)

    Button(win, text="Close", command=win.destroy).pack(pady=20)
