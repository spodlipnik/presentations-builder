# Talk Builder

A Claude Code plugin for building academic and medical presentations with structured storytelling — from research to final PPTX and speaker scripts.

## Features

- **9-skill orchestrated workflow**: briefing, vision, research, assets, narrative, slides, study documents, speaker script
- **Evidence-based research**: PubMed and Consensus integration with DOI/PMID verification
- **Storytelling frameworks**: ABT, Sparkline, STAR moments, assertion-evidence design
- **Personal style config**: `design_tokens` (color palette + fonts) applied consistently across all generated visuals
- **PPTX generation**: delegates to the official `document-skills:pptx` skill — inherits design improvements automatically
- **Study documents**: comprehensive review-article-style reference and per-paper summaries
- **Speaker scripts**: preparation table + teleprompter format

## Requirements

- **Claude Code** (latest version)
- **poppler** — PDF image extraction: `brew install poppler`
- **`document-skills:pptx` skill** — official Anthropic skill for PPTX generation. Install: `/plugin install document-skills` from `claude-plugins-official` marketplace.
- **Recommended**: PubMed and Consensus MCP servers (claude.ai > Settings > MCP Servers) for `talk-research`

## Installation

Install from the marketplace:

```
/plugin install talk-builder
```

Or load locally for development:

```bash
claude --plugin-dir ./presentations-builder
```

## Quick Start

1. Run `/talk-builder:talk-setup` to configure your personal style
2. Create a new directory for your presentation: `mkdir my-talk && cd my-talk`
3. Run `/talk-builder:talk` to start the guided workflow

## Skills

| Skill | Purpose |
|---|---|
| `/talk` | Main orchestrator — detects phase and guides workflow |
| `/talk-setup` | One-time setup of `config.yaml` (language, complexity, design_tokens) |
| `/talk-briefing` | Collect topic, duration, audience, preferences |
| `/talk-vision` | Define personal angle, message, emotional intent |
| `/talk-research` | Search PubMed/Consensus, read PDFs, build evidence base |
| `/talk-assets` | Extract figures from PDFs, generate SVG charts/diagrams, propose AI prompts |
| `/talk-narrative` | Build slide structure (12 canonical types) with storytelling arc |
| `/talk-slides` | Generate `presentation.pptx` by delegating to `document-skills:pptx` |
| `/talk-study-doc` | Create comprehensive study document with active recall |
| `/talk-script` | Generate teleprompter-format speaker script (optional) |

## How It Works

Each presentation is a directory. Talk Builder detects your progress by checking which files exist:

| File | Phase |
|---|---|
| `docs/talk.yaml` | Briefing complete |
| `docs/vision.md` | Vision defined |
| `docs/research.md` | Research complete |
| `docs/narrative.md` | Narrative approved |
| `images/` (non-empty) | Assets ready |
| `docs/study-document.md` | Study docs complete |
| `docs/speaker-script.md` | Script ready |
| `presentation.pptx` | Slides generated |

The project root stays clean — only `presentation.pptx` lives there. All working documents are in `docs/`, images in `images/`, and research papers in `pdfs/`.

Run `/talk` at any point to see your status and continue from where you left off.

## Configuration

Personal style — language, narrative preferences, and `design_tokens` (color palette + fonts) — is stored in a `config.yaml` at a path you choose during setup. Per-project overrides go in `docs/talk.yaml`.

`design_tokens` are passed to `document-skills:pptx` at every PPTX generation, so all your decks share the same visual identity.

See `config.example.yaml` for all available options.

## License

MIT — see [LICENSE](LICENSE)
