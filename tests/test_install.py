from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.py"


class InstallTests(unittest.TestCase):
    def test_install_removes_previous_managed_paths_and_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            codex_home = base / "codex-home"
            agents_home = base / "agents-home"
            codex_home.mkdir(parents=True)
            agents_home.mkdir(parents=True)

            stale_file = codex_home / "hooks" / "legacy-redteam-hook.py"
            stale_file.parent.mkdir(parents=True, exist_ok=True)
            stale_file.write_text("legacy", encoding="utf-8")

            stale_skill = agents_home / "skills" / "red-team-command-doctrine-old"
            stale_skill.mkdir(parents=True, exist_ok=True)
            (stale_skill / "SKILL.md").write_text("legacy", encoding="utf-8")

            manifest = codex_home / "redteam-install-manifest.json"
            manifest.write_text(json.dumps({
                "name": "codex-redteam-optin-mode",
                "version": "0.2.0",
                "managed_paths": [
                    str(stale_file),
                    str(stale_skill),
                ],
            }, ensure_ascii=False, indent=2), encoding="utf-8")

            subprocess.run([
                sys.executable,
                str(INSTALL),
                "--codex-home",
                str(codex_home),
                "--agents-home",
                str(agents_home),
            ], check=True)

            self.assertFalse(stale_file.exists())
            self.assertFalse(stale_skill.exists())
            self.assertTrue(manifest.exists())
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], "codex-redteam-optin-mode")
            self.assertIn("managed_paths", data)
            self.assertTrue(any(path.endswith("instruction.ctf.md") for path in data["managed_paths"]))
            self.assertEqual([], [str(p) for p in base.rglob("*.bak.*")])

    def test_install_preserves_existing_agents_and_hooks_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            codex_home = base / "codex-home"
            agents_home = base / "agents-home"
            codex_home.mkdir(parents=True)
            agents_home.mkdir(parents=True)

            agents_file = codex_home / "AGENTS.md"
            agents_file.write_text("# User AGENTS\n\n- keep my custom rules\n", encoding="utf-8")

            hooks_file = codex_home / "hooks.json"
            hooks_file.write_text(json.dumps({
                "hooks": {
                    "UserPromptSubmit": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "python custom_hook.py",
                                    "statusMessage": "User custom hook",
                                    "timeout": 10,
                                }
                            ]
                        }
                    ]
                }
            }, ensure_ascii=False, indent=2), encoding="utf-8")

            install_cmd = [
                sys.executable,
                str(INSTALL),
                "--codex-home",
                str(codex_home),
                "--agents-home",
                str(agents_home),
            ]
            subprocess.run(install_cmd, check=True)
            subprocess.run(install_cmd, check=True)

            merged_agents = agents_file.read_text(encoding="utf-8")
            self.assertIn("keep my custom rules", merged_agents)
            self.assertEqual(1, merged_agents.count("codex-redteam-optin-mode:start"))
            self.assertIn("canonical model instructions file", merged_agents)

            hooks = json.loads(hooks_file.read_text(encoding="utf-8"))
            user_hook_found = False
            managed_session = 0
            managed_prompt = 0
            for entries in hooks.get("hooks", {}).values():
                for entry in entries:
                    for hook in entry.get("hooks", []):
                        if hook.get("statusMessage") == "User custom hook":
                            user_hook_found = True
                        if hook.get("statusMessage") == "Loading session mode context":
                            managed_session += 1
                        if hook.get("statusMessage") == "Checking mode-gated offensive routing":
                            managed_prompt += 1
            self.assertTrue(user_hook_found)
            self.assertEqual(1, managed_session)
            self.assertEqual(1, managed_prompt)
            self.assertEqual([], [str(p) for p in base.rglob("*.bak.*")])


if __name__ == "__main__":
    unittest.main()
