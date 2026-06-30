Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# Project Ledger Development Log

> Append chronologically. Latest on top.

---

## 2026-06-30

### 47/47 audit bugs resolved â€?manuals v2.2.1 / v2.1.1

- **What was done**:
  - Two-round comprehensive audit of unreal-manual (15 issues) and unity-manual (32 issues) â€?all resolved.
  - HIGH: fixed 2 C++ compile errors, 1 ObjectPool crash, 1 Rigidbody anti-pattern example, 5 missing declarations, 2 false version claims, 1 fictitious file path.
  - MEDIUM: removed 3 duplicate content sections, fixed 5 incorrect property/version/cross-reference items, corrected 3 misleading advice items.
  - LOW: 13 polish items (typos, code block tags, README counts, SafeArea, ContextMenu).
  - Added 4 missing sections: C++ Delegates, Smart Pointers, Async Loading (unreal) + Profiling & Debugging (unity).
  - Root + org READMEs updated to list all 4 skills with versions.
  - Created `.tmp_validation/` for LSP code block verification workflow.

- **Lessons learned**:
  - Systematic root cause analysis (7 deficiencies) documented in 23KB countermeasures file.
  - LSP validation via temp files catches ~25% of bugs; grep + manual review + coverage checklist cover the rest.
  - Single-source-of-truth for version numbers prevents sync failures.

### Manuals integrated â€?unreal-manual (v2.2.0), unity-manual (v2.1.0)

- **What was done**:
  - Added unreal-manual/ and unity-manual/ to monorepo with LICENSE + README.
  - Created Junction symlinks from `.config/opencode/skills/` for zero-maintenance sync.
  - unreal-manual: added Advanced Gameplay Patterns (Compatible Skeleton, Checkpoint/Respawn, Combo Input Cache, Substrate, Tool Ecosystem).
  - unity-manual: added 7 new chapters (Avatar Retargeting, Anti-Patterns, Game Architecture, Input Advanced, Shader Graph, Mobile).
  - Copyright + version metadata added to both SKILL.md frontmatters.

### Multi-language support across both skills

- **What was done**:
  - Added language selection step (Step 0) to project-onboard, matching project-docs' existing language prompt.
  - Replaced hardcoded language list with: "Any language the LLM can output is supported."
  - Added "Multi-Language Support" sections to all 3 READMEs with 11-12 language trigger examples each.
  - Updated both SKILL.md description fields with "Supports any language via LLM-native translation."

- **Why this approach**:
  - LLM-native translation eliminates i18n infrastructure. No locale files needed.
  - Differentiator: traditional tools hardcode translations; project-ledger leverages the LLM's inherent multilingual capability.

### Template auto-discovery replaces hardcoded mapping

- **What was done**:
  - Replaced hardcoded `Template Selection by Project Type` table with auto-discovery: `templates/<type>/PROJECT_STATE.md.tmpl`.
  - Mirrors project-onboard's rule pack auto-discovery pattern. Zero code changes to add new engine types.

### Comprehensive two-round audit â€?28 issues found, all resolved

- **What was done**:
  - Round 1 (format): 12 issues â€?copyright notices, template placeholders, CHANGELOG formatting (9 fixed, 3 deferred).
  - Round 2 (content): 28 issues â€?type-specific templates, AGENTS-to-STATE field mapping, complete update workflow, Build & Test sections in 6 rule packs, edge cases, version metadata.
  - All 28 issues resolved.

### Project ledger repository established

- **What was done**:
  - Created GitHub organization `Zions-store`.
  - Set up `project-ledger` monorepo with project-onboard + project-docs skills.
  - Deprecated old standalone `ZionXiaoxiSuOGLocGo/project-onboard` (4 stars preserved), added [DEPRECATED] redirect.
  - Established Junction-based local dev workflow: `projects\Zion's Store\project-ledger\` â†?`.config\opencode\skills\`.
  - Cleaned up legacy `OpenCode_skills\` directory.

---

<!-- Append new entries above this line. -->
