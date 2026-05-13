---
name: task
description: Mutter task system — create, update, split, or execute tasks under .mutter/tasks with incremental safe steps.
---

# /mutter:task

Parse **`$ARGUMENTS`** as a subcommand and payload.

## Subcommands (prefix first token)

- `create ...` — new markdown task in `.mutter/tasks/current/` with status, numbered steps, affected domains, affected files, **acceptance checks** (observable behavior, required artifacts, or commands), and verification commands. **Skeleton:** copy `.mutter/templates/TASK.md` (from bootstrap template) to `tasks/current/<slug>.md`, replace placeholders, keep **Acceptance** and **Verify** concrete before starting long work.
- `update <task-file> ...` — patch sections (status, steps, notes) without rewriting unrelated tasks.
- `split <task-file> ...` — break an oversized task into multiple linked tasks; mark parent `split`.
- `execute <task-file>` — run the **next** unchecked step only: read listed files + index shards, then follow `safe-edit` discipline for edits.

## Automation (scripts)

When this repository (or a consumer repo that vendors `scripts/mutter.py`) is on disk, run from the **repository root** that contains `.mutter/`:

**Validation**

- `python3 scripts/mutter.py validate-task` — checks the task in `.mutter/state/current.json` (`active_task`), or pass `--task .mutter/tasks/current/<file>.md`.
- `python3 scripts/mutter.py validate-tasks` — scans `.mutter/tasks/{current,planned,blocked}/` for structural issues; add `--deep` to warn on missing **Read:** paths in Steps; `--warnings-as-errors` for strict CI.
- `python3 scripts/mutter.py validate-plan` / **`validate-plans`** — same idea for `.mutter/plans/*.md` (Affected paths, **Testing/Verify fenced commands required**, Definition of done); `validate-plan` uses `active_plan` when `--plan` is omitted.
- `python3 scripts/mutter.py validate-adr` — checks `.mutter/adr/*.md` for Status + Context/Decision/Consequences sections.
- `python3 scripts/mutter.py validate-quality-gate --type <bugfix|feature|refactor|migration|security>` — ensures `.mutter/quality-gates/<type>.md` exists and has checklist structure.
- `python3 scripts/mutter.py validate-migrations` — if migration-like paths changed in git diff, requires rollback/backup/backward-compat language in the active task/plan.

**State & scan**

- `python3 scripts/mutter.py status` — prints `state/current.json` and short previews of the resolved active task and plan when set.
- `python3 scripts/mutter.py scan-state` — lists `changed_files` from `.mutter/metadata/scan-state.json` when present.

**Team-scale governance (large repos)**

- `python3 scripts/mutter.py preflight` — readiness: optional `--require-active-task`, `--check-acceptance-verify`, `--require-plan-for-large`, dirty git, missing scan-state.
- `python3 scripts/mutter.py context-pack` — single Markdown bundle: state, task/plan excerpts, changed paths, ADRs, `ownership/modules.md`, `architecture/decisions.md` tail; `--out PATH` to write a file.
- `python3 scripts/mutter.py risk-check` — scores paths **LOW/MEDIUM/HIGH** (default input: git diff vs `HEAD`, else scan-state); `--paths` to override.
- `python3 scripts/mutter.py suggest-tests` — uses `.mutter/testing/commands.json` to propose commands for changed paths (`--from-git` / `--paths`).
- `python3 scripts/mutter.py pr-template` — PR Markdown skeleton from active task/plan + git paths + suggested tests.
- `python3 scripts/mutter.py report-change` — post-change Markdown skeleton for PR bodies or logs.
- `python3 scripts/mutter.py check-boundaries` — optional `.mutter/boundaries.json` (or `.yml` with PyYAML) + heuristic forbidden-import scan on changed files.
- `python3 scripts/mutter.py scan-secrets` — lightweight obvious-secret patterns (best-effort; use real secret scanners in CI for guarantees).
- `python3 scripts/mutter.py scan-todos` — writes TODO/FIXME/HACK index to `.mutter/metadata/todos.json`.
- `python3 scripts/mutter.py guard-large-change` — fails when diff is huge or touches enough **HIGH**-risk paths without `active_plan` set.

**Plugin / CI**

- `python3 scripts/mutter.py check-skill-refs` — ensures relative `.md` links in `mutter-claude/skills` and `mutter-cursor/skills` resolve (plugin development).
- `python3 scripts/mutter.py ci --check-cursor-sync` — runs refs + task + plan validation + `sync_cursor_skills.py` and fails if Cursor skills drift from git (CI / maintainers). Add **`--with-governance`** to also run `validate-adr`, `scan-secrets`, and `guard-large-change`.

Prefer running **`validate-task` before marking work done** so Acceptance, Verify (real fenced shell commands), and Affected paths are mechanically consistent. Use **`validate-plan`** after large `/mutter:plan` writes. For a new session on a risky change, run **`context-pack`** (or `preflight`) first.

## Rules

- **One-window rule:** each step must be doable with the step’s listed files + small index/context slice in roughly one model turn. If the goal needs unbounded exploration, **`split`** first or route exploration through **`workers`** with a capped path list.
- Never attempt all steps of a large task in one response.
- After each executed step, update the task file, append a line to `.mutter/logs/tasks.log` with timestamp + step id.
- Update `.mutter/state/current.json` `active_task` when starting execution.

## Epics and multiple agents

For goals spanning many files or sessions, use **`workers`** after splitting: one task (or step) per worker brief, state on disk between dispatches, serialize overlapping edits.

## Token rules

- When displaying a task in chat, show **title, status, current step only** unless user asks for full file.

## Stuck handling

- If the same failure pattern repeats twice with no new evidence, **stop**: append a short note to the task, set `blocked` or split into a smaller step, and log under `.mutter/logs/` instead of burning context re-trying blindly.
