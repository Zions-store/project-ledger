Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# Project Ledger Development Log

> Append chronologically. Latest on top.

---

## 2026-07-19

### project-docs v1.3.0 — Output validation, regression coverage, safety hardening

- **What was done**:
  - Full audit of project-docs at master (f747df1): identified 4 P0 (encoding corruption, missing trust boundary, no write protection, v2 interface drift) and multiple P1 issues.
  - Phase 1: Fixed UTF-8 corruption in 5 files (CHANGELOG.md, maintenance-spec.md, 3 templates) — E2 80 3F → E2 80 94 (em-dash), U+FFFD restoration for Japanese/Korean.
  - Phase 2: Added Security Foundation to SKILL.md (repository trust boundary, secret exclusion, key-names-only config, atomic writes).
  - Phase 3: Added write protection (managed markers `<!-- project-docs:managed:start/end -->`, diff-first writes, confirmation before modifying user-owned documents, v2 manual region awareness).
  - Phase 4: Aligned with project-onboard v2 interface (Technology Stack → Basic Information fallback, Development Workflows → Build & Run fallback, Type path validation).
  - Added `tests/validate_output.py` (UTF-8, secrets, placeholders, marker order), `tests/validate_utf8.py`, `tests/validate_contract.py`, 7 host regression cases.
  - Created dedicated CI workflow (`project-docs-validate.yml`).
  - Version: 1.1.0 → 1.2.0 (safety) → 1.3.0 (validation + regression).

- **Why this approach**:
  - Encoding fixes followed same pattern as project-onboard v1.2.1 (E2-xx-3F corruption, same root cause).
  - Security hardening mirrored project-onboard v1.3.0's _common.md patterns — trust boundary, secret exclusion, key-names-only.
  - Write protection used project-onboard v2.0.0's marker system as precedent — managed:start/end markers ensure user content preservation.
  - v2 interface alignment was necessary because project-onboard v2.0.0 renamed output sections (Basic Information → Technology Stack, Build & Run → Development Workflows).

- **What was learned / verified**:
  - Same UTF-8 corruption pattern across both skills confirms systematic encoding issue in the development toolchain.
  - Single-file rule pack registration (project-onboard) and single-file template registration (project-docs) share the same auto-discovery philosophy.
  - Cross-skill field mapping contracts must be validated when either skill changes output structure.

### project-onboard v2.0.0 — Full release with behavior regression

- **What was done**:
  - Completed v1.2.1 (UTF-8 hotfix) → v1.3.0 (security foundation + scan kernel) → v1.4.0 (topology + workspace) → v2.0.0 (execution modes + plugin architecture) in four sequential releases.
  - v2.0.0-rc1 underwent three rounds of static audit with iterative fixes (refinement discovery, POSIX ERE, validator hardening, template alignment).
  - 48-case behavior regression suite executed on OpenCode 1.17.18: P0-A security (6), P0-B write protection (2), P0-C four modes (8), P1-A type detection (12), P1-B topology (9), P2 edge cases (6).
  - Result: 48/48 PASS, 0 FAIL, 0 BLOCKED (46 physical executions, 2 shared evidence pairs).
  - 4 smoke tests on finalize/v2.0.0 branch: inspect, generate, refresh, secret safety — all PASS.
  - Branch protection configured (5 required checks on master), annotated tag v2.0.0 created, GitHub Release published.

- **Why this approach**:
  - Sequential version delivery allowed security patches (v1.3.0) to ship before feature work (v1.4.0, v2.0.0).
  - Three-session release model (evidence alignment → version conversion → smoke/merge/tag) prevented mixed responsibilities.
  - Behavior regression used full fixture isolation (tests/work/<case-id>/) to prevent cross-contamination.
  - Annotated tag + merge commit preservation ensures full audit trail.

- **What was learned / verified**:
  - Windows junction behavior for external symlink tests differs from Linux symlinks — dual evidence strategy (Windows OpenCode behavior + Linux CI fixture contract) is necessary.
  - `gh` CLI unauthenticated on Windows — web UI fallback for PRs/releases is reliable but slower.
  - Branch protection ruleset names must exactly match workflow job names (static-validation (3.11)/(3.12), fixture-contract).
  - Release candidate iteration with public audit produces higher confidence than single-shot release.

### project-ledger self-onboarding — Dogfooding the skills

- **What was done**:
  - Used project-onboard v2.0.0 to analyze the project-ledger monorepo itself and generate AGENTS.md.
  - Used project-docs v1.3.0 to initialize PROJECT_STATE.md with current status.
  - Updated DEVLOG.md with v1.3.0→v2.0.0 development history.
  - Updated root README and org profile README with current versions and descriptions.

- **Why this approach**:
  - The monorepo had DEVLOG.md but no AGENTS.md or PROJECT_STATE.md — missing the foundational documents its own skills generate.
  - Self-onboarding validates the skills work on their own development environment.
  - Enables future sessions to quickly recover context by reading AGENTS.md + PROJECT_STATE.md + DEVLOG.md.

---

## 2026-07-08

### project-onboard v1.2.0 + project-docs v1.1.0 — MonoGame support

- **What was done**:
  - Added `references/monogame.md` rule pack (project-onboard): content-based
    sub-type refinement after `csharp` match, detected via `MonoGame.Framework.*`
    package or `**/*.mgcb`. Analyzes backend variant, content pipeline, `Game`
    lifecycle, 2D/3D rendering.
  - SKILL.md Step 2: added content-based refinement note + table; `--type` now
    accepts `monogame`.
  - Added `templates/monogame/PROJECT_STATE.md.tmpl` (project-docs): engine-oriented
    sections (version/backend, Game lifecycle, Content.mgcb checklist, input map,
    game-loop flow). Auto-discovered by AGENTS.md Type `monogame`.
  - Bumped versions (onboard 1.1.1→1.2.0, docs 1.0.0→1.1.0), updated both
    CHANGELOGs and root README (11→12 rule packs).

- **Why this approach**:
  - MonoGame is a game framework whose analysis needs differ sharply from the
    ASP.NET/WPF/MAUI focus of the generic `csharp` rule pack.
  - Detection is content-based (not a top-level name signature) because MonoGame's
    signals live inside `.csproj` / `Content/` — so it refines `csharp` rather than
    being a standalone Step 2 signature.

- **What was learned / verified**:
  - C# regression: a plain `Microsoft.NET.Sdk.Web` project without MonoGame stays
    `csharp` (no false positive); a project with `MonoGame.Framework.DesktopGL` or
    a `.mgcb` file routes to `monogame`. Verified with fixtures + the real
    `Mono 2D Test` project.

---

## 2026-07-01

### project-onboard v1.1.1 — Language auto-detection

- **What was done**:
  - Step 0: Added language auto-detection from the user's input message. If the user writes in Chinese (e.g., "分析这个项目"), the skill auto-selects Chinese as the output language. User can override. Falls back to English if unclear.
  - Updated CHANGELOG, version metadata (v1.1.0 → v1.1.1), and README references.

- **Why this approach**:
  - Reduces friction — users no longer need to explicitly state their language preference.
  - The LLM detects the input language naturally; we just need to act on it.

## 2026-06-30

### 47/47 audit bugs resolved �?manuals v2.2.1 / v2.1.1

- **What was done**:
  - Two-round comprehensive audit of unreal-manual (15 issues) and unity-manual (32 issues) �?all resolved.
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

### Manuals integrated �?unreal-manual (v2.2.0), unity-manual (v2.1.0)

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

### Comprehensive two-round audit �?28 issues found, all resolved

- **What was done**:
  - Round 1 (format): 12 issues �?copyright notices, template placeholders, CHANGELOG formatting (9 fixed, 3 deferred).
  - Round 2 (content): 28 issues �?type-specific templates, AGENTS-to-STATE field mapping, complete update workflow, Build & Test sections in 6 rule packs, edge cases, version metadata.
  - All 28 issues resolved.

### Project ledger repository established

- **What was done**:
  - Created GitHub organization `Zions-store`.
  - Set up `project-ledger` monorepo with project-onboard + project-docs skills.
  - Deprecated old standalone `ZionXiaoxiSuOGLocGo/project-onboard` (4 stars preserved), added [DEPRECATED] redirect.
  - Established Junction-based local dev workflow: `projects\Zion's Store\project-ledger\` �?`.config\opencode\skills\`.
  - Cleaned up legacy `OpenCode_skills\` directory.

---

<!-- Append new entries above this line. -->
