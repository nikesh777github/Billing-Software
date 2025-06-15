from reportlab.lib import colors

def draw_product_rows(c, entries, x_positions, col_widths, start_y, row_height=20):
    c.setFont("Helvetica", 8)
    y = start_y - row_height

    for row_index, row in enumerate(entries):
        # Use very light grey: custom RGB color
        light_grey = colors.Color(0.88, 0.88, 0.88)  # lighter than lightgrey
        row_color = light_grey if row_index % 2 == 0 else colors.whitesmoke

        c.setFillColor(row_color)
        c.rect(x_positions[0], y - row_height, sum(col_widths), row_height, fill=1, stroke=0)

        # Borders
        c.setFillColor(colors.black)
        c.setStrokeColor(colors.black)
        c.rect(x_positions[0], y - row_height, sum(col_widths), row_height, stroke=1, fill=0)

        # Vertical lines
        for i in range(len(x_positions)):
            c.line(x_positions[i], y, x_positions[i], y - row_height)
        c.line(x_positions[-1] + col_widths[-1], y, x_positions[-1] + col_widths[-1], y - row_height)

        # Text
        for i, item in enumerate(row):
            c.drawString(x_positions[i] + 2, y - 15, str(item))

        y -= row_height

    return y
