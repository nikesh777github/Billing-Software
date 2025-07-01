import json
from tkinter import *
from tkinter import ttk, messagebox

from PIL.ImageChops import constant
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

from create_receipt_gui.business_box import draw_business_info
from create_receipt_gui.footer_box import draw_footer_box
from create_receipt_gui.gst_box import draw_gst_box
from create_receipt_gui.headers import draw_table_headers
from create_receipt_gui.product_rows import draw_product_rows
from create_receipt_gui.summary_row import draw_summary_row
from create_receipt_gui.to_box import draw_to_box
from customer_details_gui.customer_storage import update_customer_history_and_pending
from utils.inline_edit import enable_inline_editing
from utils.load_json import load_json


def start_billing_app(parent_root=None):
    global billing_root, status_var, cust_name_var, cust_addr1_var
    global cust_addr2_var, cust_contact_var, cust_gst_var, cust_dl_var
    global product_name_var, pack_var, batch_var, exp_var
    global mrp_var, qty_var, gst_prod_var, rate_var, gross_total_var, net_amount_var
    global tree, product_entries
    global selected_business


    product_entries = []

    def add_product():
        name = selected_product.get().strip() or product_name_var.get().strip()

        if not name:
            return

        hsn = hsn_var.get().strip()
        pack = pack_var.get().strip()
        batch = batch_var.get().strip()
        exp = exp_var.get().strip()
        mrp = float(mrp_var.get())
        qty = int(qty_var.get())
        gst_add_product = float(gst_prod_var.get())
        rate = float(rate_var.get())
        value = qty * rate
        amount = value + (value * (gst_add_product/100))

        found = False
        for entry in product_entries:
            if (entry[2] == name and entry[1] == hsn and entry[4] == batch and
                    entry[5] == exp and entry[6] == mrp and entry[7] == qty and entry[9] == rate):

                # Only Pack is different → update existing row
                if entry[3] != pack:
                    entry[3] = pack
                    found = True
                    break
                else:
                    # Exact match already exists → update quantity if needed (optional)
                    messagebox.showinfo("Duplicate", f"Product '{name}' already exists.")
                    return

        if not found:
            sr_no = len(product_entries) + 1
            product_entries.append([
                sr_no, hsn, name, pack, batch, exp, mrp, qty,
                f"{gst_add_product}%", rate, value, amount
            ])

        # Reassign serial numbers
        for i, entry in enumerate(product_entries):
            entry[0] = i + 1

        update_tree()

    def remove_selected():
        selected = tree.selection()
        for item in selected:
            index = int(tree.item(item, 'values')[0]) - 1
            del product_entries[index]
        for i, entry in enumerate(product_entries):
            entry[0] = i + 1
        update_tree()

    def update_tree():
        tree.delete(*tree.get_children())
        for entry in product_entries:
            tree.insert('', 'end', values=entry)
        update_totals()

    def update_totals():
        gross_total = sum([item[-1] for item in product_entries])
        gross_total_var.set(f"{gross_total:.2f}")
        net_amount_var.set(f"{gross_total:.2f}")

    if parent_root:
        parent_root.withdraw()  # Hide main menu

    billing_root = Toplevel()
    billing_root.title("Billing Software")
    billing_root.geometry("1200x600")

    def go_back_to_main():
        billing_root.destroy()
        if parent_root:
            parent_root.deiconify()  # Show main menu again

    Button(billing_root, text="← Back to Menu", command=go_back_to_main, bg="lightgrey").pack(pady=5)

    billing_root.title("Billing Software")


    frame1 = Frame(billing_root)
    frame1.pack(pady=5)

    # Business Selection
    bus_name = StringVar()
    adr_l1 = StringVar()
    adr_l2 = StringVar()
    contact = StringVar()
    email = StringVar()
    gst = StringVar()
    invoice_no = StringVar(value="000")
    prev_invoice_no = StringVar()
    def on_business_select(event=None):
        bus = business_lookup.get(selected_business.get(), {})
        bus_name.set(bus.get("Business Name", ""))
        adr_l1.set(bus.get("Addr line 1", ""))
        adr_l2.set(bus.get("Addr line 2", ""))
        contact.set(bus.get("Contact", ""))
        email.set(bus.get("email", ""))
        gst.set(bus.get("GSTIN", ""))
        invoice_no.set(str(bus.get("invoice-no", 0)))
        prev_invoice_no.set(str(bus.get("invoice-no", 0)))


    businesses = load_json("data/businesses.json")
    # After loading businesses
    for bid, details in businesses.items():
        if "invoice-no" not in details:
            details["invoice-no"] = 0

    # Save it back to file if modified
    with open("data/businesses.json", "w") as f:
        json.dump(businesses, f, indent=4)

    business_names = [b["Business Name"] for b in businesses.values()]
    business_lookup = {b["Business Name"]: b for b in businesses.values()}
    selected_business = StringVar(value=business_names[0])
    on_business_select()
    # Business Selection Frame
    Label(frame1, text="Select Business:").grid(row=0, column=0)
    bus_dropdown = ttk.Combobox(frame1, textvariable=selected_business, values=business_names)
    bus_dropdown.grid(row=0, column=1)
    bus_dropdown.bind("<<ComboboxSelected>>", on_business_select)

    # Displaying Business Values on Create Receipt (read-only)
    ttk.Label(frame1, text="Business Name:").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame1, textvariable=bus_name, state="readonly", width=30).grid(row=1, column=1, padx=5, pady=2)

    ttk.Label(frame1, text="Address Line 1:").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame1, textvariable=adr_l1, state="readonly", width=30).grid(row=2, column=1, padx=5, pady=2)

    ttk.Label(frame1, text="Address Line 2:").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame1, textvariable=adr_l2, state="readonly", width=30).grid(row=3, column=1, padx=5, pady=2)

    ttk.Label(frame1, text="Contact:").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame1, textvariable=contact, state="readonly", width=30).grid(row=4, column=1, padx=5, pady=2)

    ttk.Label(frame1, text="Email:").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame1, textvariable=email, state="readonly", width=30).grid(row=5, column=1, padx=5, pady=2)

    ttk.Label(frame1, text="GSTIN:").grid(row=6, column=0, sticky="w")
    ttk.Entry(frame1, textvariable=gst, state="readonly", width=30).grid(row=6, column=1, padx=5, pady=2)


    # Invoice Frame
    ttk.Label(frame1, text="Invoice No:").grid(row=0, column=2, sticky="w")
    Entry(frame1, textvariable=invoice_no).grid(row=0, column=3, padx=5, pady=2)

    ttk.Label(frame1, text="Original Invoice No:").grid(row=1, column=2, sticky="w")
    ttk.Entry(frame1, textvariable=prev_invoice_no, state="readonly", width=10).grid(row=1, column=3, padx=5, pady=2)

    status_var = StringVar(value="CREDIT")
    Label(frame1, text="Status:").grid(row=2, column=2)
    ttk.Combobox(frame1, textvariable=status_var, values=["PAID", "CREDIT"]).grid(row=2, column=3)


    # Customer Frame
    selected_customer = StringVar()
    cust_name_var = StringVar()
    cust_addr1_var = StringVar()
    cust_addr2_var = StringVar()
    cust_contact_var = StringVar()
    cust_gst_var = StringVar()
    cust_dl_var = StringVar()

    customers = load_json("data/customers.json")
    customer_names = [c["Customer Name"] for c in customers.values()]
    customer_lookup = {c["Customer Name"]: c for c in customers.values()}

    def on_customer_select(event=None):
        cust = customer_lookup.get(selected_customer.get(), {})
        cust_name_var.set(cust.get("Customer Name", ""))
        cust_addr1_var.set(cust.get("Address Line 1", ""))
        cust_addr2_var.set(cust.get("Address Line 2", ""))
        cust_contact_var.set(cust.get("Contact", ""))
        cust_gst_var.set(cust.get("GST No", ""))
        cust_dl_var.set(cust.get("DL No", ""))

    Label(frame1, text="Select Customer:").grid(row=0, column=5)
    cust_dropdown = ttk.Combobox(frame1, textvariable=selected_customer, values=customer_names)
    cust_dropdown.grid(row=0, column=6)
    cust_dropdown.bind("<<ComboboxSelected>>", on_customer_select)

    ttk.Label(frame1, text="Address Line 1:").grid(row=1, column=5, sticky="w")
    ttk.Entry(frame1, textvariable=cust_addr1_var, width=30).grid(row=1, column=6, padx=5, pady=2)

    ttk.Label(frame1, text="Address Line 2:").grid(row=2, column=5, sticky="w")
    ttk.Entry(frame1, textvariable=cust_addr2_var, width=30).grid(row=2, column=6, padx=5, pady=2)

    ttk.Label(frame1, text="Contact:").grid(row=3, column=5, sticky="w")
    ttk.Entry(frame1, textvariable=cust_contact_var, width=30).grid(row=3, column=6, padx=5, pady=2)

    ttk.Label(frame1, text="GST No:").grid(row=4, column=5, sticky="w")
    ttk.Entry(frame1, textvariable=cust_gst_var, width=30).grid(row=4, column=6, padx=5, pady=2)

    ttk.Label(frame1, text="DL No:").grid(row=5, column=5, sticky="w")
    ttk.Entry(frame1, textvariable=cust_dl_var, width=30).grid(row=5, column=6, padx=5, pady=2)


    # Product Frame
    selected_product = StringVar()
    product_name_var = StringVar()
    hsn_var = StringVar()
    pack_var = StringVar()
    batch_var = StringVar()
    exp_var = StringVar()
    mrp_var = StringVar()
    qty_var = StringVar()
    gst_prod_var = StringVar()
    rate_var = StringVar()
    gross_total_var = StringVar()
    net_amount_var = StringVar()


    products = load_json("data/products.json")
    product_names = [c["product-name"] for c in products.values()]
    product_lookup = {c["product-name"]: c for c in products.values()}

    def on_product_select(event=None):
        prod_name = selected_product.get()
        prod = product_lookup.get(prod_name, {})
        product_name_var.set(prod.get("product-name", prod_name))  # fallback
        hsn_var.set(prod.get("hsn", ""))
        pack_var.set(prod.get("pack", ""))
        batch_var.set(prod.get("batch", ""))
        exp_var.set(prod.get("exp", ""))
        mrp_var.set(prod.get("mrp", ""))
        qty_var.set(prod.get("qty-per-pack", "1"))  # reset to 1 or prod.get("Qty/Pack", "") if you store it
        gst_prod_var.set(prod.get("gst"))
        rate_var.set(prod.get("rate", ""))

    frame3 = Frame(billing_root)
    frame3.pack(pady=5)
    Label(frame3, text="Select Product:").grid(row=0, column=0)
    product_dropdown = ttk.Combobox(frame3, textvariable=selected_product, values=product_names)
    product_dropdown.grid(row=0, column=1)
    product_dropdown.bind("<<ComboboxSelected>>", on_product_select)

    Label(frame3, text="Pack:").grid(row=0, column=2)
    Entry(frame3, textvariable=pack_var, width=5).grid(row=0, column=3)
    Label(frame3, text="Batch:").grid(row=0, column=4)
    Entry(frame3, textvariable=batch_var, width=10).grid(row=0, column=5)
    Label(frame3, text="Exp:").grid(row=0, column=6)
    Entry(frame3, textvariable=exp_var, width=10).grid(row=0, column=7)
    Label(frame3, text="MRP:").grid(row=0, column=8)
    Entry(frame3, textvariable=mrp_var, width=5).grid(row=0, column=9)
    Label(frame3, text="Qty:").grid(row=0, column=10)
    Entry(frame3, textvariable=qty_var, width=5).grid(row=0, column=11)
    Label(frame3, text="Rate:").grid(row=0, column=12)
    Entry(frame3, textvariable=rate_var, width=5).grid(row=0, column=13)
    Label(frame3, text="GST:").grid(row=0, column=13)
    Entry(frame3, textvariable=gst_prod_var, width=5).grid(row=0, column=14)
    Button(frame3, text="Add Product", command=add_product).grid(row=0, column=15)
    Button(frame3, text="Remove Selected", command=remove_selected).grid(row=0, column=16)
    Button(frame3, text="🔄", command=on_product_select).grid(row=0, column=17)
    # Product Column view
    cols = ["S.No", "HSN", "Product", "Pack", "Batch", "Exp", "MRP", "Qty", "GST", "Rate", "Value", "Amount"]
    tree = ttk.Treeview(billing_root, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=70)
    tree.pack(pady=5)
    # Enable double-click editing
    enable_inline_editing(tree, product_entries, update_tree)
    # Totals
    frame4 = Frame(billing_root)
    frame4.pack()
    Label(frame4, text="GROSS TOTAL:").grid(row=0, column=0)
    Entry(frame4, textvariable=gross_total_var, state="readonly").grid(row=0, column=1)
    Label(frame4, text="NET AMOUNT:").grid(row=0, column=2)
    Entry(frame4, textvariable=net_amount_var, state="readonly").grid(row=0, column=3)

    def save_new_customer():
        cust_name = selected_customer.get()
        if cust_name and cust_name not in customer_lookup:
            new_cust = {
                "Customer Name": cust_name,
                "Address Line 1": cust_addr1_var.get(),
                "Address Line 2": cust_addr2_var.get(),
                "Contact": cust_contact_var.get(),
                "GST No": cust_gst_var.get(),
                "DL No": cust_dl_var.get()
            }

            customers[cust_name] = new_cust
            customer_lookup[cust_name] = new_cust

            with open("data/customers.json", "w") as f:
                json.dump(customers, f, indent=4)

    def save_new_products():
        updated = False
        for entry in product_entries:
            prod_name = entry[2]
            if prod_name not in product_lookup:
                new_product = {
                    "product-name": prod_name,
                    "hsn": entry[1],
                    "pack": entry[3],
                    "batch": entry[4],
                    "exp": entry[5],
                    "mrp": entry[6],
                    "qty-per-pack": entry[7],
                    "gst": entry[8],
                    "rate": entry[9]
                }
                products[prod_name] = new_product
                product_lookup[prod_name] = new_product
                updated = True

        if updated:
            with open("data/products.json", "w") as f:
                json.dump(products, f, indent=4)

    def update_invoice_no():
        # Get current invoice no and update it
        current_bus = business_lookup.get(selected_business.get(), {})
        try:
            current_invoice = int(invoice_no.get())
        except ValueError:
            current_invoice = current_bus.get("invoice-no", 0)

        current_bus["invoice-no"] = current_invoice + 1

        # Save back to JSON
        with open("data/businesses.json", "w") as f:
            json.dump(businesses, f, indent=4)
            # ✅ Update it in GUI
        invoice_no.set(str(current_invoice + 1))

    # PDF Generation
    def generate_pdf():
        save_new_customer()
        save_new_products()
        if not cust_name_var.get():
            cust_name_var.set(selected_customer.get())
        now = datetime.datetime.now()
        timestamp = now.strftime("%d-%m-%y-%H-%M-%S")
        filename = f"{cust_name_var.get()}-{timestamp}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)

        width, height = A4
        today = now.strftime("%d-%m-%Y")
        due_date = (now + datetime.timedelta(days=30)).strftime("%d-%m-%Y")

        repeat = 2 if duplicate_bill_var.get() else 1
        section_height = height // repeat

        col_widths = [30, 40, 120, 30, 35, 40, 40, 40, 25, 40, 40, 50]
        x_positions = [30]
        for w in col_widths[:-1]:
            x_positions.append(x_positions[-1] + w)

        for i in range(repeat):
            section_top = height - (i * section_height)
            start_y = section_top - 125

            draw_business_info(c, section_top, business_lookup.get(selected_business.get(), {}))
            draw_gst_box(c, section_top, invoice_no.get(), today, due_date, status_var.get())
            draw_to_box(c, section_top, cust_name_var.get(), cust_addr1_var.get(), cust_addr2_var.get(),
                        cust_contact_var.get(), cust_gst_var.get(), cust_dl_var.get())

            draw_table_headers(c, x_positions, col_widths, start_y)
            end_y = draw_product_rows(c, product_entries, x_positions, col_widths, start_y)
            end_y = draw_summary_row(c, product_entries, x_positions, col_widths, end_y)
            draw_footer_box(c, x_positions, col_widths, end_y, net_amount_var.get())

        c.save()
        messagebox.showinfo("Success", f"Invoice PDF generated as '{filename}'.")
        update_invoice_no()
        # After save_new_customer()
        update_customer_history_and_pending(
            cust_name_var.get(),  # Customer Name
            invoice_no.get(),  # Invoice Number
            status_var.get(),  # Status (CREDIT / PAID)
            float(net_amount_var.get())  # Final Net Amount
        )
    duplicate_bill_var = IntVar()
    Checkbutton(billing_root, text="Duplicate Bill", variable=duplicate_bill_var).pack()

    Button(billing_root, text="Generate PDF", command=generate_pdf).pack(pady=10)

    billing_root.mainloop()
