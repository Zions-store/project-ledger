#!/usr/bin/env python3
"""Validate generated project-docs output before it replaces a user document."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


MANAGED_START = "<!-- project-docs:managed:start -->"
MANAGED_END = "<!-- project-docs:managed:end -->"
LINK_START = "<!-- project-docs:links:start -->"
LINK_END = "<!-- project-docs:links:end -->"
GENERATED_START = "<!-- project-onboard:generated:start -->"
GENERATED_END = "<!-- project-onboard:generated:end -->"

SECRET_PATTERNS = [
    (r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----", "private key block"),
    (r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{20,})\b", "known token prefix"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key ID"),
    (r"(?im)^\s*(?:password|secret|token|api[_ -]?key)\s*[:=]\s*(?!<redacted>|redacted|omitted|not set|unknown)[^\s]{4,}", "credential assignment"),
    (r"\b[a-z][a-z0-9+.-]*://[^\s/@:]+:[^@\s]+@", "URL with embedded credentials"),
    (r"\bBearer\s+eyJ[A-Za-z0-9._~+/-]+", "JWT bearer token"),
]


def marker_issues(content: str, kind: str) -> list[str]:
    issues: list[str] = []
    if kind in {"state", "devlog"}:
        if content.count(MANAGED_START) != 1 or content.count(MANAGED_END) != 1:
            issues.append("expected exactly one project-docs managed marker pair")
        elif content.index(MANAGED_START) > content.index(MANAGED_END):
            issues.append("managed:start appears after managed:end")
    else:
        starts, ends = content.count(LINK_START), content.count(LINK_END)
        if starts != ends or starts > 1:
            issues.append("project-docs link markers must be paired and unique")
        if starts == 1 and GENERATED_START in content and GENERATED_END in content:
            generated = content[content.index(GENERATED_START):content.index(GENERATED_END)]
            if LINK_START in generated or LINK_END in generated:
                issues.append("project-docs links must not be inside project-onboard generated content")
    return issues


def validate_content(content: str, kind: str) -> list[str]:
    issues = marker_issues(content, kind)
    if "\ufffd" in content:
        issues.append("contains replacement character (U+FFFD)")
    if re.search(r"\{\{[^{}\n]+\}\}", content):
        issues.append("contains unresolved template placeholder")
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"contains {label}")
    return issues


def validate_path(path: Path, kind: str) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"invalid UTF-8 at byte {exc.start}"]
    return validate_content(content, kind)


def self_test() -> int:
    valid = f"# State\n{MANAGED_START}\nKnown: none\n{MANAGED_END}\n"
    checks = [
        (valid, "state", False),
        (valid.replace("none", "{{TODO}}"), "state", True),
        (valid.replace("none", "api_key=sk-abcdefghijklmnopqrstuvwxyz"), "state", True),
        ("# State\n" + MANAGED_START + "\n", "state", True),
        (f"{GENERATED_START}\n{LINK_START}\n{LINK_END}\n{GENERATED_END}\n", "agents", True),
    ]
    failures = 0
    for index, (content, kind, should_fail) in enumerate(checks, 1):
        failed = bool(validate_content(content, kind))
        if failed != should_fail:
            failures += 1
            print(f"self-test {index}: unexpected result")
    print(f"Output validator self-test: {'PASS' if failures == 0 else 'FAIL'}")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--kind", choices=("state", "devlog", "agents"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.path is None or args.kind is None:
        parser.error("path and --kind are required unless --self-test is used")
    issues = validate_path(args.path, args.kind)
    if issues:
        print(f"FAIL {args.path}")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"PASS {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
