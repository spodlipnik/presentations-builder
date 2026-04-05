#!/usr/bin/env python3
"""Extract structured layout catalog from a reference PPTX file.

Usage:
    python3 extract_references.py --input ref.pptx --output catalog.yaml --theme-name my-theme
"""
from pathlib import Path
from pptx import Presentation


def load_presentation(pptx_path):
    """Load a PPTX file and return the Presentation object."""
    return Presentation(str(pptx_path))
