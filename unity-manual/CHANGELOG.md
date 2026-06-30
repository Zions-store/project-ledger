# unity-manual Changelog

## [2.1.1] - 2026-06-30 — Audit Bug Fixes
**Source**: project-ledger quality audit

### Fixed
- H1: Fix `ObjectPool.Get()` empty queue `Dequeue()` crash
- H2: Remove conflicting `Rigidbody` from Player teaching example
- H3: Replace outdated namespace limitation with "lifted in 2022.2" note
- H4: Fix fictitious `EditorSettings.ini` to real menu instructions
- H5: Add missing `health` field declarations (x2 locations)
- H6: Fix `Unity 2023+` → `Unity 2022.2+ / Unity 6`
- H7: Add `Renderer` declaration to `FadeOut` coroutine
- M2: Cache `WaitForSeconds` in coroutine example
- M4: Fix undefined `impulse` variable
- M5: Fix async/await error-on-destroy table
- M8: Fix dead cross-reference to unreal-manual
- M9: Fix `collisionDetectionMode` property name
- M11: Add Addressables note to Resources.LoadAll example
- M13: Fix Fixed Timestep advice
- M1: Replace duplicate SO Event Channel with cross-reference
- L2: Fix lowercase "unity" → "Unity"
- L4: Add SafeArea/notch handling note
- L5: Update README line count

### Added
- Profiling & Debugging section (Profiler, Frame Debugger, common commands)
- `Animator.Play()` and `StringToHash()` examples
- `[ContextMenu]` attribute quick reference
- `async void` lifecycle warning in UniTask example

---

## [2.1.0] - 2026-06-30 — Anti-Patterns + Game Architecture + Retargeting + Mobile
**Source**: project-ledger audit session

### Added
- **Copyright + Version**: Copyright notice + SPDX identifier, version 2.1.0 metadata in frontmatter
- **Animation → Retargeting (Humanoid Avatar)**: Avatar setup/configuration workflow, muscle space masks, cross-model animation sharing, common issues
- **Common Anti-Patterns** (new chapter): Physics transform-position misuse, Unity API misuse (FindObjectOfType in Update, GetComponent caching, LINQ in hot paths), event subscription leaks, GC allocation hotspots table with fixes
- **Game Architecture Patterns** (new chapter): Finite State Machine (enum-based), Strategy Pattern via interface, Observer via ScriptableObject Event Channel (decoupled sender/listener)
- **Input System Advanced** (new chapter): Action Map switching, runtime rebinding (InteractiveRebinding + PlayerPrefs persistence), touch input patterns, Enhanced Input touch bindings
- **Shader Graph Basics** (new chapter): Creation workflow, 14-node quick reference, key material properties, common effects (dissolve, outline, ripple, fresnel, toon)
- **Mobile Optimization** (new chapter): Platform-specific settings checklist, runtime quality/lod/texture management, memory/fps detection, mobile-specific pitfalls (overdraw, battery, touch vs mouse)

---

## [2.0] - 2026-06-20 — Major Expansion
**Source**: project-ledger audit session

### Added
- **Editor Basics**: panel layout (Scene/Game/Hierarchy/Inspector/Project/Console), scene navigation shortcuts, Transform tools (W/E/R/Q/T/Y/V), Play/Pause/Step modes.
- **Project Setup**: template comparison table (6 templates), folder structure diagram, Unity Hub version management, Git setup with required `.gitignore` and `.meta` file explanation.
- **Package Manager**: 10 common packages quick-reference table with install/update/remove workflow.
- **C# Scripting Basics**: field visibility cheat sheet, Vector3/Vector2/Quaternion/Color type reference, `Time.deltaTime` with anti-pattern examples.
- **Lerp / SmoothDamp / MoveTowards**: 5 interpolation functions compared, common Lerp misuse (`t = Time.deltaTime`) with fix, SmoothDamp/SmoothStep/InverseLerp references.
- **Namespace**: 16 common namespaces table, custom namespace pattern, critical limitation warning (one file = one namespace for MonoBehaviour in Unity 2020.1+).
- **Null Reference Handling**: 6 common causes with fixes, defensive pattern code, Unity's special null override behavior.
- **Events & Delegates**: 4 communication patterns compared (serialized reference, UnityEvent, C# event/Action, SendMessage), cheat sheet for choosing.
- **Time.timeScale & Pausing**: pause/slow-motion code, affected vs unaffected table, selective pausing pattern.
- **Camera**: component properties table, scripting examples (ScreenPointToRay, WorldToScreenPoint), multi-camera setups (minimap, weapon overlay, split-screen, UI camera), Cinemachine quick-start.
- **Lighting**: light types comparison, real-time vs baked vs mixed decision table, Light Probes and Reflection Probes, Tags & Layers reference.
- **Physics vs Transform Movement**: the #1 beginner pitfall — direct transform.position on Rigidbody — with correct alternatives table.
- **Raycasting**: full API (raycast, sphere/box cast, layer masks, RaycastAll), debug visualization, Blueprint equivalent note.
- **2D Basics**: 3D→2D component mapping, Sprite Editor workflow, 2D physics API differences, sorting order hierarchy.
- **VFX (Particle System)**: Shuriken module reference table, script control, VFX Graph introduction, Shuriken vs VFX Graph selection guide.
- **Object Pooling**: full queue-based pool implementation, Unity built-in `ObjectPool<T>` reference, when-to-pool decision table.
- **Addressables**: load-by-address and AssetReference patterns, Resources replacement benefits.
- **Build & Publish**: Build Settings workflow, Player Settings quick-reference, Development Build, output folder structure.
- **Custom Inspector (Editor Scripting)**: CustomEditor pattern, `Editor/` folder convention.
- **async/await + UniTask**: UniTask quick-start, native Task caution, coroutine vs async decision table, cancellation token pattern.

### Principles
- Editor/Project Setup chapters for absolute beginners; coding chapters for intermediate.
- Each section includes both theory (why) and concrete code (how).
- Anti-patterns explicitly marked with ❌ and correct approaches with ✅.
- Decision tables added where multiple valid approaches exist.

---

## [1.0.0] - 2026-06-19 — Initial Release
**Source**: openSkills project launch (created via skill-creator)

### Added
- Unity engine core concepts: GameObject/Component architecture, scene management, render pipelines (URP/HDRP/Built-in), physics, animation system, UI Toolkit, uGUI, audio, input system (old + new), MonoBehaviour lifecycle, prefabs, ScriptableObject, coroutines, performance best practices.
- Version-specific references: `urp-2022.md` and `urp-unity6.md`.
- 14.8KB SKILL.md, ~1,088 lines.

### Principles
- Covers concept explanations and practical API patterns.
- Version-aware — separate reference files for 2022.3 LTS vs Unity 6.
- Maintenance: update when encountering recurring bugs, version migrations, or new engine features.
