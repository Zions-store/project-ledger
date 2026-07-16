Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Rule Pack Template

Use this template to create a new project type rule pack. Fill in the frontmatter and replace `<Type>` with the actual project type name.

---

```yaml
---
schema_version: 1
id: <type>
display_name: <Human-Readable Name>
priority: <0-100, normal packs typically 50-100; used for scan ordering and tie-breaking, never causes first-match selection>
aliases: []
kind: normal

# kind values:
#   normal    - standard type rule pack (default)
#   fallback  - loaded when no normal candidate reaches low confidence (only `general`)
#   refinement - sub-type that depends on a parent match (monogame)

signatures:
  # Use `any` for simple OR matching (any one entry = candidate)
  any:
    - <glob-or-filename>
  # Or use `any_of` with `all` groups for AND combinations:
  # any_of:
  #   - all: [<must-have-1>, <must-have-2>]
  #   - all: [<alternative-set-1>, <alternative-set-2>]
  # Or use `all` for strict AND (all entries must match)

exclusions:
  # Use `all` for AND exclusion (all entries must match to exclude)
  all: []

refinements: []

workspace_files: []

priority_files:
  - <most-important-files>

entry_point_patterns: []

external_reference_mechanisms: []

generated_paths: []

large_structured_files: []

binary_asset_types: []

default_ignore_paths: []

known_blind_spots: []

optional_output_sections: []
---
```

## Field Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `schema_version` | Yes | int | Schema version (currently `1`) |
| `id` | Yes | string | Machine identifier, matches filename (e.g. `python`) |
| `display_name` | Yes | string | Human-readable name (e.g. `Python`) |
| `priority` | Yes | int | 0–100, used for scan ordering and confidence tie-breaking. Never causes first-match selection. |
| `aliases` | Yes | list | Alternative short names (e.g. `["py"]`) |
| `kind` | Yes | string | `normal` (standard type), `fallback` (activated when no normal candidate reaches low confidence), or part of `refinements` for sub-types |
| `signatures` | Yes | dict | Detection signatures. Supports `all` (all must match), `any` (at least one matches), `any_of` (list of `all` groups). [See example above for syntax.] |
| `exclusions` | No | dict | Exclusion rules. Supports `all` (all entries must match to exclude). Use `all` to require both `Assets/` and `ProjectSettings/` before excluding C#/Node in Unity projects. |
| `refinements` | No | dict or list | Content-based sub-type rules (e.g. C# -> MonoGame). Can be a dict with `parent`, `condition` for simple refinements, or a list of such dicts. |
| `workspace_files` | No | list | Files indicating multi-project workspaces |
| `priority_files` | Yes | list | Top 3-5 files to read first |
| `entry_point_patterns` | No | list | POSIX extended regex patterns for finding entry points via grep. Use `[[:space:]]+` for whitespace, `\(` to match literal parens (ERE treats `()` as grouping). Avoid GNU/PCRE extensions: `\b`, `\s`, `\d`, `\w`. All patterns must validate as strict POSIX ERE. |
| `external_reference_mechanisms` | No | list | How this ecosystem references external code |
| `generated_paths` | No | list | Directories typically containing generated code |
| `large_structured_files` | No | list | Glob patterns for large structured text files |
| `binary_asset_types` | No | list | File extensions for binary assets |
| `default_ignore_paths` | No | list | Type-specific directories to skip |
| `known_blind_spots` | No | list | Things this rule pack cannot detect |
| `optional_output_sections` | No | list | Additional AGENTS.md sections for this type |

---

# <Type> Project Analysis Rules

## Detection Evidence

[What file/folder signatures trigger detection. How to confirm a match is genuine.]

## False Positives and Exclusions

[When this type's signatures appear but the project is actually something else.]

## Priority Metadata

[Which files to read first and what to extract from them.]

## Workspace and Module Discovery

[How to discover multi-module structures, workspaces, and sub-projects.]

## Entry Point Discovery

[How to locate runnable entry points, main files, and startup scenes.]

## Dependency Discovery

[How to find and interpret dependency declarations. Key packages and their meanings.]

## Architecture Evidence

[Common architectural patterns and how to detect them.]

## Large Structured File Strategy

[How to handle type-specific large files (e.g. .unity, .ipynb, lockfiles).]

## Generated Content

[Where generated code typically lives and how to identify its source.]

## External References

[How this ecosystem references code outside the project root.]

## Build and Test Command Evidence

[Where to find build/test/lint commands and how to verify them.]

## Type-Specific AGENTS.md Additions

[Additional sections to include in the output for this project type.]

## Known Limitations

[What this rule pack cannot detect or analyze. Honest about blind spots.]
