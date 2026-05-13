from __future__ import annotations


def phase_contract() -> dict:
    return {
        "phase": "recon",
        "input": ["scan_output", "target_scope"],
        "output": ["hosts", "ports", "services", "os_guess", "evidence_refs", "confidence"],
        "goal": "extract environment topology and keep only evidence-backed facts",
    }
