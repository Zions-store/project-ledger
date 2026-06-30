# unreal-manual Changelog

## [2.2.0] - 2026-06-30 — Advanced Gameplay Patterns + Substrate + Tool Ecosystem
**Source**: ThirdPersonTest project-ledger development session

### Added
- **Advanced Gameplay Patterns** (new standalone chapter):
  - Compatible Skeleton retargeting workflow (IK Rig fallback for Mixamo in UE5.8)
  - C++ BlueprintPure expanded example for multi-state AnimBP access
  - Checkpoint/Respawn system: Controller-stored Transform, respawn position restoration, full state reset
  - Combo attack input cache pattern: CachedInputTime + AttackCooldown + Tolerance + AnimNotify chain
- **Animation → Compatible Skeleton Retargeting**: When IK Rig fails, use Manage Compatible Skeletons for lightweight runtime retargeting
- **Substrate Material System**: UE5.5+ next-gen material basics, BSDF graph, MakeSubstrateMaterialAttributes migration
- **Tool Ecosystem**: Understand-Anything knowledge graph integration, opencode MCP launch prerequisite (must start from project directory)
- Copyright notice + SPDX identifier added to SKILL.md
- Version metadata (2.3.0) added to SKILL.md frontmatter

### Changed
- Compatibility updated to include UE5.8

---

## [2.1.0] - 2026-06-25 — MCP + ABP + Project Knowledge Board
**Source**: ThirdPersonTest UE 5.8 project (crouch animation + MCP integration session)

### Added
- **MCP Integration** (new standalone chapter): Official vs community MCP comparison, deployment workflow (plugin copy → build → Python venv → opencode config), UE5.8 compatibility fixes (`ANY_PACKAGE`→`nullptr`, `BufferSize` shadow warning), MCP limitations (no AnimBP support, no asset deletion, static mesh assignment restrictions).
- **Animation → ABP Creation & Troubleshooting**: Proper AnimBP creation (Animation Blueprint from context menu, not generic `create_blueprint`), AnimGraph verification, copy-paste between ABPs, Event Graph variable update chain pattern, C++ `BlueprintPure` getter for AnimBP access.
- **Troubleshooting**: Live Coding active blocking builds; `ANY_PACKAGE` undeclared fix for UE5.5+; ABP variable name whitespace sensitivity diagnostics.
- **Project Knowledge Board**: New section at end of manual — per-project memory entries with key paths, class names, engine version, fix history. Enables session-to-session continuity without polluting global knowledge sections.

### Principles
- Global reusable knowledge → insert into matching core chapter (Animation, MCP, Troubleshooting).
- Project-specific memory → Project Knowledge Board with date + project name header.
- Variable names in ABP are whitespace-sensitive (`MovementComponent` ≠ `Movement Component`) — always verify exact spelling in source My Blueprint.
- ABP copy-paste across skeletons works only if both ABPs share the same target skeleton.

---

## [2.0.0] - 2026-06-24 — Major Update
**Source**: ThirdPersonTest UE 5.8 project hands-on summary

### Added
- **Lifecycle**: CDO Constructor asset loading (FObjectFinder failure under World Partition OFPA, 3 alternatives), hot-reload vs full-rebuild decision matrix, Blueprint CDO rebuild overwrite warnings.
- **Enhanced Input**: Multi-IMC simultaneous loading with BeginPlay fallback, ETriggerEvent full event table, interface calling conventions (UINTERFACE MinimalAPI+NotBlueprintable → no `Execute_` generation).
- **Animation**: AnimNotify architecture (UAnimNotify → Cast interface → drive game logic).
- **Character Movement**: Crouch settings (SetCrouchedHalfHeight replaces deprecated member), state bitfield packing, wall-jump pattern.
- **Collision**: SweepMultiByObjectType vs SweepMultiByChannel selection guide, Actor Tag system for AI target identification.
- **StateTree AI** (new standalone section): UE5 default NPC behavior system, StateTreeComponent + AAIController bridging, NavMesh debugging.
- **UMG**: WidgetComponent Screen vs World rendering space, RequestRedraw trigger conditions, GetWidgetFromName bypass for BP events.
- **Level Management**: World Partition OFPA activation detection (`__ExternalActors__/` + `__ExternalObjects__/`) and development implications.
- **Troubleshooting**: Output Log search quick-reference, benign PIE log identification, UE_LOG debugging template.

### Principles
- Additions inserted into matching sections, not appended at end.
- Keep original heading hierarchy and code style consistent with the base manual.
- No project-specific class names or paths.

---

## [1.0.0] - 2026-06-20 — Initial Release
**Source**: openSkills project launch (created via skill-creator)

### Added
- Unreal Engine core concepts: Actor/Pawn/Character, GameMode/GameState/PlayerController framework, Blueprint vs C++, rendering, physics, animation, UMG UI, Enhanced Input, network replication, UPROPERTY/UFUNCTION macros, GameInstance lifecycle, C++ vs Blueprint tradeoffs.
- 62.2KB SKILL.md.
