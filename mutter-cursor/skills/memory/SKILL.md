---
name: memory
description: Maintain long-lived project memory under .mutter/memory — conventions, domain language, recurring workflows; use official-tech-docs-roadmap for doc URLs before web search.
---

# /mutter:memory

`$ARGUMENTS` is the memory operation (e.g. “add naming convention for DTOs”, “document catalog domain terms”).

## Official documentation roadmap

- The template ships **`memory/official-tech-docs-roadmap.md`**: languages, databases, frameworks, DevOps, ML — **official documentation links**.
- When looking up APIs or language behavior online, **grep or open the relevant section** in that file first; prefer listed URLs over generic search.
- Do **not** read the entire roadmap into chat; one heading/section only.

## Rules

- One topic per file (`conventions-php.md`, `domain-catalog.md`).
- Deduplicate: search existing `memory/` filenames before adding new shards.
- Link to code paths and tests, never store secrets.

## Token rules

- Chat: summarize what was added/changed in ≤5 bullets.
