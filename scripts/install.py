from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def color(text: str, code: str) -> str:
    if os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def info(msg: str) -> None:
    print(color(f"[INFO] {msg}", "36"))


def good(msg: str) -> None:
    print(color(f"[OK] {msg}", "32"))


def warn(msg: str) -> None:
    print(color(f"[WARN] {msg}", "33"))


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


def render_hooks_template(repo_root: Path, codex_home: Path, dry_run: bool) -> None:
    src = repo_root / "templates" / "hooks.json.template"
    dst = codex_home / "hooks.json"
    python_cmd = "python" if os.name == "nt" else "python3"
    script_dir = str(codex_home / "hooks")
    if os.name == "nt":
        script_dir = script_dir.replace("\\", "\\\\")
    text = (
        src.read_text(encoding="utf-8")
        .replace("{{PYTHON_CMD}}", python_cmd)
        .replace("{{CODEX_HOOKS_DIR}}", script_dir)
    )
    info(f"render {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")


def run_validate(repo_root: Path, codex_home: Path, dry_run: bool) -> None:
    if dry_run:
        return
    validate = repo_root / "scripts" / "validate.py"
    subprocess.run(
        [sys.executable, str(validate), "--codex-home", str(codex_home)],
        check=True,
    )


def uninstall(repo_root: Path, codex_home: Path, agents_home: Path, dry_run: bool) -> None:
    targets = [
        codex_home / "AGENTS.md",
        codex_home / "hooks.json",
        codex_home / "hooks" / "session-start-context.py",
        codex_home / "hooks" / "hook-security-context-hook.py",
        codex_home / "hooks" / "redteam_state.py",
        codex_home / "hooks" / "core",
        agents_home / "skills" / "red-team-command-doctrine",
    ]
    for target in targets:
        info(f"remove {target}")
        if not dry_run and target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()


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

    if args.uninstall:
        uninstall(repo_root, codex_home, agents_home, args.dry_run)
        good("uninstall complete")
        return

    for path in [
        codex_home / "AGENTS.md",
        codex_home / "hooks.json",
        codex_home / "hooks" / "session-start-context.py",
        codex_home / "hooks" / "hook-security-context-hook.py",
        codex_home / "hooks" / "redteam_state.py",
        codex_home / "hooks" / "core",
        agents_home / "skills" / "red-team-command-doctrine",
    ]:
        backup(path, args.dry_run)

    copy_file(repo_root / "codex" / "AGENTS.md", codex_home / "AGENTS.md", args.dry_run)
    copy_file(repo_root / "codex" / "hooks" / "session-start-context.py", codex_home / "hooks" / "session-start-context.py", args.dry_run)
    copy_file(repo_root / "codex" / "hooks" / "hook-security-context-hook.py", codex_home / "hooks" / "hook-security-context-hook.py", args.dry_run)
    copy_file(repo_root / "codex" / "hooks" / "redteam_state.py", codex_home / "hooks" / "redteam_state.py", args.dry_run)
    copy_tree(repo_root / "codex" / "hooks" / "core", codex_home / "hooks" / "core", args.dry_run)
    copy_tree(repo_root / "agents" / "skills" / "red-team-command-doctrine", agents_home / "skills" / "red-team-command-doctrine", args.dry_run)
    render_hooks_template(repo_root, codex_home, args.dry_run)
    run_validate(repo_root, codex_home, args.dry_run)
    good("install complete")


if __name__ == "__main__":
    main()
