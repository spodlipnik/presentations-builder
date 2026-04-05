#!/usr/bin/env python3
"""Cluster slides from a reference-catalog.yaml into variant groups.

Groups slides by geometric similarity (rounded box coordinates) to identify
recurring layout patterns. Each cluster represents one variant candidate
that the user will validate in talk-theme-builder Fase 2.

Usage:
    python3 cluster_slides.py --input catalog.yaml --output clusters.yaml [--bucket 0.05]
"""
import argparse
import yaml
from collections import Counter
from pathlib import Path


def _round_to_bucket(value, bucket):
    """Round value to nearest bucket increment."""
    return round(round(value / bucket) * bucket, 3)


def make_slide_signature(slide, bucket=0.05):
    """Create a tuple signature representing the slide's layout pattern.

    Shapes are sorted by position (y, then x) so slides with same layout
    but different z-order produce the same signature.
    """
    shape_tuples = []
    for shape in slide.get("shapes", []):
        box = shape.get("box", [0, 0, 0, 0])
        rounded = tuple(_round_to_bucket(v, bucket) for v in box)
        shape_tuples.append((shape.get("type", "other"), rounded))
    # Sort by (y, x) for position-independent signature
    shape_tuples.sort(key=lambda t: (t[1][1], t[1][0]))
    return tuple(shape_tuples)


def cluster_catalog(catalog, bucket=0.05):
    """Group slides by layout signature. Returns list of cluster dicts.

    Each cluster: {role, count, slide_numbers, representative_slide_number, signature}
    Role is the majority inferred_role across slides in the cluster.
    """
    slides = catalog.get("slides", [])
    if not slides:
        return []

    # Map signature → list of slides
    groups = {}
    for slide in slides:
        sig = make_slide_signature(slide, bucket=bucket)
        groups.setdefault(sig, []).append(slide)

    # Build cluster summaries
    clusters = []
    for sig, slide_list in groups.items():
        # Majority-vote on role (handles mixed inferred_role)
        role_counter = Counter(s.get("inferred_role") or "unknown" for s in slide_list)
        majority_role, _ = role_counter.most_common(1)[0]
        clusters.append({
            "role": majority_role,
            "count": len(slide_list),
            "slide_numbers": [s["slide_number"] for s in slide_list],
            "representative_slide_number": slide_list[0]["slide_number"],
            "signature": [{"type": t, "box": list(box)} for t, box in sig],
        })
    # Sort by count descending, then by first slide number
    clusters.sort(key=lambda c: (-c["count"], c["representative_slide_number"]))
    return clusters


def main():
    parser = argparse.ArgumentParser(description="Cluster reference catalog slides into variant groups.")
    parser.add_argument("--input", "-i", required=True, help="Input catalog.yaml (from extract_references.py)")
    parser.add_argument("--output", "-o", required=True, help="Output clusters.yaml")
    parser.add_argument("--bucket", type=float, default=0.05, help="Rounding bucket for positions (default 0.05)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        catalog = yaml.safe_load(f)

    clusters = cluster_catalog(catalog, bucket=args.bucket)
    output = {
        "source_catalog": Path(args.input).name,
        "bucket": args.bucket,
        "clusters_count": len(clusters),
        "clusters": clusters,
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        yaml.safe_dump(output, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    print(f"Clustered {sum(c['count'] for c in clusters)} slides into {len(clusters)} variants → {args.output}")


if __name__ == "__main__":
    main()
