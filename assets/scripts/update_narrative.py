#!/usr/bin/env python3
"""Write variant selections back to narrative.md with `# auto` markers.

Respects user-locked variants (those without `# auto` suffix).
"""
import re
from pathlib import Path


_SLIDE_HEADER = re.compile(r"^##\s+Slide\s+(\d+)\s*$")
_VARIANT_LINE = re.compile(r"^(Variant:\s*)(.+?)\s*$")


def update_narrative_variants(narrative_path, slide_variants):
    """Update narrative.md with auto-chosen variants.

    Args:
        narrative_path: path to narrative.md
        slide_variants: dict {slide_number: variant_id}

    Behavior:
    - If a slide already has a Variant: line WITH `# auto` marker → replace value
    - If a slide has a Variant: line WITHOUT `# auto` → leave it alone (user-locked)
    - If a slide has no Variant: line → insert one after Type: line
    """
    narrative_path = Path(narrative_path)
    lines = narrative_path.read_text(encoding="utf-8").split("\n")

    # First pass: find slide boundaries and existing variants
    # Each entry: (start_idx, end_idx, slide_num, variant_line_idx_or_None, is_auto)
    slides = []
    cur_start = None
    cur_num = None
    cur_var_idx = None
    cur_is_auto = False

    for i, line in enumerate(lines):
        m = _SLIDE_HEADER.match(line)
        if m:
            if cur_start is not None:
                slides.append((cur_start, i, cur_num, cur_var_idx, cur_is_auto))
            cur_start = i
            cur_num = int(m.group(1))
            cur_var_idx = None
            cur_is_auto = False
            continue
        vm = _VARIANT_LINE.match(line)
        if vm and cur_start is not None and cur_var_idx is None:
            cur_var_idx = i
            cur_is_auto = "# auto" in vm.group(2)

    if cur_start is not None:
        slides.append((cur_start, len(lines), cur_num, cur_var_idx, cur_is_auto))

    # Second pass: build modification plan
    replacements = {}
    insertions = {}

    for start, end, num, var_idx, is_auto in slides:
        new_variant = slide_variants.get(num)
        if not new_variant:
            continue
        if var_idx is not None:
            if is_auto:
                replacements[var_idx] = f"Variant: {new_variant}  # auto"
            # else: user-locked, do not modify
        else:
            # No Variant line — insert after first Type: line in slide range
            for i in range(start + 1, end):
                if lines[i].startswith("Type:"):
                    insertions[i] = f"Variant: {new_variant}  # auto"
                    break

    # Apply changes
    output = []
    for i, line in enumerate(lines):
        if i in replacements:
            output.append(replacements[i])
        else:
            output.append(line)
        if i in insertions:
            output.append(insertions[i])

    narrative_path.write_text("\n".join(output), encoding="utf-8")
