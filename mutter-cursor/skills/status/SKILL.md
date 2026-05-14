---
name: status
description: Task checklist dashboard — markdown table with ✓/○ progress, optional single-task drill-down; pairs with execution_progress in state.
---

# /mutter:status

Show **how many checklist steps are done** across Mutter task files (and optional **Acceptance** counts). This complements `python3 scripts/mutter.py status`, which dumps raw `state/current.json`.

## Parse **`$ARGUMENTS`**

- **Empty** (or only whitespace) → all tasks in the selected buckets (default: every bucket under `.mutter/tasks/`).
- **One identifier** (e.g. `task-01`, `my-feature.md`, `.mutter/tasks/current/foo.md`) → that task only, plus a **Steps detail** list.

## What to run (repository root with `.mutter/`)

Always prefer the CLI so numbers stay consistent with CI:

```bash
python3 scripts/mutter.py tasks-status
python3 scripts/mutter.py tasks-status --task <slug-or-path>
```

Optional: `python3 scripts/mutter.py status` when you need **active_task**, **active_plan**, or **execution_progress** JSON from disk.

## How to present results

1. **Echo the CLI output** (it is already Markdown): table columns **Bucket | File | Title | Meta | Steps | Acceptance | Progress** where **Progress** uses **✓** (done) and **○** (open) for each step in the **Steps** section.
2. If the user asked for a **single task**, keep the table row **and** the **Steps detail** block the CLI prints.
3. Mention **execution_progress** from `state/current.json` only if it is fresh — it updates when someone runs **`sync-task-progress`** after editing checklists (see **`task`** skill).

## Rules

- **Disk is truth** for counts: always derive from task `.md` checklists via `tasks-status`, not from chat memory.
- Do not paste entire task bodies unless the user asked for a deep read; the table + step lines are enough.
