# Workflow: review

1. Load task/plan from `.mutter/state/current.json` if set.
2. `/mutter:review-diff` with checklist: architecture, security, tests, conventions.
3. Write outcome under `.mutter/reviews/` dated file.
