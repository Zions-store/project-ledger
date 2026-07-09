Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# Tests

Regression fixtures and expected baselines for the generic auditor.

## Primary regression — self-contained fixture (no external dependency)

`fixtures/sample_open_world/` is a **sanitized, self-contained** design-doc set
(no real project lore). It is the primary regression source: it does not depend on
any external/real project path, which is required for release (1.0). It also uses
`<!-- AUDIT: … -->` markers, so it additionally covers the language-independent
STYLE-parsing path.

Baseline: `expected/sample_fixture_baseline.json` → `P0=0 P1=0 P2=0 P3=1 INFO=0`
(single P3 = `RULE-SAMPLE-ONLY: RULE anchor has no REF`).

```
python ../tools/global_doc_audit.py \
  --root     "fixtures/sample_open_world/md file" \
  --style    "fixtures/sample_open_world/md file/STYLE_GUIDE.md" \
  --profile  "fixtures/sample_open_world/md file/Project_Profile.yaml" \
  --out      "<temp audit dir>" \
  --baseline "expected/sample_fixture_baseline.json" \
  --no-state
```

Expected tail: `Baseline compare: EQUIVALENT`.

## Secondary regression — origin project (optional, real-world)

`expected/current_project_baseline.json` is the known-good audit of the first real
project (the origin `open_world_narrative_tactical_shooter` project). Useful as a
real-world sanity check, but **not** required to be present for the primary
regression above.

Baseline: `P0=0 P1=0 P2=0 P3=1 INFO=0`
(single P3 = `RULE-NAMING-FACT-BOUNDARY: RULE anchor has no REF`).

```
python ../tools/global_doc_audit.py \
  --root     "<origin project>/Design Document/md file" \
  --style    "<origin project>/Design Document/md file/STYLE_GUIDE.md" \
  --profile  "../profiles/open_world_narrative_tactical_shooter.yaml" \
  --out      "<temp audit dir>" \
  --baseline "expected/current_project_baseline.json" \
  --no-state
```

## Notes

For baseline regression, use a fresh output directory or pass `--no-state`. This
prevents a prior `issue_state.jsonl` suppression from changing the expected P3 count.

## fixtures/sample_open_world/

```
md file/
  Design_Document.md      # index; carries FACT-SAMPLE-ORIGIN (auth) + RULE-SAMPLE-ONLY (auth)
  Gameplay_Systems.md     # carries REF: FACT-SAMPLE-ORIGIN
  Naming.md
  STYLE_GUIDE.md          # AUDIT-marker registries (enabled docs / anchors / deprecated)
  Project_Profile.yaml    # enabled_docs + one boundary + one consistency (crafted to 0 hits)
```

The single expected P3 comes from `RULE-SAMPLE-ONLY` being registered with an
authority occurrence but no `REF:` — the deterministic, sanitized analogue of the
origin project's `RULE-NAMING-FACT-BOUNDARY`.
