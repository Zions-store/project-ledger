Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

> [!WARNING]
> This branch is a public audit preview of project-onboard v2.0.0.
> It is not a stable release and should not be used in production.
> Current candidate version: v2.0.0-rc1.

# Project Onboard

Auto-detect project type and generate AGENTS.md for AI coding agents. Four execution modes: inspect (read-only), generate (create), refresh (update), audit (compare). Rule packs self-register via YAML frontmatter — adding a new type requires one file.

## What It Does

Give your AI agent a project path — it automatically:

1. Discovers project topology (single, monorepo, workspace, polyglot)
2. Scores all matching project types with evidence and confidence
3. Performs a security-bounded, budgeted deep scan by file role
4. Generates an evidence-tagged AGENTS.md with coverage reporting

### Execution Modes

| Mode | Writes Files | Use When |
|------|-------------|----------|
| **inspect** | No | "What does this project do?" — read-only analysis |
| **generate** | Yes | "Create AGENTS.md" — first-time generation |
| **refresh** | Yes (generated sections only) | "Update AGENTS.md" — preserve manual content |
| **audit** | No | "Is AGENTS.md still accurate?" — structured diff |

### Scan Depths

| Depth | Scope | Typical Output |
|-------|-------|---------------|
| **quick** | Manifest, entry points, key modules | 20-60 line summary |
| **standard** | Full topology, dependencies, architecture | Complete AGENTS.md (~150-300 lines) |
| **deep** | Sub-project graphs, asset/code relations | AGENTS.md + per-subproject summaries |

## Why Project Onboard

| | Understand-Anything | Project Onboard |
|---|---|---|
| Dependencies | Node.js + pnpm + knowledge graph | **None** |
| Customizable rules | Generic C# only | **Pluggable per-engine rules** |
| Output audience | Human onboarding guide | **AI agent context** |
| Speed | 5-15 min (full graph) | **1-3 min** |
| Engine awareness | Basic | **Unity .meta/prefab, UE .Build.cs, etc.** |
| Auto-detection + override | ❌ | **Auto-detect or `--type` force** |
| Composable | Standalone | **Can chain with Understand-Anything** |
| Cross-platform | Claude Code only | **opencode / Claude Code / Codex / Cursor** |
| Footprint | Repo + Node.js + pnpm | **19 files** |
| **Execution modes** | One-size-fits-all | **inspect / generate / refresh / audit** |
| **Rule registration** | N/A | **Self-registering (YAML frontmatter)** |

## Bundled Rule Packs

These rule packs ship with project-onboard. Additional types auto-discover from `references/*.md` YAML frontmatter — adding a new type requires only one file.

| Type | Signature |
|---|---|
| Unity | `Assets/` + `ProjectSettings/` |
| Unreal Engine | `*.uproject` (with or without `Source/`) |
| MonoGame | Via C# refinement: `MonoGame.Framework.*` in `.csproj` or `**/*.mgcb` |
| Node.js / Frontend | `package.json` (no `Assets/`) |
| Python | `pyproject.toml` / `requirements.txt` / `setup.py` / `Pipfile` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Java / Maven / Gradle | `pom.xml` / `build.gradle` / `build.gradle.kts` |
| C / C++ | `CMakeLists.txt` / `Makefile` |
| C# / .NET | `*.csproj` / `*.sln` (non-Unity) |
| Lua | `*.rockspec` / `lua_modules/` / `lua/` |
| General | Fallback for anything else |

## Installation

Copy to your skills directory:

```
~/.config/opencode/skills/project-onboard/SKILL.md
~/.config/opencode/skills/project-onboard/references/
~/.config/opencode/skills/project-onboard/templates/
```

Also compatible with `.claude/skills/` and `.agents/skills/`.
The `tests/` directory is for development validation only and is not required for runtime use.

## Usage

Just tell your AI agent:

```
onboard this project
analyze my project
help me understand this project
generate AGENTS.md for this project
what does this project do?
```

Or specify a path and optional type:

```
onboard C:\my-unity-project
onboard C:\my-project --type unity
```

Output:
- `inspect` / `audit` — results returned in conversation (no file written)
- `generate` / `refresh` — `<project_root>/AGENTS.md`

## Multi-Language Support

Project-onboard generates AGENTS.md in any language your LLM can output. The agent translates section headers and labels at generation time — keeping paths, commands, and dependency names intact.

Trigger phrases work in any language:

| Language | Trigger phrase examples |
|---|---|
| English | "onboard this project", "analyze this project" |
| 中文 | "分析这个项目", "生成项目文档" |
| 日本語 | "プロジェクトを分析", "AGENTS.mdを生成" |
| 한국어 | "프로젝트 분석", "AGENTS.md 생성" |
| Français | "analyser ce projet", "générer AGENTS.md" |
| Deutsch | "Projekt analysieren", "AGENTS.md erstellen" |
| Español | "analizar proyecto", "generar AGENTS.md" |
| Русский | "анализировать проект", "создать AGENTS.md" |
| Português | "analisar projeto", "gerar AGENTS.md" |
| Italiano | "analizza progetto", "genera AGENTS.md" |
| العربية | "تحليل المشروع", "إنشاء AGENTS.md" |

...and any other language the LLM can produce.

## Adding New Project Types

1. Copy `references/_rule-pack-template.md` to `references/<name>.md`
2. Fill in the YAML frontmatter (signatures, workspace files, known blind spots)
3. Write the type-specific analysis rules following the template body

The rule pack auto-discovers on next run. No modifications to SKILL.md or README are needed. The bundled type table above is documentation only; runtime type registration is derived from rule-pack frontmatter at scan time.

## License

GPL-3.0 — see [LICENSE](LICENSE)
