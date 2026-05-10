# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-05-07
### Added
- structured JSON state
- modular hooks core
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
