---
name: explain
description: Explain a symbol, file, or behavior with minimal reads using .mutter/index and architecture shards.
---

# /mutter:explain

`$ARGUMENTS` is what to explain (path, symbol, or concept).

## Steps

1. Resolve the target via `.mutter/index/` if possible; else ask one clarifying question.
2. Read **only** the resolved files and one hop of imports/references.
3. Answer with: purpose, key collaborators, extension points, tests proving behavior (paths only).

## Token rules

- No large code quotations—summarize with pointers.
