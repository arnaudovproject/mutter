# Test command registry

Edit **`commands.json`** so `python3 scripts/mutter.py suggest-tests` can map changed files to commands.

Supported keys:

- **`by_extension`** — map file suffix (e.g. `".py"`) → list of shell commands.
- **`by_prefix`** — map path prefix → list of commands (longest prefix wins).
- **`path_globs`** — map glob → list of commands.
