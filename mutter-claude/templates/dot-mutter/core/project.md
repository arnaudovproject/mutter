# Mutter — project AI workspace (v1)

This directory (`.mutter/`) is the **persistent structured memory** for AI-assisted work on this repository. Entry points for humans and agents:

| Path | Purpose |
|------|---------|
| `core/project.md` | This file — orientation only |
| `metadata/scan-state.json` | Incremental scan bookkeeping |
| `index/` | Fast lookup shards (e.g. `backend.index.json`, `catalog.example.json`) |
| `architecture/` | Living architecture text + ADRs |
| `adr/` | Numbered ADRs (`python3 scripts/mutter.py validate-adr`) |
| `ownership/` | Module ownership / review policy for agents (`modules.md`) |
| `quality-gates/` | Definition-of-done profiles by work type (`validate-quality-gate`) |
| `testing/commands.json` | Test/lint command hints (`suggest-tests`) |
| `boundaries.json` | Optional import boundaries (`check-boundaries`; `.yml` needs PyYAML) |
| `roadmap/` | Features, milestones, debt |
| `tasks/` | `current/`, `planned/`, `blocked/`, `completed/` |
| `memory/` | Conventions, domain notes, long-lived facts; `official-tech-docs-roadmap.md` = official doc links (check before web search) |
| `workflows/` | `feature.md`, `bugfix.md`, etc. |
| `plans/` | Generated plans from `/mutter plan` |
| `reviews/` | Review outputs |
| `diffs/` | Notable diffs / migration records |
| `scans/` | Raw or partial scan payloads per run |
| `cache/` | Embeddings, graphs, token analysis (optional) |
| `logs/` | Scan/task/review logs |
| `brainstore/` | Output of `/mutter brainstore` |
| `prd/` | Workspace Product Requirements Document — **`PRD.md`** (`prd-init`, `validate-prd`, **`/mutter:prd`**) |
| `snapshots/` | Point-in-time copies of index/architecture/roadmap |
| `state/` | `current.json` — active task/plan/workflow + `execution_progress` (from `sync-task-progress`) |
| `context/` | Small curated context bundles (not whole-repo dumps) |
| `rules/` | Project-specific mutter rules shards |
| `templates/` | Local templates for tasks, PRD scaffold, plans |

## Principles

1. **No monolith files** — split by domain; link instead of paste. Exception: `memory/official-tech-docs-roadmap.md` is a **link index** for official docs; never load it whole into chat—open one section at a time.
2. **Incremental scans** — update `metadata/scan-state.json` and only reprocess changed paths.
3. **Token discipline** — load shards from `index/` and `context/` relevant to the active task.

## Operating posture (speed + accuracy, fewer tokens)

Mutter does not ship a separate agent runtime; behavior comes from **discipline on disk**. Borrow these ideas from spec-driven / context-engineered workflows (for example [GSD 2](https://github.com/gsd-build/gsd-2)) without copying its stack:

1. **Disk is the coordinator** — `state/current.json`, tasks, and plans must be enough to resume after a new session. Do not rely on long chat memory for scope or checklist state.
2. **One-window steps** — each task step should be completable with an explicit short file list + index keys in roughly one turn; if the step needs “the whole repo”, split or use `workers` with a fresh brief.
3. **Preload intent, not bulk** — before wide reads, open `state/current.json`, the active task/plan path, and only the shards those files name.
4. **Noisy work stays off-transcript** — long build/test/logs belong under `logs/` or `scans/` with a short digest in chat (paths + exit code + 3–8 lines), not full stdout in the conversation.
5. **Verify before “done”** — tasks and plans should name commands or observable checks; run the narrowest check that proves the step.
6. **Team-scale guardrails (optional)** — `python3 scripts/mutter.py preflight`, `context-pack`, `risk-check`, `guard-large-change`, and `scan-secrets` complement validation; keep config in `.mutter/testing/`, `ownership/`, `adr/`, `boundaries.json`.
7. **CLI cadence on disk** — `python3 scripts/mutter.py agent-cadence` (optional `--out .mutter/context/agent-cadence.md`) records *when* to run each subcommand so new sessions do not re-derive process from chat.
8. **Session context threshold** — after each **finished** task step (once disk is updated), agents run the **~40% checkpoint** in the **`task`** skill: prefer **`context-pack`** in a **new** session when usage is high; never interrupt a step mid-flight just because context grew.

## Root entry files

- **Claude:** repo-root `CLAUDE.md` (minimal) points here.
- **Cursor:** `.cursor/rules/mutter.mdc` in your project (minimal) points here — same routing intent as `CLAUDE.md`.

Both must stay small and identical in **routing intent**.
