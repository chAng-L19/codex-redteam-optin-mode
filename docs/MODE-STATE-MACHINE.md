# Mode State Machine

See:

- `agents/skills/red-team-command-doctrine/references/MODE-STATE-MACHINE.md`

Key runtime invariant:

- session start resets only the **current session**
- one session does not overwrite another session's mode state
