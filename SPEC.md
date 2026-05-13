# Mutter — Product specification

**Version:** 1.0  
**Name:** Mutter  
**Command namespace (Claude Code):** `/mutter:<skill>` — the plugin manifest `name` is `mutter`, so slash skills are **namespaced** (e.g. `/mutter:scan`, `/mutter:help`). The human shorthand “`/mutter scan`” in docs maps to **`/mutter:scan`** in Claude Code.

## Vision

Mutter is an **AI workspace orchestration system** for large software projects. It provides the same **architecture, workflows, memory model, task system, token strategy, indexing, planning, safety, and context rules** across **Claude Code**, **Cursor**, **OpenAI Codex**, and **OpenCode** (same skill bodies under `mutter-claude/skills/` where applicable).

Goal: enable AI to work on very large codebases with **high precision**, **low hallucination**, **low token use**, and **long-term architectural consistency**.

## What Mutter is

- An **AI project operating system** (not a thin code-generation snippet pack)
- A **persistent structured memory** layer under **`.mutter/`**
- A **token-efficient** context manager (incremental reads, index shards, no monolith docs)
- A **task / plan / review** orchestration layer
- An **AI-safe editing** discipline (explain → minimal diff → verify)

## Repository layout

| Path | Purpose |
|------|---------|
| `.mutter/` | **Project intelligence root** (in consumer repos). Indexed, sharded, incremental. |
| `CLAUDE.md` (repo root) | **Minimal** Claude entry: routes to `.mutter/`; stays small. |
| `mutter-cursor/rules/mutter.mdc` | **Minimal** Cursor routing (shipped with the Cursor plugin). Consumer projects may also use `.cursor/rules/mutter.mdc` (bootstrap); same intent as `CLAUDE.md`. |
| `docs/mutter-cursor-ide-routing.md` | Same routing text as `mutter.mdc` for reference (this repo does **not** track `.cursor/`). |
| `mutter-claude/` | Claude Code plugin (`.claude-plugin/plugin.json`, `skills/`, `templates/`). Also hosts **Codex** manifest at `.codex-plugin/plugin.json` pointing at the same `skills/` tree. |
| `mutter-cursor/` | Cursor plugin (`.cursor-plugin/plugin.json`, `rules/`, `skills/`, `commands/`). |
| `.cursor-plugin/marketplace.json` | Cursor **team marketplace** catalog at repo root — entry `mutter` → `./mutter-cursor` ([multi-plugin repos](https://cursor.com/docs/reference/plugins.md)). |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog — `mutter` → `./mutter-claude`. |
| `.agents/plugins/marketplace.json` | **Codex** repo-scoped marketplace ([build plugins](https://developers.openai.com/codex/plugins/build)) — `mutter` → `./mutter-claude`. Codex also reads `.claude-plugin/marketplace.json` when present. |
| `package.json` (repo root) | **OpenCode** git/npm plugin entry (`main` → `.opencode/plugins/mutter.js`); install with `mutter@git+https://github.com/arnaudovproject/mutter.git` per `.opencode/INSTALL.md`. |
| `.opencode/plugins/mutter.js` | OpenCode plugin: registers `mutter-claude/skills` on `config.skills.paths` and injects bootstrap text from `mutter-claude/templates/CLAUDE.md`. |
| `scripts/mutter.py` | **Workspace CLI** — validate tasks (`validate-task`, `validate-tasks`) and plans (`validate-plan`, `validate-plans`), `status`, `scan-state`, `check-skill-refs`, and `ci` (refs + tasks + plans + skill tree sync parity for Claude + Cursor). |
| `mutter-claude/templates/scripts/mutter.py` | **Bootstrap copy** — same script; bootstrap installs it to `<repo>/scripts/mutter.py` when missing. |

## `.mutter/` directory map

See `.mutter/core/project.md` for the canonical tree. Top-level dirs:

`core/`, `context/`, `architecture/`, `roadmap/`, `tasks/{current,completed,blocked,planned}/`, `memory/` (includes **`memory/official-tech-docs-roadmap.md`**: curated official doc links — consult before web search), `scans/`, `workflows/`, `rules/`, `plans/`, `reviews/`, `diffs/`, `index/`, `cache/`, `logs/`, `metadata/`, `brainstore/`, `templates/`, `snapshots/`, `state/`.

## Commands / skills (parity)

**Claude Code:** `/mutter:<folder>` for each folder under `mutter-claude/skills/`.

**Cursor:** same logical names under `mutter-cursor/skills/` plus **commands** in `mutter-cursor/commands/*.md` (`name: mutter-<skill>`).

**Codex:** skills are the same Markdown bodies as under `mutter-claude/skills/<folder>/SKILL.md` with YAML frontmatter `name` + `description` (and optional `disable-model-invocation`). Invoke via Codex **@** plugin/skill UI or prompts; see [Codex plugins](https://developers.openai.com/codex/plugins).

**OpenCode:** skills directory registered by the root `package.json` plugin; use OpenCode’s **skill** tool to list/load by name. See [OpenCode plugins](https://opencode.ai/docs/plugins/) and `.opencode/INSTALL.md`.

Core set: `bootstrap`, `help`, `scan`, `brainstore`, `task`, `plan`, `workers`, `safe-edit`, `review-diff`, plus navigation: `roadmap`, `architecture`, `context`, `memory`, `workflow`, `snapshot`, `review`, `explain`, `analyze`, `risks`, `dependencies`, `tests`, `affected`.

## Critical rules

1. **No monolith files** — never store whole-project memory in `CLAUDE.md`, global rules, or a single architecture file.
2. **Incremental scan** — track state in `.mutter/metadata/scan-state.json`; hash diff; reprocess only changed paths; patch index shards.
3. **Index-first navigation** — use `.mutter/index/*.json` shards; do not reload entire repos in chat.
4. **Small entry files** — `CLAUDE.md` and **`mutter-cursor/rules/mutter.mdc`** (or consumer `.cursor/rules/mutter.mdc`) contain routing + safety only.

## References

- Workspace CLI, hooks, and Cursor commands (**mutter-validate**, **mutter-preflight**, **mutter-context-pack**, **mutter-governance**): **`docs/mutter-workspace-tools-audit.md`**
- Claude plugins: [Create plugins](https://code.claude.com/docs/en/plugins)
- Cursor plugins: [Plugins](https://cursor.com/docs/plugins), [Plugins reference](https://cursor.com/docs/reference/plugins.md)
- Codex plugins: [Plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build)
- OpenCode plugins: [Plugins](https://opencode.ai/docs/plugins/)
- Public repo: https://github.com/arnaudovproject/mutter
- Plugin / harness development reference: **`docs/mutter-plugin-harness-reference.md`**
