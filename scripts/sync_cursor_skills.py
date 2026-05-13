#!/usr/bin/env python3
"""Normalize mutter-claude skill frontmatter (name + description + optional flags for Codex/Claude); regenerate mutter-cursor/skills."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
claude_root = ROOT / "mutter-claude" / "skills"
cursor_root = ROOT / "mutter-cursor" / "skills"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit("No frontmatter block")
    fm_raw = m.group(1)
    body = text[m.end() :]
    data: dict[str, str] = {}
    for line in fm_raw.splitlines():
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
        colon = line.find(":")
        if colon <= 0:
            continue
        key = line[:colon].strip()
        val = line[colon + 1 :].strip()
        data[key] = val
    return data, body


def build_claude_frontmatter(folder: str, data: dict[str, str]) -> str:
    desc = data.get("description", "").strip()
    if not desc:
        raise SystemExit(f"Missing description: {folder}")
    lines = ["---", f"name: {folder}", f"description: {desc}"]
    dmi = data.get("disable-model-invocation")
    if dmi:
        lines.append(f"disable-model-invocation: {dmi}")
    lines.append("---\n")
    return "\n".join(lines)


def main() -> None:
    cursor_root.mkdir(parents=True, exist_ok=True)
    n = 0
    for d in sorted(claude_root.iterdir()):
        if not d.is_dir():
            continue
        src = d / "SKILL.md"
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        data, body = parse_frontmatter(text)
        folder = d.name
        new_claude = build_claude_frontmatter(folder, data) + body
        if new_claude != text:
            src.write_text(new_claude, encoding="utf-8")

        desc = data.get("description", "").strip()
        new_fm_cursor = f"---\nname: {folder}\ndescription: {desc}\n---\n"
        out_dir = cursor_root / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(new_fm_cursor + body, encoding="utf-8")
        n += 1

    print(f"Normalized {n} Claude skills + synced mutter-cursor/skills → {cursor_root}")


if __name__ == "__main__":
    main()
