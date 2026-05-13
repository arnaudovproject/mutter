---
name: workflow
description: Select and follow a workflow template from .mutter/workflows (feature, bugfix, refactor, review, migration, release).
---

# /mutter:workflow

`$ARGUMENTS` is the workflow name (without `.md`), e.g. `feature`, `bugfix`, `refactor`, `review`, `migration`, `release`.

## Steps

1. Read `.mutter/workflows/<name>.md` if it exists; otherwise offer to create from built-in skeleton in this skill’s repo template.
2. Set `.mutter/state/current.json` `active_workflow` to that name.
3. Execute steps **incrementally**—do not jump to implementation before plan/task steps when the workflow forbids it.

## Token rules

- Quote at most **8 lines** of the workflow file in chat; otherwise point to path.
