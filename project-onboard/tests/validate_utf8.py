#!/usr/bin/env python3
"""
validate_utf8.py - Verify all Markdown files in project-onboard are valid UTF-8.
Usage: python validate_utf8.py [--fix]
"""

import os
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWN_CORRUPTIONS = [
    (b'\xe2\x86\x3f', b'->', 'corrupted arrow (E2 86 3F)'),
    (b'\xe2\x80\x3f', b'-', 'corrupted dash (E2 80 3F)'),
]

MOJIBAKE_SNIPPETS = [
    b'\xc3\xa2\xe2\x80\xa0',  # "a" (corrupted dash)
    b'\xc3\x83\xe2\x80\x93',  # "A-" (corrupted em dash)
]


def find_markdown_files(root):
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', 'tests')]
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    return sorted(md_files)


def validate_file(filepath, fix=False):
    with open(filepath, 'rb') as f:
        data = f.read()

    issues = []

    try:
        data.decode('utf-8')
    except UnicodeDecodeError as e:
        issues.append(f"UTF-8 decode error at byte {e.start}")

    if b'\xef\xbf\xbd' in data:
        pos = data.find(b'\xef\xbf\xbd')
        issues.append(f"Replacement character (U+FFFD) at byte {pos}")

    for snippet, _replacement, desc in KNOWN_CORRUPTIONS:
        count = data.count(snippet)
        if count > 0:
            issues.append(f"{count} occurrences of {desc}")

    for snippet in MOJIBAKE_SNIPPETS:
        count = data.count(snippet)
        if count > 0:
            issues.append(f"{count} occurrences of mojibake pattern {snippet.hex()}")

    if issues and fix:
        fixed = data
        for pattern, replacement, _desc in KNOWN_CORRUPTIONS:
            fixed = fixed.replace(pattern, replacement)
        try:
            fixed.decode('utf-8')
            with open(filepath, 'wb') as f:
                f.write(fixed)
            return filepath, True, issues
        except UnicodeDecodeError:
            pass

    return filepath, len(issues) == 0, issues


def main():
    fix_mode = '--fix' in sys.argv

    md_files = find_markdown_files(SKILL_ROOT)
    all_ok = True
    fixed_count = 0

    for filepath in md_files:
        path, ok, issues = validate_file(filepath, fix=fix_mode)
        rel = os.path.relpath(path, SKILL_ROOT)

        if ok:
            print(f"OK  {rel}")
        else:
            all_ok = False
            status = "FIXED" if fix_mode else "FAIL"
            print(f"{status} {rel}")
            for issue in issues:
                print(f"     - {issue}")
            if fix_mode:
                fixed_count += 1

    print()
    print(f"Files checked: {len(md_files)}")
    if fix_mode:
        print(f"Files fixed: {fixed_count}")
    print(f"All valid: {all_ok}")

    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
