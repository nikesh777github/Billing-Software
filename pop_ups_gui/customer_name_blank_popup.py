from tkinter import messagebox

def confirm_blank_customer():
    response = messagebox.askquestion(
        "Customer Name Is Blank",
        "Customer Name is blank. Do you want to continue?",
        icon='warning'
    )
    return response == 'yes'

def confirm_no_products():
    response = messagebox.askquestion(
        "No Products Added",
        "No products have been added. Do you want to continue?",
        icon='warning'
    )
    return response == 'yes'