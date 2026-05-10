#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))

from core import (
    detect_phase,
    doctrine_for_phase,
    emit_hook_json,
    extract_prompt,
    extract_session_id,
    load_runtime_state,
    parse_mode_command,
    parse_opsec_command,
    save_runtime_state,
)
from core.prompt_parser import decode_stdin, load_payload


def main() -> None:
    raw = decode_stdin(sys.stdin.buffer.read())
    if not raw.strip():
        return
    try:
        payload = load_payload(raw)
    except Exception:
        return
    prompt = extract_prompt(payload)
    if not prompt.strip():
        return
    session_id = extract_session_id(payload)

    state = load_runtime_state(session_id=session_id)

    mode = parse_mode_command(prompt)
    if mode is not None:
        state = replace(state, mode=mode, phase="general")
        save_runtime_state(state, session_id=session_id)
        if mode == "normal":
            print(emit_hook_json("UserPromptSubmit", "[mode] Red-team mode disabled. Return to normal mode; do not inject offensive doctrine unless you explicitly enable it again."))
        else:
            print(emit_hook_json("UserPromptSubmit", f"[mode] Red-team mode enabled ({mode}). Subsequent prompts will use red-team doctrine until you explicitly disable it."))
        return

    opsec = parse_opsec_command(prompt)
    if opsec is not None:
        state = replace(state, opsec_level=opsec)
        save_runtime_state(state, session_id=session_id)
        print(emit_hook_json("UserPromptSubmit", f"[mode] OPSEC level updated to {opsec}."))
        return

    if state.mode == "normal":
        return

    phase = detect_phase(prompt)
    state = replace(state, phase=phase)
    save_runtime_state(state, session_id=session_id)
    print(emit_hook_json("UserPromptSubmit", doctrine_for_phase(phase, state.opsec_level)))


if __name__ == "__main__":
    main()
