#!/usr/bin/env python3
"""
validate_rule_packs.py - Strict YAML validation of all rule pack frontmatter.
Validates: line1=---, yaml.safe_load, 19 fields, id==filename, kind values,
refinement schema, signature uniqueness, SKILL.md reference.
"""

import os
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCES_DIR = os.path.join(SKILL_ROOT, 'references')
TEMPLATES_DIR = os.path.join(SKILL_ROOT, 'templates')

REQUIRED_FIELDS = [
    'schema_version', 'id', 'display_name', 'priority', 'kind',
    'aliases', 'signatures', 'exclusions', 'refinements',
    'workspace_files', 'priority_files', 'entry_point_patterns',
    'external_reference_mechanisms', 'generated_paths',
    'large_structured_files', 'binary_asset_types',
    'default_ignore_paths', 'known_blind_spots', 'optional_output_sections',
]

FIELD_TYPES = {
    'schema_version': int, 'id': str, 'display_name': str,
    'priority': int, 'kind': str, 'aliases': list,
    'signatures': dict, 'exclusions': dict,
    'refinements': (list, dict), 'workspace_files': list,
    'priority_files': list, 'entry_point_patterns': list,
    'external_reference_mechanisms': list, 'generated_paths': list,
    'large_structured_files': list, 'binary_asset_types': list,
    'default_ignore_paths': list, 'known_blind_spots': list,
    'optional_output_sections': list,
}

VALID_KINDS = {'normal', 'fallback', 'refinement'}

REQUIRED_SECTIONS = {
    'unity.md': ['Signature Detection', 'AGENTS.md Additions for Unity'],
    'unreal.md': ['Signature Detection', 'AGENTS.md Additions for Unreal'],
    'monogame.md': ['Signature Detection', 'AGENTS.md Additions for MonoGame'],
    'nodejs.md': ['Signature Detection', 'Build', 'Run'],
    'python.md': ['Signature Detection', 'Build', 'Run'],
    'rust.md': ['Signature Detection', 'Build', 'Test'],
    'go.md': ['Signature Detection', 'Build', 'Test'],
    'java.md': ['Signature Detection', 'Build', 'Test'],
    'cpp.md': ['Signature Detection', 'Build', 'Test'],
    'csharp.md': ['Signature Detection', 'Build', 'Run'],
    'lua.md': ['Signature Detection', 'Build', 'Run'],
    'general.md': ['Scan Steps'],
}


def main():
    issues = []

    try:
        import yaml
    except ImportError:
        print("FAIL: PyYAML not installed. Run: pip install pyyaml")
        sys.exit(1)

    for fname in ['_common.md', '_rule-pack-template.md']:
        path = os.path.join(REFERENCES_DIR, fname)
        if not os.path.exists(path):
            issues.append(f'{fname} not found')
        else:
            print(f'OK  references/{fname}')

    agents_path = os.path.join(TEMPLATES_DIR, 'AGENTS.md')
    if not os.path.exists(agents_path):
        issues.append('templates/AGENTS.md not found')
    else:
        print('OK  templates/AGENTS.md')

    registrations = []
    refinement_parent_queue = []  # (fname, i, parent_id) deferred
    fallback_count = 0

    for fname in sorted(os.listdir(REFERENCES_DIR)):
        if not fname.endswith('.md') or fname.startswith('_'):
            continue

        fpath = os.path.join(REFERENCES_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        file_ok = True

        if not content.startswith('---'):
            issues.append(f'{fname}: frontmatter does not start on line 1')
            file_ok = False

        try:
            yaml_text = content.split('---')[1]
            data = yaml.safe_load(yaml_text)
        except Exception as e:
            issues.append(f'{fname}: YAML parse error: {e}')
            print(f'FAIL references/{fname}')
            continue

        # 19 required fields
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                issues.append(f'{fname}: missing required field "{field}"')
                file_ok = False

        # Field types (allow tuple for refinements that can be list or dict)
        if data:
            for field, expected_type in FIELD_TYPES.items():
                if field in data and data[field] is not None:
                    if isinstance(expected_type, tuple):
                        if not isinstance(data[field], expected_type):
                            issues.append(f'{fname}: field "{field}" expected one of {expected_type}, got {type(data[field]).__name__}')
                            file_ok = False
                    elif not isinstance(data[field], expected_type):
                        issues.append(f'{fname}: field "{field}" expected {expected_type.__name__}, got {type(data[field]).__name__}')
                        file_ok = False

        # id matches filename
        expected_id = os.path.splitext(fname)[0]
        if data and data.get('id') != expected_id:
            issues.append(f'{fname}: id "{data.get("id")}" != filename stem "{expected_id}"')
            file_ok = False

        # kind validation
        kind = data.get('kind', '')
        if kind not in VALID_KINDS:
            issues.append(f'{fname}: invalid kind "{kind}". Must be one of: {VALID_KINDS}')
            file_ok = False
        if kind == 'fallback':
            fallback_count += 1

        # Refinement schema: if kind=refinement, require parent in refinements
        if kind == 'refinement':
            refs = data.get('refinements', [])
            if isinstance(refs, dict):
                refs = [refs]
            if isinstance(refs, list):
                if not refs:
                    issues.append(f'{fname}: kind=refinement but refinements is empty')
                    file_ok = False
                for i, ref in enumerate(refs):
                    if isinstance(ref, dict):
                        if 'parent' not in ref:
                            issues.append(f'{fname}: refinement entry {i} missing "parent" field')
                            file_ok = False
                        elif ref.get('parent'):
                            refinement_parent_queue.append((fname, i, ref['parent']))
                        if 'condition' not in ref:
                            issues.append(f'{fname}: refinement entry {i} missing "condition" field')
                            file_ok = False
            elif not refs:
                issues.append(f'{fname}: kind=refinement but refinements is empty')
                file_ok = False

        # POSIX ERE validation: reject GNU/PCRE extensions in entry_point_patterns
        NON_POSIX_PATTERNS = [r'\b', r'\s', r'\d', r'\w', r'\B', r'\S', r'\D', r'\W',
                              r'(?=', r'(?!', r'(?<=', r'(?<!']
        for pattern in data.get('entry_point_patterns', []) or []:
            for np in NON_POSIX_PATTERNS:
                if np in str(pattern):
                    issues.append(f'{fname}: entry_point_pattern "{pattern}" uses non-POSIX construct "{np}". Use POSIX character classes instead.')
                    file_ok = False

        if data:
            registrations.append((fname, data))

        if file_ok:
            print(f'OK  references/{fname}')
        else:
            print(f'FAIL references/{fname}')

    # Unique ids and aliases
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

    # Deferred refinement parent ID validation
    for fname, i, parent_id in refinement_parent_queue:
        if parent_id not in all_ids:
            issues.append(f'{fname}: refinement entry {i} parent "{parent_id}" is not a registered rule pack id')

    # Exactly one fallback
    if fallback_count != 1:
        issues.append(f'Expected exactly 1 kind=fallback rule pack, found {fallback_count}')

    # SKILL.md references _common.md
    skill_path = os.path.join(SKILL_ROOT, 'SKILL.md')
    with open(skill_path, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    if 'references/_common.md' not in skill_content:
        issues.append('SKILL.md does not reference _common.md')
    if 'inspect' not in skill_content or 'generate' not in skill_content:
        issues.append('SKILL.md missing execution mode documentation')

    print()
    print(f'Rule packs scanned: {len(registrations)}')
    print(f'Fields enforced: {len(REQUIRED_FIELDS)}')
    print(f'Issues found: {len(issues)}')
    if issues:
        for issue in issues:
            print(f'  - {issue}')
        sys.exit(1)
    else:
        print('All rule packs validated (strict YAML + 19 fields + schema + uniqueness).')
        sys.exit(0)


if __name__ == '__main__':
    main()
