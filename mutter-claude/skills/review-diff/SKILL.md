---
name: review-diff
description: Review diffs and changes for architecture violations, duplication, security, missing tests, and convention drift; write structured output under .mutter/reviews.
---

# /mutter:review-diff

Input: **`$ARGUMENTS`** optional focus (file, PR id, or “last commit”).

## Process

1. Determine diff scope (git or working tree). If unknown, ask one clarifying question.
2. Load relevant **index shards** and `architecture/decisions.md` sections (search by keyword, do not read entire repo).
3. Checklist:
   - Architecture boundaries respected?
   - Duplicated logic / dead code introduced?
   - Security (injection, authz, secrets, unsafe defaults)?
   - Tests added/updated where behavior changed?
   - Conventions from `.mutter/memory/` (if present)?
   - Oversized or risky edits that should be split?
4. Write `.mutter/reviews/<iso-date>-review.md` with **severity-tagged** findings (Critical / Major / Minor / Note).
5. If Critical issues exist, recommend **blocking** further execution until fixed.

## Chat output

- Top 5 findings max in chat; point to review file for the rest.
