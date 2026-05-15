# Mutter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/github/stars/arnaudovproject/mutter?style=social)](https://github.com/arnaudovproject/mutter)

**Mutter** brings a small **on-disk workspace** (folder **`.mutter/`**) into your repository so AI coding agents can **remember** architecture, tasks, and plans between sessions—without loading the whole tree into context. The same workflow patterns work across **Claude Code**, **Cursor**, **OpenAI Codex**, and **OpenCode**.

| Section | Best for |
|---------|----------|
| [Who is Mutter for?](#who-is-mutter-for) | Decide if this matches your workflow |
| [Recommended first path](#recommended-first-path) | Install and first commands (Claude Code) |
| [Five-minute example](#five-minute-example) | One concrete pass: bootstrap → task → validate |
| [Installation](#installation) | Cursor, Codex, OpenCode, and full Claude steps |
| [Typical workflow](#typical-workflow-your-repo) | Day-to-day and before-merge habits |
| [Skills](#skills-most-used-first) · [Workspace CLI](#workspace-cli) | Reference tables |

---

## Who is Mutter for?

Mutter fits **developers and teams** who already use (or plan to use) **AI coding agents** on **medium and large codebases** and want:

- **Project memory on disk**—tasks, plans, architecture notes, and logs—not only chat history
- **Repeatable agent behavior**—shared rules, checklists, and validation hooks
- **Cheaper, calmer sessions**—indexes and small “context packs” instead of pasting the repo into every thread

If you only touch a repo once for a tiny change, you might not need this much structure. If agents work across **days, branches, or multiple PRs**, Mutter is aimed at you.

---

## Recommended first path

If you are new, start with **Claude Code** (the examples below use its **`/mutter:<skill>`** style):

1. **Install the plugin** — follow [Quick install (Claude Code)](#quick-install-claude-code) (register the **repository root** that contains `.claude-plugin/marketplace.json`, then install **`mutter@mutter-plugins`**).
2. Open **your project** in Claude Code and run **`/mutter:bootstrap`** — creates `.mutter/`, light entry files, and `scripts/mutter.py` when missing.
3. Run **`/mutter:scan`** — builds incremental indexes under `.mutter/index/`.
4. Run **`/mutter:help`** — see available skills and how they map to validation commands.

**Other agents:** install Mutter for [Cursor](#cursor), [OpenAI Codex](#openai-codex), or [OpenCode](#opencode), then use the same *ideas* (bootstrap → scan → task/help); command names differ by **harness** (see [Typical workflow](#typical-workflow-your-repo)).

---

## Five-minute example

In **your** repository, with the plugin installed:

1. **`/mutter:bootstrap`**
2. **`/mutter:scan`**
3. **`/mutter:task create "Add user profile page"`** (or any small, clear task title)
4. Ask your agent to **execute the first unchecked step** in the generated task (keep one main outcome per turn while learning the flow)
5. Before you call the task “done”, from the repo root: **`python3 scripts/mutter.py validate-task`**

That path covers the core loop; everything else in this README extends it (plans, PRD, reviews, CI helpers).

---

## Example: workspace CLI output

After **bootstrap**, **`python3 scripts/mutter.py status`** shows where state lives and prints **`.mutter/state/current.json`** (active task, plan, and progress). Example:

```text
repo_root: /path/to/your/project
state file: /path/to/your/project/.mutter/state/current.json
{
  "active_task": null,
  "active_plan": null,
  "active_workflow": null,
  "execution_progress": null,
  "paused": false,
  "updated_at": null
}
```

**`python3 scripts/mutter.py context-pack --out .mutter/context/session-pack.md`** writes a **Markdown bundle** (state, active task/plan slices when set, useful excerpts) you can attach when starting a **new** session—lighter than copying ad hoc file dumps.

**Claude Code spelling:** skills are **`/mutter:<skill>`** (e.g. `/mutter:scan`). Some prose uses `/mutter scan`; Claude Code expects the **colon** form. Plugin id: **`mutter`** (lowercase).

---

## Quick install (Claude Code)

Register the **repository root** (the folder that contains `.claude-plugin/marketplace.json`), not `mutter-claude/`:

```text
/plugin marketplace add /path/to/mutter
/plugin install mutter@mutter-plugins
/reload-plugins
```

Confirm with **`/mutter:help`**.

Use the **marketplace** flow only — do **not** symlink into `~/.claude/plugins`. Add the repo with **`/plugin marketplace add`**, then install **`mutter@mutter-plugins`**.

---

## What it does

| Area | Description |
|------|-------------|
| **Project memory** | `.mutter/` holds architecture, tasks, plans, optional product spec (**PRD** at `.mutter/prd/PRD.md`), indexes, logs, and rules—without monolithic chat dumps. |
| **Navigation** | Index shards and explicit paths first; avoid loading the whole repo into context when a task names a smaller slice. |
| **Orchestration** | **Skills** (agent commands like **scan**, **task**, **plan**) plus the **workspace CLI** (`scripts/mutter.py`) for validation, preflight, **context-pack**, **agent-cadence**, and CI-oriented checks. |
| **Discipline** | Small repo-root entry files (**`CLAUDE.md`**, Cursor rules); detail stays under `.mutter/`. |
| **Multi-harness** | Parity across Claude Code, Cursor, Codex, and OpenCode—see [Code layout (by harness)](#code-layout-by-harness). |

- Full spec: [`SPEC.md`](SPEC.md)
- Harness / plugin development: [`docs/mutter-plugin-harness-reference.md`](docs/mutter-plugin-harness-reference.md)

---

## Code layout (by harness)

| Agent | Location in this repo |
|-------|------------------------|
| **Claude Code** | `mutter-claude/` (`.claude-plugin/plugin.json`) |
| **OpenAI Codex** | Same skills as Claude — `mutter-claude/.codex-plugin/plugin.json` → `mutter-claude/skills/` |
| **Cursor** | `mutter-cursor/` (rules, skills, commands) |
| **OpenCode** | Root `package.json` + `.opencode/plugins/mutter.js` (registers `mutter-claude/skills`) |

Cursor’s `mutter-cursor/skills/` is kept in sync with `mutter-claude/skills/` during Mutter development (`python3 scripts/sync_cursor_skills.py`).

From here down, the README is **reference-heavy**: full install notes for every harness, the complete lifecycle workflow, and command tables. Skim the **quick links** table under the opening paragraph if you want to jump to one topic.

---

## Installation

### Claude Code

1. **Clone** (if needed): `git clone https://github.com/arnaudovproject/mutter.git`
2. **Install** — follow [Quick install (Claude Code)](#quick-install-claude-code): marketplace path = **clone root** (the directory that contains `.claude-plugin/marketplace.json`). Example: repo at `/code/mutter/mutter` → `/plugin marketplace add /code/mutter/mutter`. Catalog name **`mutter-plugins`** ([`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)); package under [`mutter-claude/`](mutter-claude/) installs as **`mutter@mutter-plugins`**.
3. **Update** — `git pull`, then **`/reload-plugins`**
4. **Uninstall** — `/plugin uninstall mutter`, then `/plugin marketplace remove mutter-plugins`

**Local / dev** (no marketplace): from repo root, `claude --plugin-dir ./mutter-claude`; after edits, **`/reload-plugins`**.

Docs: [Plugins](https://code.claude.com/docs/en/plugins) · [Plugins reference](https://code.claude.com/en/plugins-reference).

### Cursor

- **Team marketplace:** import this Git repo per [Cursor Plugins](https://cursor.com/docs/plugins). [`.cursor-plugin/marketplace.json`](.cursor-plugin/marketplace.json) maps the `mutter` entry to `./mutter-cursor`.
- **Local dev:** symlink or copy so `mutter-cursor/.cursor-plugin/plugin.json` is at the **root** of the installed plugin, e.g. `ln -s /path/to/mutter/mutter-cursor ~/.cursor/plugins/local/mutter` — then **Developer: Reload Window**.

Docs: [Plugins](https://cursor.com/docs/plugins) · [Reference](https://cursor.com/docs/reference/plugins.md). IDE routing (this repo does not ship `.cursor/`): [`docs/mutter-cursor-ide-routing.md`](docs/mutter-cursor-ide-routing.md).

### OpenAI Codex

Skills: **`mutter-claude/skills/`** · Manifest: **`mutter-claude/.codex-plugin/plugin.json`**.

- **In this repo:** [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) points at `./mutter-claude` for local dogfooding / CI.
- **In a consumer repo:** add a marketplace and install per [Codex Plugins](https://developers.openai.com/codex/plugins) and [Build plugins](https://developers.openai.com/codex/plugins/build).

Skill names and YAML frontmatter align with Claude.

### OpenCode

Requires [OpenCode](https://opencode.ai). In `opencode.json` (project or `~/.config/opencode/opencode.json`), add to **`plugin`**:

```json
{ "plugin": ["mutter@git+https://github.com/arnaudovproject/mutter.git"] }
```

Pin a revision by appending `#branch`, `#tag`, or `#sha`:

```json
{ "plugin": ["mutter@git+https://github.com/arnaudovproject/mutter.git#main"] }
```

Restart OpenCode. More: [`.opencode/INSTALL.md`](.opencode/INSTALL.md) · [OpenCode Plugins](https://opencode.ai/docs/plugins/).

---

## Typical workflow (your repo)

**Harness spellings:** Claude → **`/mutter:<skill>`** · Cursor → palette **`mutter-<skill>`** (e.g. **`mutter-scan`**) or the same skill names · Codex / OpenCode → plugin / skill UI. **CLI** = `python3 scripts/mutter.py …` from **repo root** (after **bootstrap** installed the script).

### 0 — First time

1. **`/mutter:bootstrap`** — `.mutter/`, entry files, `scripts/mutter.py` if missing
2. **`/mutter:scan`** — `metadata/scan-state.json` + `index/` shards
3. Optional: **`python3 scripts/mutter.py agent-cadence --out .mutter/context/agent-cadence.md`** — when to run which skill vs CLI
4. Optional (product / application repos): **`python3 scripts/mutter.py prd-init`**, then **`python3 scripts/mutter.py validate-prd`** — canonical **`.mutter/prd/PRD.md`** (see **Direction** under step 2 below)

### 1 — New session (resume cheaply)

1. **`python3 scripts/mutter.py status`** — `active_task` / `active_plan` in `.mutter/state/current.json`
2. **`python3 scripts/mutter.py context-pack --out .mutter/context/session-pack.md`**
3. Before heavy work: **`python3 scripts/mutter.py preflight --require-active-task --check-acceptance-verify`** (add **`--require-plan-for-large`** for big / risky diffs)

### 2 — Direction (before locking scope)

- **`/mutter:prd`** — workspace **Product Requirements Document** at **`.mutter/prd/PRD.md`** (product “what / why” for agents). First time: **`python3 scripts/mutter.py prd-init`**; after edits: **`python3 scripts/mutter.py validate-prd`**. Distinct from repo-root **`SPEC.md`** when your repo is **Mutter itself** — **`SPEC.md`** describes the framework; **`PRD.md`** describes *your* product in a consumer workspace.
- **`/mutter:brainstore`** — notes / spikes → `.mutter/brainstore/`
- **`/mutter:architecture`** — boundaries, APIs, ADRs; after ADR edits → **`python3 scripts/mutter.py validate-adr`**
- **`/mutter:roadmap`** — themes, milestones, debt. With **empty** args: align roadmap with architecture, then **`/mutter:task create`** (no title) can spawn tasks from open roadmap items

### 3 — PRD vs roadmap vs plan

- **PRD** (optional but recommended for app/product work) = stable **product intent**: goals, users, problems, functional scope — **`.mutter/prd/PRD.md`**. **`context-pack`** includes a PRD excerpt when that file exists.
- **Roadmap** = *what* over time (outcomes, milestones).
- **Plan** = *how* for **one** scoped change → **`/mutter:plan`**, then **`python3 scripts/mutter.py validate-plan`**. Optional: **`python3 scripts/mutter.py risk-check --from-git`**.

### 4 — Tasks (execute / continue)

1. **`/mutter:task create "…"`** — one **Steps** checkbox ≈ one agent turn (one **Read:** list, one outcome); **`split`** if a step needs “the whole repo”. Prefer **reuse** of existing modules/helpers (see **task** skill and **`TASK.md`** template). If no explicit task file, follow the **task** skill: check **`.mutter/plans/`**, **`.mutter/roadmap/`**, optionally **`.mutter/prd/PRD.md`**, **`.mutter/state/current.json`**
2. Set **`active_task`** in **`.mutter/state/current.json`** when executing (per **task** skill)
3. Per step: **`/mutter:safe-edit`** (or same discipline) → tick **one** step → append **`.mutter/logs/tasks.log`** → **`python3 scripts/mutter.py sync-task-progress`** → **`/mutter:status`** or **`python3 scripts/mutter.py tasks-status --task <slug>`**
4. **Session context:** After a step is **fully** done (not mid-step), check your harness’s context meter. If it’s **~40% or higher**, the default recommendation is a **new chat**, then **`context-pack`** and **`status`**, then the next **Steps** line — see **`/mutter:task`** and **`agent-cadence`**. Staying in the same thread is fine if you explicitly choose it.
5. Before “done”: **`python3 scripts/mutter.py validate-task`**

### 5 — After code lands

- **`/mutter:scan`** when meaningful code changed

### 6 — Before PR / merge

1. **`/mutter:review-diff`** → findings under **`.mutter/reviews/`**; fix **Critical** before merge
2. **`python3 scripts/mutter.py suggest-tests --from-git`**, **`scan-secrets`**, **`validate-task`** / **`validate-tasks`** as needed
3. **`python3 scripts/mutter.py pr-template`**

### 7 — Ship

- CI: **`validate-tasks`**, **`validate-plans`**, optional **`guard-large-change`**
- **`python3 scripts/mutter.py report-change`** for release notes / handoff

**Regenerate cheat sheet anytime:** **`python3 scripts/mutter.py agent-cadence`**. Workspace tools detail: [`docs/mutter-workspace-tools-audit.md`](docs/mutter-workspace-tools-audit.md).

### Token habits (same ideas as [`.mutter/core/project.md`](.mutter/core/project.md))

- **Disk coordinates** — scope, checklists, `execution_progress` live in `.mutter/` so new sessions do not replay the whole story in chat.
- **One-window steps** — explicit paths + index keys per step; **`split`** or **`workers`** if too wide.
- **context-pack** over ad-hoc multi-file pastes; pair with the **task** skill’s **~40% checkpoint** when a long session gets heavy.
- **Logs off-transcript** — long output → **`.mutter/logs/`**; in chat: exit code, a few lines, path.
- **Official docs** — before web search, open **one** section of **`memory/official-tech-docs-roadmap.md`** if your project maintains it.

---

## Skills (most used first)

Claude: **`/mutter:<name>`** · Cursor: same names + palette · Codex: plugin UI · OpenCode: skill tool.

| Skill | When | What |
|-------|------|------|
| **bootstrap** | No `.mutter/` or upgrade | Template; **`bootstrap-sync`** refreshes shipped files without wiping tasks/plans/architecture. |
| **scan** | After real code change | Incremental scan, indexes, `scan-state`. |
| **task** | Work on disk | **create** / **update** / **split** / **execute**; one **Steps** box per turn; **`sync-task-progress`** after each tick; **~40% session checkpoint** after each finished step (new session + **`context-pack`** when high); bare **task** = current queue. |
| **status** | Progress | With **`tasks-status`**. |
| **plan** | Multi-file or risky change | Scoped plan + verify; then **`validate-plan`**. |
| **safe-edit** | Any edit | Explain → minimal diff → narrow verify; long output → **`.mutter/logs/`**. |
| **review-diff** | Pre-merge | Quality, security, tests; severity tags → **`.mutter/reviews/`**. |
| **brainstore** | Ideas / intel | **`.mutter/brainstore/`** — use early to keep chat small. |
| **prd** | Product spec for agents | **`.mutter/prd/PRD.md`** — **`prd-init`**, **`validate-prd`**; revise when roadmap/architecture changes product scope. |
| **roadmap** | Direction over time | **`.mutter/roadmap/`**; empty args → align with **architecture** before new tasks. |
| **architecture** | Boundaries / ADRs | Design truth; **`validate-adr`** when ADRs change. |
| **workers** | Epics / parallelism | Queue + briefs + file caps; after **split** if still too wide. |
| **context** | Tight bundles | **`.mutter/context/`** + **`context-pack`**. |
| **memory** | Long-lived conventions | Includes **`official-tech-docs-roadmap.md`**. |
| **workflow** | Repeatable process | Files under **`.mutter/workflows/`**. |
| **snapshot** | Checkpoint | Index / architecture / roadmap snapshot. |
| **help** | Orientation | Index of commands / rules. |
| **explain** | Understand code | Minimal reads. |
| **analyze** | Deeper dive | Needs explicit file list. |
| **risks** | Change assessment | Risk register. |
| **dependencies** | Graph | Dependency slice. |
| **tests** | Coverage mapping | Tests vs changes. |
| **affected** | Blast radius | Affected files / domains. |
| **review** | Extra pass | Structured review wrapper. |

---

## Cursor palette (`mutter-cursor/commands/`)

Markdown-backed commands (**`mutter-<skill>`**). Common governance / validation:

| Command | Use |
|---------|-----|
| **mutter-agent-cadence** | Skill vs CLI cadence (`agent-cadence`). |
| **mutter-preflight** | State, dirty git, diff size, etc. |
| **mutter-status** | Checklist table (`tasks-status`). |
| **mutter-context-pack** | Session Markdown bundle. |
| **mutter-prd** | PRD workflow (`prd` skill); pairs with **`prd-init`** / **`validate-prd`**. |
| **mutter-validate** | Task / plan validation via workspace CLI. |
| **mutter-governance** | ADRs, boundaries, quality gates. |

Other `*.md` files mirror skills (scan, plan, task, prd, …).

---

## Workspace CLI

Primary entry point: **`scripts/mutter.py`** (run from repo root after **bootstrap**).

**Requirements:** Python 3 (stdlib for most commands). YAML boundaries may need **PyYAML** — see `.mutter/core/project.md` and `boundaries.json`.

Resolves repo root by walking up for **`.mutter/`**, or pass **`--root`**. In consumer repos the file usually comes from **bootstrap** (`mutter-claude/templates/scripts/mutter.py` → `<repo>/scripts/mutter.py`).

| Command | When | What |
|---------|------|------|
| `agent-cadence` | Start / onboarding | Phases → skills → CLI; `--out .mutter/context/agent-cadence.md` |
| `status` | Each new session | `.mutter/state/current.json` + active task/plan snippets |
| `preflight` | Before large / risky work | State, optional active task, dirty git, diff size |
| `context-pack` | Cold start / handoff | Markdown pack (task, plan, **PRD excerpt** if present); `--out` |
| `tasks-status` | After task steps | Table; `--task` for one file |
| `sync-task-progress` | After checkbox ticks | `execution_progress` in `.mutter/state/current.json` |
| `validate-task` | Before task “done” | One task (default: active) |
| `validate-tasks` | CI / release | Tasks in selected buckets |
| `validate-plan` | After a plan | One file under `.mutter/plans/` |
| `validate-plans` | CI | All plans |
| `prd-init` | First PRD | Create `.mutter/prd/PRD.md` from template (`--force` overwrites) |
| `validate-prd` | After PRD edits | Structure check (default: `.mutter/prd/PRD.md`; `--prd` path) |
| `suggest-tests` | Before PR | Commands from `.mutter/testing/commands.json` |
| `pr-template` | Open PR | Body from task/plan + git + suggested tests |
| `scan-state` | After scan | `changed_files` from `metadata/scan-state.json` |
| `risk-check` | Around a change | LOW/MEDIUM/HIGH heuristics (git or scan-state) |
| `scan-secrets` | Before merge | Best-effort local secret patterns |
| `report-change` | Release notes | Markdown skeleton |
| `bootstrap-sync` | Plugin upgrade | Refresh template-managed `.mutter/` + `mutter.py` |
| `check-boundaries` | Architecture | From `.mutter/boundaries.json` |
| `validate-migrations` | DB migrations | Rollback / backup notes when paths change |
| `validate-adr` | ADR edits | `.mutter/adr/*.md` structure |
| `validate-quality-gate` | By work type | `quality-gates/<type>.md` exists |
| `scan-todos` | Tech debt | TODO/FIXME → `metadata/todos.json` |
| `guard-large-change` | Large PRs | Thresholds / critical paths need plan |
| `check-skill-refs` | Mutter dev | Relative `.md` links in skills |
| `ci` | This repo’s CI | Refs + tasks + plans + optional Cursor skill sync |

```bash
python3 scripts/mutter.py --help
```

**Optional hook:** `git config core.hooksPath scripts/git-hooks` (when `.mutter/` and `scripts/mutter.py` exist).

**Cursor ↔ Claude skill sync (Mutter development):** `python3 scripts/sync_cursor_skills.py` — `ci` with **`--check-cursor-sync`** requires `mutter-cursor/skills` to match `mutter-claude/skills`.

---

## `.mutter/` layout

Canonical map: [`.mutter/core/project.md`](.mutter/core/project.md) — `index/`, `architecture/`, `tasks/`, `plans/`, **`prd/`**, `state/`, `workflows/`, `memory/`, `logs/`, `brainstore/`, etc. **Incremental shards**, not one giant file.

---

## Community

- **Author:** [Ventsislav Arnaudov](https://varnaudov.com)
- **Repo:** [github.com/arnaudovproject/mutter](https://github.com/arnaudovproject/mutter)
- **Issues:** [GitHub Issues](https://github.com/arnaudovproject/mutter/issues)

Similar **idea space** to [Superpowers](https://github.com/obra/superpowers) (skills encode **process**; filesystem coordinates). Mutter is its own product: `.mutter/` indexes, tasks, plans, and parity across Claude, Cursor, Codex, and OpenCode.

---

## License

MIT — see `package.json` and manifests under `mutter-claude/` and `mutter-cursor/`.
