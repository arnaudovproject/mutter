# Workflow: bugfix

1. Identify domain via `.mutter/index/`; read only related shards and tests.
2. Log repro in `.mutter/tasks/current/` task file.
3. Minimal `/mutter:plan` (one screen) with suspected files.
4. `/mutter:safe-edit`; add or adjust tests.
5. `/mutter:review-diff`; update scan metadata if public surfaces changed.
