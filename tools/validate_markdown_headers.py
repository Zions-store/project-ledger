#!/usr/bin/env python3
"""
validate_markdown_headers.py — Copyright/SPDX header validator for Markdown files.

Handles two file types:
  - Normal Markdown: checks Copyright/SPDX in the first 20 lines.
  - YAML frontmatter Markdown: first line must be "---"; after the closing
    "---" delimiter, checks Copyright/SPDX in the first 5 content lines.

Usage: python tools/validate_markdown_headers.py [root_dir...]
Exits 0 if all valid, 1 if any files are missing headers.
"""

import os
import sys

EXCLUDE_PATHS = {
    "tests/fixtures",
    "tests/work",
}

COPYRIGHT_TOKEN = "Copyright (C)"
SPDX_TOKEN = "SPDX-License-Identifier:"


def check_normal(lines, filepath):
    pool = "".join(lines[:20])
    issues = []
    if COPYRIGHT_TOKEN not in pool:
        issues.append(f"MISSING copyright: {filepath}")
    if SPDX_TOKEN not in pool:
        issues.append(f"MISSING SPDX: {filepath}")
    return issues


def check_frontmatter(lines, filepath):
    if not lines or lines[0].rstrip() != "---":
        return check_normal(lines, filepath)

    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            end = i
            break
    if end is None:
        return check_normal(lines, filepath)

    body = lines[end + 1 : end + 6]
    pool = "".join(body)
    issues = []
    if COPYRIGHT_TOKEN not in pool:
        issues.append(f"MISSING copyright (after frontmatter): {filepath}")
    if SPDX_TOKEN not in pool:
        issues.append(f"MISSING SPDX (after frontmatter): {filepath}")
    return issues


def is_excluded(relpath):
    parts = relpath.replace(os.sep, "/").split("/")
    for excl in EXCLUDE_PATHS:
        excl_parts = excl.replace("/", os.sep).split(os.sep)
        if parts[: len(excl_parts)] == excl_parts:
            return True
    return False


def scan(root, issues):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fname in filenames:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, root)
            if is_excluded(rel):
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()
            except OSError:
                issues.append(f"ERROR reading: {fpath}")
                continue

            file_issues = check_frontmatter(lines, rel)
            issues.extend(file_issues)
            if file_issues:
                print("\n".join(file_issues))


def main():
    roots = sys.argv[1:] if len(sys.argv) > 1 else ["."]
    all_issues = []
    for root in roots:
        if not os.path.isdir(root):
            print(f"WARNING: not a directory — {root}")
            continue
        scan(root, all_issues)

    if all_issues:
        print(f"\nTotal issues: {len(all_issues)}")
        sys.exit(1)
    print("All files have valid copyright/SPDX headers.")
    sys.exit(0)


if __name__ == "__main__":
    main()
