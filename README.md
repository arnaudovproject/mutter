# Mutter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/github/stars/arnaudovproject/mutter?style=social)](https://github.com/arnaudovproject/mutter)

## Quick install (Claude Code)

Register the **repository root** (the folder that contains `.claude-plugin/marketplace.json`), not `mutter-claude/`:

```text
/plugin marketplace add /path/to/mutter
/plugin install mutter@mutter-plugins
/reload-plugins
```

Verify with **`/mutter:help`**.

**Do not** install Mutter by symlinking into `~/.claude/plugins`. It is a **Claude marketplace** plugin: add the repo with **`/plugin marketplace add`**, then install **`mutter@mutter-plugins`** as above.

---

**Mutter** is a plugin and methodology for an **AI workspace** on top of your code: structured on-disk memory (`.mutter/`), token-efficient workflows, tasks, plans, incremental indexing, and consistent operating rules across several agent harnesses.

The plugin name in manifests is **`mutter`** (lowercase). In **Claude Code**, skills are invoked under the **`/mutter:<name>`** namespace — for example `/mutter:scan`, `/mutter:status`, `/mutter:help` (docs sometimes shorten this to “`/mutter scan`”; in Claude Code the colon form is canonical).

---

## What Mutter does

| Area | Description |
|------|-------------|
| **Project memory** | The `.mutter/` tree — architecture, tasks, plans, indexes, logs, rules — without dumping monolithic blobs into chat. |
| **Navigation** | Index shards and explicit paths first; the whole repository is not loaded into context. |
| **Orchestration** | Scanning, `task`, `plan`, parallel `workers`, `safe-edit`, and `review-diff`. |
| **Discipline** | Small entry files (`CLAUDE.md`, Cursor rules); detail lives under `.mutter/`. |
| **Tooling** | Optional Python CLI `scripts/mutter.py` for validation, preflight, context packing, CI checks, and more. |

**Who it is for:** teams and large codebases where you want agents to follow one process, resume state between sessions, and use fewer tokens for the same accuracy.

Full product spec: [`SPEC.md`](SPEC.md). Harness and plugin development reference: [`docs/mutter-plugin-harness-reference.md`](docs/mutter-plugin-harness-reference.md).

---

## Supported agents and where the code lives

| Agent | Package / path in this repo |
|-------|----------------------------|
| **Claude Code** | `mutter-claude/` (`.claude-plugin/plugin.json`) |
| **OpenAI Codex** | Same skills as Claude — manifest at `mutter-claude/.codex-plugin/plugin.json` |
| **Cursor** | `mutter-cursor/` (rules, skills, palette commands) |
| **OpenCode** | Repo root: `package.json` + `.opencode/plugins/mutter.js` (registers `mutter-claude/skills`) |

Codex and Claude share the **same** Markdown skills under `mutter-claude/skills/`. Cursor keeps a synchronized copy under `mutter-cursor/skills/` (refreshed by a script during development).

---

## Installation

### Claude Code

**Global install:** use [Quick install (Claude Code)](#quick-install-claude-code) at the top of this README (`/plugin marketplace add` → `/plugin install mutter@mutter-plugins` → `/reload-plugins`).

1. **Clone** (if you do not have the repo yet): `git clone https://github.com/arnaudovproject/mutter.git`
2. **Marketplace path** — pass the **clone root**. Example: if the repo is at `/code/claude/mutter/mutter`, run `/plugin marketplace add /code/claude/mutter/mutter`. Claude registers the catalog from [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) (name **`mutter-plugins`**); the plugin package lives under [`mutter-claude/`](mutter-claude/) and installs as **`mutter@mutter-plugins`**.
3. **Update** — `git pull` in the clone, then **`/reload-plugins`** in Claude Code.
4. **Uninstall** — `/plugin uninstall mutter`, then `/plugin marketplace remove mutter-plugins`.

**Local / dev** (run from a clone without marketplace): from the repo root, `claude --plugin-dir ./mutter-claude`. After editing plugin files: **`/reload-plugins`**.

Official docs: [Plugins](https://code.claude.com/docs/en/plugins) · [Plugins reference](https://code.claude.com/en/plugins-reference).

---

### Cursor

- **Marketplace / team catalog:** import the Git repo as a [team marketplace](https://cursor.com/docs/plugins) (e.g. Dashboard → Plugins → Team Marketplaces → Import). At the repo root, [`.cursor-plugin/marketplace.json`](.cursor-plugin/marketplace.json) points at `./mutter-cursor` for the `mutter` plugin.
- **Local development install:** copy or symlink the plugin tree so `mutter-cursor/.cursor-plugin/plugin.json` sits at the **root** of the installed plugin, for example:

```bash
ln -s /path/to/mutter/mutter-cursor ~/.cursor/plugins/local/mutter
```

Then in Cursor: **Developer: Reload Window**.

Documentation: [Cursor Plugins](https://cursor.com/docs/plugins) · [Plugins reference](https://cursor.com/docs/reference/plugins.md).

IDE routing (this repo does not track `.cursor/`): [`docs/mutter-cursor-ide-routing.md`](docs/mutter-cursor-ide-routing.md).

---

### OpenAI Codex

Skills live in **`mutter-claude/skills/`**; the manifest is **`mutter-claude/.codex-plugin/plugin.json`**.

- **Inside a cloned `mutter` repo:** [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) already defines a **local** source `./mutter-claude` — useful for dogfooding and CI.
- **In a consumer project:** add a marketplace using the official flow (`codex plugin marketplace add` and plugin install) per [Codex Plugins](https://developers.openai.com/codex/plugins) and [Build plugins](https://developers.openai.com/codex/plugins/build).

Skill names and YAML frontmatter (`name`, `description`) match the same files as Claude.

---

### OpenCode

Requires [OpenCode](https://opencode.ai) to be installed. In `opencode.json` (project or `~/.config/opencode/opencode.json`), add to the **`plugin`** array:

```json
{
  "plugin": ["mutter@git+https://github.com/arnaudovproject/mutter.git"]
}
```

To pin a revision, append a ref after `#` (branch, tag, or SHA):

```json
{
  "plugin": ["mutter@git+https://github.com/arnaudovproject/mutter.git#main"]
}
```

Restart OpenCode. Details: [`.opencode/INSTALL.md`](.opencode/INSTALL.md). Plugin docs: [OpenCode Plugins](https://opencode.ai/docs/plugins/).

---

## How to work with Mutter (short flow)

1. **Bootstrap** — if the project has no `.mutter/`, run the **`bootstrap`** skill (or follow it) to materialize the template from `mutter-claude/templates/dot-mutter/`. If `.mutter/` already exists and you upgraded the Mutter plugin, run **`python3 scripts/mutter.py bootstrap-sync --dry-run`** then **`bootstrap-sync`** to refresh templates and `mutter.py` without touching your tasks, plans, or architecture docs.
2. **Entry files** — keep root **`CLAUDE.md`** (or Cursor rules) **small**; they should only route to `.mutter/core/project.md` and global safety rules.
3. **Scan** — **`/mutter:scan`** in Claude (or the equivalent in your harness) for incremental updates and indexes.
4. **Tasks and plans** — **`task`**, **`plan`**, **`status`** (checklist progress); for large epics — **`workers`**.
5. **Changes** — **`safe-edit`**; before merge — **`review-diff`**.
6. **Terminal checks** (when `scripts/mutter.py` exists): `python3 scripts/mutter.py preflight` before a large change; `tasks-status` / `sync-task-progress` during execution; `validate-task` / `validate-plans` in CI.

More on workspace tools: [`docs/mutter-workspace-tools-audit.md`](docs/mutter-workspace-tools-audit.md).

---

## Skills — when to use each

In **Claude Code** the format is **`/mutter:<skill>`**. In **Cursor**, the same names appear as skills plus palette commands (see the next section). In **Codex**, use the plugin / skill UI. In **OpenCode**, use the skill tool to load by name.

| Skill | When to use it | What it does |
|-------|----------------|--------------|
| **bootstrap** | New project without `.mutter/` | Initializes structure from template; copies `scripts/mutter.py` when needed. |
| **help** | Orientation | Reference for commands and rules. |
| **scan** | After code changes / periodically | Incremental scan, index updates, `scan-state`. |
| **brainstore** | Ideas, notes, structured intel | Writes under `.mutter/brainstore/`. |
| **task** | A concrete unit of work | Create, update, split, execute tasks; bare `task` or `execute` runs the **current** queue; `create` with no text pulls from **roadmap**. |
| **status** | Visibility | Markdown table of step/acceptance checklist progress (`tasks-status`). |
| **plan** | Before a larger change | Plan with risks and affected files. |
| **workers** | Epics, parallel agents | Queue, briefs, safe parallelism. |
| **safe-edit** | Any editing | Explain → minimal diff → verify. |
| **review-diff** | Before PR / merge | Architecture, security, tests, conventions. |
| **roadmap** | Planning | Maintain roadmap under `.mutter/roadmap/`; empty args first align with **architecture** shards. |
| **architecture** | Design and boundaries | Architecture docs and ADRs. |
| **context** | Tight agent context | Curated bundles under `.mutter/context/`. |
| **memory** | Long-lived rules | Conventions; includes `official-tech-docs-roadmap.md` (official doc links before web search). |
| **workflow** | Named process | Select or run a file under `.mutter/workflows/`. |
| **snapshot** | Checkpoint | Snapshot index / architecture / roadmap. |
| **review** | Structured review | Wrapper for review output. |
| **explain** | Understanding code | Explanation with minimal reads. |
| **analyze** | Deeper analysis | With an explicit file list. |
| **risks** | Change assessment | Risk register. |
| **dependencies** | Graph | Dependency slice. |
| **tests** | Change coverage | Test mapping for the change. |
| **affected** | Change scope | Affected files / domains. |

---

## Cursor — palette commands (`mutter-cursor/commands/`)

These Markdown files define discoverable commands (names like **`mutter-<skill>`**). Common ones for validation and governance:

| Command (prefix) | Use |
|------------------|-----|
| **mutter-validate** | Task / plan validation (ties into the workspace CLI). |
| **mutter-preflight** | Pre-work checks (state, dirty git, diff size, etc.). |
| **mutter-context-pack** | Compact Markdown bundle for agents. |
| **mutter-governance** | ADRs, boundaries, quality — per the matching `.md` in `commands/`. |
| **mutter-status** | Task checklist table (`tasks-status` CLI). |

Other `.md` files in `mutter-cursor/commands/` mirror skill names (e.g. `scan`, `plan`, `task`).

---

## Python: `scripts/mutter.py` (workspace CLI)

**Requirements:** **Python 3** (stdlib covers most commands). Some checks (e.g. YAML boundaries) may need **PyYAML** — see `.mutter/core/project.md` and `boundaries.json`.

The script walks upward from the current directory for a repo root containing **`.mutter/`**, or pass **`--root /path/to/repo`**.

In **your** project, the script usually arrives via the **bootstrap** template (`mutter-claude/templates/scripts/mutter.py` → copy at `<repo>/scripts/mutter.py`).

### Subcommands

| Command | When | What it does |
|---------|------|----------------|
| `validate-task` | Before merging a task | Validates one task `.md` (default: active from `state`). |
| `validate-tasks` | CI / before release | All tasks in selected buckets (`current`, `planned`, …). |
| `validate-plan` | Before merging a plan | One plan under `.mutter/plans/`. |
| `validate-plans` | CI | All plans. |
| `status` | Quick look | `state/current.json` and snippets of active task/plan. |
| `scan-state` | After a scan | Prints `changed_files` from `metadata/scan-state.json`. |
| `check-skill-refs` | Mutter development | Validates relative `.md` links in skills. |
| `ci` | CI in the Mutter repo | Refs + tasks + plans + optional Cursor skill sync. |
| `validate-adr` | ADR changes | Structure of `.mutter/adr/*.md`. |
| `validate-quality-gate` | By work type | Ensures `quality-gates/<type>.md` profile exists. |
| `risk-check` | Before / after a change | LOW/MEDIUM/HIGH heuristics on paths (git or scan-state). |
| `context-pack` | Agent context | Markdown pack (task, plan, ADR, ownership). |
| `preflight` | Session start / PR | State, optional active task, dirty git, diff size. |
| `report-change` | Change notes | Markdown skeleton after a change. |
| `pr-template` | Opening a PR | Markdown from task/plan + git + suggested tests. |
| `suggest-tests` | Local testing | Commands from `.mutter/testing/commands.json` for paths. |
| `check-boundaries` | Architecture | Heuristic checks from `.mutter/boundaries.json`. |
| `validate-migrations` | DB migrations | Requires rollback/backup notes when migration paths change. |
| `scan-secrets` | Security | Lightweight local patterns for obvious secrets (best-effort). |
| `scan-todos` | Tech debt | Collects TODO/FIXME into `metadata/todos.json`. |
| `guard-large-change` | Large PRs | Fails on threshold breaches or critical paths without an active plan. |

Reference:

```bash
python3 scripts/mutter.py --help
```

**Optional Git hook:** after clone, validate on commit: `git config core.hooksPath scripts/git-hooks` (when `.mutter/` and `scripts/mutter.py` exist).

**Cursor ↔ Claude sync (Mutter development):**

```bash
python3 scripts/sync_cursor_skills.py
```

With **`--check-cursor-sync`** on `ci`, `mutter-cursor/skills` must match the canonical `mutter-claude/skills`.

---

## `.mutter/` layout (orientation)

A concise map lives in [`.mutter/core/project.md`](.mutter/core/project.md): `index/`, `architecture/`, `tasks/`, `plans/`, `state/`, `workflows/`, `memory/`, `logs/`, `brainstore/`, and more. The idea is **incremental updates** and **small context shards**, not the whole repository in one file.

---

## Community

- **Author:** [Ventsislav Arnaudov](https://varnaudov.com)
- **Repository:** [github.com/arnaudovproject/mutter](https://github.com/arnaudovproject/mutter)
- **Issues and ideas:** [Issues](https://github.com/arnaudovproject/mutter/issues)

If you know ecosystems like [Superpowers](https://github.com/obra/superpowers) — where skills encode **process**, not casual tips — Mutter is in a similar **idea space**: the filesystem coordinates work and skills compose; Mutter is nonetheless a **separate product**, focused on `.mutter/` indexes, tasks, plans, and parity across Claude, Cursor, Codex, and OpenCode.

---

## License

MIT — stated in `package.json` and in the plugin manifests under `mutter-claude/` and `mutter-cursor/`.
