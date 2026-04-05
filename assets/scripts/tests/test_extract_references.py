"""Tests for extract_references.py — uses real PPTX fixtures, no mocks."""
import sys
from pathlib import Path

# Add scripts dir to path so we can import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_references import load_presentation, get_slide_dimensions, extract_shape_box


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


def test_extract_shape_box_returns_fractions(simple_title_pptx):
    prs = load_presentation(simple_title_pptx)
    slide = prs.slides[0]
    shape = slide.shapes[0]
    box = extract_shape_box(shape, prs.slide_width, prs.slide_height)
    # Shape was at left=1.0in, top=2.0in, width=11.0in, height=1.5in
    # Slide is 13.333in x 7.5in → fractions should be ~[0.075, 0.267, 0.825, 0.2]
    assert abs(box[0] - 0.075) < 0.005  # x = 1/13.333
    assert abs(box[1] - 0.267) < 0.005  # y = 2/7.5
    assert abs(box[2] - 0.825) < 0.005  # w = 11/13.333
    assert abs(box[3] - 0.200) < 0.005  # h = 1.5/7.5


def test_extract_font_info_returns_formatting(simple_title_pptx):
    from extract_references import extract_font_info

    prs = load_presentation(simple_title_pptx)
    shape = prs.slides[0].shapes[0]
    font = extract_font_info(shape)
    assert font is not None
    assert font["family"] == "Inter"
    assert font["size_pt"] == 54.0
    assert font["weight"] == 700  # bold
    assert font["color_rgb"] == "1A1A1A"


def test_extract_font_info_returns_none_for_non_text_shape(simple_title_pptx):
    from extract_references import extract_font_info

    # Title textbox IS a text shape; we test None path by passing fake shape
    class FakeShape:
        has_text_frame = False

    assert extract_font_info(FakeShape()) is None
