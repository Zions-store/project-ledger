---
schema_version: 1
id: general
display_name: General (Fallback)
priority: 0
aliases: [fallback, unknown]
kind: fallback

signatures:
  any: []

exclusions:
  any: []

refinements: []

workspace_files: []

priority_files:
  - README.md
  - Makefile
  - Dockerfile
  - docker-compose.yml

entry_point_patterns:
  - "main"
  - "index.html"

external_reference_mechanisms: []

large_structured_files: []

binary_asset_types: []

default_ignore_paths: []

generated_paths: []

known_blind_spots:
  - unrecognized build systems
  - proprietary tools

optional_output_sections:
  - Sub-Type Hints
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# General Project Analysis Rules (Fallback)

Used when no specific project type is detected.

## Scan Steps

### 1. Map Top-Level Structure
```bash
glob * (or read the root directory)
```
Identify what each top-level file/directory suggests about the project.

### 2. Find Build/Language Clues
Look for these files in order:
| File | Implies |
|---|---|
| `package.json` | Node.js/JavaScript |
| `tsconfig.json` | TypeScript |
| `requirements.txt` or `pyproject.toml` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `pom.xml` or `build.gradle` | Java |
| `CMakeLists.txt` | C/C++ |
| `Makefile` | C or general build |
| `Dockerfile` | Containerized |
| `.sql` files or `migrations/` | Database-focused |
| `.glsl` or `.hlsl` files | Shader/graphics |
| `.csproj` or `.sln` | .NET/C# (non-Unity) |
| `index.html` | Static web |

### 3. Find Entry Points
```bash
grep "main" in top-level files (package.json, Makefile, etc.)
```
```bash
glob **/main.* or glob **/index.* or glob **/app.* or glob **/server.*
```

### 4. Read Key Files
Read these in priority order (30-80 lines each, within scan budget):
1. README or README.md
2. The main entry file found in step 3
3. Package/dependency manifest
4. Top-level config file (config.js, settings.py, Makefile) — never read .env or secret files
5. Directory with most files (likely the main source)

### 5. Categorize
Based on what was found, classify the project type:
- Web app (frontend + backend)
- CLI tool
- Library/SDK
- Database/SQL project
- Graphics/Shader project
- Game (unknown engine)
- Other (describe briefly)

### 6. Sub-Type Specific Hints

**Docker projects** (`Dockerfile` + `docker-compose.yml` detected at step 2):
- Read `Dockerfile` to identify base image, exposed ports, multi-stage builds
- Read `docker-compose.yml` to identify services, volumes, networks
- Entry points: `CMD` / `ENTRYPOINT` directives

**Database projects** (`*.sql` + `migrations/` detected at step 2):
- Identify DB engine from file extensions (`.sql`, `.psql`, `.mysql`)
- Check for ORM migration frameworks (Prisma, Alembic, Flyway, etc.)
- Entry points: schema files, seed scripts, main migration file

**Shader projects** (`.glsl`/`.hlsl` detected at step 2):
- Identify shader types: vertex, fragment/pixel, compute, geometry
- Check for shader toolchain (ShaderLab, Unity Shader Graph, custom pipeline)
- Entry points: main shader file or include chain

## AGENTS.md Output
Follow the standard template. In "Notes", flag anything unusual and suggest the user create a type-specific rule pack if they work with this project type frequently.
