# Workflow: migration

1. Document current and target in `.mutter/plans/`.
2. List data/API risks in plan; order steps to keep system runnable.
3. Use `/mutter:safe-edit` with explicit rollback notes per step.
4. Store migration diffs summary under `.mutter/diffs/`.
