#!/usr/bin/env python3
"""Validate a docs/narrative.md against the 12-canonical-type schema.

Used by talk-slides as an executable guard before delegating to document-skills:pptx.
Without this, the rejection of legacy v1 narratives relies purely on instruction-following.

Usage:
  python3 validate_narrative.py path/to/narrative.md [--project-root DIR]

Exits 0 on success; 1 on any validation error (printed to stderr).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Canonical 12 types and their required fields. Mirrors .claude/rules/canonical-types.md.
TYPE_SCHEMA: dict[str, set[str]] = {
    "title": {"title", "author", "affiliation"},
    "text-list": {"title", "items"},
    "divider": {"section_label", "section_title"},
    "assertion-evidence": {"headline", "image"},
    "assertion-evidence-left": {"headline", "image"},
    "chart": {"headline", "chart_image"},
    "callout": {"big_text", "sub_label"},
    "quote": {"quote_text", "attribution"},
    "comparison": {"headline", "left_label", "left_content", "right_label", "right_content"},
    "gallery": {"headline", "image_1", "image_2", "image_3", "image_4"},
    "fullbleed": {"image_full"},
    "closing": {"main_text", "contact_info"},
}

# Image-bearing fields per type — paths must point to existing files (after stripping
# inline-comment annotations like "# or [GENERATE]" and quotes).
IMAGE_FIELDS: dict[str, set[str]] = {
    "assertion-evidence": {"image"},
    "assertion-evidence-left": {"image"},
    "chart": {"chart_image"},
    "gallery": {"image_1", "image_2", "image_3", "image_4"},
    "fullbleed": {"image_full"},
}

# Bracketed placeholders that are valid in image fields (no file expected yet).
PLACEHOLDER_RE = re.compile(r"^\[(?:GENERATE|SPEAKER ADDS|TBD)[^\]]*\]")

SLIDE_HEADER_RE = re.compile(r"^###\s+Slide\s+(\d+|\w+)[:\s]", re.MULTILINE)
FIELD_RE = re.compile(r"^-\s+\*\*([a-z_][a-z0-9_]*):\*\*\s*(.*?)\s*$", re.MULTILINE)


def parse_slides(content: str) -> list[dict]:
    """Split narrative content into per-slide records.

    Each record is a dict of fieldname → raw value string. The slide's positional
    label (e.g. "5") is stored under the special key `_slide_label`.
    """
    headers = list(SLIDE_HEADER_RE.finditer(content))
    if not headers:
        return []

    slides: list[dict] = []
    for i, header in enumerate(headers):
        label = header.group(1)
        body_start = header.end()
        body_end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
        body = content[body_start:body_end]

        record: dict = {"_slide_label": label}
        for m in FIELD_RE.finditer(body):
            field, value = m.group(1), m.group(2)
            # Strip a trailing inline comment (e.g., "images/foo.png  # or [GENERATE]")
            value = re.sub(r"\s+#.*$", "", value).strip()
            # Strip surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            record[field] = value
        slides.append(record)
    return slides


def resolve_image_path(raw: str, project_root: Path) -> Path:
    """Resolve narrative.md image path to absolute Path (relative paths are CWD-relative)."""
    p = Path(raw)
    if p.is_absolute():
        return p
    return (project_root / p).resolve()


def validate_slide(slide: dict, project_root: Path) -> list[str]:
    """Return a list of error strings for this slide. Empty list = valid."""
    label = slide.get("_slide_label", "?")
    errors: list[str] = []

    slide_type = slide.get("type")
    if not slide_type:
        errors.append(f"Slide {label}: missing `type:` field")
        return errors

    if slide_type not in TYPE_SCHEMA:
        valid = ", ".join(sorted(TYPE_SCHEMA))
        errors.append(
            f"Slide {label}: type={slide_type!r} is not one of the 12 canonical types. "
            f"Legacy v1 type — see CHANGELOG.md 2.0.0 migration table. Valid: {valid}"
        )
        return errors

    required = TYPE_SCHEMA[slide_type]
    for field in sorted(required):
        if not slide.get(field):
            errors.append(f"Slide {label} (type={slide_type}): missing required field `{field}`")

    for field in IMAGE_FIELDS.get(slide_type, set()):
        raw = slide.get(field)
        if not raw:
            # Missing-required-field error already reported above; skip path check.
            continue
        if PLACEHOLDER_RE.match(raw):
            continue
        path = resolve_image_path(raw, project_root)
        if not path.exists():
            errors.append(
                f"Slide {label} (type={slide_type}): `{field}` points to "
                f"{raw!r} which does not exist (resolved: {path})"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("narrative", type=Path, help="Path to docs/narrative.md")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root for resolving image paths (default: narrative's parent's parent)",
    )
    args = parser.parse_args()

    if not args.narrative.is_file():
        print(f"❌ {args.narrative}: not a file", file=sys.stderr)
        return 1

    project_root = args.project_root or args.narrative.resolve().parent.parent
    content = args.narrative.read_text(encoding="utf-8")

    slides = parse_slides(content)
    if not slides:
        print(f"❌ {args.narrative}: no slides parsed (expected `### Slide N: ...` headers)", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for slide in slides:
        all_errors.extend(validate_slide(slide, project_root))

    if all_errors:
        print(f"❌ {len(all_errors)} validation error(s) in {args.narrative}:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"✅ Narrative valid: {len(slides)} slides, all using the 12 canonical types.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
