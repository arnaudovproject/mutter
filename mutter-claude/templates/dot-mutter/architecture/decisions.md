# Architecture decisions (ADR-style)

Append newest decisions at the top. Keep each entry compact.

Numbered, machine-validated ADRs: **`.mutter/adr/*.md`** (see `python3 scripts/mutter.py validate-adr`).

## Template

```text
## YYYY-MM-DD — Title

Decision:
Reason:
Consequences:
```

## Log

## 2026-05-13 — Codex + OpenCode harness parity

Decision: Ship **Codex** via `mutter-claude/.codex-plugin/plugin.json` sharing `mutter-claude/skills/` with Claude; ship **OpenCode** via root `package.json` + `.opencode/plugins/mutter.js` registering the same skills path. Repo **`.agents/plugins/marketplace.json`** documents a local Codex marketplace entry for dogfooding.

Reason: One canonical skill tree; Codex/OpenCode docs and [superpowers](https://github.com/obra/superpowers) patterns favor manifest beside skills and git-backed OpenCode installs.

Consequences: `scripts/sync_cursor_skills.py` normalizes **`name`** in Claude frontmatter; CI `--check-cursor-sync` diffs **both** `mutter-claude/skills` and `mutter-cursor/skills`. Version bumps should touch Claude, Cursor, Codex manifests and root `package.json` together.

_(No numbered ADRs yet.)_
