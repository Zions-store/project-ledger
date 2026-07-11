#!/usr/bin/env python3
"""
validate_rule_packs.py - Strict YAML validation of all rule pack frontmatter.
Usage: python validate_rule_packs.py

Validates:
  1. Frontmatter starts on line 1 (---)
  2. YAML parses correctly (yaml.safe_load)
  3. Required fields present (schema_version, id, display_name, priority, signatures, known_blind_spots)
  4. id matches filename stem
  5. All ids and aliases are unique across rule packs
  6. README supported type list matches registry
"""

import os
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCES_DIR = os.path.join(SKILL_ROOT, 'references')
TEMPLATES_DIR = os.path.join(SKILL_ROOT, 'templates')
README_PATH = os.path.join(SKILL_ROOT, 'README.md')

REQUIRED_FIELDS = [
    'schema_version', 'id', 'display_name', 'priority',
    'signatures', 'known_blind_spots',
]

FIELD_TYPES = {
    'schema_version': int,
    'id': str,
    'display_name': str,
    'priority': int,
    'signatures': dict,
    'known_blind_spots': list,
}


def main():
    issues = []

    # Load YAML
    try:
        import yaml
    except ImportError:
        print("FAIL: PyYAML not installed. Run: pip install pyyaml")
        print("       This is a development dependency, not a runtime dependency.")
        sys.exit(1)

    # Check _common.md and _rule-pack-template.md exist
    for fname in ['_common.md', '_rule-pack-template.md']:
        path = os.path.join(REFERENCES_DIR, fname)
        if not os.path.exists(path):
            issues.append(f'{fname} not found')
        else:
            print(f'OK  references/{fname}')

    # Check templates/AGENTS.md exists
    agents_path = os.path.join(TEMPLATES_DIR, 'AGENTS.md')
    if not os.path.exists(agents_path):
        issues.append('templates/AGENTS.md not found')
    else:
        print('OK  templates/AGENTS.md')

    # Scan rule packs
    registrations = []
    for fname in sorted(os.listdir(REFERENCES_DIR)):
        if not fname.endswith('.md') or fname.startswith('_'):
            continue

        fpath = os.path.join(REFERENCES_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        file_ok = True

        # 1. Frontmatter must start on line 1
        if not content.startswith('---'):
            issues.append(f'{fname}: frontmatter does not start on line 1')
            file_ok = False

        # 2. Parse YAML
        try:
            yaml_text = content.split('---')[1]
            data = yaml.safe_load(yaml_text)
        except Exception as e:
            issues.append(f'{fname}: YAML parse error: {e}')
            print(f'FAIL references/{fname}')
            continue

        # 3. Required fields
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                issues.append(f'{fname}: missing required field "{field}"')
                file_ok = False

        # 4. Field types
        if data:
            for field, expected_type in FIELD_TYPES.items():
                if field in data and not isinstance(data[field], expected_type):
                    issues.append(f'{fname}: field "{field}" expected {expected_type.__name__}, got {type(data[field]).__name__}')
                    file_ok = False

        # 5. id matches filename
        expected_id = os.path.splitext(fname)[0]
        if data and data.get('id') != expected_id:
            issues.append(f'{fname}: id "{data.get("id")}" does not match filename stem "{expected_id}"')
            file_ok = False

        if data:
            registrations.append((fname, data))

        if file_ok:
            print(f'OK  references/{fname}')
        else:
            print(f'FAIL references/{fname}')

    # 6. Unique ids and aliases
    all_ids = {}
    all_aliases = {}
    for fname, data in registrations:
        rid = data.get('id', '')
        if rid in all_ids:
            issues.append(f'Duplicate id "{rid}" in {fname} and {all_ids[rid]}')
        all_ids[rid] = fname
        for alias in data.get('aliases', []) or []:
            alias = str(alias)
            if alias in all_aliases:
                issues.append(f'Duplicate alias "{alias}" in {fname} and {all_aliases[alias]}')
            all_aliases[alias] = fname

    # 7. README supported type list vs registry
    if os.path.exists(README_PATH):
        with open(README_PATH, 'r', encoding='utf-8') as f:
            readme = f.read()
        for _, data in registrations:
            display = data.get('display_name', '')
            # Check README mentions the display name or id
            rid = data.get('id', '')
            if rid == 'general':
                continue  # general is a special fallback
            if display and display not in readme:
                # Check aliases
                found = False
                for alias in data.get('aliases', []) or []:
                    if alias in readme:
                        found = True
                        break
                if rid in readme:
                    found = True
                if not found:
                    issues.append(f'README may not list type "{display}" (id={rid})')

    # 8. Check SKILL.md references _common.md
    skill_path = os.path.join(SKILL_ROOT, 'SKILL.md')
    with open(skill_path, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    if 'references/_common.md' not in skill_content:
        issues.append('SKILL.md does not reference _common.md')

    # Summary
    print()
    print(f'Rule packs scanned: {len(registrations)}')
    print(f'Issues found: {len(issues)}')
    if issues:
        for issue in issues:
            print(f'  - {issue}')
        sys.exit(1)
    else:
        print('All rule packs validated (strict YAML + schema + uniqueness).')
        sys.exit(0)


if __name__ == '__main__':
    main()
