---
name: context
description: Build or refresh small curated context bundles under .mutter/context for a feature, bug, or task (not whole-repo dumps).
---

# /mutter:context

`$ARGUMENTS` names the bundle id or topic (e.g. `billing-refactor`).

## Idempotent re-runs

If **`.mutter/context/<bundle>.md`** already exists and **`$ARGUMENTS`** maps to the same bundle, **read it first**. Refresh only stale bullets (e.g. paths removed from the repo, renamed modules); **retain** still-valid links. If nothing is stale, report “context bundle current” and skip.

## Steps

1. Identify relevant index keys from `.mutter/index/*.json` using keywords from `$ARGUMENTS`.
2. Create or update `.mutter/context/<bundle>.md` containing:
   - Linked file paths (not full contents)
   - 5–15 bullet facts the agent must remember for this bundle
   - “Out of scope” list to prevent wandering reads
   - Optional **resume line** (keep it one tight sentence): **`state/current.json`**, active task **path**, active plan path if any, the **next** unchecked **Steps** line (first line of that step), and the **Verify** fenced command(s) to re-run after edits — enough for a cold session to continue without transcript replay
3. Never paste large file bodies into the bundle file.

## Chat output

- Confirm bundle path + bullet count only.
