---
name: mutter-governance
description: Run Mutter governance checks — staged secrets scan, large-change guard, optional ADR validation (aligns with git hook).
---

# mutter governance

Use this **before commit or push** when you want the same class of checks as the optional **git pre-commit** governance block (without replacing full CI).

From the **repository root**:

1. **Staged files — obvious secrets (best-effort)**  
   `python3 scripts/mutter.py scan-secrets --git-staged --max-files 500 --max-bytes 256000`

2. **Large / critical diff — requires `active_plan` when triggered**  
   `python3 scripts/mutter.py guard-large-change`

3. **Optional — ADRs on disk**  
   `python3 scripts/mutter.py validate-adr`

4. **Optional — readiness**  
   `python3 scripts/mutter.py preflight --check-acceptance-verify`

## Agent instructions

1. Run (1) and (2) at minimum when the user is about to commit; stop on non-zero exit and summarize errors (no log dumps).
2. If `scripts/mutter.py` is missing, suggest **bootstrap**.

**Git hook:** enable with `git config core.hooksPath scripts/git-hooks`. Set **`MUTTER_HOOK_SKIP_GOVERNANCE=1`** to skip `scan-secrets` + `guard-large-change` in the hook if a repo needs a lighter hook.

See **`docs/mutter-workspace-tools-audit.md`**.
