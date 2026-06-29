---
name: project-docs
description: Initialize or update the three-document project knowledge system (AGENTS.md + PROJECT_STATE.md + DEVLOG.md). Use when the user says "init docs", "建立文档体系", "project-docs", "更新项目状态", or when a new project needs a living documentation framework.
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# project-docs

Creates and maintains a three-document project knowledge system.

## Three-Document System

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `AGENTS.md` | Project overview: identity, directory structure, class architecture, entry points, dependencies, Notes | Per milestone (~3-5 new files/classes) |
| `PROJECT_STATE.md` | Living document: full class spectrum (with params), blueprint config checklist, input system map, game system flows, level config, done/todo list | Every session end |
| `DEVLOG.md` | Development log: timeline entries — what was done, why, what was learned | Per day or per feature milestone |

See `maintenance-spec.md` for detailed rules on update triggers, content boundaries, and consistency checks.

## When to Use This Skill

- User says "init project docs" / "建立文档体系" / "project-docs"
- A new project needs PROJECT_STATE.md and DEVLOG.md
- An existing project has AGENTS.md but missing the other two
- User asks to update project status after a session

## Workflow

### 1. Initialize (new project / missing documents)

0. **Ask the user** what language to generate documents in:
   > "What language should the project docs be written in? (e.g., English, 中文, 日本語, 한국어, Français)"

1. Check if `AGENTS.md` exists.
   - **If not**: Guide user to generate AGENTS.md first (e.g., run the project-onboard skill or similar initialization). Stop here.
   - **If yes**: Read and extract project name, engine version, class list from it.

2. Generate `PROJECT_STATE.md` from `templates/PROJECT_STATE.md.tmpl`:
   - Pre-fill §1-§3 from AGENTS.md data.
   - **If language is not English**: translate the section headers, labels, and placeholder descriptions to the chosen language before writing. Keep `{{PLACEHOLDER}}` markers intact.

3. Generate `DEVLOG.md` from `templates/DEVLOG.md.tmpl`:
   - Fill in project name.
   - **If language is not English**: translate the template text to the chosen language.

4. Prepend the following block to the top of `AGENTS.md` (after the title line):
   ```markdown
   ## Read This First

   1. Read `PROJECT_STATE.md` — current task status and to-do items (§10)
   2. Read `DEVLOG.md` — recent development history

   ---
   ```
   **If language is not English**: translate the heading, list items, and descriptions.

5. Report what was created and in which language.

### 2. Update (existing documents)

1. Read `PROJECT_STATE.md` → identify §10 todo list
2. Ask user what was completed / what changed
3. Update §3 (new members), §4 (blueprint changes), §8 (parameter changes), §10 (done/todo/issues)
4. Append entry to `DEVLOG.md` (per `maintenance-spec.md` format)
5. If architecture changed (new classes, plugins, directories) → update `AGENTS.md`

### 3. Consistency Check

After any update, verify:
- No overlapping data between AGENTS and STATE (architecture vs details)
- STATE §10 todo list matches DEVLOG latest entry
- AGENTS directory structure entries exist in STATE file manifest

## Templates

- `templates/PROJECT_STATE.md.tmpl` — Full §1-§10 template with `{{PLACEHOLDER}}` markers. English source; LLM translates to user's chosen language at generation time.
- `templates/DEVLOG.md.tmpl` — First-entry template. Same translation pattern.

## Rules

- **Never overwrite** existing files. If a document exists, update it in-place.
- **Respect content boundaries**: AGENTS = architecture overview. STATE = parameter details + status. DEVLOG = timeline narrative.
- **Maintenance spec**: See `maintenance-spec.md` for exact update triggers, content boundaries, and prohibited practices.
- **Project-specific paths/class names** in STATE/DLOG are expected — these are project documents, not reusable manuals.
