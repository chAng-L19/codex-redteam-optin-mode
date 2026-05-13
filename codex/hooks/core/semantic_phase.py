from __future__ import annotations

import math
import re
from collections import Counter
from functools import lru_cache
from typing import Iterable


PHASE_EXAMPLES: dict[str, list[str]] = {
    "web": [
        "trace one exploit path through requests parameters session state and hidden endpoints",
        "analyze a web vulnerability chain with reproduction steps and request order",
        "review this burp traffic and determine whether the issue is exploitable",
        "梳理这个接口的鉴权 会话状态 隐藏参数和请求顺序 证明一条可利用链",
        "分析网页登录 流量 边界检查 和漏洞复现路径",
        "审查 burp 数据包 鉴权边界 API 行为和参数污染",
    ],
    "ad": [
        "map trust edges sessions credential opportunities and the lowest-noise path through active directory",
        "reason about kerberos delegation acl abuse and lateral movement in a windows domain",
        "identify the next quiet step in an ad attack chain using sessions and permissions",
        "分析域控环境中的委派 票据 会话和 ACL 路径",
        "在 AD 中寻找最小噪声的凭证复用和横向链路",
    ],
    "postex": [
        "triage a foothold for privilege escalation credential reuse and next-hop value",
        "evaluate what to do after code execution on a host",
        "reason about host enumeration privesc and post exploitation priorities",
        "拿到 foothold 后判断提权 凭证收集和下一跳价值",
        "后渗透阶段如何做主机分诊和推进",
        "拿到 shell 之后先做什么 如何继续后渗透和主机分诊",
    ],
    "reverse": [
        "recover the execution chain of a binary loader or malware sample",
        "analyze unpacking configuration extraction process launch sequence and binary logic",
        "reverse engineer the program to understand stages callbacks and operator tradecraft",
        "分析样本执行链 释放逻辑 配置提取和子进程拉起",
        "从逆向角度梳理二进制的控制流 载荷和行为链",
        "程序启动后会释放文件并拉起子进程 帮我梳理执行链和行为逻辑",
    ],
    "code-audit": [
        "trace one controllable input to a dangerous sink across handlers middleware and trust boundaries",
        "review source code for auth permission logic hidden trust shortcuts and a precise proof path",
        "analyze code structure to find an exploitable path from entrypoint to sink",
        "从源码入口追到危险函数 检查鉴权 边界和信任假设",
        "做代码审计 梳理 controller middleware 和 sink 之间的一条漏洞路径",
        "帮我从入口一路追到危险函数 看看权限边界哪里失守",
    ],
    "payload": [
        "choose payload shape launcher format staged versus stageless tradeoffs and delivery constraints",
        "reason about shellcode loaders and the best payload format for the target",
        "compare delivery formats and operator tradeoffs for an implant or launcher",
        "选择载荷形态 staged 或 stageless 以及投递格式",
        "比较 shellcode launcher 和 payload 方案的适配性",
    ],
    "evasion": [
        "plan av edr waf or sandbox bypass techniques with low-noise tradeoffs",
        "evaluate defender bypass options and operational constraints",
        "reason about waf bypass header tricks request shaping and av evasion",
        "分析免杀 绕过 对抗和低噪声规避路径",
        "对比 WAF 绕过 AV EDR 规避和沙箱逃逸策略",
    ],
}


TOKEN_RE = re.compile(r"[a-z0-9_./-]+|[\u4e00-\u9fff]")


def _normalize(text: str) -> str:
    text = text.casefold()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _char_ngrams(token: str, n: int = 3) -> Iterable[str]:
    if len(token) <= n:
        yield token
        return
    for i in range(len(token) - n + 1):
        yield token[i : i + n]


def _tokenize(text: str) -> list[str]:
    normalized = _normalize(text)
    pieces = TOKEN_RE.findall(normalized)
    tokens: list[str] = []
    for piece in pieces:
        if re.fullmatch(r"[\u4e00-\u9fff]", piece):
            tokens.append(piece)
            continue
        tokens.append(piece)
        tokens.extend(_char_ngrams(piece))
    return tokens


def _vectorize(text: str) -> Counter[str]:
    return Counter(_tokenize(text))


def _cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b.get(k, 0) for k in a)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@lru_cache(maxsize=1)
def _phase_prototypes() -> dict[str, Counter[str]]:
    return {phase: _vectorize(" ".join(examples)) for phase, examples in PHASE_EXAMPLES.items()}


def classify_phase_semantically(prompt: str) -> tuple[str | None, float]:
    query = _vectorize(prompt)
    best_phase: str | None = None
    best_score = 0.0
    for phase, proto in _phase_prototypes().items():
        score = _cosine(query, proto)
        if score > best_score:
            best_phase = phase
            best_score = score
    return best_phase, best_score
