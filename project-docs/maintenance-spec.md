Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# Project Documentation Maintenance Spec

> Applies to: `AGENTS.md`, `PROJECT_STATE.md`, `DEVLOG.md`
> PROJECT_STATE.md sections vary by project type (see SKILL.md for template selection). This spec documents all possible sections; unused sections may be absent from a given project's STATE.

## Document Responsibilities

| File | Role | Content Boundary | Audience |
|------|------|-----------------|----------|
| **AGENTS.md** | Project overview | Project identity, directory structure, class architecture, entry points, dependencies, Notes | Agent startup first impression |
| **PROJECT_STATE.md** | Living document | Full source spectrum (with params), configuration checklist, system flows, done/todo list | New session context recovery |
| **DEVLOG.md** | Development log | Timeline entries โ€?what was done, why, what was learned | Review / traceability |

**No overlap:** AGENTS = architecture overview. STATE = parameter details. AGENTS = directory structure. STATE = file manifest. No single piece of information should appear in two documents.

**No omissions:** Every status change updates STATE (living document). Major milestones append DEVLOG. Architecture changes append AGENTS.

## AGENTS.md Update Rules

### Trigger conditions
- New source file, class, or module subdirectory
- New key asset path or configuration file
- Plugin/package added or removed
- Entry point change (startup file, main class, entry scene)
- Dependency manifest change (build config, package manager)

### Non-triggers
- Bug fixes, parameter tweaks, config changes โ?record in PROJECT_STATE.md
- Feature status changes โ?record in PROJECT_STATE.md "Current Status" list

### Update frequency
Per major milestone (~every 3-5 new files/classes, or weekly).

## PROJECT_STATE.md Update Rules

### Per-section update frequency

Sections adapt to project type. Unreal and Unity have engine-specific sections; all other types use the generic template. See SKILL.md "Template Selection" for auto-discovery rules.

| Section (generic / game-engine) | Frequency | Trigger |
|---------|-----------|---------|
| ยง2 Directory Structure | Low | New/deleted subdirectory |
| ยง3 Source/Script Spectrum | Medium | New file / class / new key member |
| ยง4 Configuration & Environment / Prefab & Asset Checklist | High | Any config file change, defaults change |
| ยง5 Module Map / Input System | Medium | New module, new binding, new package export |
| ยง6 Architecture & Data Flow / Game Systems | Medium | System logic change |
| ยง7 Dependencies & Services / Scene/Level Config | Medium | New service, new actor, new external dependency |
| ยง8 Key Parameters Quick Reference | High | Any numeric parameter change |
| ยง9 Build & Run / Build Settings | Very low | New compile errors, build command changes |
| ยง10 Current Status | **Every session end** | Done list, todo list, known issues |

### Done/Todo Entry Template
```
### Done (N/M)
<!-- "N completed out of M total" โ€?update the ratio when items move. -->
- [x] <brief description>
### Todo
| # | Item | Priority |
|---|---|---|
| 1 | <description> | High/Med/Low/TBD |
```

## DEVLOG.md Update Rules

### Entry format
```markdown
## YYYY-MM-DD
### <brief title>
- <what was done>
- <why this approach>
- <problems encountered + how resolved>
- <lessons learned>
```

### Granularity
One entry per **day** or per **feature milestone**. Do not record every minor edit or rebuild.

### Prohibited
- โ?Duplicating parameter tables or config checklists already in STATE
- โ?Using DEVLOG as a progress tracker in place of STATE's "Current Status"
- โ?Describing "what will be done" (only write after completion)

## Consistency Checklist

Run after every STATE update:

- [ ] AGENTS directory structure entries all have counterparts in STATE
- [ ] STATE ยง8 parameter values match actual source/code defaults (e.g., `.h` defaults, config file values, class default overrides per template type)
- [ ] STATE ยง10 todo list does not contradict DEVLOG latest entry (if DEVLOG says done, STATE should match)
- [ ] No duplicate information across the three documents (one fact = one location)
