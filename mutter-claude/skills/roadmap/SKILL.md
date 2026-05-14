---
name: roadmap
description: Maintain roadmap shards under .mutter/roadmap; empty args = align roadmap with architecture signals first.
---

# /mutter:roadmap

Use **`$ARGUMENTS`** as the edit intent (e.g. “add milestone Q3”, “prioritize bug X”, “log tech debt for module Y”).

## Idempotent re-runs

**Read the relevant roadmap shard(s)** first. If the requested change is **already present** (same milestone text, same debt line), **report paths and “already recorded”**—do not append duplicates. For edits, **patch the smallest section** that needs to change; remove completed items when the user confirms they shipped.

## Empty or vague arguments

If **`$ARGUMENTS`** is empty, only “roadmap”, or otherwise gives **no concrete edit intent**:

1. **Inventory** `.mutter/roadmap/` (list shards; read titles / first sections only).
2. **Search architecture for grounding:** at minimum skim `.mutter/architecture/overview.md`, `.mutter/architecture/decisions.md` (recent tail), and any domain shards named by roadmap hints or `ownership/modules.md`.
3. Return a **short gap analysis**: what roadmap promises vs what architecture says exists, what is missing, and **proposed next edits** (bullet list + suggested filenames under `roadmap/`). Apply edits only if the user confirms.

## Rules

- Never create one giant roadmap file; prefer dated or thematic shards (`2026-h2.md`, `debt-backend.md`).
- Cross-link to tasks in `.mutter/tasks/` when work is scheduled.
- After substantive edits, add a one-line entry to `.mutter/logs/roadmap.log`.

## Token rules

- In chat, return only the delta summary and file paths touched.
