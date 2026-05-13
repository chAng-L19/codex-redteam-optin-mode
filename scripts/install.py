from __future__ import annotations

import argparse
import copy
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

APP_NAME = "codex-redteam-optin-mode"
APP_VERSION = "0.3.1"
AGENTS_BLOCK_START = "<!-- codex-redteam-optin-mode:start -->"
AGENTS_BLOCK_END = "<!-- codex-redteam-optin-mode:end -->"
SESSION_STATUS = "Loading session mode context"
PROMPT_STATUS = "Checking mode-gated offensive routing"


def color(text: str, code: str) -> str:
    if os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def info(msg: str) -> None:
    print(color(f"[INFO] {msg}", "36"))


def good(msg: str) -> None:
    print(color(f"[OK] {msg}", "32"))


def manifest_path(codex_home: Path) -> Path:
    return codex_home / "redteam-install-manifest.json"


def detect_codex_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    env = os.environ.get("CODEX_HOME")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".codex"


def detect_agents_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    return Path.home() / ".agents"


def backup(path: Path, dry_run: bool) -> None:
    if not path.exists():
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = path.with_name(path.name + f".bak.{stamp}")
    info(f"backup {path} -> {dest}")
    if not dry_run:
        if path.is_dir():
            shutil.copytree(path, dest)
        else:
            shutil.copy2(path, dest)


def remove_path(path: Path, dry_run: bool) -> None:
    info(f"remove {path}")
    if dry_run or not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def copy_file(src: Path, dst: Path, dry_run: bool) -> None:
    info(f"copy {src} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path, dry_run: bool) -> None:
    info(f"copy {src} -> {dst}")
    if dry_run:
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build_hooks_payload(repo_root: Path, codex_home: Path) -> dict:
    src = repo_root / "templates" / "hooks.json.template"
    python_cmd = "python" if os.name == "nt" else "python3"
    script_dir = str(codex_home / "hooks")
    if os.name == "nt":
        script_dir = script_dir.replace("\\", "\\\\")
    text = (
        src.read_text(encoding="utf-8")
        .replace("{{PYTHON_CMD}}", python_cmd)
        .replace("{{CODEX_HOOKS_DIR}}", script_dir)
    )
    return json.loads(text)


def managed_agents_block(repo_root: Path) -> str:
    body = (repo_root / "codex" / "AGENTS.md").read_text(encoding="utf-8").strip()
    return f"{AGENTS_BLOCK_START}\n{body}\n{AGENTS_BLOCK_END}\n"


def upsert_agents_file(repo_root: Path, codex_home: Path, dry_run: bool) -> None:
    dst = codex_home / "AGENTS.md"
    block = managed_agents_block(repo_root)
    info(f"merge {repo_root / 'codex' / 'AGENTS.md'} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        current = dst.read_text(encoding="utf-8")
        pattern = re.compile(rf"{re.escape(AGENTS_BLOCK_START)}.*?{re.escape(AGENTS_BLOCK_END)}\n?", re.S)
        if pattern.search(current):
            merged = pattern.sub(lambda _: block, current)
        else:
            sep = "" if current.endswith("\n") or current == "" else "\n"
            merged = f"{current}{sep}\n{block}"
    else:
        merged = block
    dst.write_text(merged, encoding="utf-8")


def remove_agents_block(codex_home: Path, dry_run: bool) -> None:
    dst = codex_home / "AGENTS.md"
    if not dst.exists():
        return
    info(f"remove managed block from {dst}")
    if dry_run:
        return
    current = dst.read_text(encoding="utf-8")
    pattern = re.compile(rf"\n?{re.escape(AGENTS_BLOCK_START)}.*?{re.escape(AGENTS_BLOCK_END)}\n?", re.S)
    updated = pattern.sub("\n", current).strip()
    if updated:
        dst.write_text(updated + "\n", encoding="utf-8")
    else:
        dst.unlink()


def is_managed_hook(hook: dict) -> bool:
    command = str(hook.get("command", ""))
    status = str(hook.get("statusMessage", ""))
    return (
        "session-start-context.py" in command
        or "hook-security-context-hook.py" in command
        or status in {SESSION_STATUS, PROMPT_STATUS}
    )


def scrub_managed_hooks(payload: dict) -> dict:
    hooks_root = payload.get("hooks", {})
    cleaned: dict = {}
    for event, entries in hooks_root.items():
        new_entries = []
        for entry in entries:
            hooks = [hook for hook in entry.get("hooks", []) if not is_managed_hook(hook)]
            if hooks:
                cloned = copy.deepcopy(entry)
                cloned["hooks"] = hooks
                new_entries.append(cloned)
        if new_entries:
            cleaned[event] = new_entries
    payload["hooks"] = cleaned
    return payload


def merge_hooks_json(repo_root: Path, codex_home: Path, dry_run: bool) -> None:
    dst = codex_home / "hooks.json"
    rendered = build_hooks_payload(repo_root, codex_home)
    info(f"merge {repo_root / 'templates' / 'hooks.json.template'} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        existing = json.loads(dst.read_text(encoding="utf-8"))
    else:
        existing = {"hooks": {}}
    existing = scrub_managed_hooks(existing)
    hooks_root = existing.setdefault("hooks", {})
    for event, entries in rendered.get("hooks", {}).items():
        target = hooks_root.setdefault(event, [])
        target.extend(copy.deepcopy(entries))
    dst.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")


def remove_managed_hooks(codex_home: Path, dry_run: bool) -> None:
    dst = codex_home / "hooks.json"
    if not dst.exists():
        return
    info(f"remove managed hooks from {dst}")
    if not dry_run:
        payload = json.loads(dst.read_text(encoding="utf-8"))
        payload = scrub_managed_hooks(payload)
        hooks_root = payload.get("hooks", {})
        if hooks_root:
            dst.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            dst.unlink()


def run_validate(repo_root: Path, codex_home: Path, dry_run: bool) -> None:
    if dry_run:
        return
    validate = repo_root / "scripts" / "validate.py"
    subprocess.run([sys.executable, str(validate), "--codex-home", str(codex_home)], check=True)


def managed_targets(codex_home: Path, agents_home: Path) -> list[Path]:
    return [
        codex_home / "instruction.ctf.md",
        codex_home / "hooks" / "session-start-context.py",
        codex_home / "hooks" / "hook-security-context-hook.py",
        codex_home / "hooks" / "redteam_state.py",
        codex_home / "hooks" / "core",
        codex_home / "router",
        codex_home / "orchestrator",
        agents_home / "skills" / "red-team-command-doctrine",
    ]


def load_manifest_targets(codex_home: Path) -> list[Path]:
    manifest = manifest_path(codex_home)
    if not manifest.exists():
        return []
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    raw_paths = data.get("managed_paths", [])
    targets: list[Path] = []
    for raw in raw_paths:
        try:
            targets.append(Path(raw))
        except TypeError:
            continue
    return targets


def write_manifest(codex_home: Path, targets: list[Path], dry_run: bool) -> None:
    manifest = manifest_path(codex_home)
    payload = {
        "name": APP_NAME,
        "version": APP_VERSION,
        "installed_at": datetime.now().isoformat(timespec="seconds"),
        "managed_paths": [str(path) for path in targets],
        "merged_files": [str(codex_home / "AGENTS.md"), str(codex_home / "hooks.json")],
    }
    info(f"write manifest {manifest}")
    if dry_run:
        return
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def upgrade_cleanup(codex_home: Path, default_targets: list[Path], dry_run: bool) -> None:
    manifest = manifest_path(codex_home)
    previous_targets = load_manifest_targets(codex_home)
    cleanup_targets = previous_targets or default_targets
    protected = {str(codex_home / "AGENTS.md"), str(codex_home / "hooks.json")}

    remove_path(manifest, dry_run)
    seen: set[str] = set()
    for target in cleanup_targets:
        key = str(target)
        if key in seen:
            continue
        seen.add(key)
        if key in protected:
            continue
        remove_path(target, dry_run)


def uninstall(repo_root: Path, codex_home: Path, agents_home: Path, dry_run: bool) -> None:
    targets = load_manifest_targets(codex_home) or managed_targets(codex_home, agents_home)
    manifest = manifest_path(codex_home)
    for target in targets:
        remove_path(target, dry_run)
    remove_agents_block(codex_home, dry_run)
    remove_managed_hooks(codex_home, dry_run)
    remove_path(manifest, dry_run)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home")
    parser.add_argument("--agents-home")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    codex_home = detect_codex_home(args.codex_home)
    agents_home = detect_agents_home(args.agents_home)

    info(f"platform: {platform.system()}")
    info(f"codex home: {codex_home}")
    info(f"agents home: {agents_home}")

    current_targets = managed_targets(codex_home, agents_home)

    if args.uninstall:
        uninstall(repo_root, codex_home, agents_home, args.dry_run)
        good("uninstall complete")
        return

    upgrade_cleanup(codex_home, current_targets, args.dry_run)

    copy_file(repo_root / "instruction.ctf.md", codex_home / "instruction.ctf.md", args.dry_run)
    upsert_agents_file(repo_root, codex_home, args.dry_run)
    copy_file(repo_root / "codex" / "hooks" / "session-start-context.py", codex_home / "hooks" / "session-start-context.py", args.dry_run)
    copy_file(repo_root / "codex" / "hooks" / "hook-security-context-hook.py", codex_home / "hooks" / "hook-security-context-hook.py", args.dry_run)
    copy_file(repo_root / "codex" / "hooks" / "redteam_state.py", codex_home / "hooks" / "redteam_state.py", args.dry_run)
    copy_tree(repo_root / "codex" / "hooks" / "core", codex_home / "hooks" / "core", args.dry_run)
    copy_tree(repo_root / "codex" / "router", codex_home / "router", args.dry_run)
    copy_tree(repo_root / "codex" / "orchestrator", codex_home / "orchestrator", args.dry_run)
    copy_tree(repo_root / "agents" / "skills" / "red-team-command-doctrine", agents_home / "skills" / "red-team-command-doctrine", args.dry_run)
    merge_hooks_json(repo_root, codex_home, args.dry_run)
    write_manifest(codex_home, current_targets, args.dry_run)
    run_validate(repo_root, codex_home, args.dry_run)
    good("install complete")


if __name__ == "__main__":
    main()
