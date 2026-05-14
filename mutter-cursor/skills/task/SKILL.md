---
name: task
description: Mutter task system — create (from roadmap when bare), update, split, execute one-by-one with progress sync, or run the whole current queue.
---

# /mutter:task

Parse **`$ARGUMENTS`** as a subcommand and payload. **Progress discipline:** whenever you finish an **execute** step (checkbox ticked in the task file), run **`python3 scripts/mutter.py sync-task-progress`** for that task so `.mutter/state/current.json` → **`execution_progress`** stays accurate, and keep appending **`.mutter/logs/tasks.log`**.

## Step completion messaging (required)

After **each** step you mark done, output a **short progress line** for that task, e.g. **`Steps 2/5 done; Acceptance 1/3`** (derive counts the same way as **`python3 scripts/mutter.py tasks-status --task <slug>`**—run that command if you want a guaranteed consistent count). Then **ask** whether to continue with the next step if any checklists remain.

## Bare invocation (no subcommand)

If **`$ARGUMENTS`** is empty or only whitespace:

1. Treat it as **execute the whole queue**: consider every `*.md` under `.mutter/tasks/current/` (except `README.md`) in **lexicographic order**.
2. **Skip** a file when **Meta `Status:` is `done`** *or* every top-level **Steps** checkbox is already `[x]` (no pending `- [ ]` step lines at the same markdown level as the template’s steps). Completed work **stays**; only tasks with remaining steps run.
3. For **each** remaining task, run the same loop as **`execute`** (one step → update disk → log → **sync-task-progress** → **validate-task** if appropriate).
4. After **each** step inside a task, if more steps remain in **that** file, **ask the user** whether to continue (unless they already asked for unattended execution).

## Subcommands (prefix first token)

- `create ...` — new markdown task in `.mutter/tasks/current/`. **Skeleton:** copy `.mutter/templates/TASK.md` to `tasks/current/<slug>.md`, replace placeholders, keep **Acceptance** and **Verify** concrete before starting long work. If the payload is empty or only `create` (no title or scope text), **first read every shard under `.mutter/roadmap/`** (and skim `.mutter/architecture/overview.md` + `decisions.md` tail for constraints), then **materialize tasks** from open roadmap bullets / milestones (one file per coherent unit of work, cross-link roadmap paths in each task’s Summary).
- `update <task-file> ...` — patch sections (status, steps, notes) without rewriting unrelated tasks.
- `split <task-file> ...` — break an oversized task into multiple linked tasks; mark parent `split`.
- `execute` — behavior depends on the rest of **`$ARGUMENTS`**:
  - **`execute` alone** — same as **Bare invocation** (whole **current** queue), **skipping** tasks that are already **done** or have **no remaining Steps checklists** (see Bare invocation).
  - **`execute <task>`** — `<task>` may be a path, `.mutter/tasks/current/foo.md`, or a **slug** like `task-01` / `foo` (resolved like the CLI). If that task is **already complete**, report **`tasks-status --task`** and stop unless the user wants a reopen. Set **`active_task`** in `state/current.json`, then repeat: run the **next** unchecked top-level step only → edit with **`safe-edit`** discipline → tick the step → append **`tasks.log`** → **`sync-task-progress`** → print **Steps N/M** line → if **more** unchecked steps remain, **ask** the user to proceed; if **no** steps left, move on only when doing a multi-task queue, else stop.

## Automation (scripts)

When this repository (or a consumer repo that vendors `scripts/mutter.py`) is on disk, run from the **repository root** that contains `.mutter/`:

**Validation**

- `python3 scripts/mutter.py validate-task` — checks the task in `.mutter/state/current.json` (`active_task`), or pass `--task .mutter/tasks/current/<file>.md`.
- `python3 scripts/mutter.py validate-tasks` — scans `.mutter/tasks/{current,planned,blocked}/` for structural issues; add `--deep` to warn on missing **Read:** paths in Steps; `--warnings-as-errors` for strict CI.
- `python3 scripts/mutter.py validate-plan` / **`validate-plans`** — same idea for `.mutter/plans/*.md` (Affected paths, **Testing/Verify fenced commands required**, Definition of done); `validate-plan` uses `active_plan` when `--plan` is omitted.
- `python3 scripts/mutter.py validate-adr` — checks `.mutter/adr/*.md` for Status + Context/Decision/Consequences sections.
- `python3 scripts/mutter.py validate-quality-gate --type <bugfix|feature|refactor|migration|security>` — ensures `.mutter/quality-gates/<type>.md` exists and has checklist structure.
- `python3 scripts/mutter.py validate-migrations` — if migration-like paths changed in git diff, requires rollback/backup/backward-compat language in the active task/plan.

**State, scan, and task progress**

- `python3 scripts/mutter.py status` — prints `state/current.json` and short previews of the resolved active task and plan when set.
- **`python3 scripts/mutter.py tasks-status`** — Markdown table of **Steps** / **Acceptance** checklist progress for all tasks (or `--task <slug>` for one). Use with **`/mutter:status`**.
- **`python3 scripts/mutter.py sync-task-progress`** — refreshes **`execution_progress`** in `state/current.json` from the resolved task’s checklists (pass `--task` or rely on **`active_task`**).
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
- Never attempt all steps of a large task in **one model response** unless the user explicitly asked for unattended execution.
- After each executed step, update the task file, append a line to `.mutter/logs/tasks.log` with timestamp + step id, run **`sync-task-progress`**, and keep **`active_task`** pointing at the file you are executing.

## Epics and multiple agents

For goals spanning many files or sessions, use **`workers`** after splitting: one task (or step) per worker brief, state on disk between dispatches, serialize overlapping edits.

## Token rules

- When displaying a task in chat, show **title, status, current step only** unless user asks for full file.

## Stuck handling

- If the same failure pattern repeats twice with no new evidence, **stop**: append a short note to the task, set `blocked` or split into a smaller step, and log under `.mutter/logs/` instead of burning context re-trying blindly.
