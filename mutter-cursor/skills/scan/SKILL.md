---
name: scan
description: Incremental full-project scan — hash diff vs scan-state, reprocess only changed paths; merge index shards; no-op when nothing changed.
---

# /mutter:scan

Operate on the **repository root where `.mutter/` is initialized** (the whole project tree under that root is in scope, excluding obvious noise like `node_modules/`, `.git/`, build outputs when you can detect them cheaply).

## Preconditions

- Read **`.mutter/metadata/scan-state.json`**.
- If missing, create defaults (or instruct **`/mutter:bootstrap`**) so the next scan can persist hashes.

## Idempotent re-runs

Running **`/mutter:scan` three times in a row** must **not** re-analyze the whole codebase if **nothing changed**:

1. Compare current file **mtime/size** (and **`sha256`** for text-like files) against **`file_hashes`** (or equivalent) in scan-state.
2. Build **`changed_files`** (and optionally “unchanged” counts). If **empty** and **`last_scan`** exists, **append a one-line log**, update nothing else (or only bump a `last_checked` field if you track it), and **exit early** with a short chat summary (“0 files changed”)—**do not** regenerate index prose or rescan binaries.
3. **Reprocess only** changed paths **plus** small “always refresh” manifests (`package.json`, `composer.json`, `go.mod`, `Dockerfile`, `*.csproj`, lockfiles you already list in scan-state policy).
4. **Merge** new observations into **existing** **`.mutter/index/*.json`** shards: **add/update/remove keys** for touched paths; **do not** discard unrelated entries. Same for domain summaries under **`.mutter/scans/`**—append a new summary file or patch the latest, but do not rewrite history unless the user asked for a clean rescan.
5. Update **`metadata/scan-state.json`**: new **`file_hashes`**, **`last_scan`**, counts, and **clear or trim `changed_files`** after a successful merge so the next run starts clean.

## Algorithm (full detail)

1. **Inventory** repo-relative paths (respect `.gitignore` / common skip dirs) with size and mtime; compute **`sha256`** per text-like file (skip giant binaries; record skips under **`.mutter/scans/<iso>-skipped.txt`** if useful).
2. **Diff** against persisted hashes in scan-state → **`changed_files`**.
3. If **`changed_files` is empty** → early exit (see above).
4. **Emit / patch index shards** under **`.mutter/index/`** as small JSON (domain-split: backend, frontend, api, tests, routes, dependencies). **Merge**; never replace a whole shard with `{}` unless the shard file was deleted by the user.
5. **Detect** at high level for **changed** files only: languages, frameworks, test runners, CI, containers, API layers, entity-like symbols (best-effort), risky paths (report paths only for secrets-like patterns).
6. Persist scan-state.

## Outputs

- Optional human summary under **`.mutter/scans/<date>-summary.md`** (short bullets: delta only).

## Token rules

- Never print full repository listings in chat.
- Cite only top-level stats and **3–5 representative** new/changed paths.
- Large tool output → **`.mutter/scans/`** or **`.mutter/logs/`** + digest in chat (exit code, counts, a few paths).
