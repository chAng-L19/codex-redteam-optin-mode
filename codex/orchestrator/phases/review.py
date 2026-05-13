from __future__ import annotations


def phase_contract() -> dict:
    return {
        "phase": "review",
        "input": ["artifact_candidate"],
        "output": ["status", "syntax_issues", "logic_issues", "opsec_issues", "next_action"],
        "goal": "reject or revise artifacts that fail syntax, logic, or OPSEC gates before delivery",
    }
