# to_box.py
def draw_to_box(c, height, name, addr1, addr2, contact, gst, dl):
    c.rect(335, height - 125, 225, 100)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(340, height - 40, "To:")
    c.drawString(340, height - 52, name.upper())
    c.setFont("Helvetica", 9)
    c.drawString(340, height - 64, addr1)
    c.drawString(340, height - 76, addr2)
    c.drawString(340, height - 88, f"Contact No: {contact}")
    c.drawString(340, height - 100, f"GST No: {gst}")
    c.drawString(340, height - 112, f"DL No: {dl}")
