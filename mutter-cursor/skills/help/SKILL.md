---
name: help
description: List Mutter slash commands and what each skill does (reference for /mutter namespace).
disable-model-invocation: true
---

# /mutter:help

Namespace is **`/mutter:<skill-folder>`** (plugin `name` is `mutter`).

## Core (most used first)

| Skill | Purpose |
|-------|---------|
| `bootstrap` | Create `.mutter/` from template **or** refresh plugin files via `bootstrap-sync` |
| `scan` | Incremental project scan + indexes |
| `task` | Create / update / split / execute tasks (one step per turn; `sync-task-progress` after ticks) |
| `status` | Task checklist dashboard (`tasks-status` CLI) |
| `plan` | Scoped plan with risks and affected files |
| `safe-edit` | Explain impact, then edit in small steps |
| `review-diff` | Senior-style diff review → `.mutter/reviews/` |
| `brainstore` | Idea → structured intelligence under `.mutter/brainstore/` |
| `prd` | Workspace **Product Requirements Document** at `.mutter/prd/PRD.md` (`prd-init`, `validate-prd`) |
| `roadmap` | Roadmap maintenance; empty args → align with architecture |
| `architecture` | Architecture files + ADRs |
| `workers` | Epic work: queue, multi-agent briefs, safe parallelism |

## Navigation & context

| Skill | Purpose |
|-------|---------|
| `context` | Curated context bundles |
| `memory` | Long-lived conventions; **`official-tech-docs-roadmap.md`** for official doc links (check before web search) |
| `workflow` | Pick or run a named workflow file |
| `snapshot` | Snapshot index/architecture/roadmap |
| `review` | Wrapper to structured review output |
| `explain` | Targeted explanation with minimal reads |
| `analyze` | Deeper analysis with explicit file list |
| `risks` | Risk register for a change |
| `dependencies` | Dependency graph slice |
| `tests` | Test mapping for a change |
| `affected` | Affected files/domains for a change |

Always keep **root** `CLAUDE.md` and **`.cursor/rules/mutter.mdc`** small; put bulk content under `.mutter/`.

**Cursor:** palette commands include **mutter-agent-cadence**, **mutter-validate**, **mutter-preflight**, **mutter-context-pack**, **mutter-governance**, and **mutter-status** (see `mutter-cursor/commands/` in this repo).

## Workspace CLI (optional)

If **`scripts/mutter.py`** exists at the repo root (installed by **bootstrap** when missing), run **`python3 scripts/mutter.py --help`**. **Session map:** **`agent-cadence`** (optional **`--out .mutter/context/agent-cadence.md`**). Common entrypoints: **`status`**, **`preflight`**, **`context-pack`**, **`tasks-status`**, **`sync-task-progress`**, **`validate-task`**, **`bootstrap-sync`**, **`validate-plans`**, **`prd-init`**, **`validate-prd`**, **`risk-check`**, **`suggest-tests`**, **`pr-template`**, **`scan-secrets`**, **`guard-large-change`**. Full reference: **`docs/mutter-workspace-tools-audit.md`**. Optional git hook: enable with `git config core.hooksPath scripts/git-hooks` after clone.
