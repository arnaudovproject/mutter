---
name: snapshot
description: Create point-in-time snapshots of index, architecture, or roadmap under .mutter/snapshots for major changes or releases.
---

# /mutter:snapshot

`$ARGUMENTS` lists targets, e.g. `index architecture` or `all`.

## Idempotent re-runs

If a snapshot for the **same slug + same day** already exists and **no source files changed** since its `manifest.json` mtime, **skip** creating a duplicate folder unless the user asked for a **forced** snapshot. Otherwise create a **new dated folder** only when there is new material to freeze.

## Steps

1. Create folder `.mutter/snapshots/<iso-date>-<slug>/`.
2. Copy or export **small** JSON/Markdown shards (not entire cache). Prefer symlinks only if the repo policy allows; otherwise copy trimmed files.
3. Record manifest `manifest.json` in that snapshot folder listing included files.

## Token rules

- Chat: return snapshot directory path + file count only.
