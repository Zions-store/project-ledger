Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# MonoGame Project Analysis Rules

## Signature Detection

MonoGame is a sub-type of C# that requires reading file contents (the top-level
`glob *` scan in SKILL.md Step 2 cannot see it). Detect it **after** a project
has matched `csharp`:

- Any `*.csproj` contains a `PackageReference` to `MonoGame.Framework.*`
  (e.g. `MonoGame.Framework.DesktopGL`, `MonoGame.Framework.WindowsDX`,
  `MonoGame.Framework.Android`, `MonoGame.Framework.iOS`), **or**
- A MonoGame Content Builder file exists: `**/*.mgcb`

If either holds, use this rule pack instead of `csharp.md`.

> Not Unity: MonoGame projects have **no** `Assets/` + `ProjectSettings/`.
> Not a generic C# app: there is no ASP.NET/WPF/WinForms/MAUI SDK — the entry
> point runs a `Game` loop.

## Scan Steps

### 1. Read Project File(s)
```bash
read *.csproj
```
Extract:
- `<TargetFramework>` — .NET version (net8.0, net9.0, ...)
- `<OutputType>` — usually `WinExe` (desktop) or `Exe`
- `MonoGame.Framework.*` package → **backend variant**:
  - `DesktopGL` → cross-platform OpenGL (Windows/macOS/Linux)
  - `WindowsDX` → Windows-only DirectX
  - `Android` / `iOS` → mobile
- `MonoGame.Content.Builder.Task` → content pipeline auto-builds at compile time
- MonoGame version (e.g. `3.8.*`)

If multiple `*.csproj` exist (per-platform variants), note the shared code
project vs the platform head projects.

### 2. Read the Content Pipeline
```bash
read Content/Content.mgcb   (or glob **/*.mgcb)
```
Extract:
- `/platform:` line (DesktopGL / Windows / Android / iOS)
- `/profile:` line (Reach / HiDef)
- Listed content items (textures, fonts, audio, effects) and their processors.
  An empty References/Content section means no assets imported yet.

### 3. Find Entry Point
```bash
grep "new .*Game" Program.cs   or   read Program.cs
```
Typical entry: `Program.cs` → `using var game = new <Ns>.Game1(); game.Run();`
The `Game` subclass (often `Game1`) is the real starting point.

### 4. Find the Game Class & Lifecycle
```bash
grep "class .* : Game" *.cs
```
Read the `Game` subclass and extract the MonoGame lifecycle:
- Constructor — `GraphicsDeviceManager`, `Content.RootDirectory`, `IsMouseVisible`
- `Initialize()` — one-time setup
- `LoadContent()` — create `SpriteBatch`, load assets via `Content.Load<T>()`
- `Update(GameTime)` — per-frame logic & input (Keyboard/GamePad/Mouse)
- `Draw(GameTime)` — per-frame rendering (`GraphicsDevice.Clear`, `SpriteBatch`)

### 5. Identify Rendering Dimension
- **2D**: uses `SpriteBatch`, `Texture2D`, `SpriteFont`
- **3D**: uses `BasicEffect`/custom `Effect`, `Model`, `VertexBuffer`,
  world/view/projection `Matrix`

### 6. Identify Architecture Patterns
- Single `Game` class holding all logic — minimal / prototype
- Screen/state machine — look for `ScreenManager`, `GameScreen`
- Component pattern — `GameComponent` / `DrawableGameComponent`
- Entity systems — custom ECS

### 7. Build & Run Commands
- **Build**: `dotnet build`
- **Run**: `dotnet run`
- **Publish**: `dotnet publish -c Release`
- **Content**: built automatically by `MonoGame.Content.Builder.Task`; edited
  via MGCB Editor (`mgcb-editor`) opening `Content/Content.mgcb`.
- **Open in IDE**: double-click the `.sln` (VS2022). MonoGame has **no**
  dedicated editor — development is code-first in the `Game` subclass.

## AGENTS.md Additions for MonoGame
Include:
- Backend variant (DesktopGL / WindowsDX / Android / iOS) and whether the
  project has multiple per-platform heads
- MonoGame version + TargetFramework
- Content pipeline status (imported assets, or "empty — none yet")
- 2D vs 3D (SpriteBatch vs BasicEffect/Model)
- Reminder: code-first framework, no visual editor; assets must be compiled to
  `.xnb` through the content pipeline before `Content.Load<T>()`.
