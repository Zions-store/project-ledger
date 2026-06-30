Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# C/C++ Project Analysis Rules

## Signature Detection
- `CMakeLists.txt` or `Makefile` exists at root
- `.cpp` / `.c` / `.h` / `.hpp` files present

## Scan Steps

### 1. Read Build System

**CMake (CMakeLists.txt)** â€?preferred, most common:
- `cmake_minimum_required(VERSION ...)` â†?CMake version
- `project(<name> VERSION ... LANGUAGES CXX C)` â†?Project identity
- `add_executable(...)` â†?Binary targets
- `add_library(...)` â†?Library targets
- `find_package(...)` â†?External dependencies. Key packages:
  - `Qt5` / `Qt6` â†?Qt GUI framework
  - `OpenGL`, `Vulkan`, `SDL2`, `GLFW` â†?Graphics/game
  - `Boost`, `OpenCV`, `Eigen` â†?Scientific/compute
  - `protobuf`, `gRPC` â†?API/RPC
  - `CURL`, `OpenSSL` â†?Networking
  - `Doxygen` â†?Documentation generator
- `target_link_libraries(...)` â†?Which libs link to what

**Makefile** â€?simpler, less structured:
- Look for `CC`, `CXX`, `CFLAGS`, `LDFLAGS`
- `all:` target â†?what gets built by default

### 2. Determine Project Type
| Clues | Type |
|---|---|
| `QApplication` or `QWidget` in source | Qt application |
| `glfw`, `glad`, `glew`, `sdl` dependency | Graphics/game |
| `main()` with `while(running)` loop | Game engine or real-time app |
| `WinMain` for Windows | Windows native app |
| `src/` + `include/` layout | Library |
| CLI-only with no GUI deps | Command-line tool |
| Embedded build tool (PlatformIO, Arduino) | Embedded firmware |
| `vulkan` or `opengl` dependency | Graphics engine |
| CUDA in CMake (`find_package(CUDA)`) | GPU compute |

### 3. Map Directory Structure
Common C++ project layouts:

**Classic (many projects):**
```
src/          â†?Source files (.cpp, .c)
include/      â†?Public headers (.h, .hpp)
lib/          â†?External libraries
test/         â†?Test code
build/        â†?Build output (ignore for analysis)
third_party/  â†?Vendored dependencies
docs/         â†?Documentation
```

**Modern CMake (header-only or module):**
```
libs/<name>/
  include/<name>/  â†?Public headers
  src/              â†?Implementation
  CMakeLists.txt    â†?Library build
apps/<name>/
  src/              â†?Application
  CMakeLists.txt    â†?App build
```

**Game/Graphics engine:**
```
Source/        â†?Engine core
Editor/        â†?Editor code (separate target)
Shaders/       â†?GLSL/HLSL files
Assets/        â†?Game assets
Config/        â†?Engine config
```

### 4. Find Entry Points
```bash
grep "int main(" in src/ or *.cpp *.c
```
```bash
grep "WinMain" in src/ or *.cpp  (Windows)
```
For Qt: look for `QApplication` + `exec()` call.

### 5. Identify Architecture
- **Object-oriented**: Class hierarchies, virtual functions, inheritance
- **Data-oriented (ECS)**: Entity/Component/System pattern, small POD structs
- **Procedural**: Flat functions, structs without methods (common in C)
- **RAII pattern**: Smart pointers (`unique_ptr`, `shared_ptr`), constructors/destructors
- **Singleton**: `static` local or Meyer's singleton pattern
- **Observer pattern**: Callback lists, signals/slots (especially Qt)

### 6. Check Config Files
- `.clang-format` â†?Code formatting rules
- `.clang-tidy` â†?Static analysis rules
- `Doxyfile` â†?Documentation config
- `conanfile.txt` or `vcpkg.json` â†?Package manager
- `.github/workflows/` â†?CI configuration
- `.editorconfig` â†?Editor settings

### 7. Build & Test Commands
**CMake:**
```bash
mkdir build && cd build
cmake ..
cmake --build .           # or make (on Linux/Mac)
ctest                     # run tests
```

**Makefile:**
```bash
make          # build
make test     # test (if target exists)
make clean    # clean
```

**Cross-platform note**: Build commands differ on Windows (Visual Studio/MSBuild) vs Linux/Mac (make/ninja). Ask the user for their build setup if CMake isn't clear.

### 8. Identify Headers vs Sources
C/C++ typically separates declaration (`.h`/`.hpp`) from implementation (`.c`/`.cpp`). This is important for the AI agent to know when analyzing the codebase:
- Read headers to understand the API contract
- Read sources to understand implementation details
- `.cppm` files â†?C++20 modules (new, less common)
