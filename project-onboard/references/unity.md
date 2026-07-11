---
schema_version: 1
id: unity
display_name: Unity
priority: 100
kind: normal
aliases: [unity3d]

signatures:
  all:
    - Assets/
    - ProjectSettings/

exclusions:
  any: []

refinements: []

workspace_files: []

priority_files:
  - Packages/manifest.json
  - ProjectSettings/ProjectVersion.txt
  - ProjectSettings/EditorBuildSettings.asset

entry_point_patterns:
  - "class.*Manager"
  - "class.*Controller"
  - "class.*GameManager"

external_reference_mechanisms:
  - local UPM package
  - file:../shared-package

generated_paths:
  - Library/
  - Temp/
  - Obj/
  - Logs/

large_structured_files:
  - "*.unity"
  - "*.prefab"
  - "*.asset"
  - "*.meta"

binary_asset_types:
  - "*.fbx"
  - "*.png"
  - "*.wav"
  - "*.dll"

default_ignore_paths:
  - Library/
  - Temp/
  - Obj/
  - Logs/

known_blind_spots:
  - script-to-prefab references (YAML GUIDs)
  - asset bundle dependencies

optional_output_sections:
  - Unity Project Structure
  - Render Pipeline
  - Input System
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Unity Project Analysis Rules

## Signature Detection
- `Assets/` directory exists
- `ProjectSettings/` directory exists
- `.unity` files (scene files) present
- `Packages/manifest.json` present

## Scan Steps

### 1. Read Package Dependencies
```bash
read Packages/manifest.json
```
Extract key packages and their purposes:
- `com.unity.render-pipelines.universal` ->URP
- `com.unity.render-pipelines.high-definition` ->HDRP
- `com.unity.inputsystem` ->New Input System
- `com.unity.cinemachine` ->Camera system
- `com.unity.textmeshpro` ->Text rendering
- `com.unity.timeline` ->Cutscene system
- `com.unity.netcode.gameobjects` ->Netcode for GameObjects
- Other `com.unity.*` packages ->Unity official
- Non-`com.unity` packages ->Third-party

### 2. Map Directory Structure
Use `glob` to list `Assets/` subdirectories. Common patterns:
- `Assets/Scripts/` ->Game logic (scan for `*Manager.cs`, `*Controller.cs`, `*Singleton.cs`)
- `Assets/Scenes/` ->Scene files (identify `*MainMenu*.unity`, `*Start*.unity`)
- `Assets/Prefabs/` ->Reusable GameObjects
- `Assets/Art/` or `Assets/Sprites/` ->Visual assets
- `Assets/Audio/` ->Sound files
- `Assets/Animations/` ->Animation clips/controllers
- `Assets/Resources/` ->Runtime-loadable assets
- `Assets/Settings/` ->URP/HDRP pipeline assets
- `Assets/Plugins/` ->Native libraries

### 3. Find Entry Scenes
```bash
glob **/Scenes/*.unity   or   glob **/*.unity
```
Read Build Settings to find scene build order:
```bash
grep "scenes" in ProjectSettings/EditorBuildSettings.asset
```

### 4. Find Core Scripts
```bash
grep "class.*Manager\|class.*Controller\|class.*GameManager\|class.*Singleton" in Assets/Scripts/
```
Read top 50 lines of each core script to extract class name and purpose.

### 5. Identify Patterns
- ECS (Entity Component System)? ->Look for `SystemGroup`, `ISystem`
- MVC? ->Look for `View`, `Controller`, `Model` naming
- Singleton managers? ->Very common in Unity projects
- Event-driven? ->Look for `UnityEvent`, `Action`, `delegate`
- Dependency injection? ->Look for `[Inject]` attribute, Zenject/VContainer

### 6. Check Special Files
- `.meta` files: GUID references, ignore for analysis (just note they exist)
- `.asset` files: ScriptableObject data
- `.prefab` files: YAML format, note but don't deep-read (can be very large)
- `.unity` files: Scene data, YAML format, note entry scenes only

### 7. Build & Run Commands
- **Run in Editor**: Open the project in Unity Hub ->Select version ->Open
- **Build**: File ->Build Settings ->select platform ->Build
- **Test**: Unity Test Framework (Window ->General ->Test Runner)
- **Package Manager**: Packages managed via `Packages/manifest.json` (auto-resolved by Unity)

## AGENTS.md Additions for Unity
Include:
- Render pipeline in use (Built-in/URP/HDRP)
- Input system in use (Old/New)
- Whether Netcode is present
- Scene loading order
- Singleton pattern warnings: "If you see DontDestroyOnLoad + singleton, this is the global state manager"
