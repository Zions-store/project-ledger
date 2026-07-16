Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# project-onboard Changelog

## [2.0.0] - 2026-07-17
**Source**: v2.0.0-rc1 finalization

### Release validation
- 48/48 behavior cases passed (46 unique OpenCode executions).
- 0 failures and 0 blocked cases.
- Static validation passed on Python 3.11 and 3.12.
- Fixture contracts passed on Linux.
- Tested host: OpenCode 1.17.18.

### Changed
- Version promoted from 2.0.0-rc1 to 2.0.0 (SKILL.md, VERSION, templates/AGENTS.md).
- README: removed release-candidate warning; added host compatibility matrix; corrected runtime footprint to 16 files.
- Root README: updated project-onboard entry to v2.0.0 with host verification status.
- CI: upgraded `actions/checkout` to v5 and `actions/setup-python` to v6.

No runtime behavior changes from 2.0.0-rc1; this release promotes the version and aligns public documentation.

---

## [2.0.0-rc1] - 2026-07-11 — Execution Modes & Plugin Architecture
**Source**: project-onboard P0 behavior contract + P1 self-registration

### Added
- **Four execution modes**: inspect (read-only analysis, default), generate (create AGENTS.md), refresh (incremental update with auto/manual zone protection), audit (structured diff report without writing). Mode is inferred from trigger phrases and controls write behavior explicitly.
- **Execution mode trigger phrase mapping**: "analyze"/"what does this project do" -> inspect; "generate"/"create"/"onboard" -> generate; "refresh"/"update"/"sync" -> refresh; "audit"/"check"/"is...still accurate" -> audit.
- **Rule pack self-registration**: all 12 rule packs now carry complete YAML frontmatter (19 fields: schema_version, id, display_name, priority, kind, aliases, signatures, exclusions, refinements, workspace_files, priority_files, entry_point_patterns, external_reference_mechanisms, generated_paths, large_structured_files, binary_asset_types, default_ignore_paths, known_blind_spots, optional_output_sections). New types auto-discover without SKILL.md or README modification.
- **`references/_rule-pack-template.md`**: complete template with field reference table for creating new rule packs.
- **Formal contract template**: `templates/AGENTS.md` now includes `generated:start/end` + `manual:start/end` markers with mode-specific behaviors, template version field, and evidence-tagged output sections.
- **Atomic write**: generate/refresh modes write to temporary file, validate, and atomically replace. No direct overwrite or in-place modification.
- **validate_rule_packs.py**: upgraded to enforce all 19 fields, field types, kind values (normal/fallback/refinement), refinement schema (parent must be present in refinements entries), unique fallback check, and id/alias uniqueness.
- **Mode-depth mapping**: inspect defaults to quick; generate/refresh/audit default to standard; user can override depth independently of mode.

### Changed
- **SKILL.md**: full rewrite for v2.0.0 — Execution Modes section added as primary behavioral contract; Step 0 now resolves mode and language simultaneously; all steps are mode-aware; anti-pitfalls enforce mode contracts (inspect NEVER writes).
- **SKILL.md version**: 1.4.0 -> 2.0.0-rc1.
- **README**: updated with execution mode table, scan depth table, self-registration workflow; file count updated (16->19); comparison table extended.
- **templates/AGENTS.md**: upgraded from basic template to formal contract with markers, mode documentation, template version, and evidence-tagged sections.

### Removed
- All old trigger-words-default-to-write behavior. inspect mode is now the default for ambiguous requests.
- "EXACTLY this structure" requirement for output — replaced with required/conditional section model.
- Old "Adding New Project Types" workflow requiring three-file modification — replaced with single-file self-registration.
- Residual old code references: first match wins cleanup, fixed 50-file artifacts, EXACTLY template remnants.

### Principles
- inspect is the default mode. Files are written only when explicitly requested.
- Rule packs define themselves. The Skill discovers them. One file = one new type.
- Write operations are atomic. Manual content is sacred.
- Evidence, scope, and gaps are reported. The Skill communicates what it did not know, not just what it did.

---

## [1.4.0] - 2026-07-11 — Project Topology & Workspace Support
**Source**: project-onboard audit P1 topology items

### Added
- **Candidate scoring model**: replaced "first match wins" with evidence-based candidate collection, scoring (high/medium/low + evidence/counter-evidence/basis), and topology classification.
- **Topology classification**: single project, multi-module, monorepo, polyglot, engine project, and unknown categories with distinct analysis strategies.
- **Workspace detection by ecosystem**: `_common.md` §12 now lists workspace files and external reference mechanisms for all 10 ecosystems (Node.js pnpm-workspace/Turborepo/Nx, Rust Cargo [workspace], Go go.work, Java includeBuild/settings.gradle, C/C++ CMake add_subdirectory, .NET .sln, Python uv workspace, Unity local UPM, Unreal external plugins).
- **Sub-project analysis**: monorepos get a root-level project matrix with per-sub-project summaries. Multi-module projects load the same rule pack across all modules.
- **Blueprint-only Unreal detection**: `.uproject` without `Source/` is now recognized as an Unreal candidate (engine project with Blueprint limitation noted).
- **External reference recording**: symlink targets, path dependencies, submodules, and composite builds are recorded with their linkage type, reference mechanism, and project role — without being entered.

### Changed
- **SKILL.md Step 1**: added topology discovery phase that scans for workspace files, multi-project signals, and external references before type detection.
- **SKILL.md Step 2**: full rewrite — collects all candidates across all scopes, applies content-based refinement, scores each candidate with evidence, and classifies topology. The "first match wins" rule is formally removed.
- **SKILL.md Step 3**: now handles multi-type loading — monorepos load per-sub-project rule packs, polyglot projects load all matching rule packs simultaneously.
- **SKILL.md version**: 1.3.0 -> 1.4.0.

### Removed
- **First match wins**: formally removed from detection logic. All candidates are collected, scored, and compared before a topology decision is made. Cleanup of residual code and old documentation references deferred to v2.0.0.

### Principles
- Topology discovery precedes type detection. Workspace graph determines analysis scope before rule packs are loaded.
- External references are recorded but not entered without authorization. The user controls scope expansion.
- Blueprint-only projects are still Unreal projects — binary asset limitation is a transparency issue, not a detection gap.

---

## [1.3.0] - 2026-07-11 — Security Foundation & Common Scan Kernel
**Source**: project-onboard comprehensive audit P0+P1 safety items

### Added
- **`references/_common.md`** (15 chapters): universal security rules and scan strategy applicable to all project types. Covers trust boundary, authorized roots, secret/sensitive data rules, global ignore paths, symlink/junction/external reference handling, A-G file role classification, text/binary detection, large file strategy, generated content rules, multi-dimensional scan budgets, monorepo/polyglot rules, evidence levels, output scope/gap reporting, and pre-write validation checklist.
- **`templates/AGENTS.md`**: output template with required sections (Project Summary, Technology Stack, Entry Points, Core Architecture, Dependencies, Development Workflows, Configuration Keys, Known Pitfalls) and conditional sections (Analysis Scope, Subproject Map, Editing Boundaries, Generated/Vendor Paths, External References, Confidence and Gaps).
- **`tests/validate_rule_packs.py`**: rule pack structure and section validator.
- **`tests/validate_output.py`**: AGENTS.md output quality checker (secret detection, required sections, evidence tagging).
- **`--depth` parameter**: quick / standard / deep scan depth. Quick produces 20-60 line summary. Deep doubles scan budgets for large projects.
- **`--include-root` parameter**: authorize additional read-only scan roots for external dependencies.

### Changed
- **SKILL.md**: version 1.2.1 -> 1.3.0. Added Security Foundation section (trust boundary, authorized boundaries, secret rules, global ignore paths, symlink rules). Execution flow restructured: Step 0 now skips confirmation when language is clear; Step 1 adds boundary establishment and AGENTS.md conflict detection; Step 3 loads _common.md before type-specific rule packs; Step 4 adds file role classification (A-G) and scan budgets; Step 5 adopts new output template with evidence tagging; Step 6 (new) adds pre-write safety validation; Step 7 report includes scan depth, confidence levels, and gap reporting.
- **Write behavior**: an AGENTS.md found at the target path without project-onboard markers is treated as manual and not overwritten without explicit confirmation. This is transition-period behavior; full inspect/generate/refresh/audit mode system arrives in v2.0.0.
- **Scan strategy**: replaced fixed "50 file limit" with multi-dimensional budgets (file count soft target, byte budget, per-file complete-read budget, type quotas). 512 KB is the default complete-read budget per file; larger files transition to keyword search, sectioned reading, or structural sampling rather than being skipped.
- **Evidence standards**: all key conclusions must carry evidence level tags (Verified / Inferred / Conventional / Unknown). Inferred and Conventional must not be labeled as Verified. Conventional ecosystem commands must not be presented as project-specific commands without evidence.
- **Coverage reporting**: output must include Analysis Scope and Confidence and Gaps sections documenting what was scanned, what was skipped, and why.
- **Principles**: updated from 5 generic principles to 6 safety-evidenced principles.

### Principles
- Security patches do not depend on feature work. Trust boundary, secret protection, and boundary enforcement ship together.
- Scan budgets and role classification apply to all project types uniformly. Rule packs supplement, not override.
- Evidence tagging creates verifiability. Gaps are reported, not hidden.
- Mode system (inspect/generate/refresh/audit) is deferred to v2.0.0 when scan kernel and topology layer are stable.

---

## [1.2.1] - 2026-07-11 — Encoding & Detection Integrity Hotfix
**Source**: project-onboard comprehensive audit

### Fixed
- **UTF-8 encoding corruption**: 10 rule packs had corrupted byte sequences in arrow and dash characters (E2 86 3F and E2 80 3F), replaced with ASCII equivalents. Affected files: cpp.md, csharp.md, go.md, java.md, lua.md, nodejs.md, python.md, rust.md, unity.md, unreal.md. Total fixes: 244 corrupted sequences.
- **Duplicate section in unreal.md**: merged the duplicate `### 9. Identify Patterns` into a new `## AGENTS.md Additions for Unreal` section.
- **README file count**: corrected from "14 files" to "16 files".
- **README supported types**: added MonoGame row to the Supported Project Types table.
- **SKILL.md detection table** aligned with rule pack signatures:
  - Python: added `setup.cfg` and `environment.yml`
  - Java: added `build.gradle.kts`
  - C/C++: added `Makefile`
  - Lua: added `lua/` directory pattern
- **nodejs.md**: added `devDependencies` scanning instruction.

### Added
- `tests/validate_utf8.py` - UTF-8 validity checker for all Markdown files, with `--fix` mode
- `tests/validate_frontmatter.py` - YAML frontmatter syntax validator for SKILL.md
- `tests/fixtures/` and `tests/expected/` directories (scaffold for future test fixtures)

### Principles
- Detection result changes are permitted in hotfixes; execution model, flow architecture, and user interface remain unchanged
- UTF-8 and frontmatter validation are CI-ready scripts with zero external dependencies beyond Python stdlib

---

## [1.2.0] - 2026-07-08 — MonoGame Rule Pack
**Source**: project-ledger — dedicated game-framework support

### Added
- **MonoGame rule pack** (`references/monogame.md`): content-based sub-type
  refinement after a `csharp` match. Detected via `MonoGame.Framework.*`
  package reference or `**/*.mgcb` content file. Analyzes backend variant
  (DesktopGL/WindowsDX/Android/iOS), content pipeline, `Game` lifecycle
  (Initialize/LoadContent/Update/Draw), and 2D/3D rendering.

### Changed
- **Step 2 detection**: added a content-based refinement note + table — after
  matching `csharp`, read the `.csproj`; if it references MonoGame or a `.mgcb`
  exists, switch to the `monogame` rule pack.
- **Parameters**: `--type` now accepts `monogame`.

---

## [1.1.1] - 2026-07-01 — Language Auto-Detection
**Source**: project-ledger quality improvement

### Changed
- **Step 0**: Language auto-detection — skill now detects user message language as default output language. User can override. Falls back to English if unclear.

---

## [1.1.0] - 2026-06-29 — Community Contribution
**Source**: PR #1 by Lulugue (first community contribution)

### Added
- **C#/.NET rule pack** (`references/csharp.md`): detection via `.csproj`/`.sln`, ASP.NET Core/Blazor/WPF/MAUI/EF Core classification, NuGet dependency analysis, appsettings.json parsing.
- **Lua rule pack** (`references/lua.md`): detection via `.rockspec`/`lua_modules/`/`.luacheckrc`, LOVE2D/Neovim/OpenResty/WoW Addon/etc. classification, LuaRocks dependency analysis.

### Principles
- Community contributions welcome under GPL-3.0.
- New rule packs follow the same structure as existing ones.

---

## [1.0.1] - 2026-06-21 — Emergency Fix
**Source**: ThirdPersonTest project usage feedback

### Fixed
- YAML frontmatter parsing failure caused by Copyright and SPDX lines placed before `---` delimiters. Moved copyright notice to after the YAML block.
- `.git/` directory inside skill install path prevented opencode from discovering the skill. Removed `.git/` from `~/.config/opencode/skills/project-onboard/`.

### Added
- Dual-directory workflow: `~/OpenCode_skills/` (development, with Git) vs `~/.config/opencode/skills/` (install target, no `.git`).

### Principles
- No non-YAML content before the `---` frontmatter block in SKILL.md.
- Skill install directories must not contain `.git/`.
- Development happens in `OpenCode_skills/`; sync to `.config/opencode/skills/` excluding `.git`.

---

## [1.0.0] - 2026-06-19 — Initial Release
**Source**: openSkills project launch

### Added
- Core execution flow: confirm target -> detect project type (12 signature matches) -> load rule pack -> deep scan -> generate AGENTS.md.
- 9 complete rule packs: Unity, Unreal, Node.js, Python, Rust, Go, Java, C/C++, General.
- README with competitive advantages comparison table (9 dimensions vs Understand-Anything).
- GPL-3.0 license.
- Copyright by ZionXiaoxiSuOGLocGo.

### Principles
- Pluggable rule packs — adding a new type requires only one `.md` file, no core logic changes.
- AGENTS.md optimized for AI agent consumption (tables + bullet lists, 200-400 lines), not human documentation.
- Zero external dependencies — uses only opencode built-in tools (`glob`/`grep`/`read`).
- Auto-detection first, with optional `--type` override.
