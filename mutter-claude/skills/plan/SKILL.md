---
name: plan
description: Produce a scoped implementation plan with affected files, risks, architecture/API/migration/testing impact and execution order.
---

# /mutter:plan

Planning input is **`$ARGUMENTS`** (free text goal).

## Preconditions

- Skim `.mutter/core/project.md`, `.mutter/architecture/overview.md`, and **only** index shards likely related (infer from keywords in `$ARGUMENTS`).
- Read `.mutter/state/current.json` for active task/workflow if set.

## Deliverable

Write a dated plan file under `.mutter/plans/` containing:

1. Goal restatement (one paragraph max)
2. **Affected files** (paths) grouped by domain
3. **Risks** (ranked) + mitigations
4. **Architecture impact** bullets (link to `architecture/*.md`)
5. **API / data migration impact** if any
6. **Testing strategy** (commands + what to assert)
7. **Execution order** (ordered checklist, each step verifiable)
8. **Definition of done / must-haves** — short list of mechanically checkable outcomes (commands to run, files that must exist, behaviors to assert). Prefer “lint passes on touched package” over vague “code quality OK”.
9. For **epic / multi-hour** scope: note work packages suitable for **`workers`** (explicit file caps per package, which packages may run read-only in parallel).

After writing the plan, optionally run **`python3 scripts/mutter.py validate-plan --plan .mutter/plans/<file>.md`** (from repo root) if `scripts/mutter.py` exists — catches missing Affected paths, **empty Testing/Verify fenced commands** (error), and thin Definition-of-done sections.

## Chat output

- Summarize plan in **≤15 bullets**; link to the plan file path.
- Set `.mutter/state/current.json` `active_plan` to the new plan filename.

## Token rules

- Do not inline whole architecture documents—reference paths.
