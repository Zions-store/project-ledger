Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Project Onboard

Auto-detect project type and generate AGENTS.md for AI coding agents. Zero dependencies.

## What It Does

Give your AI agent a project path — it automatically:

1. Scans directory structure to detect the project type
2. Loads the matching rule pack
3. Generates a concise AGENTS.md with architecture, dependencies, entry points, and core modules

Your agent instantly understands the project without you explaining anything.

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
| Footprint | Repo + Node.js + pnpm | **14 files, ~44KB** |

## Supported Project Types

| Type | Signature |
|---|---|
| Unity | `Assets/` + `ProjectSettings/` |
| Unreal Engine | `Source/` + `.uproject` |
| Node.js / Frontend | `package.json` (no `Assets/`) |
| Python | `pyproject.toml` / `requirements.txt` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Java / Maven / Gradle | `pom.xml` / `build.gradle` |
| C / C++ | `CMakeLists.txt` |
| C# / .NET | `*.csproj` / `*.sln` (non-Unity) |
| Lua | `*.rockspec` / `lua_modules/` |
| General | Fallback for anything else |

## Installation

Copy to your skills directory:

```
~/.config/opencode/skills/project-onboard/SKILL.md
~/.config/opencode/skills/project-onboard/references/*.md
```

Also compatible with `.claude/skills/` and `.agents/skills/`.

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

Output: `<project_root>/AGENTS.md`

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

1. Add a detection signature in `SKILL.md` Step 2
2. Create `references/<name>.md` following the existing format
3. The rule pack auto-loads on next `onboard` run

## License

GPL-3.0 — see [LICENSE](LICENSE)
