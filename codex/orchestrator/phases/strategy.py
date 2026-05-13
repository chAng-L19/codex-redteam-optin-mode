from __future__ import annotations


def phase_contract() -> dict:
    return {
        "phase": "strategy",
        "input": ["recon_artifact"],
        "output": ["candidate_paths", "chosen_path", "assumptions", "required_validation", "evidence_refs"],
        "goal": "rank attack paths and choose one verifiable path before expansion",
    }
