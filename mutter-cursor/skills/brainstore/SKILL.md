---
name: brainstore
description: Turn a raw product or technical idea into structured project intelligence under .mutter/brainstore (and links into architecture/roadmap when appropriate).
---

# /mutter:brainstore

User text after the command (or conversation goal) is captured as **`$ARGUMENTS`**.

## Idempotent re-runs

**List and skim** existing **`.mutter/brainstore/*.md`** (titles + first section) before writing. If **`$ARGUMENTS`** adds **nothing new** versus what is already captured, **do not duplicate**—link to the existing file(s) and stop. Otherwise **create a new small file** *or* **patch** the single best-matching existing file (prefer patch when the topic already exists). Never bulk-regenerate every brainstore file on each invocation.

## Input

- `$ARGUMENTS` — the idea, constraints, and success criteria.

## Process

1. Note gaps and contradictions only; do not reload every brainstore file into context.
2. Produce **small focused files** (one topic per file), for example:
   - `vision.md`, `domains.md`, `tech-stack.md`, `testing.md`, `deployment.md`, `roadmap.md`, `api-design.md`, `security.md`, `scaling.md`, `documentation.md`, `risks.md`
3. Each file: short sections, bullet-first, links to **future** code paths as hypotheses (mark *TBD* when unknown).
4. If decisions are firm enough, add or append ADR-style bullets to `.mutter/architecture/decisions.md` (do not duplicate long text—reference brainstore files).

## Token rules

- Cap new prose per file (~80 lines); split rather than grow monoliths.
- In chat, return a **table of files written** and 1-line purpose each—not full contents.
