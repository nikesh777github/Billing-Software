from reportlab.lib import colors

def draw_footer_box(c, x_positions, col_widths, y, net_amount):
    box_height = 90
    box_y = y - 10 - box_height
    box_x = x_positions[0]
    box_width = sum(col_widths)

    # Main white background
    c.setFillColor(colors.white)
    c.rect(box_x, box_y, box_width, box_height, fill=1, stroke=1)

    # Left side legal notes
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    left_text = [
        "Goods once sold will not be taken back or ",
        "exchanged.",
        "Bills not paid due date will attract 24% ",
        "interest.",
        "All disputes subject to NANDED Jurisdiction ",
        "only.",
        "Prescribed Sales Tax declarations will be given."
    ]
    left_x = box_x + 10
    left_y = box_y + box_height - 12
    for line in left_text:
        c.drawString(left_x, left_y, line)
        left_y -= 12

    # Bank Details on right
    right_x = x_positions[7] + 5
    c.setFont("Helvetica-Bold", 9)
    c.drawString(right_x, box_y + box_height - 12, "Bank Details:")
    c.setFont("Helvetica", 9)
    c.drawString(right_x, box_y + box_height - 24, "NARMADA ENTERPRISES [SBI]")
    c.drawString(right_x, box_y + box_height - 36, "A/C: 43995663319")
    c.drawString(right_x, box_y + box_height - 48, "IFSC Code: SBIN0020052 [Bhokar]")

    # NET AMOUNT background
    grey_x = right_x - 5
    grey_y = box_y + box_height - 65
    grey_width = (x_positions[-1] + col_widths[-1]) - grey_x - 5
    grey_height = 15

    c.setFillColor(colors.lightgrey)
    c.rect(grey_x, grey_y, grey_width, grey_height, fill=1, stroke=0)

    # NET AMOUNT label
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(right_x, grey_y + 3, "NET AMOUNT:")

    # NET AMOUNT value
    amount_text = f"Rs. {net_amount}"
    c.setFont("Helvetica-Bold", 9)
    text_width = c.stringWidth(amount_text, "Helvetica-Bold", 9)
    c.drawString(x_positions[-1] + col_widths[-1] - text_width - 10, grey_y + 3, amount_text)

    # Authorised Signatory (moved slightly higher)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(box_x + box_width / 2, box_y + 10, "Authorised Signatory")

    return box_y
