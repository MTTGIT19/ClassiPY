#!/usr/bin/env python3
import argparse
import pathlib
import os
from glob import glob
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

banner_percentage_of_height = 5  # Adjust the percentage as needed
font_percentage_of_banner = 50  # Adjust the font size percentage as needed

def add_banner(input_image, output_image, classification='CUI'):
    with Image(filename=input_image) as img:
        banner_height = int(img.height * (banner_percentage_of_height / 100))
        banner = Image(width=img.width, height=banner_height)
        if classification=='CUI':
            banner.background_color = Color('#502b85')
        elif classification=='S':
            banner.background_color = Color('red')
        banner.alpha_channel = 'remove'
        
        # Calculate font size based on a percentage of the banner's height
        font_size = int(banner_height * (font_percentage_of_banner / 100))

        with Drawing() as draw:
            #draw.font = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # Path to your font file or try 'Times new roman'
            draw.font_size = font_size
            draw.fill_color = Color('white')
            draw.text_alignment = 'center'
            if classification=='CUI':
                draw.text(x=banner.width // 2,
                          y=banner_height // 2 + font_size // 3, body='CUI')
                draw.text(x=banner.width // 2,
                          y=img.height + banner_height +
                          banner_height // 2 + font_size // 3, body='CUI')
            elif classification=='S':
                draw.text(x=banner.width // 2,
                          y=banner_height // 2 + font_size // 3, body='SECRET')
                draw.text(x=banner.width // 2,
                          y=img.height + banner_height +
                          banner_height // 2 + font_size // 3, body='SECRET')                
            draw(banner)
           # Calculate font size based on the banner's height
           # font_size = int(banner_height * 6)

        with Image(filename=input_image) as img:  # Re-open the image to avoid closure issue
            with Image(width=img.width,
                       height=img.height + 2 * banner_height) as result:
                result.composite(banner, top=0, left=0)
                result.composite(img, top=banner_height, left=0)
                result.composite(banner, top=img.height + banner_height,
                                 left=0)
                border_style = 6  # Change border 
                result.border(color=Color('black'), width=border_style,
                              height=border_style)
                result.save(filename=output_image)

def label_folder(input_folder, output_folder, classification='CUI'):
    if not pathlib.Path(output_folder).exists():
        os.makedirs(output_folder)

    extensions = ['.jpg', '.png', '.jpeg']
    image_files = [x for x in pathlib.Path(input_folder).iterdir()
                   if x.suffix.lower() in extensions]
    
    for image_file in image_files:
        if classification=='CUI':
            output_file = pathlib.Path(output_folder,
                                       f"(CUI) {image_file.name}")
        elif classification=='S':
            output_file = pathlib.Path(output_folder,
                                       f"(S) {image_file.name}")
        add_banner(image_file, output_file, classification)


def main():
    parser = argparse.ArgumentParser(description="Add classificaiton banner to folder of images")
    parser.add_argument('--image', '-I', required=True, type=str,
                        help='path to image folder')
    parser.add_argument('--output', '-O', required=False, type=str,
                        help='path folder of tagged images')
    parser.add_argument('--classification', '-C', required=True, type=str,
                        choices=['CUI', 'S'],
                        help='Level to classify images: CUI or S')
    args = parser.parse_args()
    args.image = pathlib.Path(args.image).resolve()
    if not args.output:
        args.output = args.image
    else:
        args.output = pathlib.Path(args.output).resolve()
    cwd = pathlib.Path.cwd()
    label_folder(args.image, args.output, args.classification)

if __name__=='__main__':
    main()
