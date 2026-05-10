from __future__ import annotations

from dataclasses import replace
from typing import Optional

from redteam_state import RedTeamState, load_state, reset_state, save_state


def load_runtime_state(session_id: str | None = None) -> RedTeamState:
    return load_state(session_id)


def save_runtime_state(state: RedTeamState, session_id: str | None = None) -> None:
    save_state(state, session_id)


def reset_runtime_state(session_id: str | None = None) -> RedTeamState:
    return reset_state(session_id)


def update_mode(state: RedTeamState, mode: str, phase: Optional[str] = None, session_id: str | None = None) -> RedTeamState:
    state = replace(state, mode=mode, phase=phase or state.phase)
    save_runtime_state(state, session_id=session_id)
    return state
