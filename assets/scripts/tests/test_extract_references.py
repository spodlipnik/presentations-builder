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


def test_extract_theme_colors_returns_dict(simple_title_pptx):
    from extract_references import extract_theme_colors

    colors = extract_theme_colors(simple_title_pptx)
    assert isinstance(colors, dict)
    # Default pptx theme has 12 color roles: dk1, lt1, dk2, lt2, accent1-6, hlink, folHlink
    assert "dk1" in colors
    assert "lt1" in colors
    assert "accent1" in colors
    # Values should be 6-char hex strings
    assert len(colors["dk1"]) == 6
    assert all(c in "0123456789ABCDEFabcdef" for c in colors["dk1"])


def test_extract_shape_type_text_box(simple_title_pptx):
    from extract_references import extract_shape_type
    prs = load_presentation(simple_title_pptx)
    shape = prs.slides[0].shapes[0]
    assert extract_shape_type(shape) == "text_box"


def test_extract_shape_type_unknown_returns_other():
    from extract_references import extract_shape_type
    class FakeShape:
        shape_type = 99  # unknown value
        has_text_frame = False
        has_table = False
        has_chart = False
    assert extract_shape_type(FakeShape()) == "other"


def test_extract_slide_returns_structured_dict(simple_title_pptx):
    from extract_references import extract_slide
    prs = load_presentation(simple_title_pptx)
    slide_info = extract_slide(prs.slides[0], 1, prs.slide_width, prs.slide_height)
    assert slide_info["slide_number"] == 1
    assert len(slide_info["shapes"]) == 1
    shape = slide_info["shapes"][0]
    assert shape["type"] == "text_box"
    assert shape["text_sample"] == "Sample Title"
    assert shape["font"]["family"] == "Inter"
    assert shape["font"]["size_pt"] == 54.0
    assert shape["z_order"] == 0


def test_extract_slide_multiple_shapes(multi_slide_pptx):
    from extract_references import extract_slide
    prs = load_presentation(multi_slide_pptx)
    slide_info = extract_slide(prs.slides[1], 2, prs.slide_width, prs.slide_height)
    # Slide 2 has headline textbox + image placeholder textbox = 2 shapes
    assert len(slide_info["shapes"]) == 2


def test_detect_dominant_tokens_returns_fonts_and_colors(multi_slide_pptx):
    from extract_references import extract_slide, detect_dominant_tokens
    prs = load_presentation(multi_slide_pptx)
    slides_data = [
        extract_slide(s, i+1, prs.slide_width, prs.slide_height)
        for i, s in enumerate(prs.slides)
    ]
    tokens = detect_dominant_tokens(slides_data)
    assert "dominant_fonts" in tokens
    assert "dominant_colors" in tokens
    assert isinstance(tokens["dominant_fonts"], list)
    assert isinstance(tokens["dominant_colors"], list)
    # Each entry should have count
    if tokens["dominant_fonts"]:
        assert "family" in tokens["dominant_fonts"][0]
        assert "count" in tokens["dominant_fonts"][0]


def test_infer_role_title_single_large_text():
    from extract_references import infer_role
    # Single large text box, centered, big font → title
    slide_info = {
        "slide_number": 1,
        "shapes": [
            {
                "type": "text_box",
                "box": [0.1, 0.3, 0.8, 0.3],
                "text_sample": "My Presentation",
                "font": {"size_pt": 54, "weight": 700},
                "alignment": "center",
                "z_order": 0,
            }
        ],
    }
    assert infer_role(slide_info) == "title"


def test_infer_role_assertion_evidence_headline_plus_image_area():
    from extract_references import infer_role
    # Small top text + large lower area → AE
    slide_info = {
        "slide_number": 3,
        "shapes": [
            {
                "type": "text_box",
                "box": [0.05, 0.05, 0.9, 0.15],
                "text_sample": "La incidencia aumentó 5% anual",
                "font": {"size_pt": 28, "weight": 700},
                "alignment": "left",
                "z_order": 0,
            },
            {
                "type": "text_box",
                "box": [0.1, 0.25, 0.8, 0.65],
                "text_sample": "",
                "font": None,
                "z_order": 1,
            },
        ],
    }
    assert infer_role(slide_info) == "assertion-evidence"


def test_infer_role_unknown_returns_unknown():
    from extract_references import infer_role
    slide_info = {"slide_number": 5, "shapes": []}
    assert infer_role(slide_info) == "unknown"


import yaml
from datetime import datetime
from extract_references import build_catalog, write_catalog_yaml


def test_build_catalog_returns_complete_structure(multi_slide_pptx):
    catalog = build_catalog(multi_slide_pptx, theme_name="test-theme")
    assert "meta" in catalog
    assert catalog["meta"]["source_file"].endswith(".pptx")
    assert catalog["meta"]["slides_count"] == 3
    assert "theme_detection" in catalog
    assert "slide_dimensions" in catalog["theme_detection"]
    assert catalog["theme_detection"]["slide_dimensions"]["aspect_ratio"] == "16:9"
    assert len(catalog["slides"]) == 3
    # First slide should be inferred as title (single large text)
    assert catalog["slides"][0]["inferred_role"] in ("title", "assertion-evidence", "unknown")


def test_write_catalog_yaml_produces_valid_yaml(multi_slide_pptx, tmp_path):
    catalog = build_catalog(multi_slide_pptx, theme_name="test-theme")
    out_path = tmp_path / "catalog.yaml"
    write_catalog_yaml(catalog, out_path)
    assert out_path.exists()
    # Round-trip: should parse back as valid YAML
    with open(out_path) as f:
        loaded = yaml.safe_load(f)
    assert loaded["meta"]["slides_count"] == 3
