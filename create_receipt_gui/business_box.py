# business_box.py
def draw_business_info(c, height):
    starting_pixel = 30
    c.rect(starting_pixel, height - 125, 190, 100)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(starting_pixel+10, height - 40, "NARMADA ENTERPRISES")
    c.setFont("Helvetica", 9)
    c.drawString(starting_pixel+10, height - 52, "Plot No. 2785, Kinwat Road")
    c.drawString(starting_pixel+10, height - 64, "Bhokar, Nanded, Maharashtra")
    c.drawString(starting_pixel+10, height - 76, "Contact: 9172258572")
    c.drawString(starting_pixel+10, height - 88, "narmadaenterprises257@gmail.com")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(starting_pixel+10, height - 113, "GSTIN: 27EFEPP7089K1ZM")
