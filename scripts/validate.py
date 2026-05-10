from __future__ import annotations

import argparse
import importlib.util
import io
import json
import runpy
import sys
from pathlib import Path


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"missing: {path}")


class FakeIn:
    def __init__(self, b: bytes) -> None:
        self.buffer = io.BytesIO(b)


def run_hook(path: Path, payload: dict) -> str:
    old_stdin, old_stdout = sys.stdin, sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    sys.stdin = FakeIn(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    try:
        runpy.run_path(str(path), run_name="__main__")
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout
    return buf.getvalue().strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    args = parser.parse_args()
    codex_home = Path(args.codex_home)

    files = [
        codex_home / "AGENTS.md",
        codex_home / "hooks.json",
        codex_home / "hooks" / "session-start-context.py",
        codex_home / "hooks" / "hook-security-context-hook.py",
        codex_home / "hooks" / "redteam_state.py",
        codex_home / "hooks" / "core" / "__init__.py",
    ]
    for f in files:
        assert_exists(f)

    hooks_dir = codex_home / "hooks"
    if str(hooks_dir) not in sys.path:
        sys.path.insert(0, str(hooks_dir))

    for idx, hook in enumerate([files[2], files[3], files[4]], start=1):
        name = f"validate_mod_{idx}"
        spec = importlib.util.spec_from_file_location(name, hook)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        sys.modules[name] = mod
        spec.loader.exec_module(mod)

    enable = run_hook(files[3], {"prompt": "进入红队模式"})
    reverse = run_hook(files[3], {"prompt": "请从二进制反编译的角度分析这个程序"})
    reverse_sem = run_hook(files[3], {"prompt": "程序启动后会释放文件并拉起子进程，帮我梳理执行链"})
    audit = run_hook(files[3], {"prompt": "请对这份源码做安全审计"})
    audit_sem = run_hook(files[3], {"prompt": "帮我从入口一路追到危险函数，看看权限边界哪里失守"})
    postex_sem = run_hook(files[3], {"prompt": "拿到 shell 之后下一步应该先做什么"})
    disable = run_hook(files[3], {"prompt": "退出红队模式"})

    report = [
        "# Validation Report",
        "",
        f"- files: ok ({len(files)})",
        f"- enable: {'ok' if 'enabled' in enable else 'fail'}",
        f"- reverse phase: {'ok' if 'phase:reverse' in reverse else 'fail'}",
        f"- reverse semantic fallback: {'ok' if 'phase:reverse' in reverse_sem else 'fail'}",
        f"- code-audit phase: {'ok' if 'phase:code-audit' in audit else 'fail'}",
        f"- code-audit semantic fallback: {'ok' if 'phase:code-audit' in audit_sem else 'fail'}",
        f"- postex semantic fallback: {'ok' if 'phase:postex' in postex_sem else 'fail'}",
        f"- disable: {'ok' if 'disabled' in disable else 'fail'}",
    ]
    print("\n".join(report))


if __name__ == "__main__":
    main()
