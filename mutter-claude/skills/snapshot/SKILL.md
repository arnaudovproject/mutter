---
name: snapshot
description: Create point-in-time snapshots of index, architecture, or roadmap under .mutter/snapshots for major changes or releases.
---

# /mutter:snapshot

`$ARGUMENTS` lists targets, e.g. `index architecture` or `all`.

## Steps

1. Create folder `.mutter/snapshots/<iso-date>-<slug>/`.
2. Copy or export **small** JSON/Markdown shards (not entire cache). Prefer symlinks only if the repo policy allows; otherwise copy trimmed files.
3. Record manifest `manifest.json` in that snapshot folder listing included files.

## Token rules

- Chat: return snapshot directory path + file count only.
