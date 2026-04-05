#!/usr/bin/env python3
"""Extract structured layout catalog from a reference PPTX file.

Usage:
    python3 extract_references.py --input ref.pptx --output catalog.yaml --theme-name my-theme
"""
import zipfile
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from lxml import etree


EMU_PER_INCH = 914400


def load_presentation(pptx_path):
    """Load a PPTX file and return the Presentation object."""
    return Presentation(str(pptx_path))


def get_slide_dimensions(prs):
    """Return slide dimensions as dict with width_in, height_in, aspect_ratio."""
    width_in = round(prs.slide_width / EMU_PER_INCH, 3)
    height_in = round(prs.slide_height / EMU_PER_INCH, 3)
    ratio = width_in / height_in
    # Common ratios
    if abs(ratio - 16/9) < 0.01:
        aspect = "16:9"
    elif abs(ratio - 4/3) < 0.01:
        aspect = "4:3"
    else:
        aspect = f"{width_in}:{height_in}"
    return {
        "width_in": width_in,
        "height_in": height_in,
        "aspect_ratio": aspect,
    }


def extract_shape_box(shape, slide_width_emu, slide_height_emu):
    """Return [x, y, w, h] as fractions (0-1) of slide dimensions.

    Fractions are resolution-independent and readable.
    """
    return [
        round(shape.left / slide_width_emu, 3),
        round(shape.top / slide_height_emu, 3),
        round(shape.width / slide_width_emu, 3),
        round(shape.height / slide_height_emu, 3),
    ]


def extract_font_info(shape):
    """Extract font info from first run of first paragraph of a text shape.

    Returns None if shape has no text frame or no runs.
    Returns dict with family, size_pt, weight, color_rgb (may have None values).
    """
    if not getattr(shape, "has_text_frame", False):
        return None
    tf = shape.text_frame
    if not tf.paragraphs or not tf.paragraphs[0].runs:
        return None

    run = tf.paragraphs[0].runs[0]
    font = run.font

    # Weight: python-pptx gives bool bold; convert to OpenType weight
    if font.bold is True:
        weight = 700
    elif font.bold is False:
        weight = 400
    else:
        weight = None  # inherited

    # Color: only extract RGB, not theme colors (handled separately in Task 9)
    color_rgb = None
    try:
        if font.color.type is not None and hasattr(font.color, "rgb") and font.color.rgb is not None:
            color_rgb = str(font.color.rgb)
    except (AttributeError, TypeError):
        pass

    return {
        "family": font.name,
        "size_pt": font.size.pt if font.size else None,
        "weight": weight,
        "color_rgb": color_rgb,
    }


# OOXML namespaces for theme XML
_THEME_NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

# Order of color roles in theme1.xml clrScheme element
_THEME_COLOR_ORDER = [
    "dk1", "lt1", "dk2", "lt2",
    "accent1", "accent2", "accent3", "accent4", "accent5", "accent6",
    "hlink", "folHlink",
]


def extract_theme_colors(pptx_path):
    """Parse ppt/theme/theme1.xml from PPTX zip and return role→hex color map.

    Returns dict like {"dk1": "000000", "lt1": "FFFFFF", "accent1": "4472C4", ...}
    """
    with zipfile.ZipFile(str(pptx_path), "r") as z:
        # Find first theme file (most PPTX have exactly one)
        theme_files = [n for n in z.namelist() if n.startswith("ppt/theme/theme") and n.endswith(".xml")]
        if not theme_files:
            return {}
        with z.open(theme_files[0]) as f:
            tree = etree.parse(f)

    root = tree.getroot()
    # Find <a:clrScheme> which contains the 12 theme colors in order
    clr_scheme = root.find(".//a:clrScheme", _THEME_NS)
    if clr_scheme is None:
        return {}

    colors = {}
    # Each child of clrScheme is a color role: <a:dk1>, <a:lt1>, etc.
    # Inside each is either <a:srgbClr val="HEX"/> or <a:sysClr lastClr="HEX"/>
    for role_name in _THEME_COLOR_ORDER:
        role_elem = clr_scheme.find(f"a:{role_name}", _THEME_NS)
        if role_elem is None:
            continue
        srgb = role_elem.find("a:srgbClr", _THEME_NS)
        sysclr = role_elem.find("a:sysClr", _THEME_NS)
        if srgb is not None:
            colors[role_name] = srgb.get("val", "").upper()
        elif sysclr is not None:
            colors[role_name] = sysclr.get("lastClr", "").upper()

    return colors


def extract_shape_type(shape):
    """Categorize shape as: text_box, image, table, chart, group, placeholder, or other.

    Handles SmartArt safely (returns 'other' without raising).
    """
    try:
        st = shape.shape_type
    except (AttributeError, NotImplementedError):
        return "other"

    # Check graphic frames first (tables/charts live inside these)
    if getattr(shape, "has_table", False):
        return "table"
    if getattr(shape, "has_chart", False):
        return "chart"
    if st == MSO_SHAPE_TYPE.GROUP:
        return "group"
    if st == MSO_SHAPE_TYPE.PICTURE:
        return "image"
    if st == MSO_SHAPE_TYPE.PLACEHOLDER:
        return "placeholder"
    if getattr(shape, "has_text_frame", False):
        return "text_box"
    return "other"


def iter_shapes_recursive(shapes):
    """Yield all shapes, recursing into groups. Skips SmartArt safely.

    Returns (shape, z_order) tuples. z_order is the iteration index (0-based,
    first = back).
    """
    z = 0
    for shape in shapes:
        try:
            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                for inner_shape, _ in iter_shapes_recursive(shape.shapes):
                    yield inner_shape, z
                    z += 1
                continue
        except (AttributeError, NotImplementedError):
            # SmartArt or unsupported — skip gracefully
            continue
        yield shape, z
        z += 1
