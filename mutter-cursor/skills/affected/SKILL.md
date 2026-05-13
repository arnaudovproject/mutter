---
name: affected
description: List affected files and domains for a proposed change using index shards and task/plan linkage — minimal reads.
---

# /mutter:affected

`$ARGUMENTS` describes the change or references an active plan/task id.

## Steps

1. Resolve domains/files from `.mutter/index/*.json` and any active `.mutter/state/current.json` pointers.
2. Output structured list: domains → files → related tests (paths).
3. Save a machine-readable fragment under `.mutter/plans/<slug>-affected.json` when the user will reuse it.

## Token rules

- Chat: compact bullet groups, max ~25 paths; spillover only in the saved JSON.
