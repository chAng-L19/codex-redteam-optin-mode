# Codex Red Team Opt-In Mode

English | [中文](./README_ZH.md)

> **Normal by default. Offensive only when explicitly armed.**

A lightweight, phase-aware red-team operating profile for Codex.

This project keeps Codex in **normal mode** by default and only enables **offensive routing** when you explicitly turn it on. It now adds:

- opt-in red-team mode
- lightweight hooks
- structured JSON mode state
- rule-first + semantic phase detection
- session-isolated mode state
- structured offensive task orchestration
- **phase → method → router → leaf** routing
- skill-pack style integration references for `qiushi-skill`, `hack-skills`, and `Anthropic-Cybersecurity-Skills`
- root-level `config.toml` + `instruction.ctf.md` profile layout

---

## Why this project

Most “always-on red-team prompts” fail in one of two ways:

1. they **pollute normal work**
2. they **blow up context** with heavy doctrine injection

This project takes the opposite approach:

- **normal mode stays normal**
- **red-team mode is explicit**
- **hooks stay small**
- **routing stays layered**

---

## Features

- **Opt-in only**
  - normal mode is the default
  - red-team mode only activates after explicit enable

- **Layered routing**
  - phase
  - method
  - router
  - leaf

- **Skill integration**
  - `qiushi-skill` → method layer
  - `hack-skills` → technical router layer
  - `Anthropic-Cybersecurity-Skills` → skill-pack structure and progressive disclosure references

- **Expanded offensive domains**
  - web
  - ad
  - postex
  - reverse
  - code-audit
  - payload
  - evasion

- **Rule-first + semantic fallback**
  - direct matches win first
  - lightweight semantic fallback catches natural-language prompts that do not match exact keywords

- **Session isolation**
  - one session does not overwrite another session’s mode state

- **Structured orchestration layer**
  - recon → strategy → exploit-dev → review → reporting
  - artifact schemas and gates
  - review-before-delivery workflow

- **Cross-platform install**
  - Windows / macOS / Linux

- **Validation and tests**
  - install validation
  - hook validation
  - router validation
  - orchestration gate validation
  - ordinary-mode cleanliness checks

---

## Install

The installer performs a **managed additive install**:

- preserves existing `AGENTS.md` and `hooks.json`
- merges this project's managed block into `AGENTS.md`
- merges this project's managed hooks into `hooks.json`
- directly removes previously managed runtime code paths from older installs
- installs the current runtime version cleanly
- writes a local install manifest for the next upgrade
- runs validation after install

### Python

```bash
python scripts/install.py
```

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

### macOS / Linux

```bash
python3 scripts/install.py
```

---

## Quick Start

### Enable red-team mode

```text
进入红队模式
开启红队模式
/redteam on
/redteam light
/redteam full
enable red team mode
```

### Disable red-team mode

```text
退出红队模式
关闭红队模式
/redteam off
disable red team mode
```

### Validate install

```bash
python scripts/validate.py
```

---

## How it works

### 1. Mode-gated behavior

The project starts in **normal** mode.

It does **not** inject offensive doctrine into ordinary work unless red-team mode is explicitly enabled.

### 2. Lightweight hooks

The runtime hooks are intentionally small:

- small session-start context
- no giant prompt injection
- no always-on offensive bias

### 3. Layered red-team routing

The runtime now emits a compact route envelope:

```text
[security:redteam]
[mode:redteam-light]
[phase:web]
[method:investigation-first]
[router:auth-sec]
[leaf:jwt-oauth-token-attacks]
```

### 4. Structured orchestration

For larger tasks, the project includes a lightweight orchestration layer:

```text
recon -> strategy -> exploit-dev -> review -> reporting
```

This layer is **not** always-on runtime automation.  
It is a structured planning and gating framework.

---

## Repository Layout

```text
.github/
config.toml
instruction.ctf.md
agents/
  skills/
    red-team-command-doctrine/
codex/
  AGENTS.md
  hooks/
  router/
  orchestrator/
docs/
scripts/
templates/
tests/
```

The canonical prompt now lives in:

- `./instruction.ctf.md`

and the repository root `config.toml` points to it with:

```toml
# Codex red-team profile
model_instructions_file = './instruction.ctf.md'
```

---

## Validation

The project validates:

- mode enable / disable
- phase routing
- method / router / leaf routing
- semantic fallback
- ordinary-mode cleanliness
- session isolation
- orchestration gates

---

## Known Limitations

- this is a **control/profile layer**, not a full attack platform
- it does not include RAG or private knowledge retrieval
- execution depth still depends on your MCP/tooling surface

---

## ⚠️ Disclaimer

**This project is for authorized penetration testing, red-team research, and defensive security experiments only.**

- Use it only where you have explicit authorization.
- Unauthorized use against third-party or production systems is strictly prohibited.
- The authors and contributors assume **no liability** for misuse, legal consequences, service disruption, or data loss.
- By using this project, you accept full responsibility for complying with applicable laws and rules of engagement.

---

## Thanks / Contributions

感谢米斯特安全团队的浩熙大佬提出的修改意见：加入语义判定。  
浩熙X：@xishan12509850

感谢 `qiushi-skill`、`hack-skills` 与 `Anthropic-Cybersecurity-Skills` 提供的方法层、技术路由层与 skill pack 结构参考。  
参考项目：`qiushi-skill` / `yaklang/hack-skills` / `mukul975/Anthropic-Cybersecurity-Skills`

See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

MIT with an authorized-use-only notice.  
See [LICENSE](./LICENSE).
