---
name: context
description: Build or refresh small curated context bundles under .mutter/context for a feature, bug, or task (not whole-repo dumps).
---

# /mutter:context

`$ARGUMENTS` names the bundle id or topic (e.g. `billing-refactor`).

## Steps

1. Identify relevant index keys from `.mutter/index/*.json` using keywords from `$ARGUMENTS`.
2. Create or update `.mutter/context/<bundle>.md` containing:
   - Linked file paths (not full contents)
   - 5–15 bullet facts the agent must remember for this bundle
   - “Out of scope” list to prevent wandering reads
   - Optional **resume line**: pointer to `state/current.json` and the active task/plan filename so a new session can rehydrate without replaying chat
3. Never paste large file bodies into the bundle file.

## Chat output

- Confirm bundle path + bullet count only.
