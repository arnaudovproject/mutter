# Claude Instructions (Mutter)

Read `.mutter/core/project.md` first.

## Rules

- Use `.mutter/index/` for navigation; never load the whole repository into context.
- Follow `.mutter/rules/` and `.mutter/architecture/` for decisions and boundaries.
- Follow Mutter workflows under `.mutter/workflows/` when applicable.
- Prefer **incremental** context: open only files listed for the active task or plan.
- Before **web search** for official language/framework/database documentation, check **`.mutter/memory/official-tech-docs-roadmap.md`** for a direct link (read one section only).
- Keep **this file small**; do not move bulk memory here—use `.mutter/`.
- **Multi-harness parity:** when you change or extend anything that affects how the Mutter plugins behave (skills, templates, manifests, OpenCode bootstrap, versions), do it **in parallel for every harness we ship** — `mutter-claude/`, `mutter-cursor/` (run `python3 scripts/sync_cursor_skills.py` after skill edits), `mutter-claude/.codex-plugin/`, and the repo-root OpenCode entry (`package.json`, `.opencode/`). Do not upgrade one harness and leave the others behind unless the task explicitly documents a harness-only exception.

## Commands

Use the Mutter plugin skills. In Claude Code, namespaced skills look like **`/mutter:<skill>`** (not a space). For example:

- `/mutter:scan` — incremental project scan
- `/mutter:brainstore` — structured idea → intelligence files
- `/mutter:task` — task create/update/split/execute (see skill body)
- `/mutter:plan` — planning with risks and affected files
- `/mutter:safe-edit` — explain-then-edit discipline
- `/mutter:review-diff` — architecture and quality review
- `/mutter:workers` — epic queue, multi-agent briefs, safe parallelism

## Safety

- Do not paste entire trees or unrelated modules into the transcript.
- Update `.mutter/tasks/`, `.mutter/architecture/decisions.md`, and `.mutter/metadata/scan-state.json` when your actions change project truth.
