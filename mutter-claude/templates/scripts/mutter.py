#!/usr/bin/env python3
"""
Mutter workspace helpers — soft enforcement for tasks, state, and plugin docs.

Inspired by validation patterns in:
  - https://github.com/gsd-build/gsd-2 (structured checks, CI-friendly scripts)
  - https://github.com/obra/superpowers (plugin hygiene scripts)

Usage (from repository root that contains `.mutter/`):
  python3 scripts/mutter.py --help
  python3 scripts/mutter.py validate-task
  python3 scripts/mutter.py validate-task --task .mutter/tasks/current/foo.md
  python3 scripts/mutter.py validate-tasks --include planned blocked
  python3 scripts/mutter.py check-skill-refs
  python3 scripts/mutter.py status
  python3 scripts/mutter.py scan-state
  python3 scripts/mutter.py validate-plan
  python3 scripts/mutter.py validate-plans
  python3 scripts/mutter.py preflight
  python3 scripts/mutter.py context-pack
  python3 scripts/mutter.py risk-check
  python3 scripts/mutter.py suggest-tests
  python3 scripts/mutter.py pr-template
  python3 scripts/mutter.py report-change
  python3 scripts/mutter.py validate-adr
  python3 scripts/mutter.py validate-quality-gate --type migration
  python3 scripts/mutter.py check-boundaries
  python3 scripts/mutter.py validate-migrations
  python3 scripts/mutter.py scan-secrets
  python3 scripts/mutter.py scan-todos
  python3 scripts/mutter.py guard-large-change
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Issue:
    path: str
    level: str  # "error" | "warn"
    message: str
    line: int | None = None


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)

    def add(self, path: str, level: str, message: str, line: int | None = None) -> None:
        self.issues.append(Issue(path, level, message, line))

    def exit_code(self, warnings_as_errors: bool) -> int:
        for i in self.issues:
            if i.level == "error":
                return 1
            if warnings_as_errors and i.level == "warn":
                return 1
        return 0

    def print(self) -> None:
        for i in self.issues:
            loc = f":{i.line}" if i.line is not None else ""
            print(f"{i.level.upper()} {i.path}{loc}: {i.message}", file=sys.stderr)
        if not self.issues:
            print("OK — no issues found.")


def find_repo_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(40):
        if (cur / ".mutter").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def parse_sections(md: str) -> dict[str, str]:
    """Split markdown on '## ' headings (first line may be # title)."""
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in md.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def section_body(sections: dict[str, str], prefix: str) -> str | None:
    for name, body in sections.items():
        if name.startswith(prefix):
            return body
    return None


def section_matching(sections: dict[str, str], fragment: str) -> str | None:
    """First section whose heading contains fragment (case-insensitive)."""
    frag = fragment.lower()
    for name, body in sections.items():
        if frag in name.lower():
            return body
    return None


_PLACEHOLDER_ITEM = re.compile(
    r"^\s*-\s*\[[ xX]\]\s*(\.{3}|…|\.{3}\s*|TBD|TODO|FIXME|placeholder.*|.*<short.*>.*)\s*$",
    re.I,
)
_VAGUE_ONLY = re.compile(r"^(…|\.{3}|—|-\s*|n/?a)\s*$", re.I)


def acceptance_items(body: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for i, line in enumerate(body.splitlines(), start=1):
        if re.match(r"^\s*-\s*\[[ xX]\]\s+", line):
            out.append((i, line))
    return out


def verify_fenced_commands(body: str) -> list[str]:
    """Lines inside first fenced block in Verify (excluding pure # comments and blanks)."""
    lines = body.splitlines()
    in_fence = False
    fence_buf: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_fence:
                break
            in_fence = True
            continue
        if in_fence:
            fence_buf.append(line)
    cmds: list[str] = []
    for line in fence_buf:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        cmds.append(s)
    return cmds


def extract_repo_paths_from_affected(affected_body: str, repo_root: Path) -> list[tuple[int, str]]:
    """Paths to check: backticks and bullets that look like repo-relative paths."""
    found: list[tuple[int, str]] = []
    for i, line in enumerate(affected_body.splitlines(), start=1):
        for m in re.finditer(r"`([^`]+\.(?:md|json|ts|tsx|js|jsx|py|rs|go|toml|yaml|yml))`", line):
            p = m.group(1).strip()
            if not p.startswith(("http://", "https://", "/")):
                found.append((i, p))
        for m in re.finditer(r"`([^`/][^`]*/[^`]+)`", line):
            p = m.group(1).strip()
            if p.endswith((".md", ".json")) or "/" in p:
                if not p.startswith(("http://", "https://")):
                    found.append((i, p))
    # De-dupe preserve order
    seen: set[tuple[int, str]] = set()
    out: list[tuple[int, str]] = []
    for item in found:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_read_paths_from_steps(steps_body: str) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for i, line in enumerate(steps_body.splitlines(), start=1):
        if "**Read:**" not in line and "**read:**" not in line.lower():
            continue
        for m in re.finditer(r"`([^`]+)`", line):
            p = m.group(1).strip()
            if "/" in p or p.endswith((".md", ".json", ".ts", ".tsx", ".py")):
                if not p.startswith(("http://", "https://")):
                    found.append((i, p))
    return found


def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    cand = (repo_root / raw).resolve()
    if cand.exists():
        return cand
    mutter = repo_root / ".mutter" / raw
    if mutter.exists():
        return mutter.resolve()
    return cand


def section_definition_of_done(sections: dict[str, str]) -> str | None:
    for name, body in sections.items():
        nl = name.lower().strip()
        if "definition" in nl and "done" in nl:
            return body
        if nl in ("done", "must-haves", "must haves", "definition of done"):
            return body
        if nl.startswith("definition ") and "done" in nl:
            return body
    return None


def validate_plan_file(plan_path: Path, repo_root: Path, report: Report) -> None:
    """Light structure check aligned with /mutter:plan deliverable."""
    try:
        rel = str(plan_path.relative_to(repo_root))
    except ValueError:
        rel = str(plan_path)
    if not plan_path.is_file():
        report.add(rel, "error", "plan file does not exist")
        return
    text = plan_path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    if len(sections) < 2:
        report.add(rel, "warn", "plan has very few ## sections — consider Goal, Affected, Risks, Testing, Definition of done")

    aff = section_matching(sections, "affected")
    if not aff or not aff.strip():
        report.add(rel, "error", "missing or empty section whose heading contains 'Affected'")
    else:
        for line_no, raw in extract_repo_paths_from_affected(aff, repo_root):
            resolved = resolve_repo_path(repo_root, raw)
            if not resolved.exists():
                report.add(
                    rel,
                    "error",
                    f"Affected path does not exist: {raw!r} (resolved {resolved})",
                    line_no,
                )

    risks = section_matching(sections, "risk")
    if not risks or len(risks.strip()) < 15:
        report.add(rel, "warn", "Risks section missing or very short — plan skill expects ranked risks + mitigations")

    testing = section_matching(sections, "testing") or section_matching(sections, "verify")
    if testing:
        cmds = verify_fenced_commands(testing)
        if not cmds:
            report.add(
                rel,
                "error",
                "Testing/Verify: must include a ``` fenced block with concrete commands (not prose placeholders)",
            )
    else:
        if not verify_fenced_commands(text):
            report.add(rel, "warn", "no Testing/Verify heading and no fenced command block in file — add how to assert success")

    dod = section_definition_of_done(sections)
    if not dod or len(dod.strip()) < 10:
        report.add(rel, "warn", "Definition of done / must-haves section missing or too short")


def validate_task_file(
    task_path: Path,
    repo_root: Path,
    *,
    check_step_reads: bool,
    report: Report,
) -> None:
    try:
        rel = str(task_path.relative_to(repo_root))
    except ValueError:
        rel = str(task_path)
    if not task_path.is_file():
        report.add(rel, "error", "task file does not exist")
        return
    text = task_path.read_text(encoding="utf-8")
    sections = parse_sections(text)

    acc = section_body(sections, "Acceptance")
    if not acc:
        report.add(rel, "error", "missing '## Acceptance' section")
    else:
        items = acceptance_items(acc)
        if not items:
            report.add(rel, "error", "Acceptance has no '- [ ]' checklist items")
        for line_no, line in items:
            rest = re.sub(r"^\s*-\s*\[[ xX]\]\s*", "", line).strip()
            if len(rest) < 6 or _VAGUE_ONLY.match(rest) or _PLACEHOLDER_ITEM.match(line):
                report.add(rel, "warn", f"Acceptance item looks placeholder or too vague: {rest!r}", line_no)

    ver = section_body(sections, "Verify")
    if not ver:
        report.add(rel, "error", "missing '## Verify' section")
    else:
        cmds = verify_fenced_commands(ver)
        if not cmds:
            report.add(
                rel,
                "error",
                "Verify: must include a ``` fenced block with real shell commands (not prose like 'looks good')",
            )

    aff = section_body(sections, "Affected")
    if not aff:
        report.add(rel, "warn", "missing '## Affected' section")
    else:
        for line_no, raw in extract_repo_paths_from_affected(aff, repo_root):
            resolved = resolve_repo_path(repo_root, raw)
            if not resolved.exists():
                report.add(
                    rel,
                    "error",
                    f"Affected path does not exist: {raw!r} (resolved {resolved})",
                    line_no,
                )

    if check_step_reads:
        st = section_body(sections, "Steps")
        if st:
            for line_no, raw in extract_read_paths_from_steps(st):
                resolved = resolve_repo_path(repo_root, raw)
                if not resolved.exists():
                    report.add(
                        rel,
                        "warn",
                        f"Steps **Read:** path missing: {raw!r}",
                        line_no,
                    )


def load_state(repo_root: Path) -> dict:
    p = repo_root / ".mutter" / "state" / "current.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def resolve_plan_arg(repo_root: Path, plan_arg: str | None) -> Path | None:
    if plan_arg:
        raw = Path(plan_arg)
        if raw.is_file():
            return raw.resolve()
        candidates = [
            repo_root / plan_arg,
            repo_root / ".mutter" / plan_arg,
            repo_root / ".mutter" / "plans" / plan_arg,
            repo_root / ".mutter" / "plans" / Path(plan_arg).name,
        ]
        for c in candidates:
            if c.is_file():
                return c.resolve()
        return None
    state = load_state(repo_root)
    ap = state.get("active_plan")
    if not ap:
        return None
    s = str(ap).strip().lstrip("./")
    return resolve_plan_arg(repo_root, s)


def resolve_task_arg(repo_root: Path, task_arg: str | None) -> Path | None:
    if task_arg:
        raw = Path(task_arg)
        if raw.is_file():
            return raw.resolve()
        cand = (repo_root / task_arg).resolve()
        if cand.is_file():
            return cand
        return (repo_root / ".mutter" / task_arg).resolve() if (repo_root / ".mutter" / task_arg).is_file() else None

    state = load_state(repo_root)
    at = state.get("active_task")
    if not at:
        return None
    return resolve_task_arg(repo_root, str(at))


def cmd_validate_task(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    tp = resolve_task_arg(repo_root, args.task)
    if not tp or not tp.is_file():
        print(
            "ERROR: no task file. Pass --task PATH or set active_task in .mutter/state/current.json",
            file=sys.stderr,
        )
        return 1
    validate_task_file(tp, repo_root, check_step_reads=args.deep, report=report)
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_validate_tasks(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    roots = [repo_root / ".mutter" / "tasks" / d for d in args.include]
    for base in roots:
        if not base.is_dir():
            continue
        for md in sorted(base.glob("*.md")):
            if md.name == "README.md":
                continue
            validate_task_file(md, repo_root, check_step_reads=args.deep, report=report)
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_validate_plan(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    pp = resolve_plan_arg(repo_root, args.plan)
    if not pp or not pp.is_file():
        print(
            "ERROR: no plan file. Pass --plan PATH or set active_plan in .mutter/state/current.json",
            file=sys.stderr,
        )
        return 1
    validate_plan_file(pp, repo_root, report)
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_validate_plans(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    base = repo_root / ".mutter" / "plans"
    if not base.is_dir():
        report.add(str(base), "warn", ".mutter/plans directory missing — nothing to validate")
        report.print()
        return report.exit_code(args.warnings_as_errors)
    for md in sorted(base.glob("*.md")):
        if md.name == "README.md":
            continue
        validate_plan_file(md, repo_root, report)
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_status(_args: argparse.Namespace, repo_root: Path) -> int:
    state_path = repo_root / ".mutter" / "state" / "current.json"
    print(f"repo_root: {repo_root}")
    print(f"state file: {state_path}")
    if state_path.is_file():
        data = json.loads(state_path.read_text(encoding="utf-8"))
        print(json.dumps(data, indent=2))
        at = data.get("active_task")
        if at:
            tp = resolve_task_arg(repo_root, str(at))
            if tp and tp.is_file():
                print(f"\nresolved active task: {tp}")
                head = "\n".join(tp.read_text(encoding="utf-8").splitlines()[:25])
                print("\n--- first 25 lines ---\n" + head)
            else:
                print(f"\nWARN: active_task {at!r} does not resolve to an existing file", file=sys.stderr)
        ap = data.get("active_plan")
        if ap:
            pp = resolve_plan_arg(repo_root, str(ap))
            if pp and pp.is_file():
                print(f"\nresolved active plan: {pp}")
                head = "\n".join(pp.read_text(encoding="utf-8").splitlines()[:20])
                print("\n--- plan first 20 lines ---\n" + head)
            else:
                print(f"\nWARN: active_plan {ap!r} does not resolve to an existing file", file=sys.stderr)
    else:
        print("(no current.json)")
    return 0


def cmd_scan_state(_args: argparse.Namespace, repo_root: Path) -> int:
    p = repo_root / ".mutter" / "metadata" / "scan-state.json"
    if not p.is_file():
        print(f"No scan state at {p}", file=sys.stderr)
        return 1
    data = json.loads(p.read_text(encoding="utf-8"))
    changed = data.get("changed_files") or data.get("changed") or []
    if isinstance(changed, list):
        print(f"changed_files ({len(changed)}):")
        for f in changed[:200]:
            print(f"  {f}")
        if len(changed) > 200:
            print(f"  ... and {len(changed) - 200} more")
    else:
        print(json.dumps(data, indent=2)[:8000])
    return 0


# --- Skill .md reference check (adapted from gsd-build/gsd-2 check-skill-references) ---


def _should_validate_md_ref(ref: str) -> bool:
    if not ref.endswith(".md"):
        return False
    if ref.startswith(("http://", "https://")):
        return False
    if ref.startswith("~"):
        return False
    if any(c in ref for c in "*{}"):
        return False
    if re.search(r"\{[^}]+\}", ref):
        return False
    if re.match(r"^\.\w+$", ref):
        return False
    if ref.startswith("path/to/"):
        return False
    if ref.startswith("/"):
        return False
    return ref.startswith(("./", "../", "references/", "workflows/", "scripts/", "templates/"))


def _extract_md_refs(content: str) -> list[tuple[int, str]]:
    refs: list[tuple[int, str]] = []
    lines = content.splitlines()
    in_code = False
    for i, line in enumerate(lines, start=1):
        if re.match(r"^(\s*)(`{3,}|~{3,})", line):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in re.finditer(r"\[(?:[^\]]*)\]\(([^)]+)\)", line):
            raw = m.group(1).strip().split("#", 1)[0].strip()
            if _should_validate_md_ref(raw):
                refs.append((i, raw))
        for m in re.finditer(r"`([^`]+\.md(?:#[^`]*)?)`", line):
            raw = m.group(1).strip().split("#", 1)[0].strip()
            if _should_validate_md_ref(raw):
                refs.append((i, raw))
    return refs


def _collect_md_files(root: Path) -> list[Path]:
    out: list[Path] = []
    if not root.is_dir():
        return out
    for p in root.rglob("*.md"):
        if "node_modules" in p.parts:
            continue
        out.append(p)
    return sorted(out)


def _resolve_md_ref(md_path: Path, ref: str, repo_root: Path) -> Path:
    """Resolve relative skill refs: next to the .md file, then from repo root (monorepo)."""
    cand = (md_path.parent / ref).resolve()
    if cand.is_file():
        return cand
    cand2 = (repo_root / ref).resolve()
    if cand2.is_file():
        return cand2
    # `templates/...` in skills often means the sibling plugin package (mutter-claude / mutter-cursor).
    if ref.startswith("templates/"):
        for plugin in ("mutter-claude", "mutter-cursor"):
            cand3 = (repo_root / plugin / ref).resolve()
            if cand3.is_file():
                return cand3
    return cand


def cmd_check_skill_refs(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    dirs = [repo_root / d for d in args.skill_roots]
    broken = 0
    checked = 0
    for skills_root in dirs:
        if not skills_root.is_dir():
            report.add(str(skills_root), "warn", "skills directory missing — skip")
            continue
        for md in _collect_md_files(skills_root):
            text = md.read_text(encoding="utf-8")
            for line, ref in _extract_md_refs(text):
                checked += 1
                target = _resolve_md_ref(md, ref, repo_root)
                if not target.is_file():
                    rel_md = md.relative_to(repo_root)
                    report.add(str(rel_md), "error", f'broken .md ref "{ref}"', line)
                    broken += 1
    report.print()
    if broken:
        print(f"\n{broken} broken reference(s), {checked} checked.", file=sys.stderr)
    else:
        print(f"All skill .md references OK ({checked} checked).")
    return 1 if broken else 0


def cmd_ci(args: argparse.Namespace, repo_root: Path) -> int:
    """Run repo hygiene checks (CI entrypoint)."""
    exe = sys.executable
    script = Path(__file__).resolve()
    task_cmd = [exe, str(script), "validate-tasks"]
    if args.strict_tasks:
        task_cmd.append("--warnings-as-errors")
    plan_cmd = [exe, str(script), "validate-plans"]
    if args.strict_tasks:
        plan_cmd.append("--warnings-as-errors")
    steps: list[list[str]] = [
        [exe, str(script), "check-skill-refs"],
        task_cmd,
        plan_cmd,
    ]
    rc = 0
    for cmd in steps:
        print("+", " ".join(cmd), flush=True)
        p = subprocess.run(cmd, cwd=repo_root)
        rc = max(rc, p.returncode)
    sync = repo_root / "scripts" / "sync_cursor_skills.py"
    if sync.is_file():
        print(f"+ {exe} {sync}", flush=True)
        p = subprocess.run([exe, str(sync)], cwd=repo_root)
        rc = max(rc, p.returncode)
        if args.check_cursor_sync:
            if not (repo_root / ".git").exists():
                print("WARN: not a git repo — skip mutter-cursor/skills diff check", file=sys.stderr)
            else:
                print(
                    "+ git diff --exit-code mutter-claude/skills mutter-cursor/skills",
                    flush=True,
                )
                p = subprocess.run(
                    ["git", "diff", "--exit-code", "mutter-claude/skills", "mutter-cursor/skills"],
                    cwd=repo_root,
                )
                if p.returncode != 0:
                    print(
                        "ERROR: skill trees out of sync — run python3 scripts/sync_cursor_skills.py",
                        file=sys.stderr,
                    )
                    rc = max(rc, 1)
    if args.with_governance:
        adr_cmd = [exe, str(script), "validate-adr"]
        print("+", " ".join(adr_cmd), flush=True)
        p = subprocess.run(adr_cmd, cwd=repo_root)
        rc = max(rc, p.returncode)
        sec_cmd = [exe, str(script), "scan-secrets", "--max-files", "600", "--max-bytes", "400000"]
        print("+", " ".join(sec_cmd), flush=True)
        p = subprocess.run(sec_cmd, cwd=repo_root)
        rc = max(rc, p.returncode)
        guard_cmd = [exe, str(script), "guard-large-change"]
        print("+", " ".join(guard_cmd), flush=True)
        p = subprocess.run(guard_cmd, cwd=repo_root)
        rc = max(rc, p.returncode)
    return rc


# --- Governance helpers (large repos, team scale) ---


def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=120,
    )


def git_is_repo(repo_root: Path) -> bool:
    return (repo_root / ".git").exists()


def git_porcelain(repo_root: Path) -> str:
    if not git_is_repo(repo_root):
        return ""
    p = _run_git(repo_root, "status", "--porcelain")
    if p.returncode != 0:
        return ""
    return p.stdout or ""


def git_changed_paths(repo_root: Path, *, staged: bool = False) -> list[str]:
    if not git_is_repo(repo_root):
        return []
    args = ["diff", "--name-only"]
    if staged:
        args.append("--cached")
    else:
        args.append("HEAD")
    p = _run_git(repo_root, *args)
    if p.returncode != 0:
        return []
    return [ln.strip() for ln in (p.stdout or "").splitlines() if ln.strip()]


def git_diff_shortstat(repo_root: Path) -> tuple[int, int, int]:
    """Return (files_changed, insertions, deletions) from unstaged+staged vs HEAD."""
    if not git_is_repo(repo_root):
        return (0, 0, 0)
    p = _run_git(repo_root, "diff", "--shortstat", "HEAD")
    if p.returncode != 0 or not (p.stdout or "").strip():
        return (0, 0, 0)
    s = p.stdout.strip()
    files = 0
    ins = 0
    dels = 0
    m = re.search(r"(\d+)\s+files? changed", s)
    if m:
        files = int(m.group(1))
    m = re.search(r"(\d+)\s+insertions?", s)
    if m:
        ins = int(m.group(1))
    m = re.search(r"(\d+)\s+deletions?", s)
    if m:
        dels = int(m.group(1))
    return (files, ins, dels)


def load_scan_changed(repo_root: Path) -> list[str]:
    p = repo_root / ".mutter" / "metadata" / "scan-state.json"
    if not p.is_file():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    changed = data.get("changed_files") or data.get("changed") or []
    if isinstance(changed, list):
        return [str(x) for x in changed if x]
    return []


def default_risk_rules() -> list[tuple[str, str]]:
    """Glob-ish patterns (substring / fnmatch) -> LOW | MEDIUM | HIGH."""
    return [
        ("migrations/*", "HIGH"),
        ("**/migrations/**", "HIGH"),
        ("**/doctrine/**", "HIGH"),
        ("auth/*", "HIGH"),
        ("**/auth/**", "HIGH"),
        ("payments/*", "HIGH"),
        ("**/payments/**", "HIGH"),
        ("infra/*", "HIGH"),
        ("**/infra/**", "HIGH"),
        ("**/infrastructure/**", "HIGH"),
        (".github/workflows/*", "HIGH"),
        ("**/schema.sql", "HIGH"),
        ("src/*", "MEDIUM"),
        ("apps/*", "MEDIUM"),
        ("packages/*", "MEDIUM"),
        ("docs/*", "LOW"),
        ("**/*.md", "LOW"),
        ("**/.mutter/**", "LOW"),
    ]


def path_risk_level(path: str, rules: list[tuple[str, str]] | None = None) -> str:
    rules = rules or default_risk_rules()
    norm = path.replace("\\", "/").lstrip("./")
    best = "LOW"
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    for pat, lvl in rules:
        if "*" in pat or "?" in pat or "[" in pat:
            if fnmatch.fnmatch(norm, pat) or fnmatch.fnmatch(norm, "**/" + pat.lstrip("./")):
                if order[lvl] > order[best]:
                    best = lvl
        else:
            if pat in norm or norm.startswith(pat.rstrip("*")):
                if order[lvl] > order[best]:
                    best = lvl
    return best


def risk_aggregate(paths: list[str]) -> tuple[str, list[str]]:
    worst = "LOW"
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    high_paths: list[str] = []
    for p in paths:
        r = path_risk_level(p)
        if order[r] > order[worst]:
            worst = r
        if r == "HIGH":
            high_paths.append(p)
    return worst, high_paths


def load_boundaries(repo_root: Path) -> dict[str, Any] | None:
    mut = repo_root / ".mutter"
    for fname in ("boundaries.json", "boundaries.yml", "boundaries.yaml"):
        p = mut / fname
        if not p.is_file():
            continue
        raw = p.read_text(encoding="utf-8")
        if fname.endswith(".json"):
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"ERROR: invalid JSON in {fname}: {e}", file=sys.stderr)
                return None
        try:
            import yaml  # type: ignore[import-untyped]

            try:
                data = yaml.safe_load(raw)
            except yaml.YAMLError as e:
                print(f"ERROR: invalid YAML in {fname}: {e}", file=sys.stderr)
                return None
        except ImportError:
            print(
                "ERROR: boundaries.yml requires PyYAML (`pip install pyyaml`) or use boundaries.json instead.",
                file=sys.stderr,
            )
            return None
        if not isinstance(data, dict):
            return None
        return data
    return None


def _boundary_module_roots(entry: dict[str, Any], name: str) -> list[str]:
    roots: list[str] = []
    if isinstance(entry.get("root"), str):
        roots.append(entry["root"].strip().strip("/"))
    if isinstance(entry.get("roots"), list):
        for r in entry["roots"]:
            if isinstance(r, str):
                roots.append(r.strip().strip("/"))
    if not roots:
        roots = [f"src/{name}", f"packages/{name}", name]
    return roots


def path_owner_module(path: str, modules: dict[str, Any]) -> str | None:
    norm = path.replace("\\", "/").lstrip("./")
    best: tuple[int, str] | None = None
    for name, meta in modules.items():
        if not isinstance(meta, dict):
            continue
        for root in _boundary_module_roots(meta, str(name)):
            root = root.strip("/")
            if norm == root or norm.startswith(root + "/"):
                ln = len(root)
                if best is None or ln > best[0]:
                    best = (ln, str(name))
    return best[1] if best else None


def check_file_boundary_violations(
    repo_root: Path,
    rel_path: str,
    modules: dict[str, Any],
) -> list[str]:
    """Heuristic: forbidden names must not appear in import/from strings."""
    issues: list[str] = []
    mod = path_owner_module(rel_path, modules)
    if not mod:
        return issues
    meta = modules.get(mod)
    if not isinstance(meta, dict):
        return issues
    forbidden = meta.get("forbidden") or meta.get("forbidden_imports") or []
    if not isinstance(forbidden, list):
        return issues
    fp = repo_root / rel_path
    if not fp.is_file():
        return issues
    try:
        text = fp.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return issues
    for fb in forbidden:
        if not isinstance(fb, str):
            continue
        token = re.escape(fb.replace("/", "."))
        if re.search(rf"(?:^|\n)\s*(?:from|import)\s+{token}\b", text, re.M):
            issues.append(f"{rel_path}: forbidden import '{fb}' for module '{mod}'")
        if re.search(rf"from\s+['\"]([^'\"]*{re.escape(fb)}[^'\"]*)['\"]", text):
            issues.append(f"{rel_path}: forbidden import path containing '{fb}' for module '{mod}'")
    return issues


def load_test_registry(repo_root: Path) -> dict[str, Any]:
    p = repo_root / ".mutter" / "testing" / "commands.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def suggest_commands_for_paths(registry: dict[str, Any], paths: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    by_ext = registry.get("by_extension") or {}
    by_prefix = registry.get("by_prefix") or {}
    globs = registry.get("path_globs") or {}

    if not isinstance(by_ext, dict):
        by_ext = {}
    if not isinstance(by_prefix, dict):
        by_prefix = {}
    if not isinstance(globs, dict):
        globs = {}

    prefix_items = sorted(by_prefix.items(), key=lambda kv: len(kv[0]), reverse=True)

    for raw in paths:
        norm = raw.replace("\\", "/").lstrip("./")
        ext = Path(norm).suffix.lower()
        if ext and isinstance(by_ext.get(ext), list):
            for c in by_ext[ext]:
                if isinstance(c, str) and c not in seen:
                    seen.add(c)
                    out.append(c)
        for pref, cmds in prefix_items:
            pref_n = pref.strip("/")
            if norm == pref_n or norm.startswith(pref_n + "/"):
                if isinstance(cmds, list):
                    for c in cmds:
                        if isinstance(c, str) and c not in seen:
                            seen.add(c)
                            out.append(c)
                break
        for pattern, cmds in globs.items():
            if not isinstance(pattern, str) or not isinstance(cmds, list):
                continue
            if fnmatch.fnmatch(norm, pattern) or fnmatch.fnmatch(norm, "**/" + pattern):
                for c in cmds:
                    if isinstance(c, str) and c not in seen:
                        seen.add(c)
                        out.append(c)
    return out


_SECRET_PATTERNS = [
    (re.compile(r"(?i)\bAPI_KEY\s*=\s*['\"]?[^\s'\"]{8,}"), "possible API_KEY assignment"),
    (re.compile(r"(?i)\bPRIVATE_KEY\s*=\s*['\"]?[^\s'\"]{8,}"), "possible PRIVATE_KEY assignment"),
    (re.compile(r"(?i)\bpassword\s*=\s*['\"][^'\"]{3,}['\"]"), "password= literal"),
    (re.compile(r"(?i)AKIA[0-9A-Z]{16}"), "AWS access key id pattern"),
    (re.compile(r"(?i)ghp_[a-zA-Z0-9]{20,}"), "GitHub token pattern"),
    (re.compile(r"(?i)xox[baprs]-[a-zA-Z0-9-]+"), "Slack token pattern"),
]


def scan_file_secrets(path: Path, report: Report, rel: str) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    for i, line in enumerate(text.splitlines(), start=1):
        if ".env" in line and not line.strip().startswith("#"):
            if re.search(r"(?i)\.env\s", line) and "example" not in line.lower():
                report.add(rel, "warn", "line may reference committing .env — verify secrets are not tracked", i)
        for rx, msg in _SECRET_PATTERNS:
            if rx.search(line):
                report.add(rel, "error", f"secrets scan: {msg}", i)


def collect_source_paths(repo_root: Path, max_files: int = 4000) -> list[Path]:
    skip = {".git", "node_modules", "vendor", ".mutter", ".mutter/cache"}
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fn in filenames:
            if len(out) >= max_files:
                return out
            suf = Path(fn).suffix.lower()
            if suf not in {
                ".py",
                ".ts",
                ".tsx",
                ".js",
                ".jsx",
                ".go",
                ".rs",
                ".java",
                ".php",
                ".md",
                ".yml",
                ".yaml",
                ".json",
                ".toml",
                ".env",
            }:
                continue
            out.append(Path(dirpath) / fn)
    return out


_TODO_PATTERN = re.compile(
    r"\b(TODO|FIXME|HACK|TEMP|@deprecated)\b",
    re.I,
)


def cmd_validate_adr(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    base = repo_root / ".mutter" / "adr"
    if not base.is_dir():
        report.add(str(base), "warn", "no .mutter/adr/ — create ADRs as 0001-title.md")
        report.print()
        return 0
    for md in sorted(base.glob("*.md")):
        if md.name.lower() == "readme.md":
            continue
        rel = str(md.relative_to(repo_root))
        text = md.read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:60])
        if not re.search(r"(?m)^#\s+.+", text):
            report.add(rel, "error", "ADR must start with '# Title' heading")
        if not re.search(r"(?im)^status:\s*(proposed|accepted|deprecated|superseded)\b", head):
            report.add(rel, "error", "ADR needs 'Status: proposed|accepted|deprecated|superseded' near top")
        for label in ("context", "decision", "consequences"):
            if not re.search(rf"(?im)^##\s+{label}\s*$", text):
                report.add(rel, "error", f"missing '## {label.capitalize()}' section heading")
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_validate_quality_gate(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    t = args.type.strip().lower().replace(" ", "_")
    path = repo_root / ".mutter" / "quality-gates" / f"{t}.md"
    if not path.is_file():
        report.add(str(path), "error", f"unknown quality gate type {args.type!r} — add {path.name}")
        report.print()
        return 1
    rel = str(path.relative_to(repo_root))
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 80:
        report.add(rel, "warn", "quality gate file is very short")
    if not re.search(r"(?im)^##\s+", text):
        report.add(rel, "error", "quality gate should use ## headings and bullet checklist")
    if not re.search(r"(?m)^\s*-\s+\[[ xX]\]", text):
        report.add(rel, "warn", "add '- [ ]' checklist items for mechanical gates")
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_risk_check(args: argparse.Namespace, repo_root: Path) -> int:
    paths: list[str] = []
    if args.paths:
        paths = [p.strip() for p in args.paths if p.strip()]
    elif args.from_scan:
        paths = load_scan_changed(repo_root)
    elif args.from_git:
        paths = git_changed_paths(repo_root, staged=args.staged)
    else:
        paths = git_changed_paths(repo_root, staged=False)
        if not paths:
            paths = load_scan_changed(repo_root)

    if not paths:
        print("No paths to score (git unchanged and scan-state empty). Pass --paths a b c", file=sys.stderr)
        return 0

    worst, highs = risk_aggregate(paths)
    print(f"Overall risk: **{worst}** ({len(paths)} path(s))")
    by: dict[str, list[str]] = {"HIGH": [], "MEDIUM": [], "LOW": []}
    for p in paths:
        by[path_risk_level(p)].append(p)
    for lvl in ("HIGH", "MEDIUM", "LOW"):
        ps = by[lvl]
        if not ps:
            continue
        print(f"\n### {lvl} ({len(ps)})")
        for p in ps[:200]:
            print(f"- `{p}`")
        if len(ps) > 200:
            print(f"- … and {len(ps) - 200} more")

    if worst == "HIGH" or highs:
        print(
            "\n---\n**HIGH risk:** include rollback plan, testing evidence, and reviewer in task/plan "
            "before merging."
        )
    return 0


def cmd_context_pack(args: argparse.Namespace, repo_root: Path) -> int:
    lines: list[str] = ["# Mutter context pack", ""]
    state = load_state(repo_root)
    lines.append("## State (.mutter/state/current.json)")
    lines.append("```json")
    lines.append(json.dumps(state, indent=2))
    lines.append("```")
    lines.append("")

    tp = resolve_task_arg(repo_root, args.task)
    if tp and tp.is_file():
        lines.append(f"## Active task (`{tp.relative_to(repo_root)}`)")
        lines.append("\n".join(tp.read_text(encoding="utf-8").splitlines()[:120]))
        lines.append("")
    else:
        lines.append("## Active task")
        lines.append("_(none resolved)_")
        lines.append("")

    pp = resolve_plan_arg(repo_root, args.plan)
    if pp and pp.is_file():
        lines.append(f"## Active plan (`{pp.relative_to(repo_root)}`)")
        lines.append("\n".join(pp.read_text(encoding="utf-8").splitlines()[:120]))
        lines.append("")
    else:
        lines.append("## Active plan")
        lines.append("_(none resolved)_")
        lines.append("")

    changed = load_scan_changed(repo_root)
    if not changed and git_is_repo(repo_root):
        changed = git_changed_paths(repo_root, staged=False)[:500]
    lines.append("## Changed paths (scan-state or git)")
    if changed:
        for c in changed[:300]:
            lines.append(f"- `{c}`")
        if len(changed) > 300:
            lines.append(f"- … {len(changed) - 300} more")
    else:
        lines.append("- _(none)_")
    lines.append("")

    adr_dir = repo_root / ".mutter" / "adr"
    if adr_dir.is_dir():
        lines.append("## ADRs (.mutter/adr/)")
        for md in sorted(adr_dir.glob("*.md"))[:30]:
            if md.name.lower() == "readme.md":
                continue
            peek = md.read_text(encoding="utf-8").splitlines()[:12]
            lines.append(f"### `{md.relative_to(repo_root)}`")
            lines.append("\n".join(peek))
            lines.append("")
    else:
        lines.append("## ADRs")
        lines.append("_(no .mutter/adr/)_")
        lines.append("")

    own = repo_root / ".mutter" / "ownership" / "modules.md"
    if own.is_file():
        lines.append("## Ownership (modules.md excerpt)")
        lines.append("\n".join(own.read_text(encoding="utf-8").splitlines()[:80]))
        lines.append("")
    else:
        lines.append("## Ownership")
        lines.append("_(add .mutter/ownership/modules.md)_")
        lines.append("")

    dec = repo_root / ".mutter" / "architecture" / "decisions.md"
    if dec.is_file():
        lines.append("## architecture/decisions.md (tail)")
        tail = dec.read_text(encoding="utf-8").splitlines()[-40:]
        lines.append("\n".join(tail))
        lines.append("")

    out = "\n".join(lines)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(out)
    return 0


def cmd_preflight(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    state = load_state(repo_root)
    if args.require_active_task:
        at = state.get("active_task")
        if not at:
            report.add(".mutter/state/current.json", "error", "active_task not set")
        else:
            tp = resolve_task_arg(repo_root, str(at))
            if not tp or not tp.is_file():
                report.add(".mutter/state/current.json", "error", f"active_task {at!r} does not resolve")

    if args.check_acceptance_verify:
        tp = resolve_task_arg(repo_root, None)
        if tp and tp.is_file():
            validate_task_file(tp, repo_root, check_step_reads=False, report=report)
        elif args.require_active_task:
            pass
        else:
            report.add("task", "warn", "no active task — cannot validate Acceptance/Verify")

    if args.require_plan_for_large:
        files, ins, dels = git_diff_shortstat(repo_root)
        large = files >= args.large_files or (ins + dels) >= args.large_lines
        crit = False
        for p in git_changed_paths(repo_root, staged=False):
            if path_risk_level(p) == "HIGH":
                crit = True
                break
        if large or crit:
            ap = state.get("active_plan")
            pp = resolve_plan_arg(repo_root, str(ap) if ap else None)
            if not pp or not pp.is_file():
                report.add(
                    ".mutter/state/current.json",
                    "error",
                    "large or high-risk change requires active_plan in state/current.json",
                )

    dirty = git_porcelain(repo_root)
    if dirty:
        if args.fail_on_dirty:
            report.add("git", "error", "working tree is dirty — commit/stash before preflight")
        else:
            report.add("git", "warn", "working tree has uncommitted changes")

    scan_p = repo_root / ".mutter" / "metadata" / "scan-state.json"
    if args.expect_scan_state and not scan_p.is_file():
        report.add(str(scan_p), "warn", "scan-state.json missing — run mutter scan workflow")

    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_report_change(args: argparse.Namespace, repo_root: Path) -> int:
    paths = git_changed_paths(repo_root, staged=False) if git_is_repo(repo_root) else []
    worst, _ = risk_aggregate(paths) if paths else ("LOW", [])
    print("# Post-change report\n")
    print("## What changed\n")
    print("_(fill: intent / behavior)_\n")
    print("## Files touched\n")
    if paths:
        for p in paths:
            print(f"- `{p}`")
    else:
        print("_(no git diff vs HEAD — list manually)_")
    print("\n## Tests run\n")
    print("```bash")
    print("# paste commands + outcomes")
    print("```\n")
    print("## Risks\n")
    print(f"- Scored worst path risk: **{worst}**")
    print("\n## Manual checks\n")
    print("- [ ] …\n")
    print("## Follow-ups\n")
    print("- …\n")
    return 0


def cmd_pr_template(args: argparse.Namespace, repo_root: Path) -> int:
    tp = resolve_task_arg(repo_root, args.task)
    pp = resolve_plan_arg(repo_root, args.plan)
    paths = git_changed_paths(repo_root, staged=args.staged) if git_is_repo(repo_root) else []
    worst, highs = risk_aggregate(paths) if paths else ("LOW", [])

    title = "PR: _(title)_"
    if tp and tp.is_file():
        first = tp.read_text(encoding="utf-8").splitlines()[:1]
        if first:
            title = first[0].lstrip("# ").strip()

    print("## Summary\n")
    print(f"{title}\n")
    print("## Related task\n")
    if tp:
        print(f"- `{tp.relative_to(repo_root)}`")
    else:
        print("- _(none)_")
    print("\n## Related plan\n")
    if pp:
        print(f"- `{pp.relative_to(repo_root)}`")
    else:
        print("- _(none)_")
    print("\n## Affected paths\n")
    for p in paths[:400]:
        print(f"- `{p}`")
    if len(paths) > 400:
        print(f"- … {len(paths) - 400} more")
    print("\n## Testing\n")
    print("```bash")
    reg = load_test_registry(repo_root)
    for c in suggest_commands_for_paths(reg, paths):
        print(c)
    if not paths:
        print("# add verify commands")
    print("```\n")
    print("## Risk level\n")
    print(f"- **{worst}**" + (" — touches critical areas" if highs else ""))
    print("\n## Rollback\n")
    print("_(how to revert / feature flag)_\n")
    if git_is_repo(repo_root):
        if args.staged:
            p = _run_git(repo_root, "diff", "--cached", "--stat", "HEAD")
        else:
            p = _run_git(repo_root, "diff", "--stat", "HEAD")
        if p.stdout:
            print("## Git diff stat\n")
            print("```text")
            print(p.stdout.strip()[:8000])
            print("```")
    return 0


def cmd_suggest_tests(args: argparse.Namespace, repo_root: Path) -> int:
    reg = load_test_registry(repo_root)
    if not reg:
        print(
            "No .mutter/testing/commands.json — add by_extension / by_prefix / path_globs (see template).",
            file=sys.stderr,
        )
        return 1
    if args.paths:
        paths = args.paths
    elif args.from_git:
        paths = git_changed_paths(repo_root, staged=args.staged)
    else:
        paths = git_changed_paths(repo_root, staged=False) or load_scan_changed(repo_root)
    cmds = suggest_commands_for_paths(reg, paths)
    if not cmds:
        print("No matching commands for current paths.", file=sys.stderr)
        return 0
    print("# Suggested commands\n")
    for c in cmds:
        print(c)
    return 0


def cmd_check_boundaries(args: argparse.Namespace, repo_root: Path) -> int:
    data = load_boundaries(repo_root)
    if data is None and any(
        (repo_root / ".mutter" / n).is_file() for n in ("boundaries.yml", "boundaries.yaml")
    ):
        return 1
    if not data:
        print("No .mutter/boundaries.json (or .yml with PyYAML). Nothing to check.", file=sys.stderr)
        return 0
    modules = data.get("modules")
    if not isinstance(modules, dict):
        print("ERROR: boundaries file must have top-level 'modules' object", file=sys.stderr)
        return 1
    paths = args.paths or git_changed_paths(repo_root, staged=args.staged)
    if not paths:
        print("No paths to check.", file=sys.stderr)
        return 0
    report = Report()
    for rel in paths:
        for msg in check_file_boundary_violations(repo_root, rel, modules):
            report.add(rel, "error", msg)
    report.print()
    return report.exit_code(args.warnings_as_errors)


_MIGRATION_HINTS = re.compile(
    r"(?i)(rollback|backup|backward|compat)",
)


def cmd_validate_migrations(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    mig_paths = [
        p
        for p in git_changed_paths(repo_root, staged=args.staged)
        if re.search(
            r"(^|/)(migrations/|doctrine/migrations/|db/migrate/|schema\.sql)",
            p.replace("\\", "/"),
        )
    ]
    if not mig_paths:
        print("No migration-like paths in current git diff.")
        return 0
    tp = resolve_task_arg(repo_root, args.task)
    text = ""
    if tp and tp.is_file():
        text = tp.read_text(encoding="utf-8")
    pp = resolve_plan_arg(repo_root, args.plan)
    if pp and pp.is_file():
        text += "\n" + pp.read_text(encoding="utf-8")
    if not _MIGRATION_HINTS.search(text):
        report.add(
            "migrations",
            "error",
            "Migration files changed but active task/plan lack rollback/backup/backward-compat notes",
        )
    for rel in mig_paths:
        report.add(rel, "warn", "migration touched — ensure validate + staging run")
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_scan_secrets(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    targets: list[Path] = []
    root = repo_root.resolve()
    if args.paths:
        for raw in args.paths:
            p = (repo_root / raw).resolve()
            if p.is_file() and (root == p or root in p.parents):
                targets.append(p)
    elif args.git_staged and git_is_repo(repo_root):
        p = _run_git(repo_root, "diff", "--cached", "--name-only")
        for rel in (p.stdout or "").splitlines():
            if rel.strip():
                targets.append((repo_root / rel.strip()).resolve())
    else:
        lim = args.max_files
        for p in collect_source_paths(repo_root, max_files=lim):
            pr = p.resolve()
            if root == pr or root in pr.parents:
                targets.append(pr)

    for fp in targets:
        try:
            rel = str(fp.relative_to(repo_root))
        except ValueError:
            continue
        if fp.stat().st_size > args.max_bytes:
            continue
        if fp.name == ".env" and not args.include_env:
            report.add(rel, "warn", ".env file present — ensure it is gitignored")
            continue
        scan_file_secrets(fp, report, rel)
    report.print()
    return report.exit_code(args.warnings_as_errors)


def cmd_scan_todos(args: argparse.Namespace, repo_root: Path) -> int:
    out: list[dict[str, Any]] = []
    for fp in collect_source_paths(repo_root, max_files=args.max_files):
        if fp.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".php"}:
            continue
        try:
            lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, start=1):
            if _TODO_PATTERN.search(line):
                try:
                    rel = str(fp.relative_to(repo_root))
                except ValueError:
                    rel = str(fp)
                out.append({"path": rel, "line": i, "text": line.strip()[:500]})
    meta = repo_root / ".mutter" / "metadata"
    meta.mkdir(parents=True, exist_ok=True)
    dest = meta / "todos.json"
    dest.write_text(json.dumps({"items": out}, indent=2), encoding="utf-8")
    print(f"Recorded {len(out)} hits to {dest.relative_to(repo_root)}")
    return 0


def cmd_guard_large_change(args: argparse.Namespace, repo_root: Path) -> int:
    report = Report()
    files, ins, dels = git_diff_shortstat(repo_root)
    total_lines = ins + dels
    paths = git_changed_paths(repo_root, staged=False)
    crit = [p for p in paths if path_risk_level(p) == "HIGH"]

    triggered = files >= args.max_files or total_lines >= args.max_lines or len(crit) >= args.critical_paths

    if triggered:
        if files >= args.max_files:
            report.add("diff", "error", f"too many files changed ({files} >= {args.max_files})")
        if total_lines >= args.max_lines:
            report.add("diff", "error", f"diff too large ({total_lines} lines >= {args.max_lines})")
        if len(crit) >= args.critical_paths and crit:
            report.add("diff", "error", f"critical paths touched ({len(crit)}): require plan + risk + tests")
        state = load_state(repo_root)
        if not state.get("active_plan"):
            report.add(".mutter/state/current.json", "error", "set active_plan for large/high-risk changes")
    else:
        print(f"OK — within guard ({files} files, {total_lines} line changes, {len(crit)} critical path hits).")
        return 0

    report.print()
    return report.exit_code(args.warnings_as_errors)


def main() -> int:
    ap = argparse.ArgumentParser(description="Mutter workspace maintenance CLI.")
    ap.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (directory containing .mutter/). Default: walk up from CWD.",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate-task", help="Validate one task (default: active_task in state).")
    p_val.add_argument("--task", type=str, default=None, help="Path to task .md (repo-relative or absolute).")
    p_val.add_argument(
        "--deep",
        action="store_true",
        help="Also warn on missing **Read:** paths under Steps.",
    )
    p_val.add_argument("--warnings-as-errors", action="store_true", help="Non-zero exit on warnings too.")
    p_val.set_defaults(func=cmd_validate_task)

    p_vals = sub.add_parser("validate-tasks", help="Validate all *.md tasks under .mutter/tasks/<bucket>/.")
    p_vals.add_argument(
        "--include",
        nargs="+",
        default=["current", "planned", "blocked"],
        choices=["current", "planned", "blocked", "completed"],
        help="Which task buckets to scan.",
    )
    p_vals.add_argument("--deep", action="store_true")
    p_vals.add_argument("--warnings-as-errors", action="store_true")
    p_vals.set_defaults(func=cmd_validate_tasks)

    p_vp = sub.add_parser("validate-plan", help="Validate one plan (default: active_plan in state).")
    p_vp.add_argument("--plan", type=str, default=None, help="Path to plan .md under .mutter/plans/ or repo-relative.")
    p_vp.add_argument("--warnings-as-errors", action="store_true")
    p_vp.set_defaults(func=cmd_validate_plan)

    p_vps = sub.add_parser("validate-plans", help="Validate all *.md under .mutter/plans/ (except README).")
    p_vps.add_argument("--warnings-as-errors", action="store_true")
    p_vps.set_defaults(func=cmd_validate_plans)

    p_st = sub.add_parser(
        "status",
        help="Show .mutter/state/current.json and short previews of active task/plan when set.",
    )
    p_st.set_defaults(func=cmd_status)

    p_sc = sub.add_parser("scan-state", help="Print changed_files from .mutter/metadata/scan-state.json.")
    p_sc.set_defaults(func=cmd_scan_state)

    p_sk = sub.add_parser("check-skill-refs", help="Validate relative .md links inside plugin skills (parity).")
    p_sk.add_argument(
        "--skill-roots",
        dest="skill_roots",
        nargs="+",
        default=["mutter-claude/skills", "mutter-cursor/skills"],
        help="Directories to scan for SKILL.md etc.",
    )
    p_sk.set_defaults(func=cmd_check_skill_refs)

    p_ci = sub.add_parser(
        "ci",
        help="Run check-skill-refs, validate-tasks, validate-plans, sync_cursor_skills.py, optional git diff.",
    )
    p_ci.add_argument(
        "--strict-tasks",
        action="store_true",
        help="Treat validate-tasks and validate-plans warnings as errors (recommended for release branches).",
    )
    p_ci.add_argument(
        "--check-cursor-sync",
        action="store_true",
        help="After sync script, fail if mutter-cursor/skills still differs from git (requires clean tree).",
    )
    p_ci.add_argument(
        "--with-governance",
        action="store_true",
        help="Also run validate-adr, scan-secrets, guard-large-change (after core checks).",
    )
    p_ci.set_defaults(func=cmd_ci)

    p_adr = sub.add_parser(
        "validate-adr",
        help="Validate .mutter/adr/*.md structure (Status, Context, Decision, Consequences).",
    )
    p_adr.add_argument("--warnings-as-errors", action="store_true")
    p_adr.set_defaults(func=cmd_validate_adr)

    p_qg = sub.add_parser("validate-quality-gate", help="Check .mutter/quality-gates/<type>.md exists and has checklist.")
    p_qg.add_argument("--type", type=str, required=True, help="e.g. bugfix, feature, migration, security, refactor")
    p_qg.add_argument("--warnings-as-errors", action="store_true")
    p_qg.set_defaults(func=cmd_validate_quality_gate)

    p_risk = sub.add_parser("risk-check", help="Score path list by built-in LOW/MEDIUM/HIGH heuristics.")
    p_risk.add_argument("--paths", nargs="*", default=None, help="Repo-relative paths (default: git or scan-state).")
    p_risk.add_argument("--from-git", action="store_true", help="Use git diff vs HEAD.")
    p_risk.add_argument("--staged", action="store_true", help="With --from-git: staged diff only.")
    p_risk.add_argument("--from-scan", action="store_true", help="Use changed_files from scan-state.json.")
    p_risk.set_defaults(func=cmd_risk_check)

    p_ctx = sub.add_parser("context-pack", help="Emit a compact Markdown bundle for agents (task, plan, ADRs, ownership).")
    p_ctx.add_argument("--task", type=str, default=None)
    p_ctx.add_argument("--plan", type=str, default=None)
    p_ctx.add_argument("--out", type=Path, default=None, help="Write to file instead of stdout.")
    p_ctx.set_defaults(func=cmd_context_pack)

    p_pf = sub.add_parser("preflight", help="Readiness gate: state, optional task validation, dirty tree, scan-state.")
    p_pf.add_argument("--require-active-task", action="store_true", help="Fail if active_task missing or broken.")
    p_pf.add_argument("--check-acceptance-verify", action="store_true", help="Run validate-task rules on active task.")
    p_pf.add_argument(
        "--require-plan-for-large",
        action="store_true",
        help="If diff is large or HIGH-risk paths, require active_plan.",
    )
    p_pf.add_argument("--large-files", type=int, default=20)
    p_pf.add_argument("--large-lines", type=int, default=800)
    p_pf.add_argument("--expect-scan-state", action="store_true", help="Warn if metadata/scan-state.json missing.")
    p_pf.add_argument("--fail-on-dirty", action="store_true", help="Error if git working tree is dirty.")
    p_pf.add_argument("--warnings-as-errors", action="store_true")
    p_pf.set_defaults(func=cmd_preflight)

    p_rep = sub.add_parser("report-change", help="Print a Markdown skeleton for post-change / PR notes.")
    p_rep.set_defaults(func=cmd_report_change)

    p_prt = sub.add_parser("pr-template", help="Print PR Markdown from active task/plan + git paths + suggested tests.")
    p_prt.add_argument("--task", type=str, default=None)
    p_prt.add_argument("--plan", type=str, default=None)
    p_prt.add_argument("--staged", action="store_true", help="Use staged-only diff for paths and stat.")
    p_prt.set_defaults(func=cmd_pr_template)

    p_sug = sub.add_parser("suggest-tests", help="Suggest commands from .mutter/testing/commands.json for paths.")
    p_sug.add_argument("--paths", nargs="*", default=None)
    p_sug.add_argument("--from-git", action="store_true")
    p_sug.add_argument("--staged", action="store_true")
    p_sug.set_defaults(func=cmd_suggest_tests)

    p_bnd = sub.add_parser("check-boundaries", help="Heuristic forbidden-import check using .mutter/boundaries.json.")
    p_bnd.add_argument("--paths", nargs="*", default=None)
    p_bnd.add_argument("--staged", action="store_true")
    p_bnd.add_argument("--warnings-as-errors", action="store_true")
    p_bnd.set_defaults(func=cmd_check_boundaries)

    p_mig = sub.add_parser(
        "validate-migrations",
        help="If migration paths changed, require rollback/backup notes in task/plan.",
    )
    p_mig.add_argument("--task", type=str, default=None)
    p_mig.add_argument("--plan", type=str, default=None)
    p_mig.add_argument("--staged", action="store_true")
    p_mig.add_argument("--warnings-as-errors", action="store_true")
    p_mig.set_defaults(func=cmd_validate_migrations)

    p_sec = sub.add_parser("scan-secrets", help="Lightweight local patterns for obvious secrets (best-effort).")
    p_sec.add_argument("--paths", nargs="*", default=None, help="Limit to these repo-relative files.")
    p_sec.add_argument("--git-staged", action="store_true", help="Scan staged files only.")
    p_sec.add_argument("--max-files", type=int, default=4000)
    p_sec.add_argument("--max-bytes", type=int, default=512000)
    p_sec.add_argument("--include-env", action="store_true", help="Scan .env contents (default: warn-only skip body).")
    p_sec.add_argument("--warnings-as-errors", action="store_true")
    p_sec.set_defaults(func=cmd_scan_secrets)

    p_td = sub.add_parser("scan-todos", help="Collect TODO/FIXME/HACK into .mutter/metadata/todos.json.")
    p_td.add_argument("--max-files", type=int, default=4000)
    p_td.set_defaults(func=cmd_scan_todos)

    p_gl = sub.add_parser(
        "guard-large-change",
        help="Fail if diff exceeds thresholds or touches critical paths without active_plan.",
    )
    p_gl.add_argument("--max-files", type=int, default=20)
    p_gl.add_argument("--max-lines", type=int, default=800)
    p_gl.add_argument("--critical-paths", type=int, default=1, help="Min HIGH-risk files to trigger guard.")
    p_gl.add_argument("--warnings-as-errors", action="store_true")
    p_gl.set_defaults(func=cmd_guard_large_change)

    args = ap.parse_args()
    start = args.root if args.root else Path.cwd()
    repo_root = start if args.root and (start / ".mutter").is_dir() else find_repo_root(start)
    if repo_root is None:
        print("ERROR: could not find .mutter/ — use --root <repo>", file=sys.stderr)
        return 1

    func = args.func
    return int(func(args, repo_root))


if __name__ == "__main__":
    sys.exit(main())
