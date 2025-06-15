from reportlab.lib import colors

def draw_summary_row(c, product_entries, x_positions, col_widths, start_y, row_height=20):
    total_items = len(product_entries)
    gross_total = sum([row[-1] for row in product_entries])

    y = start_y - 10 - row_height  # leave 10px gap

    # Draw background rectangle (light grey)
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.rect(x_positions[0], y, sum(col_widths), row_height, fill=1, stroke=0)

    # Set text color back to black
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)

    # "Total Items"
    c.drawString(x_positions[0] + 5, y + 5, f"Total Items: {total_items}")

    # "GROSS TOTAL" aligned with Qty/Pack column
    qty_col_index = 7  # Index of "Qty/Pack"
    c.drawString(x_positions[qty_col_index], y + 5, "GROSS TOTAL:")

    # Total amount with "Rs."
    amount_col_index = 11  # Index of "Amount"
    total_text = f"Rs. {gross_total:.2f}"

    # Right-align the amount in last column
    text_width = c.stringWidth(total_text, "Helvetica-Bold", 9)
    right_edge = x_positions[amount_col_index] + col_widths[amount_col_index]
    c.drawString(right_edge - text_width - 5, y + 5, total_text)

    return y  # return new end_y
