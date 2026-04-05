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
