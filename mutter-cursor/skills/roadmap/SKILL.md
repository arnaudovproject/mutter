---
name: roadmap
description: Maintain roadmap files under .mutter/roadmap — features, milestones, debt, releases — in small shards.
---

# /mutter:roadmap

Use **`$ARGUMENTS`** as the edit intent (e.g. “add milestone Q3”, “prioritize bug X”, “log tech debt for module Y”).

## Rules

- Never create one giant roadmap file; prefer dated or thematic shards (`2026-h2.md`, `debt-backend.md`).
- Cross-link to tasks in `.mutter/tasks/` when work is scheduled.
- After substantive edits, add a one-line entry to `.mutter/logs/roadmap.log`.

## Token rules

- In chat, return only the delta summary and file paths touched.
