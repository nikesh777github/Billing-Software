import json
from tkinter import *
from tkinter import ttk, messagebox
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
from utils.load_json import load_json


def start_billing_app(parent_root=None):
    global billing_root, invoice_no_var, status_var, cust_name_var, cust_addr1_var
    global cust_addr2_var, cust_contact_var, cust_gst_var, cust_dl_var
    global product_name_var, pack_var, batch_var, exp_var
    global mrp_var, qty_var, rate_var, gross_total_var, net_amount_var
    global tree, product_entries
    global selected_business

    # Mock HSN DB
    # HSN_DB = {
    #     "Cotton Bandage (12x8M)": "3005040",
    #     "Cotton Bandage (4x3M)": "30059041",
    # }
    product_entries = []
    def add_product():
        name = product_name_var.get()
        hsn = hsn_var.get()
        pack = pack_var.get()
        batch = batch_var.get()
        exp = exp_var.get()
        mrp = float(mrp_var.get())
        qty = int(qty_var.get())
        gst = 0.05
        rate = float(rate_var.get())
        value = qty * rate
        amount = value + (value * gst)
        sr_no = len(product_entries) + 1
        product_entries.append(
            [sr_no, hsn, name, pack, batch, exp, mrp, qty, f"{int(gst * 100)}%", rate, value, amount])
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

    # GUI Setup
    # root = Tk()
    if parent_root:
        parent_root.withdraw()  # Hide main menu

    billing_root = Toplevel()
    billing_root.title("Billing Software")

    def go_back_to_main():
        billing_root.destroy()
        if parent_root:
            parent_root.deiconify()  # Show main menu again

    Button(billing_root, text="← Back to Menu", command=go_back_to_main, bg="lightgrey").pack(pady=5)

    billing_root.title("Billing Software")

    invoice_no_var = StringVar(value="000")
    status_var = StringVar(value="CREDIT")


    # Invoice Frame
    frame1 = Frame(billing_root)
    frame1.pack(pady=5)
    Label(frame1, text="Invoice No:").grid(row=0, column=0)
    Entry(frame1, textvariable=invoice_no_var).grid(row=0, column=1)
    Label(frame1, text="Status:").grid(row=0, column=2)
    ttk.Combobox(frame1, textvariable=status_var, values=["PAID", "CREDIT"]).grid(row=0, column=3)


    # Business Selection
    businesses = load_json("data/businesses.json")
    business_names = [b["Business Name"] for b in businesses.values()]
    business_lookup = {b["Business Name"]: b for b in businesses.values()}
    selected_business = StringVar(value=business_names[0])
    # Business Selection Frame
    Label(frame1, text="Select Business:").grid(row=0, column=4)
    ttk.Combobox(frame1, textvariable=selected_business, values=business_names).grid(row=0, column=5)


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

    frame2 = Frame(billing_root)
    frame2.pack(pady=5)
    Label(frame2, text="Select Customer:").grid(row=0, column=0)
    cust_dropdown = ttk.Combobox(frame2, textvariable=selected_customer, values=customer_names)
    cust_dropdown.grid(row=0, column=1)
    cust_dropdown.bind("<<ComboboxSelected>>", on_customer_select)
    # Label(frame2, text="Customer Name:").grid(row=0, column=0)
    # Entry(frame2, textvariable=cust_name_var).grid(row=0, column=1)
    Label(frame2, text="Address Line 1:").grid(row=0, column=2)
    Entry(frame2, textvariable=cust_addr1_var).grid(row=0, column=3)
    Label(frame2, text="Address Line 2:").grid(row=0, column=4)
    Entry(frame2, textvariable=cust_addr2_var).grid(row=0, column=5)
    Label(frame2, text="Contact:").grid(row=1, column=0)
    Entry(frame2, textvariable=cust_contact_var).grid(row=1, column=1)
    Label(frame2, text="GST No:").grid(row=1, column=2)
    Entry(frame2, textvariable=cust_gst_var).grid(row=1, column=3)
    Label(frame2, text="DL No:").grid(row=2, column=0)
    Entry(frame2, textvariable=cust_dl_var).grid(row=2, column=1)



    # Product Frame
    selected_product = StringVar()
    product_name_var = StringVar(value="Cotton Bandage (12x8M)")
    hsn_var = StringVar(value="12345")
    pack_var = StringVar(value="10")
    batch_var = StringVar(value="24025")
    exp_var = StringVar(value="May-28")
    mrp_var = StringVar(value="100")
    qty_var = StringVar(value="10")
    rate_var = StringVar(value="10")
    gross_total_var = StringVar()
    net_amount_var = StringVar()


    products = load_json("data/products.json")
    product_names = [c["Product Name"] for c in products.values()]
    product_lookup = {c["Product Name"]: c for c in products.values()}

    def on_product_select(event=None):
        prod = product_lookup.get(selected_product.get(), {})
        product_name_var.set(prod.get("Product Name", ""))
        hsn_var.set(prod.get("HSN", ""))
        exp_var.set(prod.get("Exp", ""))
        mrp_var.set(prod.get("MRP", ""))
        rate_var.set(prod.get("Rate", ""))

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
    Button(frame3, text="Add Product", command=add_product).grid(row=0, column=14)
    Button(frame3, text="Remove Selected", command=remove_selected).grid(row=0, column=15)

    # Product Column view
    cols = ["S.No", "HSN", "Product", "Pack", "Batch", "Exp", "MRP", "Qty", "GST", "Rate", "Value", "Amount"]
    tree = ttk.Treeview(billing_root, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=70)
    tree.pack(pady=5)

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

    # PDF Generation
    def generate_pdf():
        save_new_customer()
        now = datetime.datetime.now()
        timestamp = now.strftime("%d-%m-%y-%H-%M-%S")
        filename = f"invoice-{timestamp}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)

        width, height = A4
        today = now.strftime("%d-%m-%Y")
        due_date = (now + datetime.timedelta(days=30)).strftime("%d-%m-%Y")

        draw_business_info(c, height, business_lookup.get(selected_business.get(), {}))

        draw_gst_box(c, height, invoice_no_var.get(), today, due_date, status_var.get())
        draw_to_box(c, height, cust_name_var.get(), cust_addr1_var.get(), cust_addr2_var.get(),
                    cust_contact_var.get(), cust_gst_var.get(), cust_dl_var.get())

        # Table column widths and positions
        col_widths = [30, 40, 120, 30, 35, 40, 40, 40, 25, 40, 40, 50]  # Increased Product Name width (index 2)
        x_positions = [30]
        for w in col_widths[:-1]:
            x_positions.append(x_positions[-1] + w)

        start_y = height - 125

        draw_table_headers(c, x_positions, col_widths, start_y)
        end_y = draw_product_rows(c, product_entries, x_positions, col_widths, start_y)
        end_y = draw_summary_row(c, product_entries, x_positions, col_widths, end_y)
        end_y = draw_footer_box(c, x_positions, col_widths, end_y, net_amount_var.get())
        # Totals
        # c.setFont("Helvetica-Bold", 9)
        # c.drawString(400, end_y - 10, f"GROSS TOTAL: ₹ {gross_total_var.get()}")
        # c.drawString(400, end_y - 30, f"NET AMOUNT: ₹ {net_amount_var.get()}")

        c.save()
        messagebox.showinfo("Success", f"Invoice PDF generated as '{filename}'.")

    Button(billing_root, text="Generate PDF", command=generate_pdf).pack(pady=10)

    billing_root.mainloop()
