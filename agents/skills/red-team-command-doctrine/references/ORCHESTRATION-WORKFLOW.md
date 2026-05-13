# Orchestration Workflow

Use structured orchestration when the task is too large for a single phase hint.

## Stages

1. `recon` -> produce a `ReconArtifact`
2. `strategy` -> produce a `StrategyArtifact`
3. `exploit-dev` -> produce an `ExploitArtifact`
4. `review` -> produce a `ReviewArtifact`
5. `reporting` -> deliver the final operator-facing output

## Rules

- pass structured artifacts between stages
- do not pass hidden chain-of-thought text as the primary handoff format
- do not skip review for generated artifacts
- keep evidence refs attached to every stage that depends on environmental claims
