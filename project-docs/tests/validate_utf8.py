#!/usr/bin/env python3
"""Validate project-docs text assets are strict UTF-8 and contain no U+FFFD."""

from pathlib import Path
import sys


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".tmpl"}


def iter_text_assets() -> list[Path]:
    return sorted(
        path
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and path.suffix in TEXT_SUFFIXES
    )


def validate(path: Path) -> list[str]:
    data = path.read_bytes()
    issues: list[str] = []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"invalid UTF-8 at byte {exc.start}"]
    if "\ufffd" in text:
        issues.append(f"replacement character (U+FFFD) at character {text.index(chr(0xfffd))}")
    return issues


def main() -> int:
    files = iter_text_assets()
    failures = 0
    for path in files:
        issues = validate(path)
        relative = path.relative_to(SKILL_ROOT)
        if issues:
            failures += 1
            print(f"FAIL {relative}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"OK   {relative}")

    print(f"\nFiles checked: {len(files)}")
    print(f"All valid: {failures == 0}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

