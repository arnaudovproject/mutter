---
name: safe-edit
description: Safe editing workflow — explain changes, risks, architecture and dependency impact before applying minimal diffs.
---

# /mutter:safe-edit

Goal text or target files may arrive as **`$ARGUMENTS`**.

## Before any Write/Edit tool use

1. List **intended edits** as bullets (file + one-line intent per bullet).
2. List **risks** (data loss, API break, security) and **rollback** approach.
3. List **architecture** touchpoints (which `architecture/*.md` or ADRs apply).
4. List **dependencies** that might break (imports, shared types, configs).

## Execution

- Apply **smallest** change that satisfies the current step; prefer one logical commit worth of work per invocation unless user asked broader scope.
- After edits, run the narrowest relevant checks (unit slice, lint on touched files) if available. For noisy commands (full test suite, wide grep), capture full output under `.mutter/logs/` and summarize **3–12 lines + path** in chat instead of pasting everything.
- Record a short entry under `.mutter/diffs/` when the change is cross-cutting or risky.

## Token rules

- Do not paste full files back unless the user explicitly requested a full read.
- When showing a diff in chat, prefer **hunks** or summarized delta.
