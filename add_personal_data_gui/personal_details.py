from tkinter import *
from tkinter import font
from add_personal_data_gui.business_form import open_personal_details_form
from add_personal_data_gui.business_storage import load_businesses, delete_business


def open_add_data_window(parent_root=None):
    window = Toplevel()
    window.title("Manage Businesses")
    window.geometry("1200x600")
    window.configure(bg="#f0f2f5")

    title_font = font.Font(family="Segoe UI", size=16, weight="bold")
    label_font = font.Font(family="Segoe UI", size=10)

    if parent_root:
        parent_root.withdraw()

    def go_back_to_main():
        window.destroy()
        if parent_root:
            parent_root.deiconify()

    # Back button
    top_bar = Frame(window, bg="#f0f2f5")
    top_bar.pack(fill=X, pady=10, padx=10)

    Button(top_bar, text="← Back", command=go_back_to_main, bg="#dcdcdc", font=("Segoe UI", 10), relief="flat", padx=10).pack(side=LEFT)

    Button(top_bar, text="➕ Add Business", command=lambda: open_personal_details_form(window, refresh_display),
           bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=4).pack(side=RIGHT)

    # Main Canvas Area
    canvas = Canvas(window, bg="#f0f2f5", bd=0, highlightthickness=0)
    scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    display_frame = Frame(canvas, bg="#f0f2f5")

    display_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=display_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side=RIGHT, fill=Y)

    def refresh_display():
        for widget in display_frame.winfo_children():
            widget.destroy()

        businesses = load_businesses()

        if not businesses:
            Label(display_frame, text="No business details found.", fg="gray", bg="#f0f2f5", font=label_font).pack(
                anchor="center", pady=20)
            return

        for bid, details in businesses.items():
            card = Frame(display_frame, bg="white", bd=1, relief="solid", padx=15, pady=10)
            card.pack(fill=X, padx=10, pady=(10, 5))

            # Title
            Label(card, text=details.get("Business Name", "Unnamed"), bg="white", font=title_font).grid(row=0, column=0,
                                                                                                        columnspan=6,
                                                                                                        sticky="w",
                                                                                                        pady=(0, 10))

            # Horizontal key-value layout
            row = 1
            col = 0
            for key, value in details.items():
                if key != "Business Name":
                    Label(card, text=f"{key}:", bg="white", font=label_font, anchor="e").grid(row=row, column=col * 2,
                                                                                              sticky="e", padx=(5, 2),
                                                                                              pady=2)
                    Label(card, text=value, bg="white", font=label_font, anchor="w").grid(row=row, column=col * 2 + 1,
                                                                                          sticky="w", padx=(0, 15),
                                                                                          pady=2)
                    col += 1
                    if col == 3:
                        col = 0
                        row += 1

            # Add a spacer row to push buttons down
            spacer = Label(card, text="", bg="white")
            spacer.grid(row=row + 1, column=0, columnspan=6)

            # Buttons at bottom right
            btn_frame = Frame(card, bg="white")
            btn_frame.grid(row=row + 2, column=5, columnspan=1, sticky="e", pady=(10, 0))

            Button(btn_frame, text="📝 Edit",
                   command=lambda b=bid, d=details: open_personal_details_form(window, refresh_display, d, b),
                   bg="#2ecc71", fg="white", relief="flat", font=("Segoe UI", 9), padx=10).pack(side=LEFT, padx=5)
            Button(btn_frame, text="🗑️ Delete", command=lambda b=bid: delete_business(b, refresh_display),
                   bg="#e74c3c", fg="white", relief="flat", font=("Segoe UI", 9), padx=10).pack(side=LEFT, padx=5)

            # Horizontal separator line
            Frame(display_frame, bg="#dcdcdc", height=1).pack(fill=X, padx=10, pady=(0, 10))

    refresh_display()
