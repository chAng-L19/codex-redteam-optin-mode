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


def hook_context_len(output: str) -> int:
    if not output:
        return 0
    raw = json.loads(output)
    return len(raw["hookSpecificOutput"]["additionalContext"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    args = parser.parse_args()
    codex_home = Path(args.codex_home)

    manifest_file = codex_home / "redteam-install-manifest.json"
    instruction_file = codex_home / "instruction.ctf.md"
    agents_file = codex_home / "AGENTS.md"
    hooks_json = codex_home / "hooks.json"
    session_hook = codex_home / "hooks" / "session-start-context.py"
    prompt_hook = codex_home / "hooks" / "hook-security-context-hook.py"
    state_file = codex_home / "hooks" / "redteam_state.py"
    core_init = codex_home / "hooks" / "core" / "__init__.py"
    router_init = codex_home / "router" / "__init__.py"
    orch_init = codex_home / "orchestrator" / "__init__.py"

    files = [
        manifest_file,
        instruction_file,
        agents_file,
        hooks_json,
        session_hook,
        prompt_hook,
        state_file,
        core_init,
        router_init,
        orch_init,
    ]
    for f in files:
        assert_exists(f)

    hooks_dir = codex_home / "hooks"
    for insert_path in (hooks_dir, codex_home):
        insert_str = str(insert_path)
        if insert_str not in sys.path:
            sys.path.insert(0, insert_str)

    for idx, hook in enumerate([session_hook, prompt_hook, state_file], start=1):
        name = f"validate_mod_{idx}"
        spec = importlib.util.spec_from_file_location(name, hook)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        sys.modules[name] = mod
        spec.loader.exec_module(mod)

    enable = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "进入红队模式"})
    reverse = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "请从二进制反编译的角度分析这个程序"})
    reverse_sem = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "程序启动后会释放文件并拉起子进程，帮我梳理执行链"})
    audit = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "请对这份源码做安全审计"})
    audit_sem = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "帮我从入口一路追到危险函数，看看权限边界哪里失守"})
    postex_sem = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "拿到 shell 之后下一步应该先做什么"})
    full_enable = run_hook(prompt_hook, {"session_id": "validate-full", "prompt": "/redteam full"})
    full_web = run_hook(prompt_hook, {"session_id": "validate-full", "prompt": "Burp 里这个 JWT 登录接口怎么验证鉴权边界和 token 复用风险"})
    session_ctx = run_hook(session_hook, {"session_id": "validate-session"})
    ordinary = run_hook(prompt_hook, {"session_id": "validate-session-2", "prompt": "普通编程问题"})
    disable = run_hook(prompt_hook, {"session_id": "validate-main", "prompt": "退出红队模式"})

    if str(codex_home) not in sys.path:
        sys.path.insert(0, str(codex_home))
    import orchestrator as orch

    recon = orch.ReconArtifact(scope="lab", hosts=["10.0.0.5"], ports=["80/tcp"], services=["http"], evidence_refs=["scan.json"], confidence=0.9)
    strategy = orch.StrategyArtifact(
        candidate_paths=[orch.StrategyPath(name="web-path", rationale="http present")],
        chosen_path="web-path",
        evidence_refs=["scan.json"],
    )
    review = orch.ReviewArtifact(status="pass", next_action="deliver")
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest_ok = manifest_data.get("name") == "codex-redteam-optin-mode" and any(
        str(path).endswith("instruction.ctf.md") for path in manifest_data.get("managed_paths", [])
    )

    report = [
        "# Validation Report",
        "",
        f"- files: ok ({len(files)})",
        f"- install manifest: {'ok' if manifest_ok else 'fail'}",
        f"- enable: {'ok' if 'enabled' in enable else 'fail'}",
        f"- reverse phase: {'ok' if 'phase:reverse' in reverse else 'fail'}",
        f"- reverse semantic fallback: {'ok' if 'phase:reverse' in reverse_sem else 'fail'}",
        f"- code-audit phase: {'ok' if 'phase:code-audit' in audit else 'fail'}",
        f"- code-audit semantic fallback: {'ok' if 'phase:code-audit' in audit_sem else 'fail'}",
        f"- postex semantic fallback: {'ok' if 'phase:postex' in postex_sem else 'fail'}",
        f"- method/router/leaf routing: {'ok' if all(token in full_web for token in ('method:', 'router:', 'leaf:')) else 'fail'}",
        f"- redteam-full distinction: {'ok' if '[mode:redteam-full]' in full_web and '[workflow:structured-orchestration]' in full_web and '[review:required]' in full_web else 'fail'}",
        f"- session start context size: {'ok' if hook_context_len(session_ctx) <= 260 else 'fail'}",
        f"- ordinary prompt stays empty: {'ok' if ordinary == '' else 'fail'}",
        f"- recon gate: {'ok' if orch.recon_gate(recon).ok else 'fail'}",
        f"- strategy gate: {'ok' if orch.strategy_gate(strategy).ok else 'fail'}",
        f"- review gate: {'ok' if orch.review_gate(review).ok else 'fail'}",
        f"- disable: {'ok' if 'disabled' in disable else 'fail'}",
    ]
    print("\n".join(report))


if __name__ == "__main__":
    main()
