---
name: analyze
description: Deeper multi-file analysis for a hypothesis or bug — explicit file list first, then incremental reads.
---

# /mutter:analyze

`$ARGUMENTS` states the hypothesis or question.

## Steps

1. Propose an explicit **file list** (≤12 files) before bulk reading; justify each path in one line.
2. Read files in that list only; update `.mutter/context/<slug>.md` if the analysis will be reused.
3. Conclude with evidence-backed findings and unknowns.

## Token rules

- If the list would exceed 12 files, split into phases and write interim notes under `.mutter/plans/`.
