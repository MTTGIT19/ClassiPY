#!/usr/bin/env python3

import argparse
from pathlib import Path
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

banner_percent_of_height = 5  # Adjust the percentage as needed
font_percent_of_banner = 50  # Adjust the font size percentage as needed
extensions = [".jpg", ".png", ".jpeg"]  # file extensions to look for


class Markings:
    def __init__(self, classifications):
        self.classifications = classifications

    def get_symbol(self, classification):
        if classification == "CUI":
            return "CUI"
        elif classification == "S":
            return "S"

    def get_long_name(self, classification):
        if classification == "CUI":
            return "CUI"
        elif classification == "S":
            return "SECRET"

    def get_color(self, classification):
        if classification == "CUI":
            return "#502b85"
        elif classification == "S":
            return "red"


markings = Markings(["CUI", "S"])


def add_banner(input_image, output_image, classification="CUI"):
    with Image(filename=input_image) as img:
        banner_height = int(img.height * (banner_percent_of_height / 100))
        banner = Image(width=img.width, height=banner_height)
        banner.background_color = markings.get_color(classification)
        banner.alpha_channel = "remove"

        # Calculate font size based on a percentage of the banner's height
        font_size = int(banner_height * (font_percent_of_banner / 90))

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
                y=img.height + banner_height + banner_height // 2 + font_size // 3,
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
                    color=Color("black"), width=border_style, height=border_style
                )
                result.save(filename=output_image)


def label_folder(input_folder, output_folder, classification="CUI"):
    if not Path(output_folder).exists():
        output_folder.mkdir(parents=True, exist_ok=True)

    image_files = [
        x for x in Path(input_folder).iterdir() if x.suffix.lower() in extensions
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
        "--image", "-I", required=True, type=str, help="Folder path to orginal images"
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
    args.image = Path(args.image).resolve()
    args.output = args.image if args.output is None else Path(args.output).resolve()

    label_folder(args.image, args.output, args.classification)


if __name__ == "__main__":
    main()
