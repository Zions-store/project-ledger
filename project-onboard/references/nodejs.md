---
schema_version: 1
id: nodejs
display_name: Node.js / Frontend
priority: 80
kind: normal
aliases: [node, js, ts, javascript, typescript]

signatures:
  any:
    - package.json

exclusions:
  all:
    - Assets/
    - ProjectSettings/

refinements: []

workspace_files:
  - pnpm-workspace.yaml
  - nx.json
  - turbo.json
  - rush.json

priority_files:
  - package.json
  - tsconfig.json
  - README.md

entry_point_patterns:
  - '"main":'
  - '"start":'
  - 'app.listen'
  - 'express[[:space:]]*\('

external_reference_mechanisms:
  - "file:../shared"
  - "link:../lib"

generated_paths:
  - dist/
  - .next/
  - build/

large_structured_files:
  - package-lock.json
  - pnpm-lock.yaml

binary_asset_types: []

default_ignore_paths:
  - node_modules/
  - dist/
  - .next/
  - build/
  - coverage/

known_blind_spots:
  - runtime module resolution
  - dynamic imports

optional_output_sections:
  - Package Manager
  - Workspace Graph
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Node.js / Frontend Project Analysis Rules

## Signature Detection
- `package.json` exists
- Excluded if both `Assets/` AND `ProjectSettings/` exist (to distinguish from Unity)

## Scan Steps

### 1. Read package.json
```bash
read package.json
```
Extract:
- `name`, `version`, `description`
- `scripts` ->build, dev, start, test commands
- `dependencies` ->key frameworks:
  - `react`, `next`, `vue`, `svelte`, `angular` ->frontend framework
  - `express`, `fastify`, `koa`, `hapi` ->Node.js server
  - `tailwindcss`, `bootstrap`, `chakra-ui` ->CSS framework
  - `prisma`, `typeorm`, `drizzle-orm` ->ORM
  - `typescript` ->TypeScript project
  - `vite`, `webpack`, `esbuild` ->bundler
  - `jest`, `vitest`, `mocha` ->test framework
- `devDependencies` ->development/build tools (may include `typescript`, `vite`, `jest`, `eslint`, `prettier`)

### 2. Detect Project Type
| Clues | Type |
|---|---|
| `next` in deps | Next.js (full-stack or frontend) |
| `react` but no `next` | React SPA |
| `vue` or `nuxt` | Vue.js |
| `express` or `fastify` | Node.js API server |
| `vite` as devDep | Vite-based (likely React/Vue) |
| `astro` | Astro static site |
| `"type": "module"` | ESM project |

### 3. Map Directory Structure
Common patterns to look for:
| Directory | Common Role |
|---|---|
| `src/` | Main source code |
| `app/` | Next.js App Router pages |
| `pages/` | Next.js Pages Router or route files |
| `components/` | Reusable UI components |
| `lib/` or `utils/` | Utility functions |
| `api/` or `routes/` | API endpoints |
| `public/` | Static assets |
| `styles/` | CSS/SCSS files |
| `prisma/` | Database schema |
| `tests/` or `__tests__/` | Test files |

### 4. Find Entry Points
```bash
grep "start\|dev\|build" in package.json scripts section
```
Find the actual entry file:
- Next.js: `app/layout.tsx` or `pages/_app.tsx`
- Express: `grep "app.listen" in src/` or `grep "express()" in src/`
- Vite: `index.html` in root
- General: `glob **/index.{ts,js,tsx,jsx}` in src/

### 5. Build & Run Commands
Extract from `package.json` scripts:
- **Install**: `npm install` / `yarn` / `pnpm install`
- **Dev**: Check `dev` or `start` script (e.g., `vite`, `next dev`, `nodemon`)
- **Build**: Check `build` script
- **Test**: Check `test` script (e.g., `jest`, `vitest`, `mocha`)
- **Lint**: Check `lint` script

### 6. Check for Config Files
- `tsconfig.json` ->TypeScript configuration
- `tailwind.config.*` ->Tailwind CSS
- `.eslintrc.*` ->Linting rules
- `.prettierrc` ->Code formatting
- `.env.example` ->Required environment variables
- `Dockerfile` ->Container deployment
- `docker-compose.yml` ->Multi-service setup
