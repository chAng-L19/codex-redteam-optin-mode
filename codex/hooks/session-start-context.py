#!/usr/bin/env python3
from __future__ import annotations
import json
import os
from pathlib import Path


def state_path() -> Path:
    temp_dir = Path(os.environ.get('TEMP') or os.environ.get('TMP') or str(Path.home()))
    return temp_dir / 'codex_redteam_mode_state.json'


def main() -> None:
    try:
        state_path().write_text(json.dumps({'enabled': False}, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass
    context = '[mode] Default session mode is normal. Red-team mode is disabled unless the user explicitly enables it with phrases like 进入红队模式 or /redteam on.'
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'SessionStart',
            'additionalContext': context,
        }
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
