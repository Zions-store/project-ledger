Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# game-design-doc-governance Changelog

## [Unreleased]

_P4 planned: NTFS junction wiring, origin-project switch to a thin wrapper (D4),
genre-specific doc modules._

---

## [0.3.0] - 2026-07-09 — P3 Full Governance

### Added
- **modules** 07_export_and_snapshot, 08_migration_workflow, 09_ai_collaboration_rules.
- **templates** DESIGN_DOCUMENT_TEMPLATE.md, AUTHORITY_MATRIX_TEMPLATE.md,
  CHANGE_CHECKLIST_TEMPLATE.md, AUDIT_HISTORY_TEMPLATE.md.
- **Issue-state tracking** in `tools/global_doc_audit.py`: reads/writes
  `issue_state.jsonl` with states OPEN / FIXED_PENDING_VERIFY / VERIFIED /
  FALSE_POSITIVE / ACCEPTED_EXCEPTION / REOPENED. Human-marked FALSE_POSITIVE /
  ACCEPTED_EXCEPTION issues are suppressed from the counts (surfaced as
  "suppressed"); `--no-state` opts out.

### Verified
- Parallel verification on the origin project (D4 P3, run 1): hard-coded script vs
  generic script + origin `Project_Profile.yaml` both yield `[0,0,0,1,0]` — EQUIVALENT.
- Regression vs baseline still EQUIVALENT.
- Suppression: marking the P3 as ACCEPTED_EXCEPTION drops P3 to 0 with suppressed=1.

### Note
- The origin project gains `Design Document/md file/Project_Profile.yaml` (D7). Its
  own audit script is unchanged (D4: switch to thin wrapper deferred to P4).

---

## [0.2.0] - 2026-07-09 — P2 Genre Library

### Added
- **modules/03_genre_profiles.md** — the two profile shapes (genre vs project
  instance) and a 10-genre matrix.
- **9 genre profiles** (`profiles/*.yaml`): open_world_rpg, linear_action_adventure,
  multiplayer_shooter, survival_crafting, roguelite, strategy_simulation,
  puzzle_adventure, horror_narrative, liveops_mobile — each with
  `recommended_docs` / `optional_docs` / `disabled_docs`, `high_risk_boundaries`,
  `audit_focus`, `suggested_doc_modules`.
- **16 doc_module skeletons** (`doc_modules/*.md.tmpl`): Narrative_Bible / Script /
  Pipeline, Character_Sheets, Mission_Design, World_Design, Level_Design,
  Encounter_Design, Gameplay_Systems, Resource_And_Economy, Progression_Design,
  Collectibles_Design, Multiplayer_Design, LiveOps_Design, UI_UX_Design,
  Technical_Design — each with applies / owns / does-not-own / recommended chapters /
  common boundaries / common audit rules.

### Changed
- `open_world_narrative_tactical_shooter.yaml`: added `recommended_docs` to match the
  genre-profile shape (`enabled_docs` retained for the auditor / regression fixture).

### Verified
- Regression against the origin project still EQUIVALENT (`P0=0 P1=0 P2=0 P3=1`).

---

## [0.1.0] - 2026-07-09 — P1 MVP

### Added
- **SKILL.md** entry point (English; Step 0 output-language selection; module index;
  new-project workflow; audit flow; safety rules).
- **tools/global_doc_audit.py** — generic, data-driven auditor:
  - Reads rules from `STYLE_GUIDE.md` (document list / anchor registry /
    deprecated-term registry) and `Project_Profile.yaml`
    (`enabled_docs` / `boundary_checks` / `consistency_checks` / `exceptions` /
    thresholds).
  - Generic checks retained in the engine (file list, tables, anchors + REF,
    deprecated terms, cross-document links).
  - Project-specific checks are **externalised** to the Profile (no hard-coded
    lore). `boundary_checks` support `forbid_regex` / `forbid_any`,
    `unless_near`, `stop_at`, and `match: first_per_term`;
    `consistency_checks` support `require_negation_near` /
    `require_all_context_near`.
  - English report `audit_report.md` + `audit_report.json`; appends
    `audit_history.md`; `--baseline` count comparison; CLI
    `--root/--out/--profile/--style/--strict/--fail-on-p2/--pedantic/`
    `--json-only/--md-only/--no-history`.
- **profiles/open_world_narrative_tactical_shooter.yaml** — first genre profile;
  also the regression fixture. Migrates the origin project's five hard-coded
  checks into data rules.
- **templates/PROJECT_PROFILE_TEMPLATE.yaml** and **templates/STYLE_GUIDE_TEMPLATE.md**.
- **modules/** 01 (document architecture), 02 (project profile),
  04 (authority & boundaries), 05 (anchors & change safety), 06 (audit workflow).
- **tests/expected/current_project_baseline.json** — regression baseline.

### Verified
- Regression against the origin project (`open_world_narrative_tactical_shooter`)
  reproduces `P0=0 P1=0 P2=0 P3=1 INFO=0`; `--baseline` reports EQUIVALENT.
- Does not modify the origin project's existing audit script (D4: P1/P2 leave it in place).
