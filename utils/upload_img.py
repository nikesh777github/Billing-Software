from reportlab.lib.utils import ImageReader

def draw_footer_image(c, x, y, width, img_path, height=None):
    try:
        img = ImageReader(img_path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)

        if height is None:
            height = width * aspect  # auto maintain aspect ratio

        c.drawImage(img, x, y, width=width, height=height, mask='auto')
    except Exception as e:
        print(f"Error loading image: {e}")
