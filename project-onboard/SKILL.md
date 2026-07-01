---
name: project-onboard
version: 1.1.1
description: Analyze any project directory and generate AGENTS.md for AI context. Supports any language via LLM-native translation. Use when the user asks to "onboard", "analyze this project", "分析这个项目", or provides a project path. Auto-detects Unity, Unreal, Node.js, Python, Rust, Go, Java, C/C++, C#, Lua, and general projects.
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Project Onboard

Turn any project directory into an AGENTS.md that gives the AI agent instant project context. Auto-detects project type and applies type-specific analysis rules. Zero external dependencies — uses only built-in tools.

## When This Skill Triggers

- "onboard this project"
- "analyze this project" / "analyze my project"
- "help me understand this project"
- "generate AGENTS.md for this project"
- "what does this project do?"
- "分析这个项目" / "プロジェクトを分析" / "프로젝트 분석" / "analyser ce projet"
- User provides a project path without context

## Parameters

- **path** (required): Project directory path
- **type** (optional): Force project type, skip auto-detection. Values: `unity`, `unreal`, `nodejs`, `python`, `rust`, `go`, `java`, `cpp`, `csharp`, `lua`, `general`. If an invalid value is given, warn the user and fall back to auto-detection.
- **output** (optional): Where to save AGENTS.md. Default: `<project_root>/AGENTS.md`

## Execution Flow

### Step 0: Choose Output Language

Detect the language of the user's message. If they wrote their request in a non-English language (e.g., "分析这个项目" in Chinese, "プロジェクトを分析" in Japanese), that is the implied preferred language. Use it as the default. Any language the LLM can output is supported — translation is done by the agent at generation time.

Ask the user to confirm, offering the detected language as default:

> "I noticed your message is in <detected-language>. Generate AGENTS.md in <detected-language>? Reply 'yes' or specify another language."

If the user's message language is unclear or mixed, default to English:

> "What language should AGENTS.md be written in? Default: English. Any language the LLM can output is supported."

### Step 1: Confirm the Target

If no path given, ask the user which project to analyze. If path is relative, resolve to absolute. Confirm with user before proceeding.

**Edge cases:**
- **Empty directory** (fewer than 10 files): Default to `general` type. Note in AGENTS.md that the project appears to be in very early stage.
- **Monorepo** (multiple build systems at top level, e.g. a `frontend/` directory with its own `package.json` plus a `backend/` with `go.mod`): Inform the user that multiple project types were detected and ask which sub-directory to target. Record in AGENTS.md that this is a monorepo with listed sub-projects.

### Step 2: Quick Scan for Project Type (if --type not specified)

Use `glob` with pattern `*` to list top-level directory entries. Match the results against the detection table below.

| Signature | Type | Rule Pack |
|---|---|---|
| `Assets/` + `ProjectSettings/` | unity | `references/unity.md` |
| `Source/` + `.uproject` | unreal | `references/unreal.md` |
| `package.json` without `Assets/` | nodejs | `references/nodejs.md` |
| `pyproject.toml` or `requirements.txt` or `setup.py` or `Pipfile` | python | `references/python.md` |
| `Cargo.toml` | rust | `references/rust.md` |
| `go.mod` | go | `references/go.md` |
| `pom.xml` or `build.gradle` | java | `references/java.md` |
| `CMakeLists.txt` | cpp | `references/cpp.md` |
| `*.csproj` or `*.sln` without `Assets/` | csharp | `references/csharp.md` |
| `*.rockspec` or `lua_modules/` or `.luacheckrc` or `.busted` | lua | `references/lua.md` |
| None of the above | general | `references/general.md` |

Check in order. First match wins. When multiple signatures could match (e.g., a project with both `package.json` and `CMakeLists.txt`), prefer the one that appears first in the table. If ambiguous or the detected type seems wrong after scanning, fall back to `general` or ask the user to specify `--type`.

> **Ordering note**: The detection order is deliberate. Unity appears before Node.js and C# because Unity projects also contain `package.json` and `*.csproj` files in their `ProjectSettings/` directory. Do not reorder without understanding these signature overlaps.

> **Sub-type detection**: Projects with `Dockerfile`, database files (`*.sql` + `migrations/`), or shader files (`.glsl`/`.hlsl`) are detected as `general` at Step 2. The `references/general.md` rule pack handles these during the deep scan.

### Step 3: Load the Rule Pack

Read `references/<type>.md` for type-specific scanning instructions. Each rule pack defines:
- Key files to read first
- Directory structure conventions
- Dependency file location
- Entry point location conventions
- Type-specific patterns to grep for

### Step 4: Deep Scan

Follow the rule pack's instructions to:
1. Read project metadata (name, version, description)
2. Read dependency manifest (which packages/frameworks are used)
3. Map directory structure (what each top-level folder contains)
4. Identify entry points (main file, startup scene, bootstrap script)
5. Find core modules/classes and their responsibilities
6. Detect architectural patterns (MVC, ECS, layered, etc.)

Use `grep` to find key patterns. Use `read` with 30-80 line limits per file to extract structure without bloating context. Use `glob` to verify directory contents.

### Step 5: Generate AGENTS.md

Write `<project_root>/AGENTS.md` with EXACTLY this structure. If the user chose a non-English language in Step 0, translate section headers, labels, and placeholder descriptions into that language. Keep structured data (paths, commands, dependency names, version numbers) in their original language:

```markdown
# [Project Name]

## Basic Information
- **Type**: [Unity/Node.js/Python/etc.]
- **Language**: [primary language]
- **Framework/Engine**: [specific version if known]
- **Key Dependencies**: [3-8 most important packages]

## Directory Structure
[3-10 top-level directories with one-line descriptions]

## Entry Points
- [How to run/start the project]
- [Startup scene/file and what it does]

## Core Architecture
[BULLET LIST of 3-10 key files/classes and their roles. NOT verbose prose.]

## Dependencies
[TABLE: package name | purpose]

## Build & Run
- How to build: [command]
- How to run: [command]
- How to test: [command]

## Notes
- [Anything unusual or non-standard]
- [Known pitfalls if user has recorded any]
```

### Step 6: Report

Tell the user what was detected and where AGENTS.md was saved. Offer to add any project-specific notes or pitfalls they want recorded.

## Principles

- **Concise**: AGENTS.md target is 200-400 lines. Not a novel — a reference card for the AI.
- **Accurate**: Don't guess. If unsure, state uncertainty rather than fabricate.
- **Structured**: Bullet points and tables over prose. AI parses structure faster.
- **Actionable**: Every line should help the AI make better decisions in future conversations.
- **Incremental later**: The user can update AGENTS.md by saying "update AGENTS.md with [new information]".

## Adding New Project Types

When the user encounters a project type this skill doesn't recognize, offer to create a new rule pack. Ask:
1. What is the project type called?
2. What file or folder signatures identify it?
3. Where are dependencies declared?
4. Where are entry points typically found?
5. Any special file formats the AI should understand?

Then write the rule pack to `references/<name>.md` following the existing format.

## 🚫 Anti-Pitfalls

- Do NOT run external tools (npm install, cargo build, etc.) — read-only analysis only
- Do NOT modify any project files except writing AGENTS.md
- Do NOT read more than 50 files total — focus on the most important ones
- If the project has 500+ files, rely more on directory structure and less on reading individual files
- Do NOT generate user-facing documentation — this is for the AI agent's context
- If `references/<type>.md` doesn't exist yet, use `references/general.md` and suggest creating a type-specific rule pack
