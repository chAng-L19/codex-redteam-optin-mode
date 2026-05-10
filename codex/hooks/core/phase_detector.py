from __future__ import annotations

import re
from typing import Optional

from .semantic_phase import classify_phase_semantically


SEMANTIC_THRESHOLD = 0.10


PHASE_HINTS = {
    "web": "[security:redteam][phase:web] Focus on one verifiable exploit path, request order, auth/session state, hidden parameters, and precise reproduction.",
    "ad": "[security:redteam][phase:ad] Focus on credentials, trust edges, sessions, ACL paths, and lowest-noise progression.",
    "postex": "[security:redteam][phase:postex] Focus on foothold triage, privilege options, credential opportunities, and next-hop value.",
    "reverse": "[security:redteam][phase:reverse] Focus on execution chain, loader stages, binary logic, configuration extraction, and operator-relevant tradecraft lessons.",
    "code-audit": "[security:redteam][phase:code-audit] Focus on one controllable input-to-sink path, trust boundaries, auth/permission logic, and precise verification.",
    "payload": "[security:redteam][phase:payload] Focus on payload shape, launcher format, staged vs stageless tradeoffs, and delivery fit.",
    "general": "[security:redteam][phase:general] Keep the task offensively focused, evidence-first, low-noise, and explicit about next step.",
}


SECURITY_PATTERNS = [
    ("web", [r"\bxss\b", r"\bsqli\b", r"\bssrf\b", r"\bssti\b", r"\bidor\b", r"\bcsrf\b", r"\bxxe\b", r"\bburp\b", r"\brepeater\b", r"\bproxy\b", r"\bgraphql\b", r"注入", r"越权"]),
    ("ad", [r"\bkerberos\b", r"\bntlm\b", r"\badcs\b", r"\bbloodhound\b", r"域控", r"横向", r"委派", r"票据", r"凭证"]),
    ("postex", [r"\bpost[- ]?ex\b", r"\bfoothold\b", r"privilege escalation", r"lateral movement", r"提权", r"后渗透"]),
    ("reverse", [r"\breverse\b", r"\bmalware\b", r"\bdropper\b", r"\bstager\b", r"\bloader\b", r"木马", r"样本", r"逆向", r"反编译", r"二进制"]),
    ("code-audit", [r"code audit", r"审计", r"源码", r"source code", r"middleware", r"handler", r"controller", r"\bgrep\b", r"静态分析"]),
    ("payload", [r"\bpayload\b", r"\bshellcode\b", r"\bstaged\b", r"\bstageless\b", r"载荷"]),
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


def doctrine_for_phase(phase: str, opsec_level: str) -> str:
    tail = " Prefer one proven path before broad scans. Distinguish facts from assumptions. End with explicit next step."
    if opsec_level == "strict":
        tail += " Keep noise low and avoid unnecessary expansion."
    return PHASE_HINTS.get(phase, PHASE_HINTS["general"]) + tail
