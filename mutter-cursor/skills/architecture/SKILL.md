---
name: architecture
description: Curate and update architecture documentation under .mutter/architecture — keep files small and cross-linked.
---

# /mutter:architecture

`$ARGUMENTS` describes the doc update (e.g. “document auth flow”, “refresh backend boundaries”).

## Idempotent re-runs

Before editing: **open only the target shard(s)** plus one related index entry. If the request **repeats** with the same intent and the files **already reflect** it, **report “no change”** and stop. Otherwise **append** or **surgical patch**—never rewrite a large markdown file from scratch unless the user asked for a full regen. Remove obsolete bullets when code or ADRs supersede them.

## Scope

- Files: `overview.md`, `backend.md`, `frontend.md`, `database.md`, `infrastructure.md`, `event-flow.md`, `auth.md`, `deployment.md`, `decisions.md`.
- Prefer **append** or **surgical edits**; do not balloon any single file—split new detail into a sibling file when needed.

## ADRs

- New decisions go to `decisions.md` using the template in that file’s header.

## Token rules

- Read only the architecture file(s) you will edit plus one related index shard.
