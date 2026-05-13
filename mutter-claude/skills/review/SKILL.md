---
name: review
description: Run a structured review pass (lighter than review-diff) and store notes under .mutter/reviews when requested.
---

# /mutter:review

`$ARGUMENTS` optional scope (files, area, or “current task”).

## Behavior

- If a formal diff review is needed, prefer delegating mental checklist to `/mutter:review-diff`.
- Otherwise produce a concise review memo under `.mutter/reviews/` with: scope, findings, follow-ups.

## Token rules

- Chat: max 10 bullets.
