from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReconArtifact:
    scope: str = ""
    hosts: list[str] = field(default_factory=list)
    ports: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    os_guess: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class StrategyPath:
    name: str
    rationale: str
    required_validation: list[str] = field(default_factory=list)
    expected_noise: str = "balanced"
    prerequisites: list[str] = field(default_factory=list)


@dataclass
class StrategyArtifact:
    source_phase: str = "recon"
    candidate_paths: list[StrategyPath] = field(default_factory=list)
    chosen_path: str = ""
    assumptions: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)


@dataclass
class ExploitArtifact:
    path_name: str = ""
    target_constraints: list[str] = field(default_factory=list)
    delivery_format: str = ""
    dependencies: list[str] = field(default_factory=list)
    success_conditions: list[str] = field(default_factory=list)
    opsec_notes: list[str] = field(default_factory=list)


@dataclass
class ReviewArtifact:
    status: str = "revise"
    syntax_issues: list[str] = field(default_factory=list)
    logic_issues: list[str] = field(default_factory=list)
    opsec_issues: list[str] = field(default_factory=list)
    next_action: str = ""
