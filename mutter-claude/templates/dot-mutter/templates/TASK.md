# Task: <short title>

## Meta

- **Status:** `draft` | `ready` | `in_progress` | `blocked` | `done`
- **Active plan (optional):** `.mutter/plans/<file>.md`
- **Parent / split from (optional):** link to related task file

## Summary

One or two sentences: what changes and why.

## Scope

**In**

- …

**Out**

- …

## Affected

- **Domains:** e.g. backend, frontend, infra
- **Files (explicit paths):** list only what this task should touch; expand via `split` if the list grows
- **Index keys (optional):** which `.mutter/index/*.json` entries matter

## Acceptance (definition of done)

Mechanically checkable outcomes only (no vague “looks good”).

- [ ] …
- [ ] …

## Verify

Simple commands, one invocation each (no pipes / `&&` chains in a single line unless your shell skill documents it).

```text
# e.g.
npm run lint --workspace=packages/foo
npm test -- path/to/file.test.ts
```

## Steps

Do **one** step per agent turn unless the user explicitly asks otherwise.

- [ ] **Step 1 —** …
  - **Read:** `path/a`, `path/b`; shard: `index/....json` (keys: …)
  - **Acceptance:** …
  - **Notes:** …

- [ ] **Step 2 —** …
  - **Read:** …
  - **Acceptance:** …

## Execution log (optional)

Append one line per completed step: ISO date, step id, outcome. After updating checkboxes, run **`python3 scripts/mutter.py sync-task-progress`** so `state/current.json` stays aligned.
