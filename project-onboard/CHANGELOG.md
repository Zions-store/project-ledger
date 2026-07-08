Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# project-onboard Changelog

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
