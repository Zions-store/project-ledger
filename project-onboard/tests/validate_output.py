#!/usr/bin/env python3
"""
validate_output.py - Security gate for generated AGENTS.md output.

Usage: python validate_output.py <path-to-agents.md>

Validates:
  1. No real credentials or secrets leaked
  2. Required sections present
  3. Evidence tags used correctly
  4. Project-onboard markers properly paired
  5. No unreplaced placeholder text
  6. No empty sections
"""

import os
import re
import sys

# === Secret Patterns ===

SECRET_PATTERNS = [
    # Cloud provider key IDs + secrets
    (r'(?:AWS|aws)[_ ]?(?:ACCESS|SECRET)[_ ]?(?:KEY|ID)[=:]\s*[A-Z0-9+/]{16,}', 'AWS access key'),
    (r'(?:GITHUB|GITLAB|BITBUCKET)[_ ]?TOKEN[=:]\s*[\w-]{20,}', 'SCM platform token'),
    (r'(?:DATABASE_URL|DB_URL|MONGO_URI|REDIS_URL)[=:]\s*\w+://[^@\s]+:[^@\s]+@', 'URL with embedded credentials'),
    (r'(?:PRIVATE|PERSONAL|API|AUTH)[_ ]?(?:TOKEN|KEY)[=:]\s*(?:ghp_|glpat-|sk-|pk\.)[\w-]{16,}', 'known token prefix'),
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'private key block'),
    (r'Bearer\s+eyJ[A-Za-z0-9\-._~+/]+', 'JWT token'),
    (r'password[=:]\s*[^\s]{4,}', 'password value'),
    (r'secret[=:]\s*[^\s]{4,}', 'secret value'),
]

# === Placeholder Patterns ===

PLACEHOLDER_PATTERNS = [
    r'\[Project Name\]',
    r'\[One paragraph',
    r'\[How to run',
    r'\[BULLET LIST',
    r'\[date\]',
    r'<type>',
    r'<Human-Readable Name>',
    r'<glob-or-filename>',
]

# === Required Sections ===

REQUIRED_SECTIONS = [
    'Project Summary',
    'Analysis Scope',
    'Technology Stack',
    'Entry Points',
    'Core Architecture',
    'Dependencies',
    'Development Workflows',
    'Configuration Keys',
    'Known Pitfalls',
    'Confidence and Gaps',
    'Evidence Sources',
]

# === Marker Patterns ===

MARKER_GENERATED_START = '<!-- project-onboard:generated:start -->'
MARKER_GENERATED_END = '<!-- project-onboard:generated:end -->'
MARKER_MANUAL_START = '<!-- project-onboard:manual:start -->'
MARKER_MANUAL_END = '<!-- project-onboard:manual:end -->'


def check_secrets(content):
    issues = []
    for pattern, desc in SECRET_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Exclude false positives: config key names without values
            filtered = []
            for m in matches:
                if isinstance(m, str):
                    m = m.strip()
                    # Skip if it's clearly a config key name reference
                    if re.match(r'^(AWS_|DATABASE_|GITHUB_|GITLAB_|SECRET_|PRIVATE_|API_)[A-Z_]+$', m):
                        continue
                    if m in ('password=', 'secret=', 'token=', 'key=') and not re.search(r'[=:]\s*\S{4,}', m):
                        continue
                    filtered.append(m)
            if filtered:
                issues.append(f'CRITICAL: {desc} found: {filtered[0][:60]}')
    return issues


def check_placeholders(content):
    issues = []
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, content):
            issues.append(f'Unreplaced placeholder matching: {pattern[:50]}')
    return issues


def check_sections(content):
    issues = []
    for section in REQUIRED_SECTIONS:
        if f'## {section}' not in content:
            issues.append(f'Missing required section: {section}')
    lines = content.split('\n')
    current_section = None
    section_empty = True
    for line in lines:
        if line.startswith('## '):
            if current_section and section_empty:
                issues.append(f'Empty section: {current_section}')
            current_section = line[3:].strip()
            section_empty = True
        elif line.startswith('#'):
            pass  # sub-headings don't count as content
        elif line.strip() == '':
            pass  # blank lines don't count as content
        else:
            # Any non-heading, non-blank line = content (includes | tables, - lists)
            section_empty = False
    if current_section and section_empty:
        issues.append(f'Empty section: {current_section}')
    return issues


def check_markers(content):
    issues = []
    gen_start_count = content.count(MARKER_GENERATED_START)
    gen_end_count = content.count(MARKER_GENERATED_END)
    man_start_count = content.count(MARKER_MANUAL_START)
    man_end_count = content.count(MARKER_MANUAL_END)

    if gen_start_count == 0 and man_start_count == 0:
        issues.append('Missing project-onboard markers: generated output must contain generated/end markers')
        return issues

    # Strict count enforcement: _common.md mandates exactly 1 of each marker pair
    if gen_start_count == 0:
        issues.append('Missing generated:start marker')
    elif gen_start_count > 1:
        issues.append(f'Duplicate generated:start marker ({gen_start_count} found, expected 1)')
    if gen_end_count == 0:
        issues.append('Missing generated:end marker')
    elif gen_end_count > 1:
        issues.append(f'Duplicate generated:end marker ({gen_end_count} found, expected 1)')
    if man_start_count > 1:
        issues.append(f'Duplicate manual:start marker ({man_start_count} found, expected at most 1)')
    if man_end_count > 1:
        issues.append(f'Duplicate manual:end marker ({man_end_count} found, expected at most 1)')

    positions = []
    for marker in [MARKER_GENERATED_START, MARKER_GENERATED_END, MARKER_MANUAL_START, MARKER_MANUAL_END]:
        idx = -1
        while True:
            idx = content.find(marker, idx + 1)
            if idx == -1:
                break
            positions.append((idx, marker))

    positions.sort()

    if positions:
        expected_order = [MARKER_GENERATED_START, MARKER_GENERATED_END, MARKER_MANUAL_START, MARKER_MANUAL_END]
        seen = []
        for _, marker in positions:
            seen.append(marker)
        # Check each expected marker appears before the next one
        marker_set = set(m[1] for m in positions)
        if MARKER_GENERATED_END in marker_set and MARKER_GENERATED_START in marker_set:
            if positions[0][1] != MARKER_GENERATED_START:
                issues.append('Markers not in expected order: generated:start must come first')

    # Check no markers inside other markers
    gen_start_pos = content.find(MARKER_GENERATED_START)
    gen_end_pos = content.find(MARKER_GENERATED_END)
    if gen_start_pos >= 0 and gen_end_pos >= 0:
        between = content[gen_start_pos:gen_end_pos]
        if MARKER_MANUAL_START in between or MARKER_MANUAL_END in between:
            issues.append('Manual markers found inside generated block')

    return issues


def check_evidence(content):
    issues = []
    if 'Verified' not in content:
        issues.append('No Verified evidence tag found')
    if content.count('Verified:') + content.count('**Verified**') == 0:
        # At minimum, check for the keyword in a meaningful position (not just in template docs)
        verified_in_docs = 'Verified' in content.split(MARKER_GENERATED_END)[0] if MARKER_GENERATED_END in content else 'Verified' in content[:500]
        if not verified_in_docs:
            issues.append('No Verified evidence tag used in generated content')
    return issues


def main():
    if len(sys.argv) < 2:
        print('Usage: python validate_output.py <path-to-agents.md>')
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    all_issues = []
    all_issues.extend(check_secrets(content))
    all_issues.extend(check_placeholders(content))
    all_issues.extend(check_sections(content))
    all_issues.extend(check_markers(content))
    all_issues.extend(check_evidence(content))

    print(f'File: {os.path.basename(filepath)}')
    print(f'Checks run: 5 (secrets, placeholders, sections, markers, evidence)')
    print(f'Issues found: {len(all_issues)}')

    if all_issues:
        for issue in all_issues:
            print(f'  FAIL: {issue}')
        sys.exit(1)
    else:
        print('  PASS: All security and quality checks passed')
        sys.exit(0)


if __name__ == '__main__':
    main()
