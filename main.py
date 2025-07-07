from tkinter import *
from tkinter import font

from add_personal_data_gui.personal_details import open_add_data_window
from create_receipt_gui.create_receipt import create_receipt_window
from customer_details_gui.customer_window import open_customer_window
from product_details_gui.product_window import open_product_window

def main_menu():
    root = Tk()
    # root.geometry("1200x600")
    root.title("Billing Software")
    root.configure(bg="#f2f2f2")
    root.state('zoomed')
    tile_font = font.Font(family="Segoe UI", size=12, weight="bold")

    # Exit Button (top-right corner)
    exit_btn = Button(root, text="❌", command=root.destroy, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                      relief="flat", bd=0, padx=10, pady=5)
    exit_btn.place(relx=1.0, x=-10, y=10, anchor="ne")

    # Tile container
    tile_frame = Frame(root, bg="#f2f2f2")
    tile_frame.pack(pady=60)

    def make_tile(icon, text, command, col):
        tile = Frame(tile_frame, bg="white", bd=1, relief="raised", highlightthickness=1, highlightbackground="#ccc")
        tile.grid(row=0, column=col, padx=15, ipadx=15, ipady=10)

        Label(tile, text=icon, font=("Segoe UI Emoji", 18), bg="white").pack(pady=(10, 0))
        Label(tile, text=text, font=tile_font, bg="white").pack(pady=(5, 10))
        Button(tile, text="Open", command=command, bg="#3498db", fg="white", relief="flat",
               font=("Arial", 10), padx=8, pady=4).pack(pady=(0, 10))

    # Create tiles (5 across)
    make_tile("🧾", "Create Receipt", lambda: create_receipt_window(root), 0)
    make_tile("📦", "Business Details", lambda: open_add_data_window(root), 1)
    make_tile("🏷️", "Manage Products", lambda: open_product_window(root), 2)
    make_tile("👤", "Manage Customers", lambda: open_customer_window(root), 3)
    # make_tile("🚪", "Exit App", root.destroy, 4)

    root.mainloop()

main_menu()
