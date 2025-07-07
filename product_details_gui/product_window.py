from tkinter import *

from product_details_gui.product_delete import delete_product
from product_details_gui.product_form import open_product_form
from product_details_gui.product_storage import load_products


def open_product_window(parent_root=None):
    window = Toplevel()
    window.title("Manage Products")
    window.geometry("1200x600")

    def refresh_display():
        for widget in display_frame.winfo_children():
            widget.destroy()

        products = load_products()
        if not products:
            Label(display_frame, text="No product details found.", fg="gray").pack(anchor="w", padx=20, pady=5)
            return

        for pid, details in products.items():
            container = Frame(display_frame, bd=1, relief="groove", padx=10, pady=5)
            container.pack(fill=X, padx=10, pady=5)

            Label(container, text=details.get("Product Name", "Unnamed"), font=("Arial", 10, "bold")).pack(anchor="w")

            for key, value in details.items():
                if key != "Product Name":
                    Label(container, text=f"{key}: {value}", anchor="w").pack(anchor="w")

            btn_frame = Frame(container)
            btn_frame.pack(anchor="e", pady=5)

            Button(btn_frame, text="📝 Edit", command=lambda p=pid, d=details: open_product_form(window, refresh_display, d, p)).pack(side=LEFT, padx=5)
            Button(btn_frame, text="🗑️ Delete", command=lambda p=pid: delete_product(p, refresh_display)).pack(side=LEFT)

        # GUI Setup
        # root = Tk()
    if parent_root:
        parent_root.withdraw()  # Hide main menu

    def go_back_to_main():
        window.destroy()
        if parent_root:
            parent_root.deiconify()
    # Buttons at the top
    Button(window, text="➕ Add Product", command=lambda: open_product_form(window, refresh_display)).pack(pady=10)
    Button(window, text="🔙 Back", command=go_back_to_main, bg="lightgrey").pack(pady=5)
    # Scrollable frame
    canvas = Canvas(window)
    scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    display_frame = Frame(canvas)

    display_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=display_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    refresh_display()
