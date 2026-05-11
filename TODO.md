# TODO — Talk Builder

Open items not addressed in the current release. Tracked here so they don't get lost between sessions.

## Slide layout polish (pending from v2.1 layout eval)

These were identified in the v2.1 layout eval (see `eval-log.md` in the user's eval workspace) but deferred to keep v2.1 scoped.

### L4 — Divider rhythm inconsistent across slides

**Symptom**: `divider` slides with single-line titles render at ~54pt; titles that wrap to two lines render at ~48pt and visually take a different proportion of the slide. Same template, different visual rhythm.

**Fix candidates**:
- Auto-fit: clamp font size based on character count of `section_title`.
- Force the writer to keep section titles short (≤ 40 chars), reject longer in validator.
- Render the title in a fixed-height box with auto-shrink.

**Lives in**: `skills/talk-slides/SKILL.md` (divider rendering rule) and possibly `tools/validate_narrative.py` (length limit).

### L6 — Title slide is austere / upper third empty

**Symptom**: Slide 1 (`title` type) has the title block anchored to vertical-center, leaving the top ~30% of the slide as pure whitespace. Functional but doesn't feel "designed."

**Fix candidates**:
- Anchor title block to upper-third instead of vertical-center.
- Add an optional `motif` zone (a thin accent rule, a small image strip, or a geometric mark) — could be tied to X1 below.
- Allow an optional `cover_image` field for `title` (atmospheric image as background or left strip).

**Lives in**: `skills/talk-slides/SKILL.md` (title rendering rule); possibly `canonical-types.md` (new optional field).

### X1 — No visual motif repeats across slides

**Symptom**: Each slide is its own visual island. The `document-skills:pptx` skill explicitly recommends "pick ONE distinctive element and repeat it" — we currently have nothing. This is part of why generated decks read as "generic AI."

**Fix candidates**:
- Subtle page-number indicator (e.g., bottom-right in accent at 60% opacity).
- A thin accent rule at the top or bottom of every slide (NOT under the title — that's the AI-aesthetic anti-pattern).
- A small section marker on content slides (e.g., "PROBLEM ·" in accent, top-left, when inside a section bounded by dividers).

**Lives in**: `skills/talk-slides/SKILL.md` (cross-cutting rule, applies to every type except `fullbleed`).

### B4 — Quote glyph renders as parallel slashes in LibreOffice

**Symptom**: The Unicode opening double quote (`U+201C`) on the `quote` type renders correctly at small sizes but appears as parallel slashes at ~200pt in LibreOffice's render. Likely a LibreOffice + Avenir Next font fallback issue.

**Verify first**: open the PPTX directly in Keynote. If the glyph renders correctly there, no fix is needed (Keynote is the user's actual delivery target).

**Fallback fix if Keynote also breaks**: render the quote-mark as a styled image (small SVG → PNG via cairosvg) instead of relying on the Unicode glyph.

**Lives in**: `skills/talk-slides/SKILL.md` (quote rendering rule), possibly `assets/scripts/` (helper to render the glyph image).

## Schema upgrades (deferred)

### Structured `comparison.rows` instead of free-form content strings

**Today**: `comparison` schema uses `left_content` / `right_content` as newline-separated strings. `talk-slides` heuristically splits on newlines to render rows with deltas. Brittle — relies on the writer formatting content with `Label: Value` pairs.

**Proposal**:

```yaml
comparison:
  required: [headline, rows]
  rows: list of
    - { label: str, left_value: str, right_value: str, delta: str?, winner: 'left'|'right'|'tie' }
```

**Tradeoff**: more structured, supports proper winner emphasis; breaks v2.0 `comparison` slides. Needs a migration path.

**Lives in**: `.claude/rules/canonical-types.md`, `skills/talk-narrative/SKILL.md`, `skills/talk-slides/SKILL.md`, `tools/validate_narrative.py`, `CHANGELOG.md` entry. Major change → v2.2 or v3.

## Architecture (someday)

### X4 — Brief format with codified coordinates

**Today**: `talk-slides` Phase 3 builds a prose brief like "image right ~40% width (contained)." Claude derives the actual coordinates each run. Most layout drift comes from this derivation step.

**Alternative**: have `talk-slides` emit a STRUCTURED brief (JSON or YAML) with exact coordinates per slide computed from the narrative + design tokens. The pptx skill then renders mechanically from the structured brief.

**Tradeoff**: more deterministic output; loses some of the LLM's ability to adapt to edge cases (long headlines, unusual aspect ratios). Worth doing if drift remains a problem after v2.1.

**Lives in**: `skills/talk-slides/SKILL.md` Phase 3, possibly a new `references/slide-coords.md`.
