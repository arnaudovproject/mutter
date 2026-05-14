---
name: explain
description: Explain a symbol, file, or behavior with minimal reads using .mutter/index and architecture shards.
---

# /mutter:explain

`$ARGUMENTS` is what to explain (path, symbol, or concept).

## Idempotent re-runs

If the same **`$ARGUMENTS`** was answered in this session or in **`.mutter/context/`** / **`.mutter/brainstore/`**, **point to the prior write** and only re-read if the user says code changed.

## Steps

1. Resolve the target via `.mutter/index/` if possible; else ask one clarifying question.
2. Read **only** the resolved files and one hop of imports/references.
3. Answer with: purpose, key collaborators, extension points, tests proving behavior (paths only).

## Token rules

- No large code quotations—summarize with pointers.
