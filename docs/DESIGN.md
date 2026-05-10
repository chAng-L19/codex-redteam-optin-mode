# Design

## Goals

- opt-in red-team behavior only
- lightweight hooks with minimal context injection
- phase-aware routing instead of heavy global doctrine
- safe rollback and verifiable installs

## Design Principles

1. **Normal by default**
   - ordinary coding and research should stay ordinary
2. **Small hooks**
   - avoid giant prompt injections that pollute context
3. **Rule-first, semantic fallback**
   - explicit triggers win; semantic routing only fills the gaps
4. **Session isolation**
   - one session should not silently overwrite another session's mode
