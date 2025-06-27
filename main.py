from tkinter import *

from add_personal_data_gui.personal_details import open_add_data_window
from create_receipt_gui.create_receipt import start_billing_app
from customer_details_gui.customer_window import open_customer_window
from product_details_gui.product_window import open_product_window

def main_menu():
    root = Tk()
    root.title("Main Menu")
    root.geometry("1200x600")

    Button(root, text="🧾 Create Receipt", width=30, command=lambda: start_billing_app(root)).pack(pady=10)
    Button(root, text="📦 Business Details", width=30, command=lambda: open_add_data_window(root)).pack(pady=10)
    Button(root, text="🏷️ Manage Products", width=30, command=lambda: open_product_window(root)).pack(pady=10)
    Button(root, text="👤 Manage Customers", width=30, command=lambda: open_customer_window(root)).pack(pady=10)
    Button(root, text="🚪 Exit", width=30, command=root.destroy).pack(pady=10)

    root.mainloop()

main_menu()
