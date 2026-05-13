---
name: dependencies
description: Map dependency relationships for a module or file using index shards and package manifests — incremental only.
---

# /mutter:dependencies

`$ARGUMENTS` is root path or module name.

## Steps

1. Start from `.mutter/index/dependencies.index.json` if present; augment from manifest files touching the root (package.json, go.mod, etc.).
2. Emit/update shard fragment; avoid O(repo) graph in one step—cap nodes per run (e.g. 40) and document continuation token in shard meta if truncated.

## Token rules

- Chat: summarized graph (text) ≤20 lines.
