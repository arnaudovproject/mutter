# Ownership — CODEOWNERS

For GitHub/GitLab native reviews, prefer a repo-root **`CODEOWNERS`** file (see [GitHub docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)).

This folder holds **human + agent** readable ownership notes that stay next to `.mutter/` intelligence.

- **`modules.md`** — module → team, review policy, risk tier (see template table).

When automation references “owner”, point agents at **`modules.md`** first, then root `CODEOWNERS` if present.
