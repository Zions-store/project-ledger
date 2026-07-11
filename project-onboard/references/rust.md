---
schema_version: 1
id: rust
display_name: Rust
priority: 70
kind: normal
aliases: [rs]

signatures:
  any:
    - Cargo.toml

exclusions:
  any: []

refinements: []

workspace_files:
  - Cargo.toml

priority_files:
  - Cargo.toml
  - src/main.rs
  - src/lib.rs

entry_point_patterns:
  - 'fn main()'
  - 'pub fn'
  - 'mod '

external_reference_mechanisms:
  - "path = ../"
  - "[patch]"

generated_paths:
  - target/

large_structured_files:
  - Cargo.lock

binary_asset_types: []

default_ignore_paths:
  - target/

known_blind_spots:
  - proc-macro expansion
  - build.rs output

optional_output_sections:
  - Crate Graph
  - Feature Matrix
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Rust Project Analysis Rules

## Signature Detection
- `Cargo.toml` exists

## Scan Steps

### 1. Read Cargo.toml
Extract:
- `[package]` ->`name`, `version`, `description`, `edition`
- `[dependencies]` ->Key crates to identify:
  - `tokio` ->Async runtime
  - `actix-web`, `axum`, `warp`, `rocket` ->Web framework
  - `serde`, `serde_json` ->Serialization
  - `diesel`, `sqlx`, `sea-orm` ->ORM/database
  - `clap`, `structopt` ->CLI tool
  - `bevy`, `amethyst` ->Game engine
  - `wgpu`, `vulkano`, `glium` ->Graphics
  - `egui`, `iced`, `druid` ->GUI
  - `reqwest`, `hyper` ->HTTP client/server
  - `wasm-bindgen` ->WebAssembly target
  - `pyo3`, `napi` ->Language bindings
- `[dev-dependencies]` ->Test frameworks (note `proptest`, `criterion`)
- `[features]` ->Feature flags (important for conditional compilation)
- `[workspace]` ->If present, this is a monorepo workspace root

### 2. Determine Crate Type
Check `[lib]` and `[[bin]]` sections:
| Pattern | Type |
|---|---|
| Both `[[bin]]` and `[lib]` | Library + CLI tool(s) |
| Only `[lib]` | Library crate |
| Only `[[bin]]` | Binary application |
| No explicit target | Default: `src/main.rs` = binary, `src/lib.rs` = library |

### 3. Map Directory Structure
| Directory | Common Role |
|---|---|
| `src/` | Source code (flat or module tree) |
| `src/bin/` | Multiple binary targets (each a `.rs`) |
| `tests/` | Integration tests |
| `examples/` | Example usage |
| `benches/` | Benchmarks |
| `crates/` or `members/` | Workspace member crates (monorepo) |

### 4. Find Entry Points
```bash
glob src/main.rs          ->main binary entry
glob src/lib.rs            ->library entry
glob src/bin/*.rs          ->additional binaries
```
Read `src/main.rs` or `src/lib.rs` first 50 lines for the module tree (`mod X;` declarations).

### 5. Identify Architecture
- Module structure: `mod` declarations tell you the code organization
- Trait-heavy? ->Look for `pub trait` in files (interface-driven design)
- Pattern: `impl` blocks, feature-gated code (`#[cfg(feature = "...")]`)
- Builder pattern common: look for `struct FooBuilder`

### 6. Check Config Files
- `.cargo/config.toml` ->Build config, target settings
- `rust-toolchain.toml` ->Toolchain version
- `rustfmt.toml` ->Format rules
- `clippy.toml` ->Lint rules
- `.env.example` ->Environment variables
- `Dockerfile` ->Container deployment

### 7. Build & Test Commands
- Build: `cargo build` (debug) / `cargo build --release`
- Run: `cargo run` (or `cargo run --bin <name>` for multi-binary)
- Test: `cargo test`
- Lint: `cargo clippy`
- Format: `cargo fmt`
