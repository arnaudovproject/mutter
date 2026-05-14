---
name: bootstrap
description: Initialize or refresh Mutter workspace from the bundled template — new install, or plugin file sync without wiping project tasks/plans/architecture.
---

# /mutter:bootstrap

## A) First install (no `.mutter/` yet)

1. Copy the plugin template directory **`templates/dot-mutter/`** (from this plugin root) into the **repository root** as **`.mutter/`**, preserving subdirectory layout.
2. If **`scripts/mutter.py`** is missing at the **repository root**, copy **`templates/scripts/mutter.py`** into **`scripts/mutter.py`** (create `scripts/` when needed).
3. If the repo lacks minimal entry files, create or merge:
   - Root **`CLAUDE.md`** from **`templates/CLAUDE.md`** (merge if the file exists—keep existing non-Mutter content; prepend the Mutter block if missing).
   - Ensure **`.cursor/rules/mutter.mdc`** exists with the same routing intent as **`templates/CLAUDE.md`** (Cursor). Create **`.cursor/rules/`** when missing.
4. Initialize **`.mutter/metadata/scan-state.json`** only if absent after copy (do not clobber an existing scan ledger).
5. Log a one-line summary under **`.mutter/logs/`** with timestamp.

## B) Refresh / upgrade (`.mutter/` already exists)

When the user re-runs bootstrap to **pick up a newer plugin** (templates, workflows, quality gates, `mutter.py`, doc stubs):

1. **Do not delete** user-owned trees: **`tasks/`**, **`plans/*.md`**, **`architecture/`**, **`roadmap/*.md`**, **`brainstore/`** (beyond README stubs), **`memory/*.md`** (except shipped link index), **`index/`** shards produced by scan, **`state/`**, **`metadata/`** (especially **`scan-state.json`**), **`logs/*.log`**, **`context/`** bundles, **`reviews/`**, **`snapshots/`**, **`scans/`** digests.
2. From the repo root that contains **`.mutter/`**, run:

```bash
python3 scripts/mutter.py bootstrap-sync --dry-run   # preview
python3 scripts/mutter.py bootstrap-sync             # apply
```

3. If **`scripts/mutter.py`** is missing in the consumer repo, copy it once (step A2). **`bootstrap-sync`** installs/updates **`scripts/mutter.py`** when the source exists (default: **`mutter-claude/templates/scripts/mutter.py`** inside a Mutter clone; otherwise pass **`--mutter-py-source`**).
4. For template files outside the allowlist (e.g. **`boundaries.json`**, **`ownership/`**), **merge by hand** if the plugin added new guidance—`bootstrap-sync` intentionally skips files that are usually customized.

## Idempotent re-runs

If the user invokes bootstrap again with **no material change** in the plugin template, **`bootstrap-sync`** overwrites allowlisted paths with identical bytes—harmless. Prefer **`--dry-run`** first when unsure.

## After bootstrap

Tell the user to run **`/mutter:scan`** next, then **`/mutter:brainstore`** or **`/mutter:task`** as needed.

When **`scripts/mutter.py`** is present: **`validate-task`**, **`validate-plan`**, **`preflight`**, **`context-pack`**.
