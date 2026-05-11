# Changelog

All notable changes to Talk Builder will be documented in this file.

## [2.1.0] - 2026-05-11

### Added

- **Optional `stat` and `stat_label` fields on `assertion-evidence` / `assertion-evidence-left`** — when both are present, `talk-slides` renders a big-number callout on the side opposite the image, in accent color. This gives evidence slides a visual anchor without doubling the headline text. Fully backward-compatible: slides without these fields render the simpler headline+image layout. Documented in `.claude/rules/canonical-types.md` and `skills/talk-narrative/SKILL.md`.
- **`talk-slides` field-rendering rules now codify layout coordinates** for every type — fixed image sizes (assertion-evidence: 6.0"×4.0"; uniform 3:2 pre-crop), grid math (gallery: 4:3 pre-cropped uniform cells), row computation (text-list per-item addText pairs with hanging indent), and winner emphasis (comparison panel + bold + delta indicators). Coordinates are inline in `skills/talk-slides/SKILL.md` Phase 3.
- **Pre-crop step**: `talk-slides` instructs Claude to pre-crop assertion-evidence (3:2) and gallery (4:3) images via Pillow center-crop into `images/cropped/` before placing them. The venv already ships Pillow.
- **New gotchas in `skills/talk-slides/SKILL.md`** documenting failure modes discovered during the v2.1 layout eval:
  - pptxgenjs `bullet: { type: 'number' }` does not auto-increment reliably — bake numbers manually
  - text-list rich-text arrays lose hanging indent on wrap — render each row as two separate `addText` calls
  - Pre-cropping is the only path to a clean `gallery`; `sizing: cover/contain` is broken
  - `gallery` caption Y must be computed from grid bottom, not slide bottom

### Changed

- **`comparison` rendering** — always differentiates the winner via three layers (panel + value weight + delta indicator). Previously rendered both columns identically. Non-breaking; existing `comparison` slides will simply look better.
- **`text-list` vertical anchoring** — block now anchors to the upper third instead of leaving 1.5" of dead space between title and items. Numbered items use accent color for the number glyph, which also brings accent presence to more slides.
- **`assertion-evidence` empty-side handling** — the side opposite the image is no longer accidental whitespace; it's either a `stat` callout (if narrative provides one) or intentional breathing room. The image is now a fixed 6.0"×4.0" rectangle for visual consistency across slides.

### Notes

- No schema migration needed. Existing `narrative.md` files continue to validate. The optional fields and rendering improvements are opt-in (for `stat`) or automatic-on-regenerate (for layout).
- For the most consistent look, regenerate decks with `/talk-builder:talk-slides` after upgrading to v2.1.

## [2.0.0] - 2026-05-09

### Removed (BREAKING)

- **`talk-theme-builder` skill** — entirely deleted. The 5-phase wizard for building `theme.yaml` is gone.
- **`theme.yaml` system** — no more themes/ directories per-user, no more roles × variants catalog.
- **18 canonical slide roles + 43 variants** — replaced by 12 simple `type` values in `narrative.md`.
- **`Variant: ... # auto` syntax** in `narrative.md` — removed (no rubric anymore).
- **Helper scripts**: `extract_references.py`, `cluster_slides.py`, `select_variant.py`, `update_narrative.py`, `load_theme.py`, `parse_narrative.py`, `smart_crop.py`, `generate_presentation_template.js`, `render_thumbnails.sh`, `backup_theme.sh`, and their tests.
- **Reference docs**: `role-taxonomy.md`, `theme-yaml-schema.md`, `variant-selection-rubric.md`.
- **Node.js dependency** — `assets/package.json` and the `npm install` SessionStart hook are gone. Talk Builder no longer ships any Node code.
- **`sharp` (Node)** for SVG → PNG in `talk-assets` — replaced by `cairosvg` (Python).
- **`theme:` field** in `docs/talk.yaml` — `talk-briefing` no longer asks for it; `talk-slides` ignores it if present.
- **`default_theme:` and `style_analysis:`** in `config.yaml` — removed from `talk-setup` output.

### Added

- **Delegation to `document-skills:pptx`** — `talk-slides` now invokes the official Anthropic PPTX skill via the `Skill` tool. Inherits design improvements and visual QA loop automatically.
- **`design_tokens` in `config.yaml`** — single source of truth for colors and fonts. Used by `talk-assets` (SVG generation) and `talk-slides` (PPTX brief).
- **`cairosvg`** in `requirements.txt` — Python-only SVG → PNG.

### Changed

- **`talk-slides`**: 6-phase 430-line skill → 4-phase ~150-line orchestrator. No more Migrate / Select Variants / Quality Check phases (those were rubric-driven).
- **`talk-narrative`**: dropped the dual type system (7 narrative types vs 18 canonical roles), now uses 12 typed types with field schemas.
- **`talk-assets`**: reads `design_tokens` from `config.yaml`; uses `cairosvg` instead of `sharp`.
- **`talk-setup`**: collects `design_tokens` interactively (5 colors + 2 fonts). No longer creates `themes/` directory.
- **`talk-briefing`**: dropped step 7 (theme question).
- **Skill count: 10 → 9** (talk-theme-builder removed).
- **Plugin requirements**: `document-skills:pptx` skill is now a hard dependency. Node.js is no longer required.

### Migration — legacy → new type mapping

Users with existing `narrative.md` files using the old 18-role system can migrate manually using this table:

| Old `Type:` value | New `type:` value |
|---|---|
| `title` | `title` |
| `disclosure` | `text-list` |
| `agenda` | `text-list` |
| `section-divider` | `divider` |
| `assertion-evidence` | `assertion-evidence` (or `assertion-evidence-left`) |
| `patient-case` | `assertion-evidence` (with patient photo as image) |
| `methodology` | `chart` (flowchart) or `assertion-evidence` (diagram) |
| `data-chart` | `chart` |
| `data-table` | `comparison` (if A vs B columns) or `chart` (table as image) |
| `comparison` | `comparison` |
| `quote-pullout` | `quote` |
| `image-fullbleed` | `fullbleed` |
| `image-gallery` | `gallery` |
| `timeline-process` | `chart` (timeline as image) |
| `key-takeaway` | `callout` |
| `poll-question` | `text-list` or `callout` |
| `contact` | `closing` |
| `closing` | `closing` |

Also delete any `Variant: ...` and `# auto` lines.

The generic `Content:` field is replaced by typed fields per type. See the schema table in `skills/talk-narrative/SKILL.md` for required fields per type.

`talk-slides` v2.0 will refuse to process narratives using the legacy types and will print a helpful error pointing back to this table.

---

## [1.0.0] - 2026-04-04

### Added
- Initial marketplace release
- 10 skills: orchestrator + setup + 8 workflow phases
- Reference guides: storytelling, slide design, pacing, data storytelling
- SessionStart hook for system dependency validation
- Persistent PptxGenJS dependencies via `CLAUDE_PLUGIN_DATA`
- MCP tool availability check with fallback to WebSearch
- README, LICENSE, and CHANGELOG

### Fixed
- Plugin manifest moved to `.claude-plugin/plugin.json` (correct location)
- All reference paths use `${CLAUDE_PLUGIN_ROOT}` for marketplace compatibility
- Sub-skills no longer auto-invoked by Claude (only orchestrator is)
