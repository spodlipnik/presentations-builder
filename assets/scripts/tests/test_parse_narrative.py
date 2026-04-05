"""Tests for parse_narrative.py — parses narrative.md into structured slides."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from parse_narrative import parse_narrative


def test_parse_narrative_extracts_slides(tmp_path):
    narrative_md = tmp_path / "narrative.md"
    narrative_md.write_text("""# My Talk Narrative

## Slide 1
Type: title
Content: Mohs vs Imiquimod
Image:
Speaker: Welcome everyone.

## Slide 2
Type: assertion-evidence
Variant: ae.image-right
Content: Incidence increased 5% annually
Image: chart.png
Speaker: As we can see...
""", encoding="utf-8")

    slides = parse_narrative(narrative_md)
    assert len(slides) == 2
    assert slides[0]["slide_number"] == 1
    assert slides[0]["type"] == "title"
    assert slides[0]["content"] == "Mohs vs Imiquimod"
    assert slides[0].get("variant") is None
    assert slides[1]["slide_number"] == 2
    assert slides[1]["type"] == "assertion-evidence"
    assert slides[1]["variant"] == "ae.image-right"
    assert slides[1]["variant_is_auto"] is False
    assert slides[1]["image"] == "chart.png"


def test_parse_narrative_detects_auto_variant(tmp_path):
    narrative_md = tmp_path / "narrative.md"
    narrative_md.write_text("""## Slide 1
Type: title
Variant: title.centered  # auto
Content: My Talk
""", encoding="utf-8")

    slides = parse_narrative(narrative_md)
    assert slides[0]["variant"] == "title.centered"
    assert slides[0]["variant_is_auto"] is True


def test_parse_narrative_multiline_content(tmp_path):
    narrative_md = tmp_path / "narrative.md"
    narrative_md.write_text("""## Slide 1
Type: patient-case
Content: 71 year old woman with
facial macule, slow growing
Speaker: Introducing the case.
""", encoding="utf-8")

    slides = parse_narrative(narrative_md)
    assert "71 year old woman with" in slides[0]["content"]
    assert "facial macule, slow growing" in slides[0]["content"]


def test_parse_narrative_empty_returns_empty_list(tmp_path):
    narrative_md = tmp_path / "narrative.md"
    narrative_md.write_text("# Empty narrative\n", encoding="utf-8")
    assert parse_narrative(narrative_md) == []


def test_parse_narrative_counts_words_in_content(tmp_path):
    narrative_md = tmp_path / "narrative.md"
    narrative_md.write_text("""## Slide 1
Type: assertion-evidence
Content: incidence increased five percent annually in Chile
""", encoding="utf-8")
    slides = parse_narrative(narrative_md)
    assert slides[0]["content_word_count"] == 7
