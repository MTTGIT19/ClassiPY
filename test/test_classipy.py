import pytest
import tempfile
import re
from pathlib import Path
from src import classiPY


def test_markings():
    markings = classiPY.Markings()
    levels = ["CUI", "S", "U"]
    for level in levels:
        assert level == markings.get_symbol(level)

@pytest.mark.parametrize("level,full_name,color",[
    ("CUI", "CUI", "#502b85"),
    ("S", "SECRET", "red"),
    ("U", "UNCLASSIFIED", "green"),
    ])
def test_marking_output(level, full_name, color):
    markings = classiPY.Markings()
    assert markings.get_long_name(level) == full_name
    assert markings.get_color(level) == color

@pytest.mark.parametrize("level", [
    ("CUI"),
    ("S"),
    ("U"),
    ])
def test_banners(level):
    markings = classiPY.Markings()
    tempdir = tempfile.TemporaryDirectory(dir=Path('./figs'))
    classiPY.label_folder(Path('./figs'), Path(tempdir.name),
                          classification=level)
    filenames = list(Path(tempdir.name).glob('*.*'))
    assert len(filenames) == len(list(Path("./figs")))
    for filename in filenames:
        assert re.search("^({}) *".format(level), str(filename))
    tempdir.cleanup()
    
