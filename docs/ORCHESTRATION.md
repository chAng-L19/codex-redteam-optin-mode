# Structured Offensive Task Orchestration

This project now includes a **lightweight orchestration layer** for larger offensive tasks.

It is intentionally **not** an always-on auto-exploitation engine.

## Design goals

- keep runtime hooks lightweight
- keep phase routing separate from heavy task planning
- pass **structured artifacts**, not giant free-form prompt blobs
- enforce review gates before artifact delivery

## Workflow

1. `recon`
2. `strategy`
3. `exploit-dev`
4. `review`
5. `reporting`

## What it is for

- planning large offensive tasks
- structuring operator reasoning
- keeping evidence, assumptions, and outputs separated
- making review and rollback easier

## What it is not

- not a RAG layer
- not a live exploit feed consumer
- not an always-on agent swarm
- not a replacement for operator judgment
