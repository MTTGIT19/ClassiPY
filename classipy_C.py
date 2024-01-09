#!/usr/bin/env python3
import os
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

current_directory = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(current_directory, 'input_images')  # Folder named input_images
output_folder = ('/home/'+ os.getlogin() +'/Desktop/CUI_IMAGES/')  # Folder named output_images

# If you'd like to get fancy you can edit the next two lines to change the input/output paths. 
#input_folder = '/home/' + os.getlogin() + '/Downloads/screenshots1/' ## CHANGE ME TO SCREENSHOT PATH
#output_folder = '/home/' + os.getlogin() + '/Desktop/SECRET_IMAGES/' # Output location: default desktop

def add_banner_and_border_to_image(input_image, output_image):
    with Image(filename=input_image) as img:
        banner_height = int(img.height * 0.05)
        banner = Image(width=img.width, height=banner_height)
        banner.background_color = Color('#502b85')
        banner.alpha_channel = 'remove'

        with Drawing() as draw:
            draw.font = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # Path to your font file or try 'Times new roman'
            draw.font_size = 14
            draw.fill_color = Color('white')
            draw.text_alignment = 'center'
            draw.text(int(banner.width / 2), int(banner.height / 2) + 3, 'CUI')
            draw(banner)

        with Image(filename=input_image) as img:  # Re-open the image to avoid closure issue
            with Image(width=img.width, height=img.height + 2 * banner_height) as result:
                result.composite(banner, top=0, left=0)
                result.composite(img, top=banner_height, left=0)
                result.composite(banner, top=img.height + banner_height, left=0)

                border_style = 6  # Change border 
                result.border(color=Color('black'), width=border_style, height=border_style)
                result.save(filename=output_image)

def label_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(current_directory):
        for filename in files:
            if filename.lower().endswith(".jpg") or filename.lower().endswith(".png"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(output_folder, f"(CUI) {filename}")

                add_banner_and_border_to_image(input_path, output_path)

label_folder(current_directory, output_folder)