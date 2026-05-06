# Behavior Matrix

| State | Default | Doctrine Injection | Typical Use |
|---|---|---:|---|
| Normal mode | Yes | No | general work, coding, docs, browsing |
| Red-team mode | No, explicit only | Yes, lightweight | offensive work, exploitation, OPSEC-aware analysis |

## Notes
- Session start resets back to normal mode.
- Red-team mode persists only until you explicitly disable it.
- Hook output is intentionally compact to avoid context pollution.
