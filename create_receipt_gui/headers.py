# headers.py

from reportlab.lib import colors

def draw_table_headers(c, x_positions, col_widths, y, row_height=20):
    headers = [
        "Sr.No", "HSN", "Product Name", "Pack Of", "Batch", "Exp",
        "MRP", "Qty", "GST", "Rate", "Value", "Amount"
    ]

    # Draw outer rectangle
    table_x_start = x_positions[0]
    total_width = sum(col_widths)
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(table_x_start, y - row_height, total_width, row_height)

    # Vertical lines
    for i in range(len(x_positions)):
        c.line(x_positions[i], y, x_positions[i], y - row_height)
    # c.line(x_positions[-1] + col_widths[-1], y, x_positions[-1] + col_widths[-1], y - row_height)

    # Header text
    c.setFont("Helvetica-Bold", 8)
    for i, header in enumerate(headers):
        text_width = c.stringWidth(header, "Helvetica-Bold", 8)
        col_center = x_positions[i] + col_widths[i] / 2
        c.drawString(col_center - text_width / 2, y - 15, header)


