#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


FRONT_MATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
SIMPLE_FIELD_RE_TEMPLATE = r"^{key}:\s*(.*)$"


def extract_front_matter(text: str) -> str | None:
    m = FRONT_MATTER_RE.match(text)
    return m.group(1) if m else None


def extract_simple_field(front_matter: str, key: str) -> str | None:
    pattern = re.compile(SIMPLE_FIELD_RE_TEMPLATE.format(key=re.escape(key)), re.MULTILINE)
    m = pattern.search(front_matter)
    if not m:
        return None
    value = m.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value or None


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: extract_metadata.py <markdown-file>", file=sys.stderr)
        raise SystemExit(1)

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    result: dict[str, str] = {}

    front_matter = extract_front_matter(text)
    if front_matter:
        series = extract_simple_field(front_matter, "series")
        title = extract_simple_field(front_matter, "title")

        if series:
            result["series"] = series
        if title:
            result["title"] = title

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()