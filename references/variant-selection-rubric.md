# Variant Selection Rubric

Signal-based rules that `talk-slides` uses to automatically select the best variant for each slide based on narrative.md content. The rubric is deterministic and testable; LLM quality check runs at the end as verification, not as primary selector.

## How Selection Works

For each slide in `narrative.md`:

1. **Check for user override**: If `Variant:` field exists without `# auto` marker → respect user's choice, skip rubric.
2. **If `Variant:` absent or marked `# auto`**: Apply signal-based rubric below.
3. **Apply pacing rule**: If selected variant matches previous slide's variant, look for alternative in same role.
4. **Write decision back** to narrative.md with `# auto` marker.
5. **Log reasoning** in `docs/layout-decisions.md`.

## Content Signals per Role

### title
| Signal | Variant |
|---|---|
| Slide is #1 AND has image reference | `title.image-left` |
| Slide is #1 AND no image | `title.centered` |
| Slide is #1 AND "dramatic"/"impact" in context | `title.fullbleed-overlay` |

### disclosure
| Signal | Variant |
|---|---|
| Content is short list (≤5 items) | `disclosure.minimal` |
| Content is tabular (has columns like Role/Company) | `disclosure.table` |

### agenda
| Signal | Variant |
|---|---|
| Content has numbered list | `agenda.numbered` |
| Content has 4-8 items with icon mentions | `agenda.icons-grid` |

### section-divider
| Signal | Variant |
|---|---|
| Default | `divider.number-large` |
| Alternating (every other divider) | `divider.fullbleed-quote` |

### assertion-evidence (most common)
| Signal | Variant |
|---|---|
| Has image + text <30 words + image filename contains chart/plot/graph/fig | `ae.chart-center` |
| Has image + text <30 words | `ae.image-right` (alternates with `ae.image-left`) |
| Has image + text 30-50 words + image has diagram/flow | `ae.diagram-fullwidth` |
| Has image + text >50 words | `ae.image-right` (text dominates) |

### patient-case
| Signal | Variant |
|---|---|
| Has photo + history text | `case.photo-left` |
| Has timeline/evolution | `case.timeline-right` |
| Has 2 images (before/after keywords) | `case.before-after` |

### methodology
| Signal | Variant |
|---|---|
| Content mentions "flowchart"/"CONSORT"/"flow" | `method.flowchart` |
| Content is sequential (step 1, step 2...) | `method.steps-horizontal` |

### data-chart
| Signal | Variant |
|---|---|
| 1 chart/image referenced | `chart.single-key` |
| 2 charts/images referenced | `chart.dual-compare` |
| Content emphasizes single statistic (%, number + unit) | `chart.callout-stat` |

### data-table
| Signal | Variant |
|---|---|
| Default | `table.clean` |
| Content mentions "highlight"/"key row" | `table.highlighted-row` |

### comparison
| Signal | Variant |
|---|---|
| Has 2 images | `compare.two-col-image` |
| Text only ("vs"/"versus"/"compared") | `compare.two-col-text` |

### quote-pullout
| Signal | Variant |
|---|---|
| Has attribution image (author photo) | `quote.with-attribution-image` |
| Text-only quote | `quote.centered-large` |

### image-fullbleed
| Signal | Variant |
|---|---|
| Has caption text | `full.caption-bottom` |
| Short caption + dramatic image | `full.caption-overlay` |

### image-gallery
| Signal | Variant |
|---|---|
| 2 images, "comparison"/"vs" | `gallery.comparative-pair` |
| 2 images, no comparison signal | `gallery.2-vertical` |
| 4 images | `gallery.2x2-grid` |
| 5-6 images | `gallery.3x2-grid` |

### timeline-process
| Signal | Variant |
|---|---|
| 3-5 events | `timeline.horizontal` |
| 6+ events | `timeline.vertical` |

### key-takeaway
| Signal | Variant |
|---|---|
| Single sentence | `takeaway.large-statement` |
| 2-4 bullets | `takeaway.3-bullets-visual` |

### poll-question
| Signal | Variant |
|---|---|
| Single question, no options | `poll.single-question` |
| Has answer choices (A, B, C, D) | `poll.multiple-choice` |

### contact
| Signal | Variant |
|---|---|
| Has photo | `contact.card-centered` |
| Text-only minimal | `contact.minimal-horizontal` |

### closing
| Signal | Variant |
|---|---|
| Last slide, "questions"/"Q&A" | `closing.qa` |
| Last slide, "gracias"/"thanks" | `closing.thanks` |

## Pacing Rules

1. **Max consecutive same variant**: 1 (no immediate repetition)
2. **Alternation for AE**: if last AE was `ae.image-right`, next prefers `ae.image-left`
3. **Visual rhythm**: insert `image-fullbleed` every 5 content slides if not already present (creative breathing room)
4. **STAR moments**: if slide has `Emphasis: high` in narrative, prefer higher-impact variants

## Creativity Budget

The rubric allows controlled deviation when justified:
- Auto-inserted `image-fullbleed` breaks for pacing (logged with reason)
- High-emphasis slides may use variants normally reserved for openings
- All deviations documented in `docs/layout-decisions.md`

## Fallback Behavior

If no signal matches for a role:
- Use the **first variant listed** in the role's theme definition as default
- Log the decision as "fallback, no signal matched"
