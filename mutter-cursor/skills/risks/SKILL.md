---
name: risks
description: Produce or update a risk assessment for a change — store under .mutter/plans or .mutter/reviews as appropriate.
---

# /mutter:risks

`$ARGUMENTS` describes the change or links to a plan file.

## Output

- Short risk table: id, severity, likelihood, mitigation, owner (TBD ok).
- Persist to `.mutter/plans/<related-plan>-risks.md` if a plan exists; else `.mutter/reviews/<date>-risks.md`.

## Token rules

- Chat: show top 5 risks only.
