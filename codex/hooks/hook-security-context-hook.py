#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ENABLE_PATTERNS = [
    r'进入红队模式', r'开启红队模式', r'/redteam\s+on', r'enable\s+red\s*team\s*mode'
]
DISABLE_PATTERNS = [
    r'退出红队模式', r'关闭红队模式', r'/redteam\s+off', r'disable\s+red\s*team\s*mode'
]

PHASE_HINTS = {
    'web': '[security:redteam][phase:web] Focus on one verifiable exploit path, request order, auth/session state, hidden parameters, and precise reproduction.',
    'ad': '[security:redteam][phase:ad] Focus on credentials, trust edges, sessions, ACL paths, and lowest-noise progression.',
    'postex': '[security:redteam][phase:postex] Focus on foothold triage, privilege options, credential opportunities, and next-hop value.',
    'reverse': '[security:redteam][phase:reverse] Focus on execution chain, loader stages, configuration extraction, and operator-relevant tradecraft lessons.',
    'payload': '[security:redteam][phase:payload] Focus on payload shape, launcher format, staged vs stageless tradeoffs, and delivery fit.',
    'general': '[security:redteam][phase:general] Keep the task offensively focused, evidence-first, low-noise, and explicit about next step.'
}
SECURITY_PATTERNS = [
    ('web', [r'xss', r'sqli', r'ssrf', r'ssti', r'idor', r'csrf', r'xxe', r'burp', r'repeater', r'proxy', r'graphql', r'注入', r'越权']),
    ('ad', [r'kerberos', r'ntlm', r'adcs', r'bloodhound', r'域控', r'横向', r'委派', r'票据', r'凭证']),
    ('postex', [r'post[- ]?ex', r'foothold', r'privilege escalation', r'lateral movement', r'提权', r'后渗透']),
    ('reverse', [r'reverse', r'malware', r'dropper', r'stager', r'loader', r'木马', r'样本', r'逆向']),
    ('payload', [r'payload', r'shellcode', r'staged', r'stageless', r'载荷'])
]


def state_path() -> Path:
    temp_dir = Path(os.environ.get('TEMP') or os.environ.get('TMP') or str(Path.home()))
    return temp_dir / 'codex_redteam_mode_state.json'


def load_state() -> dict:
    try:
        return json.loads(state_path().read_text(encoding='utf-8'))
    except Exception:
        return {'enabled': False}


def save_state(enabled: bool) -> None:
    try:
        state_path().write_text(json.dumps({'enabled': enabled}, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass


def read_stdin_text() -> str:
    data = sys.stdin.buffer.read()
    if not data:
        return ''
    for enc in ('utf-8', 'utf-8-sig', sys.getdefaultencoding(), 'gb18030', 'gbk'):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode('utf-8', 'replace')


def extract_prompt(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if not isinstance(payload, dict):
        return ''
    for key in ('prompt', 'input', 'text', 'message', 'user_prompt'):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    messages = payload.get('messages')
    if isinstance(messages, list):
        parts = []
        for item in messages:
            if not isinstance(item, dict):
                continue
            content = item.get('content')
            if isinstance(content, str):
                parts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and isinstance(block.get('text'), str):
                        parts.append(block['text'])
        return '\n'.join(parts)
    return ''


def detect_phase(prompt: str) -> str:
    for phase, patterns in SECURITY_PATTERNS:
        for pat in patterns:
            if re.search(pat, prompt, re.I):
                return phase
    return 'general'


def emit(context: str) -> None:
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit', 'additionalContext': context}}, ensure_ascii=False))


def main() -> None:
    raw = read_stdin_text()
    if not raw.strip():
        return
    try:
        payload = json.loads(raw)
    except Exception:
        return
    prompt = extract_prompt(payload)
    if not prompt.strip():
        return

    for pat in ENABLE_PATTERNS:
        if re.search(pat, prompt, re.I):
            save_state(True)
            emit('[mode] Red-team mode enabled. Subsequent prompts will use red-team doctrine until you explicitly disable it.')
            return

    for pat in DISABLE_PATTERNS:
        if re.search(pat, prompt, re.I):
            save_state(False)
            emit('[mode] Red-team mode disabled. Return to normal mode; do not inject offensive doctrine unless you explicitly enable it again.')
            return

    if not load_state().get('enabled', False):
        return

    phase = detect_phase(prompt)
    doctrine = ' Prefer one proven path before broad scans. Distinguish facts from assumptions. End with explicit next step.'
    emit(PHASE_HINTS.get(phase, PHASE_HINTS['general']) + doctrine)


if __name__ == '__main__':
    main()
