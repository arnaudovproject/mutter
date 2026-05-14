---
name: workflow
description: Select and follow a workflow template from .mutter/workflows (feature, bugfix, refactor, review, migration, release).
---

# /mutter:workflow

`$ARGUMENTS` is the workflow name (without `.md`), e.g. `feature`, `bugfix`, `refactor`, `review`, `migration`, `release`.

## Idempotent re-runs

If **`active_workflow`** in **`state/current.json`** already matches **`$ARGUMENTS`** and the workflow’s checklist for the current phase is unchanged, **do not restart from step 1**—resume at the next unchecked item. Only re-read the full workflow when the user changed the file or switched workflows.

## Steps

1. Read `.mutter/workflows/<name>.md` if it exists; otherwise offer to create from built-in skeleton in this skill’s repo template.
2. Set `.mutter/state/current.json` `active_workflow` to that name.
3. Execute steps **incrementally**—do not jump to implementation before plan/task steps when the workflow forbids it.

## Token rules

- Quote at most **8 lines** of the workflow file in chat; otherwise point to path.
