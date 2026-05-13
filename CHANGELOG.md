# Changelog

All notable changes to this project will be documented in this file.

## [0.3.1] - 2026-05-13

### Added
- added managed overwrite install support with `redteam-install-manifest.json`
- added install regression test to ensure stale managed paths are removed on reinstall

### Changed
- installer now preserves user `AGENTS.md` and `hooks.json` and injects managed config additively
- installer now directly removes previously managed runtime paths before writing the new version
- uninstall now prefers manifest-driven cleanup instead of best-effort static path removal
- validator now checks install manifest presence and shape
- README / README_ZH now document managed additive install behavior

## [0.2.0] - 2026-05-07
### Added
- structured JSON state
- modular hooks core
- structured offensive task orchestration skeleton (`codex/orchestrator`)
- Python installer and shell wrapper
- validation script and unit tests
- reverse-engineering and code-audit phases
- docs baseline and GitHub workflow

### Changed
- phase detection now uses rule-first matching with a lightweight semantic fallback instead of regex-only routing
- README documents the semantic fallback behavior and examples
- installer now renders cross-platform hook commands and validates via subprocess
- runtime mode state is now isolated per session instead of one global file
- docs were cleaned up for release readability and rollback clarity
## [0.3.0] - 2026-05-11

### Added
- introduced a layered red-team routing model: `phase -> method -> router -> leaf`
- added `codex/router/` with method, router, leaf, and adapter modules
- added `evasion` as a first-class offensive domain
- added docs for method and routing layers
- added doctrine references for phase-to-method and phase-to-hackskills mappings
- added router-focused unit tests

### Changed
- upgraded runtime state from phase-only guidance to structured routing state
- differentiated `redteam-light` and `redteam-full` output behavior
- refreshed README / README_ZH / CONTRIBUTING with disclaimer and thanks sections
- extended installer and validator to deploy and verify the new router layer
