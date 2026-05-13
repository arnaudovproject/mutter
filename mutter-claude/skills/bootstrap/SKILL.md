---
name: bootstrap
description: Initialize .mutter workspace in the current repository from the bundled template (explicit user action).
disable-model-invocation: true
---

# /mutter:bootstrap

Run only when the user wants to **install** the Mutter tree in a project that does not yet have `.mutter/`.

## Steps

1. If `.mutter/` already exists, stop and offer: merge, backup, or abort—do not overwrite without confirmation.
2. Copy the plugin template directory `templates/dot-mutter/` (from this plugin root) into the **repository root** as `.mutter/`, preserving subdirectory layout from the spec.
3. If `scripts/mutter.py` is missing at the **repository root**, copy `templates/scripts/mutter.py` from this plugin into `scripts/mutter.py` (create `scripts/` when needed). If it already exists, do not overwrite without confirmation—same policy as entry files.
4. If the repo lacks minimal entry files, create or merge:
   - Root `CLAUDE.md` from `templates/CLAUDE.md` (merge if file exists—keep existing non-Mutter content, prepend Mutter block if missing).
   - Ensure `.cursor/rules/mutter.mdc` exists with the same routing intent as `templates/CLAUDE.md` (Cursor). If `.cursor/rules/` is missing, create it.
5. Initialize `.mutter/metadata/scan-state.json` with zeros/nulls if not present after copy.
6. Log a one-line summary under `.mutter/logs/` with timestamp.

## After bootstrap

Tell the user to run `/mutter:scan` next, then use `/mutter:brainstore` or `/mutter:task` as needed. New tasks can start from **`.mutter/templates/TASK.md`** (copy into `tasks/current/`). When `scripts/mutter.py` is present, they can run `python3 scripts/mutter.py validate-task` / `validate-plan`, **`preflight`**, or **`context-pack`** before hand-off or in CI for soft enforcement.
