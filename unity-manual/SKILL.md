---
name: unity-manual
version: 2.1.1
description: Unity engine core concepts and best practices. Use when the user mentions Unity, GameObject, Component, MonoBehaviour, Scene, URP, HDRP, render pipeline, physics engine, animation system, Animator, UI Toolkit, uGUI, audio, Input System, Input Manager, prefab, ScriptableObject, camera, Cinemachine, 2D, Sprite, particle system, VFX, Shuriken, lighting, Light Probe, build, publish, async await, UniTask, Addressables, custom inspector, events, delegates, UnityEvent, timeScale, pause, Lerp, SmoothDamp, raycast, object pooling, singleton, or is working on Unity game development tasks.
compatibility: unity-2022.3, unity-6
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Unity Engine Manual Skill

Covers Unity core concepts, API patterns, and best practices across versions from 2022.3 LTS to Unity 6.

## When to Use This Skill

Use this skill whenever the user asks about Unity development — writing scripts, designing scenes, debugging, optimizing, or understanding engine behaviour. This skill provides the mental model of how Unity works, not just API signatures.

## Editor Basics

Unity's editor is organized into dockable panels:

| Panel | Purpose |
|---|---|
| **Scene View** | Interactive 3D/2D viewport. Click to select objects, drag to move. |
| **Game View** | Preview what the player sees. Rendered from the active Camera. |
| **Hierarchy** | List of all GameObjects in the current Scene. Drag to reparent. |
| **Inspector** | Shows properties of the selected GameObject. Edit Components here. |
| **Project Window** | Your project's asset files. Drag assets into Scene or Hierarchy. |
| **Console** | Logs, warnings, errors. `Debug.Log("message")` prints here. |

**Scene navigation:**

| Action | Keys |
|---|---|
| Orbit around pivot | Hold **Alt + Left Mouse Button** + drag |
| Pan (slide view) | Hold **Alt + Middle Mouse Button** + drag |
| Zoom | **Scroll wheel** or hold **Alt + Right Mouse Button** + drag |
| Focus on selected object | Press **F** |
| Fly-through mode | Hold **Right Mouse Button** + **W/A/S/D** (hold Shift to speed up) |
| Reset pivot to origin | Double-click **Middle Mouse Button** |

**Transform tools:**

| Key | Mode |
|---|---|
| **W** | Move |
| **E** | Rotate |
| **R** | Scale |
| **Q** | Hand tool (pan view) |
| **T** | Rect tool (2D) |
| **Y** | Transform tool (move+rotate+scale) |
| **Ctrl+Shift+F** | Align with view (points object at camera) |
| **V** | Vertex snapping (hold and drag a corner to snap to another vertex) |

**Play modes:** Use the toolbar Play/Pause/Step buttons to enter Play Mode, pause execution, or advance frame-by-frame.

## Project Setup

### Creating a New Project

Open **Unity Hub** → **New Project** → pick a template:

| Template | What You Get |
|---|---|
| 2D (Built-In Render Pipeline) | 2D project, sprite defaults, no render pipeline package |
| 2D (URP) | 2D project with URP, Shader Graph, 2D lighting |
| 3D (Built-In Render Pipeline) | 3D project, legacy renderer |
| 3D (URP) | 3D project with Universal Render Pipeline |
| 3D (HDRP) | High-end 3D with HD Render Pipeline |
| Universal 3D (Unity 6+) | Unified template for mobile + desktop |

### Project Folder Structure

```
ProjectName/
├── Assets/          ← All your files live here (scenes, scripts, textures...)
├── Packages/        ← Package manifest (auto-managed)
├── ProjectSettings/ ← Editor/player settings, build config
├── Library/         ← Cached imports, shader compilation (ignore in git)
├── Temp/            ← Temporary files (ignore)
├── Logs/            ← Editor logs
└── UserSettings/    ← Per-user editor preferences (ignore)
```

### Unity Version Management

Use **Unity Hub** to install and switch engine versions. Projects created in newer versions can't be opened in older ones. Always make a backup before upgrading.

### Version Control Setup

Set in **Edit → Project Settings → Editor**:
- **Asset Serialization**: Force Text
- **Version Control Mode**: Visible Meta Files

**Required `.gitignore` entries:**
```
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
Logs/
UserSettings/
*.csproj
*.sln
```

`.meta` files MUST be committed — they store import settings, references, and GUIDs.

## Package Manager

Unity's modular system for adding features. **Window → Package Manager**.

| Package | Purpose |
|---|---|
| **Input System** | Modern input handling (replaces legacy Input Manager) |
| **Cinemachine** | Advanced camera system |
| **Universal RP / High Definition RP** | Render pipelines |
| **Shader Graph** | Visual shader creation |
| **Visual Effect Graph** | GPU particle effects |
| **ProBuilder** | In-editor 3D modeling |
| **TextMeshPro** | High-quality text rendering (default in Unity 6) |
| **Addressables** | Async asset loading and content updates |
| **Netcode for GameObjects** | Multiplayer networking |
| **2D Tilemap Editor** | 2D tile-based level design |

Click **Install** to add a package, **Update** for newer versions, **Remove** to uninstall.

---

## GameObject / Component Architecture

Every entity in Unity is a GameObject. GameObjects themselves do nothing — they are containers for Components.

### Core Principles

- **GameObject** = identity (name, tag, layer, active state) + transform + component list
- **Component** = behaviour (Rigidbody, Collider, MeshRenderer, custom scripts)
- **Transform** = always present, cannot be removed; position/rotation/scale in local and world space
- **AddComponent<T>()** adds at runtime; **GetComponent<T>()** retrieves; **TryGetComponent<T>()** is allocation-free

### Common Patterns

```csharp
// Cache references in Awake() — not in Start(), not in Update()
Rigidbody rb;
void Awake() { rb = GetComponent<Rigidbody>(); }

// Prefer TryGetComponent to avoid null checks
if (TryGetComponent<Collider>(out var col)) { /* use col */ }

// RequireComponent enforces dependencies at edit time
[RequireComponent(typeof(Rigidbody))]
public class Player : MonoBehaviour { }
```

### Key Rules

- Do not use `new` to create GameObjects — use `Instantiate()`, `GameObject.CreatePrimitive()`, or prefabs
- Destroy with `Destroy(gameObject)` or `Destroy(gameObject, delay)` — never `null` assign and expect GC
- `gameObject.SetActive(false)` disables the whole object; `enabled = false` disables one component
- Child GameObjects move/rotate/scale relative to their parent's Transform

## MonoBehaviour Lifecycle

Execution order is fixed. Understanding it prevents 90% of Unity timing bugs.

### Execution Order (simplified)

1. **Awake()** — called once when object is created. Use for self-referencing, not other objects (they may not be awake yet).
2. **OnEnable()** — called each time the object becomes active. Good for event subscriptions.
3. **Start()** — called once before first Update, after all Awake() complete. Safe to reference other objects here.
4. **FixedUpdate()** — physics timestep (default 0.02s). Put Rigidbody operations here.
5. **Update()** — once per frame. Most gameplay logic.
6. **LateUpdate()** — after all Update() calls. Camera follow, procedural animation.
7. **OnDisable()** — when object deactivates. Unsubscribe from events here.
8. **OnDestroy()** — when object is destroyed. Final cleanup.

### Common Pitfalls

- Getting another object's component in Awake() → that object's Awake() may not have run yet. Use Start() instead.
- Physics in Update() → jittery movement. Use FixedUpdate().
- Input in FixedUpdate() → missed inputs. Use Update().
- Forgetting to unsubscribe events in OnDisable() → memory leaks and null reference errors.

## C# Scripting Basics

Every script is a class that inherits from `MonoBehaviour`:

```csharp
using UnityEngine;

// Note: Simplified for teaching. For production physics movement, use
// rb.velocity or rb.MovePosition in FixedUpdate instead (see §Physics).
public class Player : MonoBehaviour
{
    // === FIELDS ===
    [SerializeField] private float speed = 5f;
    [SerializeField] private GameObject bulletPrefab;
    public int health = 100;

    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        transform.Translate(Vector3.forward * h * speed * Time.deltaTime);
    }
}
```

### Field Visibility Cheat Sheet

| Declaration | Visible in Inspector | Editable in Inspector |
|---|---|---|
| `public int x` | ✅ | ✅ |
| `[SerializeField] private int x` | ✅ | ✅ |
| `[HideInInspector] public int x` | ❌ | ❌ |
| `private int x` | ❌ | ❌ |
| `[NonSerialized] public int x` | ❌ | ❌ |

### Common Types

| Unity Type | C# Equivalent | Use |
|---|---|---|
| `Vector3` | (x, y, z) struct | Position, direction, scale |
| `Vector2` | (x, y) struct | 2D position, input, UV |
| `Quaternion` | Rotation struct | Use `Quaternion.Euler()` to create from degrees |
| `Color` | (r, g, b, a) struct | 0–1 range for each channel |
| `Transform` | Component | Position/Rotation/Scale of a GameObject |
| `GameObject` | Object | The GameObject itself |

### Time.deltaTime

Always multiply per-frame changes by `Time.deltaTime` (= seconds since last frame) to make movement frame-rate independent:

```csharp
// ❌ Frame-rate dependent
transform.Translate(Vector3.forward * speed);

// ✅ Frame-rate independent
transform.Translate(Vector3.forward * speed * Time.deltaTime);
```

### Lerp / SmoothDamp / MoveTowards

These functions smoothly interpolate values. The key mistake is misusing the `t` parameter in Lerp:

```csharp
// ❌ WRONG: Passing Time.deltaTime as t — never reaches target
transform.position = Vector3.Lerp(transform.position, target, Time.deltaTime);

// ✅ FIX: t should be a progress ratio (0→1)
float t = elapsed / duration; // 0 to 1 over time
transform.position = Vector3.Lerp(start, target, t);

// ✅ Smooth damping (spring-like motion, no overshoot, frame-rate independent)
transform.position = Vector3.SmoothDamp(transform.position, target, ref velocity, 0.3f);

// ✅ Linear movement at fixed speed
transform.position = Vector3.MoveTowards(transform.position, target, speed * Time.deltaTime);

// ✅ Color fade
spriteRenderer.color = Color.Lerp(Color.white, Color.clear, t);

// ✅ Easing (smoother start/stop)
float eased = Mathf.SmoothStep(0, 1, t);
```

| Function | Use for |
|---|---|
| **Lerp** | Generic interpolation (position, color, float) |
| **SmoothDamp** | Camera follow, springy movement, no overshoot |
| **MoveTowards** | Fixed-speed movement toward a target |
| **SmoothStep** | Eased in/out interpolation |
| **InverseLerp** | Convert a value to a 0-1 ratio |

### Namespace

#### Core Unity Namespaces

| Namespace | Purpose |
|---|---|
| **UnityEngine** | Core API: MonoBehaviour, GameObject, Transform, Vector3, Debug, Time, Random |
| **UnityEditor** | Editor-only: CustomEditor, EditorWindow, MenuItem. NOT included in builds. |
| **UnityEngine.UI** | uGUI: Button, Text, Slider, Canvas |
| **UnityEngine.UIElements** | UI Toolkit: VisualElement, Button, Label |
| **UnityEngine.InputSystem** | New Input System: InputAction, PlayerInput, Keyboard, Mouse |
| **UnityEngine.SceneManagement** | Scene loading: SceneManager, LoadSceneAsync |
| **UnityEngine.AddressableAssets** | Addressables resource management |
| **Cinemachine** | Cinemachine virtual cameras |
| **UnityEngine.VFX** | VFX Graph (GPU particles) |
| **UnityEngine.Events** | UnityEvent, UnityAction |
| **Unity.Mathematics** | Burst-compatible math: float3, float4x4, quaternion |
| **Unity.Collections** | High-performance containers: NativeArray, NativeList |
| **System** | DateTime, Math, Action, Func, EventHandler |
| **System.Collections.Generic** | List\<T\>, Dictionary\<K,V\>, Queue\<T\>, Stack\<T\> |
| **System.Linq** | LINQ queries. Use sparingly — allocates GC. |
| **System.Threading.Tasks** | Native Task, async/await |
| **Cysharp.Threading.Tasks** | UniTask (recommended async library, zero-allocation) |

#### Custom Namespace

Wrap your scripts in a namespace to prevent class name conflicts (essential when project scales up):

```csharp
// ❌ Global scope — "Controller" could conflict with another "Controller"
public class Controller : MonoBehaviour { }

// ✅ Namespaced — unambiguous
namespace MyGame.Player
{
    public class Controller : MonoBehaviour
    {
        private void Update()
        {
            float h = Input.GetAxis("Horizontal");
            transform.Translate(Vector3.forward * h * Time.deltaTime);
        }
    }
}

// Usage elsewhere:
using MyGame.Player;  // then just: Controller controller;
// or without using:  MyGame.Player.Controller controller;
```

#### Namespace Limitation (Unity 2020.1–2022.1 only)

In Unity versions prior to 2022.2, a single file could not contain MonoBehaviour classes from different namespaces. This restriction was **lifted in Unity 2022.2**. Since this skill targets 2022.3+, the limitation no longer applies. Old Asset Store packages may still contain this issue from pre-2022.2 projects.

### Null Reference Handling

The most common Unity error: `NullReferenceException`. You tried to use something that doesn't exist.

**Causes and fixes:**

| Cause | Fix |
|---|---|
| `GetComponent<T>()` returned null (component not attached) | Add `[RequireComponent(typeof(T))]` or add component manually |
| Inspector field not assigned | Assign the reference in Inspector, or use `[SerializeField]` |
| `GameObject.Find()` returned null | Wrong name or GameObject not in scene — prefer serialized references |
| `Instantiate()` returned null | Prefab field not assigned in Inspector |
| Reference destroyed between frames | Check `if (obj != null)` or use `TryGetComponent()` |
| Event listener on destroyed object | Always unsubscribe in `OnDisable()` / `OnDestroy()` |

**Defensive pattern:**
```csharp
[SerializeField] private Rigidbody rb; // assign in Inspector

void Start()
{
    if (rb == null)
        rb = GetComponent<Rigidbody>(); // fallback if not assigned

    // Prefer TryGetComponent to avoid null entirely:
    if (TryGetComponent<Collider>(out var col))
        col.enabled = false;
}
```

**Unity's special null:** Unity overrides `==` — a destroyed GameObject is `null` but not C# null. `?.` operator may behave unexpectedly. Stick with explicit `if (obj == null)` checks or `if (obj)` (Unity's implicit bool conversion).

---

## Events & Delegates

Unity provides several ways for scripts to communicate:

### 1. Serialized Reference (simplest)

Drag one GameObject into another's Inspector field:

```csharp
[SerializeField] private GameObject otherObject;
// Then: otherObject.GetComponent<Enemy>().TakeDamage(10);
```

### 2. UnityEvent (Inspector-wired, designer-friendly)

```csharp
using UnityEngine.Events;

public class Health : MonoBehaviour
{
    private int health = 100;
    public UnityEvent onDeath;  // shows in Inspector

    public void TakeDamage(int amount)
    {
        health -= amount;
        if (health <= 0)
            onDeath.Invoke(); // fires all wired listeners
    }
}
```
In Inspector, click `+` on `OnDeath`, drag a GameObject, pick a method — no code needed.

### 3. C# event / Action (code-only, performant)

```csharp
using System;

public class Health : MonoBehaviour
{
    public event Action OnDeath;  // C# event

    private void Die()
    {
        OnDeath?.Invoke(); // null-conditional: only fires if someone subscribed
    }
}

// Listener:
void OnEnable()  { GetComponent<Health>().OnDeath += Respawn; }
void OnDisable() { GetComponent<Health>().OnDeath -= Respawn; }
void Respawn()   { /* ... */ }
```

### 4. SendMessage (avoid for production)

```csharp
// Slow, string-based, no compile-time checking. Legacy.
gameObject.SendMessage("OnDamage", 10);
// Use event/UnityEvent instead.
```

### Communication Cheat Sheet

| Need | Use |
|---|---|
| Known objects in same scene | Serialized field reference |
| Designer wants to wire in Inspector | UnityEvent |
| Many listeners, code-only, high performance | C# event / Action |
| Global/manager singleton | Static instance or Singleton pattern |
| Cross-scene communication | ScriptableObject event channel |

---

## Time.timeScale & Pausing

`Time.timeScale` controls the speed of time for the entire game:

```csharp
// Pause the game (freezes Update, FixedUpdate, Coroutines, physics, audio)
Time.timeScale = 0f;

// Slow motion (half speed)
Time.timeScale = 0.5f;

// Resume normal
Time.timeScale = 1f;
```

**Pausing done right:**

```csharp
bool isPaused = false;

void Update()
{
    if (Input.GetKeyDown(KeyCode.Escape))
    {
        isPaused = !isPaused;
        Time.timeScale = isPaused ? 0f : 1f;
        pauseMenu.SetActive(isPaused);
    }
}
```

**What timeScale affects and what it doesn't:**

| Affected | NOT affected |
|---|---|
| Update(), FixedUpdate(), LateUpdate() | `Time.unscaledDeltaTime` (use for pause menu UI) |
| Coroutines (WaitForSeconds etc.) | `WaitForSecondsRealtime` |
| Physics simulation | `Update()` with `Time.unscaledDeltaTime` |
| Audio (pitch changes) | `Animator.updateMode = UnscaledTime` |

**Selective pausing:** For per-object pause (e.g., pause enemies but not player), use a manual bool flag + `if (isPaused) return;` at the top of Update() rather than timeScale.

---

## Scene Management

### Core API (Unity 5.3+ SceneManager)

```csharp
using UnityEngine.SceneManagement;

// Load single scene (replaces current)
SceneManager.LoadScene("Level2");
SceneManager.LoadScene(1); // build index

// Async loading with progress
var op = SceneManager.LoadSceneAsync("Level2");
op.allowSceneActivation = false; // pause before activation
while (op.progress < 0.9f) { /* show loading bar */ }
op.allowSceneActivation = true;

// Additive loading (multiple scenes at once)
SceneManager.LoadScene("UI", LoadSceneMode.Additive);
SceneManager.UnloadSceneAsync("UI");
```

### DontDestroyOnLoad

Objects that persist across scene loads (audio managers, game state). Creates a new root GameObject on scene change.

```csharp
void Awake() { DontDestroyOnLoad(gameObject); }
```

### Version Notes

- SceneManager API stable across 2022.3 → Unity 6
- Scene references via build settings index or full path name

## Camera

### Camera Component

| Property | Purpose |
|---|---|
| **Clear Flags** | Skybox (default), Solid Color, Depth Only, Don't Clear |
| **Projection** | Perspective (3D) or Orthographic (2D, isometric) |
| **Field of View** | Vertical FOV in degrees (perspective only) |
| **Size** | Half-height in world units (orthographic only) |
| **Clipping Planes** | Near (default 0.3) and Far (default 1000) — objects outside this range are culled |
| **Culling Mask** | Which layers the camera renders (e.g., hide UI from main camera) |
| **Depth** | Rendering order (higher = renders on top) |
| **Target Texture** | Render to a RenderTexture instead of the screen (minimaps, portals, CCTV) |

### Camera Scripting

```csharp
Camera cam = Camera.main; // returns first camera tagged "MainCamera"

// Convert screen point to world ray
Ray ray = cam.ScreenPointToRay(Input.mousePosition);
if (Physics.Raycast(ray, out RaycastHit hit))
    Debug.Log(hit.point); // world position under cursor

// Convert world to screen (for health bars, nameplates)
Vector3 screenPos = cam.WorldToScreenPoint(enemy.position);
if (screenPos.z > 0) // in front of camera
    UIElement.position = screenPos;
```

### Multiple Cameras

| Setup | How |
|---|---|
| **Minimap** | Second camera → Target Texture → RawImage in Canvas |
| **Weapon overlay** | Camera with Culling Mask = "Weapon" layer only, Depth = 1 |
| **Split-screen** | Two cameras, each with `rect` set to half the screen |
| **UI camera** | Camera with Culling Mask = "UI" layer, Clear Flags = Depth Only |

### Cinemachine

For advanced camera behaviors (follow, look-at, shake, transitions):

```csharp
using Cinemachine; // requires Cinemachine package

// Virtual camera that follows a target
CinemachineVirtualCamera vcam;
vcam.Follow = player.transform;
vcam.LookAt = player.transform;

// Camera shake
vcam.GetCinemachineComponent<CinemachineBasicMultiChannelPerlin>().m_AmplitudeGain = 2f;
```

Cinemachine handles blending, collision detection, and dead zones — use it instead of manual camera scripting for complex setups.

---

## Render Pipelines

Unity has three render pipelines. The user's project determines which to use.

### Pipeline Overview

| Pipeline | Use Case | Pipeline Asset Type |
|---|---|---|
| Built-in | Legacy projects, quick prototyping | None (default) |
| URP | Most projects (2D, 3D, mobile, cross-platform) | UniversalRenderPipelineAsset |
| HDRP | High-end 3D (PC, console, realistic graphics) | HDRenderPipelineAsset |

### URP Key Concepts

- **Forward/Deferred rendering**: Forward for most cases; Deferred for many dynamic lights
- **Renderer Features**: Custom pass injection without full SRP coding
- **Shader Graph**: Visual shader creation, URP-native
- **2D Renderer**: Dedicated 2D lighting and shadow system
- **Camera Stacking**: Overlay/Base camera system for UI overlays, minimaps

### HDRP Key Concepts

- **Physically-based rendering**: Realistic materials, lighting, volumetrics
- **HDRP Asset configuration**: Global rendering settings (shadows, LOD, decals)
- **Volume framework**: Post-processing, sky, fog applied per-zone via volumes
- **Ray tracing**: Hardware-accelerated reflections, shadows, GI (Unity 6+)

### URP Version Differences

- **2022.3**: RenderGraph API experimental; URP 14.x; Forward+ path available
- **Unity 6**: RenderGraph default; URP 17.x; GPU Resident Drawer; Probe Volumes for GI
- See `references/urp-2022.md` and `references/urp-unity6.md` for detailed differences

### Shader Basics

```hlsl
// URP shader include (HLSL)
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

// Accessing main light in URP
Light mainLight = GetMainLight();
half3 lightDir = mainLight.direction;
half3 lightColor = mainLight.color;
```

## Lighting

### Light Types

| Type | Use Case |
|---|---|
| **Directional Light** | Sun/moon. Affects everything regardless of position. |
| **Point Light** | Light bulb, explosion. Emits in all directions, has range. |
| **Spot Light** | Flashlight, headlight. Cone-shaped, range + angle. |
| **Area Light** | Soft lighting from a rectangular surface. Baked only (not real-time). |

### Real-time vs Baked

| Mode | Performance | Quality | Dynamic Objects |
|---|---|---|---|
| **Realtime** | Expensive | Good | Lit and cast shadows |
| **Baked** (Lightmap) | Cheap at runtime | Best (precomputed) | Only receive indirect light, no shadows |
| **Mixed** | Medium | Good | Static objects baked, dynamic objects get real-time |

Baking requires objects to be marked **Static** (Inspector → Static checkbox) and having `Generate Lighting` enabled.

### Light Probes & Reflection Probes

- **Light Probes**: Sample lighting at discrete positions in a scene. Dynamic objects use the nearest probes for indirect lighting. Essential when mixing baked lighting with moving characters.
- **Reflection Probes**: Capture the environment for reflections. Place near reflective surfaces (metal, water, glass).

### Tags & Layers

Tags and Layers are metadata for identifying and filtering GameObjects:

**Tag — identifies a specific object:**
```csharp
if (other.CompareTag("Player")) { /* hit the player */ }
GameObject player = GameObject.FindWithTag("Player"); // returns one object
GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy"); // all objects

// Set tag: Inspector → Tag dropdown, or script:
gameObject.tag = "Enemy";
```

**Layer — filters rendering and collision:**
```csharp
// Check if an object is on a specific layer
if (other.gameObject.layer == LayerMask.NameToLayer("Enemy"))
    return; // ignore enemies

// LayerMask for raycast filtering
int enemyMask = LayerMask.GetMask("Enemy", "Obstacle");
Physics.Raycast(origin, dir, out hit, 100f, enemyMask);
```

Define tags and layers in **Edit → Project Settings → Tags and Layers**.

---

## Physics

### Rigidbody vs Rigidbody2D

3D physics (NVIDIA PhysX) → `Rigidbody` + `Collider` (Box/Sphere/Capsule/Mesh/Terrain)
2D physics (Box2D) → `Rigidbody2D` + `Collider2D`

### Rigidbody Properties

| Property | Purpose |
|---|---|
| mass | Affects collision response, not gravity speed |
| drag | Air resistance (0 = no resistance) |
| angularDrag | Rotational resistance |
| useGravity | Enable/disable gravity |
| isKinematic | Physics-driven or script-driven |
| interpolation | Smooth movement for jitter reduction |
| collisionDetectionMode | Continuous for fast objects (prevents tunnelling) |

### Applying Forces

```csharp
// In FixedUpdate() only
void FixedUpdate() {
    rb.AddForce(Vector3.forward * speed);        // continuous force
    rb.AddForce(Vector3.up * 10f, ForceMode.Impulse);      // instant push
    rb.MovePosition(targetPos);                    // kinematic movement
}
```

### Collision Detection

```csharp
void OnCollisionEnter(Collision col) { /* first contact */ }
void OnCollisionStay(Collision col) { /* persistent contact */ }
void OnCollisionExit(Collision col) { /* contact ends */ }

// Trigger variant (IsTrigger = true on collider)
void OnTriggerEnter(Collider other) { }
```

### Layers & Collision Matrix

Use Edit → Project Settings → Physics → Layer Collision Matrix to disable collisions between specific layers. Performance-critical for complex scenes.

### Physics vs Transform Movement

The #1 beginner pitfall: moving a Rigidbody by changing `transform.position` directly.

```csharp
// ❌ BROKEN: Bypasses physics, causes tunneling, ignores collisions
transform.position += Vector3.forward * speed * Time.deltaTime;

// ❌ ALSO BROKEN: Same problem
rb.position = newPosition; // Better but still teleports (instant, no velocity transfer)

// ✅ CORRECT: Use velocity or forces (in FixedUpdate)
rb.velocity = new Vector3(input.x * speed, rb.velocity.y, input.y * speed);

// ✅ OR: Use forces for acceleration-based movement
rb.AddForce(Vector3.forward * force);

// ✅ Kinematic (non-physics) object: use MovePosition in FixedUpdate
void FixedUpdate() { rb.MovePosition(rb.position + moveDir * speed * Time.fixedDeltaTime); }
```

| When to use | Method |
|---|---|
| Player/enemy with physics interaction | `rb.velocity` or `AddForce()` in FixedUpdate |
| Platform/trigger/kinematic object | `rb.MovePosition()` in FixedUpdate |
| Purely visual (no collision, no physics) | `transform.Translate()` in Update |
| Character controller (no Rigidbody) | `CharacterController.Move()` |

### Raycasting

Fire a ray into the scene and get what it hits — essential for shooting, interaction, AI vision:

```csharp
Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
if (Physics.Raycast(ray, out RaycastHit hit, 100f))
{
    Debug.Log($"Hit: {hit.collider.name} at {hit.point}");

    // Get the object hit
    GameObject obj = hit.collider.gameObject;

    // Check tag
    if (hit.collider.CompareTag("Enemy"))
        hit.collider.GetComponent<Enemy>().TakeDamage(10);

    // Visualize in Scene view
    Debug.DrawRay(ray.origin, ray.direction * hit.distance, Color.red, 1f);
}

// Filter by layer mask
int enemyMask = LayerMask.GetMask("Enemy", "Obstacle");
if (Physics.Raycast(ray, out hit, 100f, enemyMask)) { /* only hits Enemies/Obstacles */ }

// Sphere/box casts (like a thick ray)
if (Physics.SphereCast(ray.origin, 0.5f, ray.direction, out hit, 10f)) { }

// RaycastAll (get all hits along ray, sorted by distance)
RaycastHit[] hits = Physics.RaycastAll(ray, 100f);
```

**Unreal equivalent:** `UWorld::LineTraceSingleByChannel()` in C++, or the `Line Trace By Channel` node in Blueprints.

### Common Pitfall

Ignoring the raycast origin — `ScreenPointToRay` starts at camera position. For FPS shooting from the player's gun barrel, use `gunBarrel.position` as origin rather than camera.

## 2D Basics

Unity has a dedicated 2D mode with specialized tools:

### Core Components

| Component | 3D Equivalent | Purpose |
|---|---|---|
| **Sprite Renderer** | MeshRenderer | Renders a 2D sprite (image) |
| **Sprite** | Texture/Material | The 2D image asset |
| **Rigidbody2D** | Rigidbody | 2D physics body (Box2D engine) |
| **Collider2D** (Box/Circle/Polygon) | Collider (Box/Sphere) | 2D collision shape |
| **Tilemap** | — | Grid-based tile placement |
| **Tilemap Renderer** | — | Renders tilemap grids |

### Sprite Editor

Select a sprite asset → **Sprite Editor** button in Inspector. Slice sprite sheets into individual sprites via **Slice → Grid by Cell Size** or **Automatic**.

### 2D Physics Differences

```csharp
// 2D physics uses different APIs
Rigidbody2D rb2d;
void OnCollisionEnter2D(Collision2D col) { }  // note the "2D" suffix
void OnTriggerEnter2D(Collider2D other) { }

// Movement in 2D
rb2d.velocity = new Vector2(moveSpeed, rb2d.velocity.y); // horizontal movement only

// 2D raycast
RaycastHit2D hit = Physics2D.Raycast(origin, direction, distance, layerMask);
```

### Sorting Order

Sprites render in order controlled by:
1. **Sorting Layer** (background, midground, foreground)
2. **Order in Layer** (number within the layer, higher = on top)
3. **Distance from camera** (for transparent sort axis)

Set in SpriteRenderer or via script: `spriteRenderer.sortingOrder = 5;`

---

## Animation

### Animator Controller

State machine-based animation system. Components: Animator component + AnimatorController asset.

```csharp
Animator anim;
void Awake() { anim = GetComponent<Animator>(); }

// Parameter types: Float, Int, Bool, Trigger
anim.SetFloat("Speed", moveSpeed);
anim.SetBool("IsGrounded", isGrounded);
anim.SetTrigger("Jump");

// State info
AnimatorStateInfo state = anim.GetCurrentAnimatorStateInfo(0);
if (state.IsName("Run")) { /* ... */ }

// Cross-fade with duration
anim.CrossFade("Death", 0.1f);

// Immediate state transition (no blend)
anim.Play("Death");

// Cache hash for performance (avoid string lookup per call)
int deathHash = Animator.StringToHash("Death");
if (state.shortNameHash == deathHash) { /* in Death state */ }
```

### Animation Curves

Expose parameters to curves for precise timeline control. Useful for root motion, hitbox timing, footstep events.

### Legacy Animation Component

Still functional but deprecated. Use Animator for new projects.

### Humanoid vs Generic Rigs

- **Humanoid**: Avatar system for retargeting animations between characters. Required for Mecanim.
- **Generic**: For non-human characters, simpler setup.

### Animation Retargeting (Humanoid Avatar)

Unity's Humanoid Avatar system enables reusing animations across different characters, similar to Unreal's Compatible Skeleton retargeting:

1. **Configure Avatar**: Select imported model → Rig tab → Animation Type: Humanoid → Apply. Unity auto-maps bones.
2. **Verify mapping**: Click "Configure" → check bone assignment (head, spine, arms, legs). Fix unmapped bones (green = good, grey = missing).
3. **Retarget to another model**: Select animator's Avatar → set it to any Humanoid skeleton. Animations auto-retarget — different proportions handled.

**Sharing animations across models:**
```csharp
// Import animation once, use on multiple characters:
// Set "Copy From Other Avatar" in the animation import settings
// Point to any model with a valid Humanoid Avatar
```

**Muscle space control**: Use `Avatar Mask` to control which body parts receive animation (e.g., upper body running + lower body custom IK).

```csharp
// Apply animation with mask
animator.SetLayerWeight(layerIndex, 1f); // enable layer
// Layer mask in Animator Controller controls which body parts animate
```

**Common issues:**
- T-pose instead of animation: Avatar not configured Humanoid for source model
- Bone stretching: bone mapping incorrect in Avatar configuration
- Model scale mismatch: check "Use Normalized" for muscle interpolation

## VFX (Particle System)

### Shuriken Particle System

Unity's built-in CPU particle system. Add a **Particle System** component to any GameObject.

| Module | What It Controls |
|---|---|
| **Main** | Duration, looping, start lifetime/speed/size/color, gravity modifier |
| **Emission** | Rate over time or distance, burst (one-time spawn) |
| **Shape** | Emission volume: sphere, cone, box, circle, mesh |
| **Color over Lifetime** | Gradient across particle lifespan |
| **Size over Lifetime** | Scale curve |
| **Velocity over Lifetime** | Speed changes over time |
| **Noise** | Turbulence, random wobble |
| **Renderer** | How particles look: billboard, mesh, stretched billboard |

```csharp
// Control via script
ParticleSystem ps;
ps.Play();          // start emission
ps.Stop();          // stop emitting (existing particles continue)
ps.Clear();         // remove all particles
ps.emissionRate = 50f;

// One-shot burst at position
ParticleSystem.EmitParams emitParams = new ParticleSystem.EmitParams();
emitParams.position = transform.position;
emitParams.velocity = Vector3.up * 5f;
ps.Emit(emitParams, 10); // emit 10 particles
```

### VFX Graph (GPU)

Package: **Visual Effect Graph**. GPU-based, handles millions of particles. Visual node-based editor. Use for complex VFX (swarms, trails, reactive particles). Requires URP or HDRP — not available in Built-in Render Pipeline.

### Choosing Shuriken vs VFX Graph

| Scenario | Use |
|---|---|
| Simple effects (< 1000 particles) | Shuriken |
| Complex behavior, GPU compute | VFX Graph |
| Mobile / Built-in RP | Shuriken (VFX Graph not supported) |
| Millions of particles | VFX Graph |

---

## UI Toolkit vs uGUI

Unity has two UI systems. Both are actively supported.

### uGUI (UnityEngine.UI)

The original Canvas-based UI system. Simpler, more tutorials available.

```csharp
using UnityEngine.UI;

Button btn = GetComponent<Button>();
btn.onClick.AddListener(() => Debug.Log("Clicked"));

Text label = GetComponent<Text>();
label.text = "Hello";

Slider slider = GetComponent<Slider>();
slider.onValueChanged.AddListener(OnVolumeChange);
```

Canvas render modes: Screen Space Overlay, Screen Space Camera, World Space.

**Anchors and scaling:** Select a UI element → Rect Transform → Anchor Presets. Anchors define how the element resizes/stretches when screen resolution changes. Hold Shift to set pivot, Alt to set position. For responsive layouts: Unity uses stretch anchors (the 4-arrow icon) to make UI fill a percentage of the screen.

**Canvas Scaler:** Controls how UI scales across resolutions → Constant Pixel Size (fixed), Scale With Screen Size (responsive, recommended), Constant Physical Size.

### UI Toolkit (UIElements)

Newer retained-mode UI system. CSS-like styling (USS), XML-like layout (UXML). Better for complex editor tools and scalable game UI.

```csharp
using UnityEngine.UIElements;

var root = GetComponent<UIDocument>().rootVisualElement;
var btn = root.Q<Button>("start-btn");
btn.clicked += () => Debug.Log("Clicked");

var label = root.Q<Label>("title");
label.text = "Hello";
```

### When to Use Which

- Rapid prototyping, mobile UI, simple menus → uGUI
- Complex data-driven UI, editor tools, scalable runtime UI → UI Toolkit
- Unity 6 pushes UI Toolkit more aggressively, but uGUI is not deprecated

## Audio

### Audio Source + Audio Listener

- **AudioSource**: Plays audio clips (2D/3D, spatial blend, volume, pitch, loop)
- **AudioListener**: Usually on Main Camera, receives audio

```csharp
AudioSource source;

// One-shot sound effects (no component needed)
AudioSource.PlayClipAtPoint(clip, position, volume);

// Play on existing source
source.clip = clip;
source.Play();
source.PlayOneShot(clip, volume);

// 3D audio settings
source.spatialBlend = 1.0f; // 0=2D, 1=3D
source.minDistance = 1f;
source.maxDistance = 50f;
```

### Audio Mixer

Route audio through mixer groups for volume control, effects (reverb, EQ), and snapshot transitions. Useful for volume settings, pause menus, and dynamic mixing.

## Input System

Unity has two input systems. Both are currently supported.

### Old Input Manager (Input class)

```csharp
// In Update()
float horizontal = Input.GetAxis("Horizontal");
float vertical = Input.GetAxis("Vertical");
bool jump = Input.GetButtonDown("Jump");
bool fire = Input.GetButton("Fire1");
Vector3 mousePos = Input.mousePosition;
```

- Configured in Edit → Project Settings → Input Manager
- Simple, quick to use
- No rebinding support, not device-agnostic

### New Input System (Input System Package)

```csharp
using UnityEngine.InputSystem;

// Action-based (C# events)
PlayerInput playerInput;
void Awake() {
    playerInput = GetComponent<PlayerInput>();
    playerInput.actions["Jump"].performed += OnJump;
}

// Direct read (polling)
Gamepad gamepad = Gamepad.current;
if (gamepad != null) {
    Vector2 move = gamepad.leftStick.ReadValue();
}

// Keyboard + Mouse
Keyboard keyboard = Keyboard.current;
Mouse mouse = Mouse.current;
if (keyboard.spaceKey.wasPressedThisFrame) { /* jump */ }
```

### Version Notes

- 2022.3: Both systems available; New Input System is the recommended default
- Unity 6: New Input System is the default for new projects

## Prefabs

Prefabs are reusable GameObject templates stored as assets. Changes to the prefab asset propagate to all instances.

### Key Operations

- **Create**: Drag GameObject from Hierarchy to Project window
- **Open**: Double-click prefab to edit in isolation (Prefab Mode)
- **Override**: Instance changes can be applied back to the prefab or reverted
- **Variants**: Create derived prefabs that inherit from a base prefab
- **Unpack**: Break prefab connection for full independence

```csharp
// Instantiate from prefab reference
[SerializeField] GameObject bulletPrefab;
void Fire() { Instantiate(bulletPrefab, muzzle.position, muzzle.rotation); }
```

## ScriptableObject

Data container assets that live as project files, not scene objects. Ideal for configuration, item databases, skill definitions.

```csharp
[CreateAssetMenu(fileName = "NewItem", menuName = "Game/Item")]
public class ItemData : ScriptableObject {
    public string itemName;
    public Sprite icon;
    public int maxStack;
    public GameObject prefab;
}

// Usage: reference in any MonoBehaviour
[SerializeField] ItemData healingPotion;
```

Use ScriptableObject for data that multiple objects share — avoid duplicating data across prefabs.

### ScriptableObject as Event Channel

A powerful decoupling pattern: use ScriptableObject as an intermediary that components listen to without knowing each other:

```csharp
// IntEventSO.cs — a ScriptableObject that holds an integer + an event
[CreateAssetMenu(menuName = "Events/Int Event")]
public class IntEventSO : ScriptableObject
{
    public int value;
    public UnityAction<int> OnValueChanged;

    public void SetValue(int newValue)
    {
        value = newValue;
        OnValueChanged?.Invoke(value);
    }
}

// PlayerHealth.cs — broadcasts health change
public class PlayerHealth : MonoBehaviour
{
    public IntEventSO healthEvent; // assign in Inspector
    public void TakeDamage(int dmg) { healthEvent.SetValue(currentHealth); }
}

// HealthBarUI.cs — listens for health change (no reference to PlayerHealth needed!)
public class HealthBarUI : MonoBehaviour
{
    public IntEventSO healthEvent;
    void OnEnable() { healthEvent.OnValueChanged += UpdateBar; }
    void OnDisable() { healthEvent.OnValueChanged -= UpdateBar; }
    void UpdateBar(int hp) { slider.value = hp; }
}
```

This pattern eliminates GetComponent chains and spaghetti references.

## Singleton

A global manager that persists across scenes:

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject); // destroy duplicate
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void RestartLevel() { SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex); }
}

// Usage from anywhere:
GameManager.Instance.RestartLevel();
```

**When to Singleton:** GameManager, AudioManager, SaveManager, InputManager — exactly ONE per project. Not for enemies, UI, or gameplay objects.

**When NOT to Singleton:** Don't use Singleton as a get-out-of-jail-free card instead of proper references. If only 2-3 scripts need the reference, use a serialized field. Reserve Singletons for truly global systems.

## Object Pooling

Reuse GameObjects instead of Instantiating/Destroying repeatedly — essential for bullets, enemies, VFX:

```csharp
// Basic pool pattern
public class ObjectPool : MonoBehaviour
{
    public GameObject prefab;
    public int poolSize = 20;
    private Queue<GameObject> pool = new Queue<GameObject>();

    void Start()
    {
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public GameObject Get()
    {
        if (pool.Count == 0)
        {
            // Expand pool: instantiate + enqueue before dequeueing
            GameObject newObj = Instantiate(prefab);
            newObj.SetActive(false);
            pool.Enqueue(newObj);
        }
        GameObject obj = pool.Dequeue();
        obj.SetActive(true);
        return obj;
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

**Unity's built-in:** `UnityEngine.Pool.ObjectPool<T>` and `UnityEngine.Pool.GenericPool<T>` (Unity 2021+) provide allocation-free pools with less boilerplate.

### When to Pool
| Pool | Don't Pool |
|---|---|
| Bullets, projectiles | One-off level geometry |
| Enemy spawns (hordes) | Cutscene-specific objects |
| VFX (explosions, impacts) | Player character |
| UI elements (scrolling list) | Objects with complex Awake setup |

---

## Addressables

Modern asset management system (replaces the old `Resources` folder). Assets are loaded asynchronously by address, not by file path.

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

// Load by address (set in asset's Addressable settings)
Addressables.LoadAssetAsync<GameObject>("Enemy_Goblin").Completed += handle =>
{
    if (handle.Status == AsyncOperationStatus.Succeeded)
        Instantiate(handle.Result);
};

// Load by asset reference (type-safe Inspector field)
[SerializeField] private AssetReferenceGameObject enemyPrefab;
// Load: enemyPrefab.InstantiateAsync().Completed += ...

// Load a scene
Addressables.LoadSceneAsync("Level2");
```

Benefits over `Resources`:
- No monolithic Resources folder — any asset can be addressable
- Remote asset bundles for live content updates
- Memory management: `Addressables.Release()` to unload
- Dependency tracking: shared assets loaded once

## Build & Publish

### Build Settings

**File → Build Settings** or `Ctrl+Shift+B`:

1. Add scenes to **Scenes in Build** (drag from Project window)
2. Select target **Platform** (PC/Mac/Linux, Android, iOS, WebGL)
3. Click **Switch Platform** (first time takes a while — assets reimport)
4. Click **Build** or **Build and Run**

### Player Settings

Configure app name, icon, resolution, splash screen, and platform-specific options:

| Setting | Where |
|---|---|
| Company/Product Name | Player Settings → Player |
| Default icon | Player Settings → Icon |
| Resolution / Fullscreen | Player Settings → Resolution and Presentation |
| Quality levels | Project Settings → Quality |
| Android package name | Player Settings → Other Settings → Identification |
| iOS bundle identifier | Player Settings → Other Settings → Identification |

### Development Build

Tick **Development Build** in Build Settings for debug logs, profiling, and console access in standalone builds.

### Build Folder Structure

After building, the output folder contains:
- `ProjectName.exe` (Windows) or `.app` (Mac)
- `ProjectName_Data/` (all game assets, Mono runtime, managed assemblies)
- `MonoBleedingEdge/` (.NET runtime)

Distribute the entire folder — they all depend on each other.

## Custom Inspector (Editor Scripting)

Create custom Inspector UI for your scripts:

```csharp
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(Player))]
public class PlayerEditor : Editor
{
    public override void OnInspectorGUI()
    {
        Player player = (Player)target;

        // Draw default inspector fields first
        DrawDefaultInspector();

        // Add custom buttons
        if (GUILayout.Button("Reset Player"))
            player.ResetToSpawn();

        // Add help box
        EditorGUILayout.HelpBox("Player settings affect all instances.", MessageType.Info);
    }
}
```

Place Editor scripts in an `Editor/` folder (anywhere under Assets). They won't be included in builds.

**Simpler alternative — `[ContextMenu]`:** For simple right-click context actions on a component without creating an Editor script:

```csharp
[ContextMenu("Reset Player")]
void ResetToSpawn() { transform.position = Vector3.zero; }
```

Right-click the component in Inspector → `Reset Player`. Zero Editor scripting needed.

---

## Coroutines

```csharp
void Start() { StartCoroutine(FadeOut()); }

IEnumerator FadeOut() {
    Renderer renderer = GetComponent<Renderer>();
    float t = 0;
    while (t < 1f) {
        t += Time.deltaTime / duration;
        renderer.material.color = Color.Lerp(Color.white, Color.clear, t);
        yield return null; // wait one frame
    }
}

// Wait for seconds (cache to avoid GC allocation)
WaitForSeconds wait = new WaitForSeconds(2f);
yield return wait;

// Wait until condition
yield return new WaitUntil(() => health <= 0);

// Chain coroutines
yield return StartCoroutine(AnotherRoutine());
```

### Coroutine Pitfalls

- Coroutines stop when the GameObject is disabled/destroyed — handle cleanup
- `WaitForSeconds` creates garbage; cache the instance: `WaitForSeconds wait = new(1f);`
- Don't mix async/await with coroutines — choose one pattern per system

### Coroutines vs Update vs Invoke

| | Update | Coroutine | InvokeRepeating |
|---|---|---|---|
| **Runs** | Every frame | Over time, frame by frame | Fixed interval |
| **Stops when** | Object destroyed / disabled | Object destroyed / disabled + manual StopCoroutine | Object destroyed / disabled |
| **Delay support** | Manual timer variable | `yield return new WaitForSeconds(n)` | Built-in: `Invoke("Method", delay)` |
| **GC allocation** | None if coded cleanly | Moderate (yield instructions) | String-based (slow) |
| **Readability** | State machines get messy | Clean sequenced logic | Fragmented (scattered methods) |
| **Use for** | Continuous input, animation | Sequenced events, fading, cutscenes | Simple repeating tasks (avoid for new code) |

**Decision rule:** If it's a sequence of events over time → Coroutine. If it's continuous per-frame logic → Update. Avoid `Invoke` — it's string-based and has no cancellation except `CancelInvoke()` which cancels all at once.

## async/await

Modern C# async patterns. Use `UniTask` (recommended, zero-allocation) or native `Task`.

### UniTask (Recommended)

Install `UniTask` via Package Manager (by URL: `https://github.com/Cysharp/UniTask.git?path=src/UniTask/Assets/Plugins/UniTask`).

```csharp
using Cysharp.Threading.Tasks;

// Note: async void Start is required by Unity's MonoBehaviour lifecycle.
// Prefer async UniTaskVoid for non-lifecycle methods for proper exception handling.
async void Start()
{
    // Wait 2 seconds
    await UniTask.Delay(2000);

    // Wait until condition
    await UniTask.WaitUntil(() => health <= 0);

    // Wait for next frame
    await UniTask.Yield();

    // Load scene async
    await SceneManager.LoadSceneAsync("Level2");

    // Run on main thread (from background task)
    await UniTask.SwitchToMainThread();
}
```

### Native Task (Unity 2022.2+ / Unity 6)

```csharp
using System.Threading.Tasks;

async void Start()
{
    await Task.Delay(2000);
    // Caution: Task.Delay uses thread pool, returns on different thread
    // Most Unity API calls require main thread
}
```

### Coroutine vs async/await

| | Coroutine | async/await |
|---|---|---|
| **Return value** | ❌ No | ✅ Yes (`async Task<int>`) |
| **Exception handling** | ❌ Try/catch doesn't work across `yield` | ✅ Full try/catch support |
| **GC allocation** | Moderate | Minimal (UniTask) |
| **Main thread guarantee** | ✅ Always | ⚠️ Must manually switch back |
| **Error on destroy** | ❌ Silent stop | ⚠️ Silent stop (fix with CancellationToken, see below) |
| **Use for** | Simple sequences | Complex async logic, value returns |

### Cancellation

When an object is destroyed, async operations should clean up:

```csharp
CancellationTokenSource cts = new CancellationTokenSource();

async UniTaskVoid DoWork(CancellationToken token)
{
    await UniTask.Delay(5000, cancellationToken: token);
    // Won't execute if cancelled
}

void OnDestroy()
{
    cts.Cancel();
    cts.Dispose();
}
```

---

## Performance Best Practices

### Memory / GC

- Avoid `GetComponent<T>()` in Update() — cache in Awake()
- Avoid `GameObject.Find()` / `FindObjectOfType()` — use serialized references or dependency injection
- Avoid `new` in Update() — allocate upfront and reuse
- Use `StringBuilder` for frequent string concatenation
- Use structs carefully — boxing allocates

### Rendering Performance

- Use GPU Instancing or SRP Batcher for repeated meshes
- Limit real-time lights, use baked lighting when possible
- Use LOD groups for distant objects
- Occlusion culling for complex indoor scenes
- Profile with Profiler window, not guesswork

### Physics Performance

- Use primitive colliders over MeshCollider
- Set Rigidbody to kinematic when physics response is not needed
- Keep Fixed Timestep at 0.02s (50 Hz) for most projects. Only lower for high-precision physics simulations. Do NOT tie to display framerate.
- Disable collision between layers that don't interact

## Additional References

- `references/urp-2022.md` — URP specifics for 2022.3 LTS
- `references/urp-unity6.md` — URP specifics for Unity 6

---

## Common Anti-Patterns

### Physics & Movement

```csharp
// ❌ Direct transform.position on Rigidbody — bypasses physics engine
transform.position += Vector3.forward * speed * Time.deltaTime;

// ❌ rb.position for continuous movement — teleports, no velocity transfer
rb.position = newPosition;

// ✅ Use velocity (FixedUpdate)
rb.velocity = new Vector3(input.x * speed, rb.velocity.y, input.y * speed);

// ✅ Kinematic: MovePosition in FixedUpdate
rb.MovePosition(rb.position + moveDir * speed * Time.fixedDeltaTime);
```

### Unity API Misuse

```csharp
// ❌ FindObjectOfType / GameObject.Find in Update — O(n) every frame
// ❌ GetComponent<T>() in Update — cache in Awake
// ❌ CompareTag(string) in Update — use CompareTag() (no GC) or cached bool
// ❌ string comparison for state — use enum or hash code
// ❌ LINQ in Update — allocates GC, use foreach or for loop

// ✅ Cache references
Rigidbody rb;
void Awake() { rb = GetComponent<Rigidbody>(); }

// ✅ Pre-cached tag comparison
bool IsPlayer(Collider other) => other.CompareTag("Player");

// LINQ only in editor scripts or one-time init (prefer Addressables for runtime asset loading)
void SetupWeapons() { weapons = Resources.LoadAll<WeaponData>("Weapons").ToList(); }
```

### Event Leaks

```csharp
// ❌ Subscribe without unsubscribe — memory leak, null ref after destroy
void OnEnable() { otherHealth.OnDeath += HandleDeath; }
// Missing: void OnDisable() { otherHealth.OnDeath -= HandleDeath; }

// ✅ Always pair subscribe + unsubscribe
void OnEnable()  { button.onClick.AddListener(HandleClick); }
void OnDisable() { button.onClick.RemoveListener(HandleClick); }
```

### GC Allocation Hotspots

| Pattern | GC Alloc | Fix |
|---|---|---|
| `new WaitForSeconds(1f)` every frame | High | Cache: `WaitForSeconds wait = new(1f);` |
| `string + string` in loop | High | Use `StringBuilder` |
| `foreach` over non-generic | Med | Prefer `for` or `List<T>.GetEnumerator` |
| Boxing value types | High | Avoid casting structs to `object`/interface |
| Anonymous methods | Med | Cache delegate if reused |

## Game Architecture Patterns

### Finite State Machine

Use enum-based state machines for character/entity behaviour:

```csharp
public enum PlayerState { Idle, Moving, Jumping, Attacking, Dead }

PlayerState currentState;

void Update()
{
    switch (currentState)
    {
        case PlayerState.Idle:     IdleUpdate(); break;
        case PlayerState.Moving:   MoveUpdate(); break;
        case PlayerState.Jumping:  JumpUpdate(); break;
        case PlayerState.Attacking: AttackUpdate(); break;
        case PlayerState.Dead:     return; // no updates when dead
    }
}

void ChangeState(PlayerState newState)
{
    ExitState(currentState);
    currentState = newState;
    EnterState(newState);
}

void ExitState(PlayerState state)
{
    switch (state)
    {
        case PlayerState.Attacking:
            weaponCollider.enabled = false;
            break;
    }
}
```

For complex FSMs, use `Animator` as a state machine backbone (parameter-driven transitions).

### Strategy Pattern (via Interface)

```csharp
public interface IMovementStrategy
{
    void Move(Rigidbody rb, Vector2 input);
}

public class WalkMovement : IMovementStrategy
{
    public void Move(Rigidbody rb, Vector2 input)
    {
        rb.velocity = new Vector3(input.x * 5f, rb.velocity.y, input.y * 5f);
    }
}

public class FlyMovement : IMovementStrategy
{
    public void Move(Rigidbody rb, Vector2 input)
    {
        rb.velocity = input * 8f; // full 3D movement
    }
}

// Usage: Swap movement mode at runtime
IMovementStrategy movement = new WalkMovement();
movement = new FlyMovement(); // power-up changes behaviour
```

### Observer via ScriptableObject Event Channel

See §ScriptableObject → ScriptableObject as Event Channel for the full pattern with `IntEventSO`, `PlayerHealth`, and `HealthBarUI` examples. The same decoupling pattern applies to any event-driven architecture.

## Input System Advanced

### Action Map Switching

```csharp
using UnityEngine.InputSystem;

PlayerInput playerInput;

void Start()
{
    playerInput = GetComponent<PlayerInput>();
    playerInput.SwitchCurrentActionMap("UI"); // switch to UI controls
    playerInput.SwitchCurrentActionMap("Gameplay"); // switch back
}

// Multiple control schemes per action map:
// Edit InputAction asset → Control Schemes → add Keyboard&Mouse, Gamepad, Touch
// PlayerInput auto-switches scheme based on active device
```

### Runtime Rebinding

```csharp
using UnityEngine.InputSystem;

InputAction moveAction;

void StartRebind()
{
    moveAction.PerformInteractiveRebinding()
        .WithControlsExcluding("Mouse") // don't rebind mouse
        .OnMatchWaitForAnother(0.1f)    // wait for combo inputs
        .OnComplete(op => {
            Debug.Log($"Rebound to: {op.selectedControl}");
            SaveBindingOverride(moveAction);
            op.Dispose();
        })
        .Start();
}

void SaveBindingOverride(InputAction action)
{
    var rebinds = action.actionMap.SaveBindingOverridesAsJson();
    PlayerPrefs.SetString("rebinds", rebinds);
}

void LoadBindingOverrides()
{
    var rebinds = PlayerPrefs.GetString("rebinds");
    moveAction.actionMap.LoadBindingOverridesFromJson(rebinds);
}
```

### Touch Input

```csharp
// Direct device access
Touchscreen touch = Touchscreen.current;
if (touch != null && touch.primaryTouch.press.isPressed)
{
    Vector2 touchPos = touch.primaryTouch.position.ReadValue();
    Ray ray = Camera.main.ScreenPointToRay(touchPos);
    if (Physics.Raycast(ray, out RaycastHit hit))
        HandleTouch(hit.point);
}

// Enhanced Input touch bindings:
// Bind Touchscreen's Primary Touch/Position to a Vector2 action
// Tap/gesture detection via Input Actions' Interactions (Tap, Hold, MultiTap)
```

## Shader Graph Basics

### Creating a Shader

1. **Create**: Assets → Create → Shader Graph → URP → Lit Shader Graph (or Unlit, Sprite Lit, Decal)
2. **Open**: Double-click → Shader Graph editor opens
3. **Core nodes**: Add node (Spacebar) → type name
4. **Save**: Shader auto-updates in scene

### Common Node Reference

| Node | Purpose |
|---|---|
| **Sample Texture 2D** | Sample a texture at UV coordinates |
| **Color** | Constant RGBA color output (HDR-compatible in Unity 6) |
| **Add / Multiply / Lerp** | Math on color/float/vector values |
| **Fresnel Effect** | Edge glow, rim lighting |
| **Time** | Animated shader values (scrolling, pulsing) |
| **Normal From Height** | Bump from heightmap |
| **Scene Color** | Sample what's behind this object (transparency, distortion) |
| **Vertex Color** | Mesh vertex color input |
| **Position (Object/World)** | Object world/relative position |

### Key Material Properties

```hlsl
// Expose parameters to Inspector — drag to Blackboard
// Float, Vector2/3/4, Color, Texture2D, Cubemap

// URP include for light access in custom nodes:
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
Light mainLight = GetMainLight();
half3 lightDir = mainLight.direction;
half3 lightColor = mainLight.color;
```

### Common Shader Graph Effects

| Effect | Nodes |
|---|---|
| Dissolve | `Simple Noise` → `Step` → `Alpha Clip Threshold` |
| Outline (inverted hull) | Vertex Position offset along normal, separate pass |
| Ripple (UV distortion) | `Time` + `Sine` → Add to UV → `Sample Texture 2D` |
| Fresnel glow | `Fresnel Effect` → `Multiply` with `Color` → `Emission` |
| Toon/Cel shading | `Step` on `Dot(Normal, LightDir)` for hard light falloff |

## Mobile Optimization

### Unity 2022.3 / Unity 6 Mobile Checklist

| Setting | Recommendation | Where |
|---|---|---|
| Graphics API | OpenGL ES 3.2 (broad compat) or Vulkan (newer devices) | Player Settings → Other Settings |
| Color Space | Linear (HDR rendering) | Player Settings → Other Settings |
| Texture compression | ASTC (Android), PVRTC (iOS) | Per-texture override |
| Shadow quality | Low to Medium | Quality Settings → Shadows |
| Anti-aliasing | FXAA (cheap) or off | URP Asset → Anti-aliasing |
| Maximum LOD level | Set per-platform LOD bias | Quality Settings → LOD Bias |
| VSync | On for mobile (battery), off for benchmarks | Quality Settings |
| Target framerate | 30fps default, 60fps optional | `Application.targetFrameRate = 60;` |
| Strip engine code | Enable | Player Settings → Strip Engine Code |

```csharp
// Runtime platform check
#if UNITY_ANDROID
    QualitySettings.vSyncCount = 1;
    Application.targetFrameRate = 30;
#elif UNITY_IOS
    QualitySettings.vSyncCount = 0;
    Application.targetFrameRate = 60;
#endif

// Detect device capability
if (SystemInfo.supportsComputeShaders)
    EnableAdvancedEffects();

// Memory warning callback
void Start() {
    Application.lowMemory += OnLowMemory;
}
void OnLowMemory() {
    Resources.UnloadUnusedAssets();
    textureQuality = 0; // reduce texture quality
}
```

### Mobile-Specific Pitfalls

- **Overdraw**: Transparent UI/particles kill mobile GPU. Use Frame Debugger → check overdraw.
- **Memory**: 1-2GB budget. Profile with Memory Profiler package.
- **Battery**: VSync on limits unnecessary frames. Avoid `while(true)` or unbounded Update.
- **Touch vs mouse**: Use `Input.touchSupported` to switch between touch/mouse paths.
- **Notch/Cutout**: Use `Screen.safeArea` to constrain UI to non-obscured screen regions.

---

---

## Profiling & Debugging

### Profiler Window

**Window → Analysis → Profiler** or `Ctrl+7`. Records CPU/GPU/memory/audio usage per frame:

| Module | Shows |
|---|---|
| **CPU Usage** | Scripts, physics, rendering — sorted by time cost |
| **GPU Usage** | Draw calls, shader passes, screen effects |
| **Memory** | Textures, meshes, audio, GC allocations |
| **Rendering** | Batches, set passes, VBO uploads |
| **Audio** | Audio clip playback, mixers, voices |

**Workflow:**
1. Click Record (red circle) → run the scene → stop recording
2. Click on CPU spikes to inspect per-frame script calls
3. Deep Profile: enable **Deep Profile** in Build Settings to see per-method timing (slower, development only)

### Frame Debugger

**Window → Analysis → Frame Debugger**. Captures a single frame's draw call sequence:

```
Draw Call #1: Skybox
Draw Call #2: Background meshes (StaticBatching)
Draw Call #3: Character_SK (SkinnedMeshRenderer)
Draw Call #4: UIPanel (Canvas)
...
```

**Use for:**
- Finding unnecessary draw calls (overdraw)
- Checking batching (static/dynamic/GUI)
- Verifying shader variants per object
- Spotting hidden objects still rendering (Check `isVisible`)

### Common Commands

```
Stats window → toggle real-time performance overlay
Profiler → CPU Usage → search by MonoBehaviour name
Frame Debugger → click draw call → highlights object in Scene View
```

## Maintaining This Skill

Update this skill when:
- User reports a recurring bug pattern → add to relevant section
- User discovers a non-obvious Unity behaviour → document
- User switches Unity versions with breaking changes → update version notes
- New Unity feature becomes part of user's workflow → add section
