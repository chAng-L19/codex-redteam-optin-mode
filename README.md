# Codex Red Team Opt-In Mode v1.0

> Professional offensive routing — only when you explicitly turn it on.

A lightweight Codex profile that keeps the assistant in **normal mode by default**, and only switches into **red-team doctrine** when you deliberately enable it.

## Features

- opt-in only red-team mode
- session-safe reset to normal mode
- lightweight hooks to avoid context bloat
- compact doctrine skill
- Burp-first preference for Burp-native evidence

## Enable red-team mode

```text
进入红队模式
开启红队模式
/redteam on
enable red team mode
```

## Disable red-team mode

```text
退出红队模式
关闭红队模式
/redteam off
disable red team mode
```

## Repository layout

```text
.codex/
  AGENTS.md
  hooks/
    session-start-context.py
    hook-security-context-hook.py
.agents/
  skills/
    red-team-command-doctrine/
      SKILL.md
templates/
  hooks.json.template
  config.toml.example
scripts/
  install.ps1
docs/
  BEHAVIOR.md
```

## Installation

### Manual
Copy these into your Codex home:
- `.codex/AGENTS.md`
- `.codex/hooks/session-start-context.py`
- `.codex/hooks/hook-security-context-hook.py`
- `.agents/skills/red-team-command-doctrine/SKILL.md`

Then render `templates/hooks.json.template` into your real `hooks.json`.

### PowerShell installer

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

## Design goal

This version is intentionally minimal:
- normal mode is the default
- red-team mode is explicit only
- hook output stays compact
- no heavy doctrine injection

## Notes

- `config.toml.example` is a reference, not a full drop-in replacement
- Chinese enable/disable commands are supported
