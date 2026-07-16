#!/usr/bin/env python3
"""
run_static_checks.py - Unified entry point for all project-onboard static checks.
Runs UTF-8, frontmatter, rule pack, and Python compile checks sequentially.
Usage: python run_static_checks.py
"""

import os
import subprocess
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(TESTS_DIR)

SCRIPTS = [
    ('validate_utf8.py', ['python', os.path.join(TESTS_DIR, 'validate_utf8.py')]),
    ('validate_frontmatter.py', ['python', os.path.join(TESTS_DIR, 'validate_frontmatter.py')]),
    ('validate_rule_packs.py', ['python', os.path.join(TESTS_DIR, 'validate_rule_packs.py')]),
]


def main():
    all_ok = True

    for name, cmd in SCRIPTS:
        print(f'\n=== {name} ===')
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL_ROOT)
        print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        if result.returncode != 0:
            all_ok = False
            print(f'  -> FAILED (exit {result.returncode})')
        else:
            print(f'  -> PASSED')

    # Python compile check on all .py files in tests/
    print('\n=== Python compile check ===')
    for dirpath, dirnames, filenames in os.walk(TESTS_DIR):
        dirnames[:] = [d for d in dirnames if d not in ('__pycache__', '.git')]
        for f in filenames:
            if f.endswith('.py'):
                fpath = os.path.join(dirpath, f)
                try:
                    with open(fpath, 'r', encoding='utf-8') as fh:
                        compile(fh.read(), fpath, 'exec')
                except SyntaxError as e:
                    print(f'FAIL {os.path.relpath(fpath, SKILL_ROOT)}: {e}')
                    all_ok = False
    if all_ok:
        print('  All .py files compile cleanly.')

    print()
    if all_ok:
        print('All static checks passed.')
    else:
        print('Some checks FAILED.')
    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
