# Project Ledger Development Log

> Append chronologically. Latest on top.

---

## 2026-06-30

### Project ledger repository established

- **What was done**:
  - Created GitHub organization `Zions-store` with profile README
  - Set up `project-ledger` monorepo containing `project-onboard` and `project-docs` skills
  - Deprecated old standalone `ZionXiaoxiSuOGLocGo/project-onboard` repo (13 commits, 4 stars preserved), added [DEPRECATED] notice with redirect to new location
  - Established local development workflow: `C:\Users\22410\projects\Zion's Store\project-ledger\` with NTFS Junction symlinks to `~/.config/opencode/skills/` for zero-maintenance sync

- **Why this approach**:
  - Monorepo under a dedicated GitHub organization separates the "Zion's Store" brand from personal account repos
  - Junction symlinks eliminate the manual copy-and-exclude-.git workflow previously documented in project-onboard CHANGELOG v1.0.1
  - Each skill gets a GPL-3.0 LICENSE at both repo root and skill directory level for max clarity

### Comprehensive two-round audit — 28 issues found, all resolved

- **What was done**:
  - Round 1 (format/consistency): 12 issues — copyright notices, template placeholders, CHANGELOG formatting (9 fixed, 3 deferred)
  - Round 2 (content quality): 28 issues across all files — full reading of every SKILL.md, README, reference, template, and maintenance-spec
  - Fixed: type-specific template system, AGENTS-to-STATE field mapping, complete update workflow, parameter value verification, trigger phrase alignment, Build & Test sections in 6 rule packs, edge case handling (empty repo, monorepo, invalid --type), version metadata, documentation comments

- **Problems encountered + how resolved**:
  - `Assets/Packages/manifest.json` is not a valid Unity path. Fixed to `Packages/manifest.json`.
  - 6 out of 11 rule packs had no Build & Test sections. Added sections for csharp, lua, nodejs, python, unity, unreal — matching the AGENTS.md template requirement.
  - Python detection table was missing `Pipfile` and `environment.yml` despite python.md checking them. Extended signatures.
  - Docker/database/shader entries in detection table had no corresponding reference files. Converted to sub-type hints in general.md with explicit scanning instructions.
  - project-docs template was hard-coded to Unreal Engine, making it non-functional for Unity/Node.js/Python etc. Restructured into `templates/unreal/`, `templates/unity/`, and `templates/general/` with auto-detection from AGENTS.md Type field.
  - project-docs SKILL.md said "pre-fill §1-§3 from AGENTS.md" but never specified HOW. Added complete 7-row field mapping table.
  - Update workflow only listed 4 sections; maintenance-spec defined triggers for all 10. Expanded workflow to cover §1-§10.

- **Lessons learned**:
  - Template-driven skills need explicit field-level mapping tables. "Pre-fill from AGENTS.md" is too vague for LLMs.
  - Detection table and reference files must stay in sync. When a reference file grows, the detection signature should grow too.
  - Rule pack structure consistency matters. Every rule pack should have the same set of sections, even if some only say "no specific info available."
  - `glob *` is more precise than "look for top-level entries" — different LLMs interpret the latter differently.
  - The `without Assets/` qualifier on Node.js and C# detection is deliberate: Unity projects have `package.json` in `ProjectSettings/` and `*.csproj` as generated files. The detection order protects against false matches, but the qualifiers serve as a secondary safety net.

### Key architectural decisions

- **Type-specific templates over one-size-fits-all**: project-docs now selects `PROJECT_STATE.md.tmpl` based on AGENTS.md Type field. Unreal/Unity get engine-specific templates; all other types share a clean generic template.
- **Monorepo over per-skill repos**: Easier to discover related skills, single clone. If individual repos are ever needed, git filter-repo can split them later.
- **GPL-3.0 consistency**: All skills and the repo itself use the same license.
- **Version metadata in SKILL.md frontmatter**: Both skills now declare their version (`v1.0.0` for project-docs, `v1.1.0` for project-onboard).

### Template auto-discovery replaces hardcoded mapping

- **What was done**:
  - Replaced the hardcoded `Template Selection by Project Type` mapping table with auto-discovery: the skill tries `templates/<type>/PROJECT_STATE.md.tmpl`, falling back to `templates/PROJECT_STATE.md.tmpl` if absent.
  - Updated SKILL.md, root README.md, project-docs/README.md, and maintenance-spec.md.

- **Why this approach**:
  - Mirrors project-onboard's rule pack auto-discovery (`references/<type>.md` → fallback `general.md`). Adding a new engine type now needs only `templates/<name>/PROJECT_STATE.md.tmpl` — zero code changes, no mapping table to update.
  - Architectural consistency across both skills in the same repo.

- **Lessons learned**:
  - When two skills share a pattern (rule pack discovery / template discovery), they should stay architecturally identical. Simple fallback logic scales better than documentation tables.

---

<!-- Append new entries above this line. -->
