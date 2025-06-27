import os
from reportlab.lib.utils import ImageReader

def draw_footer_image(c, box_x, box_y, box_width, image_path):
    # Adjust this path or pass it dynamically if needed
    #image_path = r"C:\Users\nikes\Downloads\Saurav-sign.png"

    if os.path.exists(image_path):
        image_width = 60
        image_height = 40
        image_x = box_x + box_width - image_width - 10
        image_y = box_y + 5

        try:
            c.drawImage(ImageReader(image_path), image_x, image_y, width=image_width, height=image_height, mask='auto')
        except Exception as e:
            print(f"Error drawing image: {e}")
