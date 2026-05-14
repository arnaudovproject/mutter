---
name: mutter-agent-cadence
description: Print or save the canonical Mutter skill vs scripts/mutter.py cadence for agents (when to run which command).
---

# mutter agent-cadence

From the **repository root** (directory containing `.mutter/` and `scripts/mutter.py`):

```bash
python3 scripts/mutter.py agent-cadence
```

Write to disk (recommended once per workspace for agents to open instead of re-deriving rules):

```bash
python3 scripts/mutter.py agent-cadence --out .mutter/context/agent-cadence.md
```

## Agent instructions

1. Run **`agent-cadence`** when onboarding a new thread, or when the user asks how Mutter fits together.
2. Pair with **`python3 scripts/mutter.py status`** immediately before **`/mutter:task execute`** or “continue”.
3. Do not paste the entire output into chat if the user only needs orientation — point to **`.mutter/context/agent-cadence.md`** after the first generation.

See **`docs/mutter-workspace-tools-audit.md`** in the Mutter repository for the full CLI list.
