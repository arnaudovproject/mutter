---
name: mutter-bootstrap
description: Mutter workspace command — bootstrap (install or refresh via bootstrap-sync; see skill `bootstrap`).
---

# mutter bootstrap

Run the **bootstrap** workflow from the Mutter plugin.

1. Open `.mutter/core/project.md` for orientation.
2. Invoke the matching skill **bootstrap** (same name) so full instructions load.
3. For an **existing** `.mutter/`, prefer **`python3 scripts/mutter.py bootstrap-sync --dry-run`** then **`bootstrap-sync`** to pull updated templates and `mutter.py` without wiping tasks or architecture.

For slash-style usage in Claude Code, use `/mutter:bootstrap`. In Cursor, use the Command palette entry or ask the agent to follow the **bootstrap** skill.
