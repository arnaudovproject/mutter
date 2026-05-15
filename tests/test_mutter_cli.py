#!/usr/bin/env python3
"""Smoke tests for scripts/mutter.py — run from repo root: python3 tests/test_mutter_cli.py"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import tempfile

REPO = Path(__file__).resolve().parents[1]
MUTTER = REPO / "scripts" / "mutter.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(MUTTER), *args],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )


def main() -> int:
    assert MUTTER.is_file(), MUTTER

    # --help lists subcommands
    r = run("--help")
    assert r.returncode == 0, r.stderr
    assert "agent-cadence" in r.stdout, r.stdout[:500]
    assert "validate-prd" in r.stdout and "prd-init" in r.stdout, r.stdout[:1200]

    # agent-cadence mentions PRD lifecycle
    r = run("agent-cadence")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "Mutter agent cadence" in out
    assert "sync-task-progress" in out
    assert "40%" in out or "~40%" in out
    assert "validate-prd" in out or "/mutter:prd" in out
    assert str(REPO) in out or ".mutter" in out

    # agent-cadence --out writes file
    tmp = REPO / ".mutter" / "context" / "_test_agent_cadence.md"
    r = run("agent-cadence", "--out", ".mutter/context/_test_agent_cadence.md")
    assert r.returncode == 0, r.stderr
    assert tmp.is_file()
    body = tmp.read_text(encoding="utf-8")
    assert "preflight" in body
    tmp.unlink(missing_ok=True)

    # status on dogfood repo
    r = run("status")
    assert r.returncode == 0, r.stderr
    assert "current.json" in r.stdout or "state" in r.stdout.lower()

    # tasks-status markdown table
    r = run("tasks-status", "--include", "current")
    assert r.returncode == 0, r.stderr
    assert "|" in r.stdout or "Steps" in r.stdout or "task" in r.stdout.lower(), r.stdout[:400]

    # scan-state (may be empty list)
    r = run("scan-state")
    assert r.returncode == 0, r.stderr

    # validate-prd on isolated workspace (--root)
    tmpl_prd = REPO / "mutter-claude" / "templates" / "dot-mutter" / "templates" / "PRD.md"
    assert tmpl_prd.is_file(), tmpl_prd
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".mutter" / "prd").mkdir(parents=True)
        prd_path = root / ".mutter" / "prd" / "PRD.md"
        prd_path.write_text(
            "# Broken PRD\n\n## Overview\n\nThis overview is long enough to pass the minimum.\n",
            encoding="utf-8",
        )
        rb = subprocess.run(
            [sys.executable, str(MUTTER), "--root", str(root), "validate-prd"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        assert rb.returncode != 0, rb.stdout + rb.stderr

        prd_path.write_text(tmpl_prd.read_text(encoding="utf-8"), encoding="utf-8")
        rok = subprocess.run(
            [sys.executable, str(MUTTER), "--root", str(root), "validate-prd"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        assert rok.returncode == 0, rok.stdout + rok.stderr

    print("OK — test_mutter_cli smoke tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
