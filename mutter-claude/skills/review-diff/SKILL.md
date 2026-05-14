---
name: review-diff
description: Senior-style diff review — architecture, security, correctness, tests, ops, and debt; structured output under .mutter/reviews with must-fix vs follow-ups.
---

# /mutter:review-diff

Input: **`$ARGUMENTS`** optional focus (path, PR id, commit range, or “working tree”).

## Preconditions

1. Resolve diff scope (**git** `HEAD`, branch range, or unstaged/staged); if ambiguous, ask **one** question.
2. From disk (incremental): relevant **`.mutter/index/*.json`** shards (infer from changed path prefixes), **`architecture/decisions.md`** (search by keyword; do not load entire repo), **`ownership/modules.md`** when present, active **task/plan** paths from **`state/current.json`** if set.
3. Optional CLI (repo root) when `scripts/mutter.py` exists — run **before** deep reasoning to narrow focus:
   - **`python3 scripts/mutter.py risk-check --from-git`** (or `--staged`)
   - **`python3 scripts/mutter.py suggest-tests --from-git`**

## Review dimensions (senior bar)

Work through each bucket; skip only when clearly N/A, and say so in the review file.

1. **Architecture & boundaries** — layering, public API vs internals, coupling, feature flags, config drift; cross-check **`boundaries.json`** / ADRs if present.
2. **Correctness & edge cases** — null/error paths, concurrency, idempotency, retries, numeric/date boundaries, backwards compatibility.
3. **Security** — authn/authz, injection (SQL/OS/template), path traversal, SSRF, deserialization, secrets in code/logs, unsafe defaults, PII logging, dependency risk (new transitive deps called out).
4. **Reliability & ops** — observability (metrics/logs/traces), rollout/rollback, migrations with safe order, feature kill-switches, resource limits/timeouts.
5. **Performance** — hot paths, N+1 queries, unbounded loops/allocation, unnecessary sync I/O on request paths.
6. **Tests** — behavior changes need automated proof at the right level (unit vs integration); flaky patterns; missing regression for fixed bugs.
7. **Maintainability** — naming, duplication, dead code, comment debt vs complexity, API docs for public surfaces.
8. **Conventions** — project **`memory/`**, lint/format, i18n/a11y if applicable.

## Severity rubric

| Level | Meaning |
|-------|---------|
| **Critical** | Security hole, data loss, broken authz, production outage risk — **block merge** until fixed or explicitly accepted with compensating controls documented. |
| **Major** | Correctness bug, serious tech debt, missing tests for risky behavior, boundary violation — **should fix** before merge unless narrow follow-up task is agreed. |
| **Minor** | Style, small refactors, non-blocking nits. |
| **Note** | Observations, education, future ideas. |

## Deliverable

Write **`.mutter/reviews/<YYYY-MM-DD>-review.md`** (or append a dated section to today’s file if the same PR is re-reviewed) containing:

- **Scope** — commits / diff stat / key paths (short).
- **Summary** — 3–6 bullets for maintainers.
- **Findings** — table or list: **Severity**, **Area** (security/architecture/…), **Location** (file:region or symbol), **Issue**, **Recommendation**.
- **Testing gap** — explicit list of what to run or add (`suggest-tests` output may be pasted summarized).
- **Must-fix before merge** — checklist referencing finding ids.
- **Follow-ups** — safe to defer if tracked; suggest **`/mutter:task create`** titles for each non-trivial follow-up.

If **Critical** findings exist: state **merge blocked** in chat and in the file until addressed or risk is formally accepted in writing (e.g. task note + owner).

## After the review (agent)

1. For each **Critical** / **Major** item: either fix in-session with **`/mutter:safe-edit`** or create a **task** with a single verifiable step.
2. Run the **narrowest** tests or checks that prove the fix; log long output under **`.mutter/logs/`**.
3. Re-run **`/mutter:review-diff`** on the updated diff when changes were substantial.

## Chat output

- At most **5** findings inline (highest severity first); link to the review file for the full list.
- One line: **“Merge recommendation: blocked / proceed with fixes / proceed”** with rationale.

## Token rules

- Do not paste large diffs inline; reference paths and describe behavior changes.
- Prefer **checklists and tables** in the written review file over prose walls in chat.
