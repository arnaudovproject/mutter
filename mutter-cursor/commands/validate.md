---
name: mutter-validate
description: Run Mutter workspace CLI checks (tasks, plans, optional full CI) from the repo root.
---

# mutter validate

Run **disk-side validation** for `.mutter/` tasks and plans using `scripts/mutter.py` (must exist at the repository root — installed by **bootstrap** from `mutter-claude/templates/scripts/mutter.py` when missing).

## What to run

From the **repository root** (directory that contains `.mutter/`):

1. **Quick check (typical before hand-off or after editing tasks/plans)**  
   `python3 scripts/mutter.py validate-tasks`  
   `python3 scripts/mutter.py validate-plans`

2. **Single active pointers** (uses `.mutter/state/current.json`)  
   `python3 scripts/mutter.py validate-task`  
   `python3 scripts/mutter.py validate-plan`

3. **Status / scan digest**  
   `python3 scripts/mutter.py status`  
   `python3 scripts/mutter.py scan-state`

4. **Mutter plugin repo only** (skill cross-references + full `ci` bundle)  
   `python3 scripts/mutter.py check-skill-refs`  
   `python3 scripts/mutter.py ci --check-cursor-sync`

5. **Cursor palette (same CLI):** **mutter-preflight**, **mutter-context-pack**, **mutter-governance** — see `mutter-cursor/commands/*.md`.

## Agent instructions

1. Resolve repo root (folder containing `.mutter/`).
2. If `scripts/mutter.py` is missing, say so and suggest **bootstrap** or copying from the plugin template.
3. Run the narrowest commands the user asked for; print paths + exit codes; do not paste huge logs into chat.

For full command reference, see **`docs/mutter-workspace-tools-audit.md`** in the Mutter repository.

For slash-style usage in Claude Code, there is no separate validate skill — use **`/mutter:task`** (Automation section) and **`/mutter:plan`** for workflow text, or run the CLI above in the terminal.
