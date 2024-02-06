"""Automated test cases for classiPY functions"""
import math
import re
import tempfile
from pathlib import Path
import pytest
from wand.image import Image
from wand.color import Color
from src import classiPY


def test_markings():
    """Verify correct marking options exist"""
    markings = classiPY.Markings()
    levels = ["CUI", "S", "U"]
    for level in levels:
        assert level == markings.get_symbol(level)


@pytest.mark.parametrize("level,full_name,color", [
    ("CUI", "CUI", "#502b85"),
    ("S", "SECRET", "red"),
    ("U", "UNCLASSIFIED", "green"),
    ])
def test_marking_output(level, full_name, color):
    """Verify correct mappings between short-hand labels and marks that
    will appear on immages and banner colors"""
    markings = classiPY.Markings()
    assert markings.get_long_name(level) == full_name
    assert markings.get_color(level) == color


def count_pixel_colors(filename, banner_percent=5):
    pixels = []
    width, height = 0, 0
    blob = None
    with Image(filename=filename) as img:
        img.depth = 8
        blob = img.make_blob(format='RGB')
        width, height = img.width, img.height
    top_banner = int(width * height * (banner_percent / 100) * 3)
    for cursor in range(width * 3, top_banner, 3):
        pixels.append(
            (blob[cursor], blob[cursor + 1], blob[cursor + 2])
        )
    most_freq = max(set(pixels), key=pixels.count)
    return most_freq


@pytest.mark.parametrize("level, color", [
    ("CUI", "#502b85"),
    ("S", "red"),
    ("U", "green"),
    ])
def test_banners(level, color):
    """Verify correct file renaming, banner colors"""
    with tempfile.TemporaryDirectory(dir=Path('/tmp').resolve()) as tempdir:
        classiPY.label_folder(
            Path('./figs').resolve(), Path(tempdir.name),
            classification=level
        )
        filenames = list(Path(tempdir.name).glob('*.*'))
        num_test_files = len(list(Path("./figs").resolve().glob('[!.]*.*')))
        assert len(filenames) == num_test_files
        for filename in filenames:
            assert re.search(f"^({level})*", filename.name)
            banner_color = count_pixel_colors(filename)
            correct_color = (
                Color(color).red_int8, Color(color).green_int8,
                Color(color).blue_int8
            )
            for i, j in zip(banner_color, correct_color):
                assert math.isclose(i, j, abs_tol=2)
