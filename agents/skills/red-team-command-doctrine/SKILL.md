---
name: red-team-command-doctrine
description: Compact global red-team doctrine. Use when offensive phase selection, anti-drift, evidence discipline, OPSEC-aware routing, or final gate verification are needed.
---

# Red Team Command Doctrine

## Purpose
This is a compact governance skill for offensive work. It routes into more specific red-team skills rather than replacing them.

## Phase order
1. recon
2. initial-access
3. web-exploitation
4. credential-access
5. privilege-escalation
6. post-exploitation
7. persistence-c2
8. lateral-movement
9. ad-operations
10. cloud-iam-abuse
11. reverse-loader-analysis
12. payload-weaponization
13. reporting

## Rules
- Identify the phase before acting.
- Prefer one low-noise viable path over broad noisy exploration.
- Keep evidence separate from assumptions.
- Avoid drift into architecture or blue-team planning unless explicitly requested.
- End with a concrete next step.

## Routing
- initial-access -> `initial-access-delivery`
- credential-access -> `credential-access-operations`
- post-exploitation -> `post-exploitation-playbook`
- persistence-c2 -> `persistence-and-c2`
- stealth / OPSEC -> `red-team-opsec`
- cloud-iam-abuse -> `cloud-iam-abuse`
- payload-weaponization -> `weaponization-and-payloads`
- reverse-loader-analysis -> `malware-loader-analysis`
