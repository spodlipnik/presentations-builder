#!/usr/bin/env python3
"""Extract structured layout catalog from a reference PPTX file.

Usage:
    python3 extract_references.py --input ref.pptx --output catalog.yaml --theme-name my-theme
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu


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
