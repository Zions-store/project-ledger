# Project Documentation Maintenance Spec

> Applies to: `AGENTS.md`, `PROJECT_STATE.md`, `DEVLOG.md`

## Document Responsibilities

| File | Role | Content Boundary | Audience |
|------|------|-----------------|----------|
| **AGENTS.md** | Project overview | Project identity, directory structure, class architecture, entry points, dependencies, Notes | opencode startup first impression |
| **PROJECT_STATE.md** | Living document | Full class spectrum (with params), blueprint config checklist, input system map, game system flows, level config, done/todo list | New session context recovery |
| **DEVLOG.md** | Development log | Timeline entries — what was done, why, what was learned | Review / traceability |

**No overlap:** AGENTS = architecture overview. STATE = parameter details. AGENTS = directory structure. STATE = file manifest. No single piece of information should appear in two documents.

**No omissions:** Every status change updates STATE (living document). Major milestones append DEVLOG. Architecture changes append AGENTS.

## AGENTS.md Update Rules

### Trigger conditions
- New C++ class or module subdirectory
- New blueprint asset path (under `Content/`)
- Plugin added/removed
- Entry point change (GameMode, level, PlayerController)
- Module dependency change (Build.cs)

### Non-triggers
- Bug fixes, parameter tweaks, blueprint config changes → record in PROJECT_STATE.md
- Feature status changes → record in PROJECT_STATE.md "Current Status" list

### Update frequency
Per major milestone (~every 3-5 new files/classes, or weekly).

## PROJECT_STATE.md Update Rules

### Per-section update frequency

| Section | Frequency | Trigger |
|---------|-----------|---------|
| 2. Directory Structure | Low | New/deleted subdirectory |
| 3. C++ Class Spectrum | Medium | New class / new key member |
| 4. Blueprint Asset Checklist | High | Any BP Class Defaults config change |
| 5. Input System | Medium | New/modified InputAction binding |
| 6. Game Systems | Medium | System logic change |
| 7. Level Config | Medium | Actor added/removed from level |
| 8. Key Parameters Quick Reference | High | Any numeric parameter change |
| 9. Compilation & Build | Very low | Only when new compile tricks/error patterns discovered |
| 10. Current Status | **Every session end** | Done list, todo list, known issues |

### Done/Todo Entry Template
```
### Done (N/M)
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
One entry per **day** or per **feature milestone**. Do not record every Ctrl+Alt+F11.

### Prohibited
- ❌ Duplicating parameter tables or config checklists already in STATE
- ❌ Using DEVLOG as a progress tracker in place of STATE's "Current Status"
- ❌ Describing "what will be done" (only write after completion)

## Consistency Checklist

Run after every STATE update:

- [ ] AGENTS directory structure entries all have counterparts in STATE
- [ ] STATE parameter quick reference values match .h defaults (also check BP CDO overrides)
- [ ] STATE todo list does not contradict DEVLOG latest entry (if DEVLOG says done, STATE should match)
- [ ] No duplicate information across the three documents (one fact = one location)
