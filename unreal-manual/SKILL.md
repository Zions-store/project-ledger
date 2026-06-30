---
name: unreal-manual
version: 2.2.0
description: Unreal Engine core concepts and best practices. Use when the user mentions Unreal Engine, UE5, Actor, Pawn, Character, GameMode, Blueprint, UMG, Enhanced Input, Chaos, Nanite, Lumen, UPROPERTY, UFUNCTION, replication, RPC, GameInstance, Niagara, Line Trace, Timer, Event Dispatcher, Blueprint Interface, module, FString, FName, FText, DataTable, GameplayTag, Subsystem, SaveGame, Timeline, Timeline Editor, Soft Reference, Packaging, Build.cs, IMPLEMENT_MODULE, Public/Private folder, UObject, or is working on Unreal Engine game development tasks.
compatibility: ue-5.0, ue-5.5, ue-5.8
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Unreal Engine Manual

Covers UE core concepts, architecture, and best practices. See frontmatter `compatibility` field for supported engine versions.

## When to Use This Skill

Use when the user asks about UE development — creating game logic, designing levels, Blueprint/C++ decisions, debugging, networking, or understanding engine behavior. Also use when a Unity-to-UE transition question arises (see Appendix).

## Editor UI Basics

UE's editor is organized into collapsible, dockable panels. The core four:

| Panel | Purpose |
|---|---|
| **Viewport** | Interactive 3D scene view. Click to select, drag to move. |
| **World Outliner** (right side) | Hierarchical list of all Actors in all loaded levels. Double-click to focus camera on an Actor. |
| **Details Panel** (bottom right) | Shows properties of the currently selected Actor. Edit Location/Rotation/Scale, components, materials here. |
| **Content Browser** (bottom) | Your project's asset files. Drag-and-drop assets into the viewport to place them. |

**Viewport navigation:**

| Action | Keys |
|---|---|
| Orbit camera | Hold **Right Mouse Button** + move mouse |
| Pan (slide view) | Hold **Middle Mouse Button** + move mouse |
| Zoom | **Scroll wheel** or hold RMB + scroll wheel |
| Focus on selected Actor | Press **F** |
| Fly-through mode | Hold **RMB** + **W/A/S/D** (hold Shift to speed up) |
| Snap to floor | Select Actor → press **End** |
| Bookmark camera position | **Ctrl + 1~9** to save, **1~9** to recall |

**Transform modes** (same as Unity):

| Key | Mode |
|---|---|
| **W** | Move (translate) |
| **E** | Rotate |
| **R** | Scale |
| **Space** | Toggle world/local coordinate gizmo |
| **End** | Snap object to floor/surface |

**PIE (Play In Editor):** Click the **Play** button in toolbar. Three modes: Play (fullscreen), VR Preview, Simulate (run logic without possessing a player).

## Coordinate System & Units

UE uses a **left-handed coordinate system, Z-up** (Unity uses left-handed, Y-up):

| Axis | UE | Unity |
|---|---|---|
| Forward | **+X** | +Z |
| Right | **+Y** | +X |
| Up | **+Z** | +Y |
| Unit | **Centimeters** (1 unit = 1 cm) | **Meters** (1 unit = 1 m) |

A 180 cm character = 180 UE units tall (same character is 1.8 in Unity).

**Importing models:** Maya/Max export with Y-up → enable "Convert Scene" on import. Blender's FBX exporter auto-converts. FBX import scale is typically 1.0 (cm), but always verify in the import dialog's "Transform" section.

Rotation order: UE uses **X→Y→Z** (Roll→Pitch→Yaw). Yaw = Z rotation.

## Project Setup

### Creating a New Project

In Epic Games Launcher → **Unreal Engine** tab → **Launch** → pick your engine version → **New Project**. Template selection:

| Template | What You Get |
|---|---|
| Blank | Empty project, no starter content |
| First Person | FPS character + level + Enhanced Input |
| Third Person | TPS character + level + Enhanced Input |
| Top Down | Top-down camera + click-to-move |
| Vehicle | Driveable vehicle + physics |
| Handheld AR | AR mobile template |

Enable **Starter Content** for a library of basic props/materials/textures.

### Engine Association

The `.uproject` file links to a specific engine version:

```json
"EngineAssociation": "5.4"     // Launcher-installed version
"EngineAssociation": "{GUID}"  // Custom/source-built engine
```

- Double-click `.uproject` → opens in associated engine
- Right-click `.uproject` → **Switch Unreal Engine Version** → choose another installed version
- Upgrading between versions: UE auto-converts the project, but **always back up first**

### Project Migration

Move a project to another machine: copy the entire project folder. Delete `Intermediate/`, `Saved/`, and `DerivedDataCache/` before copying to save space — UE regenerates them.

### Editor Preferences

Key settings for Unity switchers:

| Setting | Location | Recommendation |
|---|---|---|
| Invert Middle Mouse Pan | Editor Preferences → Level Editor → Viewports | Enable for Unity-like pan |
| Editor Language | Editor Preferences → Region & Language | Set to English if preferred |
| Source Code Editor | Editor Preferences → Source Code | VS 2022 (default) or Rider |

---

## Actor / Component Architecture

Every object in the game world is an **Actor**. An Actor itself does nothing — it's a container for **Components**.

### Core Principles

- **Actor** = spatial identity (transform, lifespan, network role) + a list of Components
- **Component** = reusable behaviour module (mesh, collision, audio, movement, custom logic)
- **RootComponent** = the one Component that defines the Actor's transform in the world
- Actors normally have a RootComponent — without one, the Actor has no world position
- Components attach in a tree: child Components move relative to their parent

### The Actor Hierarchy

```
UObject              ← garbage-collected base (everything is a UObject)
  UActorComponent    ← non-spatial component (movement, abilities)
    USceneComponent  ← has a transform, can be attached in a tree
      UPrimitiveComponent ← renders or collides (StaticMesh, SkeletalMesh, Shape)
  AActor             ← exists in the level, contains Components
    APawn            ← can be possessed by a Controller (player or AI)
      ACharacter     ← Pawn + capsule collision + movement + skeleton
```

### Common Patterns

**C++:**
```cpp
// Spawn an actor into the world
AActor* NewActor = GetWorld()->SpawnActor<AMyActor>(SpawnClass, Location, Rotation);

// Find a component on this actor
UStaticMeshComponent* Mesh = FindComponentByClass<UStaticMeshComponent>();

// Get first actor of a class in the level (avoid in performance code)
AMyActor* Found = Cast<AMyActor>(UGameplayStatics::GetActorOfClass(GetWorld(), AMyActor::StaticClass()));

// Get the player's pawn
APawn* PlayerPawn = UGameplayStatics::GetPlayerPawn(GetWorld(), 0);
```

**Blueprint:** Right-click in Event Graph → search `Spawn Actor From Class` → select class.

### Key Rules

- **Never** use `new` to create UObjects or Actors — use `NewObject<T>()` or `SpawnActor<T>()`
- Destroy with `Actor->Destroy()` — the garbage collector handles UObject cleanup
- To disable an Actor: `SetActorHiddenInGame(true)` + `SetActorEnableCollision(false)` — or destroy it
- To disable a Component: `Component->SetActive(false)` (stops Tick + rendering + collision)
- An Actor with no RootComponent has no world position — always provide one

---

## Game Framework Classes

UE provides a structured game framework. Understanding these classes is essential before writing any logic.

### Framework Overview

| Class | Owner | Role |
|---|---|---|
| **GameMode** | Server only | Rules of the game (scoring, win conditions, spawning). Exists only on server. |
| **GameState** | Replicated to all | Game-wide state visible to all players (score, match timer, team data) |
| **PlayerController** | Each player | Translates input into actions. Owns the camera. Owns the HUD. |
| **PlayerState** | Replicated to all | Per-player state (name, score, ping). Survives player respawn. |
| **Pawn** | Controller | Physical avatar in the world. Can be possessed/unpossessed. |
| **Character** | Controller | Specialized Pawn with CapsuleComponent + CharacterMovement + SkeletalMesh |
| **HUD** | PlayerController | Legacy on-screen display. UMG Widgets preferred in modern UE5. |
| **GameInstance** | Persistent | Created on game start, destroyed on quit. Survives level transitions. |

### Data Flow

```
GameInstance (persistent)
  └─ GameMode (server only, per level)
       └─ GameState (replicated to all, per level)
            ├─ PlayerState A (replicated, per player)
            └─ PlayerState B (replicated, per player)
                 ├─ PlayerController A (per player, owns camera)
                 │    └─ Pawn A (possessed)
                 └─ PlayerController B (per player)
                      └─ Pawn B (possessed)
```

### Setting Default Classes

In **Project Settings → Maps & Modes**:
- Default GameMode → your custom GameMode
- Default Pawn Class → your custom Pawn/Character
- Default PlayerController → your custom PlayerController

Or in `Config/DefaultEngine.ini`:
```ini
[/Script/EngineSettings.GameMapsSettings]
GameDefaultMap=/Game/Maps/MainLevel
GlobalDefaultGameMode=/Game/Blueprints/BP_MyGameMode.BP_MyGameMode_C
```

### Common Pitfall

GameMode exists ONLY on the server. Never access GameMode from client code — use GameState instead (replicated to clients).

---

## Lifecycle: Actor Initialization

### Execution Order (simplified)

1. **Constructor** (C++ only) — set default property values. No world access, no gameplay logic.
2. **PostInitializeComponents()** — all Components created. Can reference own Components here.
3. **BeginPlay()** — called once when game starts (or actor is spawned). Safe for gameplay logic.
4. **Tick(float DeltaTime)** — called every frame (if enabled). DeltaTime varies, don't assume fixed timestep.
5. **EndPlay()** — called when destroyed or level unloads. Cleanup here.

### C++ Example
```cpp
AMyActor::AMyActor()
{
    // Constructor: set defaults only
    PrimaryActorTick.bCanEverTick = true;
    Strength = 100.0f;
}

void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    // Safe for gameplay initialization
    if (UWorld* World = GetWorld())
    {
        // World exists, safe to use
    }
}

void AMyActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    // Per-frame logic. DeltaTime varies.
}
```

**Blueprint:** Event Graph → right-click → `Event BeginPlay` / `Event Tick` nodes.

### Common Pitfalls

- Accessing `GetWorld()` in constructor → **nullptr**. Use `BeginPlay()` or `PostInitializeComponents()`.
- Heavy work in `Tick()` → drags framerate. Enable/disable `PrimaryActorTick.bCanEverTick` per Actor.
- `BeginPlay()` runs on both server and clients (for replicated actors). Be careful with authority checks.
- Forgetting `Super::BeginPlay()` in C++ → parent class init is skipped.

### CDO Constructor & Asset Loading

`ConstructorHelpers::FObjectFinder` in the CDO constructor can silently fail in UE5 with World Partition active. Asset registry may not be fully initialized during CDO construction.

**Recommended fix (in order of preference):**
1. **Blueprint subclass** — `UCLASS(abstract)`, create BP child, set assets in Class Defaults
2. **BeginPlay fallback** — `LoadObject<T>(nullptr, TEXT("/Game/Path/To/Asset.Asset"))` if member is null
3. **StaticLoadObject** — `Cast<T>(StaticLoadObject(T::StaticClass(), nullptr, TEXT("/Game/...")))`

Applies to: `USkeletalMesh`, `UAnimMontage`, `UInputAction`, `UInputMappingContext`.

**After full rebuild:** Blueprint CDO may retain old serialized values overriding new C++ defaults. Check BP Class Defaults for critical properties (`MaxHP`, damage values, etc.).

### Hot Reload vs Full Rebuild

| Change | Action |
|---|---|
| Modify existing function body (.cpp) | Ctrl+Alt+F11 (Live Coding) |
| Add new UFUNCTION/UCLASS declaration | Full rebuild |
| Modify Build.cs dependencies | Full rebuild |
| Change BlueprintImplementableEvent | Live Coding (BP side implements) |

**Rebuild steps:** Close editor → delete `Binaries/` + `Intermediate/` → Generate VS files → reopen.

---

## C++ vs Blueprint

UE gives you two ways to build logic. Both are valid. Most commercial projects use both.

### When to Use C++
- Complex math, algorithms, heavy computation
- Low-level systems (custom movement, networking optimization)
- Data structures, asset processing
- Anything that runs every frame on many objects
- Plugin or engine modification

### When to Use Blueprint
- Event-driven logic (on overlap, on damage, on interact)
- UI binding, animation graphs, audio logic
- Rapid prototyping and iteration
- Level-specific scripting (doors, triggers, pickups)
- Simple game rules, cosmetics, VFX

### How They Work Together

UE's reflection system binds C++ to Blueprint:

```cpp
// C++ side: expose this class to Blueprint
UCLASS(Blueprintable)        // BP can inherit from this
class AMyCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Health;             // BP can read/write

    UFUNCTION(BlueprintCallable)
    void TakeDamage(float Amount);  // BP can call this
};
```

Then in Blueprint, create a child of `AMyCharacter`, override events, and call C++ functions.

### Key Principle

**C++ = foundation. Blueprint = skin.** Write performance-critical systems in C++, expose knobs to Blueprint for designers to tweak.

## Blueprint Fundamentals

Blueprints are visual scripts — no C++ required. Every Blueprint has two main tabs:

| Tab | Purpose |
|---|---|
| **Event Graph** | Gameplay logic: events, function calls, branching, loops. Runs at runtime. |
| **Construction Script** | Runs once when the Actor is placed/edited in the level. Use for setting up mesh variants, material parameters, procedural generation at edit time. |

### Common Node Types

| Node Type | Appearance | What It Does |
|---|---|---|
| **Event** | Red title bar | Entry point. `Event BeginPlay`, `Event Tick`, `Event ActorBeginOverlap`. |
| **Function Call** | Blue title bar | Calls a C++ or Blueprint function. Has input/output pins. |
| **Pure Function** | Green title bar (no exec pins) | Reads data, no side effects. Evaluated on demand when its output is wired. |
| **Variable Get/Set** | Colored circle pins | Read or write a variable. |
| **Branch** | Diamond shape | If/else. |
| **ForLoop** | Loop body frame | Iterate N times. |
| **Delay** | Clock icon | Wait N seconds, then continue execution (latent — pauses the flow). |
| **Sequence** | Numbered outputs | Execute multiple output chains in order. |

### Variables in Blueprint

- **Create** by clicking `+` in the MyBlueprint panel (left sidebar)
- **Types**: Boolean, Integer, Float, Vector, Rotator, Actor/Object references, etc.
- **Instance Editable** checkbox → variable appears in Details panel, tweakable per Actor instance
- **Expose on Spawn** → value is set when you use `Spawn Actor From Class`
- **Tooltip field** → shows description on hover, good for designer documentation

### Macros vs Functions vs Custom Events

| | Macro | Function | Custom Event |
|---|---|---|---|
| **Where defined** | Macro Library or same BP | BP or C++ base class | Event Graph |
| **Can use Delay?** | ❌ No | ❌ No | ✅ Yes |
| **Can have return value?** | ✅ Multiple output pins | ✅ One return value | ❌ No |
| **Execution cost** | Inlined (copied) at compile | Function call overhead | Lightweight dispatch |
| **Use for** | Reusable node groups (like a template) | Computation, getter/setter logic | Async notification, event dispatch |

## Blueprint Communication

How Blueprints talk to each other. Four patterns, increasing complexity:

### 1. Direct Reference (simplest)

Drag one Actor into another's Details panel or expose a variable:
```
UPROPERTY(EditInstanceOnly)  // pick target in the level editor
AActor* TargetActor;
```
Then call functions on `TargetActor` directly. Works only when both Actors are in the same level.

### 2. Casting

When you have a generic reference (Actor/ActorComponent) but need a specific class:

```
On Begin Overlap → Other Actor → Cast to BP_Enemy → If valid → Call TakeDamage
```

Casting is necessary but expensive in BP — cache the cast result. On Tick, avoid casting every frame.

### 3. Event Dispatcher (Observer pattern)

One Blueprint broadcasts an event; others listen and react. Decouples sender from receiver.

**Setup:**
1. In sender BP → MyBlueprint panel → `Event Dispatchers` → `+` → name it (e.g., `OnPlayerDied`)
2. Drag a `Call OnPlayerDied` node onto the Event Graph where the event should fire
3. In receiver BP → find sender → Details → Events → `OnPlayerDied` → click `+` → auto-creates Bind node
4. Wire Bind node Event pin to a Custom Event in receiver

**C++ equivalent:** `DECLARE_DYNAMIC_MULTICAST_DELEGATE`

### 4. Blueprint Interface

Define a contract that any Blueprint can implement. Useful when different classes need to respond to the same message (human, AI, destructible object all respond to `TakeDamage`).

**Setup:**
1. Content Browser → right-click → Blueprints → **Blueprint Interface** → name it (e.g., `BPI_Damageable`)
2. Add function: `OnTakeDamage(float Amount)` — only input/output pins, no implementation body
3. In each Blueprint that should be "damageable": **Class Settings → Implemented Interfaces → Add** → pick your interface
4. In Event Graph, right-click → `Event OnTakeDamage` appears → wire your response logic
5. Caller: `BPI_Damageable → OnTakeDamage(Target, 50.0)` — works on ANY actor that implements the interface

### Communication Cheat Sheet

| Need | Use |
|---|---|
| Two known objects in same level | Direct reference |
| Generic reference → specific class | Cast (cache it) |
| Notify many listeners of an event | Event Dispatcher |
| Different classes, same behavior | Blueprint Interface |

---

## UE Modules (C++ Code Organization)

Modules are the primary way to organize C++ code in UE — equivalent to Unity's namespace + Assembly Definition. Each module is a self-contained compilation unit with its own dependencies, visibility rules, and loading behavior.

### Module Structure

A typical module directory under `Source/`:

```
Source/MyModule/
├── Public/                    ← headers exposed to other modules
│   └── MyActor.h
├── Private/                   ← implementation + headers internal to this module
│   ├── MyActor.cpp
│   └── MyModuleModule.cpp     ← module registration
└── MyModule.Build.cs          ← dependencies and build config
```

### .Build.cs — Dependency Declaration

Every module needs a `.Build.cs` file that declares its dependencies:

```csharp
// Source/MyModule/MyModule.Build.cs
using UnrealBuildTool;

public class MyModule : ModuleRules
{
    public MyModule(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        // Modules used in public headers — also exposed to modules that depend on you
        PublicDependencyModuleNames.AddRange(new string[] {
            "Core",
            "CoreUObject",
            "Engine"
        });

        // Modules used only in .cpp files — not exposed externally
        PrivateDependencyModuleNames.AddRange(new string[] {
            "Slate",
            "SlateCore",
            "EnhancedInput"
        });
    }
}
```

**Prefer PrivateDependencyModuleNames** whenever possible — it reduces compile times and enforces cleaner boundaries.

### Public vs Private Folders

| Folder | Visibility | What to put there |
|---|---|---|
| **Public/** | Accessible to any module that depends on yours | Headers for classes that other modules need to use |
| **Private/** | Only accessible within your module | .cpp files, internal headers, implementation details |

These are NOT related to the C++ `public`/`private` keywords — they control **cross-module** header visibility at build time.

### IMPLEMENT_MODULE — Registration

Every module needs a registration file (`Private/MyModuleModule.cpp`):

```cpp
#include "Modules/ModuleManager.h"

IMPLEMENT_MODULE(FDefaultModuleImpl, MyModule);
```

For modules that need startup/shutdown logic, implement `IModuleInterface`:

```cpp
#include "Modules/ModuleManager.h"

class FMyModule : public IModuleInterface
{
public:
    virtual void StartupModule() override
    {
        // Called when the module loads — register settings, bind delegates
    }

    virtual void ShutdownModule() override
    {
        // Called when the module unloads — cleanup
    }
};

IMPLEMENT_MODULE(FMyModule, MyModule);
```

### Module Configuration in .uproject

Define modules in your `.uproject` file:

```json
"Modules": [
    {
        "Name": "MyModule",
        "Type": "Runtime",
        "LoadingPhase": "Default"
    }
]
```

| Setting | Values | Purpose |
|---|---|---|
| **Type** | `Runtime`, `Editor`, `Developer`, `Program` | Where the module is available |
| **LoadingPhase** | `Default`, `PreDefault`, `PostConfigInit`, `PostEngineInit` | When the module loads |

Editor-only modules (tools, custom inspectors, editor extensions) use `Type: "Editor"` — they won't be included in packaged builds.

### API Export Macros

When a class in your module needs to be used by another module, mark it with your module's API macro:

```cpp
// In MyModule/Public/MyActor.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"

class MYMODULE_API AMyActor : public AActor  // ← MYMODULE_API exports this class
{
    GENERATED_BODY()
};
```

Standard engine module API macros:

| Macro | Module |
|---|---|
| `CORE_API` | Core |
| `COREUOBJECT_API` | CoreUObject |
| `ENGINE_API` | Engine |
| `SLATE_API` | Slate |
| `UMG_API` | UMG |
| `AIMODULE_API` | AIModule |

Without the API macro, the class/function is invisible outside your module (linker error).

### UE's Use of C++ Namespaces

UE traditionally avoided C++ namespaces. Since UE 5.0+, they are gradually being adopted:

```cpp
// Modern UE (5.0+)
namespace UE::Math { /* math types */ }
namespace UE::Core { /* core utilities */ }
namespace UE::Online { /* online services */ }

// Usage
UE::Math::FVector Location;
```

However, **modules remain the primary organization unit**. Namespaces supplement modules but don't replace them. Most gameplay code still uses global scope with F/U/A/I prefixes (see below).

### Type Prefix Convention

UE uses letter prefixes as a naming convention (not enforced by the compiler, but critical for readability):

| Prefix | Base Class | Examples |
|---|---|---|
| **F** | Plain struct/value type | `FVector`, `FString`, `FName`, `FTransform` |
| **U** | UObject and derivatives | `UObject`, `UActorComponent`, `UTexture`, `UDataAsset` |
| **A** | AActor and derivatives | `AActor`, `ACharacter`, `APawn`, `AGameModeBase` |
| **I** | Interface classes | `IInputDevice`, `ITargetPlatform` |
| **E** | Enums | `ECollisionChannel`, `EMovementMode` |
| **T** | Template/container classes | `TArray`, `TMap`, `TSharedPtr` |
| **S** | Slate widget classes | `SButton`, `STextBlock` |

These prefixes serve a pseudo-namespace role — you can immediately identify the base class of any type by its first letter.

### Module System Cheat Sheet

| Unity | Unreal |
|---|---|
| `namespace MyGame { }` | Module directory + `.Build.cs` |
| Assembly Definition | Module + dependency graph |
| `using` | `PublicDependencyModuleNames` / `PrivateDependencyModuleNames` |
| `internal` class | `Private/` folder |
| `public` class in assembly | `Public/` folder + API macro |
| Editor-only assembly | `Type: "Editor"` module |

---

## The Reflection System: UPROPERTY / UFUNCTION

UE's C++ is augmented by a pre-processor that generates reflection data. The macros `UCLASS`, `UPROPERTY`, and `UFUNCTION` are **not** standard C++ — they drive UE's serialization, editor integration, garbage collection, and networking.

### UPROPERTY Specifiers

```cpp
UPROPERTY(EditAnywhere)          // Show in editor details panel, editable
UPROPERTY(BlueprintReadWrite)    // BP can get/set
UPROPERTY(VisibleAnywhere)       // Show in editor but read-only
UPROPERTY(Replicated)            // Syncs from server to clients
UPROPERTY(ReplicatedUsing=OnRep_Health)  // Call OnRep_Health() on clients when changed
UPROPERTY(SaveGame)              // Serialized into save files
```

### UFUNCTION Specifiers

```cpp
UFUNCTION(BlueprintCallable)       // BP can call this function
UFUNCTION(BlueprintImplementableEvent)  // BP writes the body, C++ calls it
UFUNCTION(BlueprintNativeEvent)    // C++ default body, BP can override
UFUNCTION(Server, Reliable)        // Called from client, executes on server (RPC)
UFUNCTION(Client, Reliable)        // Called from server, executes on client
UFUNCTION(NetMulticast, Reliable)  // Called from server, executes everywhere
```

### Common Pitfall

GENERATED_BODY() must be the first line inside the class body. Forgetting it causes compile errors.

### FString vs FName vs FText

UE has three string types with distinct purposes. Using the wrong one causes bugs:

| Type | Purpose | Internal | When to use |
|---|---|---|---|
| **FString** | General-purpose mutable string | Heap-allocated, UTF-16 | File paths, debug output, dynamic concatenation. Heavy — avoid in hot loops. |
| **FName** | Immutable interned identifier | Hashed, single-entry-per-string table | Asset names, tags, gameplay identifiers. Fast comparison (`==` is O(1)). Use for anything that acts as a "key". |
| **FText** | Localized display text | Key+table lookup for translations | UI text, dialogue, anything the player sees. Never use FString for visible text — it breaks localization. |

```cpp
// FString — general purpose
FString Path = TEXT("/Game/Maps/Level1");
FString Joined = FString::Printf(TEXT("Health: %d"), Health);

// FName — identifiers (fast comparison)
FName EnemyTag = FName(TEXT("Enemy"));
if (Actor->ActorHasTag(EnemyTag)) { /* O(1) comparison */ }

// FText — localized UI text
FText DisplayName = NSLOCTEXT("MyGame", "StartButton", "Start");
// NSLOCTEXT( namespace, key, default )
```

**Conversions:**
```cpp
FString FromName = Name.ToString();
FString FromText = Text.ToString();  // loses localization info
FName FromString = FName(*String);
FText FromString = FText::FromString(String);
```

**Blueprint:** Blueprint strings are all `FString` under the hood. Use the `ToText` node for UI display.

### Common Pitfalls

- ❌ `FString` for tag comparisons → use `FName` (faster, no allocation)
- ❌ `FString` for player-visible text → use `FText` (enables localization)
- ❌ `FText::FromString()` on dynamic runtime text → OK, but no localization at all for that text
- ❌ `FName` for constantly changing data (e.g., player names typed at runtime) → FName pool never shrinks, leaks memory

---

## Timers (FTimerManager)

UE's equivalent of Unity Coroutines. Schedule a function to run after a delay, or repeat at an interval.

### C++

```cpp
// Run once after 2 seconds
GetWorldTimerManager().SetTimer(MyTimerHandle, this, &AMyActor::DelayedExplode, 2.0f, false);

// Repeat every 0.5 seconds
GetWorldTimerManager().SetTimer(MyTickHandle, this, &AMyActor::PeriodicCheck, 0.5f, true);

// Pause / unpause
GetWorldTimerManager().PauseTimer(MyTimerHandle);
GetWorldTimerManager().UnPauseTimer(MyTimerHandle);

// Cancel
GetWorldTimerManager().ClearTimer(MyTimerHandle);

// Check if running
GetWorldTimerManager().IsTimerActive(MyTimerHandle);

// Lambda timer (inline function)
GetWorldTimerManager().SetTimer(MyHandle, [](){ UE_LOG(LogTemp, Log, TEXT("Fired!")); }, 1.0f, false);
```

### Blueprint

Use **Delay** node for one-shot waits, or **Set Timer by Event / Set Timer by Function Name** for repeating logic:

| Node | Use |
|---|---|
| **Delay** | Wait N seconds then continue (latent — pauses execution flow) |
| **Set Timer by Event** | Wire a Custom Event as the callback, specify looping |
| **Set Timer by Function Name** | Call a function by name string |
| **Clear Timer by Handle** | Cancel a timer |
| **Pause / Unpause Timer by Handle** | Pause/resume |

### Timer Pitfalls

- Timers stop when their owning Actor is destroyed — no need to manually clean up if the Actor dies
- Check `IsTimerActive()` before setting a timer with the same handle to avoid double-scheduling
- `Delay` only works in latent functions (Event Graph, not Functions/Macros)
- Timer delegates in C++ use `FTimerHandle` — store as a member variable

---

## Level Management

### Core API

```cpp
// Open a level (replaces current)
UGameplayStatics::OpenLevel(GetWorld(), FName("Level2"));

// Open with options (listen server, etc.)
UGameplayStatics::OpenLevel(GetWorld(), FName("Level2"), true, "?listen");
```

**Blueprint:** `Open Level (by Name)` node.

### World Partition (UE5)

UE5's large-world system that streams only visible cells. Replaces the old World Composition from UE4.

- Enable in **World Settings → Enable World Partition**
- Each Actor is saved as a separate file (One File Per Actor / OFPA)
- `Content/__ExternalActors__/` stores OFPA data in hex-gridded subdirectories
- Data Layers control what streams when (gameplay variation, day/night, DLC)

**OFPA active** when `Content/__ExternalActors__/` + `Content/__ExternalObjects__/` exist. Implications: FObjectFinder less reliable in CDO constructor; each Actor saved as separate `.uasset`.

### Level Streaming (traditional)

Load/unload sub-levels at runtime:

```cpp
// Async load
ULevelStreamingDynamic* Level = ULevelStreamingDynamic::LoadLevelInstance(
    GetWorld(), "SubLevel", FVector::ZeroVector, FRotator::ZeroRotator, bOutSuccess);

// Unload
Level->SetShouldBeVisible(false);
```

---

## Render Pipeline (UE5)

UE5 has one unified renderer (unlike Unity's three pipelines), but with scalable features.

### Key Features

| Feature | What It Does | Enable |
|---|---|---|
| **Lumen** | Dynamic global illumination (no lightmap baking) | Project Settings → Rendering → Dynamic Global Illumination |
| **Nanite** | Virtualized geometry — no LOD authoring | Per mesh: enable Nanite on StaticMesh asset |
| **Virtual Shadow Maps** | High-res shadows with Nanite | Default enabled in UE5 |
| **TSR** (Temporal Super Resolution) | Upsampling for 60fps on consoles | Project Settings → Anti-aliasing |
| **Hardware Ray Tracing** | Accurate reflections, GI, shadows | Project Settings → Ray Tracing |
| **Substrate** (UE 5.5+) | Next-gen material system | Console var `r.Substrate 1` |
| **MegaLights** (UE 5.5+ exp.) | Hundreds of shadow-casting lights | Console var `r.MegaLights 1` |

### Graphics API

Check `Config/DefaultEngine.ini`:
```ini
DefaultGraphicsRHI=DefaultGraphicsRHI_DX12   # DirectX 12 (default UE5)
```

UE5 targets DX12 by default. Vulkan available on Linux/Android. No DX11 fallback for Nanite/Lumen.

### Scalability

UE scales features per quality level (Low/Medium/High/Epic). Set in **Settings → Engine Scalability**. Features like Lumen can be disabled on Low.

---

## Physics (Chaos)

UE5 uses Chaos physics (replacing PhysX from UE4).

### Collision Components

- **StaticMesh** → `UStaticMeshComponent` with `SetSimulatePhysics(false)` (default)  
- **Physics Body** → `UStaticMeshComponent` with `SetSimulatePhysics(true)`  
- **Character** → `ACharacter` uses CapsuleComponent for collision + CharacterMovementComponent for movement
- **Triggers** → any collision shape with `SetGenerateOverlapEvents(true)`

### Collision Responses

Each Component has a collision preset (NoCollision, BlockAll, OverlapAll, etc.) or custom per-channel response:
- **Block** → stops movement, fires OnComponentHit
- **Overlap** → no physics response, fires OnComponentBeginOverlap
- **Ignore** → no interaction

### Collision Events

```cpp
// C++ — bind in BeginPlay()
Mesh->OnComponentBeginOverlap.AddDynamic(this, &AMyActor::OnOverlapBegin);
Mesh->OnComponentHit.AddDynamic(this, &AMyActor::OnHit);

void AMyActor::OnOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
    UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    // Handle overlap
}
```

**Blueprint:** Select component → Details → Events → `OnComponentBeginOverlap` / `OnComponentHit`.

### Applying Forces

```cpp
// On a simulated physics body
Mesh->AddForce(FVector::ForwardVector * Strength);
Mesh->AddImpulse(FVector::UpVector * ImpulseStrength);
Mesh->AddTorqueInRadians(FVector::UpVector * Torque);

// On a Character
Character->LaunchCharacter(FVector::UpVector * JumpHeight, false, false);
```

### Common Pitfall

Collision/overlap events fire only if BOTH objects have `GenerateOverlapEvents` or collision enabled. If one object has collision disabled, no events fire.

### Line Trace / Raycast

UE's equivalent of Unity's `Physics.Raycast`. Fire a line into the world and get what it hits.

**C++ — single line trace:**

```cpp
FHitResult Hit;
FVector Start = GetActorLocation();
FVector End = Start + GetActorForwardVector() * 1000.0f; // 10 meters forward

FCollisionQueryParams Params;
Params.AddIgnoredActor(this); // don't hit yourself

bool bHit = GetWorld()->LineTraceSingleByChannel(
    Hit, Start, End, ECC_Visibility, Params);

if (bHit)
{
    AActor* HitActor = Hit.GetActor();
    FVector ImpactPoint = Hit.ImpactPoint;
    float Distance = Hit.Distance;
}
```

**Trace by object type** (more specific):
```cpp
FCollisionObjectQueryParams ObjParams;
ObjParams.AddObjectTypesToQuery(ECC_Pawn); // only hit pawns
GetWorld()->LineTraceSingleByObjectType(Hit, Start, End, ObjParams, Params);
```

**Multi-line trace** (hit all objects along the line):
```cpp
TArray<FHitResult> Hits;
GetWorld()->LineTraceMultiByChannel(Hits, Start, End, ECC_Visibility, Params);
```

**Shape traces** (sphere, box, capsule):
```cpp
// Sphere sweep (like a thick line trace)
GetWorld()->SweepSingleByChannel(Hit, Start, End, FQuat::Identity,
    ECC_Visibility, FCollisionShape::MakeSphere(50.0f), Params);

// Box sweep
GetWorld()->SweepSingleByChannel(Hit, Start, End, FQuat::Identity,
    ECC_Visibility, FCollisionShape::MakeBox(FVector(10, 10, 10)), Params);
```

**Blueprint:**

| Node | Use |
|---|---|
| **Line Trace By Channel** | Single trace, stops at first hit. Most common. |
| **Line Trace By Object Type** | Filter by specific object types (Pawn, WorldDynamic, etc.) |
| **Multi Line Trace By Channel** | Hits everything along the line, returns array |
| **Sphere Trace / Box Trace** | Shape traces (like thick lines) |

All trace nodes have a `Draw Debug Type` pin — set to `For One Frame` or `For Duration` to visualize the trace during development.

### Common Collision Channels

| Channel | Used For |
|---|---|
| `ECC_Visibility` | Line of sight, general purpose raycast |
| `ECC_Camera` | Camera collision, third-person camera |
| `ECC_Pawn` | Pawn/character collision |
| `ECC_WorldStatic` | Static meshes, walls, floors |
| `ECC_WorldDynamic` | Movable objects |
| `ECC_PhysicsBody` | Simulated physics bodies |
| Custom channels | Define in Project Settings → Collision |

### Trace Pitfalls

- **No hit at all** → check collision channel. If target uses `ECC_WorldStatic` but you trace `ECC_Visibility`, it won't hit.
- **Self-hit** → add `Params.AddIgnoredActor(this)` or disable `Trace Complex` in collision settings.
- **Hits behind you** → check that Start/End are correct. `GetActorForwardVector()` returns a unit vector — multiply by distance.
- **Blueprint `Draw Debug Type`** → set to `None` in shipping builds, or use `#if WITH_EDITOR` in C++.

### SweepMultiByObjectType vs SweepMultiByChannel

**`SweepMultiByChannel`** — filters by channel RESPONSE. If Pawn→Pawn is Overlap, won't detect other Pawns.
**`SweepMultiByObjectType`** — filters by object TYPE. Detects all objects of specified type(s) regardless of response. Preferred for combat traces:

```cpp
FCollisionObjectQueryParams ObjParams;
ObjParams.AddObjectTypesToQuery(ECC_Pawn);
GetWorld()->SweepMultiByObjectType(Hits, Start, End, FQuat::Identity, ObjParams, Shape, Params);
```

**Tag-based target identification:**
```cpp
Tags.Add(FName("Player"));  // in player's BeginPlay
if (HitActor->ActorHasTag(FName("Player"))) { /* apply damage */ }  // in enemy's attack trace
```

---

## Animation

### Animation Blueprint (ABP)

State machine-based system. Uses an **AnimGraph** (pose output) + **EventGraph** (per-frame logic).

- **State Machine** — transitions between states (Idle → Walk → Run) based on variables
- **Blend Space** — blends animations based on 1D or 2D parameters (e.g., speed + direction)
- **Animation Montage** — sequenced animation clips for attacks, interactions, combos
- **Aim Offset** — additive pose blending for weapon aiming
- **Control Rig** — procedural animation authoring and IK

### Key Variables

```cpp
// In Character class, update per Tick:
float Speed = GetVelocity().Size();
bool bIsInAir = GetCharacterMovement()->IsFalling();
```

Then in Animation Blueprint, read these variables to drive state transitions.

### Skeleton Animation Events

**Blueprint (in AnimGraph):** Add `AnimNotify` to timeline → fires event on the owning Actor.

### AnimNotify Architecture

AnimNotifies are `UAnimNotify` subclasses placed on montage timelines — they bridge animation to gameplay code:

```cpp
UCLASS()
class UAnimNotify_DoAttackTrace : public UAnimNotify
{
    GENERATED_BODY()
    virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation,
        const FAnimNotifyEventReference& EventReference) override;
};

// In .cpp: Cast owner to interface → call gameplay method
void UAnimNotify_DoAttackTrace::Notify(...) {
    if (ICombatAttacker* Attacker = Cast<ICombatAttacker>(MeshComp->GetOwner()))
        Attacker->DoAttackTrace(AttackBoneName);
}
```

**Common combat Notifies:** `DoAttackTrace`, `CheckCombo`, `CheckChargedAttack`, `EndDash`.

**Placement:** Open montage → Notifies track → right-click → Add Notify → select class → position on timeline.

### Common Pitfall

Forgetting to set `Mesh->SetAnimationMode(EAnimationMode::AnimationBlueprint)` or assign the AnimBP in the Character Blueprint → character is in T-pose.

### Compatible Skeleton Retargeting

When IK Rig Retarget fails in UE5.8 (Mixamo FBX: no Humanoid dropdown, IK Rig preview skeleton won't resolve):
1. Open target Skeleton → Skeleton Tree → right-click → **Manage Compatible Skeletons**
2. Add source skeleton → all its animations auto-retarget at runtime
3. Works for UE4→UE5 Mannequin, Animation Starter Pack (62 animations). Not for radically different skeletons.

### ABP Creation & Troubleshooting

**Creating a proper Animation Blueprint:**
- Content Browser → right-click → Animation → **Animation Blueprint** → parent class `AnimInstance` → target Skeleton.
- Do **NOT** use `create_blueprint` with `parent_class="AnimInstance"` — the MCP and generic Blueprint factory create a regular `UBlueprint`, which lacks the **AnimGraph** tab.
- To verify: a correct AnimBP has `Event Graph | Anim Graph` tabs. A regular BP has `Event Graph | Construction Script | Viewport`.

**Copying between Animation Blueprints:**
- AnimGraph and Event Graph from one ABP can be copy-pasted (`Ctrl+A` → `Ctrl+C` → `Ctrl+V`) into another ABP **with the same skeleton**.
- After Paste: **Compile immediately**. Missing variables from the source ABP will cause errors — check `My Blueprint → Variables` and recreate any that failed to copy (e.g., `GroundSpeed`, `Direction`, `ShouldMove`, `IsFalling`).
- Common cached references in ABP: `Character` (Object Reference), `Movement Component` (Character Movement Component). These must exist as local variables for the copied Event Graph to compile.

**Event Graph Variable Update Chain (standard pattern):**
```
Event Blueprint Update Animation
  → Sequence
    → Try Get Pawn Owner → Cast to Character → SET Character (cache)
    → Get Character → Get Character Movement → SET Movement Component
    → Get Movement Component → Get Velocity → Vector Length → SET GroundSpeed
    → Get Movement Component → Get Current Acceleration → ... → SET Direction
    ... → Get Is Crouched → SET Is Crouched     (custom crouch chain)
```
All `SET` nodes are on the Sequence execution chain. `Get` nodes are pure functions (no exec pins), connected by data lines to their targets.

**C++ BlueprintPure for AnimBP access:** See §Advanced Gameplay Patterns → C++ BlueprintPure for Animation Blueprint Access for full example with multi-function pattern and ABP Event Graph flow.

## Timelines

UE's visual animation curve editor. Create bezier/linear/key curves for float, vector, color, or other values over time — usable from Blueprint without C++.

**Create:** Content Browser → right-click → Miscellaneous → **Timeline**. Or inside any Blueprint Event Graph, right-click → `Add Timeline`.

**Structure:**
- **Track** — drives one value type (Float, Vector, Color, Event). A timeline can have multiple tracks.
- **Keyframe** — a point in time + value. Connect keyframes with curves.
- **Play / Reverse / Stop** — timeline control nodes.
- **Update** — output fires every frame while the timeline is playing.
- **Finished** — output fires when the timeline reaches the end.

**Common uses:**
- Smooth door/lift movement (Vector track driving `SetActorLocation`)
- UI fade in/out (Float track driving opacity)
- Camera fade to black (Float track driving a post-process parameter)
- Timed events (Event track firing sound effects at specific moments)

**Timeline vs Timer vs Tick:**

| | Timeline | Timer | Tick |
|---|---|---|---|
| **Curve-driven values** | ✅ Native | Requires manual lerp | Manual per-frame |
| **Precision** | Curve-precise | Delta-based | Frame-dependent |
| **Blueprint-friendly** | ✅ Visual editor | ✅ Nodes | ✅ Event node |
| **Overhead** | Medium | Low | Per-frame cost |
| **Use for** | Smooth animations, fading | Delayed/repeating logic | Continuous gameplay |

---

## Character Movement

`ACharacter` comes with a built-in **CharacterMovementComponent** (CMC). It handles walking, jumping, falling, swimming, flying — and syncs with Animation Blueprints automatically.

### Key Properties

| Property | What It Controls |
|---|---|
| `MaxWalkSpeed` | Top speed while walking (600 default) |
| `JumpZVelocity` | Vertical launch speed for jumps (420 default) |
| `AirControl` | How much the player can steer in mid-air (0.05 default, low) |
| `GravityScale` | Gravity multiplier (1.0 = normal) |
| `MaxAcceleration` | How fast speed ramps up |
| `BrakingDecelerationWalking` | How fast speed drops when no input |
| `bWantsToCrouch` | Request crouch (character resizes capsule) |

### Movement Modes

CMC has a `MovementMode` enum that determines how the character moves:

| Mode | Behavior |
|---|---|
| `MOVE_Walking` | On ground, affected by slopes |
| `MOVE_Falling` | In air, gravity applies |
| `MOVE_Flying` | Free 3D movement, no gravity |
| `MOVE_Swimming` | Underwater, buoyancy |
| `MOVE_NavWalking` | AI navigation on navmesh |
| `MOVE_Custom` | Override with custom movement logic (dash, wall-run, grapple) |

### Common Operations

```cpp
UCharacterMovementComponent* CMC = GetCharacterMovement();

// Jump
void AMyCharacter::OnJump()
{
    if (GetCharacterMovement()->IsMovingOnGround())
    {
        Jump();  // inherited from ACharacter, uses JumpZVelocity
    }
}

// Sprint
void AMyCharacter::OnSprintStart()  { CMC->MaxWalkSpeed = 1200.0f; }
void AMyCharacter::OnSprintEnd()    { CMC->MaxWalkSpeed = 600.0f; }

// Crouch
void AMyCharacter::OnCrouch()
{
    if (CMC->IsMovingOnGround())
    {
        Crouch();  // halves capsule height, adjusts camera
    }
}
```

**Blueprint:** `Get Character Movement` node → drag off to set properties or call `Jump`/`Crouch`/`StopJumping`.

### Movement Input

CMC reads movement input automatically when you call:

```cpp
void AMyCharacter::OnMove(const FInputActionValue& Value)
{
    FVector2D Input = Value.Get<FVector2D>();
    AddMovementInput(GetActorForwardVector(), Input.Y);   // W/S
    AddMovementInput(GetActorRightVector(), Input.X);     // A/D
}
```

CMC handles acceleration, friction, and slope limits from this raw input — no manual velocity math needed.

### Animation Integration

CMC exposes several variables that ABPs read directly:
- `GetVelocity().Size()` → speed → drives Walk/Run/Idle blends
- `IsFalling()` → jump/fall state
- `IsCrouching()` → crouch state
- `GetCurrentAcceleration()` → movement input direction → Blend Space parameter

### Common Pitfalls

- Calling `Jump()` when already in air → ignored. Check `IsMovingOnGround()` first.
- Modifying `MaxWalkSpeed` in Tick without caching CMC → constant GetComponent overhead.
- Changing `MaxWalkSpeed` directly on the MovementComponent, NOT on the Character — `Character->MaxWalkSpeed` is a deprecated wrapper.
- The `Crouch()`/`UnCrouch()` methods are on `ACharacter`, not on CMC.
- Directly setting `CMC->Velocity` in Tick → overridden next frame by CMC. Use `AddMovementInput()` or `LaunchCharacter()` instead.

### Crouch Setup

```cpp
// Constructor
GetCharacterMovement()->GetNavAgentPropertiesRef().bCanCrouch = true;
GetCharacterMovement()->SetCrouchedHalfHeight(48.f);  // use setter, not deprecated public member
```

Animation side (ABP): `Try Get Pawn Owner` → `Cast to YourCharacter` → `Get Is Crouched` → drive state machine or Blend Poses by Bool. Engine Manny crouch animations at `/Engine/Characters/Mannequins/Animations/Unarmed/Crouch/` (enable Show Engine Content).

### State Bitfields

Combine multiple gameplay states into one byte:
```cpp
uint8 bHasWallJumped : 1;
uint8 bHasDoubleJumped : 1;
uint8 bHasDashed : 1;
uint8 bIsDashing : 1;
uint8 bIsAttacking : 1;
uint8 bIsChargingAttack : 1;
```
Reset flags on landing: `Landed()` → zero out movement-specific flags.

---

## StateTree AI (UE5 Default)

UE5 game templates use **StateTree** for NPC behavior (not legacy Behavior Trees):

```
NPC's UStateTreeComponent → StateTree asset
  → Evaluators: check conditions (distance, HP, line-of-sight)
  → Tasks: execute actions (move, attack, evade)
```

**Key classes:** `AAIController` bridges StateTree and Navigation System. `UStateTree` asset defines behavior.

**Troubleshooting:** "Context Requirements failed" on PIE stop = benign. NPC freeze → press P to check NavMesh. NPC won't attack → verify target Tag/collision channel.

---

## UMG (UI)

UMG (Unreal Motion Graphics) is the Widget Blueprint system — UE's equivalent of uGUI.

### Widget Blueprint

Create in Content Browser → right-click → User Interface → Widget Blueprint. Use the **Designer** tab to arrange UI elements visually, and the **Graph** tab for logic.

### Common Widgets

| Widget | Purpose |
|---|---|
| Button | Clickable element with OnClicked event |
| Text Block | Display text |
| Image | Show texture/material |
| Progress Bar | Fill bar (health, loading) |
| Canvas Panel | Arbitrary pixel positioning |
| Horizontal/Vertical Box | Automatic layout |
| Overlay | Layered stacking |

### Creating and Showing UI

```cpp
// C++ — create widget and add to viewport
UUserWidget* Widget = CreateWidget<UUserWidget>(GetWorld(), WidgetClass);
Widget->AddToViewport();

// Remove
Widget->RemoveFromParent();
```

**Blueprint:** `Create Widget` → `Add to Viewport` nodes.

### Data Binding

UE5 supports property binding: Widget text/value → function or property → updates automatically. Set in the Designer, next to each property dropdown.

### CommonUI (UE 5.1+)

A cross-platform UI framework for controller/keyboard/touch navigation. Handles focus management, button styles per platform, and input mode switching automatically.

### WidgetComponent (3D World Widgets)

`UWidgetComponent` attaches a UMG widget to an Actor in the 3D world (health bars, nameplates):

```cpp
WComp->SetWidgetClass(WidgetClass);
WComp->InitWidget();                              // force immediate creation
WComp->SetRelativeLocation(FVector(0,0,120));     // above character head
WComp->SetDrawSize(FVector2D(150, 20));           // render resolution
WComp->SetTwoSided(true);
```

**Screen space** (`EWidgetSpace::Screen`): rendered above scene, always visible, **must call `RequestRedraw()`** after property changes (RenderTarget cache).

**World space** (`EWidgetSpace::World`): rendered in 3D world, participates in depth test (occluded behind geometry), auto-refreshes.

**Updating widget values from C++:**
```cpp
// Bypass BP event, directly access child widget by name
UProgressBar* PB = Cast<UProgressBar>(Widget->GetWidgetFromName(TEXT("Bar")));
if (PB) PB->SetPercent(0.75f);
WComp->RequestRedraw();  // required for Screen space
```
Widget name is found in the Widget BP Designer → Hierarchy panel.

---

## Audio

### Audio Components

- **AudioComponent** — plays SoundCues/SoundWaves, supports spatial 3D audio, looping, fading
- Add to any Actor via `UAudioComponent`

### Playing Sounds

```cpp
// One-shot (no component needed)
UGameplayStatics::PlaySound2D(GetWorld(), SoundCueAsset);
UGameplayStatics::PlaySoundAtLocation(GetWorld(), SoundCueAsset, Location);

// On an AudioComponent
AudioComp->SetSound(SoundCueAsset);
AudioComp->Play();
AudioComp->FadeIn(2.0f);
```

**Blueprint:** `Play Sound 2D` / `Play Sound at Location` nodes.

### MetaSounds (UE5)

MetaSounds is a procedural, programmable audio system — like a Material Editor for audio. Graph-based, data-driven, supports runtime parameter changes.

### Sound Cues

Traditional node-based audio logic (randomization, attenuation, modulation). Still supported alongside MetaSounds.

---

## Niagara (VFX)

Niagara is UE5's particle and visual effects system (replacing Cascade from UE4). It uses a modular, stack-based approach — each emitter is a pipeline of reorderable modules.

### System vs Emitter

| Level | What It Does |
|---|---|
| **Niagara System** | Top-level asset you place in the level. Contains one or more Emitters. The System handles shared parameters, timings, and world interaction. |
| **Emitter** | One particle emitter inside a System. Each emitter has its own spawn rate, lifetime, modules, and renderer. You can stack multiple emitters (fire trail + smoke burst + sparks). |

### Core Modules (Emitter Pipeline)

Each emitter processes particles through a fixed-order pipeline:

| Module | Function |
|---|---|
| **Emitter State** | Emitter lifecycle: active/inactive, loops, duration |
| **Spawn Rate / Spawn Burst** | How many particles per second, or a one-time burst count |
| **Particle Spawn** | Initialize each new particle: position, velocity, color, size, lifetime |
| **Particle Update** | Per-frame updates: velocity, forces, color-over-life, size-over-life, drag |
| **Render** | How particles look: sprite, mesh, ribbon, light, volume |

### Common Operations

**Change particle count:**
- Select Emitter → **Spawn Rate** module → drag `SpawnRate` value higher/lower
- For instant burst: add **Spawn Burst Instantaneous** module in Particle Spawn

**Change particle lifetime:**
- Emitter → **Particle Spawn** → `Initialize Particle` → modify `Lifetime` range

**Change particle size / color:**
- **Particle Update** → `Scale Color` or `Scale Sprite Size` → set curve/constant over particle life

**Add gravity / wind:**
- **Particle Update** → `Add Velocity` or `Curl Noise Force` → adjust strength

**GPU vs CPU emitters:**
- Select Emitter → `Properties` → `Sim Target`: `CPUSim` (features + collision) or `GPUComputeSim` (massive counts, limited features)

### Opening a Niagara System

Double-click any Niagara asset in the Content Browser, or drag one into a level → right-click Actor → `Edit Niagara System`.

### Lightweight Emitters (UE 5.4+)

Stateless emitters for simple VFX (sparkles, dust motes, UI particles). No per-frame state stored — lower overhead, but no collision support. Good for ambient effects with high emitter counts.

### Niagara Data Channels (UE 5.5+)

Pass data between different Niagara Systems (e.g., a footstep system tells a dust system exactly where to spawn). Also used to inject gameplay events into shared VFX pools for better performance.

### Heterogeneous Volumes (UE 5.5+, Beta)

Import VDB volumetric data (smoke, explosions) into Niagara and render as Sparse Volume Textures. Supports self-shadowing and overlapping volumes.

### Choosing Niagara vs Blueprint Spawned VFX

| Scenario | Use |
|---|---|
| Continuous ambient effects (dust, fog, rain) | Niagara with Lightweight Emitters |
| Complex particle behavior (curves, forces, burst) | Niagara CPU/GPU emitter |
| Simple one-shot effects (muzzle flash) | Spawn a Niagara System Actor via Blueprint |
| Logic-driven VFX (boss spawn, cutscene) | Trigger Niagara activation from Blueprint event |

---

## Enhanced Input

UE5's modern input system (replaces legacy Axis/Action mappings from UE4).

### Core Concepts

| Asset | Purpose |
|---|---|
| **Input Action** | Abstract action: "Jump", "Fire", "Move" |
| **Input Mapping Context** | Maps keys/buttons to Input Actions |
| **Input Modifier** | Post-processes raw input (negate, dead zone, scalar) |
| **Input Trigger** | Determines when action fires (pressed, held, released, tapped) |

### Setup Workflow

1. Create **Input Actions** in `Content/Input/Actions/`
2. Create **Input Mapping Context** in `Content/Input/`
3. In Character Blueprint → `Event BeginPlay` → `Get Player Controller` → `Enhanced Input Local Player Subsystem` → `Add Mapping Context`
4. Bind Input Actions to your logic via `Enhanced Input Action Event` nodes

### C++ Binding

```cpp
// Setup
void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    if (UEnhancedInputComponent* EnhancedInput = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        EnhancedInput->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AMyCharacter::OnMove);
        EnhancedInput->BindAction(JumpAction, ETriggerEvent::Started, this, &AMyCharacter::OnJump);
    }
}

void AMyCharacter::OnMove(const FInputActionValue& Value)
{
    FVector2D MovementVector = Value.Get<FVector2D>();
    AddMovementInput(GetActorForwardVector(), MovementVector.Y);
    AddMovementInput(GetActorRightVector(), MovementVector.X);
}
```

### Common Pitfall

Forgetting to add the Input Mapping Context in BeginPlay → Enhanced Input does nothing silently. Also, ensure `EnhancedInput` plugin is enabled in `.uproject`.

### Multi-IMC Loading

Load multiple IMCs in the PlayerController:

```cpp
if (UEnhancedInputLocalPlayerSubsystem* Sub = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
{
    Sub->AddMappingContext(IMC_Default, 0);    // WASD + mouse
    Sub->AddMappingContext(IMC_MouseLook, 0);  // mouse camera control
    Sub->AddMappingContext(IMC_Gameplay, 0);   // combat/jump/dash
}
```

If ConstructorHelpers fails (IMC array empty), fallback in `BeginPlay`:
```cpp
UInputMappingContext* IMC = LoadObject<UInputMappingContext>(nullptr, TEXT("/Game/Input/IMC_Fused.IMC_Fused"));
if (IMC) DefaultMappingContexts.Add(IMC);
```

### Trigger Events

| ETriggerEvent | When |
|---|---|
| `Started` | Input becomes non-zero (press) |
| `Ongoing` | Every tick while held |
| `Triggered` | Thresholds met (hold time, tap) |
| `Completed` | Input returns to zero (release) |
| `Canceled` | Interrupted before completion |

**Typical bindings:**
```cpp
BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
BindAction(JumpAction, ETriggerEvent::Completed, this, &ACharacter::StopJumping);
BindAction(CrouchAction, ETriggerEvent::Started, this, &AMyChar::ToggleCrouch);
```

**Note:** Some UE versions merge identical InputAction Mappings into one row. Use multiple Triggers within a single row as workaround.

### Interface Calling Convention

When a `UINTERFACE` uses `MinimalAPI` + `NotBlueprintable`:
```cpp
UINTERFACE(MinimalAPI, NotBlueprintable)
class UCombatDamageable : public UInterface { ... };
```
UHT does **NOT** generate `Execute_` helpers. Call directly:
```cpp
if (ICombatDamageable* Dmg = Cast<ICombatDamageable>(HitActor))
    Dmg->ApplyDamage(...); // correct
// NOT: ICombatDamageable::Execute_ApplyDamage(...) — won't compile
```

`Execute_` is only generated for `BlueprintImplementableEvent`/`BlueprintNativeEvent` on Blueprint-exposed UINTERFACEs. Always check the interface header first.

---

## Network Replication

UE has built-in client-server networking. The server is authoritative; clients send inputs, server runs logic, state syncs back.

### Key Concepts

| Term | Meaning |
|---|---|
| **Server** | Authoritative. Runs GameMode, executes gameplay logic. |
| **Client** | Owns one PlayerController + Pawn. Sends input, receives state. |
| **Listen Server** | One player is both server AND client. |
| **Dedicated Server** | Server with no local player — purely authoritative. |
| **Replication** | Server sends property/actor state to clients. |

### Property Replication

```cpp
UPROPERTY(Replicated)
float Health;

UPROPERTY(ReplicatedUsing = OnRep_Ammo)
int32 Ammo;

UFUNCTION()
void OnRep_Ammo();  // Called on clients when Ammo changes on server

// Must override in .cpp:
void AMyCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyCharacter, Health);
    DOREPLIFETIME_CONDITION(AMyCharacter, Ammo, COND_OwnerOnly); // only to owning client
}
```

### RPC (Remote Procedure Calls)

```cpp
UFUNCTION(Server, Reliable)     // Called from client → executes on server
void ServerFire();

UFUNCTION(Client, Reliable)     // Called from server → executes on owning client
void ClientShowDamage(float Amount);

UFUNCTION(NetMulticast, Reliable)  // Called from server → executes on ALL clients
void MulticastPlayExplosion(FVector Location);

// Implementation:
void AMyCharacter::ServerFire_Implementation()
{
    // This runs on the server
    MulticastPlayExplosion(GetActorLocation());
}

bool AMyCharacter::ServerFire_Validate() { return true; } // optional validation
```

### Authority Check Pattern

```cpp
// Only run on server
if (HasAuthority())
{
    // Apply damage, spawn items, etc.
}

// Only run on owning client
if (IsLocallyControlled())
{
    // Show local UI, play local effects
}
```

**Blueprint:** `Switch Has Authority` node.

### Common Pitfall

- RPCs must be called from the correct side (Server RPC → called only on client). Calling a Server RPC from the server → ignored.
- Forget to add `GetLifetimeReplicatedProps` → properties don't replicate, no warning.
- Replicated properties only sync server→client. Clients never modify replicated properties directly — use Server RPCs to request server state changes.

---

## GameInstance

Created on game start, persists across ALL level transitions. Destroyed only on game quit.

### What Goes in GameInstance

- Persistent managers (save system, settings, achievement tracking)
- Cross-level data (selected character, difficulty)
- Score/campaign state that survives death
- Online session management

### Accessing GameInstance

```cpp
UGameInstance* GI = GetGameInstance();
UMyGameInstance* MyGI = Cast<UMyGameInstance>(GI);
if (MyGI) { MyGI->PlayerScore = 100; }
```

**Blueprint:** `Get Game Instance` node → cast to your custom GameInstance class.

## SaveGame (USaveGame)

UE's serialization system for saving/loading player progress:

```cpp
// MySaveGame.h — define save data
UCLASS()
class UMySaveGame : public USaveGame
{
    GENERATED_BODY()

public:
    UPROPERTY()
    float PlayerHealth;

    UPROPERTY()
    int32 Level;

    UPROPERTY()
    FVector PlayerPosition;

    UPROPERTY()
    TArray<FString> CompletedQuests;
};

// Save
UMySaveGame* SaveGameInstance = Cast<UMySaveGame>(
    UGameplayStatics::CreateSaveGameObject(UMySaveGame::StaticClass()));
SaveGameInstance->PlayerHealth = 100.0f;
UGameplayStatics::SaveGameToSlot(SaveGameInstance, TEXT("Slot1"), 0);

// Load
UMySaveGame* LoadedGame = Cast<UMySaveGame>(
    UGameplayStatics::LoadGameFromSlot(TEXT("Slot1"), 0));
if (LoadedGame)
    Health = LoadedGame->PlayerHealth;

// Check if save exists
if (UGameplayStatics::DoesSaveGameExist(TEXT("Slot1"), 0)) { }

// Delete save
UGameplayStatics::DeleteGameInSlot(TEXT("Slot1"), 0);
```

**Blueprint:** `Save Game to Slot` / `Load Game from Slot` nodes.

**Common pattern:** Autosave on level transition, manual save at checkpoints, load on game start in GameInstance.

## Subsystems

The modern replacement for Singletons in UE5. Managed by the engine, auto-instantiated:

| Subsystem Type | Lifetime | Use for |
|---|---|---|
| **UGameInstanceSubsystem** | Entire game session | SaveManager, AchievementTracker |
| **UWorldSubsystem** | Per level/map | SpawnManager, Weather, QuestTracker |
| **ULocalPlayerSubsystem** | Per local player | Input binding, UI state manager |
| **UEditorSubsystem** | Editor only | Editor tools, automation |

```cpp
// MyWorldSubsystem.h
UCLASS()
class UMyWorldSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    void SpawnWave(int32 Count);
};

// Usage from anywhere:
UMyWorldSubsystem* Sub = GetWorld()->GetSubsystem<UMyWorldSubsystem>();
if (Sub) Sub->SpawnWave(10);
```

Subsystems are auto-discovered — no registration, no Singleton pattern. Use them instead of static managers.

---

## Data Assets (UDataAsset / UPrimaryDataAsset)

Similar to Unity's ScriptableObject — data containers that live as project assets, not scene objects.

```cpp
UCLASS(BlueprintType)
class UWeaponData : public UDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString WeaponName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float Damage;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    UTexture2D* Icon;
};
```

Create in Content Browser → right-click → Miscellaneous → Data Asset → select your class.

Great for weapon stats, enemy configs, item databases, dialogue trees.

### DataTables

For tabular data — rows of entries with the same columns. Like a spreadsheet:

1. Create a struct: `USTRUCT(BlueprintType) struct FWeaponRow : public FTableRowBase { ... };`
2. Create DataTable asset → set row struct to `FWeaponRow`
3. Fill rows in the editor (CSV import supported)

```cpp
// Lookup by row name
FWeaponRow* Row = DataTable->FindRow<FWeaponRow>(FName("Shotgun"), TEXT(""));
if (Row) float Damage = Row->Damage;
```

**Blueprint:** `Get Data Table Row` node → pick row by name → break struct.

**DataAsset vs DataTable:**

| | DataAsset | DataTable |
|---|---|---|
| One entry per asset | ✅ | ❌ |
| Tabular/mass data | ❌ | ✅ |
| CSV import | ❌ | ✅ |
| Use for | Unique configs | Item databases |

### GameplayTags

Hierarchical labels for categorizing and querying: `Enemy.Melee.Goblin`, `State.Dead`, `Ability.Cooldown`.

```cpp
// Match with hierarchy (O(1)) — Enemy.Melee.Goblin matches "Enemy"
if (Actor->HasMatchingGameplayTag(FGameplayTag::RequestGameplayTag("Enemy"))) { }

// Request once, reuse
FGameplayTag DeadTag = FGameplayTag::RequestGameplayTag("State.Dead");
```

**Blueprint:** `Has Matching Gameplay Tag` node. Enable the `GameplayTags` plugin.

Use tags instead of string/enum-based state checks for: damage types, character state, ability categories, UI filters.

### Soft References (TSoftObjectPtr)

Defer loading large assets — critical for memory and load times:

```cpp
// Hard reference — loads immediately, stays in memory
UPROPERTY() UTexture2D* Icon;

// Soft reference — paths only, loads on demand
UPROPERTY() TSoftObjectPtr<UTexture2D> IconSoft;
IconSoft.LoadSynchronous(); // blocking load (small assets OK)
// For large: use FStreamableManager::RequestAsyncLoad()
```

**Blueprint:** `Soft Object Reference` variable → `Async Load Asset` node → use result on success pin.

---

## Gameplay Ability System (Overview)

GAS is UE's built-in framework for abilities, attributes, buffs, and cooldowns. Used by games like Fortnite, ARK, Borderlands.

### When to Use
- RPGs, MOBAs, hero shooters with many abilities/buffs
- Complex attribute systems (health + shield + armor + modifiers)
- Cooldown management, ability costs (mana, stamina)

### When NOT to Use
- Simple games with few mechanics
- Prototyping phase (adds significant complexity)
- Teams without a programmer comfortable with GAS

### Key Modules
- `AbilitySystemComponent` — attaches to Pawn/Character, manages abilities
- `GameplayAbility` — one ability (fire, jump, heal)
- `GameplayEffect` — modifier (damage, buff, debuff, heal)
- `GameplayTag` — hierarchical labels for categorization

GAS is fully exposed to Blueprint. Enabling the `GameplayAbilities` plugin activates it.

---

## Performance Best Practices

### C++ Performance
- Avoid `GetAllActorsOfClass()` in Tick — cache or use a manager
- Prefer `TArray` over `std::vector` — UE's allocator is optimized
- Use `FString` for text, `FName` for identifiers (interned, fast comparison), `FText` for localized display
- Avoid `LoadObject` at runtime — use `TSoftObjectPtr` for async loading

### Blueprint Performance
- Blueprint `Tick` is slower than C++ `Tick` — move heavy work to C++
- Avoid casting on Tick — cache the cast result
- Use `Sequence` instead of many function calls with output pins when data doesn't depend on order

### Rendering
- Enable Nanite on high-poly static meshes
- Use LODs for skeletal meshes and non-Nanite geometry
- Limit dynamic shadow-casting lights
- Use Light Function Atlas (UE 5.5+) to reduce light function cost
- Profile with `stat gpu`, `stat unit`, `stat scenerendering`

### Physics
- Use simple collision shapes (box, sphere, capsule) over complex mesh collision
- Disable physics simulation on objects that don't need it
- Limit the number of simulated bodies — Chaos is cheaper than PhysX but still not free

## Packaging & Shipping

### Build Configuration

`Project Settings → Packaging` or **Platforms → Windows → Package Project**.

**Key settings:**
- **Build Configuration:** `Development` (debug info, logs) or `Shipping` (optimized, no console, for release)
- **Full Rebuild:** Recompiles everything — use when things break mysteriously
- **Cook only maps in list:** cooks only levels in Project Settings → Maps list (saves time)

### Package Folder

Output goes to project root's `Windows/` folder (or corresponding platform). The `.exe` requires all adjacent DLLs and the `Content/Paks/` folder — distribute the entire output directory.

### Shipping Build Checklist

| Item | Why |
|---|---|
| Set `bIsShipping = true` in `.Target.cs` | Removes debug code, editor-only features |
| Disable `Draw Debug` trace/print | `DrawDebugLine` doesn't compile in Shipping |
| Remove console commands | `stat fps`, `stat unit` not available in Shipping |
| Test on target hardware | Editor ≠ standalone build. GPU/CPU profiles differ. |
| Package Content Compression | Project Settings → Packaging → Enable Pak compression |
| Check asset references | Any missing assets become invisible (no error) |
| Test with `-game` flag | Launch `.exe -game -log` for debug output |

### Cross-Platform

| Platform | Additional Requirements |
|---|---|
| **Windows** | None — out of the box |
| **Mac** | Requires Mac with Xcode (can't cross-compile from Windows) |
| **Linux** | Cross-compile toolchain or build on Linux |
| **Android** | Android SDK + NDK + device for testing |
| **iOS** | Mac + Xcode + Apple Developer account |

### Patch & DLC

Use **Patching** in Project Settings → Packaging for delta updates. Content-only patches can be smaller than a full rebuild. External Data Layers + Game Features plugins support DLC without touching base game content.

---

## MCP Integration (UE5.5+)

The Model Context Protocol enables AI assistants to control Unreal Editor through natural language. Two implementations exist: the official UE5 built-in plugin and the community-driven chongdashu/unreal-mcp.

### Official vs Community MCP

| | Official (Built-in) | Community (chongdashu/unreal-mcp) |
|---|---|---|
| **Activation** | Edit → Plugins → Enable "ModelContextProtocol" | Copy `Plugins/UnrealMCP/` to project + build |
| **Port** | HTTP :8000 | TCP :55557 (C++ plugin) + Python bridge |
| **Tool Count** | ~4 (AgentSkill only) | ~30 (Actor, Blueprint, UMG, Editor, Input) |
| **Python Setup** | None | `uv` venv with `fastmcp`, `mcp[cli]` |

### Community MCP Deployment (opencode)

1. **Plugin**: Clone repo → copy `MCPGameProject/Plugins/UnrealMCP/` to project `Plugins/`
2. **Build**: Close editor → `Engine\Build\BatchFiles\Build.bat ProjectEditor Win64 Development -Project="path.uproject" -WaitMutex`
3. **Python**: `uv venv` in `Plugins/UnrealMCP/Python/` → `uv pip install -e .`
4. **opencode config** (`~/.config/opencode/opencode.json`):
```json
"mcp": {
  "unrealMCP": {
    "type": "local",
    "command": ["uv.exe", "--directory", "<path>/Python", "run", "unreal_mcp_server.py"]
  }
}
```

### UE5.8 Compatibility Fixes

| Issue | Fix |
|---|---|
| `ANY_PACKAGE` undeclared (removed in 5.8) | Replace with `nullptr` in `FindObject<UClass>(nullptr, ...)` |
| `BufferSize` shadows engine `StringConv.h` | Rename local `BufferSize` → `MCPSocketBufferSize` |
| `add_component_to_blueprint` fails for `StaticMeshComponent` | Known limitation — `FindObject<UClass>` can't resolve at MCP call time |
| StaticMesh not assignable to spawned Actor via `set_actor_property` | MCP only sets Actor-level properties, not component sub-properties |

### MCP Limitations

- **No Animation Blueprint support**: `find_blueprint_nodes` / `add_blueprint_variable` only work on regular Blueprints, not AnimBPs.
- **No asset deletion**: `delete_actor` only removes level actors, not Content Browser assets.
- **Static mesh assignment**: `set_static_mesh_properties` only works on Blueprint CDOs, not spawned actors.
- **UE Editor must be running**: Python bridge connects to the C++ plugin's TCP server inside the editor process.

---

## Troubleshooting Common Issues

### Shader Compilation Stuck or Crashing

Symptom: Editor freezes with "Compiling Shaders (XXXX remaining)" or crashes on launch.

- **Wait it out** — first launch after engine/project update compiles thousands of shaders. Can take 10-30 minutes.
- **Out of VRAM** — integrated GPUs (Intel Arc, AMD APU) may run out of VRAM during shader compilation. Lower in-engine quality to Medium: Settings → Engine Scalability → Medium.
- **Driver update** — update your GPU driver to the latest version.
- **Nuke shader cache**: Delete `DerivedDataCache/` and `Intermediate/` in both project folder and engine install, then restart.

### EXCEPTION_ACCESS_VIOLATION

Most common crash. Null pointer dereference — you accessed an Actor/Component that doesn't exist.

- Check if `GetWorld()`, `GetOwner()`, `FindComponentByClass<T>()` returned `nullptr` before use.
- In Blueprint: use `IsValid?` node before accessing object references.
- Character falling out of world → set `World Settings → Kill Z` to remove and respawn below a threshold instead of crashing.

### Project Won't Open / Version Mismatch

- Right-click `.uproject` → **Switch Unreal Engine Version** → pick installed version.
- If engine not listed: launch Epic Games Launcher → Unreal Engine tab → Library → install matching version.
- Corrupted project: delete `Intermediate/` and `Saved/` folders → reopen.
- "Modules are missing or built with a different engine version" → right-click `.uproject` → **Generate Visual Studio Project Files**.

### DX12 / GPU Crashes

Symptom: Flickering, artifacts, or crash mentioning D3D12.

- Switch to DX11 as fallback: Edit → Project Settings → Platforms → Windows → Default RHI → DX11. Restart editor.
- **Note:** Some UE5 features (Nanite, hardware Lumen) require DX12. DX11 mode disables them.
- On Intel Arc GPUs: ensure drivers are up-to-date. Disable hardware ray tracing: `r.RayTracing 0` in console.

### Blueprint Node Disappeared / Types Incorrect

- Did you rename a C++ class or variable? → Blueprint nodes referencing old names break. Compile C++ first, then reopen Blueprint.
- "Enum/Variable not found" → compile C++ first, then right-click Refresh Nodes in Blueprint.
- Drag-and-drop not working from Content Browser → check that the asset type matches the pin type (e.g., can't drag a Static Mesh onto a Material slot).

### Editor Crashed — Recovery

- Relaunch the editor. When prompted, UE will offer to recover unsaved changes.
- Recovered assets appear in the **Recovery Hub** on editor restart.
- Auto-save interval: Editor Preferences → Loading & Saving → Auto-Save → set to 5 minutes.

### Output Log Search Guide

| Pattern | Indicates |
|---|---|
| `LogUObjectGlobals: Error` | FObjectFinder path wrong, missing content |
| `LogPlayerManagement: Error` | Duplicate player creation in BeginPlay |
| `LogLoad: Game class is <X>` | Current GameMode — verify correct class |
| `LogStateTree: Warning` | Usually benign (PIE cleanup) |

**Benign PIE messages:** "StateTree Context Requirements failed", "Recreating Persistent SBTs", "HTTP request timed out", "Failed to load aqProf.dll".

**Debug logging:**
```cpp
DEFINE_LOG_CATEGORY(LogMyModule);  // top of .cpp
UE_LOG(LogMyModule, Log, TEXT("Val: %d, Float: %.1f"), IntVal, FloatVal);
```

### Build Error: Live Coding Active

Symptom: `Unable to build while Live Coding is active. Exit the editor and game.`

- Close all UE Editor instances completely, then retry the build.
- Alternatively, press `Ctrl+Alt+F11` in the editor to disable Live Coding for the current session, then build.

### Build Error: ANY_PACKAGE Undeclared (UE5.5+)

Symptom: `error C2065: 'ANY_PACKAGE': undeclared identifier`

`ANY_PACKAGE` was removed in UE5.5+. Replace all occurrences with `nullptr`:
```cpp
// Before:
FindObject<UClass>(ANY_PACKAGE, *ClassName);
// After:
FindObject<UClass>(nullptr, *ClassName);
```

### Blueprint Variable Name Mismatch

Symptom: `Could not find a variable named "X"` during ABP compile after copy-pasting.

UE is whitespace-sensitive in variable names. `MovementComponent` ≠ `Movement Component`. Check the **exact** name in the source ABP's My Blueprint panel and recreate with identical spelling, capitalization, and spacing in the target. Match the Category field too for clean organization.

---

## Appendix: Unity → UE Concept Mapping

| Unity | Unreal Engine | Notes |
|---|---|---|
| GameObject | Actor (AActor) | Actor = GameObject with optional built-in networking |
| Component (MonoBehaviour) | Component (UActorComponent) | Similar pattern, UE Components can be non-spatial |
| Transform | RootComponent (USceneComponent) | Same hierarchy, UE uses FVector/FQuat/FRotator |
| Prefab | Blueprint Class | Blueprint = Prefab + inheritance + visual scripting |
| Scene | Level (.umap) | Level = persistent base level + optional sub-levels |
| SceneManager.LoadScene() | UGameplayStatics::OpenLevel() | Async loading via ULevelStreamingDynamic |
| MonoBehaviour.Awake() | AActor::BeginPlay() | BeginPlay = Start (Awake has no direct equivalent) |
| MonoBehaviour.Update() | AActor::Tick() | Can be enabled/disabled per Actor |
| MonoBehaviour.FixedUpdate() | No built-in fixed framestep per Actor | Set `TickInterval` or use a Timer |
| Coroutine | Timer / Latent Action / Delay node | No direct C++ equivalent; use FTimerManager or Blueprint Delay |
| Input Manager (legacy) | Enhanced Input | Both are vastly different; Enhanced Input is asset-based |
| Animator Controller | Animation Blueprint | State machines + Blend Spaces, no Mecanim Humanoid |
| uGUI Canvas | UMG Widget Blueprint | Similar retention-mode UI, UMG has visual designer |
| ScriptableObject | DataAsset / UPrimaryDataAsset | Same purpose: data container asset |
| DontDestroyOnLoad | GameInstance | GameInstance is a dedicated persistent object |
| Raycast (Physics.Raycast) | UWorld::LineTraceSingleByChannel() | ECC channels determine what to trace against |
| Rigidbody.AddForce() | UPrimitiveComponent::AddForce() | Chaos physics instead of PhysX |
| OnCollisionEnter | OnComponentHit / OnComponentBeginOverlap | Separate events for block vs trigger |
| Build Settings → Scenes | Project Settings → Maps & Modes | Default map + GameMode set per-project |
| Layer-based collision | Collision Channels (Object Type + Response) | More granular: custom channels, per-body response |
| GetComponent\<T\>() | FindComponentByClass\<T\>() or Cast\<T\>() | Cast checks type; FindComponentByClass searches |
| Instantiate() | SpawnActor\<T\>() | Requires UWorld context |
| Destroy() | AActor::Destroy() | Garbage collector handles UObject cleanup |

---

## Project Knowledge Board

> Project-specific memory entries. Each entry records key paths, class names, and design decisions unique to a single project. For reuse across sessions when returning to the same project.

### ThirdPersonTest (2026-06-25)
- **UE Version**: 5.8 custom/source build, GUID `{FC15C0B3-49D4-2C64-62DD-95B5932C7147}`
- **Engine Path**: `C:/Program Files/Epic Games/UE_5.8`
- **Core Character**: `AFusedCharacter` (Variant_Fused/) — merges Combat + Platforming from three game variants
- **AnimBP**: `ABP_Fused` at `/Game/Variant_Fused/Anims/ABP_Fused`, loaded in `FusedCharacter.cpp:52`. Based on `ABP_Manny_Combat` AnimGraph + Event Graph.
- **Crouch System**: 
  - C++: `bCanCrouch = true`, `SetCrouchedHalfHeight(48.f)`, `GetIsCrouched()` BlueprintPure at `FusedCharacter.h:203-204`
  - AnimBP: Local `Is Crouched` Boolean → Locomotion state machine Crouch state → transitions with `Get Is Crouched` / `NOT`
  - **Placeholder**: Crouch state uses `BS_Idle_Walk_Run` — no real crouch animations in project. Migrate from UE4 or asset pack.
- **MCP**: Community MCP deployed at `Plugins/UnrealMCP/`, Python venv at `Plugins/UnrealMCP/Python/.venv`, opencode config at `~/.config/opencode/opencode.json`. Official `ModelContextProtocol` plugin disabled in `.uproject`.
- **Input**: 9 InputActions, IMC_Fused loaded by `FusedPlayerController`. `IA_Crouch` bound to `C` key.
- **Build Fix**: `BufferSize`→`MCPSocketBufferSize` in `MCPServerRunnable.cpp:15`; `ANY_PACKAGE`→`nullptr` in `UnrealMCPBlueprintNodeCommands.cpp` + `UnrealMCPBlueprintCommands.cpp`.

---

---

## Advanced Gameplay Patterns

### Compatible Skeleton Animation Retargeting

See §Animation → Compatible Skeleton Retargeting for the lightweight retargeting workflow (IK Rig fallback for Mixamo in UE5.8).

### C++ BlueprintPure for Animation Blueprint Access

Expose C++ state to AnimBP without long property chains:

```cpp
// In your Character header
UFUNCTION(BlueprintPure, Category="Crouch")
bool GetIsCrouched() const { return bIsCrouched; }

UFUNCTION(BlueprintPure, Category="Combat")
bool GetIsAttacking() const { return bIsAttacking; }
```

In ABP Event Graph:
```
Event Blueprint Update Animation
  → Try Get Pawn Owner → Cast to YourCharacter
  → (pure) Get Is Crouched → SET local IsCrouched
  → (pure) Get Is Attacking → SET local IsAttacking
```

No `Cast` needed after the initial owner cache. Pure functions have green pins — no execution flow required.

### Checkpoint / Respawn System

Store respawn position on the PlayerController, restore on death:

```cpp
// PlayerController stores the respawn transform
UPROPERTY()
FTransform RespawnTransform;

void SetRespawnLocation(const FTransform& NewTransform) { RespawnTransform = NewTransform; }

// Character uses it on respawn
void RespawnCharacter()
{
    SetActorLocation(GetController<AMyPlayerController>()->RespawnTransform.GetLocation());
    // Reset HP, state flags, mesh transform, collision, camera
    CurrentHP = MaxHP;
    bHasDoubleJumped = bHasWallJumped = bHasDashed = false;
    GetMesh()->SetRelativeLocation(FVector::ZeroVector);
    SetActorEnableCollision(true);
    GetCharacterMovement()->SetMovementMode(MOVE_Walking);
}
```

**Checkpoint Volume (C++):**
```cpp
// 200x200 box trigger — on overlap, update controller's RespawnTransform
void AMyCheckpointVolume::OnOverlap(AActor* Other)
{
    if (AMyCharacter* Char = Cast<AMyCharacter>(Other))
    {
        if (AMyPlayerController* PC = Cast<AMyPlayerController>(Char->GetController()))
            PC->SetRespawnLocation(Char->GetActorTransform());
    }
}
```

### Combo Attack Input Cache

Cache attack input during a fixed tolerance window to enable combo chains:

```cpp
// Properties
float ComboInputCacheTimeTolerance = 0.45f;  // window to buffer next input
float AttackCooldown = 0.2f;                  // minimum time between attacks
float AttackInputCacheTimeTolerance = 1.0f;   // buffer for initial attack
float CachedAttackInputTime = 0.0f;

void ComboAttackPressed()
{
    // Ignore if in attack cooldown
    if (GetWorld()->GetTimeSeconds() - LastAttackTime < AttackCooldown)
        return;
    
    // Cache the input time
    CachedAttackInputTime = GetWorld()->GetTimeSeconds();
    
    if (!bIsAttacking)
        ComboAttack(); // start the montage
}

void ComboAttack()
{
    bIsAttacking = true;
    PlayAnimMontage(ComboAttackMontage);
}
```

**AnimNotify chain** (placed on Montage timeline):
```
AnimNotify_CheckCombo:  // early in animation
  → if (CachedAttackInputTime within tolerance)
  → Jump to "Attack2" section in montage

AnimNotify_DoAttackTrace:  // mid-animation
  → SweepMultiByObjectType for ECC_Pawn
  → ApplyDamage to hit actors with "Player" tag

AnimNotify_AttackMontageEnded:  // end
  → bIsAttacking = false
  → Start AttackCooldown timer
```

### Substrate Material System (UE 5.5+)

UE5.5+ next-gen material system. Enable: `r.Substrate 1` (enabled by default in ThirdPersonTest):

| Substrate replaces | With |
|---|---|
| Material Domain system | Slab/Directional/Volumetric/Decal slabs |
| `Blend Mode Override` | Per-slab blending in material editor |
| PBR metallic/roughness pipeline | Explicit BSDF (Bidirectional Scattering Distribution Function) graph |

**Key differences for manual construction:**
- `MakeMaterialAttributes` → `MakeSubstrateMaterialAttributes`
- `SetMaterialAttributes` → `SetSubstrateMaterialAttributes`
- Common main node: `Substrate Slab BSDF` (replaces `MakeMaterialAttributes` for PBR)

Most tutorial UE5.4 materials auto-upgrade. Custom materials using `MakeMaterialAttributes` need manual conversion.

## Tool Ecosystem

### Understand-Anything Knowledge Graph

Generate an interactive project knowledge graph for AI agents:
1. Install: `pnpm install -g @understand-anything/core`
2. Run within project directory: `/understand` (in agent) or `understand --source Source/ --lang zh`
3. Output: `.understand-anything/knowledge-graph.json` — file nodes, class/function nodes, import edges
4. Query: `understand-chat`, `understand-explain`, `understand-dashboard` skills

Scanned 95 Source files in ThirdPersonTest, producing 201 nodes + 92 edges across 7 architecture layers.

### opencode MCP Launch Prerequisite

opencode's MCP connection to Unreal Editor requires the agent to be launched FROM the project directory:

```powershell
# ❌ MCP won't connect
C:\> opencode

# ✅ MCP connects (needs .mcp.json at working dir)
C:\Users\22410\Desktop\UE-Test\ThirdPersonTest> opencode
```

The `.mcp.json` at the project root (generated by `UnrealMCP` plugin's `GenerateClientConfig`) is only discovered when opencode starts in that directory.

---

## Maintaining This Skill

Update when:
- User reports a recurring UE bug pattern → add to relevant Pitfalls section
- A non-obvious UE behaviour is discovered → document
- New UE version introduces breaking changes → update version notes
- User workflow reveals a missing concept → add section
- Returning to a project → add/update entries in the Project Knowledge Board above
