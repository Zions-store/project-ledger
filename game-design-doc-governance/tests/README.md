Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later
# Tests

Regression fixtures and expected baselines for the generic auditor.

## expected/current_project_baseline.json

The known-good audit result of the first real project (the origin
`open_world_narrative_tactical_shooter` project). After any change to
`tools/global_doc_audit.py` or a profile, the auditor must still reproduce these
counts. The P3 message text may change slightly, but the issue must be equivalent.

Baseline: `P0=0 P1=0 P2=0 P3=1 INFO=0`
(single P3 = `RULE-NAMING-FACT-BOUNDARY: RULE anchor has no REF`).

## Running the regression

Point `--root` / `--style` at a project's `md file/` and STYLE, `--profile` at the
matching genre profile, and `--baseline` at the expected JSON:

```
python ../tools/global_doc_audit.py \
  --root    "<origin project>/Design Document/md file" \
  --style    "<origin project>/Design Document/md file/STYLE_GUIDE.md" \
  --profile  "../profiles/open_world_narrative_tactical_shooter.yaml" \
  --out      "<temp audit dir>" \
  --baseline "expected/current_project_baseline.json" \
  --no-state
```

Expected tail: `Baseline compare: EQUIVALENT`.

For baseline regression, use a fresh output directory or pass `--no-state`. This
prevents a prior `issue_state.jsonl` suppression from changing the expected P3 count.

## fixtures/

Reserved for a self-contained, sanitized fixture project (P2), so the regression
can run without depending on an external project path.
