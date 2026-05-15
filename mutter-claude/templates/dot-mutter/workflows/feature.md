# Workflow: feature

1. When **`.mutter/prd/PRD.md`** exists, skim Goals / Functional requirements so scope stays aligned; update PRD if product intent changed (**`/mutter:prd`**).
2. Read `.mutter/architecture/overview.md` and relevant index shards.
3. `/mutter:brainstore` or refresh domain notes if the feature is new ground.
4. `/mutter:plan` with scope; list affected files and risks.
5. `/mutter:task` split into verifiable steps under `.mutter/tasks/current/`.
6. `/mutter:safe-edit` per step; run tests as defined in the task.
7. `/mutter:review-diff`; update `architecture/decisions.md` if boundaries changed.
