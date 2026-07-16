---
schema_version: 1
id: unreal
display_name: Unreal Engine
priority: 95
kind: normal
aliases: [ue, ue5]

signatures:
  any:
    - "*.uproject"

exclusions:
  any: []

refinements: []

workspace_files: []

priority_files:
  - "*.uproject"
  - "*.Build.cs"
  - Config/DefaultEngine.ini

entry_point_patterns:
  - "class.*GameMode"
  - "class.*GameState"
  - "class.*PlayerController"
  - "class.*Pawn"
  - "class.*Character"

external_reference_mechanisms:
  - plugin reference paths
  - module dependencies

generated_paths:
  - Binaries/
  - Intermediate/
  - DerivedDataCache/

large_structured_files: []

binary_asset_types:
  - "*.uasset"
  - "*.umap"

default_ignore_paths:
  - Binaries/
  - Intermediate/
  - DerivedDataCache/

known_blind_spots:
  - Blueprint-only gameplay logic
  - binary asset inspection

optional_output_sections:
  - Unreal Modules and Plugins
  - Blueprint vs C++ Distribution
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Unreal Engine Project Analysis Rules

## Signature Detection
- `*.uproject` file in root (with or without `Source/`)
- If `Source/` and `.Build.cs` are also present -> C++ Unreal project (full code analysis)
- If only `.uproject` present without `Source/` -> Blueprint-only Unreal (binary assets not inspectable as text, noted in blind spots)

## Scan Steps

### 1. Read Project Metadata
Read the `.uproject` file (JSON format). Extract:
- `EngineAssociation` -Engine version (e.g. "5.4")
- `Modules[]` -Project modules (names, types: Runtime/Editor)
- `Plugins[]` -Enabled plugins

### 2. Read Module Dependencies
For each module directory under `Source/`, read the `.Build.cs` file:
- `PublicDependencyModuleNames` -Public API dependencies
- `PrivateDependencyModuleNames` -Internal dependencies
Key modules to identify:
- `Core`, `CoreUObject` -Always present
- `Engine`, `UMG` -Gameplay and UI
- `EnhancedInput` -New input system
- `GameplayAbilities` -GAS (Gameplay Ability System)
- `OnlineSubsystem` -Multiplayer
- `Niagara` -VFX
- `Chaos` -Physics
- `Landscape`, `Foliage` -Terrain

### 3. Map Directory Structure
| Directory | Common Role |
|---|---|
| `Source/<ModuleName>/Public/` | Header files (.h) |
| `Source/<ModuleName>/Private/` | Implementation files (.cpp) |
| `Content/` | Assets (Blueprints, Materials, Maps) |
| `Config/` | Engine and game configuration (.ini) |
| `Plugins/` | Additional plugins |
| `Binaries/` | Compiled binaries |
| `Intermediate/` | Build artifacts (ignore) |
| `DerivedDataCache/` | Cached assets (ignore) |

### 4. Find Core Classes
```bash
grep "class.*GameMode\|class.*GameState\|class.*PlayerController\|class.*Pawn\|class.*Character" in Source/
```
Common framework classes:
- `GameMode` -Match rules, spawning, game flow
- `GameState` -Replicated state visible to all players
- `PlayerController` -Player input and camera
- `PlayerState` -Per-player replicated state
- `Pawn` / `Character` -Physical avatar in the world
- `HUD` -On-screen display
- `GameInstance` -Persistent across levels

### 5. Find Entry Points
- Default map: Check `Config/DefaultEngine.ini` for `GameDefaultMap`
- Default GameMode: Check `Config/DefaultEngine.ini` for `GlobalDefaultGameMode`
- Level files: `glob **/*.umap` in `Content/` (binary, can't read directly)

### 6. Check Config Files
- `Config/DefaultEngine.ini` -Engine settings, renderer, input
- `Config/DefaultGame.ini` -Game-specific settings
- `Config/DefaultInput.ini` -Input bindings (if not using EnhancedInput)

### 7. Identify Patterns
- Is GAS (Gameplay Ability System) in use? ->`GameplayAbilities` module
- Is Enhanced Input in use? ->`EnhancedInput` module + `InputAction` assets
- Is Networking in use? ->Check `bReplicates` patterns + OnlineSubsystem
- Blueprint-heavy or C++-heavy? ->Compare `Content/` vs `Source/` file counts

### 8. Build & Run Commands
- **Generate project files**: Right-click `.uproject` ->Generate Visual Studio project files
- **Build**: Open `.sln` in Visual Studio ->Build, or `UnrealBuildTool` from command line
- **Run in Editor**: Double-click `.uproject` or launch from Epic Games Launcher
- **Hot Reload**: Ctrl+Alt+F11 in editor (`.cpp` function body changes only; full rebuild for header changes)
- **Cook/Package**: File ->Package Project in the editor

## AGENTS.md Additions for Unreal

Include:
- Engine version from `.uproject`
- Modules list with brief purpose
- Key framework classes (GameMode, PlayerController, etc.)
- If UMG is present, note that UI is likely Blueprint-driven
- Note: `.uasset`/`.umap` files are binary -only C++ and config files are readable
