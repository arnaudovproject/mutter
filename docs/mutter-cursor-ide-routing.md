# Mutter (Cursor) — minimal routing

_Same intent as root `CLAUDE.md`. The **mutter** git repository does not track `.cursor/`; this file is the canonical text for “small Cursor entry” when you want it in docs or to copy into a consumer project as `.cursor/rules/mutter.mdc`._

Read `.mutter/core/project.md` before substantive work.

## Rules

- Use `.mutter/index/` for navigation; never load the whole repository into context.
- Obey `.mutter/rules/` and `.mutter/architecture/` for boundaries and ADRs.
- Use `.mutter/workflows/` for repeatable procedures.
- Prefer incremental reads: only files tied to the active task, plan, or scan delta.
- Before **web search** for official language/framework/database documentation, check **`.mutter/memory/official-tech-docs-roadmap.md`** for a direct link (read one section only).
- Keep **entry files small**; bulk knowledge lives under `.mutter/`.

## Plugin alignment

When the **Mutter** Cursor plugin is installed, use its skills/commands for Mutter workflows. In **Claude Code**, the same workflows are **`/mutter:<skill>`** (e.g. `/mutter:scan`). In Cursor, use commands like **mutter-scan**, **mutter-workers**, or ask the agent to follow the matching skill. Full skill index: Claude **`/mutter:help`**, Cursor **mutter-help** command or **help** skill.

## Safety

- No dumping unrelated modules, generated artifacts, or entire frameworks into chat.
- After material changes, update `.mutter/tasks/`, `.mutter/architecture/decisions.md`, and scan metadata as appropriate.
