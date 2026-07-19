Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# project-docs Changelog

## [Unreleased]

_No unreleased changes yet._

---

## [1.2.0] - 2026-07-19 — Safety and Compatibility Hardening

### Added
- Security foundation for untrusted repository content, sensitive-data exclusion, root boundaries, diff-first writes, and atomic replacement.
- UTF-8 validator and dedicated project-docs validation workflow.
- project-docs ownership markers for safe AGENTS.md linking.

### Changed
- Template selection now reads project-onboard v2 `Technology Stack` first and supports v1 `Basic Information` as a fallback.
- Existing documents are treated as user-owned until an approved update; project-onboard generated blocks are never edited.
- Configuration templates record key names, descriptions, and source paths instead of values.
- Restored damaged UTF-8 characters in documentation and templates.

---

## [1.1.0] - 2026-07-08 — MonoGame Template

### Added
- **MonoGame PROJECT_STATE template** (`templates/monogame/PROJECT_STATE.md.tmpl`):
  engine-oriented sections — MonoGame version/backend, Game lifecycle spectrum,
  content pipeline (Content.mgcb) checklist, input map, and game-loop flow.
  Auto-discovered when AGENTS.md Type is `monogame` (no code changes).

### Changed
- Template selection docs + example tree updated to list the `monogame` template.

---

## [1.0.0] - 2026-06-29 — Initial Release

### Added
- Core workflow: initialize three-document system (AGENTS.md + PROJECT_STATE.md + DEVLOG.md)
- Update workflow for existing documents
- Consistency check across all three documents
- Multi-language support (English, 中文, 日本語 한국어, Français)
- Full §1-§10 PROJECT_STATE.md template
- DEVLOG.md first-entry template
- `maintenance-spec.md` with detailed update triggers and content boundaries
