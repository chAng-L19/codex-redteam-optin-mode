# Codex Red-Team Compatibility Layer

<!-- version: 0.3.1 -->
<!-- last-updated: 2026-05-13 -->

This repository now treats `E:\cli\codex-redteam-optin-mode\instruction.ctf.md` as the **canonical model instructions file**.

This `AGENTS.md` remains as a compatibility layer for installs or environments that still read AGENTS-based guidance.

## Compatibility rules

- default mode is `normal`
- red-team mode is opt-in only
- when red-team mode is enabled, route by `phase -> method -> router -> leaf`
- keep hooks lightweight
- keep context compact

## Explicit enable triggers

- `进入红队模式`
- `开启红队模式`
- `/redteam on`
- `/redteam light`
- `/redteam full`
- `enable red team mode`

## Explicit disable triggers

- `退出红队模式`
- `关闭红队模式`
- `/redteam off`
- `disable red team mode`

## Tool preferences

- Burp-native evidence -> `burp-ai-agent`
- Live browsing -> `web-access`
- History -> `mem-search` / `timeline-report` only when needed

## Doctrine routing

When red-team mode is enabled and the user has not named a more specific offensive skill:

1. invoke `red-team-command-doctrine`
2. route by `phase -> method -> router -> leaf`
3. keep the emitted context compact
