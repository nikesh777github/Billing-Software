from tkinter import Entry

def enable_inline_editing(tree, product_entries, update_tree):
    def on_tree_double_click(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        col_index = int(column[1:]) - 1  # "#3" → 2

        # Skip Sr.No (0) and Product Name (2)
        if col_index in [0, 2]:
            return

        item = tree.item(row_id)
        old_value = item["values"][col_index]
        x, y, width, height = tree.bbox(row_id, column)

        entry = Entry(tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, old_value)
        entry.focus()

        def save_edit(event):
            index = int(item["values"][0]) - 1  # Sr.No is index 0
            product = product_entries[index]

            try:
                if col_index in [6, 7, 9]:  # MRP, Qty, Rate
                    new_val = float(entry.get())
                else:
                    new_val = entry.get()
            except ValueError:
                entry.destroy()
                return

            product[col_index] = new_val

            # Re-fetch and parse updated values safely
            try:
                qty = int(product[7]) if col_index != 7 else int(new_val)
            except:
                qty = 1

            try:
                rate = float(product[9]) if col_index != 9 else float(new_val)
            except:
                rate = 0

            try:
                gst_raw = product[8] if col_index != 8 else str(new_val)
                gst_rate = float(gst_raw.replace('%', '')) / 100
            except:
                gst_rate = 0.05

            value = qty * rate
            amount = value + (value * gst_rate)
            product[10] = round(value, 2)
            product[11] = round(amount, 2)

            update_tree()
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    tree.bind("<Double-1>", on_tree_double_click)
