# Workflow: refactor

1. Snapshot current architecture pointers (`snapshots/` optional).
2. `/mutter:plan` with migration steps and risk list.
3. Split `/mutter:task` so each step keeps diffs reviewable.
4. Prefer mechanical changes separated from behavior changes.
5. `/mutter:review-diff` against architecture and duplication rules.
