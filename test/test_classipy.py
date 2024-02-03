import pytest
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
    
        
    
