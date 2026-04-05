"""Tests for extract_references.py — uses real PPTX fixtures, no mocks."""
import sys
from pathlib import Path

# Add scripts dir to path so we can import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_references import load_presentation, get_slide_dimensions


def test_load_presentation_returns_presentation(simple_title_pptx):
    prs = load_presentation(simple_title_pptx)
    assert prs is not None
    assert len(prs.slides) == 1


def test_get_slide_dimensions_returns_inches(simple_title_pptx):
    prs = load_presentation(simple_title_pptx)
    dims = get_slide_dimensions(prs)
    assert dims["width_in"] == 13.333
    assert dims["height_in"] == 7.5
    assert dims["aspect_ratio"] == "16:9"
