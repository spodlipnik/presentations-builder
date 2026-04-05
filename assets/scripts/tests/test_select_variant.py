"""Tests for select_variant.py — rubric-based variant selection."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from select_variant import select_variant


def _theme_with(*variants):
    """Build a minimal theme dict with given variant IDs under a test role."""
    return {
        "roles": {
            "assertion-evidence": {
                "variants": [{"id": v} for v in variants]
            },
            "title": {"variants": [{"id": "title.centered"}, {"id": "title.image-left"}]},
            "closing": {"variants": [{"id": "closing.qa"}]},
        }
    }


def test_select_variant_title_first_slide_no_image():
    slide = {"slide_number": 1, "type": "title", "content_word_count": 5, "image": None}
    theme = _theme_with("ae.image-right")
    chosen, reason = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen == "title.centered"
    assert "first slide" in reason.lower() or "no image" in reason.lower()


def test_select_variant_title_with_image_prefers_image_left():
    slide = {"slide_number": 1, "type": "title", "content_word_count": 5, "image": "hero.png"}
    theme = _theme_with("ae.image-right")
    chosen, _ = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen == "title.image-left"


def test_select_variant_ae_short_text_with_image():
    slide = {
        "slide_number": 3, "type": "assertion-evidence",
        "content_word_count": 10, "image": "photo.png",
    }
    theme = _theme_with("ae.image-right", "ae.image-left", "ae.chart-center")
    chosen, _ = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen == "ae.image-right"


def test_select_variant_ae_chart_filename_prefers_chart_center():
    slide = {
        "slide_number": 3, "type": "assertion-evidence",
        "content_word_count": 10, "image": "incidence-chart.png",
    }
    theme = _theme_with("ae.image-right", "ae.chart-center")
    chosen, _ = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen == "ae.chart-center"


def test_select_variant_pacing_avoids_repeat():
    slide = {
        "slide_number": 4, "type": "assertion-evidence",
        "content_word_count": 10, "image": "photo.png",
    }
    theme = _theme_with("ae.image-right", "ae.image-left")
    chosen, _ = select_variant(slide, theme, previous_variant="ae.image-right", total_slides=10)
    assert chosen == "ae.image-left"  # pacing alternation


def test_select_variant_closing_last_slide():
    slide = {"slide_number": 10, "type": "closing", "content_word_count": 2, "image": None}
    theme = _theme_with("ae.image-right")
    chosen, _ = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen == "closing.qa"


def test_select_variant_unknown_role_uses_first_available():
    # Role not in theme → return None
    slide = {"slide_number": 2, "type": "nonexistent-role", "content_word_count": 5, "image": None}
    theme = _theme_with("ae.image-right")
    chosen, reason = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen is None
    assert "not defined" in reason.lower() or "no variants" in reason.lower()


def test_select_variant_fallback_first_variant_when_no_signal():
    slide = {"slide_number": 5, "type": "assertion-evidence", "content_word_count": 100, "image": None}
    theme = _theme_with("ae.image-right")
    chosen, _ = select_variant(slide, theme, previous_variant=None, total_slides=10)
    assert chosen == "ae.image-right"  # first variant as fallback
