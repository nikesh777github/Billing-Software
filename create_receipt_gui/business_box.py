def draw_business_info(c, height, business):
    starting_pixel = 30
    c.rect(starting_pixel, height - 125, 190, 100)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(starting_pixel+10, height - 40, business.get("Business Name", ""))
    c.setFont("Helvetica", 9)
    c.drawString(starting_pixel+10, height - 52, business.get("Addr line 1", ""))
    c.drawString(starting_pixel+10, height - 64, business.get("Addr line 2", ""))
    c.drawString(starting_pixel+10, height - 76, f"Contact: {business.get('Contact', '')}")
    c.drawString(starting_pixel+10, height - 88, business.get("email", ""))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(starting_pixel+10, height - 113, f"GSTIN: {business.get('GSTIN', '')}")
