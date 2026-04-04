# Changelog

All notable changes to Talk Builder will be documented in this file.

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
