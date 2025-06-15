# gst_box.py
def draw_gst_box(c, height, invoice_no, today, due_date, status):
    starting_pixel = 220
    c.rect(starting_pixel, height - 125, 115, 100)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(starting_pixel+15, height - 40, "GST INVOICE")
    c.setFont("Helvetica", 9)
    c.drawString(starting_pixel+5, height - 60, f"Invoice No: {invoice_no}")
    c.drawString(starting_pixel+5, height - 72, f"Date          : {today}")
    c.drawString(starting_pixel+5, height - 84, f"Due Date  : {due_date}")
    c.drawString(starting_pixel+5, height - 96, f"Status       : {status}")
