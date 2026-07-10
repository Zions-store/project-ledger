Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# game-design-doc-governance

A reusable **game design documentation governance** Skill: build and maintain a
multi-document GDD system with single-source authority, cross-document boundaries,
change-safety anchors, and a data-driven Python audit.

One generic framework + a per-genre **Profile** + a data-driven **audit**. Games
enable different documents but obey the same governance principles.

## Layout

```
game-design-doc-governance/
--------- SKILL.md                 # entry point (progressive disclosure)
--------- README.md  CHANGELOG.md  LICENSE
--------- modules/                 # detailed guidance (01--?9)
--------- templates/               # PROJECT_PROFILE / STYLE_GUIDE / --?skeletons
--------- doc_modules/             # per-document "applies / owns / not-owns" skeletons
--------- profiles/                # genre profiles (.yaml)
--------- tools/global_doc_audit.py# generic, data-driven auditor
--------- tests/                   # regression fixtures + baseline
```

## Design in two layers (language)

- **Skill payload** (this repo): English --?meant for public release.
- **Generated product** (a project's docs): any language the user picks at run
  time (default English). The agent translates but keeps `{{PLACEHOLDER}}` and
  YAML keys intact.

## The audit

`tools/global_doc_audit.py` reads two rule sources and runs generic + data-driven
checks:

- `STYLE_GUIDE.md` --?document list, anchor registry, deprecated-term registry.
- `Project_Profile.yaml` --?enabled docs, `boundary_checks`, `consistency_checks`,
  `exceptions`, thresholds.

```
python tools/global_doc_audit.py --root <md dir> --out <audit dir> \
    --profile <Project_Profile.yaml> --style <STYLE_GUIDE.md> [--baseline <json>]
```

Requires Python 3 and `PyYAML`.

## Status

**v0.7.1 --?first public pre-1.0 release (NOT stable).** Ships: the generic
data-driven auditor, 10 genre profiles, 16 doc-module skeletons, 9 modules,
6 templates, `issue_state.jsonl` state tracking, a self-contained regression
fixture, and P4 opencode wiring (junction + thin-wrapper).

> **Pre-1.0:** the Profile schema, CLI, and scaffold workflow are **not yet frozen**;
> breaking changes may still occur before 1.0.0. Roadmap: 0.5.0 fixtures+pytest --?> 0.6.0 schema validation --?0.7.0 packaging/CLI --?0.8.0 scaffold --?0.9.0 RC --?1.0.0.

STYLE parsing is **language-independent** via `<!-- AUDIT: --?-->` marker blocks,
with a fallback to heading heuristics for existing files. `--strict` and the
profile `audit` thresholds gate pass/fail; the baseline compares P0---P3 (INFO is
informational only).

Primary regression is the self-contained fixture `tests/fixtures/sample_open_world/`
(no external project dependency). Published release tag:
`game-design-doc-governance-v0.7.1`; local P4 milestone tag `v0.4.0-local-p4`.

## License

GPL-3.0-or-later. See `LICENSE`.
