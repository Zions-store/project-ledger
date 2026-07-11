#!/usr/bin/env python3
"""
validate_frontmatter.py - Verify YAML frontmatter in SKILL.md is valid.
Usage: python validate_frontmatter.py

Checks:
- SKILL.md has valid YAML frontmatter
- Required fields: name, version, description
- No non-YAML content before the opening --- delimiter
"""

import os
import sys
import re

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_FILE = os.path.join(SKILL_ROOT, 'SKILL.md')


def validate_skill_frontmatter():
    if not os.path.exists(SKILL_FILE):
        print(f"FAIL: SKILL.md not found at {SKILL_FILE}")
        return False

    with open(SKILL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    issues = []

    # Check opening --- is at position 0
    stripped = content.lstrip()
    if not stripped.startswith('---'):
        issues.append("First non-whitespace content is not '---' (YAML frontmatter delimiter)")
        for issue in issues:
            print(f"FAIL: {issue}")
        return False

    # Extract YAML block
    start_idx = content.index('---')
    end_idx = content.index('---', start_idx + 3) if '---' in content[start_idx + 3:] else -1

    if end_idx == -1:
        issues.append("Missing closing '---' delimiter for frontmatter")

    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return False

    yaml_text = content[start_idx + 3:end_idx].strip()

    if not yaml_text:
        issues.append("YAML frontmatter is empty")

    # Try to parse with PyYAML if available
    try:
        import yaml
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            issues.append("YAML frontmatter is not a mapping (dict)")
        else:
            for field in ['name', 'version', 'description']:
                if field not in data:
                    issues.append(f"Missing required field: '{field}'")
                elif not data[field]:
                    issues.append(f"Field '{field}' is empty")
    except ImportError:
        # PyYAML not installed; do basic regex check
        pass
    except Exception as e:
        issues.append(f"YAML parse error: {e}")

    # Basic validation without PyYAML
    for field in ['name:', 'version:', 'description:']:
        found = False
        for line in yaml_text.split('\n'):
            if line.strip().startswith(field):
                found = True
                value = line.strip()[len(field):].strip()
                if not value:
                    issues.append(f"Field '{field}' is empty")
                break
        if not found:
            issues.append(f"Missing required field: '{field[:-1]}'")

    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return False

    print("OK  SKILL.md frontmatter is valid")
    return True


def main():
    ok = validate_skill_frontmatter()
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
