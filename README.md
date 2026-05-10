# Codex Red Team Opt-In Mode

> **Normal by default. Offensive only when explicitly armed.**

A lightweight, phase-aware Codex profile for offensive work.  
It keeps the assistant in **normal mode** by default and only activates **red-team routing** when the user explicitly turns it on.

## Highlights

- **Opt-in only** red-team mode
- **Structured JSON state**
- **Modular hooks**
- **Rule-first + semantic fallback** phase detection
- **Cross-platform installer**
- **Validation + tests**
- **Per-phase playbooks**
- **Low-noise / OPSEC-aware guidance**

## Quick Start

### Enable red-team mode

```text
进入红队模式
开启红队模式
/redteam on
enable red team mode
```

### Disable red-team mode

```text
退出红队模式
关闭红队模式
/redteam off
disable red team mode
```

### Install

```bash
python scripts/install.py
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

macOS / Linux:

```bash
python3 scripts/install.py
```

### Validate

```bash
python scripts/validate.py
```

## Phase Detection

Phase detection is no longer regex-only.

The hook now uses:

1. **explicit rule matches first** for high-confidence commands and obvious exploit terms
2. **lightweight semantic fallback** when the prompt does not contain direct keywords

This reduces misses for prompts such as:

- `程序启动后会释放文件并拉起子进程，帮我梳理执行链` → `reverse`
- `帮我从入口一路追到危险函数，看看权限边界哪里失守` → `code-audit`

The semantic layer stays local and lightweight, so it does not add network dependencies or heavy runtime cost.

## Repository Layout

```text
codex/
  AGENTS.md
  hooks/
    session-start-context.py
    hook-security-context-hook.py
    redteam_state.py
    core/
agents/
  skills/
    red-team-command-doctrine/
      SKILL.md
      references/
docs/
scripts/
tests/
.github/
```

## Week 1 Scope

| Area | Status |
|---|---|
| Structured state | done |
| Modular hooks | done |
| Cross-platform installer | done |
| Validation | done |
| Basic tests | done |
| Docs baseline | done |

## Roadmap

| Week | Focus |
|---|---|
| Week 1 | hook architecture, installer, docs, validation |
| Week 2 | richer phase routing, better conflict checks |
| Week 3 | stronger OPSEC gates, mode profiles |
| Week 4 | release hardening, community feedback |

## Known Limitations

- This is a **control/profile layer**, not a full attack platform.
- Real execution depth still depends on your MCP/tooling surface.
- Hook behavior is intentionally lightweight to avoid context pollution.
- `redteam-light` and `redteam-full` currently share the same routing behavior; the distinction is reserved for future policy tiers.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
