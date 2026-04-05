"""Tests for update_narrative.py — writes Variant: decisions back to narrative.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from update_narrative import update_narrative_variants


def test_update_narrative_adds_auto_marker(tmp_path):
    narrative = tmp_path / "narrative.md"
    narrative.write_text("""## Slide 1
Type: title
Content: My Talk

## Slide 2
Type: assertion-evidence
Content: Evidence
""", encoding="utf-8")

    update_narrative_variants(narrative, {1: "title.centered", 2: "ae.image-right"})
    text = narrative.read_text(encoding="utf-8")
    assert "Variant: title.centered  # auto" in text
    assert "Variant: ae.image-right  # auto" in text


def test_update_narrative_replaces_existing_auto_marker(tmp_path):
    narrative = tmp_path / "narrative.md"
    narrative.write_text("""## Slide 1
Type: title
Variant: title.image-left  # auto
Content: My Talk
""", encoding="utf-8")

    update_narrative_variants(narrative, {1: "title.centered"})
    text = narrative.read_text(encoding="utf-8")
    assert "Variant: title.centered  # auto" in text
    assert "title.image-left" not in text


def test_update_narrative_preserves_locked_variants(tmp_path):
    narrative = tmp_path / "narrative.md"
    narrative.write_text("""## Slide 1
Type: title
Variant: title.centered
Content: My Talk
""", encoding="utf-8")
    # User-locked (no # auto) — should NOT be changed
    update_narrative_variants(narrative, {1: "title.image-left"})
    text = narrative.read_text(encoding="utf-8")
    assert "Variant: title.centered" in text
    assert "title.image-left" not in text
    assert "# auto" not in text
