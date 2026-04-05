#!/usr/bin/env python3
"""Parse narrative.md files into structured slide dicts.

Expected format per slide:
    ## Slide N
    Type: <role>
    Variant: <variant-id>[  # auto]
    Content: <text, can be multiline>
    Image: <filename or empty>
    Speaker: <text>
"""
import re
from pathlib import Path


_SLIDE_HEADER = re.compile(r"^##\s+Slide\s+(\d+)\s*$")
_FIELD_PATTERN = re.compile(r"^(Type|Variant|Content|Image|Speaker|Bridge|Context|Ref|Emphasis):\s*(.*)$")


def parse_narrative(path):
    """Parse narrative.md file → list of slide dicts.

    Each slide has: slide_number, type, variant, variant_is_auto, content,
    content_word_count, image, speaker, and any extra fields found.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    slides = []
    current = None
    current_field = None

    for line in lines:
        header_match = _SLIDE_HEADER.match(line)
        if header_match:
            if current is not None:
                _finalize_slide(current)
                slides.append(current)
            current = {"slide_number": int(header_match.group(1))}
            current_field = None
            continue

        if current is None:
            continue  # content before first slide header

        field_match = _FIELD_PATTERN.match(line)
        if field_match:
            key = field_match.group(1).lower()
            value = field_match.group(2).rstrip()
            current[key] = value
            current_field = key
            continue

        # Continuation line for current multiline field (e.g., Content)
        if current_field and line.strip():
            current[current_field] = current.get(current_field, "") + "\n" + line.rstrip()

    if current is not None:
        _finalize_slide(current)
        slides.append(current)

    return slides


def _finalize_slide(slide):
    """Post-process slide dict: parse Variant auto marker, count words, etc."""
    variant_raw = slide.get("variant", "")
    if variant_raw:
        # Detect " # auto" suffix
        if "# auto" in variant_raw:
            slide["variant"] = variant_raw.split("#")[0].strip()
            slide["variant_is_auto"] = True
        else:
            slide["variant"] = variant_raw.strip()
            slide["variant_is_auto"] = False
    else:
        slide["variant"] = None
        slide["variant_is_auto"] = False

    # Word count on content
    content = slide.get("content", "") or ""
    slide["content_word_count"] = len(content.split())

    # Normalize image field (empty string → None)
    image = slide.get("image", "")
    slide["image"] = image.strip() if image and image.strip() else None

    # Normalize type to lowercase
    if "type" in slide:
        slide["type"] = slide["type"].strip().lower()
