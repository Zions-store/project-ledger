Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# game-design-doc-governance Changelog

## [Unreleased]

_P2+ planned: remaining 9 genre profiles, 16 doc_module skeletons, genre matrix
(module 03), export/migration/AI modules (07/08/09), full issue_state.jsonl._

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
