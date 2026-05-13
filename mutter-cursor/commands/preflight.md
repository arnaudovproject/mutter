---
name: mutter-preflight
description: Run Mutter preflight — readiness before AI work (state, task/plan, dirty git, large-change rules).
---

# mutter preflight

Run **`python3 scripts/mutter.py preflight`** from the **repository root** (folder containing `.mutter/` and `scripts/mutter.py`).

## Suggested flags

- **Before executing a task:**  
  `python3 scripts/mutter.py preflight --require-active-task --check-acceptance-verify`

- **Before a large or sensitive change:**  
  `python3 scripts/mutter.py preflight --require-active-task --check-acceptance-verify --require-plan-for-large`

- **Strict workspace (no uncommitted noise):**  
  add `--fail-on-dirty`

- **Expect a recent scan:**  
  add `--expect-scan-state`

- **CI-style (warnings fail):**  
  add `--warnings-as-errors`

## Agent instructions

1. Resolve repo root; if `scripts/mutter.py` is missing, point to **bootstrap** / template copy.
2. Run the narrowest command the user needs; report exit code and short stderr lines only.

See **`docs/mutter-workspace-tools-audit.md`** (Mutter repo) for the full CLI list.
