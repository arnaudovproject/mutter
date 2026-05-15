---
name: prd
description: Maintain the workspace Product Requirements Document at `.mutter/prd/PRD.md` (agent-facing product intent — goals, users, problems, scope — validated with `validate-prd`).
---

# /mutter:prd

Parse **`$ARGUMENTS`** as intent text.

This skill manages **your product’s** PRD under **`.mutter/prd/PRD.md`**. It is **not** the same file as repo-root **`SPEC.md`** (which describes the **Mutter** framework when working inside this repository).

## When to use

- Starting or refactoring **what** the team is building (stable context for agents).
- After roadmap or architecture shifts that change **product scope** — revise PRD in place (optional short **Revision log** table).
- Before **`/mutter:plan`** or **`/mutter:task create`** on ambiguous scope — align tasks/plans with PRD statements.

## Canonical location

- **`.mutter/prd/PRD.md`** — referenced by **`context-pack`** when present and checked by **`validate-prd`**.

## Workflow

1. Read **`.mutter/core/project.md`** and **`prd/README.md`** (orientation).
2. If **`PRD.md`** is missing or unrecoverably stale and the user wants a fresh scaffold: ensure **`python3 scripts/mutter.py prd-init`** has been run from repo root (creates `PRD.md` from **`.mutter/templates/PRD.md`** when available).
3. Create or update **`PRD.md`** using headings aligned with the template: **Overview**, **Goals**, **Problem statement**, **Users and personas**, **Scope**, **Functional requirements**, optional non-functional / integrations / open questions.
4. Prefer **links** to **`.mutter/architecture/`** for technical depth — avoid duplicating full architecture in the PRD.
5. After substantive edits, run **`python3 scripts/mutter.py validate-prd`** (optional **`--prd`** override).

## Relationship to other artifacts

| Artifact | Role |
|----------|------|
| **`prd/PRD.md`** | Product intent (“what / why”) — primary specification for agents executing tasks |
| **`roadmap/`** | Priorities over time — cross-link from Summary sections when useful |
| **`plans/`** | Scoped implementation — must not contradict PRD; update PRD first if intent shifts |
| **`architecture/`** | Technical boundaries (“how”) |

## Chat output

- Summarize deltas in **≤12 bullets**; link **`PRD.md`** path.
- Do not paste the entire PRD unless asked.

## Token rules

- Load PRD **once per session** when driving scope — refresh only after edits or clear drift.
