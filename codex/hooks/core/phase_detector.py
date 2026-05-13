from __future__ import annotations

import re
from typing import Optional

from .semantic_phase import classify_phase_semantically


SEMANTIC_THRESHOLD = 0.10


SECURITY_PATTERNS = [
    (
        "web",
        [
            r"\bxss\b",
            r"\bsqli\b",
            r"\bssrf\b",
            r"\bssti\b",
            r"\bidor\b",
            r"\bcsrf\b",
            r"\bxxe\b",
            r"\bburp\b",
            r"\brepeater\b",
            r"\bproxy\b",
            r"\bgraphql\b",
            r"\bapi\b",
            r"注入",
            r"越权",
            r"鉴权",
            r"接口",
            r"会话",
            r"请求顺序",
        ],
    ),
    (
        "ad",
        [
            r"\bkerberos\b",
            r"\bntlm\b",
            r"\badcs\b",
            r"\bbloodhound\b",
            r"\bacl\b",
            r"\bdelegation\b",
            r"域控",
            r"横向",
            r"委派",
            r"票据",
            r"凭证",
            r"证书服务",
        ],
    ),
    (
        "postex",
        [
            r"\bpost[- ]?ex\b",
            r"\bfoothold\b",
            r"privilege escalation",
            r"lateral movement",
            r"\bshell\b",
            r"提权",
            r"后渗透",
            r"主机分诊",
            r"拿到 shell",
        ],
    ),
    (
        "reverse",
        [
            r"\breverse\b",
            r"\bmalware\b",
            r"\bdropper\b",
            r"\bstager\b",
            r"\bloader\b",
            r"\bsample\b",
            r"木马",
            r"样本",
            r"逆向",
            r"反编译",
            r"二进制",
            r"执行链",
        ],
    ),
    (
        "code-audit",
        [
            r"code audit",
            r"\bsource code\b",
            r"\bcontroller\b",
            r"\bhandler\b",
            r"\bmiddleware\b",
            r"\bgrep\b",
            r"审计",
            r"源码",
            r"静态分析",
            r"危险函数",
            r"权限边界",
        ],
    ),
    (
        "payload",
        [
            r"\bpayload\b",
            r"\bshellcode\b",
            r"\bstaged\b",
            r"\bstageless\b",
            r"\blauncher\b",
            r"载荷",
            r"投递格式",
            r"shellcode",
        ],
    ),
    (
        "evasion",
        [
            r"\bedr\b",
            r"\bav\b",
            r"\bdefender\b",
            r"\bwaf\b",
            r"\b403\b",
            r"\bcsp\b",
            r"\bbypass\b",
            r"免杀",
            r"绕过",
            r"对抗",
            r"沙箱逃逸",
        ],
    ),
]


def detect_phase_rule_based(prompt: str) -> Optional[str]:
    for phase, patterns in SECURITY_PATTERNS:
        for pat in patterns:
            if re.search(pat, prompt, re.I):
                return phase
    return None


def detect_phase(prompt: str) -> str:
    matched = detect_phase_rule_based(prompt)
    if matched:
        return matched
    phase, score = classify_phase_semantically(prompt)
    if phase and score >= SEMANTIC_THRESHOLD:
        return phase
    return "general"
