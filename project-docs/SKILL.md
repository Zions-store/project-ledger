---
name: project-docs
version: 1.0.0
description: Initialize or update the three-document project knowledge system (AGENTS.md + PROJECT_STATE.md + DEVLOG.md). Use when the user says "init docs", "建立文档体系", "project-docs", "更新项目状态", or when a new project needs a living documentation framework.
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# project-docs

Creates and maintains a three-document project knowledge system. Supports all project types detected by project-onboard — auto-selects the correct template based on your project type.

## Three-Document System

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `AGENTS.md` | Project overview: identity, directory structure, class architecture, entry points, dependencies, Notes | Per milestone (~3-5 new files/classes) |
| `PROJECT_STATE.md` | Living document: full class/source spectrum (with params), configuration, module map, system flows, done/todo list | Every session end |
| `DEVLOG.md` | Development log: timeline entries — what was done, why, what was learned | Per day or per feature milestone |

See `maintenance-spec.md` for detailed rules on update triggers, content boundaries, and consistency checks.

## Template Selection

Templates follow the same auto-discovery pattern as `project-onboard` rule packs. The skill attempts to load `templates/<type>/PROJECT_STATE.md.tmpl` where `<type>` is the lowercased Type value from `AGENTS.md` Basic Information. If no type-specific template exists, it falls back to `templates/PROJECT_STATE.md.tmpl`.

```
templates/<type>/PROJECT_STATE.md.tmpl exists? → use it
                                             no → use templates/PROJECT_STATE.md.tmpl (generic fallback)
```

Adding support for a new engine or framework: create `templates/<type>/PROJECT_STATE.md.tmpl`. No code changes needed — the skill discovers it automatically.

All types share `templates/DEVLOG.md.tmpl` (project-type-agnostic).

## AGENTS.md → PROJECT_STATE.md Field Mapping

When pre-filling the `PROJECT_STATE.md` from `AGENTS.md` data, use this mapping:

| AGENTS.md Section | AGENTS.md Field | STATE Template Section | STATE Placeholder |
|---|---|---|---|
| Basic Information | Type, Language, Framework/Engine, Key Dependencies | §1 Project Identity | `{{PROJECT_TYPE}}`, `{{LANGUAGE}}`, `{{FRAMEWORK}}`, `{{KEY_DEPENDENCIES}}` |
| Basic Information | Engine (for game projects) | §1 Project Identity | `{{ENGINE_VERSION}}` |
| Directory Structure | Directories and descriptions | §2 Directory Structure | `{{DIRECTORY_TREE}}` (generic) or `Source/{{MODULE_NAME}}/...` (UE) |
| Core Architecture | Key files/classes and roles | §3 Source/Script Spectrum | `{{CLASS_NAME}}`, `{{RESPONSIBILITY}}`, `{{FILE_NAME}}` |
| Dependencies | Package summary | §4 Configuration / §7 Dependencies | `{{CONFIG_KEY}}`, `{{DEP_NAME}}` (context-dependent) |
| Build & Run | Build/test commands | §9 Build & Run | `{{BUILD_CMD}}`, `{{RUN_CMD}}`, `{{TEST_CMD}}` |
| Entry Points | Startup file/scene and role | §1 Project Identity (Module) | `{{MODULE_NAME}}` |

For **non-English output**: translate section headers, labels, and placeholder descriptions, but keep `{{PLACEHOLDER}}` markers intact.

## When to Use This Skill

- User says "init project docs" / "建立文档体系" / "project-docs"
- A new project needs PROJECT_STATE.md and DEVLOG.md
- An existing project has AGENTS.md but missing the other two
- User asks to update project status after a session

## Workflow

### 1. Initialize (new project / missing documents)

0. Ask the user what language to generate documents in. Default to English if they skip or say "I don't care":
   > "What language should the project docs be written in? (Default: English. Also supported: 中文, 日本語, 한국어, Français)"

1. Check if `AGENTS.md` exists.
   - **If not**: Offer to run the `project-onboard` skill first to generate AGENTS.md. Stop here.
   - **If yes**: Read AGENTS.md and extract:
     - Project name
     - **Type** (from Basic Information — e.g., "unreal", "unity", "nodejs", "python")
     - Core architecture (classes, files, roles)

2. **Detect template**: Based on the extracted Type (lowercased), try to load a type-specific template. If no match, fall back to the generic template:
   - First try `templates/<type>/PROJECT_STATE.md.tmpl`
   - If that file does not exist, use `templates/PROJECT_STATE.md.tmpl` (generic)

3. Generate `PROJECT_STATE.md` from the selected template:
   - Pre-fill §1-§3 from AGENTS.md data using the field mapping table above.
   - Leave remaining sections with their placeholder structure for future updates.

4. Generate `DEVLOG.md` from `templates/DEVLOG.md.tmpl`:
   - Fill in project name.
   - Leave the entry template ready for the first development log entry.

5. Prepend the following block to the top of `AGENTS.md`, directly after the `# Project Name` heading line (but before the rest of the content):
   ```markdown
   ## Read This First

   1. Read `PROJECT_STATE.md` — current task status and to-do items (§10)
   2. Read `DEVLOG.md` — recent development history

   ---
   ```

6. Report what was created, which template was used, and in which language.

### 2. Update (existing documents)

1. Read `PROJECT_STATE.md` → identify §10 todo list
2. Ask user what was completed / what changed
3. Update the affected sections:
   - **§1-§2**: if project identity or directory structure changed
   - **§3**: new classes, files, or key members
   - **§4**: configuration changes (blueprint properties, prefab settings, or generic config)
   - **§5**: input bindings, action mappings, or module/package changes
   - **§6**: system logic, architecture flow, or game system changes
   - **§7**: scene/level config or external services changes
   - **§8**: any numeric parameter changes
   - **§9**: build issues, new compile errors, or command changes
   - **§10**: **always update** — done list, todo list, known issues
4. Append entry to `DEVLOG.md` (per `maintenance-spec.md` format)
5. If architecture changed (new classes, plugins, directories) → update `AGENTS.md`

### 3. Consistency Check

After any update, verify:

- No overlapping data between AGENTS.md and PROJECT_STATE.md (architecture overview vs parameter details)
- AGENTS.md directory structure entries all have counterparts in PROJECT_STATE.md
- PROJECT_STATE.md §8 parameter values match actual source defaults (e.g., `.h` defaults, config file values, BP CDO overrides)
- PROJECT_STATE.md §10 todo list does not contradict DEVLOG.md latest entry (if DEVLOG says done, STATE should match)
- No duplicate information across the three documents (one fact = one location)

## Templates

Templates are auto-discovered by project type — no hardcoded mapping table. The directory mirrors the `project-onboard` reference structure:

```
templates/
├── DEVLOG.md.tmpl              ← All types (generic)
├── PROJECT_STATE.md.tmpl       ← Fallback (generic)
├── unreal/PROJECT_STATE.md.tmpl     ← Unreal Engine
└── unity/PROJECT_STATE.md.tmpl      ← Unity
```

`templates/<type>/PROJECT_STATE.md.tmpl` files are optional. The skill tries to load one matching the AGENTS.md Type; if absent, it uses the root generic template.

**Adding a new type**: create `templates/<type>/PROJECT_STATE.md.tmpl` with type-specific sections. The skill discovers it on the next run — zero code changes.

## Rules

- **Never overwrite** existing files. If a document exists, update it in-place.
- **Respect content boundaries**: AGENTS.md = architecture overview. PROJECT_STATE.md = parameter details + status. DEVLOG.md = timeline narrative.
- **Maintenance spec**: See `maintenance-spec.md` for exact update triggers, content boundaries, and prohibited practices.
- **Project-specific paths/class names** in STATE/DEVLOG are expected — these are project documents, not reusable manuals.
