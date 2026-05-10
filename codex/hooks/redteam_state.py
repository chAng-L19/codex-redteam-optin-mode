from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


VALID_MODES = {"normal", "redteam-light", "redteam-full"}
VALID_OPSEC = {"strict", "balanced"}


@dataclass
class RedTeamState:
    mode: str = "normal"
    phase: str = "general"
    opsec_level: str = "balanced"
    last_changed: str = ""
    session_id: str = ""

    def normalized(self) -> "RedTeamState":
        mode = self.mode if self.mode in VALID_MODES else "normal"
        opsec = self.opsec_level if self.opsec_level in VALID_OPSEC else "balanced"
        phase = self.phase or "general"
        last_changed = self.last_changed or now_iso()
        session_id = self.session_id or ""
        return RedTeamState(mode=mode, phase=phase, opsec_level=opsec, last_changed=last_changed, session_id=session_id)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_state(session_id: str | None = None) -> RedTeamState:
    return RedTeamState(mode="normal", phase="general", opsec_level="balanced", last_changed=now_iso(), session_id=session_id or "")


def state_dir() -> Path:
    temp_dir = Path(os.environ.get("TEMP") or os.environ.get("TMP") or str(Path.home()))
    return temp_dir / "codex_redteam_mode_states"

def _safe_session_key(session_id: str | None) -> str:
    raw = (session_id or "global").strip() or "global"
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", raw)
    return safe[:120] or "global"


def state_path(session_id: str | None = None) -> Path:
    return state_dir() / f"{_safe_session_key(session_id)}.json"


def load_state(session_id: str | None = None) -> RedTeamState:
    path = state_path(session_id)
    if not path.exists():
        return default_state(session_id)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        state = RedTeamState(**raw).normalized()
        if session_id and not state.session_id:
            state.session_id = session_id
        return state
    except Exception:
        return default_state(session_id)


def save_state(state: RedTeamState, session_id: str | None = None) -> None:
    state = state.normalized()
    if session_id:
        state.session_id = session_id
    state.last_changed = now_iso()
    directory = state_dir()
    directory.mkdir(parents=True, exist_ok=True)
    state_path(session_id or state.session_id or "global").write_text(json.dumps(asdict(state), ensure_ascii=False, indent=2), encoding="utf-8")


def reset_state(session_id: str | None = None) -> RedTeamState:
    state = default_state(session_id)
    save_state(state, session_id=session_id)
    return state
