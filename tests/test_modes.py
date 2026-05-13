from __future__ import annotations

import io
import json
import runpy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "codex" / "hooks" / "hook-security-context-hook.py"
SESSION = ROOT / "codex" / "hooks" / "session-start-context.py"


class FakeIn:
    def __init__(self, b: bytes) -> None:
        self.buffer = io.BytesIO(b)


def run_script(path: Path, payload: dict | None = None) -> str:
    old_stdin, old_stdout = sys.stdin, sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    data = b"" if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdin = FakeIn(data)
    try:
        runpy.run_path(str(path), run_name="__main__")
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout
    return buf.getvalue().strip()


def context_len(output: str) -> int:
    if not output:
        return 0
    return len(json.loads(output)["hookSpecificOutput"]["additionalContext"])


class HookTests(unittest.TestCase):
    def test_session_context_stays_small_and_normal_mode_stays_clean(self) -> None:
        session_out = run_script(SESSION, {"session_id": "size-check"})
        self.assertLessEqual(context_len(session_out), 260)
        self.assertEqual("", run_script(HOOK, {"session_id": "size-check", "prompt": "写一个普通 React 页面"}))

    def test_enable_reverse_disable(self) -> None:
        run_script(SESSION)
        self.assertIn("enabled", run_script(HOOK, {"prompt": "进入红队模式"}))
        reverse = run_script(HOOK, {"prompt": "请从二进制反编译的角度分析这个程序"})
        self.assertIn("phase:reverse", reverse)
        self.assertIn("method:", reverse)
        self.assertIn("router:", reverse)
        self.assertIn("leaf:", reverse)
        audit = run_script(HOOK, {"prompt": "请对这份源码做安全审计"})
        self.assertIn("phase:code-audit", audit)
        self.assertIn("disabled", run_script(HOOK, {"prompt": "退出红队模式"}))

    def test_semantic_phase_fallback(self) -> None:
        run_script(SESSION)
        run_script(HOOK, {"prompt": "进入红队模式"})
        self.assertIn("phase:reverse", run_script(HOOK, {"prompt": "程序启动后会释放文件并拉起子进程，帮我梳理执行链"}))
        self.assertIn("phase:code-audit", run_script(HOOK, {"prompt": "帮我从入口一路追到危险函数，看看权限边界哪里失守"}))
        self.assertIn("phase:postex", run_script(HOOK, {"prompt": "拿到 shell 之后下一步应该先做什么"}))

    def test_full_mode_adds_structured_markers(self) -> None:
        run_script(SESSION, {"session_id": "full-mode"})
        self.assertIn("enabled", run_script(HOOK, {"session_id": "full-mode", "prompt": "/redteam full"}))
        full = run_script(HOOK, {"session_id": "full-mode", "prompt": "Burp 里这个 JWT 登录接口怎么验证鉴权边界和 token 复用风险"})
        self.assertIn("[mode:redteam-full]", full)
        self.assertIn("[workflow:structured-orchestration]", full)
        self.assertIn("[review:required]", full)

    def test_session_isolation(self) -> None:
        session_a = {"session_id": "sess-A"}
        session_b = {"session_id": "sess-B"}
        run_script(SESSION, session_a)
        run_script(SESSION, session_b)
        self.assertIn("enabled", run_script(HOOK, {"session_id": "sess-A", "prompt": "进入红队模式"}))
        self.assertEqual("", run_script(HOOK, {"session_id": "sess-B", "prompt": "普通编程问题"}))
        self.assertIn("phase:postex", run_script(HOOK, {"session_id": "sess-A", "prompt": "拿到 shell 之后下一步应该先做什么"}))
