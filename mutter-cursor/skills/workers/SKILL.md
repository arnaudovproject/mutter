---
name: workers
description: Epic and multi-worker orchestration — split huge goals into isolated worker briefs, durable state under .mutter/, token budgets, and safe parallelism (read-only vs serial writers).
---

# /mutter:workers

Use when a goal is **too large for one context**, may take **many turns or hours**, or the user wants **several agents** without drift or duplicated edits.

## Principles

1. **Coordinator** (this session, or a dedicated planning pass) owns the queue and merges outcomes. Workers do not silently redefine scope.
2. **Fresh brief per worker** — each dispatch gets a self-contained packet: objective, acceptance criteria, explicit path list (from `.mutter/index/` + plan), and forbidden actions. Do **not** paste the full chat history into a worker.
3. **State on disk** — after every worker: update `.mutter/tasks/` or the active `.mutter/plans/*` checklist, append `.mutter/logs/` if useful, point `.mutter/state/current.json` at the next package. Resume must work from files alone.
4. **Evidence before “done”** — each package lists verification (commands or checks). Coordinator runs or delegates verification, then ticks the step.

## Algorithm

1. **Normalize** — run or refresh `plan` so there is one epic plan under `.mutter/plans/` with **work packages**: small, ordered, each naming candidate files (not whole trees).
2. **Shard tasks** — use `task` `split` so each package is a task (or sub-steps) with links to the plan section. One package = one bounded objective.
3. **Dispatch** by role:
   - **Explore** — readonly reconnaissance (`analyze`, index shards, grep). No edits.
   - **Implement** — follows `safe-edit`; only files listed in the package.
   - **Review** — short pass over stated diff/files (`review-diff` discipline); may be a separate worker with **diff-only** context.
   - **Shell** — bounded commands (tests, format) when the harness allows.
4. **Integrate** — coordinator applies ordering: merge branches or sequential edits; resolve conflicts once, not in parallel writers.
5. **Checkpoint** — if stopping mid-epic, leave the next unchecked step + `active_task` / `active_plan` in `.mutter/state/current.json` so the next session picks up without re-reading the whole repo.

## Parallelism (safe)

- **Parallel OK:** disjoint **read-only** exploration (different subtrees), gathering deps/tests metadata, independent doc passes.
- **Serialize:** any two packages that touch the **same files**, migrations, or shared public API surface. Same rule as proven multi-agent workflows: **never** run multiple **writers** on overlapping files without explicit merge ownership.

## Token discipline

- Cap each worker brief: **max N files** (set N in the plan; typical 3–12), cite paths not file bodies in the coordinator chat.
- For official API/language/framework docs, point workers at **`.mutter/memory/official-tech-docs-roadmap.md`** (subsection only), not open-ended search.
- Worker returns **bullets + paths** to coordinator; long raw logs go under `.mutter/logs/`, not the main transcript.
- After edits, prefer `scan` delta (`changed_files`) over full rescans.

## Optional quality gate (heavy / risky packages)

Two lightweight passes, same or different workers:

1. **Spec / plan compliance** — checklist against the plan section (missing behavior, scope creep).
2. **Code quality** — style, tests, obvious defects.

Reuse `review-diff` patterns; keep reviewer context smaller than implementer context.

## Harness notes

- **Cursor:** use subagent **Task** with `readonly: true` for explore workers; await checkpoints before chaining writers.
- **Claude Code:** same idea — fresh subagent per package with constructed brief only.

## Bounded retries

- Coordinator may retry a failed verification or flaky check **once** with a narrowed scope; after two identical failures, pause, log under `.mutter/logs/`, and update the plan/task with the new evidence—avoid tight tool loops.

## Red flags

- Skipping plan/task updates between packages (“we’ll remember”).
- Feeding workers whole-directory listings or unconstrained “read the codebase”.
- Parallel implementers on the same branch touching the same modules.
- Declaring the epic done without running the plan’s verification steps.
