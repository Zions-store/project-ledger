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

**v0.3.1 — P3 Full Governance (release-consistency fixes).** Ships: the generic
data-driven auditor, 10 genre profiles, 16 doc-module skeletons, 9 modules,
6 templates, `issue_state.jsonl` state tracking, and a regression baseline
reproduced against the first real project (`P0=0 P1=0 P2=0 P3=1`).

STYLE parsing is **language-independent** via `<!-- AUDIT: … -->` marker blocks,
with a fallback to heading heuristics for existing files. `--strict` and the
profile `audit` thresholds gate pass/fail; the baseline compares P0–P3 (INFO is
informational only).

P4 (opencode junction wiring / origin-project switch to a thin wrapper) is pending.

## License

GPL-3.0-or-later. See `LICENSE`.
