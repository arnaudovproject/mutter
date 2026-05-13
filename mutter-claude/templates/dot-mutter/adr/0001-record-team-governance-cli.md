# ADR 0001: Record team-scale governance in Mutter CLI

Status: accepted

## Context

Large teams need lightweight checks before AI-assisted edits: readiness (`preflight`), path risk, secrets, boundaries, and compact context bundles.

## Decision

Extend `scripts/mutter.py` with governance subcommands (`preflight`, `context-pack`, `risk-check`, `pr-template`, `suggest-tests`, `check-boundaries`, `scan-secrets`, ADR validation, migration hints, TODO index, large-change guard). Ship example config under `.mutter/testing/commands.json`, `.mutter/boundaries.json`, `ownership/`, `quality-gates/`, and `adr/`.

## Consequences

- Consumers get disk-first “AI engineering governance” without a separate runtime.
- `Verify` / plan **Testing** sections must use fenced command blocks (enforced as errors) to reduce fake “done”.
