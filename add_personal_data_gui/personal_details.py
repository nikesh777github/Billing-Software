from tkinter import *

from add_personal_data_gui.business_form import open_personal_details_form
from add_personal_data_gui.business_storage import load_businesses, delete_business


def open_add_data_window():
    window = Toplevel()
    window.title("Manage Businesses")
    window.geometry("600x400")

    def refresh_display():
        for widget in display_frame.winfo_children():
            widget.destroy()

        businesses = load_businesses()
        if not businesses:
            Label(display_frame, text="No business details found.", fg="gray").pack(anchor="w", padx=20, pady=5)
            return

        for bid, details in businesses.items():
            container = Frame(display_frame, bd=1, relief="groove", padx=10, pady=5)
            container.pack(fill=X, padx=10, pady=5)

            Label(container, text=details.get("Business Name", "Unnamed"), font=("Arial", 10, "bold")).pack(anchor="w")

            for key, value in details.items():
                if key != "Business Name":
                    Label(container, text=f"{key}: {value}", anchor="w").pack(anchor="w")

            btn_frame = Frame(container)
            btn_frame.pack(anchor="e", pady=5)

            Button(btn_frame, text="📝 Edit", command=lambda b=bid, d=details: open_personal_details_form(window, refresh_display, d, b)).pack(side=LEFT, padx=5)
            Button(btn_frame, text="🗑️ Delete", command=lambda b=bid: delete_business(b, refresh_display)).pack(side=LEFT)

    Button(window, text="➕ Add Business Details", command=lambda: open_personal_details_form(window, refresh_display)).pack(pady=10)

    canvas = Canvas(window)
    scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    display_frame = Frame(canvas)

    display_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=display_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    refresh_display()
