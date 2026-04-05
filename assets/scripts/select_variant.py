#!/usr/bin/env python3
"""Rubric-based variant selection for talk-slides.

Given a slide + theme + previous slide's variant, picks the best variant ID
from the theme's variants for that slide's role.
"""


_CHART_KEYWORDS = ("chart", "plot", "graph", "fig", "grafico", "grafica")


def select_variant(slide, theme, previous_variant=None, total_slides=None):
    """Select the best variant for a slide. Returns (variant_id, reason_text).

    Rules are evaluated in priority order. Pacing (no immediate repeats) is
    applied last. Returns (None, reason) if the role has no variants.
    """
    role = slide.get("type", "")
    roles = theme.get("roles", {})
    role_def = roles.get(role)

    if not role_def or not role_def.get("variants"):
        return (None, f"role {role!r} not defined in theme or has no variants")

    available_ids = [v["id"] for v in role_def["variants"]]

    # Rule dispatcher by role
    chosen = None
    reason = ""

    if role == "title":
        chosen, reason = _select_title(slide, available_ids)
    elif role == "assertion-evidence":
        chosen, reason = _select_assertion_evidence(slide, available_ids)
    elif role == "closing":
        chosen, reason = _pick_preferred(available_ids, ["closing.qa", "closing.thanks"]) or (None, "")
        reason = reason or "default closing choice"
    elif role == "comparison":
        chosen, reason = _select_comparison(slide, available_ids)
    elif role == "data-chart":
        chosen, reason = _select_chart(slide, available_ids)
    elif role == "image-gallery":
        chosen, reason = _select_gallery(slide, available_ids)

    # Fallback to first available variant if no rule matched
    if not chosen:
        chosen = available_ids[0]
        reason = reason or f"fallback: first available variant for role {role!r}"

    # Apply pacing rule: avoid same variant as previous
    if previous_variant and chosen == previous_variant and len(available_ids) > 1:
        alternatives = [v for v in available_ids if v != previous_variant]
        if alternatives:
            chosen = alternatives[0]
            reason = f"{reason} (pacing: avoided repeat of {previous_variant})"

    return (chosen, reason)


def _pick_preferred(available, preferences):
    """Return first preference that exists in available list, as (chosen, reason)."""
    for pref in preferences:
        if pref in available:
            return (pref, f"preferred variant {pref!r}")
    return None


def _select_title(slide, available):
    slide_num = slide.get("slide_number", 0)
    has_image = bool(slide.get("image"))
    if slide_num == 1:
        if has_image:
            result = _pick_preferred(available, ["title.image-left", "title.fullbleed-overlay", "title.centered"])
            if result:
                return (result[0], f"first slide with image → {result[0]}")
        else:
            result = _pick_preferred(available, ["title.centered", "title.image-left"])
            if result:
                return (result[0], "first slide without image → centered")
    return (None, "")


def _select_assertion_evidence(slide, available):
    content_words = slide.get("content_word_count", 0)
    image = slide.get("image") or ""
    image_lower = image.lower()
    has_chart = any(k in image_lower for k in _CHART_KEYWORDS)
    has_image = bool(image)

    if has_chart:
        result = _pick_preferred(available, ["ae.chart-center"])
        if result:
            return (result[0], f"image filename suggests chart → {result[0]}")

    if has_image and content_words < 30:
        result = _pick_preferred(available, ["ae.image-right", "ae.image-left"])
        if result:
            return (result[0], f"image + short text ({content_words} words) → {result[0]}")

    if has_image and 30 <= content_words <= 50:
        result = _pick_preferred(available, ["ae.diagram-fullwidth", "ae.image-right"])
        if result:
            return (result[0], f"image + medium text ({content_words} words) → {result[0]}")

    return (None, "")


def _select_comparison(slide, available):
    has_image = bool(slide.get("image"))
    if has_image:
        result = _pick_preferred(available, ["compare.two-col-image"])
        if result:
            return (result[0], "has image → two-col-image")
    return _pick_preferred(available, ["compare.two-col-text"]) or (None, "")


def _select_chart(slide, available):
    # Heuristic: by word count or number of "chart" mentions in content
    content = (slide.get("content") or "").lower()
    chart_count = sum(content.count(k) for k in _CHART_KEYWORDS)
    if chart_count >= 2:
        result = _pick_preferred(available, ["chart.dual-compare"])
        if result:
            return (result[0], "content mentions multiple charts")
    return _pick_preferred(available, ["chart.single-key", "chart.callout-stat"]) or (None, "")


def _select_gallery(slide, available):
    # Count image references in content + image field
    content = slide.get("content") or ""
    image_count = content.lower().count(".png") + content.lower().count(".jpg")
    if slide.get("image"):
        image_count += 1

    if image_count <= 2:
        result = _pick_preferred(available, ["gallery.2-vertical", "gallery.comparative-pair"])
        if result:
            return (result[0], f"2 images → {result[0]}")
    elif image_count <= 4:
        result = _pick_preferred(available, ["gallery.2x2-grid"])
        if result:
            return (result[0], f"4 images → {result[0]}")
    else:
        result = _pick_preferred(available, ["gallery.3x2-grid"])
        if result:
            return (result[0], f"5+ images → {result[0]}")
    return (None, "")
