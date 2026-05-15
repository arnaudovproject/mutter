---
name: task
description: Mutter task system — create, update, split, execute (with plans + roadmap when no exact path); progress sync; or run the whole current queue.
---

# /mutter:task

Parse **`$ARGUMENTS`** as a subcommand and payload. **Progress discipline:** whenever you finish an **execute** step (checkbox ticked in the task file), run **`python3 scripts/mutter.py sync-task-progress`** for that task so `.mutter/state/current.json` → **`execution_progress`** stays accurate, and keep appending **`.mutter/logs/tasks.log`**.

## Location resolution (when no exact task path)

Task bodies live under **`.mutter/tasks/{current,planned,blocked,completed}/`** (default bucket for new work: **`current/`**). Whenever **`create`**, **`update`**, **`split`**, or **`execute`** is invoked **without** a resolvable task path or slug:

1. **Explicit path wins** — If the user (or payload) names a **repo-relative** path to a file under **`.mutter/`** (including **`tasks/planned/…`**, **`tasks/blocked/…`**, or another shard they point at), use that as the task file target. Do **not** ignore a supplied path to chase roadmap/plans instead.
2. **State hints** — Read **`.mutter/state/current.json`**. If **`active_task`** is set and no task file was named, use it for **`update`**, **`split`**, or a **single-task** **`execute`**. If **`active_plan`** is set, open that plan for goal text, execution order, and affected paths when shaping or running work.
3. **Product intent** — When **`.mutter/prd/PRD.md`** exists and location/plans/tasks are ambiguous, skim PRD **Goals / Functional requirements / Scope** before inventing scope (prefer linking tasks to PRD sections when helpful).
4. **Plans (always consult when location is missing)** — Inventory **`.mutter/plans/*.md`** (skip `README.md`): skim **titles / goal lines / first heading** of each. Prefer matching the user’s words to a plan; set the task’s **Meta → Active plan (optional)** and cite the plan path in **Summary** when there is a clear fit. If **`validate-plan`** / **`status`** already surfaced an active plan, prefer that file first.
5. **Roadmap (same)** — Inventory **`.mutter/roadmap/`** shards (titles, open milestones, unchecked bullets). Use them to name work, **Summary** scope, and cross-links—**including** for **`create …`** when the user gave a title or body but did not say where the work came from (tie the task to roadmap bullets that overlap).
6. **Disambiguation** — If **multiple** tasks or plans match keywords, print **candidate paths** (task `.md` + plan + roadmap shard) in **≤10 lines** and ask **one** clarifying question. If **none** match, say so and suggest **`tasks-status`**, **`create`**, or pointing to a plan section.

Token rule: for steps 4–5, read **only** headings / first sections of each plan or roadmap file unless one file clearly matches—then read that file a bit deeper.

## Session hooks (scripts) — run when executing or continuing

If **`scripts/mutter.py`** exists at the **repository root**:

1. **Resume / “continue” / start execute:** **`python3 scripts/mutter.py status`** then **`python3 scripts/mutter.py tasks-status --task <slug>`** (or full table) so the next turn opens the right file with correct counts.
2. **Cold onboarding (once per workspace or new agent thread):** **`python3 scripts/mutter.py agent-cadence --out .mutter/context/agent-cadence.md`** — canonical map of *when* to run each CLI vs skill (keeps later turns from improvising).

## Task file shape (for small **execute** / **continue** slices)

When **creating** or **splitting** tasks:

- **One** top-level **Steps** `- [ ]` item = **one** agent turn (one **continue**) unless the user explicitly asked for unattended execution.
- Each step’s **Read:** line must list **every** path (or index **shard + keys**) needed for that step — no “read the codebase”.
- Use **nested bullets without checkboxes** for sub-notes only; anything that needs verification gets its **own** top-level step or a **child task** via **`split`**.

## Reuse and consolidation

- Before adding **new** modules, helpers, API surfaces, or UI patterns, search for existing implementations (paths already under **Affected**, relevant index shards, packages referenced from PRD/architecture).
- Prefer **extending or calling shared code** over duplicating logic unless the task documents why divergence is required.
- When consolidating or reusing, list **all** impacted paths in **Affected** and call out shared entry points in **Steps** so validators and reviewers see the reuse explicitly.

## Step completion messaging (required)

After **each** step you mark done (checkbox ticked, log line, **`sync-task-progress`**): output a **short progress line** for that task, e.g. **`Steps 2/5 done; Acceptance 1/3`** (derive counts the same way as **`python3 scripts/mutter.py tasks-status --task <slug>`**—run that command if you want a guaranteed consistent count). Then run **§ Session context checkpoint** below. Only after that, if more **Steps** remain, **ask** whether to continue — **unless** the user already asked for unattended execution **and** the checkpoint shows **≤ ~40%** usage (or they confirmed “ok / low / under 40” in the same turn).

## Session context checkpoint (after each completed step — all harnesses)

Scope: **only after a task step is fully finished** (disk + sync done). **Never** interrupt mid-step because context crossed a threshold.

Agents **usually cannot read** the host UI’s context meter (Cursor’s %, Claude Code usage, Codex, OpenCode, etc.). **Ask the user** for the approximate **session / context window fill %** (or a one-word band: “low / medium / high”). If the product exposes usage in-system and you truly have a number, you may use it — otherwise rely on the user.

1. **≤ ~40%** — one line acknowledging the % (or band), then proceed with the usual “continue next step?” flow if steps remain.
2. **> ~40%** (or unknown / “high” when they cannot read the meter) — treat as **elevated risk**. Present a **clear choice**:
   - **Recommended (default):** Start a **new agent session** (fresh thread / chat). In that session: **`python3 scripts/mutter.py status`** → **`python3 scripts/mutter.py context-pack --out .mutter/context/session-pack.md`** → open **only** that pack + the active task file + the **next** unchecked **Read:** paths → continue with the **next** step. State that **doing nothing / “yes” / Enter** means this path.
   - **Opt-out:** Continue in **this** session only if the user **explicitly** says so (e.g. “stay here”, “continue in this chat”), with a one-line warning that quality may drop.

3. **Unattended execution:** Still **one step per model response**. You **must not** skip the checkpoint: end the turn with the **% question + default-new-session** offer when usage is unknown or high. Do **not** silently chain another step in the same reply after a heavy step.

Harness hints for the user (when they do not know where to look): **Cursor** — context / usage indicator in the chat UI; **Claude Code** — usage / limit cues in the product chrome; **Codex / OpenCode** — whatever the environment shows for token or context consumption.

## Bare invocation (no subcommand)

If **`$ARGUMENTS`** is empty or only whitespace:

1. If **`.mutter/tasks/current/`** has **no** actionable task `*.md` (only `README.md` or empty), run **§ Location resolution** steps 3–4 and tell the user **open plan / roadmap items** that could become **`create`** targets—do not treat an empty queue as “nothing to do” without checking.
2. Treat it as **execute the whole queue**: consider every `*.md` under `.mutter/tasks/current/` (except `README.md`) in **lexicographic order**.
3. **Skip** a file when **Meta `Status:` is `done`** *or* every top-level **Steps** checkbox is already `[x]` (no pending `- [ ]` step lines at the same markdown level as the template’s steps). Completed work **stays**; only tasks with remaining steps run.
4. For **each** remaining task, run the same loop as **`execute`** (one step → update disk → log → **sync-task-progress** → **§ Session context checkpoint** → **validate-task** if appropriate).
5. After **each** step inside a task, apply **§ Session context checkpoint**, then if more steps remain in **that** file, **ask the user** whether to continue (unless they already asked for unattended execution **and** checkpoint cleared as **≤ ~40%** or equivalent).

## Subcommands (prefix first token)

- `create ...` — new markdown task in **`.mutter/tasks/current/`** (unless the user names another **`.mutter/tasks/<bucket>/`** path explicitly). **Skeleton:** copy `.mutter/templates/TASK.md` to `tasks/current/<slug>.md`, replace placeholders, keep **Acceptance** and **Verify** concrete before starting long work. **If the payload is empty or only `create`** (no title or scope text): read every shard under **`.mutter/roadmap/`** (and skim **`.mutter/architecture/overview.md`** + **`decisions.md`** tail), then **materialize tasks** from open roadmap bullets / milestones (one file per coherent unit, cross-link roadmap paths in each **Summary**). **If the user gave a title or scope but no plan/roadmap pointer:** still run **§ Location resolution** steps 3–4 and set **Active plan** / roadmap cross-links when a match exists.
- `update ...` — patch sections (status, steps, notes) without rewriting unrelated tasks. Prefer **`update <task-file> ...`** where `<task-file>` is under **`.mutter/tasks/`**. **If `<task-file>` is missing:** resolve the target via **§ Location resolution** (`active_task` → keyword match across **`tasks/{current,planned,blocked}/`** → phrases in **`active_plan`** or other plan headings).
- `split ...` — break an oversized task into multiple linked tasks; mark parent **`split`**. **If the parent task file is omitted:** resolve it the same way as **`update`** (§ Location resolution).
- `execute` — behavior depends on the rest of **`$ARGUMENTS`**:
  - **`execute` alone** (nothing after `execute`) — same as **Bare invocation** (whole **current** queue), **skipping** tasks that are already **done** or have **no remaining Steps checklists** (see Bare invocation).
  - **`execute <task>`** where `<task>` is a path, **`.mutter/tasks/...`**, or a **slug** — same as today: resolve like the CLI, set **`active_task`**, one step per loop. If that task is **already complete**, report **`tasks-status --task`** and stop unless the user wants a reopen.
  - **`execute <free text>`** where `<free text>` is **not** a path or known slug — treat it as a **label**: search **`tasks/{current,planned,blocked}/`** titles and first headings, then **plan** titles and **roadmap** bullets (§ Location resolution). If **exactly one** task file matches, use it. If **zero**, report no match and suggest **`create`** or an explicit path. If **many**, list candidates and ask **one** question.

## Automation (scripts)

When this repository (or a consumer repo that vendors `scripts/mutter.py`) is on disk, run from the **repository root** that contains `.mutter/`:

**Validation**

- `python3 scripts/mutter.py validate-task` — checks the task in `.mutter/state/current.json` (`active_task`), or pass `--task .mutter/tasks/current/<file>.md`.
- `python3 scripts/mutter.py validate-tasks` — scans `.mutter/tasks/{current,planned,blocked}/` for structural issues; add `--deep` to warn on missing **Read:** paths in Steps; `--warnings-as-errors` for strict CI.
- `python3 scripts/mutter.py validate-plan` / **`validate-plans`** — same idea for `.mutter/plans/*.md` (Affected paths, **Testing/Verify fenced commands required**, Definition of done); `validate-plan` uses `active_plan` when `--plan` is omitted.
- `python3 scripts/mutter.py validate-adr` — checks `.mutter/adr/*.md` for Status + Context/Decision/Consequences sections.
- `python3 scripts/mutter.py validate-quality-gate --type <bugfix|feature|refactor|migration|security>` — ensures `.mutter/quality-gates/<type>.md` exists and has checklist structure.
- `python3 scripts/mutter.py validate-prd` — checks `.mutter/prd/PRD.md` (Overview/Goals/Problem/Users/Functional requirements); optional **`--prd`**
- `python3 scripts/mutter.py prd-init` — scaffold **`PRD.md`** from template when missing (**`--force`** overwrites)

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

Prefer running **`validate-task` before marking work done** so Acceptance, Verify (real fenced shell commands), and Affected paths are mechanically consistent. Use **`validate-plan`** after large `/mutter:plan` writes. For a new session on a risky change, run **`context-pack`** (or `preflight`) first. Full phase → CLI map: **`python3 scripts/mutter.py agent-cadence`**.

## Rules

- **One-window rule:** each step must be doable with the step’s listed files + small index/context slice in roughly one model turn. If the goal needs unbounded exploration, **`split`** first or route exploration through **`workers`** with a capped path list.
- Never attempt all steps of a large task in **one model response** unless the user explicitly asked for unattended execution.
- After each executed step, update the task file, append a line to `.mutter/logs/tasks.log` with timestamp + step id, run **`sync-task-progress`**, keep **`active_task`** pointing at the file you are executing, then run **§ Session context checkpoint** before planning the next step in chat.

## Epics and multiple agents

For goals spanning many files or sessions, use **`workers`** after splitting: one task (or step) per worker brief, state on disk between dispatches, serialize overlapping edits.

## Token rules

- When displaying a task in chat, show **title, status, current step only** unless user asks for full file.

## Stuck handling

- If the same failure pattern repeats twice with no new evidence, **stop**: append a short note to the task, set `blocked` or split into a smaller step, and log under `.mutter/logs/` instead of burning context re-trying blindly.
