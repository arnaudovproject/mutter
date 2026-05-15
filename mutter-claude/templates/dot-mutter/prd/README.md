# Product requirements (PRD)

This folder holds the **workspace Product Requirements Document** for *your* product or initiative (not the Mutter framework itself).

## Canonical file

- **`PRD.md`** — stable path agents and scripts can rely on: `.mutter/prd/PRD.md`.

## How this relates to other `.mutter/` artifacts

| Artifact | Role |
|----------|------|
| **`prd/PRD.md`** | Product intent: goals, users, problems, scope. Primary **agent-facing specification** for “what” and “why”. |
| **`roadmap/`** | Time-based themes, milestones, and sequencing (“when” / priorities). Update roadmap when priorities shift; keep PRD aligned when scope changes. |
| **`architecture/`** | Technical shape and boundaries (“how” the system works). Link from PRD when requirements imply architectural constraints. |
| **`plans/`** | Scoped execution plan for one change. Plans should not contradict the PRD; prefer updating PRD first if product intent changed. |

## Bootstrap

From the repository root (when `scripts/mutter.py` exists):

```bash
python3 scripts/mutter.py prd-init
python3 scripts/mutter.py validate-prd
```

Use **`prd-init --force`** only when you intentionally replace `PRD.md` from the template.

## Maintenance

Treat **`PRD.md` as living documentation**: after meaningful roadmap or architecture shifts, revise the PRD in place (append a short **Revision** stanza with date + bullets if helpful). Avoid duplicating long architecture text—link paths under `.mutter/architecture/` instead.
