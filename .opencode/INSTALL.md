# Installing Mutter for OpenCode

Prerequisites: [OpenCode](https://opencode.ai) installed.

## Install from this repository

Add Mutter to the `plugin` array in `opencode.json` (project or global under `~/.config/opencode/opencode.json`):

```json
{
  "plugin": ["mutter@git+https://github.com/arnaudovproject/mutter.git"]
}
```

Restart OpenCode. The package root is this repository; `package.json` points at `.opencode/plugins/mutter.js`, which registers `mutter-claude/skills` for discovery.

Verify with the skill tool (list skills, then load e.g. `scan`, `status`, or `help`).

OpenCode is installed separately from Claude Code or Codex — add the plugin in each harness you use.

## Pin a ref

```json
{
  "plugin": ["mutter@git+https://github.com/arnaudovproject/mutter.git#main"]
}
```

Use a tag or commit SHA after `#` when you want a fixed revision.

## References

- OpenCode plugins: https://opencode.ai/docs/plugins/
- Mutter spec: `SPEC.md` in this repo
