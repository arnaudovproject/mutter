---
name: architecture
description: Curate and update architecture documentation under .mutter/architecture — keep files small and cross-linked.
---

# /mutter:architecture

`$ARGUMENTS` describes the doc update (e.g. “document auth flow”, “refresh backend boundaries”).

## Scope

- Files: `overview.md`, `backend.md`, `frontend.md`, `database.md`, `infrastructure.md`, `event-flow.md`, `auth.md`, `deployment.md`, `decisions.md`.
- Prefer **append** or **surgical edits**; do not balloon any single file—split new detail into a sibling file when needed.

## ADRs

- New decisions go to `decisions.md` using the template in that file’s header.

## Token rules

- Read only the architecture file(s) you will edit plus one related index shard.
