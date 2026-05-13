from __future__ import annotations


DEFAULT_WORKFLOW = ("recon", "strategy", "exploit-dev", "review", "reporting")


def recommended_workflow(start_phase: str = "recon") -> tuple[str, ...]:
    if start_phase not in DEFAULT_WORKFLOW:
        return DEFAULT_WORKFLOW
    idx = DEFAULT_WORKFLOW.index(start_phase)
    return DEFAULT_WORKFLOW[idx:]
