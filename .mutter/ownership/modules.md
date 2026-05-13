# Module ownership

Use one row per security/review boundary. Expand as the codebase grows.

| Module / area | Owner | Review required | Risk |
|---------------|-------|-----------------|------|
| _(example)_ payments | backend-team | yes | high |
| _(example)_ docs | any | no | low |
| mutter plugins | maintainers | yes | medium |

**Agent rule:** do not edit **high** risk rows without an explicit **plan** (`active_plan`) and human review when your workflow requires it.
