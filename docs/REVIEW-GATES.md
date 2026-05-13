# Review Gates

Artifacts produced during offensive task orchestration should pass through explicit gates.

## Gate order

1. syntax gate
2. logic gate
3. OPSEC gate

## Minimum expectations

- the artifact matches the chosen path
- target constraints are explicit
- success conditions are explicit
- risky noise is called out before delivery

## Recommended behavior

- `pass` only when the artifact is structurally sound
- `revise` when there are fixable issues
- `reject` when the path itself is unsound or too noisy
