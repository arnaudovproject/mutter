---
name: mutter-context-pack
description: Generate Mutter context-pack Markdown (state, task, plan, ADRs, ownership) for a new agent session.
---

# mutter context-pack

Emit a **single Markdown bundle** agents can paste or save before work.

From the **repository root**:

```bash
python3 scripts/mutter.py context-pack
```

Optional:

- Write to a file: `python3 scripts/mutter.py context-pack --out .mutter/context/last-pack.md`
- Override pointers: `--task PATH` / `--plan PATH` (same resolution rules as `validate-task` / `validate-plan`).

## Agent instructions

1. Resolve repo root; ensure `scripts/mutter.py` exists.
2. Prefer **`--out`** when the pack is large; otherwise print a short notice + path instead of pasting the full file into chat.

Reference: **`docs/mutter-workspace-tools-audit.md`**.
