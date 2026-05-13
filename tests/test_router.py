from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "codex") not in sys.path:
    sys.path.insert(0, str(ROOT / "codex"))

from router import select_leaf_skill, select_method, select_router, select_subphase  # noqa: E402


class RouterTests(unittest.TestCase):
    def test_method_selection(self) -> None:
        self.assertEqual(select_method("帮我分析这个 Burp 链路", "web", "redteam-light"), "investigation-first")
        self.assertEqual(select_method("这两条路径该优先打哪条", "web", "redteam-light"), "concentrate-forces")
        self.assertEqual(select_method("给我一个多阶段 workflow", "postex", "redteam-full"), "workflows")

    def test_router_and_leaf_selection(self) -> None:
        web_prompt = "Burp 里这个 JWT 登录接口怎么验证鉴权边界和 token 复用风险"
        self.assertEqual(select_router(web_prompt, "web"), "auth-sec")
        self.assertEqual(select_leaf_skill(web_prompt, "web", "auth-sec"), "jwt-oauth-token-attacks")

        audit_prompt = "帮我从 controller 入口一路追到危险函数 看看权限边界哪里失守"
        self.assertEqual(select_router(audit_prompt, "code-audit"), "hack")
        self.assertEqual(select_subphase(audit_prompt, "code-audit"), "entrypoint")

        reverse_prompt = "程序启动后会释放文件并拉起子进程，帮我梳理执行链"
        self.assertEqual(select_router(reverse_prompt, "reverse"), "malware-loader-analysis")
        self.assertEqual(select_subphase(reverse_prompt, "reverse"), "loader")

    def test_evasion_routing(self) -> None:
        prompt = "想测试 WAF 绕过和 403 旁路的低噪声路径"
        self.assertEqual(select_router(prompt, "evasion"), "windows-av-evasion")
        self.assertEqual(select_leaf_skill(prompt, "evasion", "windows-av-evasion"), "waf-bypass-techniques")
        self.assertEqual(select_subphase(prompt, "evasion"), "network")


if __name__ == "__main__":
    unittest.main()
