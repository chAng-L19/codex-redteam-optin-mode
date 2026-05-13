from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "codex") not in sys.path:
    sys.path.insert(0, str(ROOT / "codex"))

from orchestrator import (  # noqa: E402
    ExploitArtifact,
    ReconArtifact,
    ReviewArtifact,
    StrategyArtifact,
    StrategyPath,
    artifact_to_dict,
    next_allowed_phases,
    postex_gate,
    recon_gate,
    recommended_workflow,
    review_gate,
    strategy_gate,
    transition_allowed,
)


class OrchestratorTests(unittest.TestCase):
    def test_workflow_and_transitions(self) -> None:
        self.assertEqual(recommended_workflow(), ("recon", "strategy", "exploit-dev", "review", "reporting"))
        self.assertTrue(transition_allowed("recon", "strategy"))
        self.assertFalse(transition_allowed("recon", "review"))
        self.assertEqual(next_allowed_phases("review"), ("exploit-dev", "reporting"))

    def test_recon_and_strategy_gates(self) -> None:
        recon = ReconArtifact(
            scope="lab",
            hosts=["10.0.0.5"],
            ports=["445/tcp"],
            services=["smb"],
            evidence_refs=["scan.xml"],
            confidence=0.8,
        )
        self.assertTrue(recon_gate(recon).ok)

        strategy = StrategyArtifact(
            candidate_paths=[StrategyPath(name="smb-weak-password", rationale="service + creds path")],
            chosen_path="smb-weak-password",
            evidence_refs=["scan.xml"],
        )
        self.assertTrue(strategy_gate(strategy).ok)

    def test_exploit_review_and_postex_gates(self) -> None:
        exploit = ExploitArtifact(
            path_name="smb-weak-password",
            target_constraints=["Windows host", "SMB reachable"],
            delivery_format="scaffold",
            success_conditions=["authenticated access confirmed"],
        )
        self.assertEqual(artifact_to_dict(exploit)["path_name"], "smb-weak-password")

        review = ReviewArtifact(status="pass", next_action="deliver scaffold")
        self.assertTrue(review_gate(review).ok)
        self.assertTrue(postex_gate("postex", foothold_present=True).ok)
        self.assertFalse(postex_gate("general", foothold_present=False).ok)
