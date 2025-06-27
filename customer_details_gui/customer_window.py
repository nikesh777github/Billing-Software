from tkinter import *

from customer_details_gui.customer_delete import delete_customer
from customer_details_gui.customer_form import open_customer_form
from customer_details_gui.customer_storage import load_customers


def open_customer_window(parent_root=None):
    window = Toplevel()
    window.title("Manage Customers")
    window.geometry("700x500")

    def refresh_display():
        for widget in display_frame.winfo_children():
            widget.destroy()

        customers = load_customers()
        if not customers:
            Label(display_frame, text="No customer details found.", fg="gray").pack(anchor="w", padx=20, pady=5)
            return

        for cid, details in customers.items():
            container = Frame(display_frame, bd=1, relief="groove", padx=10, pady=5)
            container.pack(fill=X, padx=10, pady=5)

            Label(container, text=details.get("Customer Name", "Unnamed"), font=("Arial", 10, "bold")).pack(anchor="w")

            for key, value in details.items():
                if key != "Customer Name":
                    Label(container, text=f"{key}: {value}", anchor="w").pack(anchor="w")

            btn_frame = Frame(container)
            btn_frame.pack(anchor="e", pady=5)

            Button(btn_frame, text="📝 Edit", command=lambda c=cid, d=details: open_customer_form(window, refresh_display, d, c)).pack(side=LEFT, padx=5)
            Button(btn_frame, text="🗑️ Delete", command=lambda c=cid: delete_customer(c, refresh_display)).pack(side=LEFT)

    # GUI Setup
    # root = Tk()
    if parent_root:
        parent_root.withdraw()  # Hide main menu

    def go_back_to_main():
        window.destroy()
        if parent_root:
            parent_root.deiconify()  # Show main menu again

    Button(window, text="🔙 Back", command=go_back_to_main, bg="lightgrey").pack(pady=5)
    Button(window, text="➕ Add Customer", command=lambda: open_customer_form(window, refresh_display)).pack(pady=10)

    canvas = Canvas(window)
    scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    display_frame = Frame(canvas)

    display_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=display_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    refresh_display()
