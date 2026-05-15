# Mutter — workspace tools audit (reference)

This document is a **single source of truth** for what the Mutter project ships today for **disk-side discipline**, **CLI validation**, **git hooks**, and **Cursor commands**. Use it for onboarding and extra verification.

**Requirements:** Python **3.10+** for `scripts/mutter.py` (same as `scripts/sync_cursor_skills.py`). Commands assume a **repository root** that contains `.mutter/`.

---

## 1. What exists in the repository

| Area | Path | Role |
|------|------|------|
| Canonical workspace tree (dogfood / template source) | `.mutter/` | Tasks, plans, state, index, logs, templates, etc. |
| Workspace CLI (authoritative copy) | `scripts/mutter.py` | Validates tasks/plans, ADRs, governance checks, state preview, scan digest, skill refs, CI bundle |
| Cursor skill sync (maintainers) | `scripts/sync_cursor_skills.py` | Regenerates `mutter-cursor/skills/` from `mutter-claude/skills/` |
| Bootstrap template (dot-mutter) | `mutter-claude/templates/dot-mutter/` | Copied to `<consumer>/.mutter/` on bootstrap |
| Bootstrap template (CLI) | `mutter-claude/templates/scripts/mutter.py` | Copy of `scripts/mutter.py`; installed to `<consumer>/scripts/mutter.py` when missing |
| Git hook (optional) | `scripts/git-hooks/pre-commit` | Runs task + plan validation before commit when enabled |
| Cursor palette commands | `mutter-cursor/commands/*.md` → **mutter-agent-cadence**, **mutter-validate**, **mutter-preflight**, **mutter-context-pack**, **mutter-governance**, **mutter-status**, **mutter-prd**, … | Steers the agent to run `scripts/mutter.py` with the right cwd and subcommands |
| CI workflow | `.github/workflows/mutter-check.yml` | Runs `python3 scripts/mutter.py ci --check-cursor-sync` on push/PR |

---

## 2. `scripts/mutter.py` — subcommands

Run from repo root (or pass `--root <path>`):

```bash
python3 scripts/mutter.py --help
```

### `validate-task`

- **What:** Validates **one** markdown task: `## Acceptance`, `## Verify` (**must** contain a **```** fenced block with real shell commands — prose-only verify is an **error**), `## Affected` (paths in backticks / bullets), optional `## Steps` **Read:** paths with `--deep`.
- **Default file:** Resolves `.mutter/state/current.json` → `active_task`.
- **Override:** `--task <path>` (repo-relative, under `.mutter/`, or absolute).
- **When:** Before marking work done; in CI as part of `validate-tasks`.
- **Strict:** `--warnings-as-errors` fails on warnings too. `--deep` warns on missing step read paths.

### `validate-tasks`

- **What:** Same checks as `validate-task` for every `*.md` in selected buckets under `.mutter/tasks/` (skips `README.md`).
- **Default buckets:** `current`, `planned`, `blocked`.
- **Override:** `--include current planned blocked completed`.
- **When:** CI, pre-commit hook, periodic hygiene.

### `validate-plan`

- **What:** Light structure check for **plans** (aligned with `/mutter:plan`): non-empty **Affected** section + path existence, **Risks** length, **Testing**/**Verify** section must include a **```** fenced block with concrete commands (error if section exists but fence is empty / prose-only), **Definition of done** (avoids false match on words like “undone”).
- **Default file:** `active_plan` in `state/current.json`.
- **Override:** `--plan <path>`.
- **When:** After writing a large plan; before hand-off.

### `validate-plans`

- **What:** Runs `validate-plan` logic on every `*.md` in `.mutter/plans/` except `README.md`.
- **When:** CI, pre-commit hook.

### `prd-init`

- **What:** Ensures **`.mutter/prd/`** exists and writes **`.mutter/prd/PRD.md`** from **`.mutter/templates/PRD.md`** when missing (falls back to `mutter-claude/templates/dot-mutter/templates/PRD.md` only when developing inside this monorepo layout).
- **Flags:** **`--force`** replaces an existing PRD.
- **When:** First-time product capture; onboarding agents that expect **`.mutter/prd/PRD.md`**.

### `validate-prd`

- **What:** Structure check for the workspace PRD (Overview, Goals/Objectives excluding non-goals headings, Problem/Pain, Users/Audience/Personas; warns on thin Scope / Functional requirements).
- **Default file:** **`.mutter/prd/PRD.md`**.
- **Override:** **`--prd <path>`**.
- **When:** After substantive PRD edits; optional hygiene before locking roadmap/plan scope.

### `status`

- **What:** Prints `repo_root`, path to `current.json`, full JSON, and short previews of resolved **active_task** and **active_plan** when set.
- **When:** New chat session, debugging state.

### `tasks-status`

- **What:** Emits a **Markdown table** of every task `*.md` (default buckets: `current`, `planned`, `blocked`, `completed`): **Steps** and **Acceptance** checklist counts plus a **✓/○** visual for steps. With **`--task <slug-or-path>`**, one task plus a **Steps detail** list.
- **When:** **`/mutter:status`**; after multi-step execution to report progress without opening every file.

### `sync-task-progress`

- **What:** Reads the resolved task file’s checklists and writes **`execution_progress`** (and timestamps) into `.mutter/state/current.json`. Uses **`active_task`** when `--task` is omitted.
- **When:** After **each** `/mutter:task` execute step once the markdown checkboxes are updated — keeps state aligned for dashboards and hand-offs.

### `agent-cadence`

- **What:** Prints Markdown that maps **lifecycle phases** (bootstrap, session resume, plan, task loop, PR) to **skills** and **`scripts/mutter.py`** subcommands — canonical guidance so agents do not improvise when to run the CLI.
- **When:** Cold start / onboarding a new agent thread; after plugin upgrade when workflows change.
- **Flags:** **`--out <path>`** writes the same Markdown to a file (e.g. `.mutter/context/agent-cadence.md`) instead of stdout.

### `bootstrap-sync`

- **What:** Copies **plugin-managed** files from **`--template-root`** (default: `./mutter-claude/templates/dot-mutter` when present) into **`.mutter/`** — e.g. `templates/`, `quality-gates/`, `workflows/`, `adr/` files shipped with the template, `testing/commands.json`, `core/project.md`, **`prd/README.md`**, README stubs. **Does not** overwrite **`tasks/`** (except `tasks/current/README.md`), user **`plans/*.md`**, **`architecture/`**, user **`roadmap/*.md`**, **`brainstore/`** beyond README, **`state/`**, **`metadata/`** (keeps **`scan-state.json`**), **`index/`** data shards, or **`logs/*.log`**. Updates **`scripts/mutter.py`** when **`mutter-claude/templates/scripts/mutter.py`** exists (override with **`--mutter-py-source`**).
- **Flags:** **`--dry-run`** lists planned copies.
- **When:** Re-run **`/mutter:bootstrap`** / plugin upgrade to merge new Mutter template + CLI into a repo that already has `.mutter/`.

### `scan-state`

- **What:** Reads `.mutter/metadata/scan-state.json` and prints `changed_files` (or a JSON slice).
- **When:** After `/mutter:scan`, to narrow context.

### `check-skill-refs`

- **What:** Scans `mutter-claude/skills` and `mutter-cursor/skills` for relative `.md` links that must exist; resolves paths next to the file, from repo root, and `templates/...` under `mutter-claude/` / `mutter-cursor/`.
- **When:** **Mutter plugin development only** (this monorepo).

### `ci`

- **What:** Sequentially runs: `check-skill-refs` → `validate-tasks` → `validate-plans` → `sync_cursor_skills.py`. With `--check-cursor-sync`, runs `git diff --no-index --exit-code mutter-claude/skills mutter-cursor/skills` after sync (skipped if `.git` missing).
- **Flags:** `--strict-tasks` adds `--warnings-as-errors` to both task and plan validation. `--check-cursor-sync` for parity enforcement. **`--with-governance`** also runs `validate-adr`, `scan-secrets`, and `guard-large-change` (for stricter pipelines).
- **When:** GitHub Actions; maintainers before release.

### `validate-adr`

- **What:** Ensures each `.mutter/adr/*.md` (except `README.md`) has `#` title, `Status: proposed|accepted|deprecated|superseded`, and `## Context` / `## Decision` / `## Consequences`.
- **When:** After adding ADRs; optional CI via `ci --with-governance`.

### `validate-quality-gate`

- **What:** Checks `.mutter/quality-gates/<type>.md` exists and has checklist-style structure (`--type bugfix|feature|refactor|migration|security`).
- **When:** Before closing tasks that map to a gate profile.

### `preflight`

- **What:** Readiness gate: optional `--require-active-task`, `--check-acceptance-verify` (runs task validation), `--require-plan-for-large` (uses git diff size + HIGH-risk paths), dirty git warnings (`--fail-on-dirty` to error), optional `--expect-scan-state`.
- **When:** Before an agent starts a large or sensitive change.

### `context-pack`

- **What:** Prints (or `--out file`) a Markdown bundle: `state/current.json`, active task/plan excerpts, **PRD excerpt when `.mutter/prd/PRD.md` exists**, changed paths (scan-state or git), ADR previews, `ownership/modules.md` excerpt, `architecture/decisions.md` tail.
- **When:** New chat session or hand-off to another agent.

### `risk-check`

- **What:** Classifies paths as **LOW/MEDIUM/HIGH** using built-in heuristics (migrations, auth, payments, infra, etc.); reads git diff vs `HEAD` by default, or `--paths`, `--from-scan`, `--from-git --staged`.
- **When:** After editing to decide if plan + reviewer + rollback notes are required.

### `suggest-tests`

- **What:** Reads `.mutter/testing/commands.json` (`by_extension`, `by_prefix`, `path_globs`) and prints suggested commands for `--paths` or git-changed files.
- **When:** Before commit / in PR template flow.

### `pr-template` / `report-change`

- **What:** `pr-template` prints a PR Markdown skeleton (summary, related task/plan, paths, suggested tests, risk, rollback, `git diff --stat`). `report-change` prints a post-change skeleton.
- **When:** Opening a PR or pasting into review tools.

### `check-boundaries`

- **What:** Loads `.mutter/boundaries.json` (or `.yml`/`.yaml` with **PyYAML** installed). For each changed file under a module `roots` entry, scans source for **forbidden** import tokens (heuristic).
- **When:** Monorepo PRs with explicit module boundaries.

### `validate-migrations`

- **What:** If git diff includes migration-like paths, requires words such as rollback/backup/backward compat in the **active** task and/or plan text.
- **When:** DB schema change PRs.

### `scan-secrets`

- **What:** Best-effort regex scan for obvious secret patterns and risky `.env` references (`--paths`, `--git-staged`, size caps). Not a replacement for dedicated secret scanning in CI.
- **When:** Pre-commit / `ci --with-governance`.

### `scan-todos`

- **What:** Walks source extensions and writes `.mutter/metadata/todos.json` (TODO/FIXME/HACK/TEMP/@deprecated).
- **When:** Tech-debt audits.

### `guard-large-change`

- **What:** Fails when `git diff` vs `HEAD` exceeds `--max-files` / `--max-lines` or touches `--critical-paths` or more **HIGH**-risk files **without** `active_plan` in `state/current.json`.
- **When:** CI on large teams; pair with `risk-check`.

---

## 3. How scripts are installed in consumer projects

1. User runs **`/mutter:bootstrap`** (Claude) or **`mutter-bootstrap`** (Cursor) / follows the **bootstrap** skill.
2. Agent copies `templates/dot-mutter/` → `.mutter/`.
3. If **`scripts/mutter.py` does not exist** at the consumer repo root, agent copies `templates/scripts/mutter.py` → `scripts/mutter.py` (creates `scripts/` if needed). Existing file is **not** overwritten without confirmation.

After that, the same CLI commands apply in the consumer repo.

---

## 4. Git pre-commit hook

| Item | Detail |
|------|--------|
| **Script** | `scripts/git-hooks/pre-commit` |
| **Enable** | From repo root: `git config core.hooksPath scripts/git-hooks` |
| **Disable** | `git config --unset core.hooksPath` |
| **Runs** | `validate-tasks` and `validate-plans` if `.mutter/` and `scripts/mutter.py` exist; then **`scan-secrets --git-staged`** and **`guard-large-change`** (unless `MUTTER_HOOK_SKIP_GOVERNANCE=1`) |
| **If `python3` missing** | Prints notice, **exits 0** (does not block commit) |
| **Skip governance** | `MUTTER_HOOK_SKIP_GOVERNANCE=1` — skips `scan-secrets --git-staged` and `guard-large-change` (tasks/plans still run) |
| **Strict mode** | `MUTTER_HOOK_STRICT=1 git commit ...` — passes `--warnings-as-errors` to validators **and** to `scan-secrets` / `guard-large-change` in the governance block |

---

## 5. Cursor IDE

| Item | Detail |
|------|--------|
| **Command** | **mutter-validate**, **mutter-preflight**, **mutter-context-pack**, **mutter-governance**, **mutter-prd**, … (from `mutter-cursor/commands/`) |
| **Purpose** | Steers the agent to run `scripts/mutter.py` with the right cwd and subcommands |
| **Install** | Team marketplace / local plugin per Cursor docs |

Claude Code has no separate `validate` slash skill; use **`/mutter:task`** and **`/mutter:plan`** (Automation / post-plan notes) or the terminal.

---

## 6. Skills that mention the CLI

- **`task`** — Automation (scripts): validation, governance (`preflight`, `context-pack`, `risk-check`, `pr-template`, `suggest-tests`, `check-boundaries`, `scan-secrets`, `guard-large-change`, `validate-adr`, `validate-quality-gate`, `validate-migrations`, `validate-prd`, `prd-init`), `status`, `scan-state`, `check-skill-refs`, `ci`.
- **`plan`** — Optional `validate-plan` after writing a plan.
- **`prd`** — `prd-init` / `validate-prd`; aligns tasks/plans with `.mutter/prd/PRD.md`.
- **`bootstrap`** — Installs `scripts/mutter.py` when missing; after bootstrap mentions validation + governance commands.
- **`help`** — Points to `--help` and `docs/mutter-workspace-tools-audit.md`.

---

## 7. Quick verification checklist (for you)

Run from **this** repository root:

```bash
python3 scripts/mutter.py check-skill-refs
python3 scripts/mutter.py validate-tasks
python3 scripts/mutter.py validate-plans
python3 scripts/mutter.py validate-adr
python3 scripts/mutter.py status
python3 scripts/mutter.py scan-state
python3 scripts/mutter.py preflight --check-acceptance-verify
python3 scripts/mutter.py context-pack | head -n 40
python3 scripts/mutter.py suggest-tests --from-git
python3 scripts/mutter.py ci --check-cursor-sync   # optional; needs git + clean mutter-cursor/skills
```

Enable and test the hook:

```bash
git config core.hooksPath scripts/git-hooks
# touch a file and commit on a branch — hook should run if .mutter + scripts exist
```

Confirm **Cursor** lists **mutter-validate**, **mutter-preflight**, **mutter-context-pack**, and **mutter-governance** after plugin reload.

---

## 8. Design notes (limits)

- These tools enforce **markdown structure and path existence**, not code correctness. **Tests and product CI** remain the hard boundary.
- **Python** is intentional for one-file, cross-platform logic (see project discussion vs bash-only repos).
- **`ci`** is optimized for the **Mutter monorepo** (skills + sync). Consumer repos typically use **`validate-tasks`** / **`validate-plans`** only unless they vendor the whole plugin layout.

---

*Last aligned with repository layout and `scripts/mutter.py` behavior as of this change set.*
