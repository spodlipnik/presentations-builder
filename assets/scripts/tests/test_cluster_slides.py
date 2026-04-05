"""Tests for cluster_slides.py — groups similar slides into variant patterns."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cluster_slides import make_slide_signature, cluster_catalog


def test_make_slide_signature_rounds_boxes_to_buckets():
    slide = {
        "slide_number": 1,
        "shapes": [
            {"type": "text_box", "box": [0.102, 0.298, 0.801, 0.311]},
        ],
    }
    sig = make_slide_signature(slide, bucket=0.05)
    # Boxes should round to nearest 0.05: 0.100, 0.300, 0.800, 0.300
    assert sig == (("text_box", (0.10, 0.30, 0.80, 0.30)),)


def test_make_slide_signature_sorts_shapes_by_position():
    # Two shapes in different z-orders should produce same signature
    # if sorted by position
    slide = {
        "slide_number": 1,
        "shapes": [
            {"type": "text_box", "box": [0.5, 0.5, 0.3, 0.1]},
            {"type": "text_box", "box": [0.1, 0.1, 0.3, 0.1]},
        ],
    }
    sig = make_slide_signature(slide, bucket=0.05)
    # Sorted by (y, x)
    assert sig[0][1][:2] == (0.10, 0.10)
    assert sig[1][1][:2] == (0.50, 0.50)


def test_cluster_catalog_groups_identical_signatures():
    catalog = {
        "slides": [
            {
                "slide_number": 1,
                "shapes": [{"type": "text_box", "box": [0.1, 0.1, 0.8, 0.2]}],
                "inferred_role": "title",
            },
            {
                "slide_number": 2,
                "shapes": [{"type": "text_box", "box": [0.1, 0.1, 0.8, 0.2]}],
                "inferred_role": "title",
            },
            {
                "slide_number": 3,
                "shapes": [
                    {"type": "text_box", "box": [0.05, 0.05, 0.9, 0.15]},
                    {"type": "image", "box": [0.1, 0.25, 0.8, 0.65]},
                ],
                "inferred_role": "assertion-evidence",
            },
        ],
    }
    clusters = cluster_catalog(catalog, bucket=0.05)
    # 2 clusters: one with slides 1,2 (same sig) and one with slide 3
    assert len(clusters) == 2
    # Each cluster should have slide_numbers, role, representative
    cluster_by_size = sorted(clusters, key=lambda c: -len(c["slide_numbers"]))
    assert cluster_by_size[0]["slide_numbers"] == [1, 2]
    assert cluster_by_size[0]["role"] == "title"
    assert cluster_by_size[0]["count"] == 2
    assert cluster_by_size[1]["slide_numbers"] == [3]
    assert cluster_by_size[1]["role"] == "assertion-evidence"


def test_cluster_catalog_handles_mixed_roles_with_majority():
    # If slides with same signature have different inferred roles, use majority
    catalog = {
        "slides": [
            {"slide_number": 1, "shapes": [{"type": "text_box", "box": [0.1, 0.1, 0.8, 0.2]}], "inferred_role": "title"},
            {"slide_number": 2, "shapes": [{"type": "text_box", "box": [0.1, 0.1, 0.8, 0.2]}], "inferred_role": "title"},
            {"slide_number": 3, "shapes": [{"type": "text_box", "box": [0.1, 0.1, 0.8, 0.2]}], "inferred_role": "quote-pullout"},
        ],
    }
    clusters = cluster_catalog(catalog, bucket=0.05)
    assert len(clusters) == 1
    assert clusters[0]["role"] == "title"  # majority
    assert clusters[0]["count"] == 3


def test_cluster_catalog_empty_slides_returns_empty():
    assert cluster_catalog({"slides": []}) == []
