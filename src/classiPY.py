#!/usr/bin/env python3
"""This module provides an interface for labelling all images in a folder"""
import argparse
from pathlib import Path
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

BANNER_PERCENT_OF_HEIGHT = 5  # Adjust the percentage as needed. Change line 53 if needed. 
FONT_PERCENT_OF_BANNER = 50  # Adjust the font size percentage as needed
EXTS = (".jpg", ".png", ".jpeg")  # file extensions to look for
MARKS = ("CUI", "S", "U")


class Markings:
    """Class to define marking options. Currently: Unclass, CUI, & Secret"""
    def __init__(self, classifications=MARKS):
        self.classifications = classifications

    def get_symbol(self, classification):
        """Return short-hand symbol for classification"""
        return classification

    def get_long_name(self, classification):
        """Return full name of classification level"""
        out = None
        if classification == "CUI":
            out = "CUI"
        elif classification == "S":
            out = "SECRET"
        elif classification == "U":
            out = "UNCLASSIFIED"
        return out

    def get_color(self, classification):
        """Return color for banner matching classification level"""
        out = None
        if classification == "CUI":
            out = "#502b85"
        elif classification == "S":
            out = "red"
        elif classification == "U":
            out = "green"
        return out


markings = Markings()


def add_banner(input_image, output_image, classification="CUI"):
    """Function to add top & bottom portion markings to image file"""
    with Image(filename=input_image) as img:
        banner_height = int(30)  ## Alternative (img.height * (BANNER_PERCENT_OF_HEIGHT / 100))
        banner = Image(width=img.width, height=banner_height)
        banner.background_color = markings.get_color(classification)
        banner.alpha_channel = "remove"

        # Calculate font size based on a percentage of the banner's height
        font_size = int(banner_height * (FONT_PERCENT_OF_BANNER / 90))

        with Drawing() as draw:
            draw.font_size = font_size
            draw.font_weight = 700  # Bold font weight
            draw.fill_color = Color("white")
            draw.text_alignment = "center"
            draw.text(
                x=banner.width // 2,
                y=banner_height // 2 + font_size // 3,
                body=markings.get_long_name(classification),
            )
            draw.text(
                x=banner.width // 2,
                y=img.height + 2 * banner_height // 2 + font_size // 3,
                body=markings.get_long_name(classification),
            )
            draw(banner)

        with Image(
            filename=input_image
        ) as img:  # Re-open the image to avoid closure issue
            with Image(
                width=img.width, height=img.height + 2 * banner_height
            ) as result:
                result.composite(banner, top=0, left=0)
                result.composite(img, top=banner_height, left=0)
                result.composite(banner, top=img.height + banner_height, left=0)
                border_style = 6  # Change border
                result.border(
                    color=Color("black"), width=border_style,
                    height=border_style
                )
                result.save(filename=output_image)


def label_folder(input_folder, output_folder, classification="CUI"):
    """Function to rename all files with classification marking \
    Calls the `add_banner` function to mark images """
    if not Path(output_folder).exists():
        output_folder.mkdir(parents=True, exist_ok=True)

    image_files = [
        x for x in Path(input_folder).iterdir() if x.suffix.lower() in EXTS
    ]

    for image_file in image_files:
        output_file = Path(
            output_folder, f"({markings.get_symbol(classification)}) {image_file.name}"
        )
        add_banner(image_file, output_file, classification)


def main():
    parser = argparse.ArgumentParser(
        description="Adds classification banners to a folder of images"
    )

    # Adding required arguments as group
    required_group = parser.add_argument_group("Required arguments")
    required_group.add_argument(
        "--images", "-I", required=True, type=str,
        help="Folder path to orginal images"
    )
    required_group.add_argument(
        "--classification",
        "-C",
        required=True,
        type=str,
        choices=markings.classifications,
        help="Classification level (S or CUI)",
    )

    # Adding optional argument as group
    optional_group = parser.add_argument_group("Optional arguments")
    optional_group.add_argument(
        "--output",
        "-O",
        type=str,
        help="Folder path for newly labeled images (will be created if it does not exist)",
    )

    args = parser.parse_args()

    # Resolving and setting absolute paths using pathlib
    args.images = Path(args.images).resolve()
    args.output = args.images if args.output is None else Path(args.output).resolve()

    label_folder(args.images, args.output, args.classification)


if __name__ == "__main__":
    main()
