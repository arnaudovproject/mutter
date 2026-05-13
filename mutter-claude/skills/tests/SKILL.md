---
name: tests
description: Map tests relevant to a change or symbol using index shards and heuristics; never run the entire suite unless explicitly requested.
---

# /mutter:tests

`$ARGUMENTS` is feature area, path, or symbol.

## Steps

1. Pull candidate tests from index `tests` entries and naming heuristics (`*Test.php`, `*.spec.ts`, etc.) limited to the affected subtree.
2. Write/update `.mutter/plans/<slug>-tests.md` with commands + expected signals.
3. Run **narrow** tests when possible; log command + exit summary under `.mutter/logs/tests.log`.

## Token rules

- Do not paste full test file bodies in chat.
