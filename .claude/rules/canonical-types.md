---
description: 12 canonical slide types — the contract between talk-narrative and talk-slides
paths:
  - "skills/talk-narrative/**"
  - "skills/talk-slides/**"
---

# Canonical 12 slide types

The contract between `talk-narrative` (writer) and `talk-slides` (reader) is the 12-type schema. Adding or renaming a type means updating BOTH SKILL.md files (and the CHANGELOG migration table).

## The 12 types

`title`, `text-list`, `divider`, `assertion-evidence`, `assertion-evidence-left`, `chart`, `callout`, `quote`, `comparison`, `gallery`, `fullbleed`, `closing`.

## Field schema by type

| `type` | Required | Optional |
|---|---|---|
| `title` | `title`, `author`, `affiliation` | `subtitle`, `date` |
| `text-list` | `title`, `items` (list) | — |
| `divider` | `section_label`, `section_title` | `teaser` |
| `assertion-evidence` | `headline`, `image` | `caption` |
| `assertion-evidence-left` | `headline`, `image` | `caption` |
| `chart` | `headline`, `chart_image` | `caption` |
| `callout` | `big_text`, `sub_label` | — |
| `quote` | `quote_text`, `attribution` | — |
| `comparison` | `headline`, `left_label`, `left_content`, `right_label`, `right_content` | — |
| `gallery` | `headline`, `image_1`, `image_2`, `image_3`, `image_4` | `caption` |
| `fullbleed` | `image_full` | `overlay_text` |
| `closing` | `main_text`, `contact_info` | — |

## Speaker-facing fields (NOT used by talk-slides)

`speaker`, `context`, `bridge`, `ref`, `section`, `type_line`. These exist in `narrative.md` for the speaker's preparation. `talk-slides` reads them but never includes them in the deck. Don't compress slide-visible content into them, and don't expect them to render.

## Legacy v1 types — REJECT

Any value outside the 12 above is legacy from v1's 18-role taxonomy. `talk-slides` aborts with a CHANGELOG-pointer message rather than silently translating, because borderline cases (e.g., `data-table` → `comparison` vs `chart`) require user intent.
