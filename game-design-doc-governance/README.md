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
├── SKILL.md                 # entry point (progressive disclosure)
├── README.md  CHANGELOG.md  LICENSE
├── modules/                 # detailed guidance (01–09)
├── templates/               # PROJECT_PROFILE / STYLE_GUIDE / … skeletons
├── doc_modules/             # per-document "applies / owns / not-owns" skeletons
├── profiles/                # genre profiles (.yaml)
├── tools/global_doc_audit.py# generic, data-driven auditor
└── tests/                   # regression fixtures + baseline
```

## Design in two layers (language)

- **Skill payload** (this repo): English — meant for public release.
- **Generated product** (a project's docs): any language the user picks at run
  time (default English). The agent translates but keeps `{{PLACEHOLDER}}` and
  YAML keys intact.

## The audit

`tools/global_doc_audit.py` reads two rule sources and runs generic + data-driven
checks:

- `STYLE_GUIDE.md` → document list, anchor registry, deprecated-term registry.
- `Project_Profile.yaml` → enabled docs, `boundary_checks`, `consistency_checks`,
  `exceptions`, thresholds.

```
python tools/global_doc_audit.py --root <md dir> --out <audit dir> \
    --profile <Project_Profile.yaml> --style <STYLE_GUIDE.md> [--baseline <json>]
```

Requires Python 3 and `PyYAML`.

## Status

**v0.1.0 (P1 MVP).** Ships: the generic auditor, the
`open_world_narrative_tactical_shooter` profile, PROJECT_PROFILE / STYLE_GUIDE
templates, core modules (01/02/04/05/06), and a regression baseline reproduced
against the first real project (`P0=0 P1=0 P2=0 P3=1`). Later phases add the
remaining genre profiles, doc-module skeletons, export/migration/AI modules, and
`issue_state.jsonl`.

## License

GPL-3.0-or-later. See `LICENSE`.
