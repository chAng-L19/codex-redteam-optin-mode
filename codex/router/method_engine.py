from __future__ import annotations

import re

from .mappings import PHASE_DEFAULT_METHOD, PHASE_ESCALATION_METHOD


METHOD_HINTS = [
    ("criticism-self-criticism", [r"\breview\b", r"\bself[- ]?review\b", r"复盘", r"自检", r"审查输出"]),
    ("workflows", [r"\bworkflow\b", r"\bplaybook\b", r"\bchain\b", r"多阶段", r"整条链", r"工作流"]),
    ("overall-planning", [r"\bplan\b", r"\broadmap\b", r"总体", r"路线图", r"分阶段"]),
    ("concentrate-forces", [r"\bpriorit", r"\bwhich path\b", r"优先", r"主攻", r"先打哪条"]),
    ("contradiction-analysis", [r"\btrade[- ]?off\b", r"\bcompare\b", r"权衡", r"冲突", r"还是"]),
    ("practice-cognition", [r"\bpoc\b", r"\bscaffold\b", r"实验", r"验证脚本", r"最小实现"]),
    ("investigation-first", [r"\banalyze\b", r"\btrace\b", r"\breconstruct\b", r"梳理", r"分析", r"定位"]),
]


def select_method(prompt: str, phase: str, mode: str) -> str:
    if mode == "redteam-full":
        if re.search(r"\bworkflow\b|多阶段|整条链|计划", prompt, re.I):
            return "workflows"
    for method, patterns in METHOD_HINTS:
        if any(re.search(pat, prompt, re.I) for pat in patterns):
            return method
    return PHASE_ESCALATION_METHOD.get(phase, "overall-planning") if mode == "redteam-full" else PHASE_DEFAULT_METHOD.get(phase, "overall-planning")
