from __future__ import annotations


TRANSITIONS: dict[str, tuple[str, ...]] = {
    "recon": ("strategy",),
    "strategy": ("exploit-dev", "reporting"),
    "exploit-dev": ("review",),
    "review": ("exploit-dev", "reporting"),
    "reporting": (),
}


def next_allowed_phases(phase: str) -> tuple[str, ...]:
    return TRANSITIONS.get(phase, ())


def transition_allowed(current: str, nxt: str) -> bool:
    return nxt in next_allowed_phases(current)
