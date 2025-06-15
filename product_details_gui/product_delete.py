from tkinter import messagebox

from product_details_gui.product_storage import load_products, save_products


def delete_product(product_id, refresh_callback):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
    if confirm:
        products = load_products()
        if product_id in products:
            del products[product_id]
            save_products(products)
            refresh_callback()
