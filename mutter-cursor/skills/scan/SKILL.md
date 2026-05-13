---
name: scan
description: Incremental project scan — frameworks, languages, entry points, tests, CI, Docker, domain hints; updates .mutter/index and metadata only for changed paths.
---

# /mutter:scan

Operate on the **open repository root**.

## Preconditions

- Read `.mutter/metadata/scan-state.json`.
- If missing, run logic equivalent to **bootstrap** (create defaults) or instruct user to `/mutter:bootstrap`.

## Algorithm

1. **Inventory** file paths with size and mtime; compute `sha256` per text file (skip giant binaries; record skip list in `.mutter/scans/<iso-date>-skipped.txt` if needed).
2. **Diff** against `file_hashes` in scan-state. Build `changed_files` list.
3. If `changed_files` is empty and `last_scan` exists, write a short log entry and exit early with summary (saves tokens).
4. **Reprocess only** changed files (+ always-refresh small manifest files like `package.json`, `composer.json`, `go.mod`, `Dockerfile`, `*.csproj`).
5. **Emit index shards** under `.mutter/index/` as small JSON (domain-split: backend, frontend, api, tests, routes, dependencies). Merge into existing shards; do not rewrite unrelated keys.
6. **Detect** at high level: languages, frameworks, test runners, CI, containers, obvious API layers, entity-like symbols (best-effort), risky paths (secrets, credentials patterns—report paths only).
7. Update `metadata/scan-state.json`: `last_scan` ISO timestamp, counts, new `file_hashes`, clear `changed_files` after successful merge.

## Outputs

- Optional human summary under `.mutter/scans/<date>-summary.md` (short bullet list, not full file listing).

## Token rules

- Never print full repository listings in chat.
- Cite only top-level stats and 3–5 representative new/changed paths.
- If the scan uses shell tools and output is large, write the raw log under `.mutter/scans/` or `.mutter/logs/` and return **digest only** in chat (exit code, counts, a few paths)—same idea as capped “exec digests” in heavier agent harnesses.
